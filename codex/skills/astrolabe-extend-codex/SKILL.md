---
name: "astrolabe-extend-codex"
description: "Create or maintain Codex skills, AGENTS.md project context, reusable workflow directives, and skill distribution using the Astrolabe extension and validation practices."
---

# Extend Codex using supported mechanisms

Read [extension guidance](references/extending.md) for the requested mode. Inspect actual local capabilities and current official documentation before configuring version-dependent features. Prefer the installed `skill-creator` for skill authoring and `plugin-creator` for Codex plugin packaging when available; their absence does not justify inventing a manifest or tool.

Map the original extension concepts to their purpose:

- Skills/directives → narrowly triggered `SKILL.md` instructions and linked references.
- Project librarian and instruction files → verified `AGENTS.md` maintenance.
- Agent definitions → bounded role briefs and native subagents when exposed/authorized; explicit local role passes otherwise.
- Plugin/marketplace maintenance → supported Codex packaging/distribution with validated paths and preserved attribution, using current schema.
- Skill testing → realistic scenarios and observable outputs, structural validation plus bounded behavioral evaluation.

Do not copy vendor tool names/model tiers, install lifecycle hooks by guessing event schemas, or alter unrelated global configuration. Skills support the user's authorization; they do not add universal approval loops or permission to publish.
