#!/usr/bin/env bash

cat <<EOF
{
  "decision": "allow",
  "hookSpecificOutput": {
    "additionalContext": "When instructed to use a 'general-purpose' agent, invoke the 'using-generic-agents' skill (rpi-basic-agents:using-generic-agents) first."
  }
}
EOF

exit 0
