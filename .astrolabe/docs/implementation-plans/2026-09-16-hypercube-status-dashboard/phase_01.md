---
phase: 1
title: Watch list and collector
context-budget: small
files-required:
  - .astrolabe/docs/design-plans/2026-09-16-hypercube-status-dashboard.md
  - docs/astrolabe-state-format.md
depends-on: []
---
# B1 phase 1
Codebase verified: 2026-09-16; current branch feature/astrolabe-project-tracking. Python standard library is the existing state tooling dependency.

## Acceptance criteria coverage
- AC1.1: A valid watch list path registers exactly its listed projects; unlisted projects remain invisible.
- AC1.2: Duplicate names or malformed list entries produce a clear configuration error.
- AC2.1: A valid schema-1 STATUS.md yields all five frontmatter fields and its summary.
- AC2.2: Missing, unreadable, malformed, or unsupported status files yield per-project errors while other projects still load.
- AC2.3: A later file update appears on the next request without restart (collector portion).

## Task progress
| Task | Status | Report |
| --- | --- | --- |
| 1 | completed | `.astrolabe/runs/hypercube-status-dashboard/reports/phase-1-execute.md` |

<!-- START_TASK_1 -->
### Task 1: Implement config, parser, collector
Type: functionality. Depends on: none. Verifies: AC1.1–AC2.3.
Files: create `hypercube/status.py`, `hypercube/__init__.py`, `tests/test_hypercube_status.py`.
Implement `load_watch_list(path)`, `parse_status(text)`, and `collect(projects)` with precise design contract. Config errors are fatal; per-project status errors are records. Parse and validate all schema fields. Use fresh reads per collection.
Testing: temporary project directories with valid, changed, invalid, and missing files; duplicate/invalid config. Assert only registered projects appear and other projects survive one error.
Verification: `python3 -m unittest discover -s tests -p 'test_hypercube*.py'` exits 0.
<!-- END_TASK_1 -->

## Phase validation
Run focused unit tests and inspect the phase diff from its recorded baseline.
## Review record
Self-review complete; see `.astrolabe/runs/hypercube-status-dashboard/reports/phase-1-review.md`.
