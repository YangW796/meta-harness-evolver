from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
import pandas as pd


def _norm_col(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def _normalized_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [_norm_col(c) for c in out.columns]
    return out


def _common_numeric_features(p_df: pd.DataFrame, u_df: pd.DataFrame) -> list[str]:
    p_num = {c for c in p_df.columns if pd.api.types.is_numeric_dtype(p_df[c])}
    u_num = {c for c in u_df.columns if pd.api.types.is_numeric_dtype(u_df[c])}
    common = sorted(p_num & u_num)
    return [c for c in common if c not in {"name", "seq", "design", "5design"}]


@dataclass
class Scorer:
    feature_cols: list[str]
    medians: np.ndarray
    means: np.ndarray
    inv_stds: np.ndarray

    def score_u(self, u_df: pd.DataFrame) -> np.ndarray:
        x = u_df.reindex(columns=self.feature_cols)
        x_num = np.column_stack([pd.to_numeric(x[c], errors="coerce").to_numpy(dtype=float) for c in self.feature_cols])
        x_num = np.where(np.isfinite(x_num), x_num, np.nan)
        x_num = np.where(np.isnan(x_num), self.medians[None, :], x_num)
        z = (x_num - self.means[None, :]) * self.inv_stds[None, :]
        d2 = np.mean(z * z, axis=1)
        scores = -d2
        scores = np.asarray(scores, dtype=float)
        scores[~np.isfinite(scores)] = float("-inf")
        return scores


def fit(p_df: pd.DataFrame, u_df: pd.DataFrame | None = None, seed: int = 42) -> Scorer:
    p = _normalized_df(p_df)
    u = _normalized_df(u_df) if u_df is not None else p.iloc[:0].copy()
    feature_cols = _common_numeric_features(p, u) if len(u.columns) else [
        c for c in p.columns if pd.api.types.is_numeric_dtype(p[c]) and c not in {"name", "seq"}
    ]
    if not feature_cols:
        raise ValueError("No usable numeric feature columns found in P/U.")

    x_p = p.reindex(columns=feature_cols)
    x_num = np.column_stack([pd.to_numeric(x_p[c], errors="coerce").to_numpy(dtype=float) for c in feature_cols])
    x_num = np.where(np.isfinite(x_num), x_num, np.nan)

    medians = np.nanmedian(x_num, axis=0)
    x_imp = np.where(np.isnan(x_num), medians[None, :], x_num)
    means = np.mean(x_imp, axis=0)
    stds = np.std(x_imp, axis=0)
    inv_stds = 1.0 / np.maximum(stds, 1e-8)

    return Scorer(feature_cols=feature_cols, medians=medians, means=means, inv_stds=inv_stds)


def score_u(p_df: pd.DataFrame, u_df: pd.DataFrame, seed: int = 42) -> np.ndarray:
    scorer = fit(p_df=p_df, u_df=u_df, seed=seed)
    u = _normalized_df(u_df)
    return scorer.score_u(u)

