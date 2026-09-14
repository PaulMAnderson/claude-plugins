---
name: "rpi-implement"
description: "Execute or resume an RPI implementation plan with task reports, durable progress, per-phase review and fixes, final acceptance coverage, and evidence-based validation."
---

# Execute an implementation plan

Read [the shared workflow contract](../rpi-workflow/references/workflow.md) and [execution details](references/execution.md).

1. Resolve the plan and repository from the request or recorded active context. Verify the paths, branch/worktree, working tree, design/plan gates, and ledger. For a legacy Claude/Gemini plan, inspect its design, test mapping, `.rpi/exec/progress.md`, existing reports, and git history before initializing the new ledger. Migrate verified completed gates in order with a recovery report as evidence; do not redo completed implementation merely because the JSON ledger is new. Re-review or verify missing evidence rather than assuming an old DONE label is sufficient. Recover missing test requirements from the design; do not silently skip coverage.
2. Inventory phase filenames and dependency order without loading every task. Record the whole-run baseline before changes, including pre-existing dirty/untracked files, and required baseline test results. Register all phases in the ledger. Read any project implementation guidance.
3. For each phase, complete **read → execute → review** in order. Re-read its file, exact ACs, and required sources just in time. Record the phase-start revision and relevant before-state. Reconcile changed interfaces or new constraints before implementation; ask only if resolving a conflict changes a binding user decision.
4. Execute tasks in dependency order, with status and a durable report for each. Use [rpi-house-style](../rpi-house-style/SKILL.md) when its conventions apply. Test behavioral changes red → green → refactor; use direct operational checks for infrastructure. Address task concerns before claiming completion. Show the task's concise outcome and verification, then continue.
5. Review the entire phase after its tasks using [rpi-review](../rpi-review/SKILL.md). Record every finding verbatim, fix valid Critical/Important/Minor issues, rerun affected checks, and explicitly re-review them. A task's success report alone cannot complete the phase review gate. Continue only when no unresolved findings remain.
6. After all phases, inspect changed contracts/commands/structure and update relevant project context as needed with [rpi-extend-codex](../rpi-extend-codex/SKILL.md). Run full-change review, acceptance/test coverage analysis, and final verification in that order using `rpi-review`. If later fixes change code, re-review the affected and cross-phase behavior and refresh invalidated checks.
7. Write the human test plan under `docs/test-plans/<plan-directory-name>.md` after coverage passes. Distinguish automated coverage, executed manual checks, and pending human checks. Never report pending acceptance as validated.
8. Run the ledger `check`. Checkpoint context, then deliver phase/task counts, review cycles, exact checks/results, remaining manual work or blockers, and branch/worktree. Follow authorized integration instructions; otherwise leave work in place. Do not claim completion if a required gate is blocked.
