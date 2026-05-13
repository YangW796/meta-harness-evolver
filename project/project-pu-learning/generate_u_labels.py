#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

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


def _guess_id_col(df: pd.DataFrame, preferred: list[str]) -> str:
    cols = list(df.columns)
    for c in preferred:
        if c in cols:
            return c
    return cols[0] if cols else "id"


def _common_numeric_features(p: pd.DataFrame, u: pd.DataFrame) -> list[str]:
    p_num = {c for c in p.columns if pd.api.types.is_numeric_dtype(p[c])}
    u_num = {c for c in u.columns if pd.api.types.is_numeric_dtype(u[c])}
    common = sorted(p_num & u_num)
    return [c for c in common if c not in {"name", "seq", "design", "5design"}]


def _robust_center_scale(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    x = np.where(np.isfinite(x), x, np.nan)
    center = np.nanmedian(x, axis=0)
    abs_dev = np.abs(x - center[None, :])
    mad = np.nanmedian(abs_dev, axis=0)
    scale = np.maximum(mad * 1.4826, 1e-8)
    return center, scale


def _make_oracle_scores(z: np.ndarray, seed: int) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    z = np.where(np.isfinite(z), z, 0.0)
    n, d = z.shape
    if n == 0:
        return np.zeros((0,), dtype=float)
    if d == 0:
        return np.zeros((n,), dtype=float)

    base = -np.mean(z * z, axis=1)
    rng = np.random.default_rng(int(seed))
    w1 = rng.normal(size=(d,))
    w2 = rng.normal(size=(d,))
    w3 = rng.normal(size=(d,))
    w1 = w1 / (np.linalg.norm(w1) + 1e-12)
    w2 = w2 / (np.linalg.norm(w2) + 1e-12)
    w3 = w3 / (np.linalg.norm(w3) + 1e-12)

    p1 = (z @ w1) / np.sqrt(float(d))
    p2 = (z @ w2) / np.sqrt(float(d))
    p3 = (z @ w3) / np.sqrt(float(d))

    t1 = np.tanh(p1)
    t2 = np.sin(1.3 * p2 + 0.7 * np.tanh(p3))
    t3 = np.tanh(np.mean(np.tanh(z), axis=1))

    scores = base + 0.12 * t1 + 0.08 * t2 + 0.05 * t3
    scores = np.asarray(scores, dtype=float).reshape(-1)
    scores[~np.isfinite(scores)] = float("-inf")
    return scores


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p_csv", type=str, required=True)
    parser.add_argument("--u_csv", type=str, required=True)
    parser.add_argument("--out_u_labeled_csv", type=str, required=True)
    parser.add_argument("--label_col", type=str, default="u_label")
    parser.add_argument("--score_col", type=str, default="oracle_score")
    parser.add_argument("--write_score", type=int, default=1)
    parser.add_argument("--u_positive_ratio", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    p_csv = Path(args.p_csv).expanduser().resolve()
    u_csv = Path(args.u_csv).expanduser().resolve()
    out_path = Path(args.out_u_labeled_csv).expanduser().resolve()
    if not p_csv.exists():
        raise FileNotFoundError(str(p_csv))
    if not u_csv.exists():
        raise FileNotFoundError(str(u_csv))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    p_raw = pd.read_csv(p_csv)
    u_raw = pd.read_csv(u_csv)
    p_norm = _normalized_df(p_raw)
    u_norm = _normalized_df(u_raw)

    u_id_col = _guess_id_col(u_norm, preferred=["5design", "design", "name", "id"])
    features = _common_numeric_features(p_norm, u_norm)
    if not features:
        features = [c for c in p_norm.columns if pd.api.types.is_numeric_dtype(p_norm[c]) and c not in {"name", "seq"}]
        features = [c for c in features if c in u_norm.columns and pd.api.types.is_numeric_dtype(u_norm[c])]
    if not features:
        raise ValueError("No usable numeric feature columns found in P/U.")

    x_p = p_norm.reindex(columns=features)
    x_u = u_norm.reindex(columns=features)
    x_p_num = np.column_stack([pd.to_numeric(x_p[c], errors="coerce").to_numpy(dtype=float) for c in features])
    x_u_num = np.column_stack([pd.to_numeric(x_u[c], errors="coerce").to_numpy(dtype=float) for c in features])

    center, scale = _robust_center_scale(x_p_num)
    x_p_imp = np.where(np.isnan(x_p_num), center[None, :], x_p_num)
    x_u_imp = np.where(np.isnan(x_u_num), center[None, :], x_u_num)
    z_p = (x_p_imp - center[None, :]) / scale[None, :]
    z_u = (x_u_imp - center[None, :]) / scale[None, :]

    scores_p = _make_oracle_scores(z_p, seed=int(args.seed))
    scores_u = _make_oracle_scores(z_u, seed=int(args.seed))

    u_pos_ratio = float(args.u_positive_ratio)
    u_pos_ratio = 0.0 if not np.isfinite(u_pos_ratio) else max(0.0, min(1.0, u_pos_ratio))
    if scores_u.size == 0:
        threshold = float("inf")
    elif u_pos_ratio <= 0.0:
        threshold = float("-inf")
    elif u_pos_ratio >= 1.0:
        threshold = float("inf")
    else:
        threshold = float(np.quantile(scores_u, 1.0 - u_pos_ratio))

    if scores_p.size:
        threshold = float(min(threshold, float(np.min(scores_p)) - 1e-12))

    u_label = (scores_u >= threshold).astype(int)

    out_df = u_raw.copy()
    out_df[str(args.label_col)] = u_label.astype(int, copy=False)
    if int(args.write_score) != 0:
        out_df[str(args.score_col)] = scores_u.astype(float, copy=False)
    out_df.to_csv(out_path, index=False)
    print(f"u_id_col={u_id_col} features_n={len(features)} u_pos_ratio={u_pos_ratio} saved={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
