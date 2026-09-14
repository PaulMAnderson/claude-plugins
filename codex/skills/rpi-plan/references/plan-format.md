# Phase and test requirement formats

Use the following structure with concrete project values. `phase_1.md` from existing RPI plans is also acceptable; preserve numbering and resolve dependencies numerically. Do not silently overwrite existing phase files.

```markdown
---
phase: 1
title: Actual phase title
context-budget: small
files-required:
  - docs/design-plans/YYYY-MM-DD-feature.md
  - src/existing_module.py
depends-on: []
---

# Feature implementation plan — phase 1
Goal: One cohesive outcome.
Architecture: The relevant approach and exact boundaries.
Tech stack: Verified tools and versions.
Scope: Phase 1 of N (identify any subset of a larger design).
Codebase verified: actual date/time and revision.

## Acceptance criteria coverage
Copy the scoped IDs AND full criterion text from the design.

## Task progress
| Task | Status | Report |
| --- | --- | --- |
| 1 | pending | Not yet created |

<!-- START_TASK_1 -->
### Task 1: Concrete outcome
Type: functionality (or infrastructure/documentation).
Depends on: none, or earlier task IDs and supplied interfaces.
Verifies: feature.AC1.1, feature.AC1.2 (full text in coverage section).
Files:
- Create: exact/path
- Modify: exact/path, named symbol (line reference verified now)
- Test: tests/exact_path.py (unit/integration/e2e)

Implementation: complete behavior, exact signatures/data shapes/values,
error cases, integration points, and relevant algorithms.

Testing: assertions that distinguish correct from incorrect behavior for
each AC; regression reproduction where applicable; fixtures and setup.

Verification: exact command, working directory, expected result.
Commit: suggested message only if commits are authorized.
<!-- END_TASK_1 -->

## Phase validation
Commands and expected integration/build/test outcomes for this phase.

## Review record
Baseline, review scope, findings/report paths, cycles, and resolutions.
```

Subcomponents may wrap related tasks with `<!-- START_SUBCOMPONENT_A (tasks 1-3) -->` and `<!-- END_SUBCOMPONENT_A -->`; task markers still enclose each complete task. These markers preserve compatibility with the source plan convention and allow focused extraction. Keep required interfaces with the task brief, including exact values; do not summarize away binding details.

Create `test-requirements.md` after plan review:

| AC ID | Exact criterion | Phase/task | Mode | Test file and asserted behavior, or manual steps | Reason if manual |
| --- | --- | --- | --- | --- | --- |
| feature.AC1.1 | Actual criterion text | 1/1 | automated | Exact test path and meaningful assertion | — |

During final coverage review, augment this with implemented test symbols, evidence paths, and statuses. A test name alone is not evidence. Cross-phase ACs need a final integration assertion. Manual steps include prerequisites, action, expected observation, cleanup if needed, and who must run them. Leave unexecuted steps pending.
