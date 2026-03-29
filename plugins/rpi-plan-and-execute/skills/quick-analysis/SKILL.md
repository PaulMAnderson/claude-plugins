---
name: quick-analysis
description: Use for one-off data analysis tasks that don't require persistent design plans or multi-phase implementation - bypasses the formal RPI loop for speed
user-invocable: true
---

# Quick Analysis Workflow

## Overview

Use this skill for fast, single-session data analysis tasks. It bypasses the formal design and implementation plan requirements of the standard RPI loop.

**Announce at start:** "I'm using the quick-analysis skill to perform this one-off analysis."

## Mandatory Rules

1. **NO DESIGN DOCUMENTS:** Do not write design plans to `docs/design-plans/`.
2. **NO IMPLEMENTATION PLANS:** Do not write implementation plans to `docs/implementation-plans/`.
3. **IN-CONTEXT PLANNING ONLY:** If planning is needed, do it directly in the chat.
4. **READ CONTEXT:** If `.rpi/CONTEXT.md` or `.rpi/PROJECT.md` exist, read them to ensure the analysis aligns with the broader project.
5. **LOG OUTCOME:** On completion, append a 1-2 sentence outcome note to `.rpi/SESSION.md`.

## Process

1. **UNDERSTAND:** Clarify the analysis goal, the data source, and the required output (figure, table, stat).
2. **RESTORE CONTEXT:** Read `.rpi/` context files to ensure consistency with existing analysis patterns.
3. **IMPLEMENT:** Write and execute the analysis code directly. Use established house style patterns (e.g., NumPy vectorization, Matplotlib OO API).
4. **VERIFY:** Confirm the results are correct and the output matches the request.
5. **LOG:** Append the result/outcome to `.rpi/SESSION.md`.

## Example Log Entry

```markdown
- **Quick Analysis [timestamp]**: Computed mean evoked response for session 12; found significant (p<0.01) increase in alpha power during task.
```

## When NOT to Use

- The task requires multiple sessions to complete.
- The task affects critical project architecture.
- The user explicitly asks for a formal design or peer review.
