# rpi-extending-claude Gemini Extension

Converted from the `rpi-extending-claude` Claude Code plugin (v1.1.0).

Knowledge for extending AI coding assistants: creating plugins, commands, agents, skills, hooks, MCP servers, and maintaining marketplaces.

## Installation

```bash
gemini extensions link /Users/paul/Claude/claude-plugins/gemini/extensions/rpi-extending-claude
```

## Conversion Summary

| Component | Source | Gemini Output | Notes |
|-----------|--------|---------------|-------|
| Manifest | `.claude-plugin/plugin.json` | `gemini-extension.json` | Direct conversion |
| Skills (8) | `skills/*/SKILL.md` | `GEMINI.md` | Consolidated into sections |
| Agent (1) | `agents/project-claude-librarian.md` | `GEMINI.md` | Extracted as knowledge section |
| Commands | None in source | None | Plugin had no commands |
| Hooks | None in source | None | Plugin had no hooks |
| MCP | None in source | None | Plugin had no `.mcp.json` |

## What Was Converted

### Skills → GEMINI.md

All 8 skills were stripped of YAML frontmatter, had Claude-specific tool invocation instructions generalized, and were consolidated as sections in `GEMINI.md`:

| Skill | GEMINI.md Section |
|-------|-------------------|
| `creating-a-plugin` | Creating a Plugin |
| `creating-an-agent` | Creating an Agent |
| `maintaining-a-marketplace` | Maintaining a Marketplace |
| `maintaining-project-context` | Maintaining Project Context |
| `testing-skills-with-subagents` | Testing Skills With Subagents |
| `writing-claude-directives` | Writing Claude Directives |
| `writing-claude-md-files` | Writing CLAUDE.md Files |
| `writing-skills` | Writing Skills |

### Agent → GEMINI.md Section

The `project-claude-librarian` agent had no direct Gemini equivalent. Its knowledge and workflow instructions were extracted into the "Project Claude Librarian (Agent Knowledge)" section in `GEMINI.md`. This makes the agent's decision logic available as context, though it cannot be auto-delegated as in Claude Code.

## Limitations

### No Auto-Delegation

Claude Code can automatically delegate tasks to the `project-claude-librarian` agent based on its `description` field. Gemini CLI has no equivalent auto-delegation mechanism. The agent's knowledge is available in `GEMINI.md`, but triggering it requires explicit user direction.

### Claude-Specific Tool References

Some skill content referenced Claude-specific tools (`Read`, `Edit`, `Write`, `TodoWrite`, `TaskCreate/TaskUpdate`, `Skill`). These were either:
- Removed (tool-specific invocation instructions)
- Generalized to describe the intent (e.g., "read the file" instead of "use the Read tool")

### Skill Trigger Mechanism

Claude Code loads skills dynamically via the `Skill` tool based on `description` matching. In Gemini, all content in `GEMINI.md` is available as persistent context — there is no on-demand loading. This means more context is always present but without the selective loading that Claude Code provides.

### Cross-References Between Skills

Several skills referenced each other by name (e.g., "Read rpi-extending-claude:writing-claude-directives before using this skill"). These cross-references have been preserved as text in GEMINI.md since all content is already present in the same file.

### Supporting Files Not Converted

The following supporting files in the source plugin were not converted as they are Claude/workflow-specific or have no Gemini equivalent:
- `skills/testing-skills-with-subagents/examples/CLAUDE_MD_TESTING.md`
- `skills/writing-claude-directives/graphviz-conventions.dot`
- `skills/writing-claude-directives/long-running-state-patterns.md`

These files can be referenced manually if needed.

## Usage

After linking the extension, Gemini will automatically include the `GEMINI.md` content as context. The extension provides guidance on:

- Creating Claude Code plugins (structure, manifests, components)
- Writing effective agents with good description fields
- Managing plugin marketplaces and version sync
- Maintaining project context files (CLAUDE.md / AGENTS.md)
- Testing skills using a TDD approach
- Writing token-efficient AI directives
- Structuring CLAUDE.md files at project and domain level
