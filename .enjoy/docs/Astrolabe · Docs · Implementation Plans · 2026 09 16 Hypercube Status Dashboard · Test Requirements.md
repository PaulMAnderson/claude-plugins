---
title: Astrolabe · Docs · Implementation Plans · 2026 09 16 Hypercube Status Dashboard · Test Requirements
version: 2
id: c263cee8fed42bf4743b384610a51b06
createdAt: 2026-09-17T11:58:29.081Z
updatedAt: 2026-09-17T11:58:29.081Z
---
> Imported from `.astrolabe/docs/implementation-plans/2026-09-16-hypercube-status-dashboard/test-requirements.md` on 2026-09-17. The original file remains in place.

---

# B1 acceptance coverage

| AC | Phase/task | Automated assertion |
| --- | --- | --- |
| AC1.1 | 1/1 | Registered-only collection in `tests/test_hypercube_status.py` |
| AC1.2 | 1/1 | Duplicate and malformed watch-list errors in `tests/test_hypercube_status.py` |
| AC2.1 | 1/1 | All parsed fields in `tests/test_hypercube_status.py` |
| AC2.2 | 1/1 | Invalid/missing entry and healthy neighbor in `tests/test_hypercube_status.py` |
| AC2.3 | 1/1, 2/1 | Updated status on consecutive HTTP requests in `tests/test_hypercube_web.py` |
| AC3.1 | 2/1 | GET / status and error rows in `tests/test_hypercube_web.py` |
| AC3.2 | 2/1 | Escaped project data in `tests/test_hypercube_web.py` |
| AC3.3 | 2/1 | 404 route and configured ephemeral binding in `tests/test_hypercube_web.py` |
