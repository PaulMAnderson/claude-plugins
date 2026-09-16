---
phase: 4
title: Compression skill and /compress-context command
context-budget: small
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - plugins/rpi-plan-and-execute/skills/using-plan-and-execute/SKILL.md
depends-on: [phase_1]
---

# Phase 4: Compression Skill & Command

## Acceptance Criteria
- rpi-context-engineering.AC3.1 through AC3.3

## Tasks

### Task 4.1 — Create compressing-context skill

Create `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md`:

```markdown
---
name: compressing-context
description: Use when context window is filling up, at RPI phase boundaries, or when the context monitor hook fires — produces an Anchored Iterative Summary written to .rpi/CONTEXT.md that preserves session state across /clear
user-invocable: true
---

# Compressing Context

## Overview

Produce an Anchored Iterative Summary of this session and write it to `.rpi/CONTEXT.md`.
This file persists across `/clear` and is read at the start of the next session to restore
the essential context an agent needs to continue.

**Announce at start:** "I'm using the compressing-context skill to summarise this session."

## Core Technique: Anchored Iterative Summarization

Do NOT regenerate from scratch each time. If `.rpi/CONTEXT.md` already exists, read it
first and MERGE new information into each section rather than replacing. This prevents
information drift across multiple compression cycles.

## Sections (Required — all must be present)

### Session Intent
What is the user ultimately trying to accomplish in this project/session?
Write 2–4 sentences. Be concrete, not generic ("Implementing the rpi-context-engineering
design plan — Phase 3 of 6" not "Working on the project").

### Files Modified
List every file created or changed in this session with a one-line description of the change.
Format:
```
- path/to/file.ts: Added JWT validation function
- path/to/other.md: Created design plan document
```

If merging with existing .rpi/CONTEXT.md, add new files; do not remove old ones.

### Decisions Made
List significant decisions made in this session with brief rationale.
Format:
```
- [Decision]: [Rationale]
```
Example:
```
- Used tool-call count as proxy for token count: No direct token API access from hook scripts
- No matcher on PostToolUse hook: Should fire after every tool, not just specific ones
```

### Current State
Describe exactly where we are. What is passing? What is failing? What phase are we on?
Be precise enough that an agent reading this could resume without re-investigation.

### Next Steps
Number the immediate next actions, in order.
Format:
```
1. [Specific next action]
2. [Action after that]
```

## Process

1. **Read existing `.rpi/CONTEXT.md`** if present (use Read tool). Note what's already there.
2. **Generate the summary** section by section using the conversation history and your tool call history.
3. **Merge** — for Files Modified and Decisions Made, append; do not remove existing entries.
4. **Write** the result to `.rpi/CONTEXT.md` (use Write tool, overwrite the whole file).
5. **Confirm** by reading back the file and reporting its word count.

## Output Format

The file must follow this exact structure:

```markdown
# Session Context

_Last updated: [timestamp or phase/task reference]_

## Session Intent
[2-4 sentences]

## Files Modified
- [path]: [description]

## Decisions Made
- [Decision]: [Rationale]

## Current State
[Precise description]

## Next Steps
1. [Next action]
2. [Action after]
```

## Reading This File (For Future Sessions)

When a session starts and `.rpi/CONTEXT.md` exists, read it immediately. It tells you:
- What the user is trying to accomplish (Session Intent)
- What has already been done (Files Modified, Decisions Made)
- Exactly where to pick up (Current State, Next Steps)

Do not ask the user to re-explain context if this file is present and recent.
```

### Task 4.2 — Create compress-context command

Create `plugins/rpi-plan-and-execute/commands/compress-context.md`:

```markdown
---
description: Compress session context to .rpi/CONTEXT.md using Anchored Iterative Summarization
---

Use your Skill tool to engage the `compressing-context` skill. Follow it exactly as written.
```

## Done When
- `skills/compressing-context/SKILL.md` exists with all five required sections defined
- `commands/compress-context.md` exists and invokes the skill
- Running `/compress-context` in Claude Code invokes the compressing-context skill
