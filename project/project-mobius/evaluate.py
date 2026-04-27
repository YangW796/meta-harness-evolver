#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _get_nested(d: dict, path: list[str]):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def _find_checkpoint(checkpoint_dir: Path) -> Path | None:
    last_ckpt = checkpoint_dir / "last.ckpt"
    if last_ckpt.exists():
        return last_ckpt
    ckpts = sorted(checkpoint_dir.glob("*.ckpt"), key=lambda p: p.stat().st_mtime, reverse=True)
    return ckpts[0] if ckpts else None


def _resolve_mobius_home(script_dir: Path) -> Path:
    env = os.environ.get("MOBIUS_HOME", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    repo_root = (script_dir / "../../..").resolve()
    return (repo_root / "mobius").resolve()


def _maybe_analyze_from_checkpoint(candidate_dir: Path, metrics_path: Path) -> tuple[str | None, float | None, dict | None]:
    harness_dir = candidate_dir / "harness"
    run_output_dir = harness_dir / "outputs" / "mobius_run"
    config_path = run_output_dir / "config.yaml"
    checkpoint_dir = run_output_dir / "checkpoints"
    if not config_path.exists() or not checkpoint_dir.exists():
        return None, None, None

    checkpoint = _find_checkpoint(checkpoint_dir)
    if checkpoint is None:
        return None, None, None

    mobius_home = _resolve_mobius_home(metrics_path.parent)
    analyze_script = mobius_home / "scripts" / "analyze_test_predictions.py"
    if not analyze_script.exists():
        return None, None, None

    analysis_dir = run_output_dir / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    output_csv = analysis_dir / "test_predictions.csv"
    summary_json = analysis_dir / "test_predictions.summary.json"

    cmd = [
        sys.executable,
        str(analyze_script),
        "--config",
        str(config_path),
        "--checkpoint",
        str(checkpoint),
        "--output-csv",
        str(output_csv),
        "--summary-json",
        str(summary_json),
        "--device",
        "auto",
        "--num-workers",
        "0",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not summary_json.exists():
        return None, None, None

    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    metrics = summary.get("metrics", {})
    if not isinstance(metrics, dict):
        return None, None, None

    if "ndcg@100" in metrics:
        return "test/rerank/ndcg@100", float(metrics["ndcg@100"]), summary
    if "score_spearman" in metrics:
        return "test/rerank/score_spearman", float(metrics["score_spearman"]), summary
    return None, None, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Project-Mobius evaluator (reranking)")
    parser.add_argument("candidate_dir", type=Path)
    args = parser.parse_args()

    candidate_dir = args.candidate_dir.expanduser().resolve()
    metrics_path = candidate_dir / "harness" / "outputs" / "metrics.json"
    if not metrics_path.exists():
        print(f"Error: missing metrics file: {metrics_path}")
        return 1

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}

    primary_name = None
    primary_value = None
    primary = payload.get("primary_metric", None)
    if isinstance(primary, dict):
        primary_name = primary.get("name", None)
        primary_value = primary.get("value", None)

    if primary_value is None:
        primary_name = "test/rerank/ndcg@100"
        primary_value = _get_nested(metrics, ["test", "rerank", "ndcg@100"])

    if primary_value is None:
        primary_name = "test/rerank/score_spearman"
        primary_value = _get_nested(metrics, ["test", "rerank", "score_spearman"])

    summary = None
    if primary_value is None:
        primary_name, primary_value, summary = _maybe_analyze_from_checkpoint(candidate_dir, metrics_path)

    if primary_value is None:
        print(f"Error: missing primary metric in {metrics_path}")
        return 1

    try:
        primary_value_f = float(primary_value)
    except Exception:
        print(f"Error: invalid primary metric value for {primary_name}: {primary_value!r}")
        return 1

    if primary_name.endswith("ndcg@100"):
        score_100 = clamp(primary_value_f, 0.0, 1.0) * 100.0
    else:
        score_100 = clamp((primary_value_f + 1.0) / 2.0, 0.0, 1.0) * 100.0

    results = {
        "final_score": round(score_100, 3),
        "category_scores": {
            "primary_metric": round(score_100, 3),
        },
        "scenario_scores": {
            "primary_name": primary_name,
            "primary_value": primary_value_f,
            "source": "analyze_test_predictions" if summary is not None else "metrics.json",
        },
        "total_scenarios": 1,
        "evaluated_at": datetime.now().isoformat(),
    }
    print(json.dumps(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
