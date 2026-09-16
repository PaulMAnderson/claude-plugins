---
phase: 2
title: CLI and guide
context-budget: small
files-required:
  - .astrolabe/docs/design-plans/2026-09-16-legacy-rpi-migration.md
  - .astrolabe/docs/implementation-plans/2026-09-16-legacy-rpi-migration/phase_01.md
depends-on: [1]
---
# B2 phase 2
Codebase verified: 2026-09-16 at bf4fd04; existing root README and Python script conventions.
## Acceptance criteria coverage
AC2.1 dry-run no changes; AC2.2 errors; AC2.4 repeated run; CLI evidence for AC1.1–AC1.3. Full wording in design.
## Task progress
| Task | Status | Report |
| --- | --- | --- |
| 1 | completed | `.astrolabe/runs/legacy-rpi-migration/reports/phase-2-execute.md` |
<!-- START_TASK_1 -->
### Task 1: Expose CLI and instructions
Type: functionality/documentation. Depends on: phase 1. Verifies: AC1.1–AC1.3, AC2.1, AC2.2, AC2.4.
Files: create `scripts/migrate-rpi-project.py`; modify `README.md`, `docs/astrolabe-state-format.md`, `tests/test_migrate_rpi_project.py`.
Expose `PROJECT_ROOT` and `--dry-run`, print mapping or clear error. Document safe usage, conflict behavior, preserved originals, and new file mapping. Exercise CLI with subprocess and temporary project.
Verification: focused test suite and `python3 scripts/migrate-rpi-project.py --help` exit 0.
<!-- END_TASK_1 -->
## Phase validation
Full Python tests, journaling check, diff review.
## Review record
Self-review complete: `.astrolabe/runs/legacy-rpi-migration/reports/phase-2-review.md`.
