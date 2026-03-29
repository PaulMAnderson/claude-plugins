#!/usr/bin/env bash
# Integration tests for session-monitor.py journaling behaviour.
# Tests all three AC2 acceptance criteria.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
PASS=0
FAIL=0

TMP_PROJECT=$(mktemp -d)
trap "rm -rf '$TMP_PROJECT'" EXIT

run_hook() {
  echo "$1" | CLAUDE_PROJECT_DIR="$TMP_PROJECT" \
    RPI_CONTEXT_WARN_THRESHOLD=1000 \
    python3 "$REPO_ROOT/plugins/rpi-plan-and-execute/hooks/session-monitor.py"
}

assert_pass() {
  echo "✓ $1"
  PASS=$((PASS + 1))
}

assert_fail() {
  echo "✗ $1"
  FAIL=$((FAIL + 1))
}

# ── AC2.1: journal.json created on first tool call (non-write tool) ───────────
run_hook '{"tool_name": "Read", "tool_input": {}}' > /dev/null
if [ -f "$TMP_PROJECT/.rpi/journal.json" ]; then
  assert_pass "AC2.1: journal.json created on first (non-write) tool call"
else
  assert_fail "AC2.1: journal.json not created after first tool call"
fi

# ── AC2.2: Write tool updates modifiedFiles in journal.json ──────────────────
run_hook '{"tool_name": "Write", "tool_input": {"file_path": "src/foo.ts"}}' > /dev/null
if python3 -c "
import json, sys
j = json.load(open('$TMP_PROJECT/.rpi/journal.json'))
sys.exit(0 if 'src/foo.ts' in j['modifiedFiles'] else 1)
" 2>/dev/null; then
  assert_pass "AC2.2: Write tool appended src/foo.ts to modifiedFiles"
else
  assert_fail "AC2.2: src/foo.ts not found in journal.json modifiedFiles"
fi

# AC2.2: Edit tool also tracked
run_hook '{"tool_name": "Edit", "tool_input": {"file_path": "src/bar.ts"}}' > /dev/null
if python3 -c "
import json, sys
j = json.load(open('$TMP_PROJECT/.rpi/journal.json'))
sys.exit(0 if 'src/bar.ts' in j['modifiedFiles'] else 1)
" 2>/dev/null; then
  assert_pass "AC2.2: Edit tool appended src/bar.ts to modifiedFiles"
else
  assert_fail "AC2.2: src/bar.ts not found in journal.json modifiedFiles"
fi

# AC2.2: non-write tool does NOT add to modifiedFiles
run_hook '{"tool_name": "Bash", "tool_input": {"command": "echo hi"}}' > /dev/null
count=$(python3 -c "
import json
j = json.load(open('$TMP_PROJECT/.rpi/journal.json'))
print(len(j['modifiedFiles']))
")
if [ "$count" -eq 2 ]; then
  assert_pass "AC2.2: non-write tool does not add to modifiedFiles (count still 2)"
else
  assert_fail "AC2.2: modifiedFiles count is $count, expected 2"
fi

# ── AC2.3: SESSION.md exists with required sections ───────────────────────────
if [ -f "$TMP_PROJECT/.rpi/SESSION.md" ]; then
  assert_pass "AC2.3: SESSION.md created"
  for section in "Session Intent" "Files Modified" "Decisions Made" "Current State" "Next Steps"; do
    if grep -q "$section" "$TMP_PROJECT/.rpi/SESSION.md"; then
      assert_pass "AC2.3: SESSION.md contains '$section'"
    else
      assert_fail "AC2.3: SESSION.md missing '$section'"
    fi
  done
else
  assert_fail "AC2.3: SESSION.md not created after write tool call"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ] || exit 1
