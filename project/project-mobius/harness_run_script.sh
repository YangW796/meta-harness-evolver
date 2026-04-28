#!/usr/bin/env bash
set -euo pipefail

# 用法: bash harness_run_script.sh <candidate_dir>
# 外循环会以如下形式调用本脚本: bash <this_script> <candidate_dir>
# 本脚本需要完成:
# 1) 针对给定 candidate 的 harness 运行 Mobius 训练/测试
# 2) 写出 candidate_dir/harness/outputs/metrics.json 供 evaluate 脚本读取
CANDIDATE_DIR="${1:-${CANDIDATE_DIR:-}}"
if [[ -z "$CANDIDATE_DIR" ]]; then
  echo "Usage: bash harness_run_script.sh <candidate_dir>"
  exit 2
fi

# 规范化路径，并定位 candidate 的 harness 目录。
CANDIDATE_DIR="$(cd "$CANDIDATE_DIR" && pwd)"
HARNESS_DIR="$CANDIDATE_DIR/harness"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 解析 evolver workspace（主要用于与其它项目保持一致/便于调试）。
WORKSPACE_DIR="${EVOLVER_WORKSPACE:-}"
if [[ -z "$WORKSPACE_DIR" ]]; then
  WORKSPACE_DIR="$(cd "$CANDIDATE_DIR/../.." && pwd)"
fi

# 校验 candidate 的 harness 目录必须存在。
if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR"
  exit 2
fi

# 选择 Python 解释器，并推导仓库根目录。
PYTHON_BIN="${PYTHON_BIN:-python}"
REPO_ROOT="$(cd "$PROJECT_DIR/../../.." && pwd)"

# 定位 Mobius 代码目录（允许通过环境变量指向外部 Mobius checkout）。
MOBIUS_HOME="${MOBIUS_HOME:-$REPO_ROOT/mobius}"
if [[ ! -d "$MOBIUS_HOME" ]]; then
  echo "Mobius dir not found: $MOBIUS_HOME" >&2
  echo "Set MOBIUS_HOME=/path/to/mobius" >&2
  exit 2
fi

# 校验 Mobius 入口脚本与模型包目录是否存在。
if [[ ! -f "$MOBIUS_HOME/scripts/run_mobius_lightning.py" ]]; then
  echo "Missing mobius entrypoint: $MOBIUS_HOME/scripts/run_mobius_lightning.py" >&2
  exit 2
fi
if [[ ! -d "$MOBIUS_HOME/reranking/model" ]]; then
  echo "Missing mobius model dir: $MOBIUS_HOME/reranking/model" >&2
  exit 2
fi

# candidate 可控的模型实现（外循环允许改动的范围）。
HARNESS_MODEL_DIR="$HARNESS_DIR/model"
if [[ ! -d "$HARNESS_MODEL_DIR" ]]; then
  echo "Missing harness model dir: $HARNESS_MODEL_DIR" >&2
  exit 2
fi

# 决定本次 candidate 的 Mobius 运行产物输出到哪里。
RUN_OUTPUT_DIR="${MOBIUS_OUTPUT_DIR:-$CANDIDATE_DIR/outputs/mobius_run}"
mkdir -p "$RUN_OUTPUT_DIR"

# 生成派生 YAML 配置，确保每个 candidate 的运行输出落到各自的 output_dir。
DERIVED_CONFIG_PATH="$RUN_OUTPUT_DIR/config.yaml"
BASE_CONFIG_PATH="${MOBIUS_CONFIG:-$MOBIUS_HOME/configs/reranker_demo.yaml}"
if [[ ! -f "$BASE_CONFIG_PATH" ]]; then
  echo "Missing mobius config: $BASE_CONFIG_PATH" >&2
  exit 2
fi

# 透传给 mobius/scripts/run_mobius_lightning.py 的命令行参数覆盖（可选）。
MOBIUS_DEVICES="${MOBIUS_DEVICES:-}"
MOBIUS_ACCELERATOR="${MOBIUS_ACCELERATOR:-}"
MOBIUS_STRATEGY="${MOBIUS_STRATEGY:-}"
MOBIUS_MAX_ROWS="${MOBIUS_MAX_ROWS:-}"
MOBIUS_RESUME_FROM="${MOBIUS_RESUME_FROM:-}"

# 可选：通过环境变量覆盖 YAML 中 `data.*` 字段。
MOBIUS_DATA_ROOT="${MOBIUS_DATA_ROOT:-}"
MOBIUS_ORACLE_CSV="${MOBIUS_ORACLE_CSV:-}"
MOBIUS_NORMALIZATION_JSON="${MOBIUS_NORMALIZATION_JSON:-}"
MOBIUS_TARGET="${MOBIUS_TARGET:-}"
MOBIUS_METHOD="${MOBIUS_METHOD:-}"
MOBIUS_BATCH_SIZE="${MOBIUS_BATCH_SIZE:-}"
MOBIUS_NUM_WORKERS="${MOBIUS_NUM_WORKERS:-}"
MOBIUS_SEED="${MOBIUS_SEED:-}"

# 生成派生 config.yaml：
# - trainer.output_dir -> RUN_OUTPUT_DIR（确保输出写到 harness/outputs 下）
# - 禁用 swanlab（避免额外外部依赖）
# - 若提供了环境变量，则覆盖 data.* 配置项
BASE_CONFIG_PATH="$BASE_CONFIG_PATH" \
DERIVED_CONFIG_PATH="$DERIVED_CONFIG_PATH" \
RUN_OUTPUT_DIR="$RUN_OUTPUT_DIR" \
MOBIUS_DATA_ROOT="$MOBIUS_DATA_ROOT" \
MOBIUS_ORACLE_CSV="$MOBIUS_ORACLE_CSV" \
MOBIUS_NORMALIZATION_JSON="$MOBIUS_NORMALIZATION_JSON" \
MOBIUS_TARGET="$MOBIUS_TARGET" \
MOBIUS_METHOD="$MOBIUS_METHOD" \
MOBIUS_BATCH_SIZE="$MOBIUS_BATCH_SIZE" \
MOBIUS_NUM_WORKERS="$MOBIUS_NUM_WORKERS" \
MOBIUS_SEED="$MOBIUS_SEED" \
"$PYTHON_BIN" - <<'PY'
import os
from pathlib import Path

import yaml

base_path = Path(os.environ["BASE_CONFIG_PATH"]).expanduser().resolve()
out_path = Path(os.environ["DERIVED_CONFIG_PATH"]).expanduser().resolve()
output_dir = os.environ["RUN_OUTPUT_DIR"]

cfg = yaml.safe_load(base_path.read_text())
cfg = cfg or {}

trainer = cfg.get("trainer") or {}
trainer["output_dir"] = output_dir
cfg["trainer"] = trainer

logging_cfg = cfg.get("logging") or {}
swanlab_cfg = (logging_cfg.get("swanlab") or {})
swanlab_cfg["enabled"] = False
logging_cfg["swanlab"] = swanlab_cfg
cfg["logging"] = logging_cfg

data_cfg = cfg.get("data") or {}
for key, env_name in [
    ("data_root", "MOBIUS_DATA_ROOT"),
    ("oracle_csv", "MOBIUS_ORACLE_CSV"),
    ("normalization_json", "MOBIUS_NORMALIZATION_JSON"),
    ("target", "MOBIUS_TARGET"),
    ("method", "MOBIUS_METHOD"),
    ("batch_size", "MOBIUS_BATCH_SIZE"),
    ("num_workers", "MOBIUS_NUM_WORKERS"),
    ("seed", "MOBIUS_SEED"),
]:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        continue
    if key in {"batch_size", "num_workers", "seed"}:
        data_cfg[key] = int(raw)
    else:
        data_cfg[key] = raw
cfg["data"] = data_cfg

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(yaml.safe_dump(cfg, sort_keys=False))
PY

# 组装 Mobius 训练/测试命令。
ARGS=(
  "$PYTHON_BIN" "$MOBIUS_HOME/scripts/run_mobius_lightning.py"
  --config "$DERIVED_CONFIG_PATH"
  --model-override-dir "$HARNESS_MODEL_DIR"
)
if [[ -n "$MOBIUS_DEVICES" ]]; then
  ARGS+=(--devices "$MOBIUS_DEVICES")
fi
if [[ -n "$MOBIUS_ACCELERATOR" ]]; then
  ARGS+=(--accelerator "$MOBIUS_ACCELERATOR")
fi
if [[ -n "$MOBIUS_STRATEGY" ]]; then
  ARGS+=(--strategy "$MOBIUS_STRATEGY")
fi
if [[ -n "$MOBIUS_MAX_ROWS" ]]; then
  ARGS+=(--max-rows "$MOBIUS_MAX_ROWS")
fi
if [[ -n "$MOBIUS_RESUME_FROM" ]]; then
  ARGS+=(--resume-from "$MOBIUS_RESUME_FROM")
fi

# 在 Mobius 工程根目录下运行，确保 Mobius 内部相对路径解析正确。
cd "$MOBIUS_HOME"
"${ARGS[@]}"

# 将 Mobius Lightning 的日志转成 evolver 统一的 metrics.json 输出。
# 从 CSVLogger 的 metrics.csv 中取最后一条可用的 test 指标行，并写到：
# - harness/outputs/metrics.json
METRICS_CSV="$RUN_OUTPUT_DIR/csv_logs/version_0/metrics.csv"
METRICS_JSON="$CANDIDATE_DIR/outputs/metrics.json"
METRICS_CSV="$METRICS_CSV" METRICS_JSON="$METRICS_JSON" "$PYTHON_BIN" - <<'PY'
import csv
import json
import os
from pathlib import Path

csv_path = Path(os.environ["METRICS_CSV"]).expanduser().resolve()
out_path = Path(os.environ["METRICS_JSON"]).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

payload = {
    "metrics": {},
}

if not csv_path.exists():
    payload["error"] = f"missing_metrics_csv: {csv_path}"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    raise SystemExit(0)

rows = list(csv.DictReader(csv_path.open(newline="")))
chosen = None
for row in reversed(rows):
    if any((k.startswith("test/") and (row.get(k) not in (None, "", "nan"))) for k in row.keys()):
        chosen = row
        break
if chosen is None and rows:
    chosen = rows[-1]

def set_nested(d: dict, parts: list[str], value):
    cur = d
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value

flat = {}
for k, v in (chosen or {}).items():
    if v is None or v == "":
        continue
    try:
        fv = float(v)
    except Exception:
        continue
    flat[k] = fv
    set_nested(payload["metrics"], k.split("/"), fv)

primary = None
for key in ("test/rerank/ndcg@100", "test/rerank/score_spearman"):
    if key in flat:
        primary = {"name": key, "value": flat[key]}
        break
if primary is not None:
    payload["primary_metric"] = primary

out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
PY
