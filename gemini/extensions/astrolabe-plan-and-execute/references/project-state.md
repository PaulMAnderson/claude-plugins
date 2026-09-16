# Shared project state entry and exit

The canonical file contract is `docs/astrolabe-state-format.md` in the Astrolabe source repository. Use `gemini/extensions/astrolabe-plan-and-execute/scripts/astrolabe-state.py` for local state writes. It needs only Python 3 and the project path.

At entry, before planning or implementation:

1. Run `python3 "<extension-root>/scripts/astrolabe-state.py" --root "$PWD" init` in the project root. This preserves existing files.
2. Read `.astrolabe/PROJECT.md`, `.astrolabe/STATUS.md`, and `.astrolabe/PLANNED.md` in full. Check Backlog and Roadmap against the user's request using judgment. If an item matches and the user did not already name its ID, show its ID and text and ask whether to work on it, extend it, or proceed separately; wait for the answer. If none matches, continue.
3. Choose a lowercase hyphenated work slug. Run `python3 "<extension-root>/scripts/astrolabe-state.py" --root "$PWD" enter --tier TIER --work SLUG` with `TIER` set by the calling skill. Re-read `STATUS.md` to confirm the current work.

On completion, run `python3 "<extension-root>/scripts/astrolabe-state.py" --root "$PWD" finish --tier TIER --work SLUG --intent "INTENT" --outcome "OUTCOME"`. The command replaces the live `STATUS.md` snapshot and appends an entry to `HISTORY.md`. Make the outcome short for Micro and Quick; include plan/phase evidence for Design. For paused work, pass `--status paused` and describe the actual state; do not call incomplete work completed.

If the work reveals an out-of-scope idea, offer to add it under Backlog (concrete work) or Roadmap (longer-term idea). Add it only if the user chooses a list. Run `python3 "<extension-root>/scripts/astrolabe-state.py" --root "$PWD" add-planned --list backlog --text "IDEA"` (or `--list roadmap`). The helper uses the next unused stable ID. A decline leaves `PLANNED.md` unchanged.

In Gemini, locate the extension root from this skill path. Use `ask_user` for a matching planned item and `write_todos` for ongoing steps.

## Planned-item lifecycle

For an explicit planned ID, read its exact text, choose the existing tier, and run `python3 HELPER --root PROJECT start-planned --id ID --tier TIER --work SLUG` (substitute the helper path and project root above). This records the association in HISTORY.md and keeps the item in PLANNED.md. Carry the ID and original text into the tier artifact. On pause, leave the planned item in place. After the requested outcome and tier verification are complete, run the tier exit command (`spec-done` for Spec), then `python3 HELPER --root PROJECT complete-planned --id ID --outcome "VERIFIED OUTCOME" --artifact "PATH"`; artifact is optional. Completion removes the item from PLANNED.md and appends its ID, original text, outcome, and artifact to HISTORY.md. A finished design or phase does not close an item whose requested outcome is still pending. Completed IDs remain reserved.
