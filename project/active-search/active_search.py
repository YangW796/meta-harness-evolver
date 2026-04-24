#!/usr/bin/env python3
import argparse
import csv
import heapq
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np


def _env(prefix: str, name: str, default: str) -> str:
    if prefix:
        v = os.environ.get(f"{prefix}_{name}", "")
        if v != "":
            return v
    v = os.environ.get(name, "")
    if v != "":
        return v
    return default


def _env_int(prefix: str, name: str, default: int) -> int:
    s = _env(prefix, name, str(default))
    try:
        return int(s)
    except Exception:
        return int(default)


def _env_float(prefix: str, name: str, default: float) -> float:
    s = _env(prefix, name, str(default))
    try:
        return float(s)
    except Exception:
        return float(default)


def _load_selection_policy(model_file: str):
    model_path = Path(model_file).expanduser().resolve()
    if not model_path.exists():
        raise ValueError(f"model file does not exist: {model_path}")

    spec = importlib.util.spec_from_file_location("candidate_policy_module", str(model_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load policy module from: {model_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    if callable(getattr(module, "select", None)):
        return module.select

    for cls_name in ["SelectionPolicy", "Policy", "Model"]:
        cls = getattr(module, cls_name, None)
        if cls is None:
            continue
        inst = cls()
        if callable(getattr(inst, "select", None)):
            return inst.select

    raise ValueError("model file missing required callable: select(candidates, history, batch_size, seed) -> list[int]")


def _parse_cell(v: str) -> object:
    s = (v or "").strip()
    if s == "":
        return ""
    try:
        x = float(s)
    except Exception:
        return s
    if not np.isfinite(x):
        return 0.0
    return x


def _read_csv_rows(csv_path: str) -> list[dict[str, object]]:
    path = Path(csv_path).expanduser().resolve()
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV missing header: {path}")
        rows: list[dict[str, object]] = []
        for r in reader:
            row: dict[str, object] = {}
            for k in reader.fieldnames:
                row[k] = _parse_cell(r.get(k, ""))
            rows.append(row)
    return rows


def _make_candidate_pool(rows: list[dict[str, object]], pool_size: int, seed: int) -> list[dict[str, object]]:
    if pool_size <= 0:
        raise ValueError(f"pool_size must be positive, got: {pool_size}")
    if pool_size >= len(rows):
        return list(rows)
    rng = np.random.default_rng(int(seed))
    keep_idx = rng.choice(len(rows), size=int(pool_size), replace=False).tolist()
    return [rows[i] for i in keep_idx]


def _load_ground_truth_csv(path: str, n: int) -> np.ndarray:
    p = Path(path).expanduser().resolve()
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"ground_truth CSV missing header: {p}")
        required = {"candidate_index", "label"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"ground_truth CSV missing columns {sorted(missing)}: {p}")
        labels = np.zeros((n,), dtype=np.int8)
        seen = 0
        for r in reader:
            try:
                i = int(float(str(r.get("candidate_index", "")).strip()))
                lab = int(float(str(r.get("label", "")).strip()))
            except Exception:
                continue
            if 0 <= i < n:
                labels[i] = 1 if lab != 0 else 0
                seen += 1
        if seen == 0:
            raise ValueError(f"ground_truth CSV contains no valid rows: {p}")
    return labels


def _extract_inline_labels(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], np.ndarray | None]:
    if not rows:
        return rows, None
    if "label" not in rows[0]:
        return rows, None
    labels = np.zeros((len(rows),), dtype=np.int8)
    stripped: list[dict[str, object]] = []
    for i, r in enumerate(rows):
        rr = dict(r)
        v = rr.pop("label", 0)
        try:
            labels[i] = 1 if int(float(str(v).strip())) != 0 else 0
        except Exception:
            labels[i] = 0
        stripped.append(rr)
    return stripped, labels


def _infer_task_from_csv_path(csv_path: str) -> str:
    name = Path(csv_path).name
    if name.startswith("ground_truth_") and name.endswith(".csv"):
        return name[len("ground_truth_") : -len(".csv")]
    return ""


def _labels_from_topmovers_file(pool_rows: list[dict[str, object]], csv_path: str, task: str) -> np.ndarray | None:
    if not pool_rows:
        return np.zeros((0,), dtype=np.int8)
    t = (task or "").strip()
    if not t:
        return None
    gene_key = None
    for k in pool_rows[0].keys():
        if str(k).strip().lower() == "gene":
            gene_key = k
            break
    if gene_key is None:
        return None
    topmovers_path = Path(csv_path).expanduser().resolve().parent / f"topmovers_{t}.npy"
    if not topmovers_path.exists():
        return None
    arr = np.load(str(topmovers_path), allow_pickle=True)
    try:
        top = set(str(x) for x in arr.tolist())
    except Exception:
        top = set(str(x) for x in list(arr))
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    for i, r in enumerate(pool_rows):
        v = r.get(gene_key, "")
        if str(v) in top:
            labels[i] = 1
    return labels


def _labels_from_numeric_column(
    pool_rows: list[dict[str, object]],
    column_name: str,
    top_ratio: float,
    use_abs: bool,
) -> np.ndarray | None:
    if not pool_rows:
        return np.zeros((0,), dtype=np.int8)
    key = None
    target = str(column_name).strip().lower()
    for k in pool_rows[0].keys():
        if str(k).strip().lower() == target:
            key = k
            break
    if key is None:
        return None
    vals = np.zeros((len(pool_rows),), dtype=np.float64)
    for i, r in enumerate(pool_rows):
        v = r.get(key, 0.0)
        try:
            x = float(v)
        except Exception:
            x = 0.0
        if not np.isfinite(x):
            x = 0.0
        vals[i] = abs(x) if bool(use_abs) else x
    r = float(top_ratio)
    if not (0.0 < r < 1.0):
        raise ValueError(f"top_ratio must be in (0, 1), got: {r}")
    k = int(max(1, int(round(len(pool_rows) * r))))
    k = int(min(k, len(pool_rows)))
    order = np.argsort(-vals, kind="mergesort")
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    if k > 0:
        labels[order[:k]] = 1
    return labels


def _strip_columns_case_insensitive(rows: list[dict[str, object]], deny: set[str]) -> list[dict[str, object]]:
    if not rows:
        return rows
    deny_norm = {s.strip().lower() for s in deny if str(s).strip()}
    out: list[dict[str, object]] = []
    for r in rows:
        rr: dict[str, object] = {}
        for k, v in r.items():
            if str(k).strip().lower() in deny_norm:
                continue
            rr[k] = v
        out.append(rr)
    return out


def _sanitize_selected_indices(
    selected: object,
    n: int,
    already_selected: set[int],
    batch_size: int,
    seed: int,
) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()

    if selected is None:
        selected_list: list[object] = []
    elif isinstance(selected, (list, tuple, np.ndarray)):
        selected_list = list(selected)
    else:
        selected_list = [selected]

    for v in selected_list:
        try:
            idx = int(v)
        except Exception:
            continue
        if idx < 0 or idx >= n:
            continue
        if idx in already_selected or idx in seen:
            continue
        out.append(idx)
        seen.add(idx)
        if len(out) >= batch_size:
            break

    if len(out) < batch_size:
        remaining = [i for i in range(n) if i not in already_selected and i not in seen]
        if remaining:
            rng = np.random.default_rng(int(seed))
            fill_n = min(batch_size - len(out), len(remaining))
            fill = rng.choice(np.asarray(remaining, dtype=np.int64), size=int(fill_n), replace=False).tolist()
            out.extend(int(x) for x in fill)

    return out


def _build_history_from_records(
    pool_rows: list[dict[str, object]],
    records: list[dict[str, int]],
) -> tuple[list[dict[str, object]], set[int], int]:
    history: list[dict[str, object]] = []
    already_selected: set[int] = set()
    total_hits = 0
    n = len(pool_rows)
    for rec in records:
        try:
            i = int(rec.get("candidate_index", -1))
            lab = int(rec.get("label", 0))
        except Exception:
            continue
        if i < 0 or i >= n or i in already_selected:
            continue
        row = dict(pool_rows[i])
        row["candidate_index"] = i
        row["label"] = 1 if lab != 0 else 0
        history.append(row)
        already_selected.add(i)
        total_hits += int(row["label"])
    return history, already_selected, total_hits


def _load_state(path: str) -> dict:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return {}
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _save_state(path: str, payload: dict) -> None:
    p = Path(path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _jsonify_value(v: object, max_str_len: int) -> object:
    if v is None:
        return None
    if isinstance(v, (bool, int, float)):
        if isinstance(v, float) and not np.isfinite(v):
            return 0.0
        return v
    if isinstance(v, str):
        if len(v) <= max_str_len:
            return v
        return v[:max_str_len]
    try:
        x = float(v)
        if not np.isfinite(x):
            return 0.0
        return x
    except Exception:
        s = str(v)
        if len(s) <= max_str_len:
            return s
        return s[:max_str_len]


def _jsonify_row(row: dict[str, object], max_str_len: int) -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in row.items():
        out[str(k)] = _jsonify_value(v, max_str_len=max_str_len)
    return out


def _extract_numeric_scores(rows: list[dict[str, object]], column_name: str, use_abs: bool) -> list[float] | None:
    if not rows:
        return []
    target = str(column_name).strip().lower()
    key = None
    for k in rows[0].keys():
        if str(k).strip().lower() == target:
            key = k
            break
    if key is None:
        return None
    scores: list[float] = []
    for r in rows:
        v = r.get(key, 0.0)
        try:
            x = float(v)
        except Exception:
            x = 0.0
        if not np.isfinite(x):
            x = 0.0
        scores.append(abs(x) if bool(use_abs) else x)
    return scores


def _compute_ncg_from_records(scores: list[float] | None, queried_records: object) -> tuple[float | None, float, float, int]:
    if not scores:
        return None, 0.0, 0.0, 0
    if not isinstance(queried_records, list):
        return None, 0.0, 0.0, 0
    n = len(scores)
    selected: list[int] = []
    seen: set[int] = set()
    for r in queried_records:
        if not isinstance(r, dict):
            continue
        try:
            i = int(r.get("candidate_index", -1))
        except Exception:
            continue
        if i < 0 or i >= n or i in seen:
            continue
        selected.append(i)
        seen.add(i)
    k = len(selected)
    if k <= 0:
        return 0.0, 0.0, 0.0, 0
    selected_sum = float(sum(scores[i] for i in selected))
    topk_sum = float(sum(heapq.nlargest(k, scores)))
    if topk_sum <= 0.0:
        return 0.0, selected_sum, topk_sum, k
    return float(selected_sum / topk_sum), selected_sum, topk_sum, k


def run_active_search(
    pool_rows: list[dict[str, object]],
    labels: np.ndarray,
    select_fn,
    rounds: int,
    batch_size: int,
    seed: int,
    seed_queries: int,
    initial_history: list[dict[str, object]] | None = None,
    initial_already_selected: set[int] | None = None,
    start_round: int = 0,
) -> dict:
    n = int(len(pool_rows))
    already_selected: set[int] = set(initial_already_selected or set())
    history: list[dict[str, object]] = [dict(r) for r in (initial_history or [])]
    baseline_total_queries = int(len(history))
    baseline_total_hits = int(sum(int(r.get("label", 0)) for r in history))

    rng = np.random.default_rng(int(seed) + int(start_round))
    if seed_queries > 0 and n > 0 and not history:
        seed_queries = int(min(seed_queries, n))
        seed_idx = rng.choice(n, size=seed_queries, replace=False).tolist()
        seed_idx = _sanitize_selected_indices(seed_idx, n=n, already_selected=already_selected, batch_size=seed_queries, seed=seed)
        for i in seed_idx:
            r = dict(pool_rows[i])
            r["candidate_index"] = int(i)
            r["label"] = int(labels[int(i)])
            history.append(r)
        already_selected.update(int(i) for i in seed_idx)

    per_round: list[dict] = []
    cumulative_hits = int(sum(int(r.get("label", 0)) for r in history))
    total_queries = int(len(history))
    hit_curve_queries: list[int] = [total_queries]
    hit_curve_hits: list[int] = [cumulative_hits]

    executed_rounds = 0
    for t in range(int(rounds)):
        if len(already_selected) >= n:
            break
        global_round = int(start_round) + int(t)
        selected_raw = select_fn(pool_rows, history, int(batch_size), int(seed) + global_round)
        selected = _sanitize_selected_indices(
            selected_raw,
            n=n,
            already_selected=already_selected,
            batch_size=int(batch_size),
            seed=int(seed) + 10_000 + global_round,
        )
        hits_t = int(labels[np.asarray(selected, dtype=np.int64)].sum()) if selected else 0

        for i in selected:
            r = dict(pool_rows[int(i)])
            r["candidate_index"] = int(i)
            r["label"] = int(labels[int(i)])
            history.append(r)
        already_selected.update(int(i) for i in selected)

        cumulative_hits += hits_t
        total_queries += int(len(selected))
        hit_curve_queries.append(total_queries)
        hit_curve_hits.append(cumulative_hits)
        executed_rounds += 1

        per_round.append(
            {
                "round": int(global_round + 1),
                "queried": int(len(selected)),
                "hits": int(hits_t),
                "cumulative_hits": int(cumulative_hits),
                "precision_at_batch": float(hits_t / max(1, int(len(selected)))),
            }
        )
        if cumulative_hits >= int(labels.sum()):
            break

    top_k = int(labels.sum())
    recall = float(cumulative_hits / max(1, top_k))
    delta_queries = int(total_queries - baseline_total_queries)
    delta_hits = int(cumulative_hits - baseline_total_hits)

    area = 0.0
    for i in range(1, len(hit_curve_queries)):
        x0, x1 = float(hit_curve_queries[i - 1]), float(hit_curve_queries[i])
        y0, y1 = float(hit_curve_hits[i - 1]), float(hit_curve_hits[i])
        area += (x1 - x0) * (y0 + y1) / 2.0
    auc_norm = float(area / max(1.0, float(hit_curve_queries[-1]) * float(max(1, top_k))))

    queried_records: list[dict[str, int]] = []
    for r in history:
        try:
            queried_records.append({"candidate_index": int(r["candidate_index"]), "label": int(r["label"])})
        except Exception:
            continue
    queried_history = [_jsonify_row(dict(r), max_str_len=500) for r in history]

    return {
        "pool_size": int(n),
        "top_k": int(top_k),
        "rounds": int(start_round + executed_rounds),
        "executed_rounds": int(executed_rounds),
        "batch_size": int(batch_size),
        "seed": int(seed),
        "seed_queries": int(seed_queries),
        "baseline_total_queries": int(baseline_total_queries),
        "baseline_total_hits": int(baseline_total_hits),
        "delta_queries": int(delta_queries),
        "delta_hits": int(delta_hits),
        "total_queries": int(total_queries),
        "total_hits": int(cumulative_hits),
        "recall": recall,
        "auc": float(area),
        "auc_normalized": auc_norm,
        "hit_curve": {"queries": hit_curve_queries, "hits": hit_curve_hits},
        "round_details": per_round,
        "queried_records": queried_records,
        "queried_history": queried_history,
    }


def cli_main(env_prefix: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["active_search"], default="active_search")
    parser.add_argument("--csv", required=True, help="large CSV path or prebuilt candidate_pool CSV path")
    parser.add_argument("--model_dir", default="model.py", help="selection policy implementation file")
    parser.add_argument("--task", default=_env(env_prefix, "TASK", ""))
    parser.add_argument("--pool_size", type=int, default=_env_int(env_prefix, "POOL_SIZE", 5000))
    parser.add_argument("--top_ratio", type=float, default=_env_float(env_prefix, "TOP_RATIO", 0.2))
    parser.add_argument("--batch_size", type=int, default=_env_int(env_prefix, "BATCH_SIZE", 100))
    parser.add_argument("--rounds", type=int, default=_env_int(env_prefix, "ROUNDS", 1))
    parser.add_argument("--seed", type=int, default=_env_int(env_prefix, "SEED", 42))
    parser.add_argument("--seed_queries", type=int, default=_env_int(env_prefix, "SEED_QUERIES", 0))
    parser.add_argument("--fixed_pool", action="store_true")
    parser.add_argument("--ground_truth_csv", default=_env(env_prefix, "GROUND_TRUTH_CSV", ""))
    parser.add_argument("--state_path", default=_env(env_prefix, "STATE_PATH", ""))
    parser.add_argument("--resume_state", type=int, default=_env_int(env_prefix, "RESUME_STATE", 1))
    parser.add_argument("--score_column", default=_env(env_prefix, "SCORE_COLUMN", "Score"))
    args = parser.parse_args()

    rows = _read_csv_rows(args.csv)
    csv_name = Path(args.csv).name
    use_fixed = bool(args.fixed_pool) or csv_name.startswith("candidate_pool_")
    pool_rows = list(rows) if use_fixed else _make_candidate_pool(rows, pool_size=int(args.pool_size), seed=int(args.seed))

    pool_rows, inline_labels = _extract_inline_labels(pool_rows)
    if inline_labels is not None:
        labels = inline_labels
    elif args.ground_truth_csv:
        labels = _load_ground_truth_csv(args.ground_truth_csv, n=len(pool_rows))
    else:
        task = str(args.task or "").strip() or _infer_task_from_csv_path(args.csv)
        labels = None
        labels = _labels_from_topmovers_file(pool_rows, csv_path=args.csv, task=task)
        if labels is None:
            labels = _labels_from_numeric_column(
                pool_rows,
                column_name=str(args.score_column),
                top_ratio=float(args.top_ratio),
                use_abs=True,
            )
        if labels is None:
            raise ValueError(
                "Unable to build ground-truth labels. Provide one of: "
                "(1) CSV with 'label' column, (2) --ground_truth_csv with candidate_index,label, "
                "(3) topmovers_<TASK>.npy alongside the CSV (and a 'Gene' column), "
                "(4) a numeric score column."
            )

    scores_for_ncg = _extract_numeric_scores(pool_rows, column_name=str(args.score_column), use_abs=True)
    pool_rows = _strip_columns_case_insensitive(pool_rows, deny={str(args.score_column), "score"})
    select_fn = _load_selection_policy(args.model_dir)

    default_state_path = str(Path(args.model_dir).expanduser().resolve().parent / "outputs" / "active_search_state.json")
    state_path = args.state_path if args.state_path else default_state_path
    state = _load_state(state_path) if int(args.resume_state) != 0 else {}
    record_list: list[dict[str, int]] = []
    completed_rounds = 0
    if state:
        record_list = state.get("queried_records", [])
        if not isinstance(record_list, list):
            record_list = []
        try:
            completed_rounds = int(state.get("completed_rounds", 0))
        except Exception:
            completed_rounds = 0

    history, already_selected, _ = _build_history_from_records(pool_rows, record_list)
    seed_queries = int(args.seed_queries) if not history else 0
    metrics = run_active_search(
        pool_rows=pool_rows,
        labels=labels,
        select_fn=select_fn,
        rounds=int(args.rounds),
        batch_size=int(args.batch_size),
        seed=int(args.seed),
        seed_queries=seed_queries,
        initial_history=history,
        initial_already_selected=already_selected,
        start_round=int(completed_rounds),
    )

    ncg, ncg_selected_sum, ncg_topk_sum, ncg_k = _compute_ncg_from_records(
        scores=scores_for_ncg,
        queried_records=metrics.get("queried_records", []),
    )
    metrics["ncg"] = ncg
    metrics["ncg_k"] = int(ncg_k)
    metrics["ncg_selected_sum"] = float(ncg_selected_sum)
    metrics["ncg_topk_sum"] = float(ncg_topk_sum)

    output_dir = Path(args.model_dir).expanduser().resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"metrics": {"test": metrics}}
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    state_payload = {
        "completed_rounds": int(metrics.get("rounds", completed_rounds)),
        "pool_size": int(metrics.get("pool_size", len(pool_rows))),
        "top_k": int(metrics.get("top_k", int(labels.sum()))),
        "batch_size": int(args.batch_size),
        "seed": int(args.seed),
        "queried_records": metrics.get("queried_records", []),
        "queried_history": metrics.get("queried_history", []),
        "total_queries": int(metrics.get("total_queries", 0)),
        "total_hits": int(metrics.get("total_hits", 0)),
        "ncg": ncg,
        "ncg_k": int(ncg_k),
        "ncg_selected_sum": float(ncg_selected_sum),
        "ncg_topk_sum": float(ncg_topk_sum),
    }
    _save_state(state_path, state_payload)

    print(f"Metrics saved to {metrics_path}")
    print(f"State saved to {state_path}")
    return 0


def main() -> int:
    env_prefix = os.environ.get("ACTIVE_SEARCH_ENV_PREFIX", "PROJECT4")
    return cli_main(str(env_prefix))


if __name__ == "__main__":
    raise SystemExit(main())
