#!/usr/bin/env bash

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "When instructed to use a 'general-purpose' agent, invoke the 'using-generic-agents' skill first."
  }
}
EOF

exit 0
