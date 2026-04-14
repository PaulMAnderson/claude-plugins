# rpi-hook-claudemd-reminder (Gemini CLI Extension)

## Original Plugin

- **Name**: rpi-hook-claudemd-reminder
- **Version**: 1.0.0
- **Description**: A PostToolUse hook that reminds to invoke `project-claude-librarian` before committing when `git status` or `git log` reveals changes that may warrant CLAUDE.md updates.

## What the Claude Code Plugin Did

The plugin registered a single `PostToolUse` hook on the `Bash` tool. After every Bash tool call, `git-command-reminder.py` ran and inspected the command that was executed. If the command matched `git status` or a substantive `git log` (not a quick `--oneline -N` variant), the hook injected an `additionalContext` reminder into the model's context:

> "If you're about to commit changes that affect contracts, APIs, or domain structure, consider invoking `project-claude-librarian` (rpi-extending-claude:project-claude-librarian) to review and update CLAUDE.md files before committing."

This hook relied on Claude Code's `PostToolUse` event system and the `hookSpecificOutput.additionalContext` mechanism to surface the reminder without blocking execution.

## Conversion Summary

| Component | Claude Code | Gemini Equivalent | Status |
|-----------|-------------|-------------------|--------|
| PostToolUse hook (Bash) | Injects reminder after git commands | No equivalent | Not convertible |
| Tool restriction / blocking | N/A — hook was notification-only | `excludeTools` | N/A |

No `excludeTools` entries were added because this hook did not block any tools.

## What Could NOT Be Converted

### PostToolUse notification hook

The core behavior — inspecting a just-executed tool's input and injecting context back into the model — has no equivalent in the Gemini CLI extension system. The Gemini extension API supports:

- `gemini-extension.json` manifest (name, version, mcpServers, excludeTools, coreTools)
- `GEMINI.md` for persistent context injected at session start
- `/commands/*.toml` for slash commands

None of these mechanisms can react to individual tool calls after they execute.

## Alternative Approaches for Gemini

1. **Static reminder in GEMINI.md**: Add a standing instruction to `GEMINI.md` reminding Gemini to consider CLAUDE.md/GEMINI.md updates before committing. This is always-on rather than triggered by git commands, but covers the same intent.

2. **Git hook (pre-commit)**: Install a `pre-commit` shell script in the repository that prints the reminder. This operates at the git layer and is model-agnostic.

3. **Slash command**: Create a `commands/check-claudemd.toml` command that the user invokes manually before committing to prompt a GEMINI.md review.

## Installation

```
gemini extensions link /Users/paul/Claude/claude-plugins/gemini/extensions/rpi-hook-claudemd-reminder
```

Note: This extension contains only the manifest. The hook behavior described above cannot be replicated in Gemini CLI and must be handled via one of the alternative approaches listed above.
