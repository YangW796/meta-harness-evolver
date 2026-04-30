import argparse
import csv
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np


AUTO_ID_COLUMNS = ["id", "ID", "candidate_id", "sequence_id", "name"]
RESERVED_COLUMNS = {"label", "candidate_index"}


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


def _read_csv_rows(csv_path: str) -> tuple[list[str], list[dict[str, object]]]:
    path = Path(csv_path).expanduser().resolve()
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV missing header: {path}")
        fieldnames = list(reader.fieldnames)
        rows: list[dict[str, object]] = []
        for r in reader:
            row: dict[str, object] = {}
            for k in fieldnames:
                row[k] = _parse_cell(r.get(k, ""))
            rows.append(row)
    return fieldnames, rows


def _make_candidate_pool(rows: list[dict[str, object]], pool_size: int, seed: int) -> list[dict[str, object]]:
    if pool_size <= 0:
        raise ValueError(f"pool_size must be positive, got: {pool_size}")
    if pool_size >= len(rows):
        return list(rows)
    rng = np.random.default_rng(int(seed))
    keep_idx = rng.choice(len(rows), size=int(pool_size), replace=False).tolist()
    return [rows[i] for i in keep_idx]


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


def _parse_match_columns(raw: str) -> list[str]:
    return [c.strip() for c in (raw or "").split(",") if c.strip()]


def _normalize_key_value(v: object) -> object:
    if v is None:
        return ""
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        x = float(v)
        if not np.isfinite(x):
            return 0.0
        return round(x, 10)
    s = str(v).strip()
    try:
        x = float(s)
    except Exception:
        return s
    if not np.isfinite(x):
        return 0.0
    return round(x, 10)


def _choose_match_columns(
    candidate_fields: list[str],
    positive_fields: list[str],
    id_column: str,
    match_columns: str,
) -> tuple[str, list[str]]:
    cand_set = set(candidate_fields)
    pos_set = set(positive_fields)
    if id_column:
        if id_column not in cand_set or id_column not in pos_set:
            raise ValueError(f"id_column must exist in both CSVs: {id_column}")
        return "id_column", [id_column]

    explicit = _parse_match_columns(match_columns)
    if explicit:
        missing = [c for c in explicit if c not in cand_set or c not in pos_set]
        if missing:
            raise ValueError(f"match_columns missing from candidate or positive CSV: {missing}")
        return "match_columns", explicit

    for col in AUTO_ID_COLUMNS:
        if col in cand_set and col in pos_set:
            return "auto_id_column", [col]

    common = [
        c
        for c in candidate_fields
        if c in pos_set and c not in RESERVED_COLUMNS and not c.startswith("_")
    ]
    if not common:
        raise ValueError(
            "Could not infer matching columns. Set PROJECT_PU_ID_COLUMN or PROJECT_PU_MATCH_COLUMNS."
        )
    return "common_columns", sorted(common)


def _row_key(row: dict[str, object], columns: list[str]) -> tuple[object, ...]:
    return tuple(_normalize_key_value(row.get(c, "")) for c in columns)


def _make_pu_labels(
    pool_rows: list[dict[str, object]],
    positive_rows: list[dict[str, object]],
    positive_fields: list[str],
    candidate_fields: list[str],
    id_column: str,
    match_columns: str,
) -> tuple[np.ndarray, dict]:
    match_mode, columns = _choose_match_columns(
        candidate_fields=candidate_fields,
        positive_fields=positive_fields,
        id_column=id_column,
        match_columns=match_columns,
    )
    positive_keys = [_row_key(r, columns) for r in positive_rows]
    positive_key_set = set(positive_keys)
    duplicate_positive_keys = int(len(positive_keys) - len(positive_key_set))

    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    pool_keys = [_row_key(r, columns) for r in pool_rows]
    duplicate_pool_keys = int(len(pool_keys) - len(set(pool_keys)))
    matched_keys: set[tuple[object, ...]] = set()
    for i, key in enumerate(pool_keys):
        if key in positive_key_set:
            labels[i] = 1
            matched_keys.add(key)

    positive_in_pool = int(labels.sum())
    diagnostics = {
        "positive_rows": int(len(positive_rows)),
        "positive_unique_keys": int(len(positive_key_set)),
        "positive_duplicate_keys": duplicate_positive_keys,
        "positive_in_pool": positive_in_pool,
        "positive_keys_matched": int(len(matched_keys)),
        "pool_duplicate_keys": duplicate_pool_keys,
        "match_mode": match_mode,
        "match_columns": columns,
    }
    if positive_in_pool <= 0:
        raise ValueError(
            "No positives matched the candidate pool. Check PROJECT_PU_ID_COLUMN / "
            "PROJECT_PU_MATCH_COLUMNS or use a fixed pool with inline label."
        )
    return labels, diagnostics


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
    diagnostics: dict | None = None,
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

    result = {
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
    if diagnostics:
        result.update(diagnostics)
    return result


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


def _scrub_sensitive_runtime_context() -> None:
    for key in [
        "PROJECT_PU_POSITIVE_CSV",
        "PROJECT_PU_GROUND_TRUTH_CSV",
    ]:
        os.environ.pop(key, None)
    sys.argv = [sys.argv[0]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Project PU Learning active-search runner")
    parser.add_argument("--mode", choices=["active_search"], default="active_search")
    parser.add_argument("--csv", required=True, help="large unlabeled CSV path or prebuilt candidate_pool CSV path")
    parser.add_argument("--positive_csv", default=os.environ.get("PROJECT_PU_POSITIVE_CSV", ""))
    parser.add_argument("--model_dir", default="model.py", help="selection policy implementation file")
    parser.add_argument("--pool_size", type=int, default=int(os.environ.get("PROJECT_PU_POOL_SIZE", "5000")))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("PROJECT_PU_BATCH_SIZE", "100")))
    parser.add_argument("--rounds", type=int, default=int(os.environ.get("PROJECT_PU_ROUNDS", "1")))
    parser.add_argument("--seed", type=int, default=int(os.environ.get("PROJECT_PU_SEED", "42")))
    parser.add_argument("--seed_queries", type=int, default=int(os.environ.get("PROJECT_PU_SEED_QUERIES", "0")))
    parser.add_argument("--fixed_pool", action="store_true")
    parser.add_argument("--id_column", default=os.environ.get("PROJECT_PU_ID_COLUMN", ""))
    parser.add_argument("--match_columns", default=os.environ.get("PROJECT_PU_MATCH_COLUMNS", ""))
    parser.add_argument("--state_path", default=os.environ.get("PROJECT_PU_STATE_PATH", ""))
    parser.add_argument("--resume_state", type=int, default=int(os.environ.get("PROJECT_PU_RESUME_STATE", "1")))
    args = parser.parse_args()

    candidate_fields, rows = _read_csv_rows(args.csv)
    csv_name = Path(args.csv).name
    use_fixed = bool(args.fixed_pool) or csv_name.startswith("candidate_pool_")
    pool_rows = list(rows) if use_fixed else _make_candidate_pool(rows, pool_size=int(args.pool_size), seed=int(args.seed))

    pool_rows, inline_labels = _extract_inline_labels(pool_rows)
    diagnostics: dict = {
        "task": "pu_active_search",
        "data_csv": str(Path(args.csv).expanduser()),
        "fixed_pool": bool(use_fixed),
    }
    if inline_labels is not None:
        labels = inline_labels
        diagnostics.update(
            {
                "label_source": "inline_label",
                "positive_in_pool": int(labels.sum()),
                "positive_rows": int(labels.sum()),
                "positive_unique_keys": int(labels.sum()),
                "match_mode": "inline_label",
                "match_columns": [],
            }
        )
        if int(labels.sum()) <= 0:
            raise ValueError("Inline label column contains no positives.")
    else:
        if not args.positive_csv:
            raise ValueError("Missing --positive_csv / PROJECT_PU_POSITIVE_CSV for PU label construction.")
        positive_fields, positive_rows = _read_csv_rows(args.positive_csv)
        labels, pu_diag = _make_pu_labels(
            pool_rows=pool_rows,
            positive_rows=positive_rows,
            positive_fields=positive_fields,
            candidate_fields=[c for c in candidate_fields if c != "label"],
            id_column=str(args.id_column or ""),
            match_columns=str(args.match_columns or ""),
        )
        diagnostics.update(pu_diag)
        diagnostics.update(
            {
                "label_source": "positive_set",
            }
        )

    _scrub_sensitive_runtime_context()
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
        diagnostics=diagnostics,
    )

    output_dir = Path(args.model_dir).expanduser().resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"metrics": {"test": metrics}}
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    state_payload = {
        "completed_rounds": int(metrics.get("rounds", completed_rounds)),
        "pool_size": int(len(pool_rows)),
        "top_k": int(labels.sum()),
        "batch_size": int(args.batch_size),
        "seed": int(args.seed),
        "queried_records": metrics.get("queried_records", []),
        "total_queries": int(metrics.get("total_queries", 0)),
        "total_hits": int(metrics.get("total_hits", 0)),
    }
    _save_state(state_path, state_payload)
    print(f"Metrics saved to {metrics_path}")
    print(f"State saved to {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
