---
name: writing-implementation-plans
description: Use when design is complete and you need detailed implementation tasks for engineers with zero codebase context - creates comprehensive implementation plans with exact file paths, complete code examples, and verification steps assuming engineer has minimal domain knowledge
user-invocable: false


## Overview

Write comprehensive implementation plans for engineers with zero context. Document which files to touch, code examples, testing, and verification steps. Use bite-sized tasks, DRY, and YAGNI principles. Assume the engineer is skilled but unfamiliar with the domain.

**Announce at start:** "I'm using the writing-implementation-plans skill to create the implementation plan."

**Save plans to:** `docs/implementation-plans/YYYY-MM-DD-<feature-name>/phase_##.md`

## Critical: Design Plans Provide Direction, Not Code

**Design plans are intentionally high-level.** They describe components, modules, and contracts — not implementation code. This is by design.

**You MUST generate code fresh based on codebase investigation.** Do NOT copy code from the design document. Even if a design plan contains code examples (it shouldn't, but some might), treat them as illustrative only.

**Why this matters:**
- Design plans may be days or weeks old
- Codebase state changes between design and implementation
- Investigation reveals actual patterns, dependencies, and constraints
- Your code must work with the codebase as it exists NOW



## Before Starting

**REQUIRED: Verify scope and codebase state**


### 1. Scope Validation

Count the phases/tasks in the design plan.

**If design plan has >8 phases:** STOP. Refuse to proceed.

Tell the user:
"This design has [N] phases, which exceeds the 8-phase limit for implementation plans. Please rerun this skill with a scope of no more than 8 phases. You can:
1. Select the first 8 phases for this implementation plan
2. Break the design into multiple implementation plans
3. Simplify the design to fit within 8 phases"

**If already implementing phases 9+:** The user should provide the previous implementation plan as context when scoping the next batch.


### 2. Review Mode Selection

**After scope validation, ask how to handle phase reviews:**

Use AskUserQuestion:
```
Question: "How would you like to review the implementation plan phases?"
Options:
  - "Write all phases to disk, I'll review afterwards"
  - "Review each phase interactively before writing"
```


### 3. Codebase Verification

Dispatch `codebase-investigator` before EACH phase with design assumptions. Read REFERENCE.md for full guidance and NEVER/ALWAYS write rules.

**DO NOT verify codebase yourself.**

### 4. External Dependency Research

Dispatch `internet-researcher` (docs) or `remote-code-researcher` (internals). Read REFERENCE.md for tier framework.

## Phase-by-Phase Implementation

**Step 0: Task tracker with dependencies**

For each phase, capture absolute paths DESIGN_PATH and PLAN_DIR, then create:

```markdown
- [ ] Phase NA: Read [Phase Name] from {DESIGN_PATH}
- [ ] Phase NB: Investigate codebase for Phase N and activate relevant skills
- [ ] Phase NC: Research external deps (Phase N)
- [ ] Phase ND: Write {PLAN_DIR}/phase_0N.md
```

Set dependencies: NA ← (N-1)D, NB ← NA, NC ← NB, ND ← NC.

**VERBATIM TASK NAMES.** The phrase "and activate relevant skills" is critical.

**After all phases:** Finalization task (blocked by all *D tasks) to run code-reviewer.

**Include Acceptance Criteria from design plan.** For each phase, identify which ACs it implements. Ensure tasks produce tests verifying each AC.

## Requirements Checklist

**Before starting:**
- [ ] Count phases - refuse if >8
- [ ] Ask user for review mode (batch vs interactive)
- [ ] Capture absolute paths: DESIGN_PATH and PLAN_DIR
- [ ] Read Acceptance Criteria section from design plan
- [ ] Create granular task list with TaskCreate (NA, NB, NC, ND per phase + Finalization + Test Requirements)
- [ ] Set up dependencies with TaskUpdate addBlockedBy (see Step 0)
- [ ] Task descriptions include absolute paths (not relative)

**For each phase (tasks NA through ND):**
- [ ] **Task NA:** Mark in_progress, read `<!-- START_PHASE_N -->` from design, mark completed
- [ ] **Task NB:** Mark in_progress, dispatch codebase-investigator, review findings, mark completed
- [ ] **Task NC:** Mark in_progress, research external deps if needed (or mark completed with "N/A"), mark completed
- [ ] Write complete tasks with exact paths and code based on investigator and research findings
- [ ] **If interactive mode:** Output complete phase plan, use AskUserQuestion for approval
- [ ] **Task ND:** Mark in_progress, write to absolute path in task description, mark completed

**For each task in the plan:**
- [ ] Exact file paths with line numbers for modifications
- [ ] Complete code - zero TODOs, zero unresolved questions in comments
- [ ] Every code example runs immediately without implementation decisions
- [ ] If code references helpers/utilities, prior task creates them
- [ ] Exact commands with expected output
- [ ] No conditional instructions ("if exists", "if needed")

**Finalization (after all phase ND tasks completed):**
- [ ] Mark Finalization task as in_progress
- [ ] Dispatch code-reviewer to validate plan against design
- [ ] Fix ALL issues including Minor ones
- [ ] Re-run code-reviewer until APPROVED with zero issues
- [ ] Mark Finalization task as completed
- [ ] Proceed to Test Requirements

**Test Requirements (after Finalization):**
- [ ] Mark Test Requirements task as in_progress
- [ ] Dispatch Opus subagent to generate test requirements from Acceptance Criteria
- [ ] **If interactive mode:** Present to user, use AskUserQuestion for approval
- [ ] **If batch mode:** Write directly without asking
- [ ] Write test-requirements.md to PLAN_DIR
- [ ] Mark Test Requirements task as completed
- [ ] Proceed to execution handoff

## Common Rationalizations - STOP

These are violations of the skill requirements:

| Excuse | Reality |
|--------|---------|
| "File probably exists, I'll say 'update if exists'" | Use codebase-investigator. Write definitive instruction. |
| "Design mentioned this file, must be there" | Codebase changes. Use investigator to verify current state. |
| "I can quickly verify files myself" | Use codebase-investigator. Saves context and prevents hallucination. |
| "Design plan has code, I'll use that" | No. Design provides direction. Generate code fresh from codebase investigation. |
| "Design plan is recent, code should still work" | Codebase may have changed. Investigation is the source of truth, not the design. |
| "User can figure out if file exists during execution" | Your job is exact instructions. No ambiguity. |
| "Testing Phase 3 will fail but that's OK because it'll be fixed in Phase 4" | All phases must compile and pass tests before they conclude. |
| "Phase validation slows me down" | Going off track wastes far more time. Validate each phase. |
| "I'll batch all phases then validate at end" | Valid if user chose batch mode. Otherwise validate incrementally. |
| "I'll just ask for approval, user can see the plan" | Output complete plan in message BEFORE AskUserQuestion. User must see it. |
| "Plan looks complete enough to ask" | Show ALL tasks with ALL steps and code. Then ask. |
| "This plan has 12 phases but they're small" | Limit is 8 phases. No exceptions. Refuse and redirect. |
| "I can combine phases to fit in 8" | That's the user's decision, not yours. Refuse and explain options. |
| "Comment explains what needs to be done next" | Code comments aren't instructions. Code must run as-written. Create prior task for dependencies. |
| "Engineer will figure out the bootstrap approach" | No implementation questions in code. Resolve it now or create prerequisite task. |
| "Infrastructure tasks need TDD structure too" | No. Use infrastructure template. Verify operationally per design plan. |
| "I'll add tests to this config file task" | If design says "Done when: builds," don't invent tests. Honor the design. |
| "Functionality phase but design forgot tests" | Surface to user. Functionality needs tests. Design gap, not your call to skip. |
| "Plan looks complete, skip validation" | Always validate. Gaps found now are cheaper than gaps found during execution. |
| "Validation is overkill for simple plans" | Simple plans validate quickly. Complex plans need it more. Always validate. |
| "Finalization task is done, minor issues can wait" | NO. Task says "fix ALL issues including minor ones." Not done until zero issues. |
| "I'll skip creating granular tasks, one per phase is enough" | Granular tasks survive compaction. Create NA, NB, NC, ND per phase + Finalization. |
| "Dependencies are obvious, don't need addBlockedBy" | Task list shows blocked status. Set dependencies explicitly with TaskUpdate. |
| "Relative paths are fine in task descriptions" | After compaction, context is lost. Use absolute paths so tasks are self-contained. |
| "I'll paraphrase the task name, same meaning" | NO. Task names are VERBATIM. "and activate relevant skills" triggers behavior post-compaction. |
| "I know how this library works from training" | Research it. APIs change. Use internet-researcher for docs, remote-code-researcher for internals. |
| "Docs are probably accurate enough" | Usually yes. But if extending/customizing library behavior, verify with source code. |
| "I'll clone the repo to check the docs" | No. Use internet-researcher for docs. Only clone (remote-code-researcher) for source code investigation. |
| "Phase has external deps but I'll skip research" | Research is mandatory when phase involves external dependencies. Surface unknowns now. |
| "Test requirements can be generated during execution" | No. Test requirements must exist before execution starts. Code reviewer uses them. |
| "This type needs unit tests" | No. TypeScript compiler verifies types. Don't test what the compiler checks. |
| "Should test that this calls the dependency correctly" | No. Test behavior (the result), not wiring (how you called things). |
| "Dependency is used here, should verify it works" | No. Dependencies have their own tests. Test YOUR code's behavior. |
| "More tests = better coverage" | Wrong tests = noise. Test the ACs, nothing more. |
| "Phase doesn't have ACs but I'll add some tests anyway" | No. Explicitly state "Verifies: None" for infrastructure phases. Don't invent work. |
| "Acceptance Criteria are clear, don't need test requirements" | Test requirements map criteria to specific tests. Execution needs this mapping. |
| "I'll skip test requirements, user chose batch mode" | Batch mode skips interactive approval. Test requirements are still generated and written. |
| "Test requirements task is optional" | No. It's a tracked task with dependencies. Must complete before execution handoff. |

**All of these mean: STOP. Follow the requirements exactly.**


## Templates and Detailed Process

Read `plugins/rpi-plan-and-execute/skills/writing-implementation-plans/REFERENCE.md` for:
- Full codebase verification guidance (NEVER/ALWAYS write rules, dispatch examples)
- External dependency research tiers
- Task granularity guidance with examples
- Infrastructure vs Functionality task type details
- Phase file frontmatter format
- Plan Document Header template
- Task and Subcomponent Marker format with examples
- Infrastructure and Functionality task templates
- Finalization (code-reviewer dispatch) process
- Test Requirements generation process
- Execution Handoff instructions
- "When You Don't Know How to Proceed" — worked example
