---
phase: 3
title: Context monitor hook — PostToolUse hook with tool-count debouncing
context-budget: small
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - plugins/rpi-plan-and-execute/hooks/hooks.json
  - plugins/rpi-plan-and-execute/hooks/session-start.sh
depends-on: [phase_1]
---

# Phase 3: Context Monitor Hook

## Acceptance Criteria
- rpi-context-engineering.AC2.1 through AC2.6

## Tasks

### Task 3.1 — Create context-monitor.sh

Create `plugins/rpi-plan-and-execute/hooks/context-monitor.sh`:

```bash
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
```

Make the script executable: `chmod +x plugins/rpi-plan-and-execute/hooks/context-monitor.sh`

### Task 3.2 — Add PostToolUse entry to hooks.json

Update `plugins/rpi-plan-and-execute/hooks/hooks.json` to add the PostToolUse hook
alongside the existing SessionStart hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/context-monitor.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Note: No `matcher` on the PostToolUse hook — it should fire after every tool call.
The timeout of 5 seconds prevents the hook from blocking if the counter file is slow.

### Task 3.3 — Add .rpi/ to .gitignore
In `plugins/rpi-plan-and-execute/.gitignore`, add:
```
.rpi/
```
The `.rpi/` directory is session-scoped and should not be committed.

## Done When
- `context-monitor.sh` exists and is executable
- `hooks.json` contains a `PostToolUse` entry
- `.gitignore` includes `.rpi/`
- Manual test: run any Claude Code command in a project with this plugin; after 40+ tool calls the warning fires
