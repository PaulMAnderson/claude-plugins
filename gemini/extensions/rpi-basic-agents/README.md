# rpi-basic-agents Gemini Extension

Converted from the `rpi-basic-agents` Claude Code plugin (v1.1.0).

**Original description:** Core agents for general-purpose tasks. Other plugins expect this to exist.

## Installation

```bash
gemini extensions link /path/to/gemini/extensions/rpi-basic-agents
```

## Conversion Summary

| Component | Source | Output | Notes |
|-----------|--------|--------|-------|
| Manifest | `.claude-plugin/plugin.json` | `gemini-extension.json` | Name and version preserved |
| Skill: using-generic-agents | `skills/using-generic-agents/SKILL.md` | `GEMINI.md` section | Claude model names generalized to Gemini equivalents |
| Skill: doing-a-simple-two-stage-fanout | `skills/doing-a-simple-two-stage-fanout/SKILL.md` | `GEMINI.md` section + `commands/fanout.toml` | TaskCreate/TaskUpdate references removed; user-invocable skill became a command |
| Agent: haiku-general-purpose | `agents/haiku-general-purpose.md` | `GEMINI.md` (model guidance) | No direct equivalent; model selection guidance folded into using-generic-agents section |
| Agent: sonnet-general-purpose | `agents/sonnet-general-purpose.md` | `GEMINI.md` (model guidance) | Same as above |
| Agent: opus-general-purpose | `agents/opus-general-purpose.md` | `GEMINI.md` (model guidance) | Same as above |
| Hook: SessionStart | `hooks/hooks.json` + `hooks/session-start.sh` | `GEMINI.md` (context) | Session hooks have no Gemini equivalent; guidance folded into context |
| MCP | (none) | N/A | No `.mcp.json` present |

## What Was Converted

### Commands
- `/fanout` — Runs a two-stage fan-out analysis on a large corpus using parallel Worker, Critic, and Summarizer subagents.

### GEMINI.md Context
The extension provides two context sections that Gemini loads automatically:

1. **Using Generic Agents** — Guidance on when to use lightweight vs. standard vs. advanced models (adapted from Claude's Haiku/Sonnet/Opus model guidance).
2. **Two-Stage Fan-Out Analysis** — Full orchestration workflow for analyzing large corpora with parallel agents.

## Limitations and Not-Converted Items

### Agents (haiku/sonnet/opus-general-purpose)

Claude Code agents are typed subagents that can be launched with `rpi-basic-agents:sonnet-general-purpose` as a `subagent_type`. Gemini CLI has no equivalent typed-subagent system. The behavioral content of these agents (check for skills, execute the caller's prompt) is baked into default Gemini behavior and does not require explicit conversion.

Other plugins that reference `rpi-basic-agents:sonnet-general-purpose` as a subagent type will need their invocation patterns updated when converted to Gemini.

### SessionStart Hook

The hook injected a reminder at session start to use the `using-generic-agents` skill when working with generic agents. Gemini CLI has no hook system. The equivalent guidance is now in `GEMINI.md` and is loaded as persistent context.

### compute_layout.py

The original skill bundled a Python script for precise layout calculations. This script is not included in the Gemini extension. The `fanout` command includes inline computation instructions using `python3 -c "..."` shell invocations as a substitute.

### TaskCreate / TaskUpdate / TodoWrite

The fanout skill used Claude-specific task management tools (TaskCreate, TaskUpdate, TodoWrite) to track worker/critic dependencies. These have no Gemini equivalent. The `fanout` command omits task tracking — orchestration state is tracked via the output files in the temp directory instead.

## Usage

### Fan-Out Analysis

```
/fanout Analyze all Python files in src/ for security vulnerabilities
```

Or invoke it interactively without arguments and the command will ask for the corpus and effort level.

### Model Selection Guidance

The GEMINI.md context is automatically available in every session. When deciding which model tier to use for a subtask, refer to the "Using Generic Agents" section for guidance on lightweight vs. standard vs. advanced model selection.
