---
title: Astrolabe · Docs · Implementation Plans · 2026 09 16 Hypercube Status Dashboard · Phase 02
version: 2
id: 9db948f82a7376bad76271e2b736ff53
createdAt: 2026-09-17T11:58:29.029Z
updatedAt: 2026-09-17T11:58:29.029Z
---
> Imported from `.astrolabe/docs/implementation-plans/2026-09-16-hypercube-status-dashboard/phase_02.md` on 2026-09-17. The original file remains in place.

---

---
phase: 2
title: Web interface and CLI
context-budget: small
files-required:
  - .astrolabe/docs/design-plans/2026-09-16-hypercube-status-dashboard.md
  - .astrolabe/docs/implementation-plans/2026-09-16-hypercube-status-dashboard/phase_01.md
depends-on: [1]
---
# B1 phase 2
Codebase verified: 2026-09-16; no existing web app in this checkout.

## Acceptance criteria coverage
- AC3.1: GET / displays registered projects and their status or error.
- AC3.2: Project names and summary text are escaped as HTML.
- AC3.3: Unknown paths return 404 and the server binds to the configured address/port.
- AC2.3: A later file update appears on the next request without restart.

## Task progress
| Task | Status | Report |
| --- | --- | --- |
| 1 | completed | `.astrolabe/runs/hypercube-status-dashboard/reports/phase-2-execute.md` |

<!-- START_TASK_1 -->
### Task 1: Implement HTTP page and CLI
Type: functionality. Depends on: phase 1. Verifies: AC2.3, AC3.1–AC3.3.
Files: create `hypercube/web.py`, `hypercube/__main__.py`, `tests/test_hypercube_web.py`; modify `README.md`.
Implement escaped table UI, GET /, 404 for other routes, and argparse options `--config`, `--host` (default 127.0.0.1), `--port` (default 8765). Reload status each request. Document watch-list format and invocation.
Testing: local ephemeral HTTP server with temporary watch list. Assert response fields, escaped payload, 404, and changed file reflected on subsequent request.
Verification: `python3 -m unittest discover -s tests -p 'test_hypercube*.py'` exits 0; `python3 -m hypercube --help` exits 0.
<!-- END_TASK_1 -->

## Phase validation
Run focused suite and inspect complete implementation diff and documentation.
## Review record
Self-review complete; see `.astrolabe/runs/hypercube-status-dashboard/reports/phase-2-review.md`.
