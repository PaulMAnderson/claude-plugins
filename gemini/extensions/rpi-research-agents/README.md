# rpi-research-agents Gemini Extension

Converted from the `rpi-research-agents` Claude Code plugin (v1.0.1).

## Overview

Provides research workflows for investigating local codebases, searching the internet, and examining external library source code.

## Component Mapping

| Claude Plugin | Gemini Extension | Notes |
|---|---|---|
| `skills/investigating-a-codebase/SKILL.md` | `GEMINI.md` | Consolidated into context |
| `skills/researching-on-the-internet/SKILL.md` | `GEMINI.md` | Consolidated into context |
| `agents/codebase-investigator.md` | `commands/investigate-codebase.toml` | Agent → command |
| `agents/internet-researcher.md` | `commands/research-internet.toml` | Agent → command |
| `agents/combined-researcher.md` | `commands/research-combined.toml` | Agent → command |
| `agents/remote-code-researcher.md` | `commands/research-remote-code.toml` | Agent → command |

## Commands

- `/investigate-codebase <question>` - Investigate the local codebase to answer questions about structure, patterns, and existing code
- `/research-internet <question>` - Research a topic using web sources for current docs, library patterns, and best practices
- `/research-combined <question>` - Research using both local codebase and web sources together
- `/research-remote-code <question>` - Examine actual source code from an external repository by cloning it locally

## Installation

```bash
gemini extensions link /path/to/gemini/extensions/rpi-research-agents
```

## Limitations

The original plugin used Claude Code's multi-agent architecture, where a top-level agent could dispatch sub-agents using the Task tool. Gemini CLI has no equivalent multi-agent dispatch mechanism. The conversions handle this as follows:

- Each agent is a standalone command with the research methodology embedded directly in the prompt.
- The `combined-researcher` command instructs Gemini to perform both codebase and internet research in a single session rather than delegating to separate agents.
- Model selection (the original plugin used `haiku` for agents) is not configurable per-command in Gemini CLI extensions.
- The `user-invocable: false` flag on skills has no Gemini equivalent; all methodology is now embedded in the relevant command prompts and in `GEMINI.md` as ambient context.
