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
