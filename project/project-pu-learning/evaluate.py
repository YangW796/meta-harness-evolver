#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path


def _safe_float(x) -> float | None:
    try:
        v = float(x)
    except Exception:
        return None
    if math.isfinite(v):
        return v
    return None


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def main() -> int:
    parser = argparse.ArgumentParser(description="Project PU evaluator")
    parser.add_argument("candidate_dir", type=Path)
    args = parser.parse_args()

    candidate_dir = args.candidate_dir.expanduser().resolve()
    metrics_path = candidate_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        print(json.dumps({"error": f"missing metrics.json: {metrics_path}"}))
        return 1

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    all_stats = payload.get("score_stats_all", {}) or {}
    kept_stats = payload.get("score_stats_kept", {}) or {}
    removed_stats = payload.get("score_stats_removed", {}) or {}

    mean_all = _safe_float(all_stats.get("mean"))
    p25_all = _safe_float(all_stats.get("p25"))
    p75_all = _safe_float(all_stats.get("p75"))
    mean_kept = _safe_float(kept_stats.get("mean"))
    mean_removed = _safe_float(removed_stats.get("mean"))

    removed_n = int(payload.get("removed_n", 0) or 0)
    kept_n = int(payload.get("kept_n", 0) or 0)
    u_rows = int(payload.get("u_rows", 0) or 0)

    if mean_kept is None or mean_removed is None:
        print(json.dumps({"error": "missing kept/removed score means in metrics.json"}))
        return 1

    iqr = None
    if p25_all is not None and p75_all is not None:
        iqr = p75_all - p25_all
    if iqr is None or not math.isfinite(iqr) or abs(iqr) < 1e-9:
        iqr = 1.0

    gap = mean_kept - mean_removed
    norm_gap = float(gap / iqr)
    score_100 = _clamp(_sigmoid(norm_gap) * 100.0, 0.0, 100.0)

    results = {
        "final_score": round(score_100, 3),
        "category_scores": {
            "separation": round(score_100, 3),
        },
        "scenario_scores": {
            "u_rows": u_rows,
            "kept_n": kept_n,
            "removed_n": removed_n,
            "mean_all": mean_all,
            "mean_kept": mean_kept,
            "mean_removed": mean_removed,
            "gap": float(gap),
            "iqr_all": float(iqr),
            "normalized_gap": float(norm_gap),
        },
        "total_scenarios": 1,
        "evaluated_at": datetime.now().isoformat(),
    }
    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())

