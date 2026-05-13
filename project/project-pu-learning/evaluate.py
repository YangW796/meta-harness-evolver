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


def main() -> int:
    parser = argparse.ArgumentParser(description="Project PU evaluator")
    parser.add_argument("candidate_dir", type=Path)
    args = parser.parse_args()

    candidate_dir = args.candidate_dir.expanduser().resolve()
    metrics_path = candidate_dir / "outputs" / "metrics.json"
    legacy_metrics_path = candidate_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        metrics_path = legacy_metrics_path
    if not metrics_path.exists():
        print(json.dumps({"error": f"missing metrics.json: tried {candidate_dir / 'outputs' / 'metrics.json'} and {legacy_metrics_path}"}))
        return 1

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    metric_mode = str(payload.get("metric_mode", "topk") or "topk").strip().lower()
    f1 = _safe_float(payload.get("f1"))
    precision = _safe_float(payload.get("precision"))
    recall = _safe_float(payload.get("recall"))

    eval_payload = payload.get("eval", {}) or {}
    best_f1 = _safe_float(eval_payload.get("best_f1"))
    best_precision = _safe_float(eval_payload.get("best_precision"))
    best_recall = _safe_float(eval_payload.get("best_recall"))
    best_k = payload.get("eval", {}).get("best_k", None) if isinstance(payload.get("eval", {}), dict) else None

    if metric_mode in {"maxf1", "u_maxf1"}:
        f1 = best_f1 if best_f1 is not None else f1
        precision = best_precision if best_precision is not None else precision
        recall = best_recall if best_recall is not None else recall

    if f1 is None or not math.isfinite(float(f1)):
        print(json.dumps({"error": "missing f1 in metrics.json"}))
        return 1

    score_100 = float(f1) * 100.0

    results = {
        "final_score": round(float(score_100), 3),
        "category_scores": {
            "f1": round(float(score_100), 3),
        },
        "scenario_scores": {
            "metric_mode": metric_mode,
            "p_rows": int(payload.get("p_rows", 0) or 0),
            "p_train_rows": int(payload.get("p_train_rows", 0) or 0),
            "p_test_rows": int(payload.get("p_test_rows", 0) or 0),
            "u_rows": int(payload.get("u_rows", 0) or 0),
            "used_k": payload.get("used_k", None),
            "used_threshold": payload.get("used_threshold", None),
            "precision": precision,
            "recall": recall,
            "f1": float(f1),
            "best_k": best_k,
            "best_precision": best_precision,
            "best_recall": best_recall,
            "best_f1": best_f1,
            "p_test_eval": payload.get("breakdown", {}).get("p_test") if isinstance(payload.get("breakdown", {}), dict) else None,
            "u_test_eval": payload.get("breakdown", {}).get("u_test") if isinstance(payload.get("breakdown", {}), dict) else None,
            "all_eval": payload.get("breakdown", {}).get("all") if isinstance(payload.get("breakdown", {}), dict) else None,
        },
        "total_scenarios": 1,
        "evaluated_at": datetime.now().isoformat(),
    }
    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
