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

TOP_RATIOS_RAW="${TOP_RATIOS:-0.01,0.10,0.20,0.30}"
ITERATIONS="${ITERATIONS:-1}"
ROUNDS="${ACTIVE_SEARCH_ROUNDS:-2}"
RUN_TAG_PREFIX="${RUN_TAG_PREFIX:-topk_growth}"
FORCE_RERUN="${FORCE_RERUN:-1}"
CONDA_ENV="${CONDA_ENV:-meta-harness-evolver0}"
SUMMARY_PATH="${SUMMARY_PATH:-$ACTIVE_SEARCH_DIR/topk_growth_summary_${TASK}.csv}"

DATASETS_DIR="${ACTIVE_SEARCH_DATASETS_DIR:-$EVOLVER_ROOT/BioDiscoveryAgent/datasets}"
DATA_CSV="${ACTIVE_SEARCH_DATA_CSV:-}"
if [[ -z "$DATA_CSV" ]]; then
  DATA_CSV="$DATASETS_DIR/ground_truth_${TASK}.csv"
fi
if [[ ! -f "$DATA_CSV" ]]; then
  echo "Dataset CSV not found: $DATA_CSV" >&2
  exit 2
fi

echo -e "task,top_ratio,run_tag,workspace,round1_hits,round2_hits,r2_minus_r1_hits,r2_cumulative_delta,top_k,total_hits,status" >"$SUMMARY_PATH"

IFS=',' read -r -a TOP_RATIOS <<<"$TOP_RATIOS_RAW"
if [[ "${#TOP_RATIOS[@]}" -eq 0 ]]; then
  echo "No TOP_RATIOS parsed from: $TOP_RATIOS_RAW" >&2
  exit 2
fi

for ratio in "${TOP_RATIOS[@]}"; do
  ratio_trim="$(echo "$ratio" | tr -d '[:space:]')"
  if [[ -z "$ratio_trim" ]]; then
    continue
  fi

  ratio_tag="$(echo "$ratio_trim" | sed 's/[^0-9]//g')"
  if [[ -z "$ratio_tag" ]]; then
    ratio_tag="x"
  fi
  run_tag="${RUN_TAG_PREFIX}_${ratio_tag}"

  echo
  echo "=== top_ratio=${ratio_trim} run_tag=${run_tag} ==="

  TASK="$TASK" \
  ACTIVE_SEARCH_TASK="$TASK" \
  ACTIVE_SEARCH_DATA_CSV="$DATA_CSV" \
  ACTIVE_SEARCH_TOP_RATIO="$ratio_trim" \
  ACTIVE_SEARCH_ROUNDS="$ROUNDS" \
  ACTIVE_SEARCH_RESUME_STATE="0" \
  RUN_TAG="$run_tag" \
  ITERATIONS="$ITERATIONS" \
  FORCE_RERUN="$FORCE_RERUN" \
  CONDA_ENV="$CONDA_ENV" \
  bash "$ACTIVE_SEARCH_DIR/run_evolution.sh"

  workspace="${EVOLVER_WORKSPACE:-${ACTIVE_SEARCH_DIR}/hoss-evolution_${run_tag}_${TASK}}"
  metrics_path="$workspace/best/current/harness/outputs/metrics.json"
  if [[ ! -f "$metrics_path" ]]; then
    echo -e "${TASK},${ratio_trim},${run_tag},${workspace},0,0,0,0,0,0,metrics_missing" >>"$SUMMARY_PATH"
    continue
  fi

  parsed="$(METRICS_PATH="$metrics_path" python - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["METRICS_PATH"]).expanduser().resolve()
payload = json.loads(path.read_text(encoding="utf-8"))
test = payload.get("metrics", {}).get("test", {})
details = test.get("round_details", [])

r1_hits = int(details[0].get("hits", 0)) if len(details) >= 1 and isinstance(details[0], dict) else 0
r2_hits = int(details[1].get("hits", 0)) if len(details) >= 2 and isinstance(details[1], dict) else 0

cum1 = int(details[0].get("cumulative_hits", r1_hits)) if len(details) >= 1 and isinstance(details[0], dict) else int(r1_hits)
cum2 = int(details[1].get("cumulative_hits", cum1 + r2_hits)) if len(details) >= 2 and isinstance(details[1], dict) else int(cum1 + r2_hits)

r2_minus_r1 = int(r2_hits - r1_hits)
r2_cumulative_delta = int(cum2 - cum1)
top_k = int(test.get("top_k", 0))
total_hits = int(test.get("total_hits", 0))

status = "ok" if len(details) >= 2 else "insufficient_rounds"
print(f"{r1_hits},{r2_hits},{r2_minus_r1},{r2_cumulative_delta},{top_k},{total_hits},{status}")
PY
)"

  echo -e "${TASK},${ratio_trim},${run_tag},${workspace},${parsed}" >>"$SUMMARY_PATH"
done

echo
echo "=== Top-k growth summary ==="
cat "$SUMMARY_PATH"

echo
echo "=== Stability check (using r2_cumulative_delta) ==="
SUMMARY_PATH="$SUMMARY_PATH" python - <<'PY'
import csv
import os
import sys
from pathlib import Path

path = Path(os.environ["SUMMARY_PATH"]).expanduser().resolve()
rows = []
with path.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter=",")
    for r in reader:
        if r.get("status") != "ok":
            continue
        try:
            ratio = float(r.get("top_ratio", "0"))
            delta = int(r.get("r2_cumulative_delta", "0"))
        except Exception:
            continue
        rows.append((ratio, delta))

rows.sort(key=lambda x: x[0])
if len(rows) < 2:
    print("Not enough valid rows to judge stability.")
    sys.exit(0)

deltas = [d for _, d in rows]
non_decreasing = all(deltas[i] <= deltas[i + 1] for i in range(len(deltas) - 1))
strict_steps = sum(1 for i in range(len(deltas) - 1) if deltas[i] < deltas[i + 1])

print("Ratios / deltas:", ", ".join([f"{r:.2%}:{d}" for r, d in rows]))
print(f"non_decreasing={non_decreasing}, strict_increase_steps={strict_steps}/{len(deltas)-1}")
if non_decreasing and strict_steps >= 1:
    print("Conclusion: observed stable growth across top-k settings.")
else:
    print("Conclusion: stable growth is NOT clearly observed across top-k settings.")
PY

echo
echo "Saved summary to: $SUMMARY_PATH"
