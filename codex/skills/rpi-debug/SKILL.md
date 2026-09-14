---
name: "rpi-debug"
description: "Diagnose unexpected behavior, failing tests, builds, or integrations using root-cause investigation and hypothesis-driven regression fixes in the RPI workflow."
---

# Diagnose before fixing

1. Read the complete error and reproduce with the smallest relevant command/input. Record expected vs actual behavior, environment, version, exit code, and reproducibility. Inspect recent changes and existing reports.
2. Trace the failing data/control path to its origin. Across components, capture input/output and relevant configuration at each boundary. Avoid dumping secrets or entire datasets. Compare with a working example and primary documentation; enumerate concrete differences before selecting a cause.
3. State one falsifiable hypothesis and use the smallest experiment that distinguishes it from alternatives. Change one cause at a time. If disproved, preserve the evidence and revise the hypothesis rather than stacking speculative fixes.
4. Write a behavioral regression test reproducing the defect, confirm the intended failure, implement the cause-level fix, and run the regression plus affected checks. Add validation at genuinely distinct boundaries when invalid data can enter through multiple paths; avoid identical adjacent checks.
5. After three unsuccessful fixes, revisit assumptions and architecture. Diagnose a smaller case, investigate a different boundary, or surface the specific unresolved decision. Do not perform an unchanged fourth attempt.
6. Use [rpi-review](../rpi-review/SKILL.md) for material fixes and [rpi-context](../rpi-context/SKILL.md) for ongoing work. Report root cause, change, observed evidence, and remaining uncertainty. If the environment prevents reproduction, describe what is and is not verified; do not manufacture a passing result.
