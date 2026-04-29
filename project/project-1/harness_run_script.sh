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

# 数据/运行时配置（需要时可通过环境变量覆盖）。
# 迁移到其它机器时需要检查：
# - PYTHON_BIN 是否指向目标机器上的正确 Python/conda 环境。
# - PROJECT1_DATA_ROOT 和 PROJECT1_DATA_CSV 默认是当前集群路径；
#   迁移后需要显式设置为新机器上的数据路径。
# - PROJECT1_MODEL_PATH 默认写到 candidate 的 harness 目录下；
#   除非需要使用共享 checkpoint 路径，一般不用修改。
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
PROJECT1_DATA_ROOT="/inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli"
PROJECT1_DATA_CSV="${PROJECT1_DATA_CSV:-$PROJECT1_DATA_ROOT/merged_results.csv}"
PROJECT1_MODEL_PATH="${PROJECT1_MODEL_PATH:-$HARNESS_DIR/iptm_model.pt}"
HARNESS_DEVICE="${HARNESS_DEVICE:-cpu}"
HARNESS_BATCH_SIZE="${HARNESS_BATCH_SIZE:-16}"

if [[ ! -f "$PROJECT1_DATA_CSV" ]]; then
  echo "CSV not found: $PROJECT1_DATA_CSV"
  echo "Set PROJECT1_DATA_CSV to your dataset path."
  exit 2
fi

"$PYTHON_BIN" "$HARNESS_DIR/main.py" \
  --mode train \
  --csv "$PROJECT1_DATA_CSV" \
  --root_dir "$PROJECT1_DATA_ROOT" \
  --model_path "$PROJECT1_MODEL_PATH" \
  --device "$HARNESS_DEVICE" \
  --batch_size "$HARNESS_BATCH_SIZE"
