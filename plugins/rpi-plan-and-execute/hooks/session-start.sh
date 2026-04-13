#!/usr/bin/env bash
# SessionStart hook for rpi-plan-and-execute plugin
# Restores saved session/project context from .rpi/ if present.
# pattern: Imperative Shell

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
RPI_DIR="${PROJECT_ROOT}/.rpi"

# Helper: JSON-escape a file's contents; emits empty string if file absent
escape_file() {
    local file_path="$1"
    if [[ -f "$file_path" ]]; then
        python3 -c "import json, sys; print(json.dumps(sys.stdin.read())[1:-1])" < "$file_path"
    else
        echo ""
    fi
}

context_md_escaped=$(escape_file "${RPI_DIR}/CONTEXT.md")
project_md_escaped=$(escape_file "${RPI_DIR}/PROJECT.md")

# Only emit output when there is saved context to restore
ADDITIONAL_CONTEXT=""

if [[ -n "$context_md_escaped" ]]; then
    ADDITIONAL_CONTEXT="${ADDITIONAL_CONTEXT}<SESSION_CONTEXT>\n**Restored from .rpi/CONTEXT.md:**\n\n${context_md_escaped}\n</SESSION_CONTEXT>"
fi

if [[ -n "$project_md_escaped" ]]; then
    [[ -n "$ADDITIONAL_CONTEXT" ]] && ADDITIONAL_CONTEXT="${ADDITIONAL_CONTEXT}\n\n"
    ADDITIONAL_CONTEXT="${ADDITIONAL_CONTEXT}<PROJECT_LOG>\n**Restored from .rpi/PROJECT.md:**\n\n${project_md_escaped}\n</PROJECT_LOG>"
fi

if [[ -z "$ADDITIONAL_CONTEXT" ]]; then
    exit 0
fi

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${ADDITIONAL_CONTEXT}"
  }
}
EOF

exit 0
