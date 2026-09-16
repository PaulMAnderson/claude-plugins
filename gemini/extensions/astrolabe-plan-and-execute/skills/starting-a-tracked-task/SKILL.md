---
name: starting-a-tracked-task
description: Track a resumable task with a dated spec and numbered steps, without a full design plan
user-invocable: true
---

# Starting a Tracked Task

Use this tier when work needs a written intent and steps across sessions, but no architectural exploration or full acceptance-criterion plan.

## Entry

Follow [the shared project state entry contract](../../references/project-state.md): initialize local state, read PROJECT.md and STATUS.md, and check both PLANNED.md lists before proceeding. Use tier `spec`. If a matching planned item exists, show its ID with `ask_user` and ask whether to work on it, extend it, or proceed separately. Resume a matching in-progress spec if one exists; preserve its checked steps and notes.

## Work

Choose a lowercase hyphenated slug and record a short intent and numbered steps with `write_todos`. Run:

```sh
python3 "<extension-root>/scripts/astrolabe-state.py" --root "$PWD" spec-start --work SLUG --intent "INTENT" --step "FIRST STEP" --step "SECOND STEP"
```

The command creates `.astrolabe/docs/specs/YYYY-MM-DD-SLUG.md` with `status: in_progress`, `tier: spec`, intent, numbered checkboxes, and notes. An existing spec for the slug is resumed without replacing checked steps or notes. Read the file before acting. After completing and verifying each step, run `spec-step --work SLUG --number N` with the same script/root arguments. Record decisions and discoveries with `spec-note --work SLUG --text "NOTE"`. Keep incomplete steps unchecked. On a later invocation, read the same spec and continue the remaining steps.

## Exit and escalation

After all steps are checked and verified, run `spec-done --work SLUG --outcome "OUTCOME"` with the same script/root arguments. It marks the spec done, appends the intent and outcome to HISTORY.md, and updates STATUS.md. Do not also call `finish`; that would duplicate the history entry. If work pauses, leave the spec in progress and record the pause using the shared state exit contract with `--status paused`.

When the task needs architectural exploration, multiple approaches, or acceptance criteria, invoke `starting-a-design-plan` with this spec as context. Keep the prior spec and notes; do not discard completed steps. If an out-of-scope idea arises, offer to add it to Backlog or Roadmap through the shared contract.

Resolve `<extension-root>` from this skill file location before running a command.
