#!/usr/bin/env bash
set -euo pipefail

# Usage: bash harness_run_script.sh <candidate_dir>
CANDIDATE_DIR="${1:-${CANDIDATE_DIR:-}}"
if [[ -z "$CANDIDATE_DIR" ]]; then
  echo "Usage: bash harness_run_script.sh <candidate_dir>"
  exit 2
fi

CANDIDATE_DIR="$(cd "$CANDIDATE_DIR" && pwd)"
HARNESS_DIR="$CANDIDATE_DIR/harness"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_MAIN="$PROJECT_DIR/main_fix_train_test_input_output.py"
WORKSPACE_DIR="${EVOLVER_WORKSPACE:-}"
if [[ -z "$WORKSPACE_DIR" ]]; then
  WORKSPACE_DIR="$(cd "$CANDIDATE_DIR/../.." && pwd)"
fi
if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR"
  exit 2
fi
if [[ ! -f "$PROJECT_MAIN" ]]; then
  echo "Missing main file: $PROJECT_MAIN"
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT_PU_DATA_ROOT="${PROJECT_PU_DATA_ROOT:-}"
PROJECT_PU_DATA_CSV="${PROJECT_PU_DATA_CSV:-${PROJECT_PU_DATA_ROOT:+$PROJECT_PU_DATA_ROOT/merged_results.csv}}"
PROJECT_PU_POSITIVE_CSV="${PROJECT_PU_POSITIVE_CSV:-}"
PROJECT_PU_MODEL_IMPL_PATH="$HARNESS_DIR/model.py"
PROJECT_PU_POOL_SIZE="${PROJECT_PU_POOL_SIZE:-5000}"
PROJECT_PU_BATCH_SIZE="${PROJECT_PU_BATCH_SIZE:-100}"
PROJECT_PU_ROUNDS="${PROJECT_PU_ROUNDS:-1}"
PROJECT_PU_SEED="${PROJECT_PU_SEED:-42}"
PROJECT_PU_SEED_QUERIES="${PROJECT_PU_SEED_QUERIES:-0}"
PROJECT_PU_FIXED_POOL="${PROJECT_PU_FIXED_POOL:-0}"
PROJECT_PU_ID_COLUMN="${PROJECT_PU_ID_COLUMN:-}"
PROJECT_PU_MATCH_COLUMNS="${PROJECT_PU_MATCH_COLUMNS:-}"
PROJECT_PU_STATE_PATH="${PROJECT_PU_STATE_PATH:-}"
PROJECT_PU_RESUME_STATE="${PROJECT_PU_RESUME_STATE:-1}"

if [[ -z "$PROJECT_PU_DATA_CSV" || ! -f "$PROJECT_PU_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT_PU_DATA_CSV"
  echo "Set PROJECT_PU_DATA_CSV to your candidate/unlabeled CSV path."
  exit 2
fi

if [[ ! -f "$PROJECT_PU_MODEL_IMPL_PATH" ]]; then
  echo "Model file not found: $PROJECT_PU_MODEL_IMPL_PATH"
  exit 2
fi

if [[ -n "$PROJECT_PU_POSITIVE_CSV" && ! -f "$PROJECT_PU_POSITIVE_CSV" ]]; then
  echo "Positive CSV not found: $PROJECT_PU_POSITIVE_CSV"
  exit 2
fi

ARGS=(
  "$PYTHON_BIN" "$PROJECT_MAIN"
  --mode active_search
  --csv "$PROJECT_PU_DATA_CSV"
  --model_dir "$PROJECT_PU_MODEL_IMPL_PATH"
  --pool_size "$PROJECT_PU_POOL_SIZE"
  --batch_size "$PROJECT_PU_BATCH_SIZE"
  --rounds "$PROJECT_PU_ROUNDS"
  --seed "$PROJECT_PU_SEED"
  --seed_queries "$PROJECT_PU_SEED_QUERIES"
)
if [[ "$PROJECT_PU_FIXED_POOL" == "1" ]]; then
  ARGS+=(--fixed_pool)
fi
if [[ -n "$PROJECT_PU_ID_COLUMN" ]]; then
  ARGS+=(--id_column "$PROJECT_PU_ID_COLUMN")
fi
if [[ -n "$PROJECT_PU_MATCH_COLUMNS" ]]; then
  ARGS+=(--match_columns "$PROJECT_PU_MATCH_COLUMNS")
fi
if [[ -n "$PROJECT_PU_STATE_PATH" ]]; then
  ARGS+=(--state_path "$PROJECT_PU_STATE_PATH")
fi
ARGS+=(--resume_state "$PROJECT_PU_RESUME_STATE")
"${ARGS[@]}"
