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
PROJECT3_DATA_ROOT="${PROJECT3_DATA_ROOT:-/inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli}"
PROJECT3_DATA_CSV="${PROJECT3_DATA_CSV:-$PROJECT3_DATA_ROOT/merged_results.csv}"
PROJECT3_MODEL_IMPL_PATH="$HARNESS_DIR/model.py"
PROJECT3_POOL_SIZE="${PROJECT3_POOL_SIZE:-5000}"
PROJECT3_TOP_RATIO="${PROJECT3_TOP_RATIO:-0.2}"
PROJECT3_BATCH_SIZE="${PROJECT3_BATCH_SIZE:-100}"
PROJECT3_ROUNDS="${PROJECT3_ROUNDS:-1}"
PROJECT3_SEED="${PROJECT3_SEED:-42}"
PROJECT3_SEED_QUERIES="${PROJECT3_SEED_QUERIES:-0}"
PROJECT3_FIXED_POOL="${PROJECT3_FIXED_POOL:-0}"
PROJECT3_GROUND_TRUTH_CSV="${PROJECT3_GROUND_TRUTH_CSV:-}"
PROJECT3_RESUME_STATE="${PROJECT3_RESUME_STATE:-1}"


if [[ -z "$PROJECT3_DATA_CSV" || ! -f "$PROJECT3_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT3_DATA_CSV"
  echo "Set PROJECT3_DATA_CSV to your dataset CSV path."
  exit 2
fi

if [[ ! -f "$PROJECT3_MODEL_IMPL_PATH" ]]; then
  echo "Model file not found: $PROJECT3_MODEL_IMPL_PATH"
  exit 2
fi

if [[ -n "$PROJECT3_GROUND_TRUTH_CSV" && ! -f "$PROJECT3_GROUND_TRUTH_CSV" ]]; then
  echo "Ground truth CSV not found: $PROJECT3_GROUND_TRUTH_CSV"
  exit 2
fi

ARGS=(
  "$PYTHON_BIN" "$PROJECT_MAIN"
  --mode active_search
  --csv "$PROJECT3_DATA_CSV"
  --model_dir "$PROJECT3_MODEL_IMPL_PATH"
  --pool_size "$PROJECT3_POOL_SIZE"
  --top_ratio "$PROJECT3_TOP_RATIO"
  --batch_size "$PROJECT3_BATCH_SIZE"
  --rounds "$PROJECT3_ROUNDS"
  --seed "$PROJECT3_SEED"
  --seed_queries "$PROJECT3_SEED_QUERIES"
)
if [[ "$PROJECT3_FIXED_POOL" == "1" ]]; then
  ARGS+=(--fixed_pool)
fi
if [[ -n "$PROJECT3_GROUND_TRUTH_CSV" ]]; then
  ARGS+=(--ground_truth_csv "$PROJECT3_GROUND_TRUTH_CSV")
fi
if [[ -n "$PROJECT3_STATE_PATH" ]]; then
  ARGS+=(--state_path "$PROJECT3_STATE_PATH")
fi
ARGS+=(--resume_state "$PROJECT3_RESUME_STATE")
"${ARGS[@]}"
