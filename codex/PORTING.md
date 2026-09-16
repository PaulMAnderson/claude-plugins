# Claude Code / Gemini CLI → Codex port

The original Claude and Gemini trees are retained. The Codex implementation is a maintained skills bundle in `codex/skills`, discoverable through project `.agents/skills` links or the installer. All 39 Claude skills and 39 Gemini skills are represented, including `receiving-code-review` in `astrolabe-review`.

`source-map.json` records every source skill plus command, agent, hook, and workflow script (152 files), its SHA-256, and its target skill. This provides a complete inventory and flags upstream drift. It is a coverage map, not a mechanical string-replacement generator.

## Workflow coverage

| Original skills/commands | Codex equivalent |
| --- | --- |
| using-plan-and-execute, getting-started, how-to-customize | `astrolabe-workflow` entrypoint and shared contract |
| starting-a-design-plan, start-design-plan, asking-clarifying-questions, brainstorming, flesh-it-out, writing-design-plans | `astrolabe-design` and design template |
| starting-an-implementation-plan, start-implementation-plan, writing-implementation-plans | `astrolabe-plan` and phase/test-requirement format |
| executing-an-implementation-plan, execute-implementation-plan, implement-task | `astrolabe-implement` and execution mechanics |
| requesting-code-review, receiving-code-review, code-review, fix-review-issues, analyze-test-coverage, verification-before-completion | `astrolabe-review`, review/coverage procedure, shared evidence gates |
| test-driven-development, writing-good-tests | Shared workflow testing rule and `astrolabe-house-style` test reference |
| systematic-debugging | `astrolabe-debug` |
| compressing-context, compress-context | `astrolabe-context` with anchored merging and ledger reconciliation |
| using-git-worktrees, finishing-a-development-branch | Shared workflow git/handoff rules and `astrolabe-implement` completion |
| quick-analysis, helper-function | `astrolabe-quick` with chat intent, verification, SESSION log |
| investigating-a-codebase, researching-on-the-internet, investigate-codebase, research-internet, research-remote-code, research-combined | `astrolabe-research` local/remote/internet/combined modes |
| using-generic-agents, doing-a-simple-two-stage-fanout, fanout | Capability-aware roles plus `astrolabe-fanout` worker/critic/synthesis stages |
| coding-effectively, defense-in-depth, howto-functional-vs-imperative | `astrolabe-house-style/references/engineering.md` |
| howto-code-in-python, howto-code-in-matlab, howto-code-in-r | `astrolabe-house-style/references/languages.md` |
| howto-develop-with-mysql | `astrolabe-house-style/references/mysql.md` |
| writing-for-a-technical-audience | `astrolabe-house-style/references/writing.md` |
| writing-skills, testing-skills-with-subagents, writing-claude-directives | `astrolabe-extend-codex` skill/directive authoring and behavioral validation |
| writing-claude-md-files, maintaining-project-context | `astrolabe-extend-codex` AGENTS.md/librarian mode |
| creating-an-agent, creating-a-plugin, maintaining-a-marketplace | `astrolabe-extend-codex` capability-aware roles and current Codex packaging/distribution |

## Native adaptations

| Source mechanism | Codex implementation |
| --- | --- |
| Slash command files and vendor skill activation tools | Discoverable named skills; `$astrolabe-design`, `$astrolabe-plan`, `$astrolabe-implement`; direct linked-resource reads |
| TaskCreate/TaskUpdate or write_todos | Durable JSON run ledger plus task-level phase/report records; native planning UI may mirror it |
| Named Claude/Gemini agent types and model tiers | Bounded role briefs using actual exposed subagent capabilities and configured models, with truthful sequential/self-review fallback |
| Session-start and skill-reminder hooks | Explicit startup/resume checkpoint in the skills; optional project AGENTS.md defaults |
| Instruction-file reminder hook/librarian | Explicit contract/structure/command documentation check before final review |
| Task-brief/review-package/astrolabe-workspace helpers | Marker-based task reads; report directories scoped per run; full-phase/full-change diff procedure covering uncommitted and untracked work |
| Gemini session-monitor.py | The source file is empty; the new state helper provides explicit, tested checkpoint integrity and status |
| Mandatory /clear and manual handoffs | Checkpoint and resume; continue directly when already authorized |
| Plugin/extension manifests | A directly installable skills bundle; no dependency on vendor manifests, event schemas, or global config edits |

## Preserved invariants

1. Research actual code before design/planning; research current dependency contracts rather than guessing.
2. Definition of Done precedes detailed design; retain alternatives/rationale, constraints, interfaces, and scoped observable ACs.
3. Detailed phases use exact paths/contracts, explicit dependencies, task markers, verification commands, and verifiable end states.
4. Every AC maps to implementation and meaningful automated tests or justified manual verification. Behavior tests belong in the phase implementing that behavior.
5. Read current phase just in time; implement tasks; review the entire phase; persist findings/fixes and re-review to zero unresolved issues.
6. Final whole-change review precedes acceptance coverage analysis and human test plan; final required checks use actual evidence.
7. Preserve exact unresolved findings and constraints across context compression; reconcile status with actual files/revisions on resume.
8. Report blockers and manual acceptance honestly; never convert a timeout, unavailable environment, or unexecuted test into a pass.

## Deliberate reconciliations

- **Review cadence:** the source review skill says after every task, while the main executor explicitly says after each phase. The port follows the main executor: task verification, phase review, final review.
- **Plan code:** the source checklist requires complete code everywhere, while its detailed functionality template says to describe behavior/tests and generate code against fresh context. The port preserves concrete contracts/tasks and adds implementation code where non-obvious; it does not require stale code dumps in every plan.
- **TDD and verification scope:** keep red/green behavioral verification and regression tests; use operational/structural checks for infrastructure and low-impact documentation/configuration. Run targeted task checks and required final suites, refreshing evidence after relevant changes.
- **Approvals and phase limits:** record user-supplied/confirmed requirements separately from assumptions. Continue previously authorized work without repeated approvals or mandatory resets. Large designs are split into linked batches without losing requirements, rather than hard-refusing more than eight phases.
- **Review correctness:** every valid Minor finding still matters. An incorrect finding can be rejected with evidence and explicit disposition; silence is not resolution. A user waiver is disclosed, not represented as a zero-issue pass.
- **Git integration:** source templates unconditionally commit and sometimes clean worktrees even for PRs. The port follows actual authorization, covers uncommitted work in review, retains active worktrees, and requires explicit scope for destructive discard.
- **Scientific house style:** keep FCIS, transaction ownership, shape/unit discipline, reproducibility, and meaningful tests. Preserve existing project tooling and supported language versions. Do not treat public IDs as access control, require decimal storage for every scientific float, or impose identical validation at adjacent trusted layers.
- **Fanout:** use actual context/concurrency capacity; preserve distinct critic coverage and explicit gaps. A split/superseded task is not labeled successfully analyzed.

## Maintenance and attribution

Edit the Codex skills directly. When either source tree changes, inspect the changed material, update the target procedure and coverage tests when relevant, and refresh only the reviewed source fingerprints. Run the bundle validator and workflow tests after changes. Keep sibling skills together when distributing.

Adapted from Paul Anderson's Astrolabe fork of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins); original contributors include Ed Ropple and contributors. Superpowers-derived material credits Jesse Vincent's [obra/superpowers](https://github.com/obra/superpowers). House-style source also credits [Trail of Bits skills](https://github.com/trailofbits/skills). Each installed skill carries the original CC BY-SA 4.0 notice, MIT license for superpowers-derived material, and an adaptation notice.
