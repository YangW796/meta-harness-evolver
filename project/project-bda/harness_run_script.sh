#!/usr/bin/env bash
set -euo pipefail

# Usage: bash harness_run_script.sh <candidate_dir>
CANDIDATE_DIR="${1:-${CANDIDATE_DIR:-}}"
if [[ -z "$CANDIDATE_DIR" ]]; then
  echo "Usage: bash harness_run_script.sh <candidate_dir>" >&2
  exit 2
fi

CANDIDATE_DIR="$(cd "$CANDIDATE_DIR" && pwd)"
HARNESS_DIR="$CANDIDATE_DIR/harness"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_MAIN="$PROJECT_DIR/main_fix_train_test_input_output.py"

if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR" >&2
  exit 2
fi
if [[ ! -f "$PROJECT_MAIN" ]]; then
  echo "Missing main file: $PROJECT_MAIN" >&2
  exit 2
fi

# 数据/运行时配置（需要时可通过环境变量覆盖）。
# 迁移到其它机器时需要检查：
# - PYTHON_BIN 是否指向目标机器上的正确 Python/conda 环境。
# - BDA_DATASETS_DIR 必须指向本地 BDA 数据集目录。
# - BDA_STATE_PATH 是可选项；如果运行需要跨机器恢复，需要设置为
#   可写且可恢复的状态文件路径。
PYTHON_BIN="${PYTHON_BIN:-python}"
MODEL_IMPL_PATH="$HARNESS_DIR/model.py"
if [[ ! -f "$MODEL_IMPL_PATH" ]]; then
  echo "Model file not found: $MODEL_IMPL_PATH" >&2
  exit 2
fi

BDA_DATA_NAME="${BDA_DATA_NAME:-IFNG}"
BDA_TASK="${BDA_TASK:-perturb-genes-brief}"
BDA_STEPS="${BDA_STEPS:-5}"
BDA_NUM_GENES="${BDA_NUM_GENES:-128}"
BDA_SEED="${BDA_SEED:-42}"
BDA_RESUME_STATE="${BDA_RESUME_STATE:-1}"
BDA_INCLUDE_HIT_IN_HISTORY="${BDA_INCLUDE_HIT_IN_HISTORY:-1}"

BDA_WORKSPACE_DIR="${EVOLVER_WORKSPACE:-}"
if [[ -z "$BDA_WORKSPACE_DIR" ]]; then
  BDA_WORKSPACE_DIR="$(cd "$CANDIDATE_DIR/../.." && pwd)"
fi
if [[ -z "${BDA_STATE_PATH:-}" ]]; then
  export BDA_STATE_PATH="$BDA_WORKSPACE_DIR/bda_state.json"
fi

if [[ -z "${BDA_DATASETS_DIR:-}" ]]; then
  echo "BDA_DATASETS_DIR is required; set it to the BioDiscoveryAgent datasets directory." >&2
  exit 2
fi
if [[ ! -d "$BDA_DATASETS_DIR" ]]; then
  echo "BDA_DATASETS_DIR does not exist or is not a directory: $BDA_DATASETS_DIR" >&2
  exit 2
fi

ARGS=(
  "$PYTHON_BIN" "$PROJECT_MAIN"
  --mode bda_active_search
  --data_name "$BDA_DATA_NAME"
  --task "$BDA_TASK"
  --steps "$BDA_STEPS"
  --batch_size "$BDA_NUM_GENES"
  --seed "$BDA_SEED"
  --model_dir "$MODEL_IMPL_PATH"
  --resume_state "$BDA_RESUME_STATE"
  --include_hit_in_history "$BDA_INCLUDE_HIT_IN_HISTORY"
  --datasets_dir "$BDA_DATASETS_DIR"
)
if [[ -n "${BDA_STATE_PATH:-}" ]]; then
  ARGS+=(--state_path "$BDA_STATE_PATH")
fi

"${ARGS[@]}"
