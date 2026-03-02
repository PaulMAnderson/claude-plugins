#!/usr/bin/env bash
# PostToolUse hook: context pressure monitor
# Tracks tool call count as proxy for context growth.
# Injects reminder at configurable thresholds.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

# Configurable thresholds (override via env vars)
WARN_THRESHOLD="${RPI_CONTEXT_WARN_THRESHOLD:-40}"
URGENT_THRESHOLD="${RPI_CONTEXT_URGENT_THRESHOLD:-70}"

# Counter file — session-scoped, lives in project .rpi/ directory
# Fall back to /tmp if no project dir is accessible
RPI_DIR="${CLAUDE_PROJECT_DIR:-.}/.rpi"
mkdir -p "$RPI_DIR" 2>/dev/null || RPI_DIR="/tmp/.rpi-$$"
mkdir -p "$RPI_DIR"
COUNTER_FILE="$RPI_DIR/context-monitor-count"

# Read current count
COUNT=0
if [ -f "$COUNTER_FILE" ]; then
  COUNT=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
fi

COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Below warn threshold — exit silently
if [ "$COUNT" -lt "$WARN_THRESHOLD" ]; then
  exit 0
fi

# Urgent threshold
if [ "$COUNT" -ge "$URGENT_THRESHOLD" ]; then
  echo 0 > "$COUNTER_FILE"   # reset after alert
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "<CONTEXT_PRESSURE level=\"URGENT\">\n⚠️ URGENT: This session has accumulated significant context (${COUNT}+ tool calls). Context quality is degrading. You MUST run the compressing-context skill NOW before continuing, then use /compress-context to write the summary to .rpi/CONTEXT.md. After that, prompt the user to /clear and restart with fresh context.\n</CONTEXT_PRESSURE>"
  }
}
EOF
  exit 0
fi

# Warn threshold
if [ "$COUNT" -ge "$WARN_THRESHOLD" ]; then
  echo 0 > "$COUNTER_FILE"   # reset after alert
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "<CONTEXT_PRESSURE level=\"WARNING\">\n📊 Context notice: This session has completed ${COUNT} tool calls. Context is building up. Consider running /compress-context soon to preserve state before a /clear. You can continue for now, but plan for a compression checkpoint.\n</CONTEXT_PRESSURE>"
  }
}
EOF
  exit 0
fi

exit 0
