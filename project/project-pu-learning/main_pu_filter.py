from __future__ import annotations

import argparse
import importlib.util
import json
import math
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


def _common_numeric_features(p: pd.DataFrame, u: pd.DataFrame) -> list[str]:
    p_num = {c for c in p.columns if pd.api.types.is_numeric_dtype(p[c])}
    u_num = {c for c in u.columns if pd.api.types.is_numeric_dtype(u[c])}
    common = sorted(p_num & u_num)
    return [c for c in common if c not in {"name", "seq", "design", "5design"}]


def _safe_float(v: object) -> float | None:
    try:
        x = float(v)
    except Exception:
        return None
    if not np.isfinite(x):
        return None
    return x


def _split_indices(n: int, test_ratio: float, test_n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    n = int(n)
    if n <= 0:
        return np.asarray([], dtype=int), np.asarray([], dtype=int)
    if int(test_n) > 0:
        k = int(test_n)
    else:
        r = float(test_ratio)
        r = 0.0 if not np.isfinite(r) else max(0.0, min(1.0, r))
        k = int(round(n * r))
    k = int(max(0, min(k, n)))
    if n >= 2:
        k = int(max(1, min(k, n - 1)))
    else:
        k = int(min(k, n))
    rng = np.random.RandomState(int(seed))
    perm = rng.permutation(n).astype(int)
    test_idx = perm[:k]
    train_idx = perm[k:]
    return train_idx, test_idx


def _prf1_from_counts(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    tp = int(tp)
    fp = int(fp)
    fn = int(fn)
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def _eval_topk(scores: np.ndarray, y_true: np.ndarray, k: int) -> dict[str, object]:
    scores = np.asarray(scores, dtype=float).reshape(-1)
    y_true = np.asarray(y_true, dtype=int).reshape(-1)
    n = int(scores.shape[0])
    k = int(max(0, min(int(k), n)))
    if n == 0 or k == 0:
        return {"k": k, "tp": 0, "fp": 0, "fn": int(np.sum(y_true == 1)), "precision": 0.0, "recall": 0.0, "f1": 0.0}
    order = np.argsort(scores, kind="mergesort")[::-1]
    pred_pos = np.zeros(n, dtype=bool)
    pred_pos[order[:k]] = True
    tp = int(np.sum((y_true == 1) & pred_pos))
    fp = int(np.sum((y_true == 0) & pred_pos))
    fn = int(np.sum((y_true == 1) & (~pred_pos)))
    p, r, f1 = _prf1_from_counts(tp, fp, fn)
    return {"k": k, "tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f1}


def _eval_threshold(scores: np.ndarray, y_true: np.ndarray, threshold: float) -> dict[str, object]:
    scores = np.asarray(scores, dtype=float).reshape(-1)
    y_true = np.asarray(y_true, dtype=int).reshape(-1)
    pred_pos = scores >= float(threshold)
    tp = int(np.sum((y_true == 1) & pred_pos))
    fp = int(np.sum((y_true == 0) & pred_pos))
    fn = int(np.sum((y_true == 1) & (~pred_pos)))
    p, r, f1 = _prf1_from_counts(tp, fp, fn)
    return {"threshold": float(threshold), "tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f1}


def _eval_maxf1(scores: np.ndarray, y_true: np.ndarray) -> dict[str, object]:
    scores = np.asarray(scores, dtype=float).reshape(-1)
    y_true = np.asarray(y_true, dtype=int).reshape(-1)
    n = int(scores.shape[0])
    if n == 0:
        return {"best_k": 0, "best_f1": 0.0, "best_precision": 0.0, "best_recall": 0.0}
    order = np.argsort(scores, kind="mergesort")[::-1]
    y_sorted = y_true[order]
    tp_cum = np.cumsum(y_sorted == 1)
    fp_cum = np.cumsum(y_sorted == 0)
    total_pos = int(np.sum(y_true == 1))
    best = {"best_k": 0, "best_f1": 0.0, "best_precision": 0.0, "best_recall": 0.0}
    for k in range(1, n + 1):
        tp = int(tp_cum[k - 1])
        fp = int(fp_cum[k - 1])
        fn = int(total_pos - tp)
        p, r, f1 = _prf1_from_counts(tp, fp, fn)
        if f1 > float(best["best_f1"]):
            best = {"best_k": int(k), "best_f1": float(f1), "best_precision": float(p), "best_recall": float(r)}
    return best


def _default_fit(p_train: pd.DataFrame, u_df: pd.DataFrame) -> tuple[list[str], np.ndarray, np.ndarray]:
    p = _normalized_df(p_train)
    u = _normalized_df(u_df)
    feature_cols = _common_numeric_features(p, u)
    if not feature_cols:
        feature_cols = [c for c in p.columns if pd.api.types.is_numeric_dtype(p[c]) and c not in {"name", "seq"}]
        feature_cols = [c for c in feature_cols if c in u.columns and pd.api.types.is_numeric_dtype(u[c])]
    if not feature_cols:
        raise ValueError("No usable numeric feature columns found in P_train/U for default model.")
    x_p = p.reindex(columns=feature_cols)
    x_p_num = np.column_stack([pd.to_numeric(x_p[c], errors="coerce").to_numpy(dtype=float) for c in feature_cols])
    x_p_num = np.where(np.isfinite(x_p_num), x_p_num, np.nan)
    center = np.nanmedian(x_p_num, axis=0)
    abs_dev = np.abs(x_p_num - center[None, :])
    mad = np.nanmedian(abs_dev, axis=0)
    scale = np.maximum(mad * 1.4826, 1e-8)
    return feature_cols, center, scale


def _default_score_any(x_df: pd.DataFrame, feature_cols: list[str], center: np.ndarray, scale: np.ndarray) -> np.ndarray:
    x = _normalized_df(x_df).reindex(columns=feature_cols)
    x_num = np.column_stack([pd.to_numeric(x[c], errors="coerce").to_numpy(dtype=float) for c in feature_cols])
    x_num = np.where(np.isfinite(x_num), x_num, np.nan)
    x_imp = np.where(np.isnan(x_num), center[None, :], x_num)
    z = (x_imp - center[None, :]) / scale[None, :]
    d2 = np.mean(z * z, axis=1)
    scores = -d2
    scores = np.asarray(scores, dtype=float).reshape(-1)
    scores[~np.isfinite(scores)] = float("-inf")
    return scores


def _load_backend(model_path: Path | None, p_train: pd.DataFrame, u_df: pd.DataFrame, seed: int):
    if model_path is None:
        feature_cols, center, scale = _default_fit(p_train, u_df)
        return ("default", {"feature_cols": feature_cols}, lambda df: _default_score_any(df, feature_cols, center, scale))

    module = _load_model_module(model_path)

    fit_fn = getattr(module, "fit", None)
    if callable(fit_fn):
        last_err: Exception | None = None
        for kwargs in (
            {"p_df": p_train, "u_df": u_df, "seed": int(seed)},
            {"p_train_df": p_train, "u_df": u_df, "seed": int(seed)},
            {"p_df": p_train, "u_df": u_df},
            {"p_train_df": p_train, "u_df": u_df},
        ):
            try:
                scorer = fit_fn(**kwargs)
                break
            except Exception as e:
                last_err = e
                scorer = None
        if scorer is None:
            raise RuntimeError(f"fit(...) failed: {last_err}")
        for attr in ["score", "score_df", "score_x", "predict", "predict_score"]:
            m = getattr(scorer, attr, None)
            if callable(m):
                def _score_any(df: pd.DataFrame, _m=m) -> np.ndarray:
                    out = _m(df)
                    out = np.asarray(out, dtype=float).reshape(-1)
                    if out.shape[0] != df.shape[0]:
                        raise ValueError(f"scorer.{attr} returned {out.shape[0]} scores, but X has {df.shape[0]} rows")
                    out[~np.isfinite(out)] = float("-inf")
                    return out
                return ("custom_fit", {}, _score_any)
        raise ValueError("fit(...) must return an object with score(x_df)->np.ndarray (or score_df/score_x/predict).")

    score_x_fn = getattr(module, "score_x", None)
    if callable(score_x_fn):
        def _score_any(df: pd.DataFrame) -> np.ndarray:
            last_err: Exception | None = None
            for kwargs in (
                {"p_df": p_train, "u_df": u_df, "x_df": df, "seed": int(seed)},
                {"p_train_df": p_train, "u_df": u_df, "x_df": df, "seed": int(seed)},
                {"p_df": p_train, "u_df": u_df, "x_df": df},
                {"p_train_df": p_train, "u_df": u_df, "x_df": df},
            ):
                try:
                    out = score_x_fn(**kwargs)
                    out = np.asarray(out, dtype=float).reshape(-1)
                    if out.shape[0] != df.shape[0]:
                        raise ValueError(f"score_x returned {out.shape[0]} scores, but X has {df.shape[0]} rows")
                    out[~np.isfinite(out)] = float("-inf")
                    return out
                except Exception as e:
                    last_err = e
            raise RuntimeError(f"score_x(...) failed: {last_err}")
        return ("custom_score_x", {}, _score_any)

    score_u_fn = getattr(module, "score_u", None)
    if callable(score_u_fn):
        def _score_u(u_df2: pd.DataFrame) -> np.ndarray:
            out = score_u_fn(_normalized_df(p_train), _normalized_df(u_df2), seed=int(seed))
            out = np.asarray(out, dtype=float).reshape(-1)
            if out.shape[0] != u_df2.shape[0]:
                raise ValueError(f"score_u returned {out.shape[0]} scores, but X has {u_df2.shape[0]} rows")
            out[~np.isfinite(out)] = float("-inf")
            return out
        return ("legacy_score_u", {}, lambda df: _score_u(df))

    raise ValueError("model.py must define fit(...) or score_x(...) or score_u(p_df, u_df, seed=42).")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p_csv", type=str, required=True)
    parser.add_argument("--u_csv", type=str, required=True)
    parser.add_argument("--candidate_dir", type=str, required=True)
    parser.add_argument("--model_path", type=str, default="")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--test_n", type=int, default=0)
    parser.add_argument("--metric_mode", type=str, default="topk")
    parser.add_argument("--topk_k", type=int, default=0)
    parser.add_argument("--threshold", type=str, default="")
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

    train_idx, test_idx = _split_indices(int(p_norm.shape[0]), float(args.test_ratio), int(args.test_n), int(args.seed))
    p_train_norm = p_norm.iloc[train_idx].copy()
    p_test_norm = p_norm.iloc[test_idx].copy()
    p_train_raw = p_raw.iloc[train_idx].copy()
    p_test_raw = p_raw.iloc[test_idx].copy()

    out_dir = candidate_dir / "harness" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_kind, model_meta, score_any = _load_backend(model_path, p_train=p_train_norm, u_df=u_norm, seed=int(args.seed))

    u_scores = score_any(u_norm)

    if model_kind == "legacy_score_u":
        p_test_scores_list: list[float] = []
        for i in range(int(p_test_norm.shape[0])):
            s1 = score_any(p_test_norm.iloc[[i]])
            p_test_scores_list.append(float(s1[0]) if s1.size else float("-inf"))
        p_test_scores = np.asarray(p_test_scores_list, dtype=float)
    else:
        p_test_scores = score_any(p_test_norm)

    scores = np.concatenate([p_test_scores, u_scores], axis=0).astype(float, copy=False)
    scores[~np.isfinite(scores)] = float("-inf")
    y_true = np.concatenate([np.ones(int(p_test_norm.shape[0]), dtype=int), np.zeros(int(u_norm.shape[0]), dtype=int)], axis=0)

    metric_mode = str(args.metric_mode or "topk").strip().lower()
    if metric_mode not in {"topk", "maxf1", "threshold"}:
        raise ValueError(f"Unsupported metric_mode: {metric_mode}")

    eval_out: dict[str, object]
    used_k: int | None = None
    used_threshold: float | None = None
    if metric_mode == "topk":
        k = int(args.topk_k) if int(args.topk_k) > 0 else int(p_test_norm.shape[0])
        used_k = int(max(1, min(k, int(scores.shape[0])))) if int(scores.shape[0]) > 0 else 0
        eval_out = _eval_topk(scores, y_true, k=used_k)
    elif metric_mode == "threshold":
        raw_t = str(args.threshold or "").strip()
        if not raw_t:
            raise ValueError("metric_mode=threshold requires --threshold")
        t = float(raw_t)
        if not math.isfinite(t):
            raise ValueError("threshold must be finite")
        used_threshold = float(t)
        eval_out = _eval_threshold(scores, y_true, threshold=used_threshold)
    else:
        best = _eval_maxf1(scores, y_true)
        used_k = int(best.get("best_k", 0) or 0)
        eval_out = {
            "best_k": used_k,
            "best_precision": float(best.get("best_precision", 0.0) or 0.0),
            "best_recall": float(best.get("best_recall", 0.0) or 0.0),
            "best_f1": float(best.get("best_f1", 0.0) or 0.0),
        }

    if metric_mode != "maxf1":
        best = _eval_maxf1(scores, y_true)
        eval_out["best_k"] = int(best.get("best_k", 0) or 0)
        eval_out["best_precision"] = float(best.get("best_precision", 0.0) or 0.0)
        eval_out["best_recall"] = float(best.get("best_recall", 0.0) or 0.0)
        eval_out["best_f1"] = float(best.get("best_f1", 0.0) or 0.0)

    p_test_ids = (
        [str(x) for x in p_test_norm[p_id_col].tolist()]
        if p_id_col in p_test_norm.columns
        else [str(i) for i in range(int(p_test_norm.shape[0]))]
    )
    u_ids = (
        [str(x) for x in u_norm[u_id_col].tolist()]
        if u_id_col in u_norm.columns
        else [str(i) for i in range(int(u_norm.shape[0]))]
    )

    scores_df = pd.DataFrame(
        {
            "split": (["p_test"] * int(p_test_norm.shape[0])) + (["u"] * int(u_norm.shape[0])),
            "label": y_true.astype(int),
            "id": p_test_ids + u_ids,
            "score": scores.astype(float),
        }
    )
    scores_path = out_dir / "scores_test.csv"
    scores_df.to_csv(scores_path, index=False)

    payload: dict[str, object] = {
        "p_csv": str(p_csv),
        "u_csv": str(u_csv),
        "model_kind": model_kind,
        "model_path": str(model_path) if model_path is not None else "",
        "seed": int(args.seed),
        "p_rows": int(p_norm.shape[0]),
        "p_train_rows": int(p_train_norm.shape[0]),
        "p_test_rows": int(p_test_norm.shape[0]),
        "u_rows": int(u_norm.shape[0]),
        "p_id_col": p_id_col,
        "u_id_col": u_id_col,
        "metric_mode": metric_mode,
        "used_k": used_k,
        "used_threshold": used_threshold,
        "precision": _safe_float(eval_out.get("precision")) if "precision" in eval_out else _safe_float(eval_out.get("best_precision")),
        "recall": _safe_float(eval_out.get("recall")) if "recall" in eval_out else _safe_float(eval_out.get("best_recall")),
        "f1": _safe_float(eval_out.get("f1")) if "f1" in eval_out else _safe_float(eval_out.get("best_f1")),
        "eval": eval_out,
        "model_meta": model_meta,
        "outputs": {"scores_test_csv": str(scores_path)},
    }
    (out_dir / "metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
