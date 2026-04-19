from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent


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
    scores_file = paths.best_dir / "eval_scores.json"
    if scores_file.exists():
        return json.loads(scores_file.read_text())
    return None

