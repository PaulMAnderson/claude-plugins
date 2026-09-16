# Astrolabe project-instruction reminder for Gemini CLI

This extension registers an `AfterTool` hook for shell commands. When a git command suggests that project contracts may have changed, `hooks/git-command-reminder.py` reminds the agent to review relevant project instructions before committing.

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-hook-claudemd-reminder
```

The hook is advisory. It does not edit `CLAUDE.md` or other instruction files by itself.
