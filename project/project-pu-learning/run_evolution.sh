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

WORKSPACE_INDEX="${WORKSPACE_INDEX:-}"
DEFAULT_WORKSPACE_DIR="$PROJECT_DIR/hoss-evolution${WORKSPACE_INDEX:+-$WORKSPACE_INDEX}"
export EVOLVER_WORKSPACE="${EVOLVER_WORKSPACE:-$DEFAULT_WORKSPACE_DIR}"
PROJECT_PU_SEED_BEST_DIR="${PROJECT_PU_SEED_BEST_DIR:-$PROJECT_DIR/hoss-evolution/best}"
if [[ ! -d "$EVOLVER_WORKSPACE" ]]; then
  mkdir -p "$EVOLVER_WORKSPACE"
fi
if [[ -d "$PROJECT_PU_SEED_BEST_DIR" && ! -d "$EVOLVER_WORKSPACE/best/current" ]]; then
  mkdir -p "$EVOLVER_WORKSPACE/best"
  cp -a "$PROJECT_PU_SEED_BEST_DIR/." "$EVOLVER_WORKSPACE/best/"
fi
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="${HARNESS_RUN_TIMEOUT_SECONDS:-600}"
export FEISHU_POST_ENABLED=0

export PROJECT_PU_METRIC_MODE="${PROJECT_PU_METRIC_MODE:-u_maxf1}"
export PROPOSER_MAX_ITERATIONS="${PROPOSER_MAX_ITERATIONS:-30}"
export PROPOSER_TIMEOUT_SECONDS="${PROPOSER_TIMEOUT_SECONDS:-600}"
export PROPOSER_LLM_TIMEOUT_SECONDS="${PROPOSER_LLM_TIMEOUT_SECONDS:-}"
export NEXAU_ENABLE_RUN_SHELL_COMMAND="${NEXAU_ENABLE_RUN_SHELL_COMMAND:-0}"
export NEXAU_DENY_READ_PY_GLOBS="${NEXAU_DENY_READ_PY_GLOBS:-*/project/project-pu-learning/generate_u_labels.py}"

export EVOLVER_INJECT_PROMPT_CONTEXT="${EVOLVER_INJECT_PROMPT_CONTEXT:-1}"
export EVOLVER_PROMPT_CONTEXT_FILE="${EVOLVER_PROMPT_CONTEXT_FILE:-$PROJECT_DIR/prompt_context.py}"
export EVOLVER_ATTEMPT_PLANNER_CONTEXT_FILE="${EVOLVER_ATTEMPT_PLANNER_CONTEXT_FILE:-$PROJECT_DIR/prompt_context.py}"

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
if [[ -z "${PROJECT_PU_U_LABELED_CSV:-}" || ! -f "${PROJECT_PU_U_LABELED_CSV:-}" ]]; then
  echo "Missing PROJECT_PU_U_LABELED_CSV=/path/to/U_labeled.csv" >&2
  exit 2
fi

ARGS=(
  python -u "$EVOLVER_ROOT/scripts/run_evolution.py"
  --workspace "$EVOLVER_WORKSPACE"
  --iterations "$ITERATIONS"
  --evaluate-script "$EVALUATE_SCRIPT_PATH"
)
(cd "$EVOLVER_ROOT" && "${ARGS[@]}")
