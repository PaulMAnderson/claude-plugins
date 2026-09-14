---
name: "rpi-context"
description: "Save, compress, or restore RPI session context and project progress while preserving exact decisions, task/review state, verification evidence, and the next action across sessions."
---

# Durable context without drift

Read existing `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` before updating either. Merge new information into anchored sections; do not regenerate from memory and lose earlier decisions. The run ledger and actual repository state outrank stale summaries. Inspect both on resume.

`.rpi/CONTEXT.md` stores the active session:

- **Session Intent:** current objective, requested scope, authorization and important exclusions.
- **Files Modified:** every relevant created/modified file and purpose; distinguish pre-existing changes.
- **Decisions Made:** decisions with rationale and status (user-confirmed, supplied, or assumption); retain exact values, strings, signatures, units, and constraints verbatim.
- **Current State:** absolute worktree/design/plan/run paths, branch and recorded bases, phase/task/gate, command evidence, failing checks, unresolved findings (verbatim or links to complete issue records).
- **Next Steps:** ordered concrete actions, blockers, and what resolves them.

`.rpi/PROJECT.md` stores long-lived context:

- **Git State:** verified current branch/worktree, HEAD, dirty status, recent relevant commits, recorded run base.
- **Implementation Status:** phase/task/gate table, ledger paths, completed vs pending verification.
- **Decisions Log:** append significant architecture and contract decisions with rationale; mark superseded decisions rather than silently removing history.
- **Open Questions/Risks:** unresolved decisions, exact review issues/evidence links, blocked checks, manual acceptance, and owners where known.

Keep hot content (intent, binding constraints, blockers, active gate) concise and prominent; link warm detail (current plan/reports) and cold history (completed work/research). Do not compress away arbitrary-looking numbers or strings that form contracts. Keep unrelated runs' history and ensure summaries identify which run they describe.

Checkpoint at phase boundaries, before handoff/compaction, and after material blockers. On resume, read hot state, ledger `status`, current phase, and relevant `AGENTS.md`; verify branch, files, and evidence freshness before acting. Also inspect legacy `.rpi/exec/progress.md` and git history when continuing Claude/Gemini work. Preserve that history and migrate verified progress without rerunning completed tasks. Resume at the first incomplete gate, not the beginning of the workflow. No automatic hook injection or context reset is assumed. Tell the user which files were updated and the next action.
