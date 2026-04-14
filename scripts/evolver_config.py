#!/usr/bin/env python3

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvolverConfig:
    harness_entrypoints: tuple[str, ...] = ("run.py", "main.py", "entry.py", "model.py")
    harness_input_filename: str = "ai4s_input.json"
    harness_output_filename: str = "ai4s_output.json"
    harness_meta_filename: str = "ai4s_meta.json"
    harness_run_timeout_seconds: int = 600
    enable_harness_execution: bool = True
    require_harness_execution: bool = False

    proposer_prompt_prefix: str = ""

    def harness_io_spec(self) -> str:
        return "\n".join(
            [
                "## Harness Executable I/O Contract",
                "- Your output harness may include an executable entrypoint file inside the candidate's harness/ directory.",
                "- If you include an executable, it MUST implement a CLI interface:",
                "  - --input <path>   : JSON input data file",
                "  - --output <path>  : JSON output result file (must be created)",
                "  - --meta <path>    : JSON metadata file (optional, may be ignored)",
                "- The entrypoint MUST be one of: "
                + ", ".join(self.harness_entrypoints),
                "- The output JSON should be valid JSON and include at least:",
                "  - ok: boolean",
                "  - error: string (if ok=false)",
                "  - result: object (if ok=true)",
            ]
        )

    def proposer_prompt_suffix(self, workspace: Path, candidate_num: int) -> str:
        meta_path = workspace / "candidates" / f"candidate_{candidate_num}" / self.harness_meta_filename
        in_path = workspace / "candidates" / f"candidate_{candidate_num}" / self.harness_input_filename
        out_path = workspace / "candidates" / f"candidate_{candidate_num}" / self.harness_output_filename
        return "\n".join(
            [
                "",
                self.harness_io_spec(),
                "",
                "## Paths for This Iteration",
                f"- Input JSON: {in_path}",
                f"- Output JSON: {out_path}",
                f"- Meta JSON: {meta_path}",
                "",
            ]
        )


def load_config() -> EvolverConfig:
    enable = os.environ.get("ENABLE_HARNESS_EXECUTION", "1") == "1"
    require = os.environ.get("REQUIRE_HARNESS_EXECUTION", "0") == "1"
    timeout = int(os.environ.get("HARNESS_RUN_TIMEOUT_SECONDS", "600"))
    prefix = os.environ.get("PROPOSER_PROMPT_PREFIX", "")
    entrypoints_raw = os.environ.get("HARNESS_ENTRYPOINTS")
    input_name = os.environ.get("HARNESS_INPUT_FILENAME", "ai4s_input.json")
    output_name = os.environ.get("HARNESS_OUTPUT_FILENAME", "ai4s_output.json")
    meta_name = os.environ.get("HARNESS_META_FILENAME", "ai4s_meta.json")
    entrypoints = tuple([x.strip() for x in (entrypoints_raw or "").split(",") if x.strip()]) or EvolverConfig().harness_entrypoints
    return EvolverConfig(
        harness_entrypoints=entrypoints,
        harness_input_filename=input_name,
        harness_output_filename=output_name,
        harness_meta_filename=meta_name,
        harness_run_timeout_seconds=timeout,
        enable_harness_execution=enable,
        require_harness_execution=require,
        proposer_prompt_prefix=prefix,
    )
