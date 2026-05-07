from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
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


def _parse_json_from_stdout(stdout: str) -> dict | None:
    s = (stdout or "").strip()
    if not s:
        return None
    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else None
    except Exception:
        pass
    try:
        last = s.splitlines()[-1]
        obj = json.loads(last)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def run_proposer_with_claude_code(
    task: str,
    label: str,
    work_dir: Path,
    timeout_seconds: int,
    log_dir: Path,
    max_iterations_override: int | None = None,
) -> dict:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{label}.log"

    try:
        subprocess.run(
            [str(os.environ.get("CLAUDE_BIN", "claude")).strip() or "claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        raise RuntimeError("Claude Code CLI not found. Set CLAUDE_BIN or ensure `claude` is on PATH.")

    proposer_max_iterations = int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20"))
    if max_iterations_override is not None:
        proposer_max_iterations = int(max_iterations_override)
    proposer_timeout_seconds = int(os.environ.get("PROPOSER_TIMEOUT_SECONDS", str(timeout_seconds)))

    print("[PROPOSER] LLM input (truncated):")
    print(tail_text(task, 4000))
    print(f"[PROPOSER] LLM input length: {len(task)} chars")
    print(f"[PROPOSER] Claude Code log: {log_path}")
    print(f"[PROPOSER] Claude Code limits: max_turns={proposer_max_iterations}, timeout_seconds={proposer_timeout_seconds}")

    payload = {
        "task": task,
        "label": label,
        "work_dir": str(work_dir),
        "max_iterations": proposer_max_iterations,
    }

    cmd = [sys.executable, str(Path(__file__).resolve()), "--claude-code-proposer-child", str(log_path)]
    env = os.environ.copy()
    env["EVOLVER_WORKSPACE"] = str(work_dir)
    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=proposer_timeout_seconds,
            cwd=str(work_dir),
            env=env,
        )
    except subprocess.TimeoutExpired:
        print(f"[PROPOSER] Claude Code proposer timed out after {proposer_timeout_seconds}s")
        tail = tail_file(log_path)
        if tail:
            print("[PROPOSER] Claude Code log tail:")
            print(tail)
        raise

    stdout_tail = tail_text(result.stdout or "", 2000)
    stderr_tail = tail_text(result.stderr or "", 2000)
    if stdout_tail.strip():
        print("[PROPOSER] Claude Code stdout (truncated):")
        print(stdout_tail)
    if stderr_tail.strip():
        print("[PROPOSER] Claude Code stderr (truncated):")
        print(stderr_tail)

    log_tail = tail_file(log_path)
    if log_tail.strip():
        print("[PROPOSER] Claude Code log tail:")
        print(log_tail)

    parsed = _parse_json_from_stdout(result.stdout or "")
    if parsed is None:
        parsed = {"ok": False, "error": "Failed to parse Claude Code child output as JSON", "stdout": result.stdout}

    if result.returncode != 0 or not parsed.get("ok", False):
        err = parsed.get("error") or f"child_exit_code={result.returncode}"
        raise RuntimeError(err)

    return {
        "label": label,
        "output": parsed.get("output"),
        "timeout_seconds": timeout_seconds,
        "log_path": str(log_path),
    }


def claude_code_proposer_child(log_path: Path) -> int:
    payload_raw = sys.stdin.read()
    try:
        payload = json.loads(payload_raw)
    except Exception:
        payload = {"task": payload_raw, "label": "unknown", "work_dir": os.getcwd()}

    label = str(payload.get("label", "claude-code-proposer"))
    task = str(payload.get("task", ""))
    work_dir = Path(str(payload.get("work_dir", os.getcwd()))).resolve()
    max_iterations = int(payload.get("max_iterations", 20))

    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler(sys.stderr)],
    )
    logger = logging.getLogger(__name__)
    logger.info("Claude Code proposer child started")
    logger.info("label=%s work_dir=%s task_len=%s max_turns=%s", label, work_dir, len(task), max_iterations)

    dry_run = str(os.environ.get("CLAUDE_CODE_DRY_RUN", "")).strip() == "1"
    if dry_run:
        try:
            candidate_harness = work_dir / "harness"
            candidate_harness.mkdir(parents=True, exist_ok=True)
            model_py = candidate_harness / "model.py"
            if not model_py.exists():
                model_py.write_text("def select(candidates, history, batch_size, seed):\n    return []\n", encoding="utf-8")
            txt = model_py.read_text(encoding="utf-8", errors="replace")
            if "def select" in txt and "return []" in txt:
                model_py.write_text(txt.replace("return []", "return list(range(min(int(batch_size), len(candidates))))"), encoding="utf-8")
            reasoning = work_dir / "proposer_reasoning.md"
            reasoning.write_text("Claude Code dry run: wrote a minimal deterministic select() implementation.\n", encoding="utf-8")
            print(json.dumps({"ok": True, "output": "dry_run"}, ensure_ascii=False))
            return 0
        except Exception as e:
            print(json.dumps({"ok": False, "error": f"dry_run_failed: {e}"}, ensure_ascii=False))
            return 1

    claude_bin = str(os.environ.get("CLAUDE_BIN", "claude")).strip() or "claude"
    model = str(os.environ.get("CLAUDE_MODEL", "")).strip()
    allowed_tools = str(os.environ.get("CLAUDE_ALLOWED_TOOLS", "Read,Edit")).strip()
    permission_mode = str(os.environ.get("CLAUDE_PERMISSION_MODE", "acceptEdits")).strip()
    output_format = str(os.environ.get("CLAUDE_OUTPUT_FORMAT", "text")).strip() or "text"
    extra_add_dirs = [s.strip() for s in str(os.environ.get("CLAUDE_ADD_DIRS", "")).split(",") if s.strip()]

    if not str(os.environ.get("ANTHROPIC_API_KEY", "")).strip():
        print(json.dumps({"ok": False, "error": "Missing ANTHROPIC_API_KEY. Run `claude /login` or export ANTHROPIC_API_KEY."}, ensure_ascii=False))
        return 1

    cmd = [
        claude_bin,
        "--bare",
        "--output-format",
        output_format,
        "--permission-mode",
        permission_mode,
        "--allowedTools",
        allowed_tools,
        "--max-turns",
        str(int(max_iterations)),
        "-p",
        task,
    ]
    for d in extra_add_dirs:
        cmd.extend(["--add-dir", d])

    logger.info("cmd=%s", cmd)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(work_dir),
            env=os.environ.copy(),
        )
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"failed_to_run_claude: {e}"}, ensure_ascii=False))
        return 1

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    logger.info("exit_code=%s", result.returncode)
    if stdout.strip():
        logger.info("stdout_tail=%s", tail_text(stdout, 4000))
    if stderr.strip():
        logger.info("stderr_tail=%s", tail_text(stderr, 4000))

    parsed = _parse_json_from_stdout(stdout)
    if result.returncode != 0:
        msg = (stderr.strip().splitlines()[-1] if stderr.strip() else "") or f"claude_exit_code={result.returncode}"
        print(json.dumps({"ok": False, "error": msg, "stdout": stdout}, ensure_ascii=False))
        return 1

    print(json.dumps({"ok": True, "output": stdout}, ensure_ascii=False))
    return 0


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "--claude-code-proposer-child":
        return claude_code_proposer_child(Path(sys.argv[2]))
    raise SystemExit("Unknown mode")


if __name__ == "__main__":
    raise SystemExit(main())
