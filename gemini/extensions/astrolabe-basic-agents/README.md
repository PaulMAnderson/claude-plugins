# Astrolabe basic agents for Gemini CLI

This extension carries general-purpose agent roles and guidance for choosing a model and coordinating research tasks. Its `/fanout` command divides a large investigation into worker, critic, and synthesis steps. The role instructions are in `agents/`, with shared guidance in `GEMINI.md`.

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-basic-agents
```

The `SessionStart` hook in `hooks/` emits guidance for choosing a general-purpose agent. For the planning workflow, also link [astrolabe-plan-and-execute](../astrolabe-plan-and-execute/README.md).
