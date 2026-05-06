from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
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


def _load_model_module(model_path: Path):
    spec = importlib.util.spec_from_file_location("pu_model_module", str(model_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load model module: {model_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _get_score_fn(model_path: Path | None):
    if model_path is None:
        return None
    module = _load_model_module(model_path)
    fn = getattr(module, "score_u", None)
    if callable(fn):
        return fn
    for cls_name in ["Model", "Scorer"]:
        cls = getattr(module, cls_name, None)
        if cls is None:
            continue
        inst = cls()
        fn2 = getattr(inst, "score_u", None)
        if callable(fn2):
            return lambda p_df, u_df, seed=42: fn2(p_df=p_df, u_df=u_df, seed=seed)
    raise ValueError("model.py must define score_u(p_df, u_df, seed=42) -> np.ndarray or a class with score_u")


def _common_numeric_features(p: pd.DataFrame, u: pd.DataFrame) -> list[str]:
    p_num = {c for c in p.columns if pd.api.types.is_numeric_dtype(p[c])}
    u_num = {c for c in u.columns if pd.api.types.is_numeric_dtype(u[c])}
    common = sorted(p_num & u_num)
    return [c for c in common if c not in {"name", "seq", "design", "5design"}]


def _default_scores(p_df: pd.DataFrame, u_df: pd.DataFrame, seed: int) -> tuple[np.ndarray, list[str]]:
    p = _normalized_df(p_df)
    u = _normalized_df(u_df)
    feature_cols = _common_numeric_features(p, u)
    if not feature_cols:
        feature_cols = [c for c in p.columns if pd.api.types.is_numeric_dtype(p[c]) and c not in {"name", "seq"}]
        feature_cols = [c for c in feature_cols if c in u.columns and pd.api.types.is_numeric_dtype(u[c])]
    if not feature_cols:
        raise ValueError("No usable numeric feature columns found in P/U for default model.")

    x_p = p.reindex(columns=feature_cols)
    x_u = u.reindex(columns=feature_cols)

    x_p_num = np.column_stack([pd.to_numeric(x_p[c], errors="coerce").to_numpy(dtype=float) for c in feature_cols])
    x_u_num = np.column_stack([pd.to_numeric(x_u[c], errors="coerce").to_numpy(dtype=float) for c in feature_cols])
    x_p_num = np.where(np.isfinite(x_p_num), x_p_num, np.nan)
    x_u_num = np.where(np.isfinite(x_u_num), x_u_num, np.nan)

    medians = np.nanmedian(x_p_num, axis=0)
    x_p_imp = np.where(np.isnan(x_p_num), medians[None, :], x_p_num)
    x_u_imp = np.where(np.isnan(x_u_num), medians[None, :], x_u_num)

    means = np.mean(x_p_imp, axis=0)
    stds = np.std(x_p_imp, axis=0)
    inv_stds = 1.0 / np.maximum(stds, 1e-8)

    z = (x_u_imp - means[None, :]) * inv_stds[None, :]
    d2 = np.mean(z * z, axis=1)
    scores = -d2
    scores = np.asarray(scores, dtype=float)
    scores[~np.isfinite(scores)] = float("-inf")
    return scores, feature_cols


def _select_removed(scores: np.ndarray, remove_n: int) -> tuple[np.ndarray, np.ndarray]:
    n = int(scores.shape[0])
    remove_n = int(max(0, min(remove_n, n)))
    if remove_n == 0:
        kept = np.arange(n, dtype=int)
        removed = np.asarray([], dtype=int)
        return kept, removed
    order = np.argsort(scores, kind="mergesort")
    removed = order[:remove_n]
    removed_set = set(int(i) for i in removed.tolist())
    kept = np.asarray([i for i in range(n) if i not in removed_set], dtype=int)
    return kept, removed


def _safe_float(v: object) -> float | None:
    try:
        x = float(v)
    except Exception:
        return None
    if not np.isfinite(x):
        return None
    return x


def _summary_stats(scores: np.ndarray) -> dict[str, float | None]:
    if scores.size == 0:
        return {"min": None, "p25": None, "median": None, "p75": None, "max": None, "mean": None}
    s = scores[np.isfinite(scores)]
    if s.size == 0:
        return {"min": None, "p25": None, "median": None, "p75": None, "max": None, "mean": None}
    return {
        "min": _safe_float(np.min(s)),
        "p25": _safe_float(np.percentile(s, 25)),
        "median": _safe_float(np.median(s)),
        "p75": _safe_float(np.percentile(s, 75)),
        "max": _safe_float(np.max(s)),
        "mean": _safe_float(np.mean(s)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p_csv", type=str, required=True)
    parser.add_argument("--u_csv", type=str, required=True)
    parser.add_argument("--candidate_dir", type=str, required=True)
    parser.add_argument("--model_path", type=str, default="")
    parser.add_argument("--remove_ratio", type=float, default=0.2)
    parser.add_argument("--remove_n", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    p_csv = Path(args.p_csv).expanduser().resolve()
    u_csv = Path(args.u_csv).expanduser().resolve()
    candidate_dir = Path(args.candidate_dir).expanduser().resolve()
    model_path = Path(args.model_path).expanduser().resolve() if args.model_path else None

    if not p_csv.exists():
        raise FileNotFoundError(str(p_csv))
    if not u_csv.exists():
        raise FileNotFoundError(str(u_csv))
    if model_path is not None and not model_path.exists():
        raise FileNotFoundError(str(model_path))

    p_raw = pd.read_csv(p_csv)
    u_raw = pd.read_csv(u_csv)
    p_norm = _normalized_df(p_raw)
    u_norm = _normalized_df(u_raw)

    p_id_col = _guess_id_col(p_norm, preferred=["name", "id"])
    u_id_col = _guess_id_col(u_norm, preferred=["5design", "design", "name", "id"])

    score_fn = _get_score_fn(model_path)
    if score_fn is not None:
        scores = score_fn(p_norm, u_norm, seed=int(args.seed))
        scores = np.asarray(scores, dtype=float).reshape(-1)
        if scores.shape[0] != u_norm.shape[0]:
            raise ValueError(f"score_u returned {scores.shape[0]} scores, but U has {u_norm.shape[0]} rows")
        scores[~np.isfinite(scores)] = float("-inf")
        feature_cols: list[str] = []
        model_kind = "custom"
    else:
        scores, feature_cols = _default_scores(p_norm, u_norm, seed=int(args.seed))
        model_kind = "default"

    n_u = int(u_norm.shape[0])
    if int(args.remove_n) > 0:
        remove_n = int(args.remove_n)
    else:
        ratio = float(args.remove_ratio)
        ratio = 0.0 if not np.isfinite(ratio) else max(0.0, min(1.0, ratio))
        remove_n = int(round(n_u * ratio))
        if ratio > 0.0 and remove_n == 0:
            remove_n = 1

    kept_idx, removed_idx = _select_removed(scores, remove_n=remove_n)

    out_dir = candidate_dir / "harness" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    u_with_scores = u_raw.copy()
    u_with_scores["pu_score_like_p"] = scores

    kept_df = u_with_scores.iloc[kept_idx].copy()
    removed_df = u_with_scores.iloc[removed_idx].copy()

    kept_path = out_dir / "u_kept.csv"
    removed_path = out_dir / "u_removed.csv"
    kept_df.to_csv(kept_path, index=False)
    removed_df.to_csv(removed_path, index=False)

    kept_ids = [str(x) for x in u_norm.iloc[kept_idx][u_id_col].tolist()] if u_id_col in u_norm.columns else []
    removed_ids = [str(x) for x in u_norm.iloc[removed_idx][u_id_col].tolist()] if u_id_col in u_norm.columns else []

    payload = {
        "p_csv": str(p_csv),
        "u_csv": str(u_csv),
        "model_kind": model_kind,
        "model_path": str(model_path) if model_path is not None else "",
        "seed": int(args.seed),
        "p_rows": int(p_norm.shape[0]),
        "u_rows": int(n_u),
        "removed_n": int(removed_idx.shape[0]),
        "kept_n": int(kept_idx.shape[0]),
        "p_id_col": p_id_col,
        "u_id_col": u_id_col,
        "feature_cols": feature_cols,
        "score_stats_all": _summary_stats(scores),
        "score_stats_kept": _summary_stats(scores[kept_idx]),
        "score_stats_removed": _summary_stats(scores[removed_idx]),
        "outputs": {
            "u_kept_csv": str(kept_path),
            "u_removed_csv": str(removed_path),
        },
    }

    selection = {
        "u_id_col": u_id_col,
        "kept": kept_ids,
        "removed": removed_ids,
    }

    (out_dir / "metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "selection.json").write_text(json.dumps(selection, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
