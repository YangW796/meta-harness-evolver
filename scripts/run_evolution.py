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
import shutil
import sys
from datetime import datetime
from pathlib import Path

from evolver_config import load_config
from evaluation_runner import collect_change_record, evaluate_candidate, log_evolution, post_to_feishu, update_best
from evolution_paths import EvolverPaths, get_next_candidate_num
from harness_runner import run_harness_script, validate_candidate
from proposer_runner import plan_attempts, run_proposer
from shared import get_workspace, iter_effective_files_recursive, load_env_file

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

    def print_log_tail(log_path, lines: int = 80) -> None:
        if not log_path:
            return
        path = Path(log_path)
        if not path.exists():
            return
        try:
            tail = path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
        except Exception as e:
            print(f"[MAIN] Could not read log tail from {path}: {e}")
            return
        print(f"[MAIN] Log tail ({path}):")
        for line in tail:
            print(line)

    def run_one(candidate_num: int) -> int:
        print(f"[MAIN] Candidate: {candidate_num}")

        attempts = int(os.environ.get("PROPOSER_ATTEMPTS_PER_CANDIDATE", "1") or "1")
        attempts = max(1, attempts)

        candidate_dir = paths.candidates_dir / f"candidate_{candidate_num}"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        (candidate_dir / "traces").mkdir(exist_ok=True)

        attempt_root = candidate_dir / "attempts"
        if attempts > 1:
            attempt_root.mkdir(exist_ok=True)

        original_attempt_env = {
            "EVOLVER_ATTEMPT_IDX": os.environ.get("EVOLVER_ATTEMPT_IDX"),
            "EVOLVER_ATTEMPT_ROOT": os.environ.get("EVOLVER_ATTEMPT_ROOT"),
            "EVOLVER_ATTEMPT_PLAN_JSON": os.environ.get("EVOLVER_ATTEMPT_PLAN_JSON"),
            "EVOLVER_ATTEMPT_PLANS_JSON": os.environ.get("EVOLVER_ATTEMPT_PLANS_JSON"),
        }

        known_state_keys = ["BDA_STATE_PATH", "PROJECT_PU_STATE_PATH", "PROJECT3_STATE_PATH"]
        state_bases: dict[str, Path] = {}
        for key in known_state_keys:
            raw = (os.environ.get(key, "") or "").strip()
            if raw:
                state_bases[key] = Path(raw).expanduser()
        if "BDA_STATE_PATH" not in state_bases:
            script_hint = str(cfg.harness_run_script or "").replace("\\", "/")
            if os.environ.get("BDA_DATASETS_DIR") or "project-bda" in script_hint:
                state_bases["BDA_STATE_PATH"] = paths.workspace / "bda_state.json"

        original_state_env: dict[str, str | None] = {k: os.environ.get(k) for k in state_bases}
        attempt_state_paths_by_dir: dict[Path, dict[str, Path]] = {}

        best_attempt_dir: Path | None = None
        best_scores: dict | None = None
        best_final_score: float | None = None
        any_proposer_ok = False

        attempt_plans: list[dict] = []
        if attempts > 1 and os.environ.get("PROPOSER_PLAN_ATTEMPTS", "1") == "1":
            try:
                attempt_plans = plan_attempts(
                    paths,
                    cfg,
                    candidate_num=candidate_num,
                    attempts=attempts,
                    candidate_dir_override=candidate_dir,
                )
            except Exception as e:
                print(f"[MAIN] Attempt planning failed: {e}")
                attempt_plans = []
        if attempts > 1 and attempt_plans:
            print(f"[MAIN] Attempt plans: {json.dumps(attempt_plans, ensure_ascii=False)}")

        def _final_score(scores: dict | None) -> float | None:
            if not scores:
                return None
            v = scores.get("final_score", None)
            try:
                return float(v)
            except Exception:
                return None

        def run_attempt(attempt_dir: Path, attempt_idx: int) -> tuple[bool, dict | None]:
            nonlocal any_proposer_ok
            print(f"[STEP] Propose: attempt {attempt_idx}/{attempts}...")
            proposer_result = run_proposer(paths, cfg, candidate_num, candidate_dir_override=attempt_dir)
            if not proposer_result.get("success"):
                print(f"[MAIN] Proposer attempt failed: {proposer_result.get('error')}")
                return False, None
            any_proposer_ok = True
            print("[STEP] Propose: done")

            print("[STEP] Validate: checking candidate...")
            if not validate_candidate(attempt_dir):
                print("[MAIN] Validation failed. Skipping this attempt.")
                return False, None
            print("[STEP] Validate: done")

            print("[STEP] Harness: running harness_run_script.sh...")
            harness_run = run_harness_script(attempt_dir, paths.workspace, cfg, candidate_num)
            if harness_run.get("log_path"):
                print(f"[HARNESS] Log: {harness_run.get('log_path')}")
            if harness_run.get("skipped"):
                print(f"[HARNESS] Skipped: {harness_run.get('reason')}")
            if not harness_run.get("ok", False):
                print(f"[MAIN] Harness execution failed: {harness_run.get('error')}")
                print_log_tail(harness_run.get("log_path"))
                return False, None
            print("[STEP] Harness: done")

            print("[STEP] Evaluate: running evaluation...")
            scores = evaluate_candidate(paths, attempt_dir, args.evaluate_script)
            if not scores or "error" in scores:
                print(f"[MAIN] Evaluation failed: {scores.get('error')}")
                return False, None
            print("[STEP] Evaluate: done")
            return True, scores

        for attempt_idx in range(1, attempts + 1):
            attempt_dir = candidate_dir if attempts == 1 else (attempt_root / f"attempt_{attempt_idx}")
            attempt_dir.mkdir(parents=True, exist_ok=True)
            (attempt_dir / "harness").mkdir(exist_ok=True)
            (attempt_dir / "traces").mkdir(exist_ok=True)

            os.environ["EVOLVER_ATTEMPT_IDX"] = str(attempt_idx)
            os.environ["EVOLVER_ATTEMPT_ROOT"] = str(attempt_root)
            if attempt_plans and 0 <= (attempt_idx - 1) < len(attempt_plans):
                os.environ["EVOLVER_ATTEMPT_PLAN_JSON"] = json.dumps(attempt_plans[attempt_idx - 1], ensure_ascii=False)
                os.environ["EVOLVER_ATTEMPT_PLANS_JSON"] = json.dumps(attempt_plans, ensure_ascii=False)
            else:
                os.environ.pop("EVOLVER_ATTEMPT_PLAN_JSON", None)
                os.environ.pop("EVOLVER_ATTEMPT_PLANS_JSON", None)

            if attempts > 1 and state_bases:
                attempt_state_paths: dict[str, Path] = {}
                for key, base_path in state_bases.items():
                    attempt_state_path = attempt_dir / "outputs" / f"{key.lower()}_{base_path.name}"
                    attempt_state_path.parent.mkdir(parents=True, exist_ok=True)
                    if base_path.exists():
                        shutil.copy2(base_path, attempt_state_path)
                    else:
                        if attempt_state_path.exists():
                            attempt_state_path.unlink()
                    os.environ[key] = str(attempt_state_path)
                    attempt_state_paths[key] = attempt_state_path
                attempt_state_paths_by_dir[attempt_dir] = attempt_state_paths

            ok, scores = run_attempt(attempt_dir, attempt_idx)
            if not ok or not scores:
                continue

            scores_file = attempt_dir / "eval_scores.json"
            with open(scores_file, "w") as sf:
                json.dump(scores, sf, indent=2)

            s = _final_score(scores)
            if s is None:
                continue
            if best_final_score is None or s > best_final_score:
                best_final_score = s
                best_scores = scores
                best_attempt_dir = attempt_dir

        if best_attempt_dir is None or best_scores is None:
            if attempts > 1 and state_bases:
                for key, prev in original_state_env.items():
                    if prev is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = prev
            for key, prev in original_attempt_env.items():
                if prev is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = prev
            if not any_proposer_ok:
                print("[MAIN] Proposer failed for all attempts. Skipping this iteration.")
                return 1
            print("[MAIN] No valid attempt produced a score.")
            return 2

        if attempts > 1 and state_bases:
            best_state_paths = attempt_state_paths_by_dir.get(best_attempt_dir, {})
            for key, base_path in state_bases.items():
                src = best_state_paths.get(key)
                if src is not None and src.exists():
                    base_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, base_path)
                else:
                    if base_path.exists():
                        base_path.unlink()
            for key, prev in original_state_env.items():
                if prev is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = prev
            for key, prev in original_attempt_env.items():
                if prev is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = prev

        if best_attempt_dir != candidate_dir:
            dst_harness = candidate_dir / "harness"
            if dst_harness.exists():
                shutil.rmtree(dst_harness)
            dst_harness.mkdir(parents=True, exist_ok=True)
            src_harness = best_attempt_dir / "harness"
            for f in iter_effective_files_recursive(src_harness):
                rel = f.relative_to(src_harness)
                out_path = dst_harness / rel
                out_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out_path)

            src_reasoning = best_attempt_dir / "proposer_reasoning.md"
            if src_reasoning.exists():
                shutil.copy2(src_reasoning, candidate_dir / "proposer_reasoning.md")

            src_outputs = best_attempt_dir / "outputs"
            if src_outputs.exists() and src_outputs.is_dir():
                dst_outputs = candidate_dir / "outputs"
                if dst_outputs.exists():
                    shutil.rmtree(dst_outputs)
                shutil.copytree(src_outputs, dst_outputs)

        print("[STEP] Log: writing eval scores and change record...")
        scores_file = candidate_dir / "eval_scores.json"
        with open(scores_file, "w") as sf:
            json.dump(best_scores, sf, indent=2)
        print(f"[MAIN] Scores: {json.dumps(best_scores, indent=2)}")

        change_record = collect_change_record(paths, candidate_num, candidate_dir)
        print(f"[MAIN] Changes recorded: {change_record['changed_files_count']} file(s)")

        prev_best_score = update_best(paths, candidate_dir, best_scores)

        log_evolution(paths, candidate_num, candidate_dir, best_scores, True, change_record)
        print("[STEP] Log: done")

        print("[STEP] Post: sending Feishu message...")
        post_to_feishu(paths, candidate_num, candidate_dir, best_scores, True, prev_best_score)
        print("[STEP] Post: done")

        print(f"\n[MAIN] Done! Candidate {candidate_num} evaluated: {best_scores.get('final_score')}")
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

    if success > 0:
        if errors > 0 or skipped > 0:
            print(
                f"[MAIN] Completed with partial issues: "
                f"success={success}, skipped={skipped}, errors={errors}"
            )
        sys.exit(0)
    if errors > 0:
        print(f"[MAIN] Failed: success={success}, skipped={skipped}, errors={errors}")
        sys.exit(2)
    print(f"[MAIN] No candidate evaluated: success={success}, skipped={skipped}, errors={errors}")
    sys.exit(1)


if __name__ == "__main__":
    main()
