---
name: "astrolabe-workflow"
description: "Run the Astrolabe research, design, phased implementation, review, and validation workflow for a substantial software change, or explain how to use the Astrolabe skills."
---

# Astrolabe workflow for Codex

## Project state

Before work, follow [the shared entry and exit contract](../astrolabe-workflow/references/project-state.md) with tier `design`: initialize local files, read PROJECT.md and STATUS.md, consult both planned lists, and surface a match before proceeding. On exit, update STATUS.md and append HISTORY.md.

Preserve the chain **user outcome → design → scoped acceptance criteria → phase tasks → implementation → review → verification evidence**. Start at the stage the user requested; reuse existing artifacts rather than restarting.

For a specific Backlog or Roadmap item, invoke `$astrolabe-workflow Start B1` (substitute its ID). Read the item, select an existing tier, and use `start-planned` from the shared state contract. Keep the item listed while work continues. After the requested outcome is verified and the tier is finished, run `complete-planned` to remove it and document the original text and result in HISTORY.md. An explicit ID needs no second confirmation.

Read [the workflow contract](references/workflow.md) before substantial Astrolabe work. It defines progress tracking, quality gates, authorization, and recovery shared by the skills below.

| Request | Skill to read next |
| --- | --- |
| Design a feature; flesh out an idea | [astrolabe-design](../astrolabe-design/SKILL.md) |
| Turn an existing design into executable phases | [astrolabe-plan](../astrolabe-plan/SKILL.md) |
| Implement or resume a phased plan | [astrolabe-implement](../astrolabe-implement/SKILL.md) |
| Review code, fix review issues, validate coverage | [astrolabe-review](../astrolabe-review/SKILL.md) |
| Investigate local code, remote code, or documentation | [astrolabe-research](../astrolabe-research/SKILL.md) |
| Diagnose a failure | [astrolabe-debug](../astrolabe-debug/SKILL.md) |
| Save or restore session and project context | [astrolabe-context](../astrolabe-context/SKILL.md) |
| One-off analysis or small helper function | [astrolabe-quick](../astrolabe-quick/SKILL.md) |
| Apply Paul's coding and technical writing conventions | [astrolabe-house-style](../astrolabe-house-style/SKILL.md) |
| Extend Codex skills, instructions, or packaging | [astrolabe-extend-codex](../astrolabe-extend-codex/SKILL.md) |
| Explicit worker → critic → synthesis fanout | [astrolabe-fanout](../astrolabe-fanout/SKILL.md) |

Users can invoke these with `$astrolabe-design`, `$astrolabe-plan`, or `$astrolabe-implement` and a description or path. Codex can also select skills from natural language. Read linked files directly; no special skill-activation tool is required.

For an end-to-end request, continue across stages after recording each gate. For a design-only or planning-only request, deliver that artifact and a concrete next invocation. A new conversation is optional: checkpoint first, then continue when execution is already authorized.

Customization: read `.astrolabe/design-plan-guidance.md` for domain terms, architecture, and scope; read `.astrolabe/implementation-plan-guidance.md` for coding, tests, review, and commit conventions. Missing guidance is not a blocker. To customize, help write these files from the user's actual preferences; do not invent constraints.
