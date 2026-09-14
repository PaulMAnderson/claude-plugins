# Shared workflow contract

## Context and scope

1. Announce the relevant skill and current objective. Read applicable `AGENTS.md` instructions, existing `.rpi/CONTEXT.md` and `.rpi/PROJECT.md`, and the current plan. Verify the repository/worktree, branch, actual files, and working-tree changes before trusting saved state.
2. User instructions take precedence over this workflow. Preserve previously granted authorization. Resolve routine implementation choices from evidence and state reasonable assumptions. Ask only about missing decisions that materially affect the requested outcome, incompatible binding requirements, or actions outside authorization.
3. Capture the Definition of Done and exact constraints before design detail expands. Record whether decisions are user-confirmed, supplied in the request, or agent assumptions. An agent-selected default is never labeled user-approved. Preserve explicit interactive approval requirements when the user requests them; otherwise present concrete decisions and continue authorized work.
4. Scale artifact size to the task. A formal plan retains all gates even when compact. One-off analysis and small helpers use `rpi-quick`; do not force a multi-phase project onto them.

## Progress is durable

Use the bundled `scripts/rpi_state.py` (relative to this skill directory) to create and maintain `.rpi/runs/<slug>/state.json`. Run its `--help` and `init --help` for exact arguments. This is the authoritative machine-readable ledger; `.rpi/PROJECT.md` is its human summary. A native planning tool, when exposed, may mirror it but does not replace it.

Register all planned phases in dependency order. Each phase has separate `read`, `execute`, and `review` gates. Each gate requires evidence before completion. Store task reports and complete verbatim review findings in files under the same run directory, and point ledger entries to them. The controller alone updates state; workers return reports, avoiding concurrent writes. Do not reuse one run slug for different work.

Update the ledger at every gate transition, failed check, review finding, fix, and blocker. Track task-level progress in the phase file with `pending`, `in_progress`, `completed`, or `blocked`, plus a report path. Reports include changed files, tests/commands, exit codes, relevant output, exact tested revision or working-tree state, and concerns. Keep the original wording of unresolved issues through compaction. Silence on re-review does not resolve a finding.

At the start, between phases, and before a completion claim, inspect `status`. Use `check` to detect missing gates, unresolved issues, absent evidence, and incomplete final validation. This checks recorded evidence and ordering, not semantic correctness: inspect the evidence yourself. It does not run tests or prove that a claimed test pass is real.

Give concise progress updates during sustained work (roughly every minute): completed phase/tasks, current gate, evidence or finding, blocker, and next action. Do not invent percentages or background activity. Persistent artifacts support resumption; they do not create a background monitoring service.

## Gates and evidence

| Gate | Required result |
| --- | --- |
| Design | Investigated paths; Definition of Done; exact contracts; observable scoped ACs; alternatives and rationale; assumptions/open decisions; cohesive phases |
| Plan | Fresh codebase/dependency verification; executable ordered tasks; exact paths and checks; all ACs mapped to tasks and tests/manual verification; plan reviewed with no unresolved findings |
| Phase read | Re-read current phase and required sources just before implementation; confirm dependencies; capture baseline and phase-start revision |
| Phase execute | Every task implemented and verified; behavior tests in the phase delivering the behavior; reports recorded; no unresolved task concerns |
| Phase review | Whole phase reviewed against design and code; every finding explicitly fixed and verified or rejected with evidence; no unresolved findings |
| Final review | Full change reviewed from recorded execution baseline, including uncommitted/untracked implementation; interactions between phases checked |
| Coverage | Every AC linked to tests whose assertions were inspected, or justified manual steps; missing behavioral tests fixed and reviewed |
| Verification | Required test/build/lint/type checks run on final relevant code; output and exit codes inspected; manual acceptance status reported truthfully |

Use meaningful behavioral tests for functionality and regressions, normally red → green → refactor. Confirm the initial failure is the intended missing behavior, not a broken test setup. Infrastructure, documentation, configuration, and reversible low-impact changes use appropriate operational or structural checks; do not create tests that merely restate the implementation. A phase cannot postpone tests for its behavior until a later phase.

Run targeted checks per task, phase integration checks per phase, and required whole-project checks before completion. Reuse evidence only when it still applies to unchanged relevant code and environment. Fixes invalidate affected evidence; rerun covering checks. A missing environment or failing required check is **blocked/not verified**, never a pass. Distinguish baseline failures from new failures without quietly waiving either.

## Review roles and retries

Review is a separate pass from implementation. If native subagents are available and delegation is authorized, give a reviewer a bounded scope, raw requirements, complete diff, paths, and test reports. Use the actual tool schema and configured model; do not translate Claude/Gemini model names into guessed Codex models. Otherwise perform the same review locally and explicitly report it as self-review. Lack of subagents does not remove a gate.

Do not pre-rate issues, tell reviewers what not to flag, or hide changes. Track Critical, Important, and Minor issues individually. Fix all valid findings in scope, including Minor, and explicitly re-review each. Reject incorrect findings only with evidence. A requested waiver must be recorded and disclosed; it is not a zero-issue pass. A valid finding contradicting a binding user requirement needs the user's decision before a conflicting fix.

After three cycles with the same unresolved issue, stop repeating the same attempt: record the evidence, reassess the root cause/plan, and ask for the missing decision when necessary. For review timeout/context failure, first narrow the package, then split it into logical chunks plus a cross-component review. Never treat an empty/error response as approval.

## Git and handoff

Respect the current workspace and user's changes. Use a worktree when isolation is useful and authorized; verify its location, branch, baseline, ignored status for an in-repo worktree directory, and setup checks. Never reset, stash, remove, or overwrite another person's work to manufacture a clean baseline.

Record the execution base before the first implementation change and each phase base before its first task. Review the complete phase, not `HEAD~1`. When work is uncommitted, use the working-tree diff against the recorded base plus staged and untracked file inspection; include a before snapshot if the initial tree was dirty. Do not create commits merely to make review tooling work.

Check whether changed APIs, contracts, commands, or directory structure require updates to affected `AGENTS.md` files before final review; verify claims against code. Preserve unrelated instructions.

Commit, push, PR, merge, and cleanup follow the user's authorization and repository policy. If integration is unspecified, leave the verified work in place and report its branch/worktree. Merge only when authorized, then validate the merged result. Keep worktrees for ongoing work/PRs; deletion or discard requires explicit authorization.

Before handoff/compaction, merge state into `.rpi/CONTEXT.md` and `.rpi/PROJECT.md`. Preserve exact constraints, unresolved findings, evidence, absolute plan/worktree paths, recorded bases, and next gate. Re-read and reconcile on resume. Do not require `/clear` or pretend context is automatically injected by an uninstalled hook.
