# Astrolabe skill reinforcement hook for Gemini CLI

This extension registers a `BeforeModel` hook in `hooks/hooks.json`. Its current `hook-reminder.sh` returns an allow decision without injecting a reminder. It is a placeholder for optional skill reminders; linking it does not change skill selection today.

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-hook-skill-reinforcement
```

Link the extensions whose skills you want to use. The [root README](../../../README.md) describes the current workflow tiers.
