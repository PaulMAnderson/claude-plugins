---
name: "rpi-design"
description: "Develop an RPI design plan from a feature idea, requirements, or brainstorming, with investigated architecture, a Definition of Done, acceptance criteria, and implementation phases."
---

# Design a change

Read [the shared workflow contract](../rpi-workflow/references/workflow.md). Track context gathering, clarification, Definition of Done, alternatives, design writing, and handoff as explicit checklist items in the design working file.

1. Inspect the existing project and provided materials before asking for information. Read `.rpi/design-plan-guidance.md` if present. Use [rpi-research](../rpi-research/SKILL.md) for uncertain codebase or dependency facts. Distinguish observed paths/interfaces from proposed additions.
2. Clarify only consequential gaps in scope, terminology, constraints, success/failure behavior, and intended consumers. Preserve answers already provided. State the Definition of Done: deliverables, observable success, and exclusions actually agreed. Record its authorization/assumption status immediately in `docs/design-plans/YYYY-MM-DD-<slug>.md`, using the current date and a descriptive slug.
3. Compare two or three plausible approaches when meaningful alternatives exist. Recommend one with concrete tradeoffs, existing patterns, and rationale. Explain components, data flow, dependencies, interfaces, errors, and relevant operational or scientific constraints. Revisit the Definition of Done if design changes it; surface material scope changes before proceeding with dependent work.
4. Write directional architecture with exact public contracts (types, request/response shapes, schema, units, array dimensions, error behavior). Keep task-level implementation out of the design. Include investigated paths, reused patterns, justified divergences, and rejected approaches.
5. Derive scoped acceptance criteria `{slug}.AC{N}.{M}` from every Definition of Done item: success variations, important failures, boundaries, and cross-component behavior. Preserve exact values and observable outcomes. Check coverage in both directions so neither deliverables nor criteria drift. Present the criteria for review; use supplied requirements and existing authorization without adding a mandatory confirmation loop.
6. Define cohesive sequential phases, each with components, dependencies, covered ACs, and a verifiable end state. Functionality and its tests belong in the same phase. Prefer manageable batches around eight phases; split larger work into linked plans with explicit coverage instead of truncating requirements or refusing solely on a count.
7. Finish summary and glossary from the completed body. Review the document from a fresh reader's perspective: unclear summary or unexplainable terms signal unclear design. Remove unfinished scaffold text. Read [the design template](references/design-template.md) for the expected structure.
8. Save a context checkpoint with [rpi-context](../rpi-context/SKILL.md). If end-to-end work is authorized, proceed to [rpi-plan](../rpi-plan/SKILL.md). Otherwise deliver the design path and `$rpi-plan <absolute-design-path>`.
