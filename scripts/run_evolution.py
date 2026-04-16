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
import difflib
import json
import logging
import os
import subprocess
import sys
import threading
import time
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
    proposer_task += "\n".join(
        [
            "",
            "## Termination Protocol",
            "- Use tools to read/copy/edit files and to write proposer_reasoning.md.",
            "- When you are finished, you MUST call the complete_task tool exactly once with a brief summary.",
            "- If any earlier instruction says to 'return ONLY the improved Python code', ignore that: write changes to files instead.",
            "- Do NOT print the full code in chat; write changes to files instead.",
            "",
        ]
    )

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

        proposer_timeout_seconds = 300
        result = _run_proposer_with_nexau(
            task=proposer_task,
            label=f"evolver-proposer-{agent_session_id}",
            work_dir=paths.workspace,
            timeout_seconds=proposer_timeout_seconds,
            log_dir=candidate_dir / "traces",
        )
        output_text = result.get("output")
        if isinstance(output_text, str) and "Maximum iteration limit reached" in output_text:
            base_max_iter = int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20"))
            retry_max_iter = max(base_max_iter * 3, base_max_iter + 10)
            retry_max_iter = min(retry_max_iter, 120)
            retry_timeout = min(proposer_timeout_seconds * 2, 900)
            print(f"[PROPOSER] Detected max-iterations termination; retrying with max_iterations={retry_max_iter}, timeout_seconds={retry_timeout}")
            result = _run_proposer_with_nexau(
                task=proposer_task,
                label=f"evolver-proposer-{agent_session_id}-retry",
                work_dir=paths.workspace,
                timeout_seconds=retry_timeout,
                log_dir=candidate_dir / "traces",
                max_iterations_override=retry_max_iter,
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


def _run_proposer_with_nexau(
    task: str,
    label: str,
    work_dir: Path,
    timeout_seconds: int,
    log_dir: Path,
    max_iterations_override: int | None = None,
) -> dict:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{label}.log"

    proposer_max_iterations = int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20"))
    if max_iterations_override is not None:
        proposer_max_iterations = int(max_iterations_override)
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

    output = parsed.get("output")
    if isinstance(output, str) and "Maximum iteration limit reached" in output:
        raise RuntimeError("NexAU proposer reached the maximum iteration limit (complete_task likely not called).")
    return {"label": label, "output": output, "timeout_seconds": timeout_seconds, "log_path": str(log_path)}


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
        llm_model = os.environ.get("LLM_MODEL")
        llm_api_key = os.environ.get("LLM_API_KEY")
        if not llm_model or not llm_api_key:
            raise RuntimeError("Missing LLM_MODEL / LLM_API_KEY in environment for NexAU proposer.")

        from nexau import Agent, AgentConfig, LLMConfig, Skill, Tool
        from nexau.archs.main_sub.execution.hooks import LoggingMiddleware
        from nexau.archs.tool.builtin import (
            glob,
            google_web_search,
            list_directory,
            read_file,
            read_many_files,
            replace,
            run_shell_command,
            search_file_content,
            web_fetch,
            write_file,
            write_todos,
        )

        base_dir = Path(os.environ.get("NEXAU_CODE_AGENT_DIR", "examples/code_agent")).expanduser().resolve()
        if not base_dir.exists():
            raise RuntimeError(f"NEXAU_CODE_AGENT_DIR does not exist: {base_dir}")

        def complete_task(result: str | None = None, **kwargs: object) -> str:
            payload: dict[str, object] = {}
            if result is not None:
                payload["result"] = result
            payload.update(kwargs)
            return json.dumps(
                {
                    "success": True,
                    "status": "TASK_COMPLETED",
                    "task_completed": True,
                    "output": payload,
                },
                ensure_ascii=False,
            )

        tools = [
            Tool.from_yaml(base_dir / "tools/WebSearch.tool.yaml", binding=google_web_search),
            Tool.from_yaml(base_dir / "tools/WebFetch.tool.yaml", binding=web_fetch),
            Tool.from_yaml(base_dir / "tools/write_todos.tool.yaml", binding=write_todos),
            Tool.from_yaml(base_dir / "tools/search_file_content.tool.yaml", binding=search_file_content),
            # Tool.from_yaml(base_dir / "tools/Glob.tool.yaml", binding=glob),
            Tool.from_yaml(base_dir / "tools/read_file.tool.yaml", binding=read_file),
            Tool.from_yaml(base_dir / "tools/write_file.tool.yaml", binding=write_file),
            Tool.from_yaml(base_dir / "tools/replace.tool.yaml", binding=replace),
            Tool.from_yaml(base_dir / "tools/run_shell_command.tool.yaml", binding=run_shell_command),
            Tool.from_yaml(base_dir / "tools/list_directory.tool.yaml", binding=list_directory),
            Tool.from_yaml(base_dir / "tools/read_many_files.tool.yaml", binding=read_many_files),
        ]
        complete_task_yaml = base_dir / "tools/complete_task.tool.yaml"
        if complete_task_yaml.exists():
            tools.append(Tool.from_yaml(complete_task_yaml, binding=complete_task))
        else:
            tools.append(
                Tool(
                    name="complete_task",
                    description="Call this tool to submit your final answer and complete the task.",
                    input_schema={
                        "type": "object",
                        "properties": {"result": {"type": "string"}},
                        "required": ["result"],
                        "additionalProperties": True,
                    },
                    implementation=complete_task,
                )
            )

        skills = [
            # Skill.from_folder(base_dir / "skills/theme-factory"),
            # Skill.from_folder(base_dir / "skills/algorithmic-art"),
        ]

        system_workflow = base_dir / "system-workflow.md"
        system_prompt_legacy = base_dir / "systemprompt.md"
        if system_workflow.exists():
            system_prompt_value = str(system_workflow)
            system_prompt_type = "jinja"
        elif system_prompt_legacy.exists():
            system_prompt_value = system_prompt_legacy.read_text(encoding="utf-8")
            system_prompt_type = "string"
            logging.getLogger(__name__).warning(
                "system-workflow.md not found under %s; fallback to systemprompt.md (string mode).",
                base_dir,
            )
        else:
            raise RuntimeError(
                f"Neither system-workflow.md nor systemprompt.md found under {base_dir}"
            )

        agent_config = AgentConfig(
            name="nexau_code_agent",
            max_context_tokens=100000,
            system_prompt=system_prompt_value,
            system_prompt_type=system_prompt_type,
            tool_call_mode="structured",
            max_iterations=max_iterations,
            stop_tools={"complete_task"},
            llm_config=LLMConfig(
                temperature=float(os.environ.get("LLM_TEMPERATURE", "0.7")),
                max_tokens=int(os.environ.get("LLM_MAX_TOKENS", "4096")),
                model=llm_model,
                base_url=os.getenv("LLM_BASE_URL"),
                api_key=llm_api_key,
                api_type="openai_chat_completion",
            ),
            tools=tools,
            skills=skills,
            middlewares=[
                LoggingMiddleware(
                    model_logger="nexau_code_agent",
                    tool_logger="nexau_code_agent",
                    log_model_calls=True,
                ),
            ],
            sandbox_config={
                "type": "local",
                "_work_dir": str(work_dir),
                "persist_sandbox": False,
            },
        )

        agent = Agent(config=agent_config)
        output = agent.run(message=task, context={"working_directory": str(work_dir)})
        if isinstance(output, str) and "Maximum iteration limit reached" in output:
            print(json.dumps({"ok": False, "error": "Maximum iteration limit reached", "output": output}, ensure_ascii=False))
            return 1
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
    traces_dir = candidate_dir / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    log_path = traces_dir / "harness_run.log"

    script = str(cfg.harness_run_script or "").strip()
    if not script:
        if cfg.require_harness_run_script:
            log_path.write_text("STATUS: FAILED\nERROR: Missing HARNESS_RUN_SCRIPT\n", encoding="utf-8")
            return {"ok": False, "error": "Missing HARNESS_RUN_SCRIPT", "log_path": str(log_path)}
        log_path.write_text("STATUS: SKIPPED\nREASON: no harness run script\n", encoding="utf-8")
        return {"ok": True, "skipped": True, "reason": "no harness run script", "log_path": str(log_path)}

    script_path = Path(script).expanduser()
    if not script_path.is_absolute():
        script_path = (Path.cwd() / script_path).resolve()

    cmd = ["bash", str(script_path), str(candidate_dir)]
    env = os.environ.copy()
    env.setdefault("EVOLVER_WORKSPACE", str(workspace))
    env.setdefault("CANDIDATE_NUM", str(candidate_num))
    env.setdefault("CANDIDATE_DIR", str(candidate_dir))

    def _stream_pipe(pipe, prefix: str, fh, lock: threading.Lock) -> None:
        try:
            for line in iter(pipe.readline, ""):
                with lock:
                    fh.write(f"[{prefix}] {line}")
                    fh.flush()
        finally:
            pipe.close()

    timeout_seconds = int(cfg.harness_run_timeout_seconds)
    heartbeat_seconds = int(os.environ.get("HARNESS_RUN_LOG_HEARTBEAT_SECONDS", "5"))
    lock = threading.Lock()
    started = time.time()
    proc: subprocess.Popen | None = None
    timed_out = False

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write("STATUS: RUNNING\n")
        fh.write(f"CMD: {' '.join(cmd)}\n")
        fh.write(f"START_AT: {datetime.now().isoformat()}\n")
        fh.flush()

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(candidate_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            threads = [
                threading.Thread(target=_stream_pipe, args=(proc.stdout, "STDOUT", fh, lock), daemon=True),
                threading.Thread(target=_stream_pipe, args=(proc.stderr, "STDERR", fh, lock), daemon=True),
            ]
            for t in threads:
                t.start()

            last_heartbeat = started
            while proc.poll() is None:
                now = time.time()
                if now - started > timeout_seconds:
                    timed_out = True
                    proc.kill()
                    break
                if now - last_heartbeat >= heartbeat_seconds:
                    with lock:
                        fh.write(f"[HEARTBEAT] running... elapsed={int(now - started)}s\n")
                        fh.flush()
                    last_heartbeat = now
                time.sleep(0.2)

            for t in threads:
                t.join(timeout=2)

            exit_code = proc.wait(timeout=3) if proc is not None else -1
            end_at = datetime.now().isoformat()
            if timed_out:
                with lock:
                    fh.write(f"STATUS: TIMEOUT\nEXIT_CODE: {exit_code}\nEND_AT: {end_at}\n")
                    fh.flush()
                return {"ok": False, "error": "timeout", "log_path": str(log_path)}

            status = "OK" if exit_code == 0 else "FAILED"
            with lock:
                fh.write(f"STATUS: {status}\nEXIT_CODE: {exit_code}\nEND_AT: {end_at}\n")
                fh.flush()
            if exit_code != 0:
                return {"ok": False, "error": "harness run script failed", "exit_code": exit_code, "log_path": str(log_path)}
            return {"ok": True, "log_path": str(log_path)}
        except Exception as e:
            with lock:
                fh.write(f"STATUS: FAILED\nERROR: {e}\n")
                fh.flush()
            return {"ok": False, "error": str(e), "log_path": str(log_path)}


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


def _compute_line_diff(before: list[str], after: list[str]) -> tuple[int, int]:
    added = 0
    deleted = 0
    matcher = difflib.SequenceMatcher(a=before, b=after)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += (j2 - j1)
        elif tag == "delete":
            deleted += (i2 - i1)
        elif tag == "replace":
            deleted += (i2 - i1)
            added += (j2 - j1)
    return added, deleted


def _unified_diff(before_text: str, after_text: str, from_name: str, to_name: str) -> str:
    before_lines = before_text.splitlines(keepends=True)
    after_lines = after_text.splitlines(keepends=True)
    diff_lines = difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=from_name,
        tofile=to_name,
        lineterm="",
        n=3,
    )
    return "\n".join(diff_lines)


def collect_change_record(paths: EvolverPaths, candidate_num: int, candidate_dir: Path) -> dict:
    """Collect a per-round change record (candidate harness vs current best harness)."""
    best_harness_dir = paths.best_dir / "harness"
    candidate_harness_dir = candidate_dir / "harness"

    best_files = {}
    if best_harness_dir.exists():
        for f in iter_effective_files(best_harness_dir):
            best_files[f.name] = f

    candidate_files = {}
    if candidate_harness_dir.exists():
        for f in iter_effective_files(candidate_harness_dir):
            candidate_files[f.name] = f

    all_names = sorted(set(best_files) | set(candidate_files))
    changed_files = []
    diffs: list[dict[str, str]] = []
    for name in all_names:
        best_file = best_files.get(name)
        candidate_file = candidate_files.get(name)

        if best_file is None and candidate_file is not None:
            after_text = candidate_file.read_text(encoding="utf-8", errors="replace")
            after_lines = after_text.splitlines()
            changed_files.append(
                {
                    "file": name,
                    "status": "new",
                    "added_lines": len(after_lines),
                    "deleted_lines": 0,
                    "line_delta": len(after_lines),
                }
            )
            diff_text = _unified_diff("", after_text, f"best/{name}", f"candidate/{name}")
            diffs.append({"file": name, "status": "new", "diff": diff_text})
            continue

        if best_file is not None and candidate_file is None:
            before_text = best_file.read_text(encoding="utf-8", errors="replace")
            before_lines = before_text.splitlines()
            changed_files.append(
                {
                    "file": name,
                    "status": "deleted",
                    "added_lines": 0,
                    "deleted_lines": len(before_lines),
                    "line_delta": -len(before_lines),
                }
            )
            diff_text = _unified_diff(before_text, "", f"best/{name}", f"candidate/{name}")
            diffs.append({"file": name, "status": "deleted", "diff": diff_text})
            continue

        before_text = best_file.read_text(encoding="utf-8", errors="replace")
        after_text = candidate_file.read_text(encoding="utf-8", errors="replace")
        before_lines = before_text.splitlines()
        after_lines = after_text.splitlines()
        if before_lines == after_lines:
            continue

        added, deleted = _compute_line_diff(before_lines, after_lines)
        changed_files.append(
            {
                "file": name,
                "status": "modified",
                "added_lines": added,
                "deleted_lines": deleted,
                "line_delta": len(after_lines) - len(before_lines),
            }
        )
        diff_text = _unified_diff(before_text, after_text, f"best/{name}", f"candidate/{name}")
        diffs.append({"file": name, "status": "modified", "diff": diff_text})

    record = {
        "candidate": f"candidate_{candidate_num}",
        "compared_against": str(best_harness_dir),
        "generated_at": datetime.now().isoformat(),
        "changed_files_count": len(changed_files),
        "changed_files": changed_files,
    }

    json_path = candidate_dir / "change_record.json"
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"# Change Record — candidate_{candidate_num}",
        "",
        f"- Compared against: `{best_harness_dir}`",
        f"- Generated at: `{record['generated_at']}`",
        "",
        "## Changed Files",
    ]
    if changed_files:
        for item in changed_files:
            delta = item["line_delta"]
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            lines.append(
                f"- `{item['file']}` ({item['status']}): +{item['added_lines']} / -{item['deleted_lines']} (line delta {delta_str})"
            )
    else:
        lines.append("- (no changes)")
    lines.append("")
    if diffs:
        lines.append("## Diffs")
        lines.append("")
        for item in diffs:
            lines.append(f"### {item['file']} ({item['status']})")
            lines.append("")
            lines.append("```diff")
            lines.append(item["diff"] or "(no diff)")
            lines.append("```")
            lines.append("")
    (candidate_dir / "change_record.md").write_text("\n".join(lines), encoding="utf-8")
    return record


def log_evolution(paths: EvolverPaths, candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool, change_record: dict):
    """Append to the evolution log."""
    log_file = paths.workspace / "evolution_log.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "candidate": f"candidate_{candidate_num}",
        "candidate_dir": str(candidate_dir),
        "proposer_success": proposer_ok,
        "scores": scores,
        "final_score": scores.get("final_score", 0),
        "changes": change_record,
    }
    with open(log_file, "a") as lf:
        lf.write(json.dumps(entry) + "\n")


def post_to_feishu(paths: EvolverPaths, candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool, prev_best_score: float | None):
    """Post summary to Feishu (Lark)."""
    if os.environ.get("FEISHU_POST_ENABLED", "1") != "1":
        print("[FEISHU] Disabled (FEISHU_POST_ENABLED!=1). Skipping.")
        return

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

    timeout_seconds = int(os.environ.get("FEISHU_POST_TIMEOUT_SECONDS", "30"))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        print(f"[FEISHU] Timeout after {timeout_seconds}s. Skipping.")
        return

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
    if len(sys.argv) >= 2 and sys.argv[1] == "--nexau-proposer-child":
        if len(sys.argv) < 3:
            raise SystemExit(2)
        raise SystemExit(_nexau_proposer_child(Path(sys.argv[2])))
    main()
