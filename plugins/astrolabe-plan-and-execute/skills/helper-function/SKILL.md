---
name: helper-function
description: Add a single helper function or small utility, bypassing the Astrolabe loop
user-invocable: true
---

# Helper Function Workflow

## Project state (required)

Follow [the shared project state entry and exit contract](../../references/project-state.md) before and after this skill. Use tier `micro`. Initialize missing files, read `PROJECT.md` and `STATUS.md`, and consult `PLANNED.md` before work. Record the actual outcome in `HISTORY.md` and update `STATUS.md` on exit.

## Overview

Use this skill for fast, single-session helper function development. It bypasses the formal design and implementation plan requirements of the standard Astrolabe loop.

**Announce at start:** "I'm using the helper-function skill to develop this utility."

## Mandatory Rules

1. **NO DESIGN DOCUMENTS:** Do not write design plans to `.astrolabe/docs/design-plans/`.
2. **NO IMPLEMENTATION PLANS:** Do not write implementation plans to `.astrolabe/docs/implementation-plans/`.
3. **IN-CONTEXT INTENT:** State a 2-3 bullet point "Intent" in the chat before implementation.
4. **USE SONNET FOR SUBAGENTS:** Instruct all spawned subagents (implementation, testing, review) to use the **Sonnet** model.
5. **READ CONTEXT:** Follow the project state entry contract and read `.astrolabe/CONTEXT.md` if present.
6. **LOG INTENT AND OUTCOME:** Use the project state exit contract to append to `.astrolabe/HISTORY.md`.

## Process

1. **UNDERSTAND:** Clarify the function's purpose, inputs, and outputs.
2. **RESTORE CONTEXT:** Initialize and read project state, then read `.astrolabe/CONTEXT.md` if present.
3. **PLAN:** Share 2-3 bullet points of the implementation plan in the chat.
4. **IMPLEMENT:** Develop the function. Call subagents with: "Execute this task using the Sonnet model."
5. **TEST:** Verify the function works with appropriate tests (e.g., `pytest`).
6. **LOG:** Append intent and outcome to `.astrolabe/HISTORY.md` and update `STATUS.md`.

## Example Log Entry

```markdown
- **Helper Function [timestamp]**: 
    - **Intent**: Added `normalize_signal` function to `data_utils.py` to handle [channels, time] arrays.
    - **Outcome**: Function implemented and tested with 5 edge cases (NaNs, empty arrays, wrong shapes); all tests pass.
```

If this work needs a resumable written checklist, invoke `starting-a-tracked-task` for the Spec tier.

## When NOT to Use

- The task requires multiple sessions to complete.
- The task affects critical project architecture.
- The user explicitly asks for a formal design or peer review.
