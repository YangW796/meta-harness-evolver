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
WORKSPACE_DIR="$PROJECT_DIR/hoss-evolution"
EVALUATE_SCRIPT_PATH="$PROJECT_DIR/evaluate_project1.py"
CANDIDATE_NUM=""
ITERATIONS="${ITERATIONS:-1}"

export EVOLVER_WORKSPACE="$WORKSPACE_DIR"
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="3600"

# Default: test mode off (set to 1 for quick dry run without real proposer edits)
export EVOLVER_TEST_MODE="${EVOLVER_TEST_MODE:-0}"

ARGS=(python "$EVOLVER_ROOT/scripts/run_evolution.py" --workspace "$WORKSPACE_DIR" --iterations "$ITERATIONS" --evaluate-script "$EVALUATE_SCRIPT_PATH")
if [[ -n "$CANDIDATE_NUM" ]]; then
  ARGS+=(--candidate-num "$CANDIDATE_NUM")
fi

cd "$EVOLVER_ROOT"
conda run -n "$CONDA_ENV" "${ARGS[@]}"
