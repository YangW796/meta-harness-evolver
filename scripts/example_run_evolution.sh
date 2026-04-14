#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVOLVER_DIR="$ROOT_DIR/meta-harness-evolver"
ENV_FILE="${ENV_FILE:-$EVOLVER_DIR/.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

CONDA_ENV="${CONDA_ENV:-meta-harness-evolver}"
WORKSPACE_DIR="${EVOLVER_WORKSPACE:-$ROOT_DIR/hoss-evolution}"
EVALUATE_SCRIPT_PATH="${EVALUATE_SCRIPT:-$EVOLVER_DIR/scripts/evaluate.py}"

CANDIDATE_NUM="${CANDIDATE_NUM:-}"
if [[ "${1:-}" != "" ]]; then
  CANDIDATE_NUM="$1"
fi

export FEISHU_DRY_RUN="${FEISHU_DRY_RUN:-1}"
export EVOLVER_TEST_MODE="${EVOLVER_TEST_MODE:-0}"

ARGS=(python "$EVOLVER_DIR/scripts/run_evolution.py" --workspace "$WORKSPACE_DIR" --evaluate-script "$EVALUATE_SCRIPT_PATH")
if [[ -n "$CANDIDATE_NUM" ]]; then
  ARGS+=(--candidate-num "$CANDIDATE_NUM")
fi

cd "$ROOT_DIR"
conda run -n "$CONDA_ENV" "${ARGS[@]}"

#bash meta-harness-evolver/scripts/example_run_evolution.sh
#bash meta-harness-evolver/scripts/example_run_evolution.sh 8