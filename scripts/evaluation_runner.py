from __future__ import annotations

import difflib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from evolution_paths import EvolverPaths
from shared import iter_effective_files, iter_effective_files_recursive, resolve_maybe_relative_path


def evaluate_candidate(paths: EvolverPaths, candidate_dir: Path, evaluate_script: str | None) -> dict:
    print(f"[EVALUATE] Running benchmark for {candidate_dir.name}...")

    if evaluate_script:
        script_path = resolve_maybe_relative_path(evaluate_script)

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
    best_scores_file = paths.best_dir / "eval_scores.json"
    best_harness_dir = paths.best_dir / "harness"

    current_best: float | None = None
    if best_scores_file.exists():
        current_best = float(json.loads(best_scores_file.read_text()).get("final_score", 0))

    new_score = scores.get("final_score", 0)

    if current_best is None or new_score > current_best:
        print(f"[BEST] New best! {new_score} > {current_best}")
        paths.best_dir.mkdir(parents=True, exist_ok=True)
        if best_harness_dir.exists():
            import shutil

            shutil.rmtree(best_harness_dir)
        best_harness_dir.mkdir(parents=True, exist_ok=True)

        import shutil

        candidate_harness = candidate_dir / "harness"
        for f in iter_effective_files_recursive(candidate_harness):
            rel = f.relative_to(candidate_harness)
            dst = best_harness_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)

        with open(best_scores_file, "w") as sf:
            json.dump(scores, sf, indent=2)

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
    return "".join(difflib.unified_diff(before_lines, after_lines, fromfile=from_name, tofile=to_name))


def collect_change_record(paths: EvolverPaths, candidate_num: int, candidate_dir: Path) -> dict:
    best_harness_dir = paths.best_dir / "harness"
    candidate_harness_dir = candidate_dir / "harness"

    best_files: dict[str, Path] = {}
    if best_harness_dir.exists():
        for f in iter_effective_files_recursive(best_harness_dir):
            best_files[f.relative_to(best_harness_dir).as_posix()] = f

    candidate_files: dict[str, Path] = {}
    if candidate_harness_dir.exists():
        for f in iter_effective_files_recursive(candidate_harness_dir):
            candidate_files[f.relative_to(candidate_harness_dir).as_posix()] = f

    all_names = sorted(set(best_files) | set(candidate_files))
    changed_files: list[dict] = []
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
            diffs.append({"file": name, "diff": diff_text})
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
            diffs.append({"file": name, "diff": diff_text})
            continue

        if best_file is None or candidate_file is None:
            continue

        before_text = best_file.read_text(encoding="utf-8", errors="replace")
        after_text = candidate_file.read_text(encoding="utf-8", errors="replace")
        if before_text == after_text:
            continue
        before_lines = before_text.splitlines()
        after_lines = after_text.splitlines()
        added, deleted = _compute_line_diff(before_lines, after_lines)
        changed_files.append(
            {
                "file": name,
                "status": "modified",
                "added_lines": int(added),
                "deleted_lines": int(deleted),
                "line_delta": int(added - deleted),
            }
        )
        diff_text = _unified_diff(before_text, after_text, f"best/{name}", f"candidate/{name}")
        diffs.append({"file": name, "diff": diff_text})

    record = {
        "candidate": f"candidate_{candidate_num}",
        "compared_against": str(best_harness_dir),
        "generated_at": datetime.now().isoformat(),
        "changed_files_count": len(changed_files),
        "changed_files": changed_files,
    }

    change_record_json = candidate_dir / "change_record.json"
    change_record_md = candidate_dir / "change_record.md"
    with open(change_record_json, "w") as f:
        json.dump({**record, "diffs": diffs}, f, indent=2)

    md_lines = [
        f"# Change Record — candidate_{candidate_num}",
        "",
        f"Compared against: {best_harness_dir}",
        f"Generated at: {record['generated_at']}",
        "",
        "## Files Changed",
        "",
    ]
    for cf in changed_files:
        md_lines.append(
            f"- {cf['file']}: {cf['status']} (added={cf['added_lines']}, deleted={cf['deleted_lines']}, delta={cf['line_delta']})"
        )
    md_lines.append("")
    md_lines.append("## Diffs")
    md_lines.append("")
    for d in diffs:
        md_lines.append(f"### {d['file']}")
        md_lines.append("")
        md_lines.append("```diff")
        md_lines.append(d["diff"])
        md_lines.append("```")
        md_lines.append("")

    change_record_md.write_text("\n".join(md_lines), encoding="utf-8")
    return record


def log_evolution(paths: EvolverPaths, candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool, change_record: dict):
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
    if os.environ.get("FEISHU_POST_ENABLED", "1") != "1":
        return

    script_path = paths.scripts_dir / "post_to_research.py"
    if not script_path.exists():
        return

    try:
        score = float(scores.get("final_score", 0.0))
    except Exception:
        score = 0.0
    proposer_success = 1 if proposer_ok else 0

    cmd = [
        sys.executable,
        str(script_path),
        str(candidate_num),
        str(candidate_dir),
        str(score),
        str(proposer_success),
        "--workspace",
        str(paths.workspace),
    ]
    if prev_best_score is not None:
        cmd.extend(["--prev-best-score", str(prev_best_score)])

    try:
        timeout_seconds = int(os.environ.get("FEISHU_POST_TIMEOUT_SECONDS", "30"))
    except Exception:
        timeout_seconds = 30
    subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds)
