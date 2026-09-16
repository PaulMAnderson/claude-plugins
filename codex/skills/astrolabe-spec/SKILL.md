---
name: "astrolabe-spec"
description: "Create or resume a dated tracked task with numbered steps, notes, and local project state."
---

# Tracked task

Follow [the shared entry contract](../astrolabe-workflow/references/project-state.md): initialize state, read PROJECT.md and STATUS.md, consult both PLANNED.md lists, and surface a matching item before starting. Use tier `spec` and a lowercase hyphenated slug.

Use the bundled `../astrolabe-workflow/scripts/project_state.py` helper (resolve relative to this skill file). Run `spec-start --work SLUG --intent "INTENT" --step "STEP"` with `--root PROJECT`; include one `--step` per numbered task. It creates `.astrolabe/docs/specs/YYYY-MM-DD-SLUG.md` with frontmatter, intent, checkboxes and notes, or resumes an in-progress spec without replacing content. Read the spec before work. After verifying a step, run `spec-step --work SLUG --number N`; use `spec-note --work SLUG --text "NOTE"` to preserve discoveries. On later invocations, resume the same spec and leave checked steps intact.

When every step is complete, run `spec-done --work SLUG --outcome "OUTCOME"`. It marks the spec done, appends HISTORY.md, and updates STATUS.md; do not call `finish` again. For a pause, use the shared `finish --status paused` flow and keep the spec in progress. If architecture, multiple approaches, or full acceptance criteria are needed, start [astrolabe-design](../astrolabe-design/SKILL.md) with this spec as context.
