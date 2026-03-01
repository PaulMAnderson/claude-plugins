---
phase: 5
title: Auto-compression at RPI phase boundaries
context-budget: medium
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md
  - plugins/rpi-plan-and-execute/skills/starting-an-implementation-plan/SKILL.md
  - plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md
depends-on: [phase_1, phase_4]
---

# Phase 5: Auto-Compression at Phase Boundaries

## Acceptance Criteria
- rpi-context-engineering.AC3.4 and AC3.5

## Context

The two phase-boundary moments in the RPI workflow where context is currently discarded:
1. **Design → Plan**: end of `starting-a-design-plan` Phase 6 (Planning Handoff)
2. **Plan → Execute**: end of `starting-an-implementation-plan` final handoff

Both skills already tell users to `/clear`. We insert compression immediately before
the `/clear` instruction so session state is saved to `.rpi/CONTEXT.md`.

## Tasks

### Task 5.1 — Update starting-a-design-plan Phase 6

In `plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md`, find Phase 6:
"Planning Handoff". The current text starts with "Do NOT create implementation plan directly."

**Insert the following block BEFORE the existing Phase 6 text:**

```markdown
### Pre-Handoff: Compress Context

Before clearing context, preserve this session's state.

**REQUIRED:** Use your Skill tool to invoke `compressing-context`.

The skill will write a structured summary to `.rpi/CONTEXT.md`. This file persists
across `/clear` and lets the implementation-planning session resume without re-investigation.

Wait for the skill to confirm `.rpi/CONTEXT.md` has been written before proceeding.
```

### Task 5.2 — Update starting-an-implementation-plan final handoff

In `plugins/rpi-plan-and-execute/skills/starting-an-implementation-plan/SKILL.md`,
find the "Execution Handoff" or final `/clear` instruction section.

**Insert the following block BEFORE the existing /clear instruction:**

```markdown
### Pre-Handoff: Compress Context

Before clearing context, preserve this session's implementation planning state.

**REQUIRED:** Use your Skill tool to invoke `compressing-context`.

Ensure the summary captures:
- Which phase files were created and their paths
- Any architectural decisions made during planning
- The absolute path to the plan directory (critical for the execute command)

Wait for the skill to confirm `.rpi/CONTEXT.md` has been written before proceeding.
```

### Task 5.3 — Update the execution handoff commands to note CONTEXT.md

In both skills, after the `/clear` instruction, add a note that the next session
should check for `.rpi/CONTEXT.md` before re-investigating:

```markdown
**Note:** `.rpi/CONTEXT.md` has been written. The next session will automatically
read it to restore context about what was accomplished.
```

## Done When
- Both skill files contain a pre-handoff compression step that invokes `compressing-context`
- The compression step occurs before the `/clear` instruction in both skills
- The compress step instructs the agent to wait for confirmation that `.rpi/CONTEXT.md` was written
