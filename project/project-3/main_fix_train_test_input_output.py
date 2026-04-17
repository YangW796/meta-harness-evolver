import argparse
import csv
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np

_INDEX_IMPORT_PATH: str | None = None
try:
    _INDEX_IMPORT_PATH = str(Path(__file__).resolve().parents[4])
except IndexError:
    _INDEX_IMPORT_PATH = None

if _INDEX_IMPORT_PATH is not None:
    sys.path.insert(0, _INDEX_IMPORT_PATH)
else:
    for p in Path(__file__).resolve().parents:
        if (p / "index.py").exists():
            _INDEX_IMPORT_PATH = str(p)
            sys.path.insert(0, _INDEX_IMPORT_PATH)
            break

from index import compute_x

_SCRIPT_DIR = str(Path(__file__).resolve().parent)
for _p in [_INDEX_IMPORT_PATH, _SCRIPT_DIR, ""]:
    if _p and _p in sys.path:
        while _p in sys.path:
            sys.path.remove(_p)
sys.modules.pop("index", None)


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


def _make_ground_truth_labels(pool_rows: list[dict[str, object]], top_k: int) -> np.ndarray:
    if not pool_rows:
        return np.zeros((0,), dtype=np.int8)
    k = int(max(0, min(int(top_k), len(pool_rows))))
    y = np.asarray(compute_x(pool_rows), dtype=np.float64).reshape(-1)
    order = np.argsort(-y, kind="mergesort")
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    if k > 0:
        labels[order[:k]] = 1
    return labels


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


def run_active_search(
    pool_rows: list[dict[str, object]],
    labels: np.ndarray,
    select_fn,
    rounds: int,
    batch_size: int,
    seed: int,
    seed_queries: int,
) -> dict:
    n = int(len(pool_rows))
    already_selected: set[int] = set()
    history: list[dict[str, object]] = []

    rng = np.random.default_rng(int(seed))
    if seed_queries > 0 and n > 0:
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

    for t in range(int(rounds)):
        selected_raw = select_fn(pool_rows, history, int(batch_size), int(seed) + t)
        selected = _sanitize_selected_indices(
            selected_raw, n=n, already_selected=already_selected, batch_size=int(batch_size), seed=int(seed) + 10_000 + t
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

        per_round.append(
            {
                "round": int(t + 1),
                "queried": int(len(selected)),
                "hits": int(hits_t),
                "cumulative_hits": int(cumulative_hits),
                "precision_at_batch": float(hits_t / max(1, int(len(selected)))),
            }
        )

    top_k = int(labels.sum())
    recall = float(cumulative_hits / max(1, top_k))

    area = 0.0
    for i in range(1, len(hit_curve_queries)):
        x0, x1 = float(hit_curve_queries[i - 1]), float(hit_curve_queries[i])
        y0, y1 = float(hit_curve_hits[i - 1]), float(hit_curve_hits[i])
        area += (x1 - x0) * (y0 + y1) / 2.0
    auc_norm = float(area / max(1.0, float(hit_curve_queries[-1]) * float(max(1, top_k))))

    return {
        "pool_size": int(n),
        "top_k": int(top_k),
        "rounds": int(rounds),
        "batch_size": int(batch_size),
        "seed": int(seed),
        "seed_queries": int(seed_queries),
        "total_queries": int(total_queries),
        "total_hits": int(cumulative_hits),
        "recall": recall,
        "auc": float(area),
        "auc_normalized": auc_norm,
        "hit_curve": {"queries": hit_curve_queries, "hits": hit_curve_hits},
        "round_details": per_round,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["active_search"], default="active_search")
    parser.add_argument("--csv", required=True, help="large candidate CSV path")
    parser.add_argument("--model_dir", default="model.py", help="selection policy implementation file")
    parser.add_argument("--pool_size", type=int, default=int(os.environ.get("PROJECT3_POOL_SIZE", "5000")))
    parser.add_argument("--top_k", type=int, default=int(os.environ.get("PROJECT3_TOP_K", "1000")))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("PROJECT3_BATCH_SIZE", "100")))
    parser.add_argument("--rounds", type=int, default=int(os.environ.get("PROJECT3_ROUNDS", "10")))
    parser.add_argument("--seed", type=int, default=int(os.environ.get("PROJECT3_SEED", "42")))
    parser.add_argument("--seed_queries", type=int, default=int(os.environ.get("PROJECT3_SEED_QUERIES", "0")))
    args = parser.parse_args()

    rows = _read_csv_rows(args.csv)
    pool_rows = _make_candidate_pool(rows, pool_size=int(args.pool_size), seed=int(args.seed))
    labels = _make_ground_truth_labels(pool_rows, top_k=int(args.top_k))
    select_fn = _load_selection_policy(args.model_dir)

    metrics = run_active_search(
        pool_rows=pool_rows,
        labels=labels,
        select_fn=select_fn,
        rounds=int(args.rounds),
        batch_size=int(args.batch_size),
        seed=int(args.seed),
        seed_queries=int(args.seed_queries),
    )

    output_dir = Path(args.model_dir).expanduser().resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"metrics": {"test": metrics}}
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Metrics saved to {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
