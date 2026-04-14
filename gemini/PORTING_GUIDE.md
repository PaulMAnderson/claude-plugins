# Claude to Gemini Extension Porting Guide

This document provides detailed instructions for converting a Claude Code plugin into a Gemini CLI extension. It is intended for AI agents to ensure consistency and efficiency in the porting process.

## 1. Quick Mapping Reference

| Component | Claude Code | Gemini CLI |
|-----------|-------------|------------|
| **Manifest** | `.claude-plugin/plugin.json` | `gemini-extension.json` |
| **Context** | `GEMINI.md` (root) | `GEMINI.md` (root) |
| **Commands** | `commands/*.md` | `commands/*.toml` |
| **Agents** | `agents/*.md` | `agents/*.md` |
| **Skills** | `skills/*/SKILL.md` | `skills/*/SKILL.md` |
| **Hooks** | `hooks/hooks.json` | `hooks/hooks.json` |
| **Root Var** | `${CLAUDE_PLUGIN_ROOT}` | `${extensionPath}` |
| **Workspace Var** | `${CLAUDE_PROJECT_DIR}` | `${workspacePath}` |

---

## 2. Manifest Conversion

### Claude (`plugin.json`)
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "..."
}
```

### Gemini (`gemini-extension.json`)
```json
{
  "name": "my-extension",
  "version": "1.0.0"
}
```
*Note: Description is usually omitted in the JSON as it's often covered in README.md or GEMINI.md.*

---

## 3. Commands Conversion

Claude uses Markdown files for commands; Gemini uses TOML.

### Claude (`commands/my-cmd.md`)
```markdown
---
description: Run something
---
# Command Name
Prompt template using $ARGUMENTS
```

### Gemini (`commands/my-cmd.toml`)
```toml
description = "Run something"
prompt = """
Prompt template using {{args}}
"""
```

---

## 4. Agents Conversion

Agent definitions are remarkably similar, but model tiers and tool naming differ.

### Key Changes:
1. **Model Names**: Map Claude models to Gemini tiers:
   - `haiku` / `sonnet` -> `flash`
   - `opus` -> `pro`
2. **Naming**: Claude uses `plugin-name:agent-name`. Gemini uses `agent-name` (namespaced by extension).
3. **Tool Wildcards**: Gemini supports `*` for all tools.

### Example Gemini Agent (`agents/reviewer.md`)
```markdown
---
name: reviewer
description: Expertise in code review.
tools:
  - read_file
  - grep_search
model: pro
---
# Reviewer Persona
System prompt content goes here...
```

---

## 5. Skills Conversion

Skills are the most direct port, with two critical changes in implementation instructions.

### The "Skill" Tool
- **Claude**: Instructions say "Use the `Skill` tool to invoke...".
- **Gemini**: Instructions MUST be updated to "Use the `activate_skill` tool to invoke...".

### Task Management
- **Claude**: Often uses `TaskCreate`, `TaskUpdate`, `addBlockedBy`.
- **Gemini**: MUST be updated to use the `write_todos` tool. Gemini manages a single list of todos with statuses: `pending`, `in_progress`, `completed`, `blocked`.

### User Interaction
- **Claude**: Uses `AskUserQuestion`.
- **Gemini**: MUST be updated to use the `ask_user` tool (supports `choice`, `text`, `yesno`).

---

## 6. Lifecycle Hooks Conversion

Gemini's hook system is robust but uses different event names and requires specific JSON output.

### Event Mapping
- `SessionStart` -> `SessionStart`
- `PostToolUse` -> `AfterTool` (can be filtered by `matcher`)
- `PreToolUse` -> `BeforeTool`
- `UserPromptSubmit` -> `BeforeModel` or `BeforeAgent`

### Hook Implementation Requirements
All Gemini hooks MUST output a valid JSON object to `stdout`:
1. `{"decision": "allow"}` to proceed.
2. `{"decision": "deny", "reason": "..."}` to block.
3. `{"hookSpecificOutput": {"additionalContext": "..."}}` to inject context.

### Parsing the Payload
Gemini hooks receive a JSON payload on `stdin` containing:
- `cwd`: The current working directory (use this instead of environment variables).
- `tool_name` / `tool_input`: For tool-related hooks.
- `hook_event_name`: The event that triggered the hook.

---

## 7. Path and Environment Variables

Always use `${extensionPath}` in `hooks.json` or `commands.toml` to reference files bundled with the extension. Do not rely on hardcoded paths or `CLAUDE_*` environment variables.

In Python/Bash scripts, parse the `cwd` from the hook payload to locate the project's `.rpi` or configuration folders.

---

## 8. Best Practices for Porting

1. **FCIS Compliance**: Ensure all ported code (Python/Bash) follows the Functional Core / Imperative Shell pattern.
2. **Pattern Comments**: Every ported `.py` or `.sh` file should have `# pattern: Functional Core` or `# pattern: Imperative Shell`.
3. **Verification**: After porting, verify the extension by listing it: `gemini extensions list`.
4. **Context Injection**: Use the `SessionStart` hook to restore context from `.rpi/CONTEXT.md` to emulate Claude's session persistence.
