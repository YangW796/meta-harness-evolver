#!/usr/bin/env bash
set -euo pipefail

EVOLVER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ENV_FILE="$EVOLVER_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

export BDA_DATASETS_DIR="${BDA_DATASETS_DIR:-}"

# 迁移到其他机器时通常需要调整：Conda 安装路径
source ~/miniconda3/etc/profile.d/conda.sh
CONDA_ENV="${CONDA_ENV:-meta-harness-evolver0}"

DATA_NAME="${DATA_NAME:-IFNG}"
ITERATIONS="${ITERATIONS:-20}"
RUNS="${RUNS:-1}"
if ! [[ "$RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "RUNS must be a positive integer: $RUNS" >&2
  exit 2
fi

# 迁移到其他机器时通常需要调整：工作区根目录（可通过 PROJECT_BDA_WORKSPACE_BASE_DIR 覆盖）
WORKSPACE_BASE_DIR="${PROJECT_BDA_WORKSPACE_BASE_DIR:-$PROJECT_DIR/hoss-evolution-workspaces}"
# 迁移到其他机器时通常需要调整：初始 best 种子目录（可通过 PROJECT_BDA_SEED_BEST_DIR 覆盖）
SEED_BEST_DIR="${PROJECT_BDA_SEED_BEST_DIR:-$PROJECT_DIR/hoss-evolution/best}"

EVALUATE_SCRIPT_PATH="$PROJECT_DIR/evaluate.py"
export HARNESS_RUN_SCRIPT="$PROJECT_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="${HARNESS_RUN_TIMEOUT_SECONDS:-3600}"
export FEISHU_POST_ENABLED=0

export PROPOSER_MAX_ITERATIONS="${PROPOSER_MAX_ITERATIONS:-40}"
export PROPOSER_TIMEOUT_SECONDS="${PROPOSER_TIMEOUT_SECONDS:-600}"
export PROPOSER_LLM_TIMEOUT_SECONDS="${PROPOSER_LLM_TIMEOUT_SECONDS:-}"
export NEXAU_ENABLE_RUN_SHELL_COMMAND="1"

export BDA_TASK="${BDA_TASK:-perturb-genes-brief}"
export BDA_STEPS="${BDA_STEPS:-5}"
export BDA_NUM_GENES="${BDA_NUM_GENES:-128}"
export BDA_RESUME_STATE="${BDA_RESUME_STATE:-1}"
export BDA_INCLUDE_HIT_IN_HISTORY="${BDA_INCLUDE_HIT_IN_HISTORY:-1}"
export BDA_GENE_SEARCH="${BDA_GENE_SEARCH:-0}"
export BDA_GENE_SEARCH_DIVERSE="${BDA_GENE_SEARCH_DIVERSE:-0}"
export BDA_GENE_SEARCH_K="${BDA_GENE_SEARCH_K:-10}"
# 迁移到其他机器时通常需要调整
export BDA_CSV_PATH="${BDA_CSV_PATH:-}"

PROPOSER_PROMPT_PREFIX_PATH="$PROJECT_DIR/proposer_prompt_prefix.txt"
if [[ ! -f "$PROPOSER_PROMPT_PREFIX_PATH" ]]; then
  echo "Missing proposer prompt prefix file: $PROPOSER_PROMPT_PREFIX_PATH" >&2
  exit 2
fi
export PROPOSER_PROMPT_PREFIX="$(cat "$PROPOSER_PROMPT_PREFIX_PATH")"$'\n'

CONDA_RUN_ARGS=(-n "$CONDA_ENV")
if conda run --help 2>/dev/null | grep -q -- "--no-capture-output"; then
  CONDA_RUN_ARGS=(--no-capture-output -n "$CONDA_ENV")
fi

_ensure_seed_best() {
  local workspace_dir="$1"
  if [[ ! -d "$workspace_dir" ]]; then
    mkdir -p "$workspace_dir"
  fi
  if [[ -d "$SEED_BEST_DIR" && ! -d "$workspace_dir/best/current" ]]; then
    mkdir -p "$workspace_dir/best"
    cp -a "$SEED_BEST_DIR/." "$workspace_dir/best/"
  fi
}

_run_one_dataset() {
  local data="$1"
  local run="$2"
  local workspace_dir="$WORKSPACE_BASE_DIR/$data/run-$run"
  _ensure_seed_best "$workspace_dir"

  export EVOLVER_WORKSPACE="$workspace_dir"
  export BDA_DATA_NAME="$data"

  ARGS=(python -u "$EVOLVER_ROOT/scripts/run_evolution.py" --workspace "$workspace_dir" --iterations "$ITERATIONS" --evaluate-script "$EVALUATE_SCRIPT_PATH")
  (cd "$EVOLVER_ROOT" && conda run "${CONDA_RUN_ARGS[@]}" "${ARGS[@]}")
}

if [[ "$DATA_NAME" == "all" ]]; then
  mapfile -t GT_LIST < <(ls -1 "$BDA_DATASETS_DIR"/ground_truth_*.csv 2>/dev/null | sed -E 's/.*ground_truth_([^/]+)\.csv/\1/' | sort -u)
  for ((run = 1; run <= RUNS; run++)); do
    for d in "${GT_LIST[@]}"; do
      if [[ -f "$BDA_DATASETS_DIR/task_prompts/$d.json" ]]; then
        _run_one_dataset "$d" "$run"
      fi
    done
  done
else
  for ((run = 1; run <= RUNS; run++)); do
    _run_one_dataset "$DATA_NAME" "$run"
  done
fi
