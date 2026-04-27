#!/usr/bin/env bash
set -euo pipefail

EVOLVER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ENV_FILE="$EVOLVER_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi
source ~/miniconda3/etc/profile.d/conda.sh
CONDA_ENV="meta-harness-evolver0"
WORKSPACE_DIR="$PROJECT_DIR/hoss-evolution"
EVALUATE_SCRIPT_PATH="$PROJECT_DIR/evaluate_project1.py"
CANDIDATE_NUM=""
ITERATIONS="${ITERATIONS:-1}"

export EVOLVER_WORKSPACE="$WORKSPACE_DIR"
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="3600"
export NEXAU_ENABLE_RUN_SHELL_COMMAND="0"

# Default: test mode off (set to 1 for quick dry run without real proposer edits)
export EVOLVER_TEST_MODE="${EVOLVER_TEST_MODE:-0}"

if [[ -z "${HARNESS_DEVICE:-}" ]]; then
  USE_GPU="${USE_GPU:-0}"
  if [[ "$USE_GPU" == "1" ]]; then
    export HARNESS_DEVICE="cuda"
  else
    export HARNESS_DEVICE="cpu"
  fi
fi
export HARNESS_BATCH_SIZE="${HARNESS_BATCH_SIZE:-16}"
export PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}"

PROPOSER_PROMPT_PREFIX_PATH="$PROJECT_DIR/proposer_prompt_prefix.txt"
if [[ ! -f "$PROPOSER_PROMPT_PREFIX_PATH" ]]; then
  echo "Missing proposer prompt prefix file: $PROPOSER_PROMPT_PREFIX_PATH" >&2
  exit 2
fi
export PROPOSER_PROMPT_PREFIX="$(cat "$PROPOSER_PROMPT_PREFIX_PATH")"$'\n'



ARGS=(python -u "$EVOLVER_ROOT/scripts/run_evolution.py" --workspace "$WORKSPACE_DIR" --iterations "$ITERATIONS" --evaluate-script "$EVALUATE_SCRIPT_PATH")
if [[ -n "$CANDIDATE_NUM" ]]; then
  ARGS+=(--candidate-num "$CANDIDATE_NUM")
fi

cd "$EVOLVER_ROOT"
CONDA_RUN_ARGS=(-n "$CONDA_ENV")
if conda run --help 2>/dev/null | grep -q -- "--no-capture-output"; then
  CONDA_RUN_ARGS=(--no-capture-output -n "$CONDA_ENV")
fi
conda run "${CONDA_RUN_ARGS[@]}" "${ARGS[@]}"
