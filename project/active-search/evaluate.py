#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def main() -> int:
    parser = argparse.ArgumentParser(description="Active Search evaluator")
    parser.add_argument("candidate_dir", type=Path)
    args = parser.parse_args()

    candidate_dir = args.candidate_dir.expanduser().resolve()
    metrics_path = candidate_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        print(f"Error: missing metrics file: {metrics_path}")
        return 1

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    test_metrics = payload.get("metrics", {}).get("test", {})
    if not test_metrics:
        print(f"Error: missing test metrics in {metrics_path}")
        return 1

    total_hits = int(test_metrics.get("total_hits", 0))
    total_queries = int(test_metrics.get("total_queries", 0))
    top_k = int(test_metrics.get("top_k", 0))

    ncg = test_metrics.get("ncg", None)
    try:
        ncg = float(ncg) if ncg is not None else None
    except Exception:
        ncg = None

    delta_hits = test_metrics.get("delta_hits", None)
    delta_queries = test_metrics.get("delta_queries", None)
    try:
        delta_hits = int(delta_hits) if delta_hits is not None else None
    except Exception:
        delta_hits = None
    try:
        delta_queries = int(delta_queries) if delta_queries is not None else None
    except Exception:
        delta_queries = None

    if delta_hits is None or delta_queries is None:
        round_details = test_metrics.get("round_details", [])
        if isinstance(round_details, list) and round_details:
            try:
                dh = sum(int(it.get("hits", 0)) for it in round_details if isinstance(it, dict))
                dq = sum(int(it.get("queried", 0)) for it in round_details if isinstance(it, dict))
                delta_hits = dh
                delta_queries = dq
            except Exception:
                delta_hits = None
                delta_queries = None

    if delta_hits is None:
        delta_hits = int(total_hits)
    if delta_queries is None:
        delta_queries = int(total_queries)

    delta_precision = float(delta_hits / max(1, delta_queries))
    score_100 = clamp(delta_precision, 0.0, 1.0) * 100.0

    results = {
        "final_score": round(score_100, 1),
        "category_scores": {
            "delta_precision": round(score_100, 1),
        },
        "scenario_scores": {
            "delta_hits": int(delta_hits),
            "delta_queries": int(delta_queries),
            "delta_precision": float(delta_precision),
            "total_hits": int(total_hits),
            "top_k": int(top_k),
            "total_queries": int(total_queries),
            "ncg": ncg,
            "ncg_k": int(test_metrics.get("ncg_k", 0)),
            "ncg_selected_sum": float(test_metrics.get("ncg_selected_sum", 0.0)),
            "ncg_topk_sum": float(test_metrics.get("ncg_topk_sum", 0.0)),
            "pool_size": int(test_metrics.get("pool_size", 0)),
            "batch_size": int(test_metrics.get("batch_size", 0)),
            "rounds": int(test_metrics.get("rounds", 0)),
            "seed": int(test_metrics.get("seed", 0)),
            "auc_normalized": float(test_metrics.get("auc_normalized", 0.0)),
        },
        "total_scenarios": 1,
        "evaluated_at": datetime.now().isoformat(),
    }

    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())

