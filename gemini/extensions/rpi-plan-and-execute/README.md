# rpi-plan-and-execute — Gemini CLI Extension

Planning and execution workflows for software development projects. Converted from the `rpi-plan-and-execute` Claude Code plugin v1.10.2.

## Installation

```bash
gemini extensions link /path/to/gemini/extensions/rpi-plan-and-execute
```

## Commands

| Command | Description |
|---------|-------------|
| `/compress-context` | Compress session context to `.rpi/CONTEXT.md` |
| `/execute-implementation-plan <plan-dir> <work-dir>` | Execute a plan task-by-task |
| `/flesh-it-out` | Turn a general idea into something specific |
| `/how-to-customize` | Learn how to add project-specific guidance |
| `/quick-analysis` | Run a one-off data analysis task |
| `/start-design-plan` | Start the design process (brainstorm → clarify → plan) |
| `/start-implementation-plan` | Create an implementation plan from a design doc |
| `/workspace-dashboard` | View the workspace project dashboard |
| `/code-review` | Review completed work against plans and quality gates |
| `/fix-review-issues` | Fix issues identified by code review |
| `/implement-task` | Implement a single task with TDD and verification |
| `/analyze-test-coverage` | Validate test coverage and generate human test plan |

## Typical Workflow

```
/start-design-plan          ← collaborative design with clarification
/start-implementation-plan  ← break design into phased tasks
/execute-implementation-plan <plan-dir> <work-dir>  ← execute all phases
/code-review                ← validate against plan + quality gates
/fix-review-issues          ← address any issues found
/analyze-test-coverage      ← confirm coverage, generate human test plan
```

## Project Customization

Create `.rpi/` in your project root with optional guidance files:

- **`.rpi/design-plan-guidance.md`** — Domain terms, architectural constraints, technology choices
- **`.rpi/implementation-plan-guidance.md`** — Coding standards, testing requirements, commit conventions

See `/how-to-customize` for details and examples.

## Conversion Notes

### Original Plugin

- **Name**: `rpi-plan-and-execute`
- **Version**: 1.10.2
- **Source**: Claude Code plugin based on obra/superpowers

### Component Mapping

| Claude Component | Gemini Equivalent | Notes |
|-----------------|-------------------|-------|
| `commands/compress-context.md` | `commands/compress-context.toml` | Skill behavior inlined |
| `commands/execute-implementation-plan.md` | `commands/execute-implementation-plan.toml` | Skill behavior inlined |
| `commands/flesh-it-out.md` | `commands/flesh-it-out.toml` | Skill behavior inlined |
| `commands/how-to-customize.md` | `commands/how-to-customize.toml` | Direct conversion |
| `commands/quick-analysis.md` | `commands/quick-analysis.toml` | Expanded from stub |
| `commands/start-design-plan.md` | `commands/start-design-plan.toml` | Skill behavior inlined |
| `commands/start-implementation-plan.md` | `commands/start-implementation-plan.toml` | Skill behavior inlined |
| `commands/workspace-dashboard.md` | `commands/workspace-dashboard.toml` | Expanded from stub |
| `commands/helper-function.md` | — | See limitations below |
| `agents/code-reviewer.md` | `commands/code-review.toml` + `GEMINI.md` | Role/expertise in GEMINI.md |
| `agents/task-bug-fixer.md` | `commands/fix-review-issues.toml` + `GEMINI.md` | Role/expertise in GEMINI.md |
| `agents/task-implementor-fast.md` | `commands/implement-task.toml` + `GEMINI.md` | Role/expertise in GEMINI.md |
| `agents/test-analyst.md` | `commands/analyze-test-coverage.toml` + `GEMINI.md` | Role/expertise in GEMINI.md |
| `hooks/hooks.json` | — | See limitations below |

### Limitations

**helper-function command** — The original command (`commands/helper-function.md`) references a `helper-function` skill that is an internal Claude plugin dependency not present in the plugin's own skill directory. It was not converted because the behavior it delegates to is not available in this extension. Users needing this workflow should use `/implement-task` for small, single-function tasks.

**hooks** — The original plugin's `hooks/hooks.json` defines three hooks that have no Gemini CLI equivalent:

| Hook | Type | Purpose | Status |
|------|------|---------|--------|
| `SessionStart` | Runs `session-start.sh` on startup/resume | Likely loads context or initializes state | Not convertible — no session hooks in Gemini CLI |
| `PostToolUse` | Runs `session-monitor.py` after each tool call | Context monitoring / token tracking | Not convertible — no PostToolUse hooks in Gemini CLI |
| `StatusLine` | Runs `statusline.py` | Displays status in Claude Code UI | Not convertible — no status line API in Gemini CLI |

None of the hooks block tools, so no `excludeTools` entries are needed. The monitoring and status functionality they provide is not available in Gemini CLI extensions.

**Agent specialization** — The original agents run as Claude Code subagents with specific models, colors, and the ability to invoke other skills via the Skill tool. In this extension, the agent roles are represented as commands (prompts run in the main session) and as context in `GEMINI.md`. Gemini CLI does not currently support spawning specialized subagents.

**Skill system** — The Claude plugin delegates heavily to a skill system (e.g., `compressing-context`, `executing-an-implementation-plan`, `starting-a-design-plan`). Those skills are external to this plugin and are not available in Gemini CLI. The converted commands inline the essential workflow logic rather than delegating to skills.

**No MCP servers** — The original plugin had no `.mcp.json`, so no MCP configuration was needed.
