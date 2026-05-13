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


def _winsorize(z: np.ndarray, limit: float = 6.0) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    z = np.where(np.isfinite(z), z, 0.0)
    lim = float(limit)
    if not np.isfinite(lim) or lim <= 0.0:
        return z
    return np.clip(z, -lim, lim)


def _shrink_inv_cov(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    n, d = z.shape
    if n <= 1 or d <= 0:
        return np.eye(int(d), dtype=float)
    mu = np.mean(z, axis=0)
    x = z - mu[None, :]
    s = (x.T @ x) / float(max(1, n - 1))
    tr = float(np.trace(s))
    if not np.isfinite(tr) or tr <= 0.0:
        s = np.eye(int(d), dtype=float)
        tr = float(d)
    alpha = float(min(0.95, max(0.05, float(d) / float(n + d))))
    cov = (1.0 - alpha) * s + alpha * (tr / float(d)) * np.eye(int(d), dtype=float)
    cov = cov + 1e-8 * np.eye(int(d), dtype=float)
    inv = np.linalg.pinv(cov)
    inv = np.asarray(inv, dtype=float)
    return inv


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


def _score_like_p(z_x: np.ndarray, z_p: np.ndarray, seed: int) -> np.ndarray:
    z_x = np.asarray(z_x, dtype=float)
    z_p = np.asarray(z_p, dtype=float)
    n_x, d = z_x.shape
    if n_x == 0:
        return np.zeros((0,), dtype=float)
    if d == 0:
        return np.zeros((n_x,), dtype=float)

    z_p2 = _winsorize(z_p, limit=6.0)
    z_x2 = _winsorize(z_x, limit=6.0)
    inv_cov = _shrink_inv_cov(z_p2)
    c1, c2 = _kmeans2(z_p2, seed=int(seed), iters=12)

    x1 = z_x2 - c1[None, :]
    x2 = z_x2 - c2[None, :]
    md2_1 = np.einsum("ni,ij,nj->n", x1, inv_cov, x1, optimize=True)
    md2_2 = np.einsum("ni,ij,nj->n", x2, inv_cov, x2, optimize=True)
    md2 = np.minimum(md2_1, md2_2)
    md2 = np.where(np.isfinite(md2), md2, float("inf"))
    base = -0.5 * md2

    rng = np.random.default_rng(int(seed) + 17)
    h = int(min(48, max(12, d)))
    w1 = rng.normal(scale=1.0 / np.sqrt(float(max(1, d))), size=(d, h))
    b1 = rng.normal(scale=0.2, size=(h,))
    w2 = rng.normal(scale=1.0 / np.sqrt(float(max(1, h))), size=(h,))

    t = np.tanh(z_x2 @ w1 + b1[None, :])
    mlp = t @ w2
    mlp = np.asarray(mlp, dtype=float).reshape(-1)

    sign = np.sign(np.mean(np.tanh(z_p2), axis=0))
    align = np.mean(np.tanh(z_x2) * sign[None, :], axis=1)

    proj = rng.normal(size=(d,))
    proj = proj / (np.linalg.norm(proj) + 1e-12)
    p = (z_x2 @ proj) / np.sqrt(float(d))
    ripple = np.sin(1.7 * p + 0.3 * np.tanh(mlp))

    scores = base + 0.08 * mlp + 0.05 * align + 0.03 * ripple
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
