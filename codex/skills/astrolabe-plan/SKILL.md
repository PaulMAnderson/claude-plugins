---
name: "astrolabe-plan"
description: "Turn an Astrolabe design document into a reviewed implementation plan with ordered phase files, detailed tasks, dependency checks, and acceptance-criterion test requirements."
---

# Plan implementation

## Project state

Before work, follow [the shared entry and exit contract](../astrolabe-workflow/references/project-state.md) with tier `design`: initialize local files, read PROJECT.md and STATUS.md, consult both planned lists, and surface a match before proceeding. On exit, update STATUS.md and append HISTORY.md.

Read [the shared workflow contract](../astrolabe-workflow/references/workflow.md) and [plan formats](references/plan-format.md).

1. Resolve the design path from the request or unambiguous active context. If multiple designs plausibly match, ask which one. Read its Definition of Done, ACs, contracts, and phase overview. Read implementation guidance if present. Confirm worktree/branch and preserve existing edits.
2. Re-investigate current code and dependency APIs with [astrolabe-research](../astrolabe-research/SKILL.md). Design snippets may be stale: verify actual interfaces, versions, callers, test frameworks, commands, and prerequisites. Record the inspection date and evidence paths.
3. Track each phase's **read design → investigate code → research dependencies (or justified N/A) → write plan** steps in a planning checklist. Use batch review by default, interactive phase review if requested. Split oversized work into explicit linked batches without losing AC coverage.
4. Create `.astrolabe/docs/implementation-plans/YYYY-MM-DD-<slug>/phase_01.md`, `phase_02.md`, etc. Read and write one phase's detail at a time. Each phase carries exact AC text, required files, dependencies, context budget, and working end state. Every task includes exact create/modify/test paths, behavior, contracts, dependencies, testing obligations, commands, expected results, and status/report fields.
5. Make decisions concrete enough to execute without guessing missing APIs. Include code for non-obvious logic when useful; generate routine implementation and tests against current code at execution time. No unresolved placeholders or forward references to functionality only built in a later phase. Operational setup gets operational verification; behavioral work gets AC tests in that phase.
6. Review all phase files against the entire design using [astrolabe-review](../astrolabe-review/SKILL.md) in **plan review** mode. Check completeness, dependency order, executability, and contract alignment. Track and resolve all findings, then explicitly re-review. Do not equate a label such as APPROVED with no findings.
7. Write `test-requirements.md`: every scoped AC maps to a phase/task and an automated test with behavioral assertion, or justified manual verification with executable steps. Check the table against the design, not just the generated phase files. Human-only cases are not missing automated tests; merely inconvenient automation is not a reason to omit it.
8. Initialize the execution ledger using `../astrolabe-workflow/scripts/astrolabe_state.py init`, with the actual repository, run slug, design path, plan path, and all phase names in dependency order. Record `design` and `plan` gates using the reviewed artifact/evidence paths. Do not mark execution stages complete during planning. On an existing run, inspect `status` and reuse it; never overwrite progress.
9. Checkpoint with [astrolabe-context](../astrolabe-context/SKILL.md). Continue to [astrolabe-implement](../astrolabe-implement/SKILL.md) if authorized; otherwise deliver the verified absolute plan directory and invocation. Do not force a context reset.
