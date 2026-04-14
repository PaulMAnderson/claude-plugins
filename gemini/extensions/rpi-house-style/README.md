# rpi-house-style Gemini Extension

Converted from the `rpi-house-style` Claude Code plugin.

## Original plugin

- **Name:** rpi-house-style
- **Version:** 1.0.2
- **Description:** Stylistic particulars for writing code and English.
- **Author:** Ed (ed@ed3d.net)

## Conversion summary

| Claude component | Gemini equivalent | Status |
|-----------------|-------------------|--------|
| `.claude-plugin/plugin.json` | `gemini-extension.json` | Converted |
| `skills/coding-effectively/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/defense-in-depth/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/howto-code-in-matlab/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/howto-code-in-python/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/howto-code-in-r/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/howto-develop-with-mysql/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/howto-functional-vs-imperative/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/writing-for-a-technical-audience/SKILL.md` | Section in `GEMINI.md` | Converted |
| `skills/writing-good-tests/SKILL.md` | Section in `GEMINI.md` | Converted |
| `CLAUDE.md` | Incorporated into `GEMINI.md` intro | Converted |
| `agents/` (empty) | N/A | No agents present |
| `hooks/hooks.json` | N/A | Not present |
| `.mcp.json` | N/A | Not present |
| `commands/` | N/A | No commands present |

## What was converted

**All 9 skills** were consolidated into a single `GEMINI.md` file. Each skill becomes a top-level section. YAML frontmatter was stripped. Claude-specific tool references (Read tool, Grep tool, Bash tool, TaskCreate, TodoWrite) were removed. The substantive coding guidelines, code examples, tables, and red flag lists are fully preserved.

The `CLAUDE.md` context file (which described the plugin's purpose and skill authoring guidelines) was incorporated into the introductory section of `GEMINI.md`.

## What was not converted

- **Skill activation triggers:** Claude skills have `description` fields that control when they are automatically invoked. Gemini CLI loads `GEMINI.md` as static context for every session — there is no equivalent automatic skill selection mechanism. All skills are always in context.

- **`user-invocable: false` flags:** Claude skills can be marked non-user-invocable. This concept has no Gemini equivalent; all content in `GEMINI.md` is passively available as context.

- **Sub-skill references:** The `coding-effectively` skill references other skills by name (e.g., `@skill:howto-functional-vs-imperative`). These references are preserved as prose in the converted file, but the dynamic skill-loading behavior is not replicable in Gemini CLI.

## Limitations

- Gemini CLI has no concept of conditional skill activation. All context in `GEMINI.md` is loaded for every conversation, which increases token usage compared to the Claude plugin's selective loading.
- The FCIS pattern's mandatory file classification comment (added to every code file) depends on discipline enforced through context — this works the same way in Gemini, but there is no hook-based enforcement.

## Installation

```sh
gemini extensions link /path/to/gemini/extensions/rpi-house-style
```

Or add to your Gemini CLI configuration to load automatically.

## Structure

```
rpi-house-style/
├── gemini-extension.json   # Extension manifest
├── GEMINI.md               # Consolidated context (all skills)
└── README.md               # This file
```
