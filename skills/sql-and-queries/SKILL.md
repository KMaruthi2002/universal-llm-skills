---
name: sql-and-queries
description: >-
  Write SQL that is correct first and fast second, in any dialect: joins and
  their row-multiplication traps, aggregation and GROUP BY, window functions,
  CTEs and subqueries, NULL and three-valued logic, set operations, upserts,
  pagination, transactions and locking in queries, reading query plans,
  indexing for specific queries, fixing N+1 access from application code, and
  safe parameterised queries. Use when writing or reviewing a query, a report,
  or ORM code that generates SQL; when a query returns wrong counts or
  duplicates; when a query is slow; when reading an EXPLAIN plan; or when
  porting SQL between engines. For schema and table design use
  database-design; for schema changes use database-migrations.
metadata:
  category: development
  related: database-design, database-migrations, performance-optimization, backend-development, data-analysis, secure-coding, debugging
---

# SQL and Queries

SQL is declarative: you describe the result, the engine decides how to compute it. That makes it powerful and also makes two kinds of mistake easy — **queries that run fine and return subtly wrong results**, and **queries that return the right result but take minutes on real data**. This skill is about avoiding both, in whatever engine the project uses.

## Scope

Covers writing, reviewing, debugging, and tuning queries: reads, writes, reporting queries, and the SQL that ORMs and query builders generate. Applies across relational engines (e.g. PostgreSQL, MySQL/MariaDB, SQLite, SQL Server, Oracle) and SQL-speaking analytical engines and warehouses, with dialect notes.

Neighbours:
- Tables, keys, constraints, and which indexes the schema should have — `database-design`.
- Changing schemas or backfilling data in production — `database-migrations`.
- Broad performance work beyond the database — `performance-optimization`.
- Using query results for analysis — `data-analysis`.

## Core principles

### 1. Correct before fast

A fast wrong answer is worse than a slow right one, because nobody notices it is wrong. Write the query for correctness, check the result against known cases, and only then optimise — and re-check the result after optimising.

### 2. Know the grain of every row set

The single most useful habit in SQL: at each step (each table, join, subquery, CTE), state what one row represents — "one row per order", "one row per order line", "one row per customer per day". Most wrong results come from a join that silently changed the grain (one row per order became one row per order *line*), after which sums and counts are inflated.

### 3. NULL is not a value; it is "unknown"

Comparisons with NULL yield UNKNOWN, not true or false, and `WHERE` keeps only rows that are true. This makes `NOT IN`, `<>`, outer joins, and aggregates behave in ways that surprise people. Every nullable column in a predicate deserves a moment's thought.

### 4. Let the engine do set-based work

Row-by-row processing in application code (loop, query, loop) is slow because each round trip has fixed latency and the engine cannot optimise across iterations. Express the whole operation as one or a few set-based statements where possible.

### 5. Measure with the plan, not with intuition

Whether an index is used, how a join is executed, and where time goes are visible in the query plan. Guessing wastes time and often makes things worse. Read the plan (with actual execution statistics when safe to run) before and after every optimisation.

### 6. Never build SQL by concatenating input

Parameterised queries (bound parameters, placeholders) keep data separate from code. String concatenation of any externally influenced value — even "trusted" internal IDs — is how SQL injection happens. Identifiers that must be dynamic (column names for sorting) are chosen from an allow-list, never interpolated from input.

## Discovering context

- **Engine and version**: features and syntax differ (window functions, `FILTER`, `RETURNING`, upsert syntax, JSON operators, `LIMIT` vs. `TOP` vs. `FETCH FIRST`, recursive CTE support, lateral joins). Check before using a feature. See `references/dialect-differences.md`.
- **How the project issues SQL**: ORM, query builder, raw SQL files, stored procedures. Follow it; if raw SQL is needed in an ORM project, see how the project already does that.
- **Style conventions**: keyword case, indentation, aliasing, CTE vs. subquery preference, file layout for SQL. Match them.
- **Schema facts**: which columns are nullable, which have unique constraints, which indexes exist, row counts. Correctness and performance both depend on these. Introspect the catalog, read migrations, or ask.
- **Data volume and distribution**: a query that is fine on 10,000 rows may be catastrophic on 100 million, and skewed data (one tenant with most rows) changes plans.
- **Where the query will run**: a production primary, a replica, a warehouse, a local dev database. This determines what is safe to run while investigating.

## Writing correct queries

### Joins

| Join | Keeps | Use for |
|---|---|---|
| `INNER JOIN` | Rows with a match on both sides | Required relationships |
| `LEFT JOIN` | All left rows; NULLs where no right match | Optional relationships; "including those with none" |
| `RIGHT JOIN` | Mirror of left | Rarely needed; rewrite as left join for readability |
| `FULL OUTER JOIN` | All rows from both sides | Reconciliation between two sets |
| `CROSS JOIN` | Every combination | Generating grids (dates × products); dangerous by accident |
| Semi-join (`EXISTS`, `IN`) | Left rows that have a match, *once* | Filtering by existence without multiplying rows |
| Anti-join (`NOT EXISTS`) | Left rows with no match | "Customers with no orders" |

Traps:
- **Fan-out**: joining orders to order lines and to payments in the same query produces lines × payments rows per order. Sums of order totals are then multiplied. Fix by aggregating each child to the parent's grain in a subquery or CTE *before* joining, or by using `EXISTS` when you only need to filter.
- **Filtering an outer-joined table in `WHERE`** turns the left join into an inner join, because rows with NULLs fail the condition. Put conditions on the optional table in the `ON` clause:
  ```sql
  -- Wrong: drops customers without a 2024 order
  SELECT c.id, o.id
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
  WHERE o.created_at >= '2024-01-01';

  -- Right
  SELECT c.id, o.id
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id AND o.created_at >= '2024-01-01';
  ```
- **Joining on non-unique keys** you assumed were unique. If you expect one match, verify the uniqueness constraint exists, or check counts.
- **Implicit joins** (comma-separated `FROM a, b` with conditions in `WHERE`) make it easy to forget a condition and produce a cross join. Prefer explicit `JOIN ... ON`.

### NULL semantics

- `x = NULL` is never true; use `IS NULL` / `IS NOT NULL`. Some dialects offer a null-safe equality (`IS NOT DISTINCT FROM`, `<=>`).
- `NOT IN (subquery)` returns no rows if the subquery yields any NULL, because `x <> NULL` is UNKNOWN. Use `NOT EXISTS` instead:
  ```sql
  SELECT c.id FROM customers c
  WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
  ```
- `col <> 'x'` excludes rows where `col` is NULL. If those should be included, say so: `col <> 'x' OR col IS NULL` (or a null-safe comparison).
- Aggregates ignore NULLs: `COUNT(col)` counts non-null values, `COUNT(*)` counts rows, `AVG(col)` averages non-null values only. `SUM` over no rows (or all NULLs) is NULL, not 0 — wrap in `COALESCE(SUM(x), 0)` when a zero is meant.
- NULLs in `GROUP BY` form one group; in `ORDER BY` they sort first or last depending on the engine (use `NULLS FIRST/LAST` where supported for determinism).
- Unique constraints usually allow multiple NULLs (engine-dependent).
- Arithmetic and string concatenation with NULL yields NULL in most engines.

### Aggregation

- Every non-aggregated column in the `SELECT` must be in the `GROUP BY` (some engines permit otherwise in lax modes and return an arbitrary value — do not rely on it).
- `WHERE` filters rows before grouping; `HAVING` filters groups after. Put row conditions in `WHERE` — it is clearer and lets the engine discard rows early.
- **Conditional aggregation** pivots without multiple queries:
  ```sql
  SELECT customer_id,
         COUNT(*) AS orders,
         COUNT(*) FILTER (WHERE status = 'refunded') AS refunded  -- or SUM(CASE WHEN ... THEN 1 ELSE 0 END)
  FROM orders GROUP BY customer_id;
  ```
- `COUNT(DISTINCT x)` is a common patch for fan-out duplicates; it often hides the real problem (wrong grain) and is expensive. Fix the grain instead.
- Averages of averages are wrong when group sizes differ; compute from sums and counts.
- Integer division truncates in many engines (`1/2 = 0`); cast to a decimal type when computing ratios.

### Window functions

Window functions compute across related rows *without collapsing them*, which replaces many self-joins and correlated subqueries.

- Ranking: `ROW_NUMBER()` (unique sequence), `RANK()` (gaps on ties), `DENSE_RANK()` (no gaps).
- Offsets: `LAG()`, `LEAD()` for previous/next row comparisons.
- Running and moving aggregates: `SUM(x) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ...)`.
- **Top-N per group**:
  ```sql
  WITH ranked AS (
    SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC, id DESC) AS rn
    FROM orders o
  )
  SELECT * FROM ranked WHERE rn <= 3;
  ```
- Always make the window's `ORDER BY` deterministic (add a unique tie-breaker), or results change between runs.
- Know the default frame: with `ORDER BY` in the window, many engines default to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which treats ties as peers (running totals jump on duplicate sort values). Specify `ROWS` explicitly when you mean physical rows.
- Window functions cannot appear in `WHERE`; filter in an outer query or CTE (or `QUALIFY` where supported).

### CTEs and subqueries

- CTEs (`WITH`) name intermediate steps and make the grain of each step explicit. Use them for readability.
- Engines differ on whether CTEs are inlined (optimised with the outer query) or materialised (computed once, possibly blocking predicate pushdown). Some engines let you choose. If a CTE-based query is slow, check the plan for this.
- Correlated subqueries (`SELECT ... (SELECT ... WHERE inner.x = outer.x)`) may execute per outer row; modern optimisers often rewrite them, but check the plan on large data. Lateral joins (`LATERAL`, `CROSS APPLY`) are an explicit alternative for "top-N per row" patterns.
- **Recursive CTEs** traverse hierarchies (`parent_id` trees, graphs). Always include a termination condition, and guard against cycles (track visited paths or depth) — an unbounded recursion on cyclic data runs until it hits a limit or exhausts resources.

### Set operations

`UNION` removes duplicates (with a sort or hash cost); `UNION ALL` keeps them and is cheaper — use `UNION ALL` unless you need deduplication. `INTERSECT` and `EXCEPT` (or `MINUS`) are useful for reconciliation. Column counts and types must align by position, not name.

### Ordering and pagination

- Without `ORDER BY`, row order is undefined, even if it looks stable today.
- `ORDER BY` must be deterministic for pagination: include a unique tie-breaker.
- **Offset pagination** (`LIMIT 50 OFFSET 100000`) reads and discards all skipped rows — slow at depth, and inconsistent when rows are inserted. **Keyset pagination** seeks directly:
  ```sql
  SELECT * FROM events
  WHERE (created_at, id) < (:last_created_at, :last_id)   -- row-value comparison; expand to OR form if unsupported
  ORDER BY created_at DESC, id DESC
  LIMIT 50;
  ```
  with an index on `(created_at, id)`.

### Writes

- **Always check the `WHERE` clause of `UPDATE` and `DELETE`** — run it as a `SELECT COUNT(*)` first and compare the number with your expectation. Many tools and engines will happily update every row.
- **Upserts**: use the engine's native form (`INSERT ... ON CONFLICT`, `ON DUPLICATE KEY UPDATE`, `MERGE`) rather than select-then-insert, which races. Native `MERGE` implementations have engine-specific concurrency caveats; read them.
- **Atomic updates** instead of read-modify-write: `UPDATE accounts SET balance = balance - :amt WHERE id = :id AND balance >= :amt` and check the affected row count.
- **`RETURNING` / `OUTPUT`** clauses (where supported) return modified rows, avoiding an extra round trip and a race.
- **Large writes in batches**: updating or deleting millions of rows in one statement can hold locks for a long time, bloat logs, and stall replication. Batch by key range with pauses, especially in production (see `database-migrations`).

### Transactions and locking in queries

- Group statements that must succeed together in a transaction; keep it short.
- Know the default isolation level of the engine. Under read committed, two concurrent read-modify-write transactions can lose an update. Use atomic statements, `SELECT ... FOR UPDATE` row locks, optimistic version columns, or serializable isolation with retries.
- `SELECT ... FOR UPDATE SKIP LOCKED` (where supported) is a well-known pattern for job queues in SQL: workers claim different rows without blocking each other.
- Access tables and rows in a consistent order across transactions to reduce deadlocks; when a deadlock is reported, retry the transaction.

## Making queries fast

### Read the plan

Most engines offer `EXPLAIN` (estimated plan) and a variant that executes the query and reports actual rows and timings (e.g. `EXPLAIN ANALYZE` or equivalent). Remember the executing variant **runs the query** — for writes, wrap it in a transaction you roll back, or use estimate-only mode, and never casually run it on a heavy query against a production primary.

What to look for:
- **Full scans of large tables** where you expected an index lookup.
- **Estimated vs. actual row counts** that differ by orders of magnitude — the optimiser is working from bad statistics or a predicate it cannot estimate; it will choose poor join strategies. Refresh statistics, or rewrite the predicate.
- **Nested loops over large inputs** (fine for small outer sides, disastrous for large ones).
- **Sorts and hashes spilling to disk** — consider an index that provides order, or more memory for the operation if appropriate.
- **The step where most time is spent** — optimise that, not the rest.

See `references/query-plans-and-indexing.md` for a deeper guide to plan operators and index-design reasoning.

### Make predicates index-friendly ("sargable")

An index on `created_at` cannot be used efficiently for `WHERE DATE(created_at) = '2024-05-01'` or `WHERE created_at + INTERVAL '1 day' > now()`, because the function is applied to the column. Rewrite as a range on the bare column:
```sql
WHERE created_at >= '2024-05-01' AND created_at < '2024-05-02'
```
Similarly:
- `WHERE lower(email) = :e` needs an expression index on `lower(email)` (or a case-insensitive column type).
- `LIKE 'abc%'` can use a suitable index; `LIKE '%abc'` cannot (consider trigram or full-text indexes).
- Implicit type conversions (comparing a text column to a number) can disable index use.
- `OR` across different columns may prevent a single index scan; consider `UNION ALL` of two indexed queries, or check whether the engine can combine indexes.

### Index for the query

Covered in more depth in `database-design`; for a specific slow query:
1. Equality-filtered columns first, then the range or sort column, in a composite index.
2. Add columns the query selects to make it covering, if the read is hot and the columns are few.
3. Use partial indexes for queries that always include a fixed condition (`WHERE status = 'open'`).
4. Re-check the plan; confirm the new index is used and the time dropped. Remove indexes that did not help.
5. Consider write cost: every index slows inserts and updates on that table.

### Fetch less

- Select only needed columns, not `SELECT *` — less I/O, possible covering-index use, and immunity to added columns breaking code.
- Aggregate in the database rather than shipping rows to the application to count them.
- Limit result sizes; paginate.
- Avoid unnecessary `DISTINCT` and `ORDER BY` — both can force sorts.

### The N+1 problem

Application code fetches a list (1 query), then queries per item (N queries):
```text
orders = query("SELECT * FROM orders WHERE customer_id = ?")
for o in orders:
    o.lines = query("SELECT * FROM order_lines WHERE order_id = ?", o.id)
```
With 200 orders that is 201 round trips; at 1 ms each it is 200 ms of pure latency before any work. Fixes:
- One query with a join (watch the grain), or
- Two queries: the list, then `WHERE order_id IN (...)` (or `= ANY(:ids)`) for all children at once, assembled in memory.
- In ORMs, use eager loading / prefetch / include options, and inspect the generated SQL. Many ORMs can log queries per request; a test asserting the query count for a hot endpoint prevents regressions.

### Other common accelerators

- **Batch** inserts (multi-row `VALUES` or bulk-load tools) instead of one insert per row.
- **Precompute** expensive aggregates into summary tables or materialised views when they are read often and can tolerate refresh delay.
- **Partition** very large tables (often by time) so queries and maintenance touch only relevant partitions — make sure queries include the partition key in their filters.
- **Connection reuse** via pooling; opening a connection per query is expensive.

## Safety

- **Parameterise every value.** For dynamic identifiers (sort column, direction), map input to an allow-list of known identifiers in code.
- **Least privilege**: application roles should not have DDL or superuser rights; reporting users should be read-only, ideally on a replica.
- **Before any `UPDATE`/`DELETE` on real data**: run the equivalent `SELECT` and check the count, run inside a transaction so you can roll back, and have a backup or a way to restore affected rows. Do not run destructive statements against production without the user's explicit approval.
- **Heavy queries in production**: run investigative queries on a replica where possible; set a statement timeout for ad hoc queries; avoid `EXPLAIN ANALYZE` of expensive queries on the primary during peak load.
- **Sensitive data**: select only the columns you need when investigating; do not paste personal data into tickets or chat.

## Decision guidance

### Join vs. subquery vs. EXISTS
Use `JOIN` when you need columns from both sides at a compatible grain. Use `EXISTS` / `NOT EXISTS` when you only need to filter by the presence or absence of related rows — it cannot multiply rows. Use a subquery or CTE that pre-aggregates when you need a child's aggregate at the parent's grain.

### One clever query vs. several simple ones
One query avoids round trips and lets the optimiser work across steps. Several queries can be clearer, cacheable separately, and avoid fan-out problems. For application paths, prefer few round trips; for reports, prefer readable CTE pipelines; split when a single query's plan becomes unstable or unreadable.

### ORM vs. raw SQL
Follow the project. Use the ORM for routine CRUD; drop to raw SQL (still parameterised) for complex reporting, window functions, bulk operations, or when the ORM generates poor SQL. Keep raw SQL in a place the project's conventions designate and cover it with integration tests against the real engine.

## Pitfalls

- **Fan-out inflation** of sums and counts after joining two one-to-many relationships.
- **`NOT IN` with NULLs** returning nothing.
- **Outer join silently turned inner** by a `WHERE` condition on the optional side.
- **Non-deterministic ordering** in pagination and window functions.
- **`SUM` returning NULL** where zero was meant.
- **Integer division** truncating ratios.
- **Functions on indexed columns** in predicates, disabling index use.
- **Time zone mistakes**: comparing local dates to UTC timestamps; "today" computed in the server's zone instead of the user's.
- **Deep `OFFSET` pagination** on large tables.
- **N+1 queries** hidden inside ORM lazy loading.
- **Unbatched mass updates** locking tables and stalling replicas.
- **Concatenated SQL** with external input.
- **Testing queries only on tiny datasets** where every plan is fast and every join looks correct.
- **Trusting `DISTINCT` to fix duplicates** without understanding why they appeared.

## Quality bar and verification

Before calling a query done:

- [ ] You can state the grain of the result and of each intermediate step.
- [ ] Results were checked against known cases: a hand-computed small example, a known total, or a comparison with an independent query (e.g. counts per parent before and after a join).
- [ ] Edge cases were tested: NULLs in filtered and joined columns, empty groups, parents with no children, ties in ordering, boundaries of date ranges.
- [ ] Ordering is deterministic wherever it matters.
- [ ] All external values are bound parameters; dynamic identifiers come from an allow-list.
- [ ] For queries on large tables, the plan was inspected on realistic data volumes (or the user was told what to check), indexes are used as intended, and estimated vs. actual rows are reasonable.
- [ ] Application code does not issue per-row queries in loops on hot paths.
- [ ] Writes have been dry-run as `SELECT`s with matching counts, run in a transaction where possible, and batched if large.
- [ ] The query follows the project's SQL style and runs on the project's engine and version.

State which checks were run against a real database and which were reasoned about only.

## Depth on demand

- `references/query-plans-and-indexing.md` — reading plan operators, join algorithms, statistics, and reasoning through index design for a specific query. Read when a query is slow and the plan is not obviously explained by a missing index.
- `references/dialect-differences.md` — syntax and behaviour differences across common engines (limits, upserts, string and date functions, booleans, identifiers, NULL ordering, case sensitivity). Read when writing for an unfamiliar engine or porting SQL.
