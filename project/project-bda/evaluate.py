from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py <candidate_dir>", file=sys.stderr)
        return 2
    candidate_dir = Path(sys.argv[1]).expanduser().resolve()
    metrics_path = candidate_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        print(json.dumps({"error": f"Missing metrics.json at {metrics_path}", "final_score": 0}), flush=True)
        return 0

    try:
        payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error": f"Failed to parse metrics.json: {e}", "final_score": 0}), flush=True)
        return 0

    test = ((payload.get("metrics") or {}).get("test") or {}) if isinstance(payload, dict) else {}
    try:
        total_hits = int(test.get("total_hits", 0))
    except Exception:
        total_hits = 0
    try:
        top_k = int(test.get("top_k", 0))
    except Exception:
        top_k = 0
    try:
        ncg = float(test.get("ncg", float("nan")))
    except Exception:
        ncg = float("nan")

    if math.isfinite(ncg):
        final_score = _clamp(ncg, 0.0, 1.0) * 100.0
    else:
        recall = float(total_hits / max(1, top_k)) if top_k > 0 else 0.0
        final_score = _clamp(recall, 0.0, 1.0) * 100.0

    out = {
        "final_score": float(final_score),
        "total_hits": int(total_hits),
        "top_k": int(top_k),
        "ncg": float(ncg) if math.isfinite(ncg) else None,
        "auc_normalized": test.get("auc_normalized"),
        "total_queries": test.get("total_queries"),
        "data_name": payload.get("data_name") if isinstance(payload, dict) else None,
        "task": payload.get("task") if isinstance(payload, dict) else None,
    }
    print(json.dumps(out), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

