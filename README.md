# rpi-plugins

Claude Code plugins for design, implementation, and development workflows,
implementing the Research-Plan-Implement (RPI) methodology.

This is **Paul Anderson's fork** of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins).
It diverges from upstream in: RPI branding, integrated Context Engineering (CE) features,
context monitoring, and compression-aware file templates.

The big stick in this repository is `rpi-plan-and-execute`, which implements an "RPI" (research-plan-implement) loop that does a really good job of avoiding hallucination in the planning stages, adhering to high-level product requirements, avoiding drift between design planning and implementation planning, and reviewing the results such that you get out the other end not just what you asked for, but what you actually wanted.

## Using `rpi-plan-and-execute`
More in [the README for the plugin](plugins/rpi-plan-and-execute/README.md), and it's worth skimming, but here's a quickstart:

```
Rough Idea
    │
    ▼
/start-design-plan  ──────► Design Document (committed to git)
    │
    ▼
/start-implementation-plan ──► Implementation Plan (phase files)
    │
    ▼
/execute-implementation-plan ──► Working Code (reviewed & committed)
```

**Customization:** Create `.rpi/design-plan-guidance.md` and `.rpi/implementation-plan-guidance.md` in your project to provide project-specific constraints, terminology, and standards. Run `/how-to-customize` for details.

## Plugins

| Plugin | Description |
|--------|-------------|
| **`rpi-getting-started`** | Getting started guide and onboarding for rpi-plugins. Run `/getting-started` to see this README. |
| **`rpi-plan-and-execute`** | Planning and execution workflows for Claude Code. Feed it a decent-sized task and it'll help you get it done in a sustainable and thought-through way |
| **`rpi-house-style`** | House style for software development; Very Opinionated |
| **`rpi-basic-agents`** | Core agents for general-purpose tasks (haiku, sonnet, opus). Other plugins expect this to exist |
| **`rpi-research-agents`** | Agents for research across multiple data sources (codebase, internet, combined); other plugins expect this to exist |
| **`rpi-extending-claude`** | Knowledge skills for extending Claude Code: plugins, commands, agents, skills, hooks, MCP servers. Other plugins expect this to exist |
| **`rpi-hook-skill-reinforcement`** | UserPromptSubmit hook that reinforces skill usage — low-overhead reminder each turn |
| **`rpi-hook-claudemd-reminder`** | PostToolUse hook that reminds to update CLAUDE.md before committing when git commands reveal relevant changes |

## Installation

This repo is a Claude Code **marketplace** — one registration gives you access to all plugins by name.

### Step 1: Register the marketplace

In Claude Code, run:
```
/plugin marketplace add file:///absolute/path/to/rpi-plugins
```

Replace the path with the actual location you cloned the repo to, e.g.:
```
/plugin marketplace add file:///Users/yourname/code/rpi-plugins
```

### Step 2: Install plugins

Install the core set (required by most workflows):
```
/plugin install rpi-basic-agents@rpi-plugins
/plugin install rpi-research-agents@rpi-plugins
/plugin install rpi-plan-and-execute@rpi-plugins
/plugin install rpi-extending-claude@rpi-plugins
```

Optional extras:
```
/plugin install rpi-house-style@rpi-plugins
/plugin install rpi-getting-started@rpi-plugins
/plugin install rpi-hook-claudemd-reminder@rpi-plugins
/plugin install rpi-hook-skill-reinforcement@rpi-plugins
```

Or browse interactively:
```
/plugin browse
```

After installing, restart Claude Code or run `/clear` for changes to take effect.

### Updating

After pulling updates to this repo, reload plugins:
```
/plugin reload
```

### Alternative: shell script

If the native plugin system is unavailable, a shell script installs by copying files directly to `~/.claude/`:
```bash
cd /path/to/rpi-plugins
bash scripts/install.sh                              # installs core set
bash scripts/install.sh rpi-house-style rpi-getting-started  # specific plugins
```

## Repository Structure

```
rpi-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── rpi-getting-started/
│   ├── rpi-plan-and-execute/
│   ├── rpi-house-style/
│   ├── rpi-basic-agents/
│   ├── rpi-research-agents/
│   ├── rpi-extending-claude/
│   ├── rpi-hook-skill-reinforcement/
│   └── rpi-hook-claudemd-reminder/
├── scripts/
│   ├── install.sh
│   └── _merge_hooks.py
└── README.md
```

## Contributing
Issues and pull requests gratefully solicited, except `rpi-house-style` is _my_ house style, and provided for reference, so I might not take contributions there. (You can make your own house-style plugin though and use that instead!)

## Attribution

This repository is a fork of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins).

`rpi-plan-and-execute` and parts of `rpi-extending-claude` are derived from
[`obra/superpowers`](https://github.com/obra/superpowers) by Jesse Vincent (MIT licence).
The original code has been extensively modified. See `plugins/rpi-plan-and-execute/LICENSE.superpowers`.

Some skills in `rpi-house-style` are derived from `obra/superpowers` and others
(notably `property-based-testing`) from the
[Trail of Bits Skills repository](https://github.com/trailofbits/skills).

**Key divergences from upstream `ed3dai/ed3d-plugins`:**
- Renamed from `ed3d-*` to `rpi-*` namespace
- Context Engineering integration (context monitor hook, compression skill)
- CE memory-tier-annotated design and implementation plan templates

## License

The original [obra/superpowers](https://github.com/obra/superpowers) code in this repository is licensed under the MIT License, copyright Jesse Vincent. See `plugins/rpi-plan-and-execute/LICENSE.superpowers`.

All other content is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
