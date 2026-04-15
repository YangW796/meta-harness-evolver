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
import logging
import os
import subprocess
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from evolver_config import EvolverConfig, load_config
from shared import get_workspace, iter_effective_files, load_env_file

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
ENV_FILE = ROOT_DIR / ".env"
load_env_file(ENV_FILE)


@dataclass(frozen=True)
class EvolverPaths:
    workspace: Path
    candidates_dir: Path
    best_dir: Path
    scripts_dir: Path

    @staticmethod
    def from_workspace(workspace: Path) -> "EvolverPaths":
        ws = workspace.resolve()
        return EvolverPaths(
            workspace=ws,
            candidates_dir=ws / "candidates",
            best_dir=ws / "best" / "current",
            scripts_dir=SCRIPTS_DIR,
        )


def get_next_candidate_num(paths: EvolverPaths) -> int:
    """Find the next candidate number."""
    if not paths.candidates_dir.exists():
        paths.candidates_dir.mkdir(parents=True, exist_ok=True)
        return 1
    nums: list[int] = []
    for d in paths.candidates_dir.iterdir():
        if not (d.is_dir() and d.name.startswith("candidate_")):
            continue
        try:
            nums.append(int(d.name.split("_", 1)[1]))
        except Exception:
            continue
    return max(nums, default=0) + 1


def get_best_candidate(paths: EvolverPaths) -> dict | None:
    """Get the best candidate's scores."""
    scores_file = paths.best_dir / "eval_scores.json"
    if scores_file.exists():
        return json.loads(scores_file.read_text())
    return None


def run_proposer(paths: EvolverPaths, cfg: EvolverConfig, candidate_num: int) -> dict:
    """
    Spawn the proposer sub-agent to propose a candidate modification.
    Returns dict with 'success', 'candidate_dir', and 'reasoning'.
    """
    import uuid

    candidate_dir = paths.candidates_dir / f"candidate_{candidate_num}"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    (candidate_dir / "harness").mkdir(exist_ok=True)
    (candidate_dir / "traces").mkdir(exist_ok=True)

    # Read evolution history for context
    history = []
    for d in sorted(paths.candidates_dir.iterdir(), key=lambda x: x.name):
        if d.name == f"candidate_{candidate_num}":
            continue
        if d.is_dir():
            scores_file = d / "eval_scores.json"
            if scores_file.exists():
                history.append({
                    "candidate": d.name,
                    "scores": json.loads(scores_file.read_text())
                })

    best = get_best_candidate(paths)

    # Spawn the sub-agent
    agent_session_id = str(uuid.uuid4())[:8]

    # Dynamically list files in the current best directory for AI4S
    best_harness_dir = paths.best_dir / "harness"
    if best_harness_dir.exists():
        files = [f.name for f in iter_effective_files(best_harness_dir)]
        target_files_str = "\n".join([f"   - {f}" for f in files])
    else:
        target_files_str = "   - (No files found, please create the necessary Python scripts or configs)"

    prompt_prefix = cfg.proposer_prompt_prefix
    if prompt_prefix and not prompt_prefix.endswith("\n"):
        prompt_prefix += "\n\n"
    proposer_task = f"""{prompt_prefix}You are the Evolution Proposer for an AI4S (AI for Science) project.

Your job: Propose ONE targeted modification to the project code or configuration based on evolution history to improve the benchmark score.

## Your Workspace
- Evolution history: {paths.workspace}/candidates/
- Current best codebase: {paths.workspace}/best/current/
- Your output: {paths.workspace}/candidates/candidate_{candidate_num}/harness/

## What You Must Do

1. Read ALL prior candidates from {paths.workspace}/candidates/ (sorted by number)
2. Read the current best from {paths.workspace}/best/current/
3. Identify patterns: what's working? What's failing?
4. Propose ONE targeted, specific edit to ONE of the files. The current files include:
{target_files_str}

5. Copy the current best files to your output dir
6. Apply your targeted edit to the ONE file you chose (e.g., modifying a PyTorch model, loss function, or hyperparameters).
7. Write a BRIEF reasoning trace to {paths.workspace}/candidates/candidate_{candidate_num}/proposer_reasoning.md
   explaining: what you changed, why, what you expect to improve

## Constraints
- Do NOT do wholesale rewrites — one targeted edit max
- Make sure Python code is syntactically correct and can run.
- If you see no clear improvement path, write your reasoning and make ONE small edit anyway

## History Summary
Total prior candidates: {len(history)}
Best score so far: {best['final_score'] if best else 'N/A'}

## Output Format
Write your modified file to {paths.workspace}/candidates/candidate_{candidate_num}/harness/<FILENAME>
Write reasoning to {paths.workspace}/candidates/candidate_{candidate_num}/proposer_reasoning.md

Start now. Read the history first, then propose.
"""
    proposer_task += cfg.proposer_prompt_suffix(paths.workspace, candidate_num)

    print(f"[PROPOSER] Spawning sub-agent for candidate_{candidate_num}...")
    print(f"[PROPOSER] History: {len(history)} prior candidates")

    try:
        if best_harness_dir.exists():
            import shutil

            for f in iter_effective_files(best_harness_dir):
                shutil.copy2(f, candidate_dir / "harness" / f.name)

        if os.environ.get("EVOLVER_TEST_MODE") == "1":
            harness_out = candidate_dir / "harness"
            cfg = harness_out / "config.yaml"
            if cfg.exists():
                cfg.write_text(cfg.read_text() + "\nseed: 1\n")
            else:
                (harness_out / "config.yaml").write_text("seed: 1\n")
            (candidate_dir / "proposer_reasoning.md").write_text(
                "Test mode proposer: appended a minimal config change (seed: 1).\n"
            )
            return {"success": True, "candidate_dir": str(candidate_dir), "agent_result": {"mode": "test"}}

        result = _run_proposer_with_nexau(
            task=proposer_task,
            label=f"evolver-proposer-{agent_session_id}",
            work_dir=paths.workspace,
            timeout_seconds=300,
            log_dir=candidate_dir / "traces",
        )
        print(f"[PROPOSER] NexAU returned: {result}")
        return {"success": True, "candidate_dir": str(candidate_dir), "agent_result": result}
    except Exception as e:
        print(f"[PROPOSER] Error running proposer: {e}")
        return {"success": False, "candidate_dir": str(candidate_dir), "error": str(e)}


def _tail_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...(truncated)\n"


def _tail_file(path: Path, max_bytes: int = 8000) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    if len(data) <= max_bytes:
        return data.decode("utf-8", errors="replace")
    return data[-max_bytes:].decode("utf-8", errors="replace")


def _run_proposer_with_nexau(task: str, label: str, work_dir: Path, timeout_seconds: int, log_dir: Path) -> dict:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{label}.log"

    proposer_max_iterations = int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20"))
    proposer_timeout_seconds = int(os.environ.get("PROPOSER_TIMEOUT_SECONDS", str(timeout_seconds)))

    print("[PROPOSER] LLM input (truncated):")
    print(_tail_text(task, 4000))
    print(f"[PROPOSER] LLM input length: {len(task)} chars")
    print(f"[PROPOSER] NexAU log: {log_path}")
    print(f"[PROPOSER] NexAU limits: max_iterations={proposer_max_iterations}, timeout_seconds={proposer_timeout_seconds}")

    payload = {
        "task": task,
        "label": label,
        "work_dir": str(work_dir),
        "max_iterations": proposer_max_iterations,
    }

    cmd = [sys.executable, str(Path(__file__).resolve()), "--nexau-proposer-child", str(log_path)]
    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=proposer_timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        print(f"[PROPOSER] NexAU proposer timed out after {proposer_timeout_seconds}s")
        tail = _tail_file(log_path)
        if tail:
            print("[PROPOSER] NexAU log tail:")
            print(tail)
        raise

    stdout_tail = _tail_text(result.stdout or "", 2000)
    stderr_tail = _tail_text(result.stderr or "", 2000)
    if stdout_tail.strip():
        print("[PROPOSER] NexAU stdout (truncated):")
        print(stdout_tail)
    if stderr_tail.strip():
        print("[PROPOSER] NexAU stderr (truncated):")
        print(stderr_tail)

    log_tail = _tail_file(log_path)
    if log_tail.strip():
        print("[PROPOSER] NexAU log tail:")
        print(log_tail)

    try:
        parsed = json.loads((result.stdout or "").strip().splitlines()[-1])
    except Exception:
        parsed = {"ok": False, "error": "Failed to parse NexAU child output as JSON", "stdout": result.stdout}

    if result.returncode != 0 or not parsed.get("ok", False):
        err = parsed.get("error") or f"child_exit_code={result.returncode}"
        raise RuntimeError(err)

    return {"label": label, "output": parsed.get("output"), "timeout_seconds": timeout_seconds, "log_path": str(log_path)}


def _nexau_proposer_child(log_path: Path) -> int:
    payload_raw = sys.stdin.read()
    try:
        payload = json.loads(payload_raw)
    except Exception:
        payload = {"task": payload_raw, "label": "unknown", "work_dir": os.getcwd()}

    label = str(payload.get("label", "nexau-proposer"))
    task = str(payload.get("task", ""))
    work_dir = Path(str(payload.get("work_dir", os.getcwd()))).resolve()
    max_iterations = int(payload.get("max_iterations", 20))

    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler(sys.stderr)],
    )
    logging.getLogger(__name__).info("NexAU proposer child started")
    logging.getLogger(__name__).info("label=%s work_dir=%s task_len=%s max_iterations=%s", label, work_dir, len(task), max_iterations)

    try:
        nexau_home = Path(os.environ.get("NEXAU_HOME", "")).resolve()
        if not nexau_home.exists():
            raise RuntimeError(f"NexAU not found at {nexau_home}. Set NEXAU_HOME to your NexAU repo path.")

        if str(nexau_home) not in sys.path:
            sys.path.insert(0, str(nexau_home))

        code_agent_dir = nexau_home / "examples" / "code_agent"
        if not code_agent_dir.exists():
            raise RuntimeError(f"NexAU code_agent example not found at {code_agent_dir}")

        if str(code_agent_dir) not in sys.path:
            sys.path.insert(0, str(code_agent_dir))

        llm_model = os.environ.get("LLM_MODEL")
        llm_api_key = os.environ.get("LLM_API_KEY")
        if not llm_model or not llm_api_key:
            raise RuntimeError("Missing LLM_MODEL / LLM_API_KEY in environment for NexAU proposer.")

        from nexau import Agent, AgentConfig, LLMConfig, Tool

        import importlib
        import types

        tool_impl_dir = code_agent_dir / "tool_impl"
        if not tool_impl_dir.exists():
            examples_dir = nexau_home / "examples"
            if examples_dir.exists():
                for root, dirnames, _ in os.walk(examples_dir):
                    if "tool_impl" not in dirnames:
                        continue
                    candidate_dir = Path(root)
                    if not (candidate_dir / "tools").exists():
                        continue
                    if not (candidate_dir / "systemprompt.md").exists():
                        continue
                    code_agent_dir = candidate_dir
                    tool_impl_dir = code_agent_dir / "tool_impl"
                    break
        if tool_impl_dir.exists():
            if str(code_agent_dir) not in sys.path:
                sys.path.insert(0, str(code_agent_dir))
            if "tool_impl" not in sys.modules:
                pkg = types.ModuleType("tool_impl")
                pkg.__path__ = [str(tool_impl_dir)]
                sys.modules["tool_impl"] = pkg

        try:
            from tool_impl.complete_task import complete_task
            from tool_impl.glob_tool import glob
            from tool_impl.list_directory import list_directory
            from tool_impl.read_file import read_file
            from tool_impl.read_many_files import read_many_files
            from tool_impl.replace import replace
            from tool_impl.run_shell_command import run_shell_command
            from tool_impl.search_file_content import search_file_content
            from tool_impl.write_file import write_file
            from tool_impl.write_todos import write_todos
            from tool_impl.web_fetch import web_fetch
        except ModuleNotFoundError as e:
            if str(getattr(e, "name", "")) == "tool_impl" or str(getattr(e, "name", "")).startswith("tool_impl."):
                raise RuntimeError(
                    "Failed to import NexAU code_agent tool implementations. "
                    f"Expected tool_impl at {tool_impl_dir}. "
                    "Set NEXAU_HOME to a NexAU checkout that includes examples/code_agent/tool_impl."
                ) from e
            raise

        tools_dir = code_agent_dir / "tools"
        tools = [
            Tool.from_yaml(str(tools_dir / "read_file.tool.yaml"), binding=read_file),
            Tool.from_yaml(str(tools_dir / "read_many_files.tool.yaml"), binding=read_many_files),
            Tool.from_yaml(str(tools_dir / "write_file.tool.yaml"), binding=write_file),
            Tool.from_yaml(str(tools_dir / "list_directory.tool.yaml"), binding=list_directory),
            Tool.from_yaml(str(tools_dir / "Glob.tool.yaml"), binding=glob),
            Tool.from_yaml(str(tools_dir / "search_file_content.tool.yaml"), binding=search_file_content),
            Tool.from_yaml(str(tools_dir / "replace.tool.yaml"), binding=replace),
            Tool.from_yaml(str(tools_dir / "run_shell_command.tool.yaml"), binding=run_shell_command),
            Tool.from_yaml(str(tools_dir / "write_todos.tool.yaml"), binding=write_todos),
            Tool.from_yaml(str(tools_dir / "complete_task.tool.yaml"), binding=complete_task),
            Tool.from_yaml(str(tools_dir / "WebFetch.tool.yaml"), binding=web_fetch),
        ]

        system_prompt = (code_agent_dir / "systemprompt.md").read_text()
        agent_config = AgentConfig(
            name=label,
            system_prompt=system_prompt,
            system_prompt_type="string",
            tool_call_mode="openai",
            max_iterations=max_iterations,
            llm_config=LLMConfig(
                model=llm_model,
                base_url=os.environ.get("LLM_BASE_URL"),
                api_key=llm_api_key,
                api_type=os.environ.get("LLM_API_TYPE", "openai_chat_completion"),
                temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
                max_tokens=int(os.environ.get("LLM_MAX_TOKENS", "2048")),
            ),
            tools=tools,
            sandbox_config={
                "type": "local",
                "_work_dir": str(work_dir),
                "persist_sandbox": False,
            },
        )

        agent = Agent(config=agent_config)
        output = agent.run(message=task, context={"working_directory": str(work_dir)})
        print(json.dumps({"ok": True, "output": output}, ensure_ascii=False))
        return 0
    except Exception as e:
        logging.getLogger(__name__).error("NexAU proposer child failed: %s", e)
        logging.getLogger(__name__).error(traceback.format_exc())
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 1


def validate_candidate(candidate_dir: Path) -> bool:
    """Lightweight validation before running full benchmark."""
    print(f"[VALIDATE] Checking {candidate_dir}/harness/...")

    harness_dir = candidate_dir / "harness"
    if not harness_dir.exists():
        print(f"[VALIDATE] Missing harness directory")
        return False

    files = list(iter_effective_files(harness_dir))
    if not files:
        print(f"[VALIDATE] No files found in harness directory")
        return False

    # Basic sanity checks for scripts/configs
    for f in files:
        if f.suffix == ".py":
            import py_compile
            try:
                py_compile.compile(str(f), doraise=True)
            except py_compile.PyCompileError as e:
                print(f"[VALIDATE] Syntax error in {f.name}: {e}")
                return False
        elif f.suffix in [".md", ".yaml", ".json"]:
            content = f.read_text()
            if len(content) < 10:
                print(f"[VALIDATE] WARNING: {f.name} seems too short ({len(content)} chars)")

    print("[VALIDATE] OK")
    return True


def run_harness_script(candidate_dir: Path, workspace: Path, cfg: EvolverConfig, candidate_num: int) -> dict:
    script = str(cfg.harness_run_script or "").strip()
    if not script:
        if cfg.require_harness_run_script:
            return {"ok": False, "error": "Missing HARNESS_RUN_SCRIPT"}
        return {"ok": True, "skipped": True, "reason": "no harness run script"}

    script_path = Path(script).expanduser()
    if not script_path.is_absolute():
        script_path = (Path.cwd() / script_path).resolve()

    traces_dir = candidate_dir / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    log_path = traces_dir / "harness_run.log"

    cmd = ["bash", str(script_path), str(candidate_dir)]
    env = os.environ.copy()
    env.setdefault("EVOLVER_WORKSPACE", str(workspace))
    env.setdefault("CANDIDATE_NUM", str(candidate_num))
    env.setdefault("CANDIDATE_DIR", str(candidate_dir))
    try:
        result = subprocess.run(
            cmd,
            cwd=str(candidate_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=int(cfg.harness_run_timeout_seconds),
        )
    except subprocess.TimeoutExpired:
        log_path.write_text(f"CMD: {' '.join(cmd)}\nTIMEOUT\n", encoding="utf-8")
        return {"ok": False, "error": "timeout"}

    log_path.write_text(
        "\n".join(
            [
                f"CMD: {' '.join(cmd)}",
                f"EXIT_CODE: {result.returncode}",
                "STDOUT:",
                result.stdout or "",
                "STDERR:",
                result.stderr or "",
            ]
        ),
        encoding="utf-8",
    )
    if result.returncode != 0:
        return {"ok": False, "error": "harness run script failed", "exit_code": result.returncode}
    return {"ok": True}


def evaluate_candidate(paths: EvolverPaths, candidate_dir: Path, evaluate_script: str | None) -> dict:
    """Run the benchmark against the candidate harness."""
    print(f"[EVALUATE] Running benchmark for {candidate_dir.name}...")

    if evaluate_script:
        script_path = Path(evaluate_script).expanduser()
        if not script_path.is_absolute():
            script_path = (Path.cwd() / script_path).resolve()

        if script_path.suffix == ".py":
            cmd = [sys.executable, str(script_path), str(candidate_dir)]
        elif script_path.suffix == ".sh":
            cmd = ["bash", str(script_path), str(candidate_dir)]
        else:
            cmd = [str(script_path), str(candidate_dir)]
    else:
        cmd = [sys.executable, str(paths.scripts_dir / "evaluate-example.py"), str(candidate_dir)]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        print(f"[EVALUATE] Error: {result.stderr}")
        return {"error": result.stderr, "scores": {}}

    try:
        scores = json.loads(result.stdout.strip().split("\n")[-1])
        return scores
    except Exception as e:
        print(f"[EVALUATE] Failed to parse scores: {e}")
        return {"error": str(e), "scores": {}}


def update_best(paths: EvolverPaths, candidate_dir: Path, scores: dict) -> float | None:
    """Update the best harness if this candidate is better."""
    best_scores_file = paths.best_dir / "eval_scores.json"
    best_harness_dir = paths.best_dir / "harness"

    current_best: float | None = None
    if best_scores_file.exists():
        current_best = float(json.loads(best_scores_file.read_text()).get("final_score", 0))

    new_score = scores.get("final_score", 0)

    if current_best is None or new_score > current_best:
        print(f"[BEST] New best! {new_score} > {current_best}")
        # Copy candidate harness to best
        paths.best_dir.mkdir(parents=True, exist_ok=True)
        best_harness_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        candidate_harness = candidate_dir / "harness"
        for f in iter_effective_files(candidate_harness):
            shutil.copy2(f, best_harness_dir / f.name)

        # Copy scores
        with open(best_scores_file, "w") as sf:
            json.dump(scores, sf, indent=2)

        # Note the winner
        with open(paths.best_dir / "winner_note.md", "w") as wn:
            wn.write(f"# Best Harness — {datetime.now().isoformat()}\n\n")
            wn.write(f"Winner: {candidate_dir.name}\n")
            wn.write(f"Score: {new_score}\n")
            wn.write(f"Improvement over previous: {new_score - (current_best or 0):+.2f}\n")
    else:
        print(f"[BEST] No update. Current best: {current_best}, this candidate: {new_score}")
    return current_best if current_best is not None else 0.0


def log_evolution(paths: EvolverPaths, candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool):
    """Append to the evolution log."""
    log_file = paths.workspace / "evolution_log.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "candidate": f"candidate_{candidate_num}",
        "candidate_dir": str(candidate_dir),
        "proposer_success": proposer_ok,
        "scores": scores,
        "final_score": scores.get("final_score", 0),
    }
    with open(log_file, "a") as lf:
        lf.write(json.dumps(entry) + "\n")


def post_to_feishu(paths: EvolverPaths, candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool, prev_best_score: float | None):
    """Post summary to Feishu (Lark)."""
    print("[FEISHU] Posting message...")
    post_script = paths.scripts_dir / "post_to_research.py"

    cmd = [
        sys.executable,
        str(post_script),
        str(candidate_num),
        str(candidate_dir),
        str(scores.get("final_score", 0)),
        str(int(proposer_ok)),
    ]
    if prev_best_score is not None:
        cmd.extend(["--prev-best-score", str(prev_best_score)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"[FEISHU] Failed: {result.stderr}")
    else:
        print(f"[FEISHU] Posted successfully")


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
    cfg = load_config()

    print(f"\n{'='*60}")
    print(f"Meta-Harness Evolution — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    print(f"[MAIN] Workspace: {paths.workspace}")

    def run_one(candidate_num: int) -> int:
        print(f"[MAIN] Candidate: {candidate_num}")

        # Step 1: Run proposer
        proposer_result = run_proposer(paths, cfg, candidate_num)
        candidate_dir = Path(proposer_result["candidate_dir"])

        if not proposer_result["success"]:
            print(f"[MAIN] Proposer failed: {proposer_result.get('error')}")
            print("[MAIN] Skipping this iteration.")
            return 1

        # Step 2: Validate
        if not validate_candidate(candidate_dir):
            print("[MAIN] Validation failed. Skipping.")
            return 1

        harness_run = run_harness_script(candidate_dir, paths.workspace, cfg, candidate_num)
        if not harness_run.get("ok", False):
            print(f"[MAIN] Harness execution failed: {harness_run.get('error')}")
            return 2

        # Step 3: Evaluate
        scores = evaluate_candidate(paths, candidate_dir, args.evaluate_script)
        if not scores or "error" in scores:
            print(f"[MAIN] Evaluation failed: {scores.get('error')}")
            return 2

        # Step 4: Log eval scores to candidate dir
        scores_file = candidate_dir / "eval_scores.json"
        with open(scores_file, "w") as sf:
            json.dump(scores, sf, indent=2)
        print(f"[MAIN] Scores: {json.dumps(scores, indent=2)}")

        # Step 5: Update best if needed
        prev_best_score = update_best(paths, candidate_dir, scores)

        # Step 6: Log evolution
        log_evolution(paths, candidate_num, candidate_dir, scores, proposer_result["success"])

        # Step 7: Post to Feishu
        post_to_feishu(paths, candidate_num, candidate_dir, scores, proposer_result["success"], prev_best_score)

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
    if len(sys.argv) >= 2 and sys.argv[1] == "--nexau-proposer-child":
        if len(sys.argv) < 3:
            raise SystemExit(2)
        raise SystemExit(_nexau_proposer_child(Path(sys.argv[2])))
    main()
