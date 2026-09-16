# Astrolabe project-instruction reminder for Claude Code

This plugin's `PostToolUse` hook watches Bash calls. After a substantive `git status` or `git log`, it reminds the agent to consider updating `CLAUDE.md` if contracts, APIs, or domain structure changed. The hook is advisory and does not edit files.

The reminder points to `astrolabe-extending-claude:project-claude-librarian` and the project-context guidance. Install this plugin from the [Astrolabe marketplace](../../README.md#claude-code) if you want the reminder.
