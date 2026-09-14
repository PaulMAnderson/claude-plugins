# Execution mechanics

## Task brief and result

Extract the current task between its `START_TASK_N` / `END_TASK_N` markers, or read its bounded section directly. Supply the phase's exact AC text, binding contracts, touched interfaces, working directory, implementation guidance, and report destination. A task must not depend on another agent's conversation memory.

If delegation is authorized and available, assign disjoint files or use explicit isolation. The controller updates the ledger and integrates results. Otherwise execute locally with the same brief and report. Never invoke unavailable Claude Task types, assume a named model exists, or run nested CLI agents as a substitute for missing delegation permissions.

Write reports under `.rpi/runs/<slug>/reports/phase-N-task-M.md`:

- Status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
- Task, phase, ACs, working directory, baseline and tested revision/before-after file state.
- Changed files and observable behavior.
- Verification: command, cwd, exit code, relevant complete result, log path if large.
- TDD evidence where applicable, or why operational verification was appropriate.
- Concerns, unresolved decisions, or exact missing context.

`DONE` proceeds after the controller inspects the report and changes. `DONE_WITH_CONCERNS` requires adjudicating correctness/scope concerns now; observations can be logged. `NEEDS_CONTEXT` gets only the missing facts, then a revised attempt. `BLOCKED` requires a changed approach: investigate missing context, split an oversized task, or resolve a plan conflict. Never resubmit unchanged instructions and expect progress.

## Review package

Before the first task record the full phase-start SHA. For committed work inspect `git diff <phase-base> <current-head>` plus the commit list. For uncommitted work inspect `git diff <phase-base>` (staged and unstaged net changes), status, and new files. Read relevant untracked files explicitly: ordinary `git diff` omits them. Include binary/schema/generated changes using suitable inspection tools. Preserve snapshots of pre-existing edits so authorship/scope remains distinguishable.

Write a package/report with the actual baseline, current SHA and dirty status, file list, full diff or links to bounded chunks, task reports, raw requirements, exact constraints, and guidance. Review the whole phase, not just the final commit or latest fix. For final review use the recorded whole-run baseline, not a guessed main branch or `HEAD~1`. Read relevant surrounding code and callers when the diff alone cannot establish correctness.

For large reviews split by coherent components and retain a separate integration/contract check. A context error, missing chunk, or absent report leaves the review gate incomplete.

## Ledger usage

The state helper is at `../../rpi-workflow/scripts/rpi_state.py` relative to this reference directory. Resolve it to an absolute path before working in the target repository. Always pass `--root` and `--run` explicitly. Example (replace paths and slug with actual values):

```sh
python3 /path/to/rpi_state.py --root /path/to/project --run feature status
python3 /path/to/rpi_state.py --root /path/to/project --run feature gate phase:1:read in_progress
python3 /path/to/rpi_state.py --root /path/to/project --run feature gate phase:1:read completed --evidence /path/to/read-report.md
```

Use `issue` to register a finding from a text file before fixing. Use `resolve` only after explicit re-review, providing evidence and a disposition (`fixed` or `rejected`). `reopen <gate> --reason ...` invalidates that gate and all downstream gates when assumptions or code change. Keep prior evidence in event history and rerun affected work. The helper rejects completion out of order and reports missing evidence; it cannot judge whether the contents of a report are truthful.

## Final report

Report completed phase/task counts and review cycles, checks with results, any departures from the original plan, outstanding issues, and human verification status. Missing tools, blocked integration tests, and unavailable credentials are unresolved validation limitations, not compromises to hide. Show the exact next action that resolves a blocker. For a plan subset, explicitly name remaining batches; completion of one batch does not complete the whole design.
