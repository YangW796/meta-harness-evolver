from __future__ import annotations

import os
import re
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

from evolver_config import EvolverConfig
from shared import iter_effective_files, iter_effective_files_recursive, resolve_maybe_relative_path


def _sanitize_python_smart_quotes(path: Path) -> bool:
    try:
        raw = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False

    repl = {
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
    }
    new = raw
    for a, b in repl.items():
        new = new.replace(a, b)
    if new == raw:
        return False
    try:
        path.write_text(new, encoding="utf-8")
    except Exception:
        return False
    return True


def validate_candidate(candidate_dir: Path) -> bool:
    print(f"[VALIDATE] Checking {candidate_dir}/harness/...")

    harness_dir = candidate_dir / "harness"
    if not harness_dir.exists():
        print("[VALIDATE] Missing harness directory")
        return False

    files = list(iter_effective_files_recursive(harness_dir))
    if not files:
        print("[VALIDATE] No files found in harness directory")
        return False

    for f in files:
        if f.suffix == ".py":
            import py_compile

            if str(os.environ.get("EVOLVER_SANITIZE_SMART_QUOTES", "1")).strip() == "1":
                changed = _sanitize_python_smart_quotes(f)
                if changed:
                    print(f"[VALIDATE] Sanitized smart quotes in {f.name}")

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
    script_path = resolve_maybe_relative_path(script_path)

    cmd = ["bash", str(script_path), str(candidate_dir)]
    env = os.environ.copy()
    env["EVOLVER_WORKSPACE"] = str(workspace)
    env["CANDIDATE_NUM"] = str(candidate_num)
    env["CANDIDATE_DIR"] = str(candidate_dir)

    progress_sample_seconds = float(os.environ.get("HARNESS_RUN_LOG_PROGRESS_SAMPLE_SECONDS", "5") or "5")
    progress_last_write: dict[str, float] = {}
    progress_last_percent: dict[str, int] = {}
    progress_last_epoch: dict[str, int] = {}

    progress_re = re.compile(r"^Epoch\s+(\d+):\s+(\d+)%\|")

    def _maybe_write_line(prefix: str, line: str, fh, lock: threading.Lock) -> None:
        text = line.rstrip("\n").replace("\r", "")
        m = progress_re.match(text)
        if m is not None and progress_sample_seconds > 0:
            now = time.time()
            try:
                epoch = int(m.group(1))
                pct = int(m.group(2))
            except Exception:
                epoch = -1
                pct = -1

            allowed_pct = pct in {25, 50, 75, 100}
            allowed_epoch = (epoch >= 0 and epoch % 10 == 0) or pct == 100
            if not (allowed_pct and allowed_epoch):
                return
            last_pct = progress_last_percent.get(prefix, -999)
            last_epoch = progress_last_epoch.get(prefix, -999)
            last_ts = progress_last_write.get(prefix, 0.0)
            if pct == last_pct and epoch == last_epoch and (now - last_ts) < progress_sample_seconds:
                return
            progress_last_percent[prefix] = pct
            progress_last_epoch[prefix] = epoch
            progress_last_write[prefix] = now

        with lock:
            fh.write(f"[{prefix}] {text}\n")
            fh.flush()

    def _stream_pipe(pipe, prefix: str, fh, lock: threading.Lock) -> None:
        try:
            for line in iter(pipe.readline, ""):
                _maybe_write_line(prefix, line, fh, lock)
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
