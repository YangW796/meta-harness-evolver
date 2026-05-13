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
PROJECT_PU_U_LABELED_CSV="${PROJECT_PU_U_LABELED_CSV:-}"
PROJECT_PU_U_LABEL_COL="${PROJECT_PU_U_LABEL_COL:-u_label}"
PROJECT_PU_TEST_RATIO="${PROJECT_PU_TEST_RATIO:-0.2}"
PROJECT_PU_TEST_N="${PROJECT_PU_TEST_N:-0}"
PROJECT_PU_METRIC_MODE="${PROJECT_PU_METRIC_MODE:-u_maxf1}"
PROJECT_PU_TOPK_K="${PROJECT_PU_TOPK_K:-0}"
PROJECT_PU_THRESHOLD="${PROJECT_PU_THRESHOLD:-}"
PROJECT_PU_U_BOTTOM_N="${PROJECT_PU_U_BOTTOM_N:-0}"
PROJECT_PU_U_BOTTOM_RATIO="${PROJECT_PU_U_BOTTOM_RATIO:-0.05}"
PROJECT_PU_ITERATIONS="${PROJECT_PU_ITERATIONS:-1}"
PROJECT_PU_REMOVE_N_PER_ITER="${PROJECT_PU_REMOVE_N_PER_ITER:-0}"
PROJECT_PU_REMOVE_RATIO_PER_ITER="${PROJECT_PU_REMOVE_RATIO_PER_ITER:-0.05}"
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
if [[ -z "$PROJECT_PU_U_LABELED_CSV" || ! -f "$PROJECT_PU_U_LABELED_CSV" ]]; then
  echo "U labeled CSV not found. Set PROJECT_PU_U_LABELED_CSV=/path/to/U_labeled.csv" >&2
  exit 2
fi

MODEL_PATH="$HARNESS_DIR/model.py"
if [[ ! -f "$MODEL_PATH" ]]; then
  MODEL_PATH=""
fi

"$PYTHON_BIN" "$PROJECT_MAIN" \
  --p_csv "$PROJECT_PU_P_CSV" \
  --u_csv "$PROJECT_PU_U_CSV" \
  --u_labeled_csv "$PROJECT_PU_U_LABELED_CSV" \
  --u_label_col "$PROJECT_PU_U_LABEL_COL" \
  --candidate_dir "$CANDIDATE_DIR" \
  --model_path "$MODEL_PATH" \
  --test_ratio "$PROJECT_PU_TEST_RATIO" \
  --test_n "$PROJECT_PU_TEST_N" \
  --metric_mode "$PROJECT_PU_METRIC_MODE" \
  --topk_k "$PROJECT_PU_TOPK_K" \
  --threshold "$PROJECT_PU_THRESHOLD" \
  --u_bottom_n "$PROJECT_PU_U_BOTTOM_N" \
  --u_bottom_ratio "$PROJECT_PU_U_BOTTOM_RATIO" \
  --iterations "$PROJECT_PU_ITERATIONS" \
  --remove_n_per_iter "$PROJECT_PU_REMOVE_N_PER_ITER" \
  --remove_ratio_per_iter "$PROJECT_PU_REMOVE_RATIO_PER_ITER" \
  --seed "$PROJECT_PU_SEED"
