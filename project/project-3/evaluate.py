#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def main() -> int:
    parser = argparse.ArgumentParser(description="Project-3 evaluator (Active Search)")
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
    top_k = int(test_metrics.get("top_k", 0))
    hit_ratio = float(total_hits / max(1, top_k))
    score_100 = clamp(hit_ratio, 0.0, 1.0) * 100.0

    results = {
        "final_score": round(score_100, 1),
        "category_scores": {
            "total_hits_ratio": round(score_100, 1),
        },
        "scenario_scores": {
            "total_hits": int(total_hits),
            "top_k": int(top_k),
            "total_queries": int(test_metrics.get("total_queries", 0)),
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
