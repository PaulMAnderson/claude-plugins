---
phase: 3
title: Smart Context Monitoring
context-budget: medium
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/hooks/hooks.json
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/hooks/session-monitor.py
depends-on: [phase_02.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Implement real-time context monitoring using the StatusLine hook and enhance the session monitor to use actual context usage percentages.

**Architecture:** This phase adds a `statusline.py` hook to track `context_window.used_percentage`. It updates `hooks.json` to register this new hook. `session-monitor.py` is upgraded to read this percentage from a shared `.rpi/context-usage.json` file and trigger compression alerts based on configurable thresholds and "natural breaks" (e.g., task completion or test runs).

**Tech Stack:** Python (Hooks), JSON.

**Scope:** Phase 3 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC3: Smart Context Monitoring
- **rpi-datasci.AC3.1 Success:** `plugins/rpi-plan-and-execute/hooks/statusline.py` exists; registered in `hooks.json` as a StatusLine hook; outputs a visual bar string
- **rpi-datasci.AC3.2 Success:** StatusLine hook writes `context_window.used_percentage` to `.rpi/context-usage.json` on each invocation
- **rpi-datasci.AC3.3 Success:** `session-monitor.py` reads real % from `.rpi/context-usage.json`; emits WARNING `additionalContext` when ≥ soft threshold (default 50%) at a natural break event
- **rpi-datasci.AC3.4 Success:** `session-monitor.py` emits URGENT `additionalContext` when ≥ hard threshold (default 75%) regardless of break type
- **rpi-datasci.AC3.5 Success:** Natural break detection triggers on: `TaskUpdate` with `status: completed`; Bash calls containing `pytest`, `Rscript`, or `matlab -batch`
- **rpi-datasci.AC3.6 Success:** Thresholds configurable via `RPI_CONTEXT_SOFT_THRESHOLD` and `RPI_CONTEXT_HARD_THRESHOLD` environment variables
- **rpi-datasci.AC3.7 Failure:** `session-monitor.py` uses tool-call counter as primary signal when `.rpi/context-usage.json` exists and is fresh (< 60 seconds old)

---

<!-- START_SUBCOMPONENT_A (tasks 1-2) -->
<!-- START_TASK_1 -->
### Task 1: Implement StatusLine Hook

**Verifies:** rpi-datasci.AC3.1, rpi-datasci.AC3.2

**Files:**
- Create: `plugins/rpi-plan-and-execute/hooks/statusline.py`
- Modify: `plugins/rpi-plan-and-execute/hooks/hooks.json`

**Implementation:**
- `statusline.py`:
  - Read JSON from `sys.stdin`.
  - Extract `context_window.used_percentage`.
  - Write percentage to `.rpi/context-usage.json` (as a JSON object).
  - Generate a visual bar string based on the percentage (e.g., 50% = `[████████░░░░░░░░]`).
  - Output hook response JSON with `statusLineText`.
- `hooks.json`:
  - Register `StatusLine` hook pointing to `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/statusline.py`.

**Verification:**
Run: `echo '{"context_window": {"used_percentage": 52}}' | python3 plugins/rpi-plan-and-execute/hooks/statusline.py`
Expected: 
1. `.rpi/context-usage.json` contains `{"used_percentage": 52}`.
2. Stdout contains a JSON with `statusLineText` including the visual bar and "52%".

**Commit:** `feat(hooks): add statusline hook for context monitoring`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Enhance Session Monitor

**Verifies:** rpi-datasci.AC3.3, rpi-datasci.AC3.4, rpi-datasci.AC3.5, rpi-datasci.AC3.6, rpi-datasci.AC3.7

**Files:**
- Modify: `plugins/rpi-plan-and-execute/hooks/session-monitor.py`

**Implementation:**
- Read `RPI_CONTEXT_SOFT_THRESHOLD` (default 50) and `RPI_CONTEXT_HARD_THRESHOLD` (default 75).
- Attempt to read real percentage from `.rpi/context-usage.json`. 
- Check file age (fall back to tool-count if > 60s old or missing).
- Define "natural break" logic:
  - `tool_name == "TaskUpdate"` AND `tool_input.get("status") == "completed"`.
  - `tool_name == "Bash"` AND `tool_input.get("command")` matches `pytest`, `Rscript`, or `matlab -batch`.
- Logic:
  - If `percentage >= HARD_THRESHOLD`: fire URGENT immediately.
  - If `percentage >= SOFT_THRESHOLD` AND `is_natural_break`: fire WARNING.
  - Else: increment tool counter (as fallback/secondary signal).
- Update `additionalContext` messages to reflect real percentages.

**Verification:**
Test with simulated hook payloads:
1. `TaskUpdate` completed at 55% -> WARNING.
2. Random tool at 55% -> No warning (unless tool count high).
3. Random tool at 80% -> URGENT.

**Commit:** `feat(hooks): upgrade session-monitor to use real context usage`
<!-- END_TASK_2 -->
<!-- END_SUBCOMPONENT_A -->
