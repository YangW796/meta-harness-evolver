#!/usr/bin/env python3
"""
Meta-Harness Evolution Loop — Main Entry Point

Runs the full Meta-Harness outer loop:
  1. Read prior candidates from <workspace>/candidates/
  2. Spawn proposer sub-agent to propose a new candidate
  3. Validate the candidate
  4. Evaluate against benchmark
  5. Log results
  6. Post summary to Feishu

Usage:
  python3 run_evolution.py [--workspace DIR] [--candidate-num N] [--iterations K] [--evaluate-script PATH]

Exit codes:
  0 = success (candidate evaluated)
  1 = skipped (no valid candidate produced)
  2 = error
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from evolver_config import load_config
from evaluation_runner import collect_change_record, evaluate_candidate, log_evolution, post_to_feishu, update_best
from evolution_paths import EvolverPaths, get_next_candidate_num
from harness_runner import run_harness_script, validate_candidate
from proposer_runner import run_proposer
from shared import get_workspace, load_env_file

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
ENV_FILE = ROOT_DIR / ".env"
load_env_file(ENV_FILE)
def main():
    parser = argparse.ArgumentParser(description="Meta-Harness Evolution Loop")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Evolution workspace directory (default: $EVOLVER_WORKSPACE or ~/hoss-evolution)",
    )
    parser.add_argument("--candidate-num", type=int, default=None,
                        help="Candidate number (default: auto)")
    parser.add_argument(
        "--evaluate-script",
        type=str,
        default=os.environ.get("EVALUATE_SCRIPT"),
        help="Path to an evaluation program (bash/sh/py/executable) that accepts <candidate_dir> and prints JSON as the last line",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=int(os.environ.get("EVOLVER_ITERATIONS", "1")),
        help="How many evolution iterations to run in this process (default: $EVOLVER_ITERATIONS or 1)",
    )
    args = parser.parse_args()

    workspace = (args.workspace.expanduser().resolve() if args.workspace else get_workspace())
    paths = EvolverPaths.from_workspace(workspace)
    os.environ["EVOLVER_WORKSPACE"] = str(paths.workspace)
    cfg = load_config()

    print(f"\n{'='*60}")
    print(f"Meta-Harness Evolution — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    print(f"[MAIN] Workspace: {paths.workspace}")

    def run_one(candidate_num: int) -> int:
        print(f"[MAIN] Candidate: {candidate_num}")

        # Step 1: Run proposer
        print("[STEP] Propose: running proposer...")
        proposer_result = run_proposer(paths, cfg, candidate_num)
        candidate_dir = Path(proposer_result["candidate_dir"])

        if not proposer_result["success"]:
            print(f"[MAIN] Proposer failed: {proposer_result.get('error')}")
            print("[MAIN] Skipping this iteration.")
            return 1
        print("[STEP] Propose: done")

        # Step 2: Validate
        print("[STEP] Validate: checking candidate...")
        if not validate_candidate(candidate_dir):
            print("[MAIN] Validation failed. Skipping.")
            return 1
        print("[STEP] Validate: done")

        print("[STEP] Harness: running harness_run_script.sh...")
        harness_run = run_harness_script(candidate_dir, paths.workspace, cfg, candidate_num)
        if harness_run.get("log_path"):
            print(f"[HARNESS] Log: {harness_run.get('log_path')}")
        if harness_run.get("skipped"):
            print(f"[HARNESS] Skipped: {harness_run.get('reason')}")
        if not harness_run.get("ok", False):
            print(f"[MAIN] Harness execution failed: {harness_run.get('error')}")
            return 2
        print("[STEP] Harness: done")

        # Step 3: Evaluate
        print("[STEP] Evaluate: running evaluation...")
        scores = evaluate_candidate(paths, candidate_dir, args.evaluate_script)
        if not scores or "error" in scores:
            print(f"[MAIN] Evaluation failed: {scores.get('error')}")
            return 2
        print("[STEP] Evaluate: done")

        # Step 4: Log eval scores to candidate dir
        print("[STEP] Log: writing eval scores and change record...")
        scores_file = candidate_dir / "eval_scores.json"
        with open(scores_file, "w") as sf:
            json.dump(scores, sf, indent=2)
        print(f"[MAIN] Scores: {json.dumps(scores, indent=2)}")

        # Step 5: Record this round's changed places before best gets updated
        change_record = collect_change_record(paths, candidate_num, candidate_dir)
        print(f"[MAIN] Changes recorded: {change_record['changed_files_count']} file(s)")

        # Step 6: Update best if needed
        prev_best_score = update_best(paths, candidate_dir, scores)

        # Step 7: Log evolution
        log_evolution(paths, candidate_num, candidate_dir, scores, proposer_result["success"], change_record)
        print("[STEP] Log: done")

        # Step 8: Post to Feishu
        print("[STEP] Post: sending Feishu message...")
        post_to_feishu(paths, candidate_num, candidate_dir, scores, proposer_result["success"], prev_best_score)
        print("[STEP] Post: done")

        print(f"\n[MAIN] Done! Candidate {candidate_num} evaluated: {scores.get('final_score')}")
        print(f"{'='*60}\n")
        return 0

    success = 0
    skipped = 0
    errors = 0

    iterations = max(int(args.iterations), 1)
    for i in range(iterations):
        if i > 0:
            print(f"\n{'-'*60}")
            print(f"[MAIN] Iteration {i+1}/{iterations}")
            print(f"{'-'*60}\n")

        candidate_num = (args.candidate_num + i) if args.candidate_num is not None else get_next_candidate_num(paths)
        code = run_one(candidate_num)
        if code == 0:
            success += 1
        elif code == 1:
            skipped += 1
        else:
            errors += 1

    if errors > 0:
        sys.exit(2)
    if success > 0:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
