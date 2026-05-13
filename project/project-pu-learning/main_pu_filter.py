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


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _save_state(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p_csv", type=str, required=True)
    parser.add_argument("--u_csv", type=str, required=True)
    parser.add_argument("--u_labeled_csv", type=str, default="")
    parser.add_argument("--u_label_col", type=str, default="u_label")
    parser.add_argument("--candidate_dir", type=str, required=True)
    parser.add_argument("--state_path", type=str, default="")
    parser.add_argument("--model_path", type=str, default="")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--test_n", type=int, default=0)
    parser.add_argument("--metric_mode", type=str, default="topk")
    parser.add_argument("--topk_k", type=int, default=0)
    parser.add_argument("--topk_ratio", type=float, default=0.0)
    parser.add_argument("--threshold", type=str, default="")
    parser.add_argument("--u_bottom_n", type=int, default=0)
    parser.add_argument("--u_bottom_ratio", type=float, default=0.0)
    parser.add_argument("--u_holdout_ratio", type=float, default=0.0)
    parser.add_argument("--u_holdout_n", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--remove_n_per_iter", type=int, default=0)
    parser.add_argument("--remove_ratio_per_iter", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    p_csv = Path(args.p_csv).expanduser().resolve()
    u_csv = Path(args.u_csv).expanduser().resolve()
    u_labeled_csv = Path(args.u_labeled_csv).expanduser().resolve() if args.u_labeled_csv else None
    candidate_dir = Path(args.candidate_dir).expanduser().resolve()
    state_path = Path(args.state_path).expanduser().resolve() if args.state_path else None
    model_path = Path(args.model_path).expanduser().resolve() if args.model_path else None

    if not p_csv.exists():
        raise FileNotFoundError(str(p_csv))
    if not u_csv.exists():
        raise FileNotFoundError(str(u_csv))
    if u_labeled_csv is not None and not u_labeled_csv.exists():
        raise FileNotFoundError(str(u_labeled_csv))
    if model_path is not None and not model_path.exists():
        raise FileNotFoundError(str(model_path))

    p_raw = pd.read_csv(p_csv)
    u_raw = pd.read_csv(u_csv)
    u_labeled_raw = pd.read_csv(u_labeled_csv) if u_labeled_csv is not None else None
    p_norm = _normalized_df(p_raw)
    u_norm = _normalized_df(u_raw)

    p_id_col = _guess_id_col(p_norm, preferred=["name", "id"])
    u_id_col = _guess_id_col(u_norm, preferred=["5design", "design", "name", "id"])

    train_idx, test_idx = _split_indices(int(p_norm.shape[0]), float(args.test_ratio), int(args.test_n), int(args.seed))
    p_train_norm = p_norm.iloc[train_idx].copy()
    p_test_norm = p_norm.iloc[test_idx].copy()
    p_train_raw = p_raw.iloc[train_idx].copy()
    p_test_raw = p_raw.iloc[test_idx].copy()

    out_dir = candidate_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    u_labels_map: dict[str, int] | None = None
    if u_labeled_raw is not None:
        u_lab_norm = _normalized_df(u_labeled_raw)
        u_lab_id_col = _guess_id_col(u_lab_norm, preferred=["5design", "design", "name", "id"])
        lab_col = _norm_col(str(args.u_label_col))
        if lab_col not in u_lab_norm.columns:
            raise ValueError(f"u_labeled_csv missing label column: {args.u_label_col}")
        if u_lab_id_col not in u_lab_norm.columns:
            raise ValueError(f"u_labeled_csv missing id column: {u_lab_id_col}")
        u_labels_map = {}
        ids = u_lab_norm[u_lab_id_col].astype(str).tolist()
        labs = u_lab_norm[lab_col].tolist()
        for _id, _lab in zip(ids, labs):
            try:
                u_labels_map[str(_id)] = 1 if int(float(str(_lab).strip())) != 0 else 0
            except Exception:
                u_labels_map[str(_id)] = 0

    metric_mode = str(args.metric_mode or "topk").strip().lower()
    if metric_mode not in {"topk", "maxf1", "threshold", "u_topk", "u_maxf1", "u_threshold"}:
        raise ValueError(f"Unsupported metric_mode: {metric_mode}")

    iterations = int(max(1, int(args.iterations)))
    remove_n_per_iter_raw = int(max(0, int(args.remove_n_per_iter)))
    remove_ratio_per_iter = float(args.remove_ratio_per_iter)
    remove_ratio_per_iter = 0.0 if not np.isfinite(remove_ratio_per_iter) else max(0.0, min(1.0, remove_ratio_per_iter))
    u_bottom_n_raw = int(max(0, int(args.u_bottom_n)))
    u_bottom_ratio = float(args.u_bottom_ratio)
    u_bottom_ratio = 0.0 if not np.isfinite(u_bottom_ratio) else max(0.0, min(1.0, u_bottom_ratio))

    topk_ratio = float(args.topk_ratio)
    topk_ratio = 0.0 if not np.isfinite(topk_ratio) else max(0.0, min(1.0, topk_ratio))

    u_holdout_n_raw = int(max(0, int(args.u_holdout_n)))
    u_holdout_ratio = float(args.u_holdout_ratio)
    u_holdout_ratio = 0.0 if not np.isfinite(u_holdout_ratio) else max(0.0, min(1.0, u_holdout_ratio))

    u_ids_full = (
        [str(x) for x in u_norm[u_id_col].tolist()]
        if u_id_col in u_norm.columns
        else [str(i) for i in range(int(u_norm.shape[0]))]
    )
    if u_labels_map is None:
        u_labels_full = np.zeros((int(u_norm.shape[0]),), dtype=int)
    else:
        u_labels_full = np.asarray([int(u_labels_map.get(_id, 0)) for _id in u_ids_full], dtype=int)

    n_u = int(u_norm.shape[0])
    if u_holdout_n_raw > 0:
        u_holdout_n = int(min(u_holdout_n_raw, n_u))
    elif u_holdout_ratio > 0.0:
        u_holdout_n = int(round(float(n_u) * u_holdout_ratio))
        if n_u >= 2:
            u_holdout_n = int(max(1, min(u_holdout_n, n_u - 1)))
        else:
            u_holdout_n = int(min(u_holdout_n, n_u))
    else:
        u_holdout_n = 0

    if u_holdout_n > 0:
        rng = np.random.RandomState(int(args.seed))
        all_idx = np.arange(n_u, dtype=int)
        pos_idx = all_idx[u_labels_full.astype(int) == 1]
        neg_idx = all_idx[u_labels_full.astype(int) != 1]
        rng.shuffle(pos_idx)
        rng.shuffle(neg_idx)
        desired_pos = int(round(float(u_holdout_n) * (float(pos_idx.size) / float(max(1, n_u)))))
        pos_take = int(min(max(0, desired_pos), int(pos_idx.size)))
        neg_take = int(min(int(u_holdout_n - pos_take), int(neg_idx.size)))
        holdout = np.concatenate([pos_idx[:pos_take], neg_idx[:neg_take]], axis=0)
        if int(holdout.size) < int(u_holdout_n):
            remaining = np.concatenate([pos_idx[pos_take:], neg_idx[neg_take:]], axis=0)
            rng.shuffle(remaining)
            need = int(u_holdout_n - int(holdout.size))
            holdout = np.concatenate([holdout, remaining[:need]], axis=0)
        holdout = np.unique(holdout.astype(int))
        train = np.setdiff1d(all_idx, holdout, assume_unique=False)
        u_train_norm0 = u_norm.iloc[train].copy()
        u_eval_norm = u_norm.iloc[holdout].copy()
        u_train_raw0 = u_raw.iloc[train].copy()
        u_eval_raw = u_raw.iloc[holdout].copy()
        u_train_ids0 = [u_ids_full[i] for i in train.tolist()]
        u_ids_all = [u_ids_full[i] for i in holdout.tolist()]
        u_eval_labels = u_labels_full[holdout]
    else:
        u_train_norm0 = u_norm.copy()
        u_eval_norm = u_norm.copy()
        u_train_raw0 = u_raw.copy()
        u_eval_raw = u_raw.copy()
        u_train_ids0 = u_ids_full
        u_ids_all = u_ids_full
        u_eval_labels = u_labels_full

    if u_bottom_n_raw > 0:
        u_bottom_n = u_bottom_n_raw
    elif u_bottom_ratio > 0.0:
        u_bottom_n = int(round(float(u_eval_norm.shape[0]) * u_bottom_ratio))
        if int(u_eval_norm.shape[0]) >= 1:
            u_bottom_n = int(max(1, min(u_bottom_n, int(u_eval_norm.shape[0]))))
        else:
            u_bottom_n = 0
    else:
        u_bottom_n = 0

    u_train_mask = np.ones((int(u_train_norm0.shape[0]),), dtype=bool)

    u_train_id_to_pos = {str(_id): int(i) for i, _id in enumerate(u_train_ids0)}

    global_removed_ids: set[str] = set()
    removed_for_next_candidates_ids: list[str] = []
    if state_path is not None:
        state_payload = _load_state(state_path)
        global_removed_ids = set(state_payload.get("removed_u_ids", []))
        for _id in list(global_removed_ids):
            pos = u_train_id_to_pos.get(str(_id), None)
            if pos is None:
                continue
            if 0 <= int(pos) < u_train_mask.shape[0]:
                u_train_mask[int(pos)] = False

    iter_records: list[dict[str, object]] = []
    last_scores_df: pd.DataFrame | None = None
    last_scores_path: Path | None = None
    last_model_kind: str = ""
    last_model_meta: dict[str, object] = {}
    last_used_k: int | None = None
    last_used_threshold: float | None = None
    last_eval_out: dict[str, object] = {}
    last_eval_out_all: dict[str, object] = {}

    for it in range(iterations):
        u_train_norm = u_train_norm0.iloc[np.nonzero(u_train_mask)[0]].copy()
        model_kind, model_meta, score_any = _load_backend(model_path, p_train=p_train_norm, u_df=u_train_norm, seed=int(args.seed))
        last_model_kind = model_kind
        last_model_meta = model_meta
        if model_kind == "legacy_score_u":
            p_test_scores_list: list[float] = []
            for i in range(int(p_test_norm.shape[0])):
                s1 = score_any(p_test_norm.iloc[[i]])
                p_test_scores_list.append(float(s1[0]) if s1.size else float("-inf"))
            p_test_scores = np.asarray(p_test_scores_list, dtype=float)
        else:
            p_test_scores = score_any(p_test_norm)

        u_eval_scores = score_any(u_eval_norm)
        scores = np.concatenate([p_test_scores, u_eval_scores], axis=0).astype(float, copy=False)
        scores[~np.isfinite(scores)] = float("-inf")

        y_true = np.concatenate([np.ones(int(p_test_norm.shape[0]), dtype=int), u_eval_labels.astype(int)], axis=0)

        eval_out: dict[str, object]
        used_k: int | None = None
        used_threshold: float | None = None
        u_only = metric_mode.startswith("u_")
        eval_scores = u_eval_scores if u_only else scores
        eval_labels = u_eval_labels if u_only else y_true

        if metric_mode in {"topk", "u_topk"}:
            default_k = int(p_test_norm.shape[0])
            if int(args.topk_k) > 0:
                k = int(args.topk_k)
            elif topk_ratio > 0.0:
                k = int(round(float(eval_scores.shape[0]) * topk_ratio))
            else:
                k = default_k
            used_k = int(max(1, min(k, int(eval_scores.shape[0])))) if int(eval_scores.shape[0]) > 0 else 0
            eval_out = _eval_topk(eval_scores, eval_labels, k=used_k)
        elif metric_mode in {"threshold", "u_threshold"}:
            raw_t = str(args.threshold or "").strip()
            if not raw_t:
                raise ValueError("metric_mode=threshold requires --threshold")
            t = float(raw_t)
            if not math.isfinite(t):
                raise ValueError("threshold must be finite")
            used_threshold = float(t)
            eval_out = _eval_threshold(eval_scores, eval_labels, threshold=used_threshold)
        else:
            best = _eval_maxf1(eval_scores, eval_labels)
            used_k = int(best.get("best_k", 0) or 0)
            eval_out = {
                "best_k": used_k,
                "best_precision": float(best.get("best_precision", 0.0) or 0.0),
                "best_recall": float(best.get("best_recall", 0.0) or 0.0),
                "best_f1": float(best.get("best_f1", 0.0) or 0.0),
            }

        if metric_mode not in {"maxf1", "u_maxf1"}:
            best = _eval_maxf1(eval_scores, eval_labels)
            eval_out["best_k"] = int(best.get("best_k", 0) or 0)
            eval_out["best_precision"] = float(best.get("best_precision", 0.0) or 0.0)
            eval_out["best_recall"] = float(best.get("best_recall", 0.0) or 0.0)
            eval_out["best_f1"] = float(best.get("best_f1", 0.0) or 0.0)

        eval_out_all: dict[str, object] = {}
        used_k_all: int | None = None
        used_threshold_all: float | None = None
        if u_only:
            base_mode = metric_mode[2:]
            if base_mode == "topk":
                default_k_all = int(p_test_norm.shape[0])
                if int(args.topk_k) > 0:
                    k_all = int(args.topk_k)
                elif topk_ratio > 0.0:
                    k_all = int(round(float(scores.shape[0]) * topk_ratio))
                else:
                    k_all = default_k_all
                used_k_all = int(max(1, min(int(k_all), int(scores.shape[0])))) if int(scores.shape[0]) > 0 else 0
                eval_out_all = _eval_topk(scores, y_true, k=used_k_all)
                best_all = _eval_maxf1(scores, y_true)
                eval_out_all["best_k"] = int(best_all.get("best_k", 0) or 0)
                eval_out_all["best_precision"] = float(best_all.get("best_precision", 0.0) or 0.0)
                eval_out_all["best_recall"] = float(best_all.get("best_recall", 0.0) or 0.0)
                eval_out_all["best_f1"] = float(best_all.get("best_f1", 0.0) or 0.0)
            elif base_mode == "threshold":
                raw_t = str(args.threshold or "").strip()
                if not raw_t:
                    raise ValueError("metric_mode=threshold requires --threshold")
                t = float(raw_t)
                if not math.isfinite(t):
                    raise ValueError("threshold must be finite")
                used_threshold_all = float(t)
                eval_out_all = _eval_threshold(scores, y_true, threshold=used_threshold_all)
                best_all = _eval_maxf1(scores, y_true)
                eval_out_all["best_k"] = int(best_all.get("best_k", 0) or 0)
                eval_out_all["best_precision"] = float(best_all.get("best_precision", 0.0) or 0.0)
                eval_out_all["best_recall"] = float(best_all.get("best_recall", 0.0) or 0.0)
                eval_out_all["best_f1"] = float(best_all.get("best_f1", 0.0) or 0.0)
            else:
                best_all = _eval_maxf1(scores, y_true)
                used_k_all = int(best_all.get("best_k", 0) or 0)
                eval_out_all = {
                    "best_k": used_k_all,
                    "best_precision": float(best_all.get("best_precision", 0.0) or 0.0),
                    "best_recall": float(best_all.get("best_recall", 0.0) or 0.0),
                    "best_f1": float(best_all.get("best_f1", 0.0) or 0.0),
                }

        last_used_k = used_k
        last_used_threshold = used_threshold
        last_eval_out = eval_out
        last_eval_out_all = eval_out_all

        p_test_ids = (
            [str(x) for x in p_test_norm[p_id_col].tolist()]
            if p_id_col in p_test_norm.columns
            else [str(i) for i in range(int(p_test_norm.shape[0]))]
        )
        scores_df = pd.DataFrame(
            {
                "split": (["p_test"] * int(p_test_norm.shape[0])) + (["u_eval"] * int(u_eval_norm.shape[0])),
                "label": y_true.astype(int),
                "id": p_test_ids + u_ids_all,
                "score": scores.astype(float),
                "iter": int(it + 1),
            }
        )
        scores_path = out_dir / f"scores_test_iter{int(it + 1)}.csv"
        scores_df.to_csv(scores_path, index=False)
        last_scores_df = scores_df
        last_scores_path = scores_path

        u_most_unlike_path = ""
        if u_bottom_n > 0 and int(u_eval_norm.shape[0]) > 0:
            u_rank = u_eval_raw.copy()
            u_rank["pu_score_like_p"] = u_eval_scores.astype(float, copy=False)
            order_u = np.argsort(u_eval_scores.astype(float, copy=False), kind="mergesort")
            u_most_unlike = u_rank.iloc[order_u[: int(min(u_bottom_n, int(u_eval_norm.shape[0])))]].copy()
            u_most_unlike_path = str(out_dir / f"u_most_unlike_p_iter{int(it + 1)}.csv")
            u_most_unlike.to_csv(u_most_unlike_path, index=False)

        removed_ids: list[str] = []
        removed_path = ""
        remove_n_per_iter_eff: int
        if remove_n_per_iter_raw > 0:
            remove_n_per_iter_eff = remove_n_per_iter_raw
        elif remove_ratio_per_iter > 0.0:
            remove_n_per_iter_eff = int(round(float(u_train_norm.shape[0]) * remove_ratio_per_iter))
        else:
            remove_n_per_iter_eff = 0

        if it < (iterations - 1) and remove_n_per_iter_eff > 0 and int(u_train_norm.shape[0]) > 0:
            u_train_scores = score_any(u_train_norm)
            remove_n = int(min(remove_n_per_iter_eff, int(u_train_norm.shape[0])))
            order_train = np.argsort(u_train_scores.astype(float, copy=False), kind="mergesort")
            remove_pos = order_train[:remove_n]
            remove_idx = u_train_norm.index.to_numpy()[remove_pos]
            for idx in remove_idx.tolist():
                try:
                    pos = int(np.where(u_train_norm0.index.to_numpy() == idx)[0][0])
                except Exception:
                    continue
                if 0 <= pos < u_train_mask.shape[0]:
                    u_train_mask[pos] = False
                    removed_id = u_train_ids0[pos] if pos < len(u_train_ids0) else str(pos)
                    removed_ids.append(removed_id)
                    global_removed_ids.add(removed_id)
                    removed_for_next_candidates_ids.append(str(removed_id))

            rem_df = u_train_raw0.iloc[np.nonzero(~u_train_mask)[0]].copy()
            removed_path = str(out_dir / f"u_train_removed_until_iter{int(it + 1)}.csv")
            rem_df.to_csv(removed_path, index=False)

        removed_for_next_candidates_this_iter: list[str] = []
        if state_path is not None and it == (iterations - 1) and remove_n_per_iter_eff > 0 and int(u_train_norm.shape[0]) > 0:
            u_train_scores = score_any(u_train_norm)
            remove_n = int(min(remove_n_per_iter_eff, int(u_train_norm.shape[0])))
            order_train = np.argsort(u_train_scores.astype(float, copy=False), kind="mergesort")
            remove_pos = order_train[:remove_n]
            active_positions = np.nonzero(u_train_mask)[0]
            for p in remove_pos.tolist():
                if not (0 <= int(p) < int(active_positions.shape[0])):
                    continue
                pos0 = int(active_positions[int(p)])
                if 0 <= pos0 < u_train_mask.shape[0]:
                    u_train_mask[pos0] = False
                    removed_id = u_train_ids0[pos0] if pos0 < len(u_train_ids0) else str(pos0)
                    removed_for_next_candidates_this_iter.append(str(removed_id))
                    removed_for_next_candidates_ids.append(str(removed_id))
                    global_removed_ids.add(str(removed_id))

        iter_records.append(
            {
                "iter": int(it + 1),
                "u_train_rows": int(u_train_norm.shape[0]),
                "u_eval_rows": int(u_eval_norm.shape[0]),
                "removed_this_iter_n": int(len(removed_ids)),
                "removed_this_iter_ids": removed_ids,
                "removed_for_next_candidates_n": int(len(removed_for_next_candidates_this_iter)),
                "removed_for_next_candidates_ids": removed_for_next_candidates_this_iter,
                "u_most_unlike_p_csv": u_most_unlike_path,
                "u_train_removed_until_csv": removed_path,
                "remove_n_per_iter_effective": int(remove_n_per_iter_eff),
                "remove_ratio_per_iter": remove_ratio_per_iter,
                "precision": _safe_float(eval_out.get("precision")) if "precision" in eval_out else _safe_float(eval_out.get("best_precision")),
                "recall": _safe_float(eval_out.get("recall")) if "recall" in eval_out else _safe_float(eval_out.get("best_recall")),
                "f1": _safe_float(eval_out.get("f1")) if "f1" in eval_out else _safe_float(eval_out.get("best_f1")),
                "eval": eval_out,
                "precision_all": _safe_float(eval_out_all.get("precision")) if "precision" in eval_out_all else _safe_float(eval_out_all.get("best_precision")) if eval_out_all else None,
                "recall_all": _safe_float(eval_out_all.get("recall")) if "recall" in eval_out_all else _safe_float(eval_out_all.get("best_recall")) if eval_out_all else None,
                "f1_all": _safe_float(eval_out_all.get("f1")) if "f1" in eval_out_all else _safe_float(eval_out_all.get("best_f1")) if eval_out_all else None,
                "eval_all": eval_out_all,
                "used_k": used_k,
                "used_threshold": used_threshold,
                "used_k_all": used_k_all,
                "used_threshold_all": used_threshold_all,
            }
        )

    payload: dict[str, object] = {
        "p_csv": str(p_csv),
        "u_csv": str(u_csv),
        "u_labeled_csv": str(u_labeled_csv) if u_labeled_csv is not None else "",
        "u_label_col": str(args.u_label_col),
        "model_kind": last_model_kind,
        "model_path": str(model_path) if model_path is not None else "",
        "seed": int(args.seed),
        "p_rows": int(p_norm.shape[0]),
        "p_train_rows": int(p_train_norm.shape[0]),
        "p_test_rows": int(p_test_norm.shape[0]),
        "u_rows": int(u_norm.shape[0]),
        "p_id_col": p_id_col,
        "u_id_col": u_id_col,
        "metric_mode": metric_mode,
        "used_k": last_used_k,
        "used_threshold": last_used_threshold,
        "iterations": iterations,
        "topk_ratio": topk_ratio,
        "u_holdout_ratio": u_holdout_ratio,
        "u_holdout_n": u_holdout_n,
        "remove_n_per_iter": remove_n_per_iter_raw,
        "remove_ratio_per_iter": remove_ratio_per_iter,
        "state_path": str(state_path) if state_path is not None else "",
        "removed_u_ids_total": int(len(global_removed_ids)),
        "removed_u_ids_added_this_candidate": sorted(list(set(removed_for_next_candidates_ids))),
        "precision": _safe_float(last_eval_out.get("precision")) if "precision" in last_eval_out else _safe_float(last_eval_out.get("best_precision")),
        "recall": _safe_float(last_eval_out.get("recall")) if "recall" in last_eval_out else _safe_float(last_eval_out.get("best_recall")),
        "f1": _safe_float(last_eval_out.get("f1")) if "f1" in last_eval_out else _safe_float(last_eval_out.get("best_f1")),
        "eval": last_eval_out,
        "precision_all": _safe_float(last_eval_out_all.get("precision")) if "precision" in last_eval_out_all else _safe_float(last_eval_out_all.get("best_precision")) if last_eval_out_all else None,
        "recall_all": _safe_float(last_eval_out_all.get("recall")) if "recall" in last_eval_out_all else _safe_float(last_eval_out_all.get("best_recall")) if last_eval_out_all else None,
        "f1_all": _safe_float(last_eval_out_all.get("f1")) if "f1" in last_eval_out_all else _safe_float(last_eval_out_all.get("best_f1")) if last_eval_out_all else None,
        "eval_all": last_eval_out_all,
        "model_meta": last_model_meta,
        "iter": iter_records,
        "outputs": {
            "scores_test_csv": str(last_scores_path) if last_scores_path is not None else "",
            "u_bottom_n": u_bottom_n,
            "u_bottom_ratio": u_bottom_ratio,
        },
    }
    
    if state_path is not None:
        state_payload = _load_state(state_path)
        state_payload["removed_u_ids"] = sorted(list(global_removed_ids))
        _save_state(state_path, state_payload)
        
    (out_dir / "metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
