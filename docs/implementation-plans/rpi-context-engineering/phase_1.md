---
phase: 1
title: Rebrand — rename directories and update all references
context-budget: large
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - .claude-plugin/marketplace.json
  - CHANGELOG.md
  - CLAUDE.md
depends-on: []
---

# Phase 1: Rebrand

## Acceptance Criteria
- rpi-context-engineering.AC1.1 through AC1.5

## Tasks

### Task 1.1 — Rename all plugin directories
Rename each `plugins/ed3d-*` directory to its `plugins/rpi-*` equivalent:

```
ed3d-00-getting-started  → rpi-getting-started
ed3d-basic-agents        → rpi-basic-agents
ed3d-extending-claude    → rpi-extending-claude
ed3d-hook-claudemd-reminder → rpi-hook-claudemd-reminder
ed3d-hook-skill-reinforcement → rpi-hook-skill-reinforcement
ed3d-house-style         → rpi-house-style
ed3d-plan-and-execute    → rpi-plan-and-execute
ed3d-playwright          → rpi-playwright
ed3d-research-agents     → rpi-research-agents
```

Use `git mv` for each so the rename is tracked properly.

### Task 1.2 — Update plugin.json name fields
In each renamed directory, open `.claude-plugin/plugin.json` and update the `"name"` field from `ed3d-*` to `rpi-*`.

### Task 1.3 — Update marketplace.json
In `.claude-plugin/marketplace.json`, update:
- The marketplace `name` from `ed3d-plugins` to `rpi-plugins`
- Every plugin entry: `name` field and `source` path from `ed3d-` to `rpi-`
- Retain all version numbers, descriptions, and author fields

### Task 1.4 — Update internal references in skill/command/agent/hook files
Run a search for `ed3d-` across all files under `plugins/` (after the directory renames). Update any remaining occurrences in:
- Skill SKILL.md files that reference other plugins by name (e.g. `ed3d-plan-and-execute:asking-clarifying-questions` → `rpi-plan-and-execute:asking-clarifying-questions`)
- Agent .md files that reference plugin-namespaced subagent types
- Hook scripts that reference plugin names

**DO NOT** update `.ed3d/` references — these are user project configuration directories and are explicitly out of scope.

### Task 1.5 — Update CLAUDE.md
In `CLAUDE.md`:
- Update heading `# ed3d-plugins` → `# rpi-plugins (Paul's RPI Fork)`
- Update all plugin name references from `ed3d-*` to `rpi-*`
- Update the Task invocation XML examples to use `rpi-*` subagent types

### Task 1.6 — Update CHANGELOG.md
Add a new entry at the top (after `# Changelog`):

```markdown
## [All plugins] Rebranded ed3d-* → rpi-*

Fork now ships as Paul Anderson's independent RPI plugin suite. All plugin names updated from `ed3d-` prefix to `rpi-` prefix. This is a breaking change for any marketplace or CLAUDE.md that references `ed3d-*` plugin names.

**Changed:**
- All 9 plugin directories renamed
- marketplace.json updated
- CLAUDE.md updated
- Internal cross-plugin references updated
```

### Task 1.7 — Update session-start.sh hook
In `plugins/rpi-plan-and-execute/hooks/session-start.sh`, update the path variable `PLUGIN_ROOT` reference and any hard-coded `ed3d-` strings.

### Task 1.8 — Verify
Run: `grep -r "ed3d-" plugins/ .claude-plugin/ CLAUDE.md`
Result must be zero matches. Any match is a bug to fix.

## Done When
`grep -r "ed3d-" plugins/ .claude-plugin/ CLAUDE.md` returns no results.
