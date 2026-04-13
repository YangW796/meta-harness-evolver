#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
EVOLVER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="${ENV_FILE:-$EVOLVER_DIR/.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

python3 -m pip show lark-oapi >/dev/null 2>&1 || python3 -m pip install -U lark-oapi

TMPDIR="$(mktemp -d)"
mkdir -p "$TMPDIR/harness"
printf "test file\n" >"$TMPDIR/harness/test.txt"

cd "$ROOT_DIR"
python3 "$SCRIPT_DIR/post_to_research.py" 0 "$TMPDIR" 0 1
