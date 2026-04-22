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

CONDA_ENV="meta-harness-evolver0"
DEFAULT_WORKSPACE_DIR="$PROJECT_DIR/hoss-evolution"
WORKSPACE_DIR="${EVOLVER_WORKSPACE:-$DEFAULT_WORKSPACE_DIR}"
EVALUATE_SCRIPT_PATH="$PROJECT_DIR/evaluate.py"
CANDIDATE_NUM=""
ITERATIONS="${ITERATIONS:-20}"
export PROPOSER_MAX_ITERATIONS=40
export PROPOSER_TIMEOUT_SECONDS=600
export EVOLVER_WORKSPACE="$WORKSPACE_DIR"
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="3600"
export FEISHU_POST_ENABLED=0
export NEXAU_ENABLE_RUN_SHELL_COMMAND="0"
# Default: test mode off (set to 1 for quick dry run without real proposer edits)
export EVOLVER_TEST_MODE="${EVOLVER_TEST_MODE:-0}"

USE_GPU="${USE_GPU:-1}"
GPU_COUNT="0"
if command -v nvidia-smi >/dev/null 2>&1; then
  GPU_COUNT="$(nvidia-smi -L 2>/dev/null | grep -c '^GPU ' || true)"
fi
if [[ "$GPU_COUNT" == "0" ]]; then
  if compgen -G "/dev/nvidia[0-9]*" >/dev/null; then
    GPU_COUNT="$(ls -1 /dev/nvidia[0-9]* 2>/dev/null | wc -l | tr -d ' ')"
  fi
fi

if [[ -z "${HARNESS_DEVICE:-}" ]]; then
  if [[ "$USE_GPU" == "1" && "${GPU_COUNT:-0}" != "0" ]]; then
    export HARNESS_DEVICE="cuda"
  else
    export HARNESS_DEVICE="cpu"
  fi
fi

if [[ "${HARNESS_DEVICE:-}" == "cuda" && "$USE_GPU" == "1" && "${GPU_COUNT:-0}" != "0" ]]; then
  export EVOLVER_NUM_GPUS="$GPU_COUNT"
else
  export EVOLVER_NUM_GPUS="0"
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
