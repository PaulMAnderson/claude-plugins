# rpi-getting-started — Gemini CLI Extension

Converted from the `rpi-getting-started` Claude Code plugin (v1.0.0).

**Original description:** Getting started guide and onboarding for rpi-plugins.

## Component Mapping

| Claude Component | Gemini Equivalent | Notes |
|---|---|---|
| `commands/getting-started.md` | `commands/getting-started.toml` | Converted |
| Skills | GEMINI.md | None present |
| Agents | commands/ | None present |
| Hooks | `excludeTools` | None present |
| `.mcp.json` | `gemini-extension.json` mcpServers | None present |

## Installation

```
gemini extensions link /Users/paul/Claude/claude-plugins/gemini/extensions/rpi-getting-started
```

## Usage

After linking, run the command in Gemini CLI:

```
/getting-started
```

This displays the first two sections of the rpi-plugins README, stopping before the Installation section.

## Limitations

- The command references `@{../../README.md}` using a relative path. Ensure the extension is linked from a location where that relative path resolves to the rpi-plugins repository root README.
