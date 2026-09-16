# Astrolabe planning and execution for Claude Code

This plugin offers four levels of structure. They share local project state, so a small task can grow into a spec or full design without losing its earlier outcome.

## Choose a workflow

| Tier | Command | Use it when | Record produced |
| --- | --- | --- | --- |
| Micro | `/helper-function` | One helper function is enough | Short entry in `HISTORY.md` |
| Quick | `/quick-analysis` | An analysis fits one session | Short entry in `HISTORY.md` |
| Spec | `/start-tracked-task` | You need a checklist that survives later sessions | `.astrolabe/docs/specs/YYYY-MM-DD-<slug>.md` |
| Full | `/start-design-plan`, `/start-implementation-plan`, `/execute-implementation-plan` | You need architecture, acceptance criteria, phased implementation, and review | Design and implementation plans, reports, and a human test plan |

A Spec stores intent, numbered checkboxes, and notes. Invoking it again with the same work slug resumes the existing file and preserves completed steps. If the task needs competing approaches or full acceptance criteria, start a design plan using the Spec as context.

### Full workflow

1. `/start-design-plan` investigates the project, clarifies requirements, and writes `.astrolabe/docs/design-plans/YYYY-MM-DD-<slug>.md` with observable acceptance criteria and phases.
2. `/start-implementation-plan @.astrolabe/docs/design-plans/YYYY-MM-DD-<slug>.md .` verifies the current code and writes phase files plus `test-requirements.md` under `.astrolabe/docs/implementation-plans/`.
3. `/execute-implementation-plan @.astrolabe/docs/implementation-plans/YYYY-MM-DD-<slug> .` executes and reviews phases, checks acceptance coverage, and writes a human test plan under `docs/test-plans/`.

The workflow records progress and evidence so a later session can resume the first incomplete gate. Git commits, pushes, pull requests, and merges follow the user's authorization and repository policy; the commands do not require a context reset between phases.

## Shared project state

The first tier invocation creates missing files under the project's `.astrolabe/` directory. Existing files are preserved. Before work, the skill reads `PROJECT.md` and `STATUS.md`, then compares the request with both lists in `PLANNED.md`. If an item matches, it shows the item and asks how to proceed. If none matches, work continues without an extra decision.

| File | Role |
| --- | --- |
| `PROJECT.md` | Stable project description |
| `STATUS.md` | Versioned live status snapshot |
| `HISTORY.md` | Append-only work outcomes |
| `PLANNED.md` | Backlog (`B1`, `B2`, …) and Roadmap (`R1`, `R2`, …) |
| `CONTEXT.md` | Optional resume summary |

At exit, the skill updates `STATUS.md` and appends an outcome to `HISTORY.md`. If an unrelated idea came up, it offers to add it to Backlog or Roadmap; declining leaves `PLANNED.md` unchanged. The [shared format](../../docs/astrolabe-state-format.md) gives the exact schema. The bundled `scripts/astrolabe-state.py` performs local state writes with Python's standard library.

No registration or network service is needed for local tracking. The optional [Hypercube dashboard](../../README.md#hypercube-dashboard) reads explicitly registered projects.

Use `/start-planned B1` to begin a Backlog or Roadmap item by ID. It stays in `PLANNED.md` until its requested outcome is verified. Completion removes it from the list and records the original item and result in `HISTORY.md`; its ID remains reserved.

## Other commands and plugins

`/compress-context` updates the resume summary. `/flesh-it-out` helps clarify a rough idea, and `/how-to-customize` describes optional `.astrolabe/design-plan-guidance.md` and `.astrolabe/implementation-plan-guidance.md` files.

The full workflow calls research, review, and documentation skills supplied by `astrolabe-research-agents`, `astrolabe-house-style`, and `astrolabe-extending-claude`. Install those plugins for their specialized behavior. The [root README](../../README.md) gives marketplace installation steps.

## Attribution and license

This plugin includes work derived from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent. See [LICENSE.superpowers](LICENSE.superpowers) for MIT-derived material and [LICENSE](LICENSE) for other content.
