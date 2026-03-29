---
phase: 5
title: Tiered Workflow Entry Points
context-budget: medium
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/commands/start-design-plan.md
depends-on: [phase_04.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Provide lightweight alternatives to the full RPI loop for smaller tasks like one-off analyses or single helper functions.

**Architecture:** This phase adds two new slash commands (`/quick-analysis` and `/helper-function`) and their corresponding skills. These entry points bypass the formal design/implementation document requirements of the full RPI loop, focusing on speed and in-context planning while still maintaining a session log in `.rpi/SESSION.md`.

**Tech Stack:** Markdown (Commands & Skills).

**Scope:** Phase 5 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC5: Tiered Workflow Entry Points
- **rpi-datasci.AC5.1 Success:** `/quick-analysis` command exists; invoking it loads `quick-analysis` skill; skill writes a brief outcome note to `.rpi/SESSION.md` on completion
- **rpi-datasci.AC5.2 Success:** `/helper-function` command exists; invoking it loads `helper-function` skill; skill produces an in-context plan before implementation; writes intent and outcome to `.rpi/SESSION.md`
- **rpi-datasci.AC5.3 Success:** `helper-function` skill instructs spawned subagents to use Sonnet model
- **rpi-datasci.AC5.4 Failure:** Either new skill invokes a design-doc or implementation-plan file write (these are single-session, no persistent plan artifacts)

---

<!-- START_SUBCOMPONENT_A (tasks 1-2) -->
<!-- START_TASK_1 -->
### Task 1: Implement Quick Analysis Workflow

**Verifies:** rpi-datasci.AC5.1, rpi-datasci.AC5.4

**Files:**
- Create: `plugins/rpi-plan-and-execute/commands/quick-analysis.md`
- Create: `plugins/rpi-plan-and-execute/skills/quick-analysis/SKILL.md`

**Implementation:**
- `commands/quick-analysis.md`: Simple command document instructing the agent to use the `quick-analysis` skill.
- `skills/quick-analysis/SKILL.md`:
  - Instructions for zero-plan execution.
  - Requirement to read `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` if present.
  - Direct implementation of the analysis task.
  - Requirement to append a brief outcome note (1-2 sentences) to `.rpi/SESSION.md` upon completion.
  - Explicit instruction NOT to create design docs or implementation plans.

**Verification:**
Run: `/quick-analysis` (mock)
Expected: Skill is loaded, task is executed, and `.rpi/SESSION.md` is updated.

**Commit:** `feat(workflow): add quick-analysis entry point`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Implement Helper Function Workflow

**Verifies:** rpi-datasci.AC5.2, rpi-datasci.AC5.3, rpi-datasci.AC5.4

**Files:**
- Create: `plugins/rpi-plan-and-execute/commands/helper-function.md`
- Create: `plugins/rpi-plan-and-execute/skills/helper-function/SKILL.md`

**Implementation:**
- `commands/helper-function.md`: Simple command document instructing the agent to use the `helper-function` skill.
- `skills/helper-function/SKILL.md`:
  - Instructions for lightweight planning.
  - Requirement to produce a 2-3 bullet point "Intent" in the chat before implementation.
  - Requirement to use Sonnet model for any spawned subagents (implementation, testing, review).
  - Direct implementation and testing of the function.
  - Requirement to append both intent and outcome to `.rpi/SESSION.md`.
  - Explicit instruction NOT to create design docs or implementation plans.

**Verification:**
Run: `/helper-function` (mock)
Expected: Skill is loaded, intent is shared, function is implemented using Sonnet subagents, and `.rpi/SESSION.md` is updated.

**Commit:** `feat(workflow): add helper-function entry point`
<!-- END_TASK_2 -->
<!-- END_SUBCOMPONENT_A -->
