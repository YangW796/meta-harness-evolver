from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import traceback
from pathlib import Path


def tail_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...(truncated)\n"


def tail_file(path: Path, max_bytes: int = 8000) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    if len(data) <= max_bytes:
        return data.decode("utf-8", errors="replace")
    return data[-max_bytes:].decode("utf-8", errors="replace")


def run_proposer_with_nexau(
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
    print(tail_text(task, 4000))
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
        tail = tail_file(log_path)
        if tail:
            print("[PROPOSER] NexAU log tail:")
            print(tail)
        raise

    stdout_tail = tail_text(result.stdout or "", 2000)
    stderr_tail = tail_text(result.stderr or "", 2000)
    if stdout_tail.strip():
        print("[PROPOSER] NexAU stdout (truncated):")
        print(stdout_tail)
    if stderr_tail.strip():
        print("[PROPOSER] NexAU stderr (truncated):")
        print(stderr_tail)

    log_tail = tail_file(log_path)
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


def nexau_proposer_child(log_path: Path) -> int:
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

        skills: list[Skill] = []

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


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--nexau-proposer-child":
        if len(sys.argv) < 3:
            return 2
        return nexau_proposer_child(Path(sys.argv[2]))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

