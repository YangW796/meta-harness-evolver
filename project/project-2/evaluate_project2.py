#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def main() -> int:
    parser = argparse.ArgumentParser(description="Project-2 evaluator")
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

    f1 = float(test_metrics.get("f1", 0.0))
    f1_score_100 = clamp(f1, 0.0, 1.0) * 100.0

    results = {
        "final_score": round(f1_score_100, 1),
        "category_scores": {
            "topk_f1": round(f1_score_100, 1),
        },
        "scenario_scores": {
            "test_f1": round(f1, 6),
            "top_ratio": float(test_metrics.get("top_ratio", 0.1)),
            "top_k": int(test_metrics.get("top_k", 0)),
            "num_samples": int(test_metrics.get("num_samples", 0)),
        },
        "total_scenarios": 1,
        "evaluated_at": datetime.now().isoformat(),
    }

    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
