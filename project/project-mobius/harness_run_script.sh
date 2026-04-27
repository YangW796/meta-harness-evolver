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
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${EVOLVER_WORKSPACE:-}"
if [[ -z "$WORKSPACE_DIR" ]]; then
  WORKSPACE_DIR="$(cd "$CANDIDATE_DIR/../.." && pwd)"
fi
if [[ ! -d "$HARNESS_DIR" ]]; then
  echo "Missing harness dir: $HARNESS_DIR"
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
REPO_ROOT="$(cd "$PROJECT_DIR/../../.." && pwd)"

MOBIUS_HOME="${MOBIUS_HOME:-$REPO_ROOT/mobius}"
if [[ ! -d "$MOBIUS_HOME" ]]; then
  echo "Mobius dir not found: $MOBIUS_HOME" >&2
  echo "Set MOBIUS_HOME=/path/to/mobius" >&2
  exit 2
fi
if [[ ! -f "$MOBIUS_HOME/scripts/run_mobius_lightning.py" ]]; then
  echo "Missing mobius entrypoint: $MOBIUS_HOME/scripts/run_mobius_lightning.py" >&2
  exit 2
fi
if [[ ! -d "$MOBIUS_HOME/reranking/model" ]]; then
  echo "Missing mobius model dir: $MOBIUS_HOME/reranking/model" >&2
  exit 2
fi

HARNESS_MODEL_DIR="$HARNESS_DIR/model"
if [[ ! -d "$HARNESS_MODEL_DIR" ]]; then
  echo "Missing harness model dir: $HARNESS_MODEL_DIR" >&2
  exit 2
fi

RUN_OUTPUT_DIR="${MOBIUS_OUTPUT_DIR:-$HARNESS_DIR/outputs/mobius_run}"
mkdir -p "$RUN_OUTPUT_DIR"
DERIVED_CONFIG_PATH="$RUN_OUTPUT_DIR/config.yaml"
BASE_CONFIG_PATH="${MOBIUS_CONFIG:-$MOBIUS_HOME/configs/reranker_demo.yaml}"
if [[ ! -f "$BASE_CONFIG_PATH" ]]; then
  echo "Missing mobius config: $BASE_CONFIG_PATH" >&2
  exit 2
fi

MOBIUS_DEVICES="${MOBIUS_DEVICES:-}"
MOBIUS_ACCELERATOR="${MOBIUS_ACCELERATOR:-}"
MOBIUS_STRATEGY="${MOBIUS_STRATEGY:-}"
MOBIUS_MAX_ROWS="${MOBIUS_MAX_ROWS:-}"
MOBIUS_RESUME_FROM="${MOBIUS_RESUME_FROM:-}"

MOBIUS_DATA_ROOT="${MOBIUS_DATA_ROOT:-}"
MOBIUS_ORACLE_CSV="${MOBIUS_ORACLE_CSV:-}"
MOBIUS_NORMALIZATION_JSON="${MOBIUS_NORMALIZATION_JSON:-}"
MOBIUS_TARGET="${MOBIUS_TARGET:-}"
MOBIUS_METHOD="${MOBIUS_METHOD:-}"
MOBIUS_BATCH_SIZE="${MOBIUS_BATCH_SIZE:-}"
MOBIUS_NUM_WORKERS="${MOBIUS_NUM_WORKERS:-}"
MOBIUS_SEED="${MOBIUS_SEED:-}"

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

MODEL_DIR="$MOBIUS_HOME/reranking/model"
BACKUP_DIR="$RUN_OUTPUT_DIR/mobius_model_backup"
RESTORED="0"
cleanup() {
  if [[ "$RESTORED" == "1" ]]; then
    return
  fi
  if [[ -d "$BACKUP_DIR" ]]; then
    rm -rf "$MODEL_DIR"
    cp -a "$BACKUP_DIR" "$MODEL_DIR"
  fi
  RESTORED="1"
}
trap cleanup EXIT

rm -rf "$BACKUP_DIR"
cp -a "$MODEL_DIR" "$BACKUP_DIR"
rm -rf "$MODEL_DIR"
cp -a "$HARNESS_MODEL_DIR" "$MODEL_DIR"

ARGS=("$PYTHON_BIN" "$MOBIUS_HOME/scripts/run_mobius_lightning.py" --config "$DERIVED_CONFIG_PATH")
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

cd "$MOBIUS_HOME"
"${ARGS[@]}"

METRICS_CSV="$RUN_OUTPUT_DIR/csv_logs/version_0/metrics.csv"
METRICS_JSON="$HARNESS_DIR/outputs/metrics.json"
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
