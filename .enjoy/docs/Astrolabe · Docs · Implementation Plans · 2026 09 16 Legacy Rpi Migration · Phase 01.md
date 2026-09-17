---
title: Astrolabe · Docs · Implementation Plans · 2026 09 16 Legacy Rpi Migration · Phase 01
version: 2
id: 819840f273afcb92d55e7073a83e88d8
createdAt: 2026-09-17T11:58:29.134Z
updatedAt: 2026-09-17T11:58:29.134Z
---
> Imported from `.astrolabe/docs/implementation-plans/2026-09-16-legacy-rpi-migration/phase_01.md` on 2026-09-17. The original file remains in place.

---

---
phase: 1
title: Migration engine
context-budget: small
files-required:
  - .astrolabe/docs/design-plans/2026-09-16-legacy-rpi-migration.md
  - docs/astrolabe-state-format.md
depends-on: []
---
# B2 phase 1
Codebase verified: 2026-09-16 at bf4fd04; Python 3.12.11; standard library only.
## Acceptance criteria coverage
AC1.1 valid core state; AC1.2 session preserved; AC1.3 guidance, plans, unknown files; AC2.1 dry-run no write; AC2.2 preflight conflict; AC2.3 staging cleanup; AC2.4 idempotent rerun. Full wording in design.
## Task progress
| Task | Status | Report |
| --- | --- | --- |
| 1 | completed | `.astrolabe/runs/legacy-rpi-migration/reports/phase-1-execute.md` |
<!-- START_TASK_1 -->
### Task 1: Implement migration engine
Type: functionality. Depends on: none. Verifies: AC1.1–AC2.4.
Files: create `scripts/migrate_rpi_project.py`, `tests/test_migrate_rpi_project.py`.
Implement `plan(root)`, `migrate(root, dry_run=False)` and custom `MigrationError`. Preflight source and target, reject symlinks recursively, create temporary sibling stage, copy tree, generate valid defaults and import entry, then rename. Preserve source and cleanup stage on failure. Tests use temporary projects and mock a copy failure to prove cleanup.
Verification: `python3 -m unittest discover -s tests -p 'test_migrate_rpi_project.py' -v` exit 0.
<!-- END_TASK_1 -->
## Phase validation
Focused tests and diff inspection.
## Review record
Self-review complete: `.astrolabe/runs/legacy-rpi-migration/reports/phase-1-review.md`.
