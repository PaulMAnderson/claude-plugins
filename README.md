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
| **`rpi-00-getting-started`** | Getting started guide and onboarding for rpi-plugins. Run `/getting-started` to see this README. |
| **`rpi-plan-and-execute`** | Planning and execution workflows for Claude Code. Feed it a decent-sized task and it'll help you get it done in a sustainable and thought-through way |
| **`rpi-house-style`** | House style for software development; Very Opinionated |
| **`rpi-basic-agents`** | Core agents for general-purpose tasks (haiku, sonnet, opus). Other plugins expect this to exist |
| **`rpi-research-agents`** | Agents for research across multiple data sources (codebase, internet, combined); other plugins expect this to exist |
| **`rpi-extending-claude`** | Knowledge skills for extending Claude Code: plugins, commands, agents, skills, hooks, MCP servers. Other plugins expect this to exist |
| **`rpi-playwright`**| Playwright automation with subagents |
| **`rpi-hook-skill-reinforcement`** | UserPromptSubmit hook that reinforces the need to activate skills—helps make sure skills actually get used. Requires `rpi-extending-claude` to work |
| **`rpi-hook-claudemd-reminder`** | PostToolUse hook that reminds to update CLAUDE.md before committing |

## Installation

### Option A — GitHub (when the repo is published)
```
/plugin marketplace add https://github.com/paulanderson/rpi-plugins.git
/plugin install rpi-plan-and-execute@rpi-plugins
```

### Option B — Local development (working directly in this repo)
```bash
./scripts/install.sh
```
Installs `rpi-basic-agents`, `rpi-research-agents`, and `rpi-plan-and-execute`.
Re-run after pulling changes or switching branches.
Restart Claude Code or `/clear` for changes to take effect.

To install specific plugins only:
```bash
./scripts/install.sh rpi-basic-agents rpi-plan-and-execute
```

## Repository Structure

```
rpi-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── rpi-00-getting-started/
│   ├── rpi-plan-and-execute/
│   ├── rpi-house-style/
│   ├── rpi-basic-agents/
│   ├── rpi-research-agents/
│   ├── rpi-extending-claude/
│   ├── rpi-playwright/
│   ├── rpi-hook-skill-reinforcement/
│   └── rpi-hook-claudemd-reminder/
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
