---
name: helper-function
description: Add a single helper function or small utility, bypassing the RPI loop
user-invocable: true
---

# Helper Function Workflow

## Overview

Use this skill for fast, single-session helper function development. It bypasses the formal design and implementation plan requirements of the standard RPI loop.

**Announce at start:** "I'm using the helper-function skill to develop this utility."

## Mandatory Rules

1. **NO DESIGN DOCUMENTS:** Do not write design plans to `docs/design-plans/`.
2. **NO IMPLEMENTATION PLANS:** Do not write implementation plans to `docs/implementation-plans/`.
3. **IN-CONTEXT INTENT:** State a 2-3 bullet point "Intent" in the chat before implementation.
4. **USE SONNET FOR SUBAGENTS:** Instruct all spawned subagents (implementation, testing, review) to use the **Sonnet** model.
5. **READ CONTEXT:** If `.rpi/CONTEXT.md` or `.rpi/PROJECT.md` exist, read them.
6. **LOG INTENT AND OUTCOME:** Append both intent and outcome to `.rpi/SESSION.md`.

## Process

1. **UNDERSTAND:** Clarify the function's purpose, inputs, and outputs.
2. **RESTORE CONTEXT:** Read `.rpi/` context files.
3. **PLAN:** Share 2-3 bullet points of the implementation plan in the chat.
4. **IMPLEMENT:** Develop the function. Call subagents with: "Execute this task using the Sonnet model."
5. **TEST:** Verify the function works with appropriate tests (e.g., `pytest`).
6. **LOG:** Append intent and outcome to `.rpi/SESSION.md`.

## Example Log Entry

```markdown
- **Helper Function [timestamp]**: 
    - **Intent**: Added `normalize_signal` function to `data_utils.py` to handle [channels, time] arrays.
    - **Outcome**: Function implemented and tested with 5 edge cases (NaNs, empty arrays, wrong shapes); all tests pass.
```

## When NOT to Use

- The task requires multiple sessions to complete.
- The task affects critical project architecture.
- The user explicitly asks for a formal design or peer review.
