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

export EVOLVER_WORKSPACE="${EVOLVER_WORKSPACE:-$PROJECT_DIR/hoss-evolution}"
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="${HARNESS_RUN_TIMEOUT_SECONDS:-600}"
export FEISHU_POST_ENABLED=0

export PROPOSER_MAX_ITERATIONS="${PROPOSER_MAX_ITERATIONS:-30}"
export PROPOSER_TIMEOUT_SECONDS="${PROPOSER_TIMEOUT_SECONDS:-600}"
export PROPOSER_LLM_TIMEOUT_SECONDS="${PROPOSER_LLM_TIMEOUT_SECONDS:-}"
export NEXAU_ENABLE_RUN_SHELL_COMMAND="${NEXAU_ENABLE_RUN_SHELL_COMMAND:-0}"

PROPOSER_PROMPT_PREFIX_PATH="$PROJECT_DIR/proposer_prompt_prefix.txt"
if [[ ! -f "$PROPOSER_PROMPT_PREFIX_PATH" ]]; then
  echo "Missing proposer prompt prefix file: $PROPOSER_PROMPT_PREFIX_PATH" >&2
  exit 2
fi
export PROPOSER_PROMPT_PREFIX="$(cat "$PROPOSER_PROMPT_PREFIX_PATH")"$'\n'

ITERATIONS="${ITERATIONS:-1}"
EVALUATE_SCRIPT_PATH="$PROJECT_DIR/evaluate.py"

if [[ -z "${LLM_MODEL:-}" || -z "${LLM_API_KEY:-}" ]]; then
  echo "Missing LLM_MODEL / LLM_API_KEY. Put them in .env or export them before running." >&2
  exit 2
fi
if [[ -z "${NEXAU_CODE_AGENT_DIR:-}" ]]; then
  echo "Missing NEXAU_CODE_AGENT_DIR (path to NexAU examples/code_agent)." >&2
  exit 2
fi
if [[ -z "${PROJECT_PU_P_CSV:-}" || ! -f "${PROJECT_PU_P_CSV:-}" ]]; then
  echo "Missing PROJECT_PU_P_CSV=/path/to/P.csv" >&2
  exit 2
fi
if [[ -z "${PROJECT_PU_U_CSV:-}" || ! -f "${PROJECT_PU_U_CSV:-}" ]]; then
  echo "Missing PROJECT_PU_U_CSV=/path/to/U.csv" >&2
  exit 2
fi

ARGS=(
  python -u "$EVOLVER_ROOT/scripts/run_evolution.py"
  --workspace "$EVOLVER_WORKSPACE"
  --iterations "$ITERATIONS"
  --evaluate-script "$EVALUATE_SCRIPT_PATH"
)
(cd "$EVOLVER_ROOT" && "${ARGS[@]}")

