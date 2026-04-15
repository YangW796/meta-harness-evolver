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
if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR"
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT2_DATA_ROOT="${PROJECT2_DATA_ROOT:-/inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli}"
PROJECT2_DATA_CSV="${PROJECT2_DATA_CSV:-$PROJECT2_DATA_ROOT/merged_results.csv}"
PROJECT2_MODEL_PATH="${PROJECT2_MODEL_PATH:-$HARNESS_DIR/iptm_model.pt}"
PROJECT2_TOP_RATIO="${PROJECT2_TOP_RATIO:-0.1}"
HARNESS_DEVICE="${HARNESS_DEVICE:-cpu}"
HARNESS_BATCH_SIZE="${HARNESS_BATCH_SIZE:-16}"

if [[ -z "$PROJECT2_DATA_CSV" || ! -f "$PROJECT2_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT2_DATA_CSV"
  echo "Set PROJECT2_DATA_CSV to your dataset CSV path."
  exit 2
fi

if [[ -z "$PROJECT2_DATA_ROOT" || ! -d "$PROJECT2_DATA_ROOT" ]]; then
  echo "Root dir not found: $PROJECT2_DATA_ROOT"
  echo "Set PROJECT2_DATA_ROOT to your structure root directory."
  exit 2
fi

"$PYTHON_BIN" "$HARNESS_DIR/main.py" \
  --mode train \
  --csv "$PROJECT2_DATA_CSV" \
  --root_dir "$PROJECT2_DATA_ROOT" \
  --model_path "$PROJECT2_MODEL_PATH" \
  --top_ratio "$PROJECT2_TOP_RATIO" \
  --device "$HARNESS_DEVICE" \
  --batch_size "$HARNESS_BATCH_SIZE"
