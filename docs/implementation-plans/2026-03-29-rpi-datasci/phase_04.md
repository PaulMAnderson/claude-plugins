---
phase: 4
title: Project-Level Progress Log
context-budget: small
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/hooks/session-start.sh
depends-on: [phase_03.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Create a persistent `PROJECT.md` to track long-term progress and decisions across sessions, and ensure it's injected at every session start.

**Architecture:** This phase enhances the `compressing-context` skill to generate a `PROJECT.md` file in the `.rpi/` directory. This file captures git state (branch, recent commits) and manually maintained sections (implementation status, decisions). The `session-start.sh` hook is updated to read and inject both `CONTEXT.md` (session-specific) and `PROJECT.md` (project-specific) into the model's context.

**Tech Stack:** Bash (Hooks), Markdown (Skills), Git.

**Scope:** Phase 4 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC4: Project-Level Progress Log
- **rpi-datasci.AC4.1 Success:** Running the `compressing-context` skill produces `.rpi/PROJECT.md` containing: current branch name, last 10 commits (short), implementation status table, decisions log entries
- **rpi-datasci.AC4.2 Success:** `.rpi/PROJECT.md` content is injected into session context by SessionStart hook when the file exists
- **rpi-datasci.AC4.3 Success:** `.rpi/CONTEXT.md` content is also injected by SessionStart hook when present (existing behaviour preserved)
- **rpi-datasci.AC4.4 Failure:** SessionStart hook fails or produces malformed JSON when `.rpi/PROJECT.md` or `.rpi/CONTEXT.md` does not yet exist

---

<!-- START_SUBCOMPONENT_A (tasks 1-2) -->
<!-- START_TASK_1 -->
### Task 1: Enhance Compressing Context Skill

**Verifies:** rpi-datasci.AC4.1

**Files:**
- Modify: `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md`

**Implementation:**
- Add a new section "Project-Level Progress Log" to the skill instructions.
- Instruct the agent to run `git branch --show-current` and `git log --oneline -10` to gather state.
- Define the format for `.rpi/PROJECT.md`:
  - Current Branch
  - Recent Commits
  - Implementation Status Table (Phases, Status, Completion %)
  - Decisions Log (Historical record of key architectural decisions)
  - Open Questions
- Update the "Process" section to include writing `.rpi/PROJECT.md` in addition to `.rpi/CONTEXT.md`.

**Verification:**
Run: `compressing-context` (mock usage)
Expected: Both `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` are created/updated with the specified content.

**Commit:** `feat(skills): add PROJECT.md generation to compressing-context`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Update SessionStart Hook

**Verifies:** rpi-datasci.AC4.2, rpi-datasci.AC4.3, rpi-datasci.AC4.4

**Files:**
- Modify: `plugins/rpi-plan-and-execute/hooks/session-start.sh`

**Implementation:**
- Update the script to check for existence of `.rpi/CONTEXT.md` and `.rpi/PROJECT.md`.
- Read and escape their contents if they exist.
- Concatenate their content into the `additionalContext` JSON payload.
- Ensure the script handles missing files gracefully (no errors, just empty/omitted context).
- Use a robust escaping method (like the existing `sed` + `awk` chain) for all injected files.

**Verification:**
Run: `plugins/rpi-plan-and-execute/hooks/session-start.sh` with and without `.rpi/` files.
Expected: JSON output is valid in both cases; context is present when files exist.

**Commit:** `feat(hooks): inject PROJECT.md and CONTEXT.md at session start`
<!-- END_TASK_2 -->
<!-- END_SUBCOMPONENT_A -->
