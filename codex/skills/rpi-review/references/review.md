# Review and coverage procedures

## Inputs

Read the design's exact ACs/contracts; plan scope; implementation guidance if it exists; full phase/run baseline and current code state; changed/untracked files; and task verification reports. If any are missing, obtain them from repository evidence before concluding. Read [execution mechanics](../../rpi-implement/references/execution.md) when package construction is needed.

For an independent reviewer provide raw requirements and code, not the implementor's desired conclusion. Do not instruct the reviewer to suppress a category or pre-assign severity. Re-run checks when evidence is absent, stale, contradictory, or newly affected; do not mechanically repeat an unchanged suite solely because a different role is reading it.

## Report format

- Scope: plan/phase/whole-change, baseline, current revision plus dirty state.
- Mode: independent reviewer or self-review; any unavailable review resources.
- Findings: stable issue ID, severity, file:line, complete description, evidence, affected AC/contract, why it matters, and suggested direction.
- Verification inspected/run: commands, exit codes, evidence paths, untested areas.
- Assessment: unresolved count by severity and specific blockers.

Critical means material correctness, safety/security, data loss, or unusable output. Important means substantial behavior/maintainability/performance/test gaps. Minor means smaller but actionable in-scope problems. Severity follows impact; do not import universal rules such as 'every public function untested is Critical' into unrelated languages/projects.

## Fix/re-review loop

1. Save complete findings in the run's reports directory and create one ledger issue per finding. Preserve original wording, location, and expected behavior.
2. Verify each issue. For valid findings, trace the root cause, change only relevant code, and add meaningful regression coverage where applicable. For false positives, record code/test evidence for rejection. For ambiguities, request the missing detail while doing independent fixes.
3. Re-run tests covering each changed behavior and affected integration checks. Record covering test files, exact command, exit code, output, and tested state.
4. Explicitly re-review each previous issue and the new changes. Keep unresolved issues even when the reviewer did not mention them again. Add newly found issues. Use the ledger `resolve` only when fixed/rejected evidence exists.
5. Repeat until zero unresolved issues. After three cycles of the same failure, change the diagnostic approach and surface the unresolved cause/decision; no endless identical retries.

If review fails operationally, narrow then split the review with an integration pass. Never mark timeout/empty response/error as passed. If a final coverage fix changes code after final review, reopen the final-review gate and redo affected review, coverage, and verification.

## Acceptance coverage analysis

Read `test-requirements.md` and compare its rows against the original design. For every AC:

1. Locate the test file and test symbol. Read setup, input, call, and assertions. Confirm the assertion tests the specified behavior and would fail if it were wrong; merely finding the AC ID or a passing mock proves nothing.
2. Check success variations, relevant failure/boundary cases, and integration behavior. Confirm fixtures and mocks do not bypass the real behavior being claimed.
3. Record `covered`, `missing`, `partial`, or `manual`, with exact evidence and gaps. A manual designation requires rationale; an automated check that cannot currently run remains not verified.
4. Add/fix missing or weak tests within authorized implementation scope, run them, re-review, then repeat the coverage analysis. After three unsuccessful coverage fixes, record the blocker and change approach.

When coverage passes, write `docs/test-plans/<implementation-plan-directory-name>.md` containing:

- Automated coverage summary with commands and test evidence.
- Manual checks: AC ID, prerequisite/environment/data, exact steps, expected observation, cleanup, status/owner.
- End-to-end scenarios that exercise the integrated implementation, grounded in actual interfaces.
- Known limitations and unexecuted steps, explicitly labeled.

Coverage PASS means the verification mapping is adequate. It does not mean pending manual acceptance has passed. Final verification must report that distinction; a required manual check remains blocking until performed or explicitly deferred by the user, with that deferral disclosed.

## Completion verification

Identify what proves each completion claim, run the full relevant command, inspect exit code and output, compare to the required outcome, then make the claim. Check the current code state matches the evidence. Run required test, build, lint, and type checks actually configured by the project, not invented generic commands. N/A needs a reason; missing prerequisites or failures are blocked. Inspect final diff/status for accidental files and scope drift. Record final evidence and run ledger `check` before reporting a clean completion.
