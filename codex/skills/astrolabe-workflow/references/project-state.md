# Local project state for Codex tiers

Use the shared format in repository-root `docs/astrolabe-state-format.md`. The standard-library helper is `../scripts/project_state.py` relative to this reference (resolve it to an absolute path before executing). It operates in any local project without registration, credentials, network, or service.

Entry for every tier: run `python3 HELPER --root PROJECT init`; read `.astrolabe/PROJECT.md`, `STATUS.md`, and `PLANNED.md` in full. Compare the user's request with both Backlog and Roadmap prose. If a matching item exists and the user did not already name its ID, show its ID/text and ask whether to work on it, extend it, or proceed separately; wait for the user's choice. If none matches, proceed without an extra decision. Choose a lowercase hyphenated slug and run `python3 HELPER --root PROJECT enter --tier TIER --work SLUG`.

Exit: run `python3 HELPER --root PROJECT finish --tier TIER --work SLUG --intent "INTENT" --outcome "OUTCOME"` after completion. It updates STATUS.md and appends HISTORY.md. Use `--status paused` for incomplete work. Keep Micro/Quick outcomes short and Full outcomes tied to plan/phase evidence. If out-of-scope work arises, offer Backlog (concrete) or Roadmap (longer-term). Only after the user chooses, run `python3 HELPER --root PROJECT add-planned --list backlog --text "IDEA"` or `--list roadmap`; a decline leaves PLANNED.md unchanged.

Spec uses `spec-start`, `spec-step`, `spec-note`, and `spec-done` on the same helper. `spec-done` records history and status itself; do not also call `finish`.

## Planned-item lifecycle

For an explicit planned ID, read its exact text, choose the existing tier, and run `python3 HELPER --root PROJECT start-planned --id ID --tier TIER --work SLUG` (substitute the helper path and project root above). This records the association in HISTORY.md and keeps the item in PLANNED.md. Carry the ID and original text into the tier artifact. On pause, leave the planned item in place. After the requested outcome and tier verification are complete, run the tier exit command (`spec-done` for Spec), then `python3 HELPER --root PROJECT complete-planned --id ID --outcome "VERIFIED OUTCOME" --artifact "PATH"`; artifact is optional. Completion removes the item from PLANNED.md and appends its ID, original text, outcome, and artifact to HISTORY.md. A finished design or phase does not close an item whose requested outcome is still pending. Completed IDs remain reserved.
