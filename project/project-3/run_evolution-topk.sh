#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ratios=("0.1" "0.2" "0.3")
labels=("10" "20" "30")

for i in "${!ratios[@]}"; do
  ratio="${ratios[$i]}"
  label="${labels[$i]}"
  (
    export PROJECT3_TOP_RATIO="$ratio"
    export WORKSPACE_INDEX="topk${label}p"
    echo "[TOPK] PROJECT3_TOP_RATIO=$PROJECT3_TOP_RATIO WORKSPACE_INDEX=$WORKSPACE_INDEX"
    bash "$PROJECT_DIR/run_evolution.sh"
  )
done
