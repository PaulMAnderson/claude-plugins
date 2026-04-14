# rpi-hook-skill-reinforcement (Gemini Extension)

Converted from the Claude Code plugin `rpi-hook-skill-reinforcement` v1.0.1.

## Original Plugin

- **Name**: rpi-hook-skill-reinforcement
- **Version**: 1.0.1
- **Description**: EXPERIMENTAL. A UserPromptSubmit hook that directs the model to consider and activate useful skills.
- **Author**: Ed

## What the Original Plugin Did

The plugin registered a single `UserPromptSubmit` hook (`hook-reminder.sh`). On every user prompt submission, the hook injected the following instruction into the model's context as `additionalContext`:

> Before responding to this prompt, consider whether you have any skills that apply. Your available skills are listed in your system context. If ANY skill applies to this task and has not been activated in this session, you MUST use the Skill tool to activate it. Do NOT skip this step.

This nudged Claude to check for and activate relevant skills before answering each prompt.

## Conversion Summary

| Component | Claude Code | Gemini Equivalent | Status |
|-----------|-------------|-------------------|--------|
| `UserPromptSubmit` hook | `hooks/hooks.json` + `hook-reminder.sh` | No equivalent | Not convertible |
| Manifest | `plugin.json` | `gemini-extension.json` | Converted |

## What Was NOT Converted

### `UserPromptSubmit` hook

The `UserPromptSubmit` hook event has no equivalent in the Gemini CLI extension system. Gemini extensions do not support lifecycle hooks that inject context or intercept user prompts before they are processed.

The specific capability — injecting an `additionalContext` reminder on every prompt — cannot be reproduced through any Gemini extension mechanism.

## Alternative Approaches for Gemini

Since Gemini CLI does not support prompt-submit hooks, consider these alternatives:

1. **GEMINI.md system context**: Place a standing instruction in your project or user-level `GEMINI.md` file reminding Gemini to check available extensions before responding. This is a static reminder rather than a per-prompt injection, but achieves a similar effect.

   Example addition to `GEMINI.md`:
   ```
   Before responding to any prompt, consider whether any available extension or tool applies to the task. If one does, use it.
   ```

2. **Extension `contextFileName`**: If a future Gemini CLI release supports per-extension context injection, the content could be placed in a context file referenced by `gemini-extension.json`.

3. **Manual workflow**: Include the reminder in your standard Gemini CLI prompt template or alias.

## Installation

```sh
gemini extensions link /Users/paul/Claude/claude-plugins/gemini/extensions/rpi-hook-skill-reinforcement
```

Or for user-wide installation, link from your Gemini extensions directory.

## Notes

This extension currently only provides the manifest (`gemini-extension.json`) with name and version. Its primary functionality (the prompt-submit hook) is not supported by the Gemini CLI extension API and must be implemented via the alternative approaches described above.
