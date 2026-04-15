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

# Data/runtime settings (override by env if needed)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT1_DATA_ROOT="/inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli"
PROJECT1_DATA_CSV="${PROJECT1_DATA_CSV:-$PROJECT1_DATA_ROOT/merged_results.csv}"
PROJECT1_MODEL_PATH="${PROJECT1_MODEL_PATH:-$HARNESS_DIR/iptm_model.pt}"

if [[ ! -f "$PROJECT1_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT1_DATA_CSV"
  echo "Set PROJECT1_DATA_CSV to your dataset path."
  exit 2
fi

"$PYTHON_BIN" "$HARNESS_DIR/main.py" \
  --mode train \
  --csv "$PROJECT1_DATA_CSV" \
  --root_dir "$PROJECT1_DATA_ROOT" \
  --model_path "$PROJECT1_MODEL_PATH"
