---
name: compressing-context
description: Compress session context to .astrolabe/CONTEXT.md when context window fills up
user-invocable: true
---

# Compressing Context

## Overview

Produce a session-specific summary in `.astrolabe/CONTEXT.md` while preserving the stable project description in `.astrolabe/PROJECT.md`.
These files persist across sessions and are read by the `SessionStart` hook to restore essential context.

**Announce at start:** "I'm using the compressing-context skill to summarise this session and update the project log."

## Core Technique: Anchored Iterative Summarization

Do NOT regenerate from scratch each time. If the files already exist, read them first and MERGE new information into each section rather than replacing. This prevents information drift across multiple compression cycles.

## 1. Session Context (.astrolabe/CONTEXT.md)

This file captures the "hot" state of the current session.

### Sections (Required)

- **Session Intent:** 2–4 sentences describing the current session's goal.
- **Files Modified:** List every file created or changed in this session with a one-line description.
- **Decisions Made:** List significant decisions made in this session with brief rationale.
- **Current State:** Precise description of where we are (passing/failing/phase).
- **Next Steps:** Numbered list of immediate next actions.

## 2. Project Description (.astrolabe/PROJECT.md)

This file is the stable project description. Read it for context and update it only when the project description itself changes; keep progress events in HISTORY.md.

Keep its human-authored purpose and enduring architecture. Put session decisions, git state, run status, and risks in CONTEXT.md; append outcomes to HISTORY.md. Do not regenerate or replace the description while checkpointing.

## Process

1. **GATHER:**
    - Read existing `.astrolabe/CONTEXT.md` and `.astrolabe/PROJECT.md` if present.
    - Run `git branch --show-current` and `git log --oneline -10`.
2. **GENERATE:**
    - Create/update the **Session Context** using the conversation history.
    - Preserve the **Project Description**; change it only if its enduring description is stale.
3. **MERGE:**
    - For lists and logs, **append** new entries; do not remove existing ones unless they are superseded.
4. **WRITE:**
    - Write the resume summary to `.astrolabe/CONTEXT.md`. Update PROJECT.md only for an actual description change.
5. **CONFIRM:**
    - Confirm both files are updated and provide a brief summary of the current project status.

## Reading These Files (For Future Sessions)

When a session starts, these files are automatically injected into your context. Use them to:
- Understand the project purpose (`PROJECT.md`) and recent progress (`CONTEXT.md` and `HISTORY.md`).
- Identify where the last session left off (`CONTEXT.md`).
- Avoid asking the user for context that is already recorded.

## Red Flags

**Stop and refactor when you see:**
- `CONTEXT.md` missing required resume sections.
- Information being lost during the "merge" phase.
- Vague "Current State" descriptions that don't help a new agent resume work.
- Run progress being written into `PROJECT.md`.
