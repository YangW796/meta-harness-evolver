#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def score_from_metrics(test_metrics: dict) -> tuple[float, dict]:
    r2 = float(test_metrics.get("r2", -1.0))
    rmse = float(test_metrics.get("rmse", 1e6))
    mae = float(test_metrics.get("mae", 1e6))
    pearson = float(test_metrics.get("pearson", -1.0))

    # Convert to 0-100, emphasizing R^2 while keeping error metrics informative.
    r2_score = clamp((r2 + 1.0) / 2.0, 0.0, 1.0) * 100.0
    pearson_score = clamp((pearson + 1.0) / 2.0, 0.0, 1.0) * 100.0
    rmse_score = clamp(100.0 / (1.0 + rmse), 0.0, 100.0)
    mae_score = clamp(100.0 / (1.0 + mae), 0.0, 100.0)

    final_score = 0.65 * r2_score + 0.15 * pearson_score + 0.10 * rmse_score + 0.10 * mae_score
    category_scores = {
        "r2": round(r2_score, 1),
        "pearson": round(pearson_score, 1),
        "rmse_inverse": round(rmse_score, 1),
        "mae_inverse": round(mae_score, 1),
    }
    return round(final_score, 1), category_scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Project-1 evaluator")
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

    final_score, category_scores = score_from_metrics(test_metrics)

    results = {
        "final_score": final_score,
        "category_scores": category_scores,
        "scenario_scores": {
            "test_r2": round(float(test_metrics.get("r2", -1.0)), 4),
            "test_rmse": round(float(test_metrics.get("rmse", 1e6)), 4),
            "test_mae": round(float(test_metrics.get("mae", 1e6)), 4),
            "test_pearson": round(float(test_metrics.get("pearson", -1.0)), 4),
        },
        "total_scenarios": 4,
        "evaluated_at": datetime.now().isoformat(),
    }

    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
