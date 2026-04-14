#!/usr/bin/env python3

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvolverConfig:
    harness_run_script: str = ""
    harness_run_timeout_seconds: int = 600
    require_harness_run_script: bool = False

    proposer_prompt_prefix: str = ""

    def proposer_prompt_suffix(self, workspace: Path, candidate_num: int) -> str:
        if not self.harness_run_script:
            return ""
        return "\n".join(
            [
                "",
                "## Harness Run Script",
                "After you generate the candidate harness files, a user-provided bash script will be executed before evaluation.",
                "Make sure your changes are runnable by that script.",
                f"- Script: {self.harness_run_script}",
                f"- Candidate dir (argv[1]): {workspace / 'candidates' / f'candidate_{candidate_num}'}",
                f"- EVOLVER_WORKSPACE (env): {workspace}",
                f"- CANDIDATE_NUM (env): {candidate_num}",
                "",
            ]
        )


def load_config() -> EvolverConfig:
    run_script = os.environ.get("HARNESS_RUN_SCRIPT", "")
    require = os.environ.get("REQUIRE_HARNESS_RUN_SCRIPT", "0") == "1"
    timeout = int(os.environ.get("HARNESS_RUN_TIMEOUT_SECONDS", "600"))
    prefix = os.environ.get("PROPOSER_PROMPT_PREFIX", "")
    return EvolverConfig(
        harness_run_script=run_script,
        harness_run_timeout_seconds=timeout,
        require_harness_run_script=require,
        proposer_prompt_prefix=prefix,
    )
