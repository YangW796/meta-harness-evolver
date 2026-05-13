from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path

import pandas as pd


def _safe_float(x: object, default: float | None = None) -> float | None:
    if x is None:
        return default
    try:
        v = float(x)
    except Exception:
        return default
    if not math.isfinite(v):
        return default
    return v


def _safe_int(x: object, default: int = 0) -> int:
    if x is None:
        return default
    try:
        return int(x)
    except Exception:
        return default


def _read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _norm_col(s: str) -> str:
    s = str(s).strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def _read_csv_columns(path: Path, nrows: int = 5) -> dict[str, object]:
    try:
        df = pd.read_csv(path, nrows=int(max(0, nrows)))
    except Exception:
        return {}
    cols = [str(c) for c in df.columns.tolist()]
    norm_cols = [_norm_col(c) for c in cols]
    return {"nrows_sampled": int(nrows), "cols": cols, "cols_normalized": norm_cols, "n_cols": int(len(cols))}


def _format_list(xs: list[str], limit: int) -> list[str]:
    limit = int(max(0, limit))
    if limit <= 0:
        return []
    if len(xs) <= limit:
        return xs
    return xs[:limit] + [f"...(+{len(xs) - limit})"]


def _collect_dataset_context() -> dict[str, object]:
    ctx: dict[str, object] = {}

    raw_p = str(os.environ.get("PROJECT_PU_P_CSV", "")).strip()
    raw_u = str(os.environ.get("PROJECT_PU_U_CSV", "")).strip()
    raw_ul = str(os.environ.get("PROJECT_PU_U_LABELED_CSV", "")).strip()
    label_col = str(os.environ.get("PROJECT_PU_U_LABEL_COL", "u_label") or "u_label").strip()

    def _as_path(raw: str) -> Path | None:
        if not raw:
            return None
        try:
            p = Path(raw).expanduser().resolve()
        except Exception:
            return None
        return p if p.exists() else None

    p_path = _as_path(raw_p)
    u_path = _as_path(raw_u)
    ul_path = _as_path(raw_ul)

    ctx["env"] = {
        "PROJECT_PU_P_CSV_set": bool(raw_p),
        "PROJECT_PU_U_CSV_set": bool(raw_u),
        "PROJECT_PU_U_LABELED_CSV_set": bool(raw_ul),
        "PROJECT_PU_U_LABEL_COL": label_col,
        "PROJECT_PU_TEST_RATIO": str(os.environ.get("PROJECT_PU_TEST_RATIO", "")).strip(),
        "PROJECT_PU_TEST_N": str(os.environ.get("PROJECT_PU_TEST_N", "")).strip(),
        "PROJECT_PU_METRIC_MODE": str(os.environ.get("PROJECT_PU_METRIC_MODE", "")).strip(),
        "PROJECT_PU_TOPK_K": str(os.environ.get("PROJECT_PU_TOPK_K", "")).strip(),
        "PROJECT_PU_THRESHOLD": str(os.environ.get("PROJECT_PU_THRESHOLD", "")).strip(),
        "PROJECT_PU_U_BOTTOM_N": str(os.environ.get("PROJECT_PU_U_BOTTOM_N", "")).strip(),
        "PROJECT_PU_U_BOTTOM_RATIO": str(os.environ.get("PROJECT_PU_U_BOTTOM_RATIO", "")).strip(),
        "PROJECT_PU_ITERATIONS": str(os.environ.get("PROJECT_PU_ITERATIONS", "")).strip(),
        "PROJECT_PU_REMOVE_N_PER_ITER": str(os.environ.get("PROJECT_PU_REMOVE_N_PER_ITER", "")).strip(),
        "PROJECT_PU_REMOVE_RATIO_PER_ITER": str(os.environ.get("PROJECT_PU_REMOVE_RATIO_PER_ITER", "")).strip(),
        "PROJECT_PU_SEED": str(os.environ.get("PROJECT_PU_SEED", "")).strip(),
    }

    ctx["csv_schema"] = {
        "P": _read_csv_columns(p_path) if p_path is not None else {},
        "U": _read_csv_columns(u_path) if u_path is not None else {},
        "U_labeled": _read_csv_columns(ul_path) if ul_path is not None else {},
    }

    p_cols_norm = ctx["csv_schema"].get("P", {}).get("cols_normalized", []) if isinstance(ctx.get("csv_schema"), dict) else []
    u_cols_norm = ctx["csv_schema"].get("U", {}).get("cols_normalized", []) if isinstance(ctx.get("csv_schema"), dict) else []
    ul_cols_norm = ctx["csv_schema"].get("U_labeled", {}).get("cols_normalized", []) if isinstance(ctx.get("csv_schema"), dict) else []

    if isinstance(p_cols_norm, list) and isinstance(u_cols_norm, list):
        ctx["normalized_col_overlap"] = {
            "p_n_cols": int(len(p_cols_norm)),
            "u_n_cols": int(len(u_cols_norm)),
            "intersection_n": int(len(set(p_cols_norm) & set(u_cols_norm))),
            "intersection_preview": _format_list(sorted(set(p_cols_norm) & set(u_cols_norm)), 40),
        }

    if isinstance(ul_cols_norm, list):
        ctx["u_labeled_special_cols_hint"] = {
            "label_col_normalized": _norm_col(label_col),
            "has_u_label": _norm_col(label_col) in set(ul_cols_norm),
            "has_oracle_score": "oracle_score" in set(ul_cols_norm),
        }

    return ctx


def _collect_best_metrics(paths) -> dict[str, object]:
    metrics_path = paths.best_dir / "outputs" / "metrics.json"
    legacy_metrics_path = paths.best_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        metrics_path = legacy_metrics_path
    payload = _read_json(metrics_path) if metrics_path.exists() else {}

    iters = payload.get("iter", []) if isinstance(payload, dict) else []
    iter_summary: list[dict[str, object]] = []
    if isinstance(iters, list):
        for r in iters[-5:]:
            if not isinstance(r, dict):
                continue
            iter_summary.append(
                {
                    "iter": _safe_int(r.get("iter"), 0),
                    "u_train_rows": _safe_int(r.get("u_train_rows"), 0),
                    "removed_this_iter_n": _safe_int(r.get("removed_this_iter_n"), 0),
                    "precision": _safe_float(r.get("precision")),
                    "recall": _safe_float(r.get("recall")),
                    "f1": _safe_float(r.get("f1")),
                    "best_f1": _safe_float((r.get("eval", {}) or {}).get("best_f1")) if isinstance(r.get("eval", {}), dict) else None,
                }
            )

    out = {
        "source_metrics_path_exists": bool(metrics_path.exists()),
        "metric_mode": str(payload.get("metric_mode", "")).strip() if isinstance(payload, dict) else "",
        "iterations": _safe_int(payload.get("iterations"), 0) if isinstance(payload, dict) else 0,
        "remove_n_per_iter": _safe_int(payload.get("remove_n_per_iter"), 0) if isinstance(payload, dict) else 0,
        "p_rows": _safe_int(payload.get("p_rows"), 0) if isinstance(payload, dict) else 0,
        "p_train_rows": _safe_int(payload.get("p_train_rows"), 0) if isinstance(payload, dict) else 0,
        "p_test_rows": _safe_int(payload.get("p_test_rows"), 0) if isinstance(payload, dict) else 0,
        "u_rows": _safe_int(payload.get("u_rows"), 0) if isinstance(payload, dict) else 0,
        "precision": _safe_float(payload.get("precision")) if isinstance(payload, dict) else None,
        "recall": _safe_float(payload.get("recall")) if isinstance(payload, dict) else None,
        "f1": _safe_float(payload.get("f1")) if isinstance(payload, dict) else None,
        "eval_best_f1": _safe_float((payload.get("eval", {}) or {}).get("best_f1")) if isinstance(payload.get("eval", {}), dict) else None,
        "recent_iter_summary": iter_summary,
    }
    return out


def build_prompt_context(paths, cfg, candidate_num: int, history, best) -> str:
    dataset_ctx = _collect_dataset_context()
    best_ctx = _collect_best_metrics(paths)
    ctx = {
        "task": "PU scoring (P positive, U partially-positive with synthetic labels in U_labeled for evaluation only).",
        "candidate_num": int(candidate_num),
        "best_final_score": best.get("final_score") if isinstance(best, dict) else None,
        "dataset": dataset_ctx,
        "best_metrics": best_ctx,
        "hard_rules": [
            "Only edit <candidate_dir>/harness/model.py.",
            "Do NOT read any CSV files from disk inside model.py. Use only p_train_df/u_df/x_df passed into fit/score.",
            "Never use u_label/oracle_score as features (they are evaluation-only).",
            "Must handle column name variations (case/underscore), missing values, and mismatched P/U columns by using common numeric features.",
            "Deterministic given seed.",
        ],
    }
    return (
        "## Runtime Data Context (MANDATORY)\n"
        "You MUST use this context when designing feature normalization and robustness.\n"
        "Treat `U_labeled` columns as evaluation-only; model.py never sees them unless you cheat (forbidden).\n"
        "\n"
        + "```json\n"
        + json.dumps(ctx, ensure_ascii=False, indent=2)
        + "\n```\n"
    )


def build_attempt_planner_context(paths, cfg, candidate_num: int, attempts: int, best):
    dataset_ctx = _collect_dataset_context()
    best_ctx = _collect_best_metrics(paths)
    prompt = "\n".join(
        [
            "## Attempt Planning Context (MANDATORY)",
            "Base your attempt diversity on these signals:",
            "- Column schema (normalized overlap) tells you what features exist in both P and U.",
            "- Best metrics' recent_iter_summary hints whether the score is stable across iterations.",
            "- Avoid strategies that depend on reading files/labels from disk.",
            "",
            "```json",
            json.dumps({"candidate_num": int(candidate_num), "attempts": int(attempts), "dataset": dataset_ctx, "best_metrics": best_ctx}, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return {"prompt": prompt, "per_attempt_fields": {}}
