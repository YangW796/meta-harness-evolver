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


def _kmeans2(z: np.ndarray, seed: int, iters: int = 12) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(z, dtype=float)
    n, d = z.shape
    if n == 0:
        return np.zeros((d,), dtype=float), np.zeros((d,), dtype=float)
    if n == 1:
        c = z[0].copy()
        return c, c.copy()
    rng = np.random.default_rng(int(seed))
    i0 = int(rng.integers(0, n))
    c1 = z[i0].copy()
    d2 = np.sum((z - c1[None, :]) ** 2, axis=1)
    i1 = int(np.argmax(d2))
    c2 = z[i1].copy()
    for _ in range(int(max(1, iters))):
        d21 = np.sum((z - c1[None, :]) ** 2, axis=1)
        d22 = np.sum((z - c2[None, :]) ** 2, axis=1)
        a = d21 <= d22
        if np.any(a):
            c1 = np.mean(z[a], axis=0)
        if np.any(~a):
            c2 = np.mean(z[~a], axis=0)
    return np.asarray(c1, dtype=float), np.asarray(c2, dtype=float)


def _feature_weights(z_p: np.ndarray) -> np.ndarray:
    z_p = np.asarray(z_p, dtype=float)
    if z_p.ndim != 2 or z_p.shape[1] == 0:
        return np.zeros((0,), dtype=float)
    m = np.mean(np.tanh(z_p), axis=0)
    w = 0.5 + 0.5 * np.abs(m)
    w = np.asarray(w, dtype=float).reshape(-1)
    w[~np.isfinite(w)] = 1.0
    w = np.maximum(w, 1e-3)
    w = w / float(np.mean(w) + 1e-12)
    return w


def _score_like_p(z_x: np.ndarray, z_p: np.ndarray, seed: int) -> np.ndarray:
    z_x = np.asarray(z_x, dtype=float)
    z_p = np.asarray(z_p, dtype=float)
    n_x, d = z_x.shape
    if n_x == 0:
        return np.zeros((0,), dtype=float)
    if d == 0:
        return np.zeros((n_x,), dtype=float)

    c1, c2 = _kmeans2(z_p, seed=int(seed), iters=10)
    w_feat = _feature_weights(z_p)
    x1 = z_x - c1[None, :]
    x2 = z_x - c2[None, :]
    d2_1 = np.sum(x1 * x1 * w_feat[None, :], axis=1)
    d2_2 = np.sum(x2 * x2 * w_feat[None, :], axis=1)
    d2 = np.minimum(d2_1, d2_2)
    d2 = np.where(np.isfinite(d2), d2, float("inf"))
    base = -0.5 * d2

    rng = np.random.default_rng(int(seed) + 17)
    w = rng.normal(size=(d,))
    w = w / (np.linalg.norm(w) + 1e-12)
    proj = (z_x @ w) / np.sqrt(float(d))
    bump = np.tanh(proj)
    w2 = rng.normal(size=(d,))
    w2 = w2 / (np.linalg.norm(w2) + 1e-12)
    proj2 = (z_x @ w2) / np.sqrt(float(d))
    ripple = np.sin(1.1 * proj + 0.7 * np.tanh(proj2))
    sign = np.sign(np.mean(z_p, axis=0))
    align = np.mean(np.tanh(z_x) * sign[None, :], axis=1)
    interaction = np.tanh(proj) * np.sin(1.7 * proj2)

    scores = base + 0.05 * bump + 0.03 * align + 0.02 * ripple + 0.02 * interaction
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

    scores_p = _score_like_p(z_p, z_p, seed=int(args.seed))
    scores_u = _score_like_p(z_u, z_p, seed=int(args.seed))

    u_pos_ratio = float(args.u_positive_ratio)
    u_pos_ratio = 0.0 if not np.isfinite(u_pos_ratio) else max(0.0, min(1.0, u_pos_ratio))
    if scores_u.size == 0:
        threshold = float("inf")
    elif u_pos_ratio <= 0.0:
        threshold = float("inf")
    elif u_pos_ratio >= 1.0:
        threshold = float("-inf")
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
