import argparse
import ast
import csv
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np


def _find_biodiscovery_datasets_dir(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if p.exists() and p.is_dir():
            return p
        raise ValueError(f"datasets_dir does not exist: {p}")

    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        cand = parent / "BioDiscoveryAgent" / "datasets"
        if cand.exists() and cand.is_dir():
            return cand
    raise ValueError("Could not locate BioDiscoveryAgent/datasets; pass --datasets_dir explicitly")


def _load_task_prompt(datasets_dir: Path, data_name: str) -> dict[str, object]:
    p = datasets_dir / "task_prompts" / f"{data_name}.json"
    if not p.exists():
        return {}
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return obj if isinstance(obj, dict) else {}


def _load_ground_truth(datasets_dir: Path, data_name: str) -> tuple[list[object], np.ndarray, dict[object, float], bool]:
    path = datasets_dir / f"ground_truth_{data_name}.csv"
    if not path.exists():
        raise FileNotFoundError(str(path))

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            raise ValueError(f"Empty CSV: {path}")

        is_pair = "Gene_pairs" in header
        id_idx = header.index("Gene_pairs") if is_pair else (header.index("Gene") if "Gene" in header else 0)
        score_idx = header.index("Score") if "Score" in header else (1 if len(header) > 1 else 0)

        ids: list[object] = []
        scores: list[float] = []
        if is_pair:
            for row in reader:
                if len(row) <= max(id_idx, score_idx):
                    continue
                try:
                    pair = ast.literal_eval(row[id_idx])
                except Exception:
                    continue
                if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                    continue
                a, b = str(pair[0]), str(pair[1])
                try:
                    score = float(row[score_idx])
                except Exception:
                    continue
                ids.append((a, b))
                scores.append(score)
        else:
            for row in reader:
                if len(row) <= max(id_idx, score_idx):
                    continue
                gene = str(row[id_idx]).strip()
                if not gene:
                    continue
                try:
                    score = float(row[score_idx])
                except Exception:
                    continue
                ids.append(gene)
                scores.append(score)

    scores_arr = np.asarray(scores, dtype=float)
    score_map: dict[object, float] = dict(zip(ids, scores_arr.tolist()))
    return ids, scores_arr, score_map, is_pair


def _normalize_topmovers(arr: object, is_pair: bool) -> set[object]:
    if arr is None:
        return set()
    items = arr.tolist() if isinstance(arr, np.ndarray) else list(arr)
    out: set[object] = set()
    for x in items:
        if is_pair:
            if isinstance(x, (list, tuple, np.ndarray)) and len(x) == 2:
                out.add((str(x[0]), str(x[1])))
            elif isinstance(x, str) and "_" in x:
                a, b = x.split("_", 1)
                out.add((a, b))
        else:
            out.add(str(x))
    return out


def _load_topmovers(datasets_dir: Path, data_name: str, is_pair: bool) -> set[object] | None:
    path = datasets_dir / f"topmovers_{data_name}.npy"
    if not path.exists():
        return None
    arr = np.load(str(path), allow_pickle=True)
    return _normalize_topmovers(arr, is_pair=is_pair)



def _jsonify_value(v: object, max_str_len: int) -> object:
    if v is None:
        return None
    if isinstance(v, (bool, int, float)):
        if isinstance(v, float) and not np.isfinite(v):
            return 0.0
        return v
    if isinstance(v, str):
        return v if len(v) <= max_str_len else v[:max_str_len]
    try:
        x = float(v)
        if not np.isfinite(x):
            return 0.0
        return x
    except Exception:
        s = str(v)
        return s if len(s) <= max_str_len else s[:max_str_len]


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


def _compute_ncg(
    ids: list[object],
    scores_arr: np.ndarray,
    score_map: dict[object, float],
    selected_set: set[object],
    use_abs_gain: bool,
) -> float:
    pred_in_lib = [x for x in selected_set if x in score_map]
    k = len(pred_in_lib)
    if k == 0:
        return float("nan")

    gains_arr = np.abs(scores_arr) if use_abs_gain else scores_arr
    topk = np.sort(gains_arr)[::-1][:k]
    denom = float(np.sum(topk))
    if denom == 0.0 or np.isnan(denom):
        return float("nan")
    numer = float(np.sum([abs(score_map[x]) if use_abs_gain else score_map[x] for x in pred_in_lib]))
    return numer / denom


def _load_state(path: str) -> dict:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return {}
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _save_state(path: str, payload: dict) -> None:
    p = Path(path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _build_history_from_records(
    candidates: list[dict[str, object]],
    score_map: dict[object, float],
    hit_set: set[object],
    is_pair: bool,
    records: list[dict[str, object]],
) -> tuple[list[dict[str, object]], set[int], int, int]:
    history: list[dict[str, object]] = []
    already_selected: set[int] = set()
    total_hits = 0
    total_queries = 0
    n = len(candidates)
    for rec in records:
        try:
            idx = int(rec.get("candidate_index", -1))
        except Exception:
            continue
        if idx < 0 or idx >= n or idx in already_selected:
            continue
        row = dict(candidates[idx])
        row["candidate_index"] = idx
        key = (row.get("gene_a"), row.get("gene_b")) if is_pair else row.get("gene")
        score = float(score_map.get(key, 0.0))
        row["score"] = score
        row["hit"] = 1 if key in hit_set else 0
        history.append(row)
        already_selected.add(idx)
        total_queries += 1
        total_hits += int(row["hit"])
    return history, already_selected, total_queries, total_hits


def run_bda_active_search(
    candidates: list[dict[str, object]],
    ids: list[object],
    scores_arr: np.ndarray,
    score_map: dict[object, float],
    hit_set: set[object],
    use_abs_gain: bool,
    select_fn,
    steps: int,
    batch_size: int,
    seed: int,
    include_hit_in_history: bool,
    initial_history: list[dict[str, object]] | None = None,
    initial_already_selected: set[int] | None = None,
    start_round: int = 0,
) -> dict:
    n = len(candidates)
    already_selected: set[int] = set(initial_already_selected or set())
    history: list[dict[str, object]] = [dict(r) for r in (initial_history or [])]
    baseline_total_queries = int(len(history))
    baseline_total_hits = int(sum(int(r.get("hit", 0)) for r in history))

    hit_curve_queries: list[int] = [baseline_total_queries]
    hit_curve_hits: list[int] = [baseline_total_hits]
    per_round: list[dict[str, object]] = []

    cumulative_hits = baseline_total_hits
    total_queries = baseline_total_queries

    for r in range(int(steps)):
        round_seed = int(seed) + int(start_round) + int(r)
        sanitized_history: list[dict[str, object]] = []
        for row in history:
            rr = dict(row)
            if not include_hit_in_history and "hit" in rr:
                rr.pop("hit", None)
            sanitized_history.append(rr)

        selected_raw = select_fn(candidates, sanitized_history, int(batch_size), int(round_seed))
        selected = _sanitize_selected_indices(
            selected=selected_raw,
            n=n,
            already_selected=already_selected,
            batch_size=int(batch_size),
            seed=int(round_seed),
        )

        hits_t = 0
        selected_genes: list[str] = []
        selected_scores: list[float] = []
        selected_hits: list[int] = []
        for idx in selected:
            row = dict(candidates[idx])
            row["candidate_index"] = int(idx)
            key = (row.get("gene_a"), row.get("gene_b")) if "gene_a" in row and "gene_b" in row else row.get("gene")
            score = float(score_map.get(key, 0.0))
            is_hit = 1 if key in hit_set else 0
            row["score"] = score
            row["hit"] = int(is_hit)
            row["round"] = int(start_round + r)
            history.append(row)
            already_selected.add(int(idx))

            total_queries += 1
            hits_t += int(is_hit)
            cumulative_hits += int(is_hit)

            if isinstance(key, tuple) and len(key) == 2:
                selected_genes.append(f"{key[0]} + {key[1]}")
            else:
                selected_genes.append(str(key))
            selected_scores.append(score)
            selected_hits.append(int(is_hit))

        hit_curve_queries.append(int(total_queries))
        hit_curve_hits.append(int(cumulative_hits))
        per_round.append(
            {
                "round": int(start_round + r),
                "selected_count": int(len(selected)),
                "hits": int(hits_t),
                "cumulative_hits": int(cumulative_hits),
                "precision_at_batch": float(hits_t / max(1, int(len(selected)))),
                "selected": selected_genes,
                "selected_scores": [float(_jsonify_value(x, max_str_len=32)) for x in selected_scores],
                "selected_hits": selected_hits,
            }
        )

    area = 0.0
    for i in range(1, len(hit_curve_queries)):
        x0, x1 = float(hit_curve_queries[i - 1]), float(hit_curve_queries[i])
        y0, y1 = float(hit_curve_hits[i - 1]), float(hit_curve_hits[i])
        area += (x1 - x0) * (y0 + y1) / 2.0

    top_k = int(len(hit_set))
    auc_norm = float(area / max(1.0, float(hit_curve_queries[-1]) * float(max(1, top_k))))

    selected_set: set[object] = set()
    queried_records: list[dict[str, object]] = []
    queried_history: list[dict[str, object]] = []
    for row in history:
        idx = int(row.get("candidate_index", -1))
        if idx < 0:
            continue
        key = (row.get("gene_a"), row.get("gene_b")) if "gene_a" in row and "gene_b" in row else row.get("gene")
        selected_set.add(key)
        rec = {
            "candidate_index": idx,
            "gene": str(key) if not (isinstance(key, tuple) and len(key) == 2) else f"{key[0]} + {key[1]}",
            "score": float(_jsonify_value(row.get("score", 0.0), max_str_len=64)),
            "hit": int(row.get("hit", 0) or 0),
            "round": int(row.get("round", 0) or 0),
        }
        queried_records.append(rec)
        queried_history.append({k: _jsonify_value(v, max_str_len=500) for k, v in rec.items()})

    ncg = _compute_ncg(
        ids=ids,
        scores_arr=scores_arr,
        score_map=score_map,
        selected_set=selected_set,
        use_abs_gain=use_abs_gain,
    )

    return {
        "pool_size": int(n),
        "rounds": int(start_round + steps),
        "executed_rounds": int(steps),
        "batch_size": int(batch_size),
        "seed": int(seed),
        "baseline_total_queries": int(baseline_total_queries),
        "baseline_total_hits": int(baseline_total_hits),
        "delta_queries": int(total_queries - baseline_total_queries),
        "delta_hits": int(cumulative_hits - baseline_total_hits),
        "total_queries": int(total_queries),
        "total_hits": int(cumulative_hits),
        "top_k": int(top_k),
        "hit_curve": {"queries": hit_curve_queries, "hits": hit_curve_hits},
        "auc": float(area),
        "auc_normalized": float(auc_norm),
        "ncg": float(ncg) if np.isfinite(ncg) else float("nan"),
        "round_details": per_round,
        "queried_records": queried_records,
        "queried_history": queried_history,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["bda_active_search"], default="bda_active_search")
    parser.add_argument("--data_name", required=True)
    parser.add_argument("--task", default=os.environ.get("BDA_TASK", "perturb-genes-brief"))
    parser.add_argument("--steps", type=int, default=int(os.environ.get("BDA_STEPS", "5")))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("BDA_NUM_GENES", "128")))
    parser.add_argument("--seed", type=int, default=int(os.environ.get("BDA_SEED", "42")))
    parser.add_argument("--model_dir", required=True)
    parser.add_argument("--datasets_dir", default=os.environ.get("BDA_DATASETS_DIR", ""))
    parser.add_argument("--state_path", default=os.environ.get("BDA_STATE_PATH", ""))
    parser.add_argument("--resume_state", type=int, default=int(os.environ.get("BDA_RESUME_STATE", "1")))
    parser.add_argument("--include_hit_in_history", type=int, default=int(os.environ.get("BDA_INCLUDE_HIT_IN_HISTORY", "1")))
    args = parser.parse_args()

    datasets_dir = _find_biodiscovery_datasets_dir(args.datasets_dir or None)
    task_prompt = _load_task_prompt(datasets_dir, args.data_name)
    ids, scores_arr, score_map, is_pair = _load_ground_truth(datasets_dir, args.data_name)
    topmovers = _load_topmovers(datasets_dir, args.data_name, is_pair=is_pair)
    use_abs_gain = topmovers is not None
    if topmovers is None:
        tau = float(np.percentile(scores_arr, 90))
        hit_set: set[object] = set(ids[i] for i, s in enumerate(scores_arr) if float(s) >= tau)
    else:
        hit_set = set(topmovers)

    candidates: list[dict[str, object]] = []
    if is_pair:
        for a, b in ids:
            candidates.append({"gene_a": a, "gene_b": b})
    else:
        for g in ids:
            candidates.append({"gene": g})

    if not is_pair and str(os.environ.get("BDA_GENE_SEARCH", "0")).strip() == "1":
        csv_dir = str(os.environ.get("BDA_CSV_PATH", "")).strip()
        if csv_dir:
            ach_path = str((Path(csv_dir).expanduser().resolve() / "achilles.csv"))
            try:
                from bda_tools import init_gene_search
            except Exception:
                init_gene_search = None
            if init_gene_search is not None:
                init_gene_search(ach_path, [str(c.get("gene", "")).strip() for c in candidates])

    select_fn = _load_selection_policy(args.model_dir)

    model_path = Path(args.model_dir).expanduser().resolve()
    output_dir = model_path.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    default_state_path = output_dir / "bda_state.json"
    state_path = Path(args.state_path).expanduser().resolve() if args.state_path else default_state_path

    state = _load_state(str(state_path)) if int(args.resume_state) != 0 else {}
    record_list: list[dict[str, object]] = []
    completed_rounds = 0
    if state:
        records = state.get("queried_records", [])
        record_list = records if isinstance(records, list) else []
        try:
            completed_rounds = int(state.get("completed_rounds", 0))
        except Exception:
            completed_rounds = 0

    history, already_selected, _, _ = _build_history_from_records(
        candidates=candidates,
        score_map=score_map,
        hit_set=hit_set,
        is_pair=is_pair,
        records=record_list,
    )

    metrics = run_bda_active_search(
        candidates=candidates,
        ids=ids,
        scores_arr=scores_arr,
        score_map=score_map,
        hit_set=hit_set,
        use_abs_gain=bool(use_abs_gain),
        select_fn=select_fn,
        steps=int(args.steps),
        batch_size=int(args.batch_size),
        seed=int(args.seed),
        include_hit_in_history=bool(int(args.include_hit_in_history)),
        initial_history=history,
        initial_already_selected=already_selected,
        start_round=int(completed_rounds),
    )

    payload: dict[str, object] = {
        "task": str(args.task),
        "data_name": str(args.data_name),
        "measurement": str(task_prompt.get("Measurement", "")),
        "task_prompt": task_prompt,
        "metrics": {"test": metrics},
    }
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    state_payload = {
        "completed_rounds": int(metrics.get("rounds", completed_rounds)),
        "pool_size": int(metrics.get("pool_size", len(candidates))),
        "batch_size": int(metrics.get("batch_size", args.batch_size)),
        "seed": int(args.seed),
        "queried_records": metrics.get("queried_records", []),
        "total_queries": int(metrics.get("total_queries", 0)),
        "total_hits": int(metrics.get("total_hits", 0)),
    }
    _save_state(str(state_path), state_payload)

    print(f"Metrics saved to {metrics_path}")
    print(f"State saved to {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
