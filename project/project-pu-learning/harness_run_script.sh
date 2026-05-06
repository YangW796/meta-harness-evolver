#!/usr/bin/env bash
set -euo pipefail

CANDIDATE_DIR="${1:-${CANDIDATE_DIR:-}}"
if [[ -z "$CANDIDATE_DIR" ]]; then
  echo "Usage: bash harness_run_script.sh <candidate_dir>" >&2
  exit 2
fi

CANDIDATE_DIR="$(cd "$CANDIDATE_DIR" && pwd)"
HARNESS_DIR="$CANDIDATE_DIR/harness"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_MAIN="$PROJECT_DIR/main_pu_filter.py"

PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT_PU_P_CSV="${PROJECT_PU_P_CSV:-}"
PROJECT_PU_U_CSV="${PROJECT_PU_U_CSV:-}"
PROJECT_PU_REMOVE_RATIO="${PROJECT_PU_REMOVE_RATIO:-0.2}"
PROJECT_PU_REMOVE_N="${PROJECT_PU_REMOVE_N:-0}"
PROJECT_PU_SEED="${PROJECT_PU_SEED:-42}"

if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR" >&2
  exit 2
fi
if [[ ! -f "$PROJECT_MAIN" ]]; then
  echo "Missing main file: $PROJECT_MAIN" >&2
  exit 2
fi
if [[ -z "$PROJECT_PU_P_CSV" || ! -f "$PROJECT_PU_P_CSV" ]]; then
  echo "P CSV not found. Set PROJECT_PU_P_CSV=/path/to/P.csv" >&2
  exit 2
fi
if [[ -z "$PROJECT_PU_U_CSV" || ! -f "$PROJECT_PU_U_CSV" ]]; then
  echo "U CSV not found. Set PROJECT_PU_U_CSV=/path/to/U.csv" >&2
  exit 2
fi

MODEL_PATH="$HARNESS_DIR/model.py"
if [[ ! -f "$MODEL_PATH" ]]; then
  MODEL_PATH=""
fi

"$PYTHON_BIN" "$PROJECT_MAIN" \
  --p_csv "$PROJECT_PU_P_CSV" \
  --u_csv "$PROJECT_PU_U_CSV" \
  --candidate_dir "$CANDIDATE_DIR" \
  --model_path "$MODEL_PATH" \
  --remove_ratio "$PROJECT_PU_REMOVE_RATIO" \
  --remove_n "$PROJECT_PU_REMOVE_N" \
  --seed "$PROJECT_PU_SEED"

