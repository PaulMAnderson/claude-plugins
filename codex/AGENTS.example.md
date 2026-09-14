# Optional RPI project defaults

Merge relevant instructions into the existing project AGENTS.md; do not replace unrelated guidance.

- For substantial feature/refactor work, use `rpi-workflow`: investigate, design, plan, implement, review, and validate. Respect the requested stage and scope; bounded one-off analyses/helpers use `rpi-quick`.
- At RPI startup/resume, read `.rpi/CONTEXT.md`, `.rpi/PROJECT.md`, and the active run ledger if present. Verify the actual branch/worktree and current phase before resuming.
- Read `.rpi/design-plan-guidance.md` before design and `.rpi/implementation-plan-guidance.md` before planning/execution/review when they exist.
- Maintain scoped acceptance criteria, phase/task progress and evidence reports. Update progress at task/gate boundaries and report meaningful updates during sustained work.
- Verify each task, review each whole phase, fix and explicitly re-review all valid findings, then perform whole-change review and acceptance coverage analysis before completion.
- Use actual command evidence; failing or unavailable required checks and pending manual acceptance remain unverified. Before handoff, inspect ledger status/check and checkpoint context.
- Check whether changed contracts, commands, or architecture require updates to relevant AGENTS.md content before final review.
- User instructions and existing authorization take precedence over skill defaults. Continue authorized work across stages; ask only for consequential missing decisions or actions outside authorization. Commit/integration/cleanup follow the user's instructions and project policy.
