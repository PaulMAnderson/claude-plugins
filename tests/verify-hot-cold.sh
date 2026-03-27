#!/usr/bin/env bash
# Verifies the Hot/Cold pattern for refactored skill files.
# Checks: SKILL.md references REFERENCE.md, line count within limit,
# and REFERENCE.md exists and is non-empty.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
PASS=0
FAIL=0

check_skill() {
  local skill_path="$1"
  local line_limit="$2"
  local ref_path="${skill_path%SKILL.md}REFERENCE.md"

  # SKILL.md must reference REFERENCE.md
  if grep -q "REFERENCE.md" "${REPO_ROOT}/${skill_path}" 2>/dev/null; then
    echo "✓ ${skill_path} → contains REFERENCE.md reference"
    PASS=$((PASS + 1))
  else
    echo "✗ ${skill_path} → MISSING reference to REFERENCE.md"
    FAIL=$((FAIL + 1))
  fi

  # REFERENCE.md must exist and be non-empty
  if [ -s "${REPO_ROOT}/${ref_path}" ]; then
    echo "✓ ${ref_path} → exists and non-empty"
    PASS=$((PASS + 1))
  else
    echo "✗ ${ref_path} → MISSING or empty"
    FAIL=$((FAIL + 1))
  fi

  # SKILL.md must be under the line limit
  local lines
  lines=$(wc -l < "${REPO_ROOT}/${skill_path}")
  if [ "$lines" -lt "$line_limit" ]; then
    echo "✓ ${skill_path} → ${lines} lines (< ${line_limit})"
    PASS=$((PASS + 1))
  else
    echo "✗ ${skill_path} → ${lines} lines (≥ ${line_limit}, too large)"
    FAIL=$((FAIL + 1))
  fi
}

# TypeScript style skill: strict 150-line limit (reference skill)
check_skill \
  "plugins/rpi-house-style/skills/howto-code-in-typescript/SKILL.md" \
  150

# Process skills: 200-line limit (enforcement tables must stay hot)
check_skill \
  "plugins/rpi-plan-and-execute/skills/writing-implementation-plans/SKILL.md" \
  200

check_skill \
  "plugins/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md" \
  150

echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ] || exit 1
