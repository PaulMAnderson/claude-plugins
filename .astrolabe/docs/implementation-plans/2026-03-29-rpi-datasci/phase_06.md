---
phase: 6
title: Model Tiering
context-budget: small
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/agents/code-reviewer.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/agents/task-bug-fixer.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/agents/task-implementor-fast.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/agents/test-analyst.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/skills/starting-an-implementation-plan/SKILL.md
depends-on: [phase_05.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Optimize model usage by tiering agents and skills, ensuring expensive Opus calls are reserved for high-reasoning tasks like design and planning, while Sonnet is used for implementation, review, and testing.

**Architecture:** This phase updates the frontmatter of agent definition files to specify the `sonnet` model where appropriate. It also adds documentation to the design and implementation planning skills to explicitly note when the `opus` model is recommended.

**Tech Stack:** Markdown (Agents & Skills).

**Scope:** Phase 6 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC6: Model Tiering
- **rpi-datasci.AC6.1 Success:** `code-reviewer.md`, `task-bug-fixer.md`, `test-analyst.md` agent files specify Sonnet as their model
- **rpi-datasci.AC6.2 Success:** `starting-a-design-plan` and `starting-an-implementation-plan` skill docs note that Opus is appropriate for design/planning phases
- **rpi-datasci.AC6.3 Failure:** Any implementation agent (`task-implementor-fast`, `code-reviewer`, `task-bug-fixer`, `test-analyst`) specifies Opus as its default model

---

<!-- START_SUBCOMPONENT_A (tasks 1-2) -->
<!-- START_TASK_1 -->
### Task 1: Update Agent Model Assignments

**Verifies:** rpi-datasci.AC6.1, rpi-datasci.AC6.3

**Files:**
- Modify: `plugins/rpi-plan-and-execute/agents/code-reviewer.md`
- Modify: `plugins/rpi-plan-and-execute/agents/task-bug-fixer.md`
- Modify: `plugins/rpi-plan-and-execute/agents/task-implementor-fast.md`
- Modify: `plugins/rpi-plan-and-execute/agents/test-analyst.md`

**Implementation:**
- Update the `model` field in the frontmatter of each file:
  - `code-reviewer.md`: `model: opus` -> `model: sonnet`
  - `task-bug-fixer.md`: `model: haiku` -> `model: sonnet`
  - `task-implementor-fast.md`: `model: haiku` -> `model: sonnet`
  - `test-analyst.md`: `model: opus` -> `model: sonnet`

**Verification:**
Run: `grep "model:" plugins/rpi-plan-and-execute/agents/*.md`
Expected: All four agents show `model: sonnet`.

**Commit:** `feat(agents): tier implementation agents to sonnet`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Update Skill Documentation for Model Rationale

**Verifies:** rpi-datasci.AC6.2

**Files:**
- Modify: `plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md`
- Modify: `plugins/rpi-plan-and-execute/skills/starting-an-implementation-plan/SKILL.md`

**Implementation:**
- Add a "Model Usage" or "Model Tiering" section (or note in Overview) explicitly stating: "The `opus` model is recommended for high-reasoning tasks like initial design, requirements gathering, and complex planning to ensure maximum architectural coherence."

**Verification:**
Check both skill files for the added note.

**Commit:** `docs(skills): document model tiering rationale for planning`
<!-- END_TASK_2 -->
<!-- END_SUBCOMPONENT_A -->
