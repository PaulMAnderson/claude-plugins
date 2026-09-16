#!/usr/bin/env bash
# Verify the append-only project history and live status contract.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
TMP_PROJECT=$(mktemp -d)
cleanup() {
  python3 - "$TMP_PROJECT" <<'PY_CLEAN'
from pathlib import Path
import shutil
import sys
path = Path(sys.argv[1])
if path.name.startswith("tmp") and path.is_dir():
    shutil.rmtree(path)
PY_CLEAN
}
trap cleanup EXIT
STATE="$REPO_ROOT/plugins/astrolabe-plan-and-execute/scripts/astrolabe-state.py"

python3 "$STATE" --root "$TMP_PROJECT" init
[ -s "$TMP_PROJECT/.astrolabe/PROJECT.md" ]
[ -s "$TMP_PROJECT/.astrolabe/PLANNED.md" ]
[ -s "$TMP_PROJECT/.astrolabe/STATUS.md" ]
[ -s "$TMP_PROJECT/.astrolabe/HISTORY.md" ]

python3 "$STATE" --root "$TMP_PROJECT" enter --tier quick --work shell-check
python3 "$STATE" --root "$TMP_PROJECT" finish --tier quick --work shell-check --intent 'first intent' --outcome 'first outcome'
python3 "$STATE" --root "$TMP_PROJECT" finish --tier quick --work shell-check --intent 'second intent' --outcome 'second outcome'
python3 "$STATE" --root "$TMP_PROJECT" init

python3 - "$TMP_PROJECT" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1]) / ".astrolabe"
history = (root / "HISTORY.md").read_text()
status = (root / "STATUS.md").read_text()
assert history.count("### ") == 2
assert "first intent" in history and "first outcome" in history
assert "second intent" in history and "second outcome" in history
assert "schema_version: 1" in status
assert "current_tier: none" in status
assert "current_work: null" in status
assert "second outcome" in status
PY
printf 'Project history and status checks passed\n'
