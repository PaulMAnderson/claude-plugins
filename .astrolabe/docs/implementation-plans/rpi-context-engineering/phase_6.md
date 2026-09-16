---
phase: 6
title: CE memory tier template upgrades for design and implementation plan files
context-budget: medium
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - plugins/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md
  - plugins/rpi-plan-and-execute/skills/writing-implementation-plans/SKILL.md
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
depends-on: [phase_1]
---

# Phase 6: CE Memory Tier Template Upgrades

## Acceptance Criteria
- rpi-context-engineering.AC4.1 through AC4.4

## Context

The goal is to add CE memory-tier awareness to generated documents so that future agents
know WHAT to read and in WHAT order when context is limited. This design doc itself is
the reference implementation — it contains the Memory Tier Index in action.

## Tasks

### Task 6.1 — Update writing-design-plans skill: add Memory Tier Index instruction

In `plugins/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md`, find the section
that describes document structure (the part listing which sections to write). After the
instruction to write the Summary section, add:

```markdown
#### Memory Tier Index (write immediately after Summary)

After writing the Summary, add a Memory Tier Index table. This is a map that tells
future agents what to read first when context is limited.

Standard mapping for all design plans:

```markdown
## 🗂 Memory Tier Index

| Tier | Sections | When to read |
|------|----------|-------------|
| 🔴 **HOT** | DoD, Acceptance Criteria | Always — load before doing anything |
| 🟡 **WARM** | Architecture, File Map, Implementation Phases | When planning or implementing a specific phase |
| 🔵 **COLD** | Background, Alternatives Considered, Glossary | Reference on demand only |
```

Customise the Warm and Cold rows if this design plan has unusual sections.
```

### Task 6.2 — Update writing-design-plans skill: annotate section headings

In the same skill, find the instructions for writing each major section heading.
Prepend each heading instruction with its tier emoji:

- Definition of Done → `## 🔴 Definition of Done`
- Acceptance Criteria → `## 🔴 Acceptance Criteria`
- Architecture → `## 🟡 Architecture`
- File Map → `## 🟡 File Map`
- Implementation Phases → `## 🟡 Implementation Phases`
- Background → `## 🔵 Background`
- Alternatives Considered → `## 🔵 Alternatives Considered`
- Glossary → `## 🔵 Glossary`

Add a note: "The tier emoji is informational — it signals to future agents how
urgently they need to read this section. Do not explain the emoji in the document body;
the Memory Tier Index at the top provides the legend."

### Task 6.3 — Update writing-implementation-plans skill: add context-budget frontmatter

In `plugins/rpi-plan-and-execute/skills/writing-implementation-plans/SKILL.md`, find
the instruction for creating individual phase files. Add the following to the phase file
template:

```markdown
Each phase file MUST begin with YAML frontmatter:

```yaml
---
phase: N
title: [Short descriptive title]
context-budget: [small | medium | large]
files-required:
  - [absolute or repo-relative path to each file the executor must load]
depends-on: [list of phase_N dependencies, or empty list]
---
```

**How to estimate context-budget:**
- `small`: Phase touches 1–3 files, tasks are straightforward edits or new file creation
- `medium`: Phase touches 4–8 files or requires reading large skill files for context
- `large`: Phase involves bulk operations (many files), complex logic, or extensive investigation

**files-required guidance:**
List every file the executing agent MUST read to complete this phase. Include:
- The design plan document (always)
- Files being modified (so the agent loads current content)
- Files being used as patterns/references
Do NOT list files the agent might optionally read. Be selective — this is the minimum required set.
```

### Task 6.4 — Update writing-implementation-plans skill: add SessionStart context hint

Add an instruction to the skill that the first phase file (phase_1.md) should always
include a reference to the design plan path in its `files-required`, and that the
`session-start.sh` hook will inject the `using-plan-and-execute` skill — so the
executor doesn't need to re-explain the workflow from scratch.

## Done When
- `writing-design-plans` skill produces a Memory Tier Index after the Summary
- `writing-design-plans` skill annotates section headings with tier emojis (🔴/🟡/🔵)
- `writing-implementation-plans` skill produces phase files with YAML frontmatter including `context-budget` and `files-required`
- A newly generated design doc (manual test) contains the Memory Tier Index table
- A newly generated implementation phase file (manual test) contains the YAML frontmatter block
