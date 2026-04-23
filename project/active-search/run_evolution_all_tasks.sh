#!/usr/bin/env bash
set -euo pipefail

ACTIVE_SEARCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVOLVER_ROOT="$(cd "$ACTIVE_SEARCH_DIR/../.." && pwd)"

DATASETS_DIR="${ACTIVE_SEARCH_DATASETS_DIR:-$EVOLVER_ROOT/BioDiscoveryAgent/datasets}"
if [[ ! -d "$DATASETS_DIR" ]]; then
  echo "Datasets dir not found: $DATASETS_DIR" >&2
  exit 2
fi

mapfile -t TASKS < <(find "$DATASETS_DIR" -maxdepth 1 -type f -name "ground_truth_*.csv" -printf "%f\n" | sed -E 's/^ground_truth_(.*)\.csv$/\1/' | sort)
if [[ "${#TASKS[@]}" -eq 0 ]]; then
  echo "No tasks found in: $DATASETS_DIR" >&2
  exit 2
fi

for task in "${TASKS[@]}"; do
  TASK="$task" ACTIVE_SEARCH_TASK="$task" ACTIVE_SEARCH_DATASETS_DIR="$DATASETS_DIR" bash "$ACTIVE_SEARCH_DIR/run_evolution.sh"
done
