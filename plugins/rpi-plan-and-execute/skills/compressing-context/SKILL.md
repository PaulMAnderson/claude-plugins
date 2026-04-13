---
name: compressing-context
description: Compress session context to .rpi/CONTEXT.md when context window fills up
user-invocable: true
---

# Compressing Context

## Overview

Produce a session-specific summary in `.rpi/CONTEXT.md` and a long-term project-level log in `.rpi/PROJECT.md`.
These files persist across sessions and are read by the `SessionStart` hook to restore essential context.

**Announce at start:** "I'm using the compressing-context skill to summarise this session and update the project log."

## Core Technique: Anchored Iterative Summarization

Do NOT regenerate from scratch each time. If the files already exist, read them first and MERGE new information into each section rather than replacing. This prevents information drift across multiple compression cycles.

## 1. Session Context (.rpi/CONTEXT.md)

This file captures the "hot" state of the current session.

### Sections (Required)

- **Session Intent:** 2–4 sentences describing the current session's goal.
- **Files Modified:** List every file created or changed in this session with a one-line description.
- **Decisions Made:** List significant decisions made in this session with brief rationale.
- **Current State:** Precise description of where we are (passing/failing/phase).
- **Next Steps:** Numbered list of immediate next actions.

## 2. Project-Level Progress Log (.rpi/PROJECT.md)

This file tracks long-term progress and architectural decisions across multiple sessions.

### Sections (Required)

- **Git State:** 
    - Current Branch: `git branch --show-current`
    - Recent Commits: `git log --oneline -10`
- **Implementation Status:** 
    - A table of phases/tasks and their current status (Planned, In Progress, Completed, Blocked).
- **Decisions Log:** 
    - A historical record of key architectural decisions that affect the entire project.
- **Open Questions/Risks:** 
    - Any unresolved questions or identified risks that need future attention.

## Process

1. **GATHER:**
    - Read existing `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` if present.
    - Run `git branch --show-current` and `git log --oneline -10`.
2. **GENERATE:**
    - Create/update the **Session Context** using the conversation history.
    - Create/update the **Project Log** by merging new git state and implementation progress.
3. **MERGE:**
    - For lists and logs, **append** new entries; do not remove existing ones unless they are superseded.
4. **WRITE:**
    - Write the result to `.rpi/CONTEXT.md` and `.rpi/PROJECT.md`.
5. **REFRESH WORKSPACE (New):**
    - Run `python3 plugins/rpi-plan-and-execute/scripts/monitor.py` to update the central workspace dashboard with the latest project phase.
6. **CONFIRM:**
    - Confirm both files are updated and provide a brief summary of the current project status.

## Reading These Files (For Future Sessions)

When a session starts, these files are automatically injected into your context. Use them to:
- Understand the long-term goal and recent progress (`PROJECT.md`).
- Identify where the last session left off (`CONTEXT.md`).
- Avoid asking the user for context that is already recorded.

## Red Flags

**Stop and refactor when you see:**
- `CONTEXT.md` or `PROJECT.md` missing required sections.
- Information being lost during the "merge" phase.
- Vague "Current State" descriptions that don't help a new agent resume work.
- Outdated git state in `PROJECT.md`.
