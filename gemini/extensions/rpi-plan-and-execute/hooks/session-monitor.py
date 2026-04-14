#!/usr/bin/env python3
"""
AfterTool hook: session journal and context pressure monitor.

Ported from rpi-plan-and-execute Claude plugin.
- journal.json creation on first tool call of any session
- modifiedFiles tracking on file-writing tool calls
- SESSION.md regeneration after each file modification
- Smart context monitoring using real usage percentage and natural breaks
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

# ── Configuration ─────────────────────────────────────────────────────────────
SOFT_THRESHOLD = int(os.environ.get("RPI_CONTEXT_SOFT_THRESHOLD", "50"))
HARD_THRESHOLD = int(os.environ.get("RPI_CONTEXT_HARD_THRESHOLD", "75"))

# Fallback thresholds based on tool counts (if real percentage is unavailable)
WARN_COUNT_THRESHOLD = int(os.environ.get("RPI_CONTEXT_WARN_THRESHOLD", "40"))
URGENT_COUNT_THRESHOLD = int(os.environ.get("RPI_CONTEXT_URGENT_THRESHOLD", "70"))

# Gemini CLI tool names that write to the filesystem
FILE_MODIFYING_TOOLS = {"replace", "write_file"}

# ── Parse hook payload from stdin ─────────────────────────────────────────────
try:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
except (json.JSONDecodeError, ValueError):
    payload = {}

cwd = payload.get("cwd", ".")
tool_name = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {})

# ── Paths ─────────────────────────────────────────────────────────────────────
rpi_dir = os.path.join(cwd, ".rpi")
os.makedirs(rpi_dir, exist_ok=True)

COUNTER_FILE = os.path.join(rpi_dir, "context-monitor-count")
JOURNAL_FILE = os.path.join(rpi_dir, "journal.json")
SESSION_FILE = os.path.join(rpi_dir, "SESSION.md")
USAGE_FILE = os.path.join(rpi_dir, "context-usage.json")

# ── Real Context Usage (AC3) ──────────────────────────────────────────────────
used_percentage = None
usage_fresh = False

if os.path.exists(USAGE_FILE):
    try:
        with open(USAGE_FILE) as f:
            usage_data = json.load(f)
            used_percentage = usage_data.get("used_percentage")
            timestamp = usage_data.get("timestamp", 0)
            if time.time() - timestamp < 60:
                usage_fresh = True
    except (json.JSONDecodeError, ValueError):
        pass

# ── Natural Break Detection (AC3.5) ───────────────────────────────────────────
is_natural_break = False
# In Gemini, we can check for commands that signify a break
if tool_name == "run_shell_command":
    cmd = tool_input.get("command", "")
    if any(x in cmd for x in ["pytest", "npm test", "go test", "cargo test", "make test"]):
        is_natural_break = True

# ── Counter Fallback ──────────────────────────────────────────────────────────
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

# ── Threshold output (AC3.3, AC3.4) ───────────────────────────────────────────
result: dict = {"decision": "allow"}
trigger_urgent = False
trigger_warning = False
current_usage_str = ""

if usage_fresh and used_percentage is not None:
    current_usage_str = f"{used_percentage}% context usage"
    if used_percentage >= HARD_THRESHOLD:
        trigger_urgent = True
    elif used_percentage >= SOFT_THRESHOLD and is_natural_break:
        trigger_warning = True
else:
    # Fallback to tool counts
    current_usage_str = f"{count} tool calls"
    if count >= URGENT_COUNT_THRESHOLD:
        trigger_urgent = True
    elif count >= WARN_COUNT_THRESHOLD:
        trigger_warning = True

if trigger_urgent:
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    result = {
        "decision": "allow",
        "hookSpecificOutput": {
            "additionalContext": (
                f'<CONTEXT_PRESSURE level="URGENT">\n'
                f"⚠️ URGENT: High context pressure detected ({current_usage_str}). "
                f"Context quality is degrading. You MUST run the compressing-context skill NOW before "
                f"continuing, then use /compress-context to write the summary to .rpi/CONTEXT.md. "
                f"After that, you should prompt the user to /clear and restart with fresh context.\n"
                f"</CONTEXT_PRESSURE>"
            ),
        }
    }
elif trigger_warning:
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    result = {
        "decision": "allow",
        "hookSpecificOutput": {
            "additionalContext": (
                f'<CONTEXT_PRESSURE level="WARNING">\n'
                f"📊 Context notice: Context pressure is rising ({current_usage_str}). "
                f"At this natural break, consider running /compress-context soon to preserve "
                f"state before a /clear. You can continue for now, but plan for a compression checkpoint.\n"
                f"</CONTEXT_PRESSURE>"
            ),
        }
    }
else:
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

sys.stdout.write(json.dumps(result))
sys.exit(0)
