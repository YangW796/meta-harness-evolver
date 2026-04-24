#!/usr/bin/env bash
set -euo pipefail

ACTIVE_SEARCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVOLVER_ROOT="$(cd "$ACTIVE_SEARCH_DIR/../.." && pwd)"

ENV_FILE="$EVOLVER_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

TASK="${TASK:-${ACTIVE_SEARCH_TASK:-}}"
if [[ -z "$TASK" ]]; then
  echo "Missing task (set TASK or ACTIVE_SEARCH_TASK)" >&2
  exit 2
fi

CONDA_ENV="${CONDA_ENV:-meta-harness-evolver0}"
ITERATIONS="${ITERATIONS:-20}"
RUN_TAG="${RUN_TAG:-evo}"
FORCE_RERUN="${FORCE_RERUN:-0}"
LLM_MODEL_NAME="${LLM_MODEL:-}"

WORKSPACE_ROOT="${WORKSPACE_ROOT:-$ACTIVE_SEARCH_DIR}"
WORKSPACE="${EVOLVER_WORKSPACE:-$WORKSPACE_ROOT/hoss-evolution_${RUN_TAG}_${TASK}}"
export EVOLVER_WORKSPACE="$WORKSPACE"

DATASETS_DIR="${ACTIVE_SEARCH_DATASETS_DIR:-$EVOLVER_ROOT/BioDiscoveryAgent/datasets}"
DATA_CSV="${ACTIVE_SEARCH_DATA_CSV:-}"
if [[ -z "$DATA_CSV" ]]; then
  DATA_CSV="$DATASETS_DIR/ground_truth_${TASK}.csv"
fi
if [[ ! -f "$DATA_CSV" ]]; then
  echo "Dataset CSV not found: $DATA_CSV" >&2
  exit 2
fi

BASELINE_MODEL="${ACTIVE_SEARCH_BASELINE_MODEL:-}"
if [[ -z "$BASELINE_MODEL" ]]; then
  if [[ -f "$EVOLVER_ROOT/project/project-4/hoss-evolution/best/current/harness/model.py" ]]; then
    BASELINE_MODEL="$EVOLVER_ROOT/project/project-4/hoss-evolution/best/current/harness/model.py"
  elif [[ -f "$EVOLVER_ROOT/project/project-3/hoss-evolution/best/current/harness/model.py" ]]; then
    BASELINE_MODEL="$EVOLVER_ROOT/project/project-3/hoss-evolution/best/current/harness/model.py"
  else
    BASELINE_MODEL=""
  fi
fi

TASK_MODEL="$WORKSPACE/best/current/harness/model.py"
if [[ ! -f "$TASK_MODEL" ]]; then
  if [[ -z "$BASELINE_MODEL" || ! -f "$BASELINE_MODEL" ]]; then
    echo "Missing baseline model (set ACTIVE_SEARCH_BASELINE_MODEL)" >&2
    exit 2
  fi
  mkdir -p "$(dirname "$TASK_MODEL")"
  cp -f "$BASELINE_MODEL" "$TASK_MODEL"
fi

SUMMARY_PATH="${SUMMARY_PATH:-$ACTIVE_SEARCH_DIR/evolution_summary_${RUN_TAG}.csv}"
if [[ ! -f "$SUMMARY_PATH" ]]; then
  {
    echo -e "task,run_tag,iterations,llm_model,workspace,status,best_final_score,winner,evaluated_at"
  } >"$SUMMARY_PATH"
fi

if [[ "$FORCE_RERUN" != "1" ]]; then
  if awk -F ',' -v t="$TASK" -v tag="$RUN_TAG" -v it="$ITERATIONS" -v lm="$LLM_MODEL_NAME" '
    NR>1 && $1==t && $2==tag && $3==it && $4==lm && $6=="ok" {found=1}
    END {exit (found?0:1)}
  ' "$SUMMARY_PATH"; then
    echo "=== Skipping task=${TASK} (already ok in $SUMMARY_PATH) ==="
    exit 0
  fi
fi

export PROPOSER_MAX_ITERATIONS=40
export PROPOSER_TIMEOUT_SECONDS=600
export HARNESS_RUN_SCRIPT="$ACTIVE_SEARCH_DIR/harness_run_script.sh"
export REQUIRE_HARNESS_RUN_SCRIPT="1"
export HARNESS_RUN_TIMEOUT_SECONDS="3600"
export FEISHU_POST_ENABLED=0
export NEXAU_ENABLE_RUN_SHELL_COMMAND="0"
export EVOLVER_TEST_MODE="${EVOLVER_TEST_MODE:-0}"
export HARNESS_BATCH_SIZE="${HARNESS_BATCH_SIZE:-16}"
export PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}"

USE_GPU="${USE_GPU:-1}"
GPU_COUNT="0"
if command -v nvidia-smi >/dev/null 2>&1; then
  GPU_COUNT="$(nvidia-smi -L 2>/dev/null | grep -c '^GPU ' || true)"
fi
if [[ "$GPU_COUNT" == "0" ]]; then
  if compgen -G "/dev/nvidia[0-9]*" >/dev/null; then
    GPU_COUNT="$(ls -1 /dev/nvidia[0-9]* 2>/dev/null | wc -l | tr -d ' ')"
  fi
fi

if [[ -z "${HARNESS_DEVICE:-}" ]]; then
  if [[ "$USE_GPU" == "1" && "${GPU_COUNT:-0}" != "0" ]]; then
    export HARNESS_DEVICE="cuda"
  else
    export HARNESS_DEVICE="cpu"
  fi
fi

if [[ "${HARNESS_DEVICE:-}" == "cuda" && "$USE_GPU" == "1" && "${GPU_COUNT:-0}" != "0" ]]; then
  export EVOLVER_NUM_GPUS="$GPU_COUNT"
else
  export EVOLVER_NUM_GPUS="0"
fi

PROPOSER_PROMPT_PREFIX_PATH="$ACTIVE_SEARCH_DIR/proposer_prompt_prefix.txt"
export PROPOSER_PROMPT_PREFIX="$(cat "$PROPOSER_PROMPT_PREFIX_PATH")"$'\n'

export ACTIVE_SEARCH_ENV_PREFIX="ACTIVE_SEARCH"
export ACTIVE_SEARCH_TASK="$TASK"
export ACTIVE_SEARCH_DATA_CSV="$DATA_CSV"
export ACTIVE_SEARCH_DATASETS_DIR="$DATASETS_DIR"
export ACTIVE_SEARCH_STATE_PATH="$WORKSPACE/active_search_state_${TASK}.json"

EVALUATE_SCRIPT_PATH="$ACTIVE_SEARCH_DIR/evaluate.py"
evaluated_at="$(date -Is)"

ARGS=(python -u "$EVOLVER_ROOT/scripts/run_evolution.py" --workspace "$WORKSPACE" --iterations "$ITERATIONS" --evaluate-script "$EVALUATE_SCRIPT_PATH")
cd "$EVOLVER_ROOT"
CONDA_RUN_ARGS=(-n "$CONDA_ENV")
if conda run --help 2>/dev/null | grep -q -- "--no-capture-output"; then
  CONDA_RUN_ARGS=(--no-capture-output -n "$CONDA_ENV")
fi
conda run "${CONDA_RUN_ARGS[@]}" "${ARGS[@]}" && run_status="ok" || run_status="run_failed"

best_score=""
winner=""
if [[ -f "$WORKSPACE/best/current/eval_scores.json" ]]; then
  result="$(EVOLVER_WORKSPACE="$WORKSPACE" python - <<'PY'
import json
import re
from pathlib import Path
import os

ws = Path(os.environ["EVOLVER_WORKSPACE"]).expanduser().resolve()
score_path = ws / "best" / "current" / "eval_scores.json"
winner_path = ws / "best" / "current" / "winner_note.md"

score = ""
winner = ""
try:
    if score_path.exists():
        score = str(json.loads(score_path.read_text(encoding="utf-8")).get("final_score", ""))
except Exception:
    score = ""
try:
    if winner_path.exists():
        m = re.search(r"Winner:\\s*(\\S+)", winner_path.read_text(encoding="utf-8"))
        if m:
            winner = m.group(1)
except Exception:
    winner = ""

print(f"{score},{winner}")
PY
)"
  best_score="${result%%,*}"
  winner="${result#*,}"
else
  if [[ "$run_status" == "ok" ]]; then
    run_status="no_best"
  fi
fi

echo -e "${TASK},${RUN_TAG},${ITERATIONS},${LLM_MODEL_NAME},${WORKSPACE},${run_status},${best_score},${winner},${evaluated_at}" >>"$SUMMARY_PATH"

echo
echo -e "task\tworkspace\tdataset_csv"
echo -e "${TASK}\t${WORKSPACE}\t${DATA_CSV}"
echo
echo "Saved summary to: $SUMMARY_PATH"
