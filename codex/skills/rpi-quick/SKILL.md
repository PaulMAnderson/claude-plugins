---
name: "rpi-quick"
description: "Perform a one-off analysis or build a small helper function with concise intent, appropriate verification, and an RPI session log, without formal design or phase-plan documents."
---

# Lightweight RPI work

Use for a bounded, single-session analysis or helper. If the request changes architecture, spans sessions, or explicitly asks for formal planning/review, use [rpi-workflow](../rpi-workflow/SKILL.md) instead.

1. Read existing `.rpi/CONTEXT.md`, `.rpi/PROJECT.md`, and applicable project guidance. Identify input, expected output, and success criteria; clarify only consequential missing information.
2. State a short intent in chat. For a helper, include its input/output contract and verification. Append intent to `.rpi/SESSION.md`. Do not create design or implementation plan documents for this path.
3. Implement using actual project patterns and applicable [house style](../rpi-house-style/SKILL.md). For analysis, record data selection, units, missing-value policy, reproducibility settings, and the requested output artifact.
4. Verify behavior with meaningful tests or direct result/operational checks proportional to the task. For scientific outputs inspect dimensions, units, boundary cases, and consistency with an independent calculation or known reference when appropriate. Inspect generated figures/tables before delivering.
5. Append a dated outcome to `.rpi/SESSION.md`: result/artifact path, exact checks, limitations. Report the result and evidence without implying unexecuted checks passed.
