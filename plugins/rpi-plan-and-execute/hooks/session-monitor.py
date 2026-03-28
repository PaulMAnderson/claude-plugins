#!/usr/bin/env python3
"""
PostToolUse hook: session journal and context pressure monitor.

Replaces context-monitor.sh. Preserves threshold warning behaviour and adds:
- journal.json creation on first tool call of any session (AC2.1)
- modifiedFiles tracking on file-writing tool calls (AC2.2)
- SESSION.md regeneration after each file modification (AC2.3)

journal.json schema:
  {
    "version": 1,
    "sessionIntent": "",        # set manually or by future tooling
    "startedAt": "<ISO 8601>",
    "modifiedFiles": [],        # appended on each file-writing tool call
    "decisions": [],            # list of {"description": str, "rationale": str}
    "currentState": "",         # set manually or by future tooling
    "nextSteps": []             # list of strings
  }
"""

import json
import os
import sys
from datetime import datetime, timezone

# ── Configuration ─────────────────────────────────────────────────────────────
WARN_THRESHOLD = int(os.environ.get("RPI_CONTEXT_WARN_THRESHOLD", "40"))
URGENT_THRESHOLD = int(os.environ.get("RPI_CONTEXT_URGENT_THRESHOLD", "70"))

# Claude Code tool names that write to the filesystem
FILE_MODIFYING_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "replace", "write_file"}

# ── Paths ─────────────────────────────────────────────────────────────────────
project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
rpi_dir = os.path.join(project_dir, ".rpi")
os.makedirs(rpi_dir, exist_ok=True)

COUNTER_FILE = os.path.join(rpi_dir, "context-monitor-count")
JOURNAL_FILE = os.path.join(rpi_dir, "journal.json")
SESSION_FILE = os.path.join(rpi_dir, "SESSION.md")

# ── Parse hook payload from stdin ─────────────────────────────────────────────
try:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
except (json.JSONDecodeError, ValueError):
    payload = {}

tool_name = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {})

# ── Counter (preserved from context-monitor.sh) ───────────────────────────────
count = 0
try:
    with open(COUNTER_FILE) as f:
        count = int(f.read().strip())
except (FileNotFoundError, ValueError):
    pass
count += 1

# ── Journal ───────────────────────────────────────────────────────────────────
journal_existed = os.path.exists(JOURNAL_FILE)

journal: dict = {}
if journal_existed:
    try:
        with open(JOURNAL_FILE) as f:
            journal = json.load(f)
    except (json.JSONDecodeError, ValueError):
        journal = {}

journal.setdefault("version", 1)
journal.setdefault("sessionIntent", "")
journal.setdefault("startedAt", datetime.now(timezone.utc).isoformat())
journal.setdefault("modifiedFiles", [])
journal.setdefault("decisions", [])
journal.setdefault("currentState", "")
journal.setdefault("nextSteps", [])

# AC2.1: create journal.json on first tool call of the session
if not journal_existed:
    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=2)

# AC2.2: track file modifications
if tool_name in FILE_MODIFYING_TOOLS:
    file_path = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or ""
    )
    if file_path and file_path not in journal["modifiedFiles"]:
        journal["modifiedFiles"].append(file_path)

    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=2)

    # AC2.3: regenerate SESSION.md
    modified_list = (
        "\n".join(f"- {p}" for p in journal["modifiedFiles"])
        or "_None yet_"
    )
    decisions_list = (
        "\n".join(
            f"- **{d.get('description', '?')}**: {d.get('rationale', '')}"
            for d in journal.get("decisions", [])
            if isinstance(d, dict)
        )
        or "_None recorded_"
    )
    next_steps_list = (
        "\n".join(
            f"{i + 1}. {s}"
            for i, s in enumerate(journal.get("nextSteps", []))
        )
        or "_Not set_"
    )
    session_md = (
        "# Session State\n\n"
        f"_Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n\n"
        "## Session Intent\n"
        f"{journal['sessionIntent'] or '_Not set — edit .rpi/journal.json to record intent_'}\n\n"
        "## Files Modified\n"
        f"{modified_list}\n\n"
        "## Decisions Made\n"
        f"{decisions_list}\n\n"
        "## Current State\n"
        f"{journal['currentState'] or '_Not set_'}\n\n"
        "## Next Steps\n"
        f"{next_steps_list}\n"
    )
    with open(SESSION_FILE, "w") as f:
        f.write(session_md)

# ── Threshold output ──────────────────────────────────────────────────────────
result: dict = {}

if count >= URGENT_THRESHOLD:
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f'<CONTEXT_PRESSURE level="URGENT">\n'
                f"⚠️ URGENT: This session has accumulated significant context ({count}+ tool calls). "
                f"Context quality is degrading. You MUST run the compressing-context skill NOW before "
                f"continuing, then use /compress-context to write the summary to .rpi/CONTEXT.md. "
                f"After that, prompt the user to /clear and restart with fresh context.\n"
                f"</CONTEXT_PRESSURE>"
            ),
        }
    }
elif count >= WARN_THRESHOLD:
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f'<CONTEXT_PRESSURE level="WARNING">\n'
                f"📊 Context notice: This session has completed {count} tool calls. "
                f"Context is building up. Consider running /compress-context soon to preserve "
                f"state before a /clear. You can continue for now, but plan for a compression checkpoint.\n"
                f"</CONTEXT_PRESSURE>"
            ),
        }
    }
else:
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

print(json.dumps(result))
