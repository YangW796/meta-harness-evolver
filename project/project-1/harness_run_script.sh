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


DATA_ROOT="${PROJECT1_DATA_ROOT:-$PROJECT_DIR}"
DATA_CSV="${PROJECT1_DATA_CSV:-}"
PYTHON_BIN="${PYTHON_BIN:-python}"

mkdir -p "$HARNESS_DIR/outputs"

ARGS=("$HARNESS_DIR/main.py" "--data-root" "$DATA_ROOT" "--output-dir" "$HARNESS_DIR/outputs")
if [[ -n "$DATA_CSV" ]]; then
  ARGS+=("--data-csv" "$DATA_CSV")
fi

"$PYTHON_BIN" "${ARGS[@]}"
