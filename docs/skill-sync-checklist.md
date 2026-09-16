# Astrolabe skill sync checklist

When changing a tier skill or state contract, inspect and update all three distributions:

1. Claude Code: `plugins/astrolabe-plan-and-execute/skills/`, `references/project-state.md`, `scripts/astrolabe-state.py`, and matching `commands/`.
2. Codex: `codex/skills/astrolabe-*/SKILL.md`, `codex/skills/astrolabe-workflow/references/project-state.md`, and `scripts/project_state.py` within that skill.
3. Gemini CLI: `gemini/extensions/astrolabe-plan-and-execute/skills/`, `references/project-state.md`, `scripts/astrolabe-state.py`, and matching `commands/`.

Verify the same `.astrolabe/` schema, entry and exit outcomes, Backlog/Roadmap consultation, Spec resume behavior, and planned-item lifecycle. A start by ID keeps the item listed; verified completion removes it, appends its original text and result to HISTORY.md, and reserves the ID permanently. Keep tool vocabulary native to each platform (`AskUserQuestion`/Task tools for Claude, Codex user input and plan tools, `ask_user`/`write_todos` for Gemini). Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s codex/tests -v` and install/load smoke checks after syncing.
