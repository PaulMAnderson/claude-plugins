# Project tracking human test plan

## Automated coverage executed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s codex/tests -v`: 21 tests passed. Covers init preservation, history append, planned IDs, Spec lifecycle, STATUS schema, three local distributions, Codex installer, and ledger behavior.
- `bash tests/verify-journaling.sh`: passed; checks two history entries survive repeat initialization and STATUS shows latest work.
- JSON/TOML and path checks: all eight Claude marketplace sources and manifests, eight Gemini extension manifests, Gemini commands, and 13 Codex skill dry-run entries validated.
- Active old-path/name sweep and staged diff whitespace check: passed. Historical design documents and changelog deliberately retain former names.

## Operational checks executed

- Claude session hook produced parseable JSON using `.astrolabe/PROJECT.md` and `CONTEXT.md`.
- `astrolabe-workspace` returned `.astrolabe/exec`; `task-brief` extracted the current task.
- All three state helper copies ran init, enter, and finish in fresh local fixture directories without registration, credentials, or network access.

## Pending human checks

Use a disposable local project for each check. Keep its files if you want to inspect them, or delete that disposable fixture afterward.

1. **External skill loading (AC1, AC6):** Install this branch into Claude Code, Codex, and Gemini CLI through each documented installer. List or invoke the new Astrolabe names and Spec tier. Expect the eight renamed Claude/Gemini plugin or extension names and 13 Codex skills; no removed `rpi-*` skill should be offered by this branch. This has not been executed in those CLIs.
2. **Planned match (AC4.3):** In a fixture project, put `- B1: Add CSV import` under `## Backlog`; request a CSV importer through each tier. Expect the agent to show B1 and ask whether to work on it, extend it, or proceed separately before implementation.
3. **No match and decline (AC4.4–AC4.5):** Request unrelated work and confirm the tier proceeds without an extra planned-item decision. Later surface an out-of-scope idea, decline the offer to add it, and confirm PLANNED.md is byte-for-byte unchanged.
4. **Spec escalation (AC3.4):** Create an in-progress Spec, check one step, and add a note. Ask for architecture alternatives and full acceptance criteria. Expect a handoff to the design tier using the existing spec as context, with the checked step and note intact.
5. **Local portability (AC6):** Repeat one tier run in each CLI with networking unavailable and no Hypercube registration. Expect STATUS.md and HISTORY.md to update locally.

`tests/verify-hot-cold.sh` still fails for a TypeScript skill that was already absent at the execution baseline; it is unrelated to this project-tracking change.
