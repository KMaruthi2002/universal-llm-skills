# SQL Dialect Differences

SQL standards exist, but every engine diverges. The table below lists frequent differences among commonly used engines. Versions matter — features have been added over time — so verify against the documentation for the exact version the project runs. Engines listed are examples; analytical warehouses each have their own dialects, usually closest to one of these.

Abbreviations: **PG** PostgreSQL, **MY** MySQL / MariaDB, **LT** SQLite, **MS** SQL Server, **OR** Oracle.

## Limiting and pagination

| Need | PG | MY | LT | MS | OR |
|---|---|---|---|---|---|
| First N rows | `LIMIT n` | `LIMIT n` | `LIMIT n` | `TOP (n)` or `OFFSET 0 ROWS FETCH NEXT n ROWS ONLY` | `FETCH FIRST n ROWS ONLY` (newer); `ROWNUM` (legacy) |
| Skip and take | `LIMIT n OFFSET m` | `LIMIT m, n` or `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` (requires `ORDER BY`) | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |

## Upsert

| Engine | Form |
|---|---|
| PG, LT | `INSERT ... ON CONFLICT (cols) DO UPDATE SET col = EXCLUDED.col` / `DO NOTHING` |
| MY | `INSERT ... ON DUPLICATE KEY UPDATE col = VALUES(col)` (newer versions prefer a row alias) ; `INSERT IGNORE` skips errors broadly — use with care |
| MS, OR | `MERGE INTO target USING source ON (...) WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...` — read the engine's concurrency notes; `MERGE` may need locking hints or retries to be safe under concurrent upserts |
| PG (newer) | Also supports `MERGE` |

## Returning modified rows

- PG, LT (newer): `INSERT/UPDATE/DELETE ... RETURNING cols`.
- MS: `OUTPUT inserted.col, deleted.col`.
- OR: `RETURNING ... INTO` in PL/SQL.
- MY: no general `RETURNING` (MariaDB has it for some statements); use `LAST_INSERT_ID()` for auto-increment keys.

## Booleans

- PG: real `BOOLEAN` with `TRUE/FALSE`.
- MY: `BOOLEAN` is an alias for a tiny integer; `TRUE` = 1.
- LT: no separate boolean type; integers 0/1.
- MS: `BIT` (0/1); no boolean expressions in `SELECT` lists without `CASE`.
- OR: `BOOLEAN` only in newer versions for SQL; historically `NUMBER(1)` or `CHAR(1)`.

## Strings

| Need | PG | MY | LT | MS | OR |
|---|---|---|---|---|---|
| Concatenate | `\|\|` or `concat()` | `CONCAT()` (`\|\|` is OR unless configured) | `\|\|` | `+` or `CONCAT()` | `\|\|` or `CONCAT()` (two args) |
| Case-insensitive match | `ILIKE`, or `lower()` | Depends on collation (often case-insensitive by default) | `LIKE` is case-insensitive for ASCII by default | Depends on collation (often case-insensitive) | Case-sensitive by default |
| Empty string | Distinct from NULL | Distinct | Distinct | Distinct | **Empty string is treated as NULL** |
| Identifier quoting | `"name"` (unquoted folded to lowercase) | `` `name` `` (or `"` in ANSI mode) | `"name"` | `[name]` or `"name"` | `"name"` (unquoted folded to uppercase) |

Case sensitivity of comparisons and uniqueness depends on collation in MY and MS — two "unique" emails differing only in case may collide there and not in PG.

## Dates and times

- Current instant: PG `now()` / `CURRENT_TIMESTAMP`; MY `NOW()`; LT `CURRENT_TIMESTAMP` (text) or `datetime('now')`; MS `SYSUTCDATETIME()` / `GETDATE()`; OR `SYSTIMESTAMP`.
- Interval arithmetic: PG `ts + INTERVAL '1 day'`; MY `DATE_ADD(ts, INTERVAL 1 DAY)`; LT `datetime(ts, '+1 day')`; MS `DATEADD(day, 1, ts)`; OR `ts + INTERVAL '1' DAY` or `ts + 1`.
- Truncation: PG `date_trunc('day', ts)`; MY `DATE(ts)` or formatting functions; MS `DATETRUNC` (newer) or `CAST(ts AS date)`; OR `TRUNC(ts)`.
- Time zone types differ: PG `timestamptz` stores an instant and displays in session zone; MY `TIMESTAMP` converts to UTC for storage while `DATETIME` does not; MS `datetimeoffset` stores the offset; LT has no date type (stores text, real, or integer). Decide on UTC storage and be explicit.

## NULL ordering

- PG, OR: NULLs sort **last** ascending by default (first descending); support `NULLS FIRST/LAST`.
- MY, LT, MS: NULLs sort **first** ascending. MY and MS lack `NULLS FIRST/LAST` (emulate with `ORDER BY col IS NULL, col` or `CASE`); LT supports it in newer versions.

## Other features to check before using

| Feature | Notes |
|---|---|
| Window functions | Supported in all modern versions; older MY (< 8.0) and older LT lack them |
| `FILTER (WHERE ...)` on aggregates | PG, LT; others use `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` |
| `QUALIFY` | Some warehouses; not PG/MY/MS — use a subquery |
| Recursive CTEs | `WITH RECURSIVE` in PG/MY/LT; `WITH` (no keyword) in MS/OR |
| `LATERAL` joins | PG, MY (8.0.14+); MS/OR use `CROSS APPLY` / `OUTER APPLY` |
| Partial indexes | PG, LT; MS has filtered indexes; MY lacks them (use generated columns or functional indexes) |
| Check constraints | Enforced in PG, MS, OR, LT; MY enforces only in newer versions (8.0.16+) |
| Transactional DDL | PG and LT can roll back schema changes; MY and OR commit DDL implicitly |
| `SELECT ... FOR UPDATE SKIP LOCKED` | PG, MY (8.0+), OR; MS uses `WITH (READPAST, UPDLOCK)` hints |
| Default isolation level | Commonly read committed (PG, MS, OR); MY InnoDB defaults to repeatable read; LT serialises writers |
| Parameter placeholders (driver level) | `$1` (PG native), `?` (MY, LT, JDBC/ODBC), `@name` (MS), `:name` (OR and many drivers) — follow the driver, not the engine |

## Porting checklist

1. Limits, upserts, and returning clauses.
2. String concatenation, case sensitivity, and empty-string handling.
3. Date arithmetic and time zone semantics.
4. Boolean representation.
5. NULL ordering in any `ORDER BY` that pagination depends on.
6. Identifier case folding and quoting.
7. Feature availability for the target version.
8. Run the ported queries' results against the source system's results on the same data.
