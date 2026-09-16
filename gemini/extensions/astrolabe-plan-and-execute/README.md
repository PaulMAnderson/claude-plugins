# Astrolabe planning and execution for Gemini CLI

This extension provides local task tracking, design, implementation, and review workflows. Its skills use the same `.astrolabe/` project format as the Claude and Codex distributions.

## Install

Link this extension from the checkout so its commands, skills, references, hooks, and scripts remain together:

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-plan-and-execute
```

The [root README](../../../README.md) lists the other Astrolabe extensions. The local state helper needs Python 3; it needs no registration, credentials, network access, or service.

## Choose a tier

| Tier | Entry | Result |
| --- | --- | --- |
| Micro | `helper-function` skill | Short history entry |
| Quick | `/quick-analysis` or `quick-analysis` skill | Short history entry |
| Spec | `/start-tracked-task` or `starting-a-tracked-task` skill | Dated spec with numbered steps and notes |
| Full | `/start-design-plan` → `/start-implementation-plan` → `/execute-implementation-plan` | Design and phase plans, review reports, and human test plan |

A Spec can be resumed with the same slug. Checked steps and notes remain in its `.astrolabe/docs/specs/YYYY-MM-DD-<slug>.md` file. If the work needs architecture or full acceptance criteria, use the Spec as context for `/start-design-plan`.

Other commands include `/flesh-it-out`, `/compress-context`, `/how-to-customize`, `/code-review`, `/fix-review-issues`, `/implement-task`, and `/analyze-test-coverage`. The matching skill files are in `skills/`, and the command definitions are in `commands/`.

## Shared project state

Before work, tier skills initialize missing state and read `PROJECT.md`, `STATUS.md`, and both lists in `PLANNED.md`. If planned work matches the request, the agent shows the item and asks whether to use it, extend it, or proceed separately. At exit, it updates `STATUS.md` and appends an outcome to `HISTORY.md`. An out-of-scope idea enters Backlog or Roadmap only after the user chooses a list.

Use `/start-planned B1` to begin a specific Backlog or Roadmap item. It remains in `PLANNED.md` while active or paused. After its requested outcome is verified, completion removes it and records its original text and result in `HISTORY.md`; its ID is never reused.

`CONTEXT.md` remains a resume summary. Design and implementation plans live under `.astrolabe/docs/`. The [shared format](../../../docs/astrolabe-state-format.md) documents the files and versioned status schema. The extension's `scripts/astrolabe-state.py` writes the local state; `hooks/session-start.sh` reads saved context when present.

The optional [Hypercube dashboard](../../../README.md#hypercube-dashboard) is separate from this extension. The [legacy migration script](../../../README.md#migrate-a-legacy-rpi-project) is also separate from this extension.

## Customization

Put optional project rules in `.astrolabe/design-plan-guidance.md` or `.astrolabe/implementation-plan-guidance.md`. `/how-to-customize` explains when the workflow reads them.

This extension is adapted from the Claude Code plugin. Gemini commands and skills use Gemini tool vocabulary, including `ask_user` and `write_todos`; its agents and hooks are in this extension's `agents/` and `hooks/` directories.
