---
name: "astrolabe-context"
description: "Save, compress, or restore Astrolabe session context and project progress while preserving exact decisions, task/review state, verification evidence, and the next action across sessions."
---

# Durable context without drift

Read existing `.astrolabe/CONTEXT.md` and `.astrolabe/PROJECT.md` before updating either. Merge new information into anchored sections; do not regenerate from memory and lose earlier decisions. The run ledger and actual repository state outrank stale summaries. Inspect both on resume.

`.astrolabe/CONTEXT.md` stores the active session:

- **Session Intent:** current objective, requested scope, authorization and important exclusions.
- **Files Modified:** every relevant created/modified file and purpose; distinguish pre-existing changes.
- **Decisions Made:** decisions with rationale and status (user-confirmed, supplied, or assumption); retain exact values, strings, signatures, units, and constraints verbatim.
- **Current State:** absolute worktree/design/plan/run paths, branch and recorded bases, phase/task/gate, command evidence, failing checks, unresolved findings (verbatim or links to complete issue records).
- **Next Steps:** ordered concrete actions, blockers, and what resolves them.

`.astrolabe/PROJECT.md` is the stable, human-authored project description. Read it on entry and update it only when the project's enduring purpose or architecture changes. Keep run status, git state, decisions, review findings, and progress in `.astrolabe/CONTEXT.md`, the run ledger, and append-only `HISTORY.md`; do not turn PROJECT.md into a progress log.

Keep hot content (intent, binding constraints, blockers, active gate) concise and prominent; link warm detail (current plan/reports) and cold history (completed work/research). Do not compress away arbitrary-looking numbers or strings that form contracts. Keep unrelated runs' history and ensure summaries identify which run they describe.

Checkpoint at phase boundaries, before handoff/compaction, and after material blockers. On resume, read hot state, ledger `status`, current phase, and relevant `AGENTS.md`; verify branch, files, and evidence freshness before acting. Also inspect legacy `.astrolabe/exec/progress.md` and git history when continuing Claude/Gemini work. Preserve that history and migrate verified progress without rerunning completed tasks. Resume at the first incomplete gate, not the beginning of the workflow. No automatic hook injection or context reset is assumed. Tell the user which files were updated and the next action.
