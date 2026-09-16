# Astrolabe research for Gemini CLI

This extension has commands for local codebase investigation, internet research, remote code research, and combined research. Its agent briefs are in `agents/`, skill instructions in `skills/`, and shared context in `GEMINI.md`.

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-research-agents
```

Use `/investigate-codebase` for repository questions, `/research-internet` for current external documentation, `/research-remote-code` for external source, or `/research-combined` when both local and external evidence matter. The planning workflow can use these roles during design and review.
