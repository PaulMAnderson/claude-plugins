# MySQL conventions

Preserve the existing schema and migrations. Verify deployed MySQL/driver versions before relying on version-specific features.

House transaction ownership rule: a method that **starts** a transaction uses `TX_`, accepts no caller-owned connection/cursor/executor, and manages commit/rollback internally. A participant uses no `TX_` and receives the transaction's cursor/connection explicitly. A single atomic statement is not automatically a transaction owner. Test multi-step rollback and prevent accidental nested ownership.

Use parameterized values; quote validated identifiers appropriately. Default queries to genuinely read-only connections/permissions where the architecture supports them; mutations use the deliberate write connection. Handle failure and cleanup at the owning boundary.

Use snake_case objects, descriptive `idx_<table>_<columns>` / `fk_<table>_<referenced>` names, and created/updated timestamps under the project convention. Soft deletion is conditional on domain requirements. Choose BIGINT auto-increment for appropriate internal tables or ULIDs when distributed creation/non-sequential public IDs are required. IDs never substitute for authorization.

Use DECIMAL with justified precision/scale for money or values requiring exact decimal semantics. Scientific floating-point measurements may correctly use FLOAT/DOUBLE; do not convert them indiscriminately. Use JSON for genuinely variable structures and validate their schema; keep stable queryable fields relational.

Index actual foreign-key/join/filter/order workloads and inspect query plans; do not add every possible index. Reason explicitly about isolation, locking, lost updates, and deadlocks for concurrent mutations. Use stricter isolation or `SELECT ... FOR UPDATE` where the invariant requires it; verify behavior with the actual engine and transaction tests.
