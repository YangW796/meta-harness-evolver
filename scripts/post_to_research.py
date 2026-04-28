#!/usr/bin/env python3
"""
Post evolution results to Feishu (Lark) via lark-oapi.

Usage:
  python3 post_to_research.py <candidate_num> <candidate_dir> <score> <proposer_success> [--workspace DIR] [--prev-best-score FLOAT]
"""

import argparse
import os
import json
import uuid
from pathlib import Path
from datetime import datetime

from shared import get_workspace, iter_effective_files_recursive, load_env_file

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
ENV_FILE = ROOT_DIR / ".env"
load_env_file(ENV_FILE)

FEISHU_APP_ID_ENV = "FEISHU_APP_ID"
FEISHU_APP_SECRET_ENV = "FEISHU_APP_SECRET"
FEISHU_RECEIVE_ID_ENV = "FEISHU_RECEIVE_ID"
FEISHU_RECEIVE_ID_TYPE_ENV = "FEISHU_RECEIVE_ID_TYPE"

def get_history_summary(workspace: Path) -> str:
    """Get evolution history from log."""
    log_file = workspace / "evolution_log.jsonl"
    if not log_file.exists():
        return "No prior history."

    entries = []
    with open(log_file) as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    if not entries:
        return "No prior history."

    # Show last 5 entries
    recent = entries[-5:]
    lines = []
    for e in recent:
        ts = datetime.fromisoformat(e["timestamp"]).strftime("%m-%d %H:%M")
        lines.append(f"  • {e['candidate']}: {e['final_score']}/100")

    return "\n".join(lines) if lines else "No prior history."


def get_best_score(workspace: Path) -> float:
    """Get the current best score."""
    best_file = workspace / "best" / "current" / "eval_scores.json"
    if best_file.exists():
        return json.loads(best_file.read_text()).get("final_score", 0)
    return 0


def get_proposer_reasoning(candidate_dir: Path) -> str:
    """Read the proposer's reasoning trace."""
    reasoning_file = candidate_dir / "proposer_reasoning.md"
    if reasoning_file.exists():
        content = reasoning_file.read_text()
        # Truncate if too long
        if len(content) > 500:
            return content[:500] + "..."
        return content
    return "No reasoning trace found."


def get_change_summary(workspace: Path, candidate_dir: Path) -> str:
    """Diff harness files vs best to show what changed."""
    best_dir = workspace / "best" / "current" / "harness"
    candidate_harness = candidate_dir / "harness"

    if not candidate_harness.exists():
        return "  (no harness dir)"

    best_files = (
        {f.relative_to(best_dir).as_posix(): f for f in iter_effective_files_recursive(best_dir)}
        if best_dir.exists()
        else {}
    )
    cand_files = {f.relative_to(candidate_harness).as_posix(): f for f in iter_effective_files_recursive(candidate_harness)}
    all_names = sorted(set(best_files) | set(cand_files))

    changes = []
    for name in all_names:
        best_file = best_files.get(name)
        cand_file = cand_files.get(name)

        if best_file is None and cand_file is not None:
            changes.append(f"  + {name} (new)")
            continue
        if best_file is not None and cand_file is None:
            changes.append(f"  - {name} (deleted)")
            continue
        if best_file is None or cand_file is None:
            continue

        best_content = best_file.read_text(encoding="utf-8", errors="replace")
        cand_content = cand_file.read_text(encoding="utf-8", errors="replace")
        if best_content != cand_content:
            best_lines = len(best_content.split("\n"))
            cand_lines = len(cand_content.split("\n"))
            diff = cand_lines - best_lines
            sign = "+" if diff > 0 else ""
            changes.append(f"  ~ {name} ({sign}{diff} lines)")

    if not changes:
        return "  (no diff — identical to current best)"

    return "\n".join(changes[:5])  # Limit to 5 changes


def build_message(workspace: Path, candidate_num: int, candidate_dir: Path, score: float, proposer_ok: bool, prev_best_score: float | None) -> str:
    """Build the Feishu text message."""

    best_score = prev_best_score if prev_best_score is not None else get_best_score(workspace)
    delta = score - best_score
    delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"

    history = get_history_summary(workspace)
    reasoning = get_proposer_reasoning(candidate_dir)
    changes = get_change_summary(workspace, candidate_dir)

    candidate_dir = Path(candidate_dir)

    status = "NEW BEST!" if score > best_score else "no change" if score == best_score else f"{delta_str} vs best"
    proposer_status = "SUCCESS" if proposer_ok else "FAILED"

    msg = "\n".join([
        "Meta-Harness Evolution — Report",
        f"Candidate: candidate_{candidate_num}",
        f"Score: {score}/100 ({status})",
        f"Proposer: {proposer_status}",
        "",
        "What Changed:",
        changes,
        "",
        "Proposer Reasoning:",
        reasoning,
        "",
        "Recent History:",
        history,
        "",
        f"Posted {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ])

    return msg


def send_feishu_text(message: str) -> bool:
    if os.environ.get("FEISHU_DRY_RUN") == "1":
        print("FEISHU_DRY_RUN=1; skipping send.")
        return True

    app_id = os.environ.get(FEISHU_APP_ID_ENV)
    app_secret = os.environ.get(FEISHU_APP_SECRET_ENV)
    receive_id = os.environ.get(FEISHU_RECEIVE_ID_ENV)
    receive_id_type = os.environ.get(FEISHU_RECEIVE_ID_TYPE_ENV, "open_id")

    missing = [k for k, v in [
        (FEISHU_APP_ID_ENV, app_id),
        (FEISHU_APP_SECRET_ENV, app_secret),
        (FEISHU_RECEIVE_ID_ENV, receive_id),
    ] if not v]
    if missing:
        print(f"Feishu not configured. Missing env: {', '.join(missing)}")
        return False

    try:
        import lark_oapi as lark
        from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    except Exception as e:
        print(f"Feishu SDK not available: {e}")
        print("Install: pip install lark-oapi -U")
        return False

    client = lark.Client.builder().app_id(app_id).app_secret(app_secret).build()
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(json.dumps({"text": message}, ensure_ascii=False))
            .uuid(str(uuid.uuid4()))
            .build()
        ) \
        .build()

    response = client.im.v1.message.create(request)
    if not response.success():
        try:
            raw = json.dumps(json.loads(response.raw.content), indent=2, ensure_ascii=False)
        except Exception:
            raw = str(response.raw.content)
        print(
            "client.im.v1.message.create failed, "
            f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp:\n{raw}"
        )
        return False

    print("Posted to Feishu successfully")
    return True


def main():
    parser = argparse.ArgumentParser(description="Post evolution results to Feishu (Lark)")
    parser.add_argument("candidate_num", type=int)
    parser.add_argument("candidate_dir", type=Path)
    parser.add_argument("score", type=float)
    parser.add_argument("proposer_success", type=int, choices=[0, 1])
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Evolution workspace directory (default: $EVOLVER_WORKSPACE or ~/hoss-evolution)",
    )
    parser.add_argument(
        "--prev-best-score",
        type=float,
        default=None,
        help="Best score before this iteration (used to compute delta correctly)",
    )
    args = parser.parse_args()

    workspace = (args.workspace.expanduser().resolve() if args.workspace else get_workspace())
    proposer_ok = bool(args.proposer_success)

    message = build_message(
        workspace=workspace,
        candidate_num=args.candidate_num,
        candidate_dir=args.candidate_dir,
        score=args.score,
        proposer_ok=proposer_ok,
        prev_best_score=args.prev_best_score,
    )

    print("FEISHU_MESSAGE:")
    print(message)
    print("END_FEISHU_MESSAGE")

    if not send_feishu_text(message):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
