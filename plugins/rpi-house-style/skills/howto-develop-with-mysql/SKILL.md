---
name: howto-develop-with-mysql
description: Write MySQL code with transaction safety and naming conventions
user-invocable: false
---

# MySQL Development Patterns

## Overview

Enforce transaction safety, naming conventions, and robust schema design to prevent data corruption and runtime errors.

**Core principles:**
- Transactions prevent partial updates (data corruption)
- Naming conventions ensure consistency
- Read-write separation prevents accidental mutations
- Backticks for identifiers to avoid reserved word conflicts

## Transaction Management

### TX_ Prefix Rule (STRICT ENFORCEMENT)

**Methods that START transactions:**
- Prefix method name with `TX_`
- Must NOT accept a connection/executor/cursor parameter
- Create and manage the transaction internally (e.g., `START TRANSACTION`, `COMMIT`, `ROLLBACK`)

**Methods that PARTICIPATE in transactions:**
- No `TX_` prefix
- MUST accept a connection/cursor parameter
- Execute queries using the provided cursor

```python
# GOOD: Starts transaction, has TX_ prefix, no cursor parameter
def TX_create_user_with_profile(self, user_data, profile_data):
    with self.db_connection.cursor() as cursor:
        try:
            self.db_connection.start_transaction()
            user_id = self.create_user(user_data, cursor)
            self.create_profile(user_id, profile_data, cursor)
            self.db_connection.commit()
            return user_id
        except Exception:
            self.db_connection.rollback()
            raise

# GOOD: Participates in transaction, no TX_ prefix, takes cursor
def create_user(self, user_data, cursor):
    sql = "INSERT INTO `users` (`username`, `email`) VALUES (%s, %s)"
    cursor.execute(sql, (user_data['username'], user_data['email']))
    return cursor.lastrowid

# BAD: Starts transaction but missing TX_ prefix
def create_user_with_profile(self, user_data, profile_data):
    # starts transaction without TX_ prefix
    ...

# BAD: Has TX_ prefix but takes cursor parameter (allows nesting)
def TX_create_user(self, user_data, cursor):
    # transaction logic here
    ...
```

**What DOES NOT count as "starting a transaction":**
- Single INSERT/UPDATE/DELETE operations
- Atomic operations like `INSERT ... ON DUPLICATE KEY UPDATE`
- SELECT queries

## Schema Design

### Primary Keys

**Default: AUTO_INCREMENT BIGINT or ULID stored as VARCHAR(26)**
- For internal-only tables or small lookup tables, `AUTO_INCREMENT` is acceptable.
- For user-visible IDs or high-distributed systems, use ULID to prevent ID enumeration attacks.

**Rule:** If unsure whether data will be user-visible, use ULID.

### Financial and Scientific Data

**Use exact decimal types (DECIMAL) for monetary or high-precision values:**
- Never use FLOAT/DOUBLE for money (causes rounding errors).
- Use `DECIMAL` with appropriate precision and scale.
- Example: `DECIMAL(19, 4)` for general financial data.

**Why:** Floating-point types accumulate rounding errors. `DECIMAL` ensures exact arithmetic.

### JSON Columns

**Use JSON columns for semi-structured data:**
- Supported in MySQL 5.7.8+.
- Prefer standard columns if the schema is stable.
- Validate JSON structure at the application level.

**Why:** Prevents runtime errors from accessing missing keys or wrong types.

### Read-Write Separation

**Maintain separate connections:**
- Read-write connection: Full mutation capabilities.
- Read-only connection: Enforces read-only at the user/permission level.
- Default to read-only for query methods.
- Use read-write only when mutations are needed.

**Why:** Prevents accidental writes to replicas, enforces deliberate mutation choices.

## Naming Conventions

### Database Identifiers

**All database objects use snake_case and backticks:**
- Tables: `user_preferences`, `order_items` -> \`user_preferences\`
- Columns: `created_at`, `user_id`, `is_active` -> \`created_at\`
- Indexes: `idx_tablename_columns` (e.g., `idx_users_email`)
- Foreign keys: `fk_tablename_reftable` (e.g., `fk_orders_users`)

**Why:** Backticks allow the use of reserved words as identifiers and prevent syntax errors.

### Schema Patterns

**Standard mixins:**
- `created_at`, `updated_at` timestamps on all tables.
- `deleted_at` for soft deletion when needed.

**Proactive indexing:**
- All foreign key columns.
- Columns used in WHERE clauses.
- Columns used in JOIN conditions.
- Columns used in ORDER BY.

## Concurrency

**Default isolation (REPEATABLE READ) for MySQL (InnoDB).**

**Use stricter isolation or locking when:**
- Financial operations: Serializable isolation.
- Critical sections: Pessimistic locking (`SELECT ... FOR UPDATE`).

## Common Mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| "This is one operation, doesn't need transaction" | Multi-step operations without transactions cause partial updates and data corruption | Wrap in transaction with TX_ prefix |
| "Single atomic operation needs TX_ prefix" | TX_ is for explicit transaction blocks, not atomic operations | No TX_ for single INSERT/UPDATE/DELETE |
| "FLOAT is fine for money, close enough" | Rounding errors accumulate, causing financial discrepancies | Use DECIMAL types for exact arithmetic |
| "I'll add indexes when we see performance issues" | Missing indexes on foreign keys cause slow queries from day one | Add indexes proactively for FKs and common filters |
| "Not using backticks for identifiers" | Can lead to syntax errors if a reserved word (like `order`) is used as a table/column name | Always use backticks: \`order\` |

## Red Flags - STOP and Refactor

**Transaction management:**
- Method calls `START TRANSACTION` but no `TX_` prefix.
- Method has `TX_` prefix but accepts cursor parameter.
- Multi-step operation without transaction wrapper.

**Schema:**
- Missing indexes on foreign keys.
- No `created_at`/`updated_at` timestamps.
- camelCase or PascalCase in database identifiers.
- Floating-point types for monetary values.

**All of these mean: Stop and fix immediately.**
