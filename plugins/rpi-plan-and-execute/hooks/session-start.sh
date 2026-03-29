#!/usr/bin/env bash
# SessionStart hook for rpi-plan-and-execute plugin
# pattern: Imperative Shell

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
RPI_DIR="${PROJECT_ROOT}/.rpi"

# Helper function to read and escape file for JSON
escape_file() {
    local file_path="$1"
    if [[ -f "$file_path" ]]; then
        # Use python for robust JSON escaping of multi-line strings
        python3 -c "import json, sys; print(json.dumps(sys.stdin.read())[1:-1])" < "$file_path"
    else
        echo ""
    fi
}

# 1. Read mandatory using-plan-and-execute skill
using_plan_escaped=$(escape_file "${PLUGIN_ROOT}/skills/using-plan-and-execute/SKILL.md")

# 2. Read optional session-specific context
context_md_escaped=$(escape_file "${RPI_DIR}/CONTEXT.md")

# 3. Read optional project-level log
project_md_escaped=$(escape_file "${RPI_DIR}/PROJECT.md")

# Build the additionalContext string
ADDITIONAL_CONTEXT="<EXTREMELY_IMPORTANT>\n**The content below is from skills/using-plan-and-execute/SKILL.md - your introduction to using skills:**\n\n${using_plan_escaped}\n</EXTREMELY_IMPORTANT>"

if [[ -n "$context_md_escaped" ]]; then
    ADDITIONAL_CONTEXT="${ADDITIONAL_CONTEXT}\n\n<SESSION_CONTEXT>\n**Restored from .rpi/CONTEXT.md:**\n\n${context_md_escaped}\n</SESSION_CONTEXT>"
fi

if [[ -n "$project_md_escaped" ]]; then
    ADDITIONAL_CONTEXT="${ADDITIONAL_CONTEXT}\n\n<PROJECT_LOG>\n**Restored from .rpi/PROJECT.md:**\n\n${project_md_escaped}\n</PROJECT_LOG>"
fi

# Output context injection as JSON
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${ADDITIONAL_CONTEXT}"
  }
}
EOF

exit 0
