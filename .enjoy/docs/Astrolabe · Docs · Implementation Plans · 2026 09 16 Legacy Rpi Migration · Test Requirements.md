---
title: Astrolabe · Docs · Implementation Plans · 2026 09 16 Legacy Rpi Migration · Test Requirements
version: 2
id: 9ff778b7ffd593f7e134cbbac86b04c2
createdAt: 2026-09-17T11:58:29.242Z
updatedAt: 2026-09-17T11:58:29.242Z
---
> Imported from `.astrolabe/docs/implementation-plans/2026-09-16-legacy-rpi-migration/test-requirements.md` on 2026-09-17. The original file remains in place.

---

# B2 acceptance coverage
| AC | Phase/task | Assertion |
| --- | --- | --- |
| AC1.1 | 1/1 | Parsed schema and core file contents after migration |
| AC1.2 | 1/1 | Raw SESSION bytes and escaped HISTORY text |
| AC1.3 | 1/1 | Guidance, plan, unknown-file bytes retained |
| AC2.1 | 1/1, 2/1 | Dry-run output and no filesystem changes |
| AC2.2 | 1/1, 2/1 | Missing/conflicting/symlink errors with unchanged trees |
| AC2.3 | 1/1 | Injected copy failure leaves no target or staging |
| AC2.4 | 1/1, 2/1 | Repeated run reports no-op and unchanged content |
