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
if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR"
  exit 2
fi
if [[ ! -f "$PROJECT_MAIN" ]]; then
  echo "Missing main file: $PROJECT_MAIN"
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT4_TASK="${PROJECT4_TASK:-IL2}"
PROJECT4_DATASETS_DIR="${PROJECT4_DATASETS_DIR:-}"
if [[ -z "$PROJECT4_DATASETS_DIR" ]]; then
  PROJECT4_DATASETS_DIR="$(cd "$PROJECT_DIR/../../.." && pwd)/BioDiscoveryAgent/datasets"
fi

PROJECT4_DATA_CSV="${PROJECT4_DATA_CSV:-}"
if [[ -z "$PROJECT4_DATA_CSV" && -n "$PROJECT4_TASK" ]]; then
  PROJECT4_DATA_CSV="$PROJECT4_DATASETS_DIR/ground_truth_${PROJECT4_TASK}.csv"
fi
PROJECT4_MODEL_IMPL_PATH="$HARNESS_DIR/model.py"
PROJECT4_POOL_SIZE="${PROJECT4_POOL_SIZE:-5000}"
PROJECT4_TOP_RATIO="${PROJECT4_TOP_RATIO:-0.2}"
PROJECT4_BATCH_SIZE="${PROJECT4_BATCH_SIZE:-100}"
PROJECT4_ROUNDS="${PROJECT4_ROUNDS:-1}"
PROJECT4_SEED="${PROJECT4_SEED:-42}"
PROJECT4_SEED_QUERIES="${PROJECT4_SEED_QUERIES:-0}"
PROJECT4_FIXED_POOL="${PROJECT4_FIXED_POOL:-0}"
PROJECT4_GROUND_TRUTH_CSV="${PROJECT4_GROUND_TRUTH_CSV:-}"
PROJECT4_RESUME_STATE="${PROJECT4_RESUME_STATE:-1}"
PROJECT4_STATE_PATH="${PROJECT4_STATE_PATH:-}"

if [[ -z "$PROJECT4_DATA_CSV" || ! -f "$PROJECT4_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT4_DATA_CSV"
  echo "Set PROJECT4_DATA_CSV to your dataset CSV path."
  exit 2
fi

if [[ ! -f "$PROJECT4_MODEL_IMPL_PATH" ]]; then
  echo "Model file not found: $PROJECT4_MODEL_IMPL_PATH"
  exit 2
fi

if [[ -n "$PROJECT4_GROUND_TRUTH_CSV" && ! -f "$PROJECT4_GROUND_TRUTH_CSV" ]]; then
  echo "Ground truth CSV not found: $PROJECT4_GROUND_TRUTH_CSV"
  exit 2
fi

ARGS=(
  "$PYTHON_BIN" "$PROJECT_MAIN"
  --mode active_search
  --csv "$PROJECT4_DATA_CSV"
  --model_dir "$PROJECT4_MODEL_IMPL_PATH"
  --pool_size "$PROJECT4_POOL_SIZE"
  --top_ratio "$PROJECT4_TOP_RATIO"
  --batch_size "$PROJECT4_BATCH_SIZE"
  --rounds "$PROJECT4_ROUNDS"
  --seed "$PROJECT4_SEED"
  --seed_queries "$PROJECT4_SEED_QUERIES"
  --task "$PROJECT4_TASK"
)
if [[ "$PROJECT4_FIXED_POOL" == "1" ]]; then
  ARGS+=(--fixed_pool)
fi
if [[ -n "$PROJECT4_GROUND_TRUTH_CSV" ]]; then
  ARGS+=(--ground_truth_csv "$PROJECT4_GROUND_TRUTH_CSV")
fi
if [[ -n "$PROJECT4_STATE_PATH" ]]; then
  ARGS+=(--state_path "$PROJECT4_STATE_PATH")
fi
ARGS+=(--resume_state "$PROJECT4_RESUME_STATE")
"${ARGS[@]}"
