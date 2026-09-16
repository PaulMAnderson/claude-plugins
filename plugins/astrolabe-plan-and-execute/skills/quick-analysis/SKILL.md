---
name: quick-analysis
description: One-off analysis or investigation bypassing the full Astrolabe planning loop
user-invocable: true
---

# Quick Analysis Workflow

## Project state (required)

Follow [the shared project state entry and exit contract](../../references/project-state.md) before and after this skill. Use tier `quick`. Initialize missing files, read `PROJECT.md` and `STATUS.md`, and consult `PLANNED.md` before work. Record the actual outcome in `HISTORY.md` and update `STATUS.md` on exit.

## Overview

Use this skill for fast, single-session data analysis tasks. It bypasses the formal design and implementation plan requirements of the standard Astrolabe loop.

**Announce at start:** "I'm using the quick-analysis skill to perform this one-off analysis."

## Mandatory Rules

1. **NO DESIGN DOCUMENTS:** Do not write design plans to `.astrolabe/docs/design-plans/`.
2. **NO IMPLEMENTATION PLANS:** Do not write implementation plans to `.astrolabe/docs/implementation-plans/`.
3. **IN-CONTEXT PLANNING ONLY:** If planning is needed, do it directly in the chat.
4. **READ CONTEXT:** Follow the project state entry contract and read `.astrolabe/CONTEXT.md` if present.
5. **LOG OUTCOME:** On completion, use the project state exit contract to append a 1-2 sentence outcome note to `.astrolabe/HISTORY.md` and update `STATUS.md`.

## Process

1. **UNDERSTAND:** Clarify the analysis goal, the data source, and the required output (figure, table, stat).
2. **RESTORE CONTEXT:** Read `.astrolabe/` context files to ensure consistency with existing analysis patterns.
3. **IMPLEMENT:** Write and execute the analysis code directly. Use established house style patterns (e.g., NumPy vectorization, Matplotlib OO API).
4. **VERIFY:** Confirm the results are correct and the output matches the request.
5. **LOG:** Append the result/outcome to `.astrolabe/HISTORY.md` and update `STATUS.md`.

## Example Log Entry

```markdown
- **Quick Analysis [timestamp]**: Computed mean evoked response for session 12; found significant (p<0.01) increase in alpha power during task.
```

If this work needs a resumable written checklist, invoke `starting-a-tracked-task` for the Spec tier.

## When NOT to Use

- The task requires multiple sessions to complete.
- The task affects critical project architecture.
- The user explicitly asks for a formal design or peer review.
