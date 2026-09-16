---
description: Start a Backlog or Roadmap item by its planned ID
---

Use the shared project state contract in `${CLAUDE_PLUGIN_ROOT}/references/project-state.md`. The argument must name an exact `B` or `R` ID from `.astrolabe/PLANNED.md`. Read that item and the project context, then choose the appropriate Micro, Quick, Spec, or Design tier. Clarify scope if the item is too broad to execute. An explicit ID is authorization to start that item; do not ask whether to use it again.

Choose a stable work slug and run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/astrolabe-state.py" --root "$PWD" start-planned --id ID --tier TIER --work SLUG`. Carry the ID and original item text into the tier's intent, spec, or plan. Continue through the tier's normal verification and exit. Keep the item in `PLANNED.md` while work is active or paused.

After the tier has completed successfully, run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/astrolabe-state.py" --root "$PWD" complete-planned --id ID --outcome "VERIFIED OUTCOME" --artifact "PATH"` (`--artifact` is optional). This removes the item from `PLANNED.md` and records its ID, original text, outcome, and optional artifact in `HISTORY.md`. Do not complete an item merely because a design or phase is done when its requested outcome remains unfinished.
