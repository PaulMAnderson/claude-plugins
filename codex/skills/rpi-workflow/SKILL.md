---
name: "rpi-workflow"
description: "Run the RPI research, design, phased implementation, review, and validation workflow for a substantial software change, or explain how to use the RPI skills."
---

# RPI workflow for Codex

Preserve the chain **user outcome → design → scoped acceptance criteria → phase tasks → implementation → review → verification evidence**. Start at the stage the user requested; reuse existing artifacts rather than restarting.

Read [the workflow contract](references/workflow.md) before substantial RPI work. It defines progress tracking, quality gates, authorization, and recovery shared by the skills below.

| Request | Skill to read next |
| --- | --- |
| Design a feature; flesh out an idea | [rpi-design](../rpi-design/SKILL.md) |
| Turn an existing design into executable phases | [rpi-plan](../rpi-plan/SKILL.md) |
| Implement or resume a phased plan | [rpi-implement](../rpi-implement/SKILL.md) |
| Review code, fix review issues, validate coverage | [rpi-review](../rpi-review/SKILL.md) |
| Investigate local code, remote code, or documentation | [rpi-research](../rpi-research/SKILL.md) |
| Diagnose a failure | [rpi-debug](../rpi-debug/SKILL.md) |
| Save or restore session and project context | [rpi-context](../rpi-context/SKILL.md) |
| One-off analysis or small helper function | [rpi-quick](../rpi-quick/SKILL.md) |
| Apply Paul's coding and technical writing conventions | [rpi-house-style](../rpi-house-style/SKILL.md) |
| Extend Codex skills, instructions, or packaging | [rpi-extend-codex](../rpi-extend-codex/SKILL.md) |
| Explicit worker → critic → synthesis fanout | [rpi-fanout](../rpi-fanout/SKILL.md) |

Users can invoke these with `$rpi-design`, `$rpi-plan`, or `$rpi-implement` and a description or path. Codex can also select skills from natural language. Read linked files directly; no special skill-activation tool is required.

For an end-to-end request, continue across stages after recording each gate. For a design-only or planning-only request, deliver that artifact and a concrete next invocation. A new conversation is optional: checkpoint first, then continue when execution is already authorized.

Customization: read `.rpi/design-plan-guidance.md` for domain terms, architecture, and scope; read `.rpi/implementation-plan-guidance.md` for coding, tests, review, and commit conventions. Missing guidance is not a blocker. To customize, help write these files from the user's actual preferences; do not invent constraints.
