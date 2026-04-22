#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PROJECT_DIR/../../.." && pwd)"

DATASETS_DIR="${PROJECT4_DATASETS_DIR:-$REPO_ROOT/BioDiscoveryAgent/datasets}"
if [[ ! -d "$DATASETS_DIR" ]]; then
  echo "Datasets dir not found: $DATASETS_DIR" >&2
  exit 2
fi

ITERATIONS="${ITERATIONS:-20}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PROJECT_DIR}"
RUN_TAG="${RUN_TAG:-evo}"

mapfile -t TASKS < <(find "$DATASETS_DIR" -maxdepth 1 -type f -name "ground_truth_*.csv" -printf "%f\n" | sed -E 's/^ground_truth_(.*)\.csv$/\1/' | sort)
if [[ "${#TASKS[@]}" -eq 0 ]]; then
  echo "No tasks found in: $DATASETS_DIR (expected ground_truth_*.csv)" >&2
  exit 2
fi

echo -e "task\tworkspace\tdataset_csv"
for task in "${TASKS[@]}"; do
  dataset_csv="$DATASETS_DIR/ground_truth_${task}.csv"
  workspace="$WORKSPACE_ROOT/hoss-evolution_${RUN_TAG}_${task}"
  echo -e "${task}\t${workspace}\t${dataset_csv}"

  PROJECT4_TASK="$task" \
  PROJECT4_DATA_CSV="$dataset_csv" \
  PROJECT4_DATASETS_DIR="$DATASETS_DIR" \
  ITERATIONS="$ITERATIONS" \
  EVOLVER_WORKSPACE="$workspace" \
  bash "$PROJECT_DIR/run_evolution.sh"
done
