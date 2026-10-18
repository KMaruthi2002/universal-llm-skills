---
name: database-migrations
description: >-
  Change database schemas and data safely in live systems: migration tooling
  and versioning, expand/contract (parallel change) for zero-downtime deploys,
  adding/renaming/dropping columns and tables, indexes and constraints without
  long locks, backfills and data migrations in batches, reversibility and
  roll-forward, coordinating code and schema deploys, and testing migrations on
  production-sized data. Use when writing or reviewing a migration, renaming
  or removing a column, adding an index or NOT NULL constraint to a big table,
  backfilling data, planning a schema change with no downtime, or recovering
  from a failed migration.
metadata:
  category: development
  related: database-design, sql-and-queries, legacy-modernization, release-management, ci-cd-pipelines, backend-development, incident-response, etl-pipelines
---

# Database Migrations

A migration changes the shape or content of data that a running application depends on. Unlike code, data cannot simply be redeployed from source: a bad migration can lock a table for an hour, break every running instance, or destroy information permanently. The craft is sequencing changes so the database and every version of the code that might be running are always compatible, and so that each step can be stopped, verified, and recovered.

## Scope

Covers schema migrations (DDL) and data migrations (DML transformations, backfills) on relational databases primarily, with notes for document stores. Includes tooling, sequencing with deploys, locking hazards, and verification.

Related:

- Designing the schema itself (normalization, keys, types) — `database-design`.
- Writing and tuning queries — `sql-and-queries`.
- Large-scale moves between systems — `legacy-modernization` and `etl-pipelines`.
- Deployment mechanics — `release-management`, `ci-cd-pipelines`.

## Core principles

### 1. Code and schema are deployed at different moments

During any deploy, old and new application versions run simultaneously (rolling deploys, multiple services, long-running workers, cached clients, a rollback). The schema must work with both. Why: the most common migration outage is not a slow migration but a fast one that removed or renamed something the still-running old code needed.

### 2. Expand, migrate, contract

Make every breaking change as a sequence of non-breaking ones: **expand** the schema (add the new thing alongside the old), **migrate** code and data to use the new thing, then **contract** (remove the old thing) only after nothing uses it. Why: each step is backward-compatible, deployable on its own, and recoverable; the breaking moment disappears.

### 3. Know what each statement locks, and for how long

Many DDL operations take locks that block reads or writes; some rewrite the whole table. On a small table that is milliseconds; on a large, busy table it is an outage. And even a "fast" DDL statement can cause an outage by waiting in the lock queue behind a long-running query while blocking everything behind it. Why: lock behaviour depends on the database engine, version, and statement — check it, do not assume.

### 4. Separate schema changes from data changes

Run backfills and data transformations as their own steps, in batches, outside the schema migration transaction where the volume is large. Why: a single huge `UPDATE` holds locks, bloats logs and replication, and cannot be paused or resumed; a schema migration that also rewrites millions of rows becomes impossible to reason about.

### 5. Prefer roll-forward, but be able to recover

"Down" migrations are useful in development but often unsafe or impossible in production (you cannot un-drop a column's data). Plan to fix forward, keep each step small enough that forward fixes are easy, and have a real recovery path for destructive steps: a backup, a retained copy, or a delayed contract step. Why: under incident pressure, a well-understood forward fix is safer than an untested rollback.

### 6. Rehearse on realistic data

Test migrations against a copy of production-scale data (sanitized as required) to measure duration, locking, and correctness. Why: a migration that takes 40 ms on a developer database can take 40 minutes on production, and production data contains values (nulls, duplicates, encoding problems) the schema claims are impossible.

## Discovering context

Before writing a migration:

- Identify the migration tool and its conventions (e.g. Rails Active Record migrations, Django migrations, Alembic, Flyway, Liquibase, Prisma Migrate, Knex, Ecto, golang-migrate, Atlas, sqitch, EF Core migrations). Read several existing migrations and match naming, structure, and whether they are reversible, transactional, or SQL vs. DSL.
- Know the database engine **and version** (behaviour differs a lot: e.g. PostgreSQL 11+ adds a column with a constant default without a rewrite; MySQL's online DDL support depends on version and operation; SQLite cannot alter most column properties in place).
- Find out table sizes and traffic for tables you touch (row counts, size on disk, write rate, longest-running queries). A rule of thumb: anything above a few million rows or with sustained writes needs the careful techniques below.
- Learn how migrations run in deploys: automatically before the new code starts, as a separate pipeline step, manually by a DBA, or via an online schema change tool. Learn whether deploys are rolling and how long old versions remain.
- Check for replicas, logical replication, change-data-capture consumers, ORMs with cached schema, and other services or reporting tools that read the same tables — all are consumers of the schema.
- Check team policy: required reviews for migrations, maintenance windows, lock-timeout settings, and whether destructive changes need sign-off.

## Process

### 1. Classify the change

| Change | Risk | Typical approach |
|---|---|---|
| Add a nullable column, new table, new index on a small table | Low | Single migration |
| Add a column with a default | Low–medium (engine/version dependent) | Single migration if the engine does not rewrite; otherwise add nullable, backfill, set default |
| Add an index on a large table | Medium | Online/concurrent index build |
| Add a NOT NULL, foreign key, or check constraint on existing data | Medium–high | Add as not-yet-validated, backfill/fix data, then validate |
| Rename a column or table | High (breaks running code) | Expand/contract |
| Change a column's type | High (rewrite + code breakage) | New column + backfill + switch + drop |
| Drop a column or table | High (irreversible, breaks old code) | Stop using in code first; drop later after a waiting period |
| Large data transformation | High | Batched backfill job, separately from DDL |
| Split/merge tables, change ownership of data | Very high | Multi-phase plan with dual writes or sync and reconciliation |

### 2. Plan the phases

For anything above low risk, write down the sequence of deploys before writing code. Each phase must be safe to stop at indefinitely.

### 3. Write the migration

- One logical change per migration file. Small migrations are easier to review, time, and recover.
- Set a **lock timeout** (and often a statement timeout) for DDL on busy tables, e.g. PostgreSQL `SET lock_timeout = '5s'`, MySQL `lock_wait_timeout`. If the lock cannot be acquired quickly, the migration fails cleanly instead of queueing and blocking all traffic. Retry later or with backoff.
- Know whether the tool wraps each migration in a transaction. Some operations cannot run in a transaction (e.g. PostgreSQL `CREATE INDEX CONCURRENTLY`); tools provide a way to disable the transaction for that migration.
- Never edit a migration that has already run in any shared environment. Write a new one. Tools track applied migrations by ID/checksum; editing history causes drift between environments.
- Keep migrations independent of application model code where possible (e.g. do not import the current ORM model class in a data migration; the model will change later and break replays of old migrations). Use raw SQL or the tool's historical model mechanism.

### 4. Review

Have migrations reviewed with these questions: what does it lock and for how long on our largest table; is it compatible with the currently deployed code; can it be stopped and resumed; what is the recovery if it fails halfway; is any data destroyed?

### 5. Rehearse and time

Run against a production-like dataset. Measure duration and observe locks (e.g. PostgreSQL `pg_locks`/`pg_stat_activity`, MySQL `performance_schema`/`SHOW PROCESSLIST`). Check replica lag during the run.

### 6. Execute with observation

Run at a low-traffic time if risk is meaningful. Watch error rates, latency, lock waits, replication lag, and disk. Have the recovery step ready. Do not run unreviewed manual DDL against production; if a manual step is truly needed, script it, review it, and record it.

### 7. Verify and clean up

Confirm the schema matches expectations, the data is correct (counts, spot checks, constraint validation), and the application is healthy. Schedule the contract phase.

## Expand/contract patterns

### Renaming a column (e.g. `name` → `full_name`)

1. **Expand**: add `full_name` (nullable).
2. **Dual write**: deploy code that writes both columns and still reads `name`.
3. **Backfill**: copy `name` into `full_name` for existing rows, in batches.
4. **Switch reads**: deploy code that reads `full_name` (still writes both, so rollback of this deploy is safe).
5. **Stop writing old**: deploy code that only uses `full_name`.
6. **Contract**: after a waiting period confirms nothing reads `name` (other services, reports, replicas), drop it.

Alternatives: some teams use a database view or a generated column to present the old name during transition. Some engines support renaming instantly, but that still breaks running code that uses the old name — the rename itself is not the problem, compatibility is.

### Changing a column type

Same shape as a rename: add a new column of the new type, dual write (converting), backfill with conversion, verify conversion of every row (count rows where conversion fails or differs), switch reads, stop old writes, drop the old column. In-place type changes typically rewrite the table under an exclusive lock unless the engine specifically supports the conversion as metadata-only (e.g. widening some varchar lengths).

### Adding a NOT NULL column

1. Add the column nullable (or with a default, if the engine adds it without a rewrite).
2. Deploy code that always writes it.
3. Backfill existing rows in batches.
4. Add the NOT NULL constraint in a way that avoids a long scan under an exclusive lock: e.g. in PostgreSQL add a `CHECK (col IS NOT NULL) NOT VALID` constraint, `VALIDATE CONSTRAINT` (takes a weaker lock), then set NOT NULL (recent versions use the validated check to skip the scan) and drop the check.

### Adding a foreign key or check constraint

Add the constraint without validating existing rows (e.g. PostgreSQL `NOT VALID`), which enforces it for new writes immediately; clean up violating existing rows; then validate. Validation scans the table but holds a lighter lock. Index the referencing column — unindexed foreign keys make deletes on the parent slow and lock-heavy.

### Adding an index on a large table

Use the online form: PostgreSQL `CREATE INDEX CONCURRENTLY` (not in a transaction; if it fails it leaves an invalid index to drop and retry), MySQL InnoDB online DDL (`ALGORITHM=INPLACE, LOCK=NONE` where supported), or an online schema change tool (e.g. gh-ost, pt-online-schema-change) for operations the engine cannot do online. Unique indexes will fail if duplicates exist — find and resolve duplicates first.

### Dropping a column or table

1. Remove all code references (including ORM model fields — some ORMs select all columns by name and break when one disappears; mark it ignored first if your ORM supports it).
2. Deploy and wait long enough for every old version, worker, and cache to be gone, and for other consumers to be confirmed absent.
3. Optionally rename the table/column to a "deprecated" name for a period, as a tripwire that fails loudly if something still uses it.
4. Take or confirm a backup that includes the data.
5. Drop.

### Splitting a table or moving data ownership

Treat as a migration project: new table(s) created, dual writes or change-data-capture sync, backfill, reconciliation job comparing old and new and reporting differences, read switch behind a flag, write switch, sync removal, old structure dropped. Keep the dual-write window short and monitored. See `legacy-modernization`.

## Locking hazards

General patterns (verify for your engine and version):

- **Exclusive locks on DDL**: many `ALTER TABLE` forms take an exclusive lock briefly or for the duration. Brief is fine; for the duration of a table rewrite is not.
- **Lock queueing**: a DDL statement waiting for a lock (because a long transaction or report holds a conflicting one) blocks every subsequent query on that table. A one-second operation can cause a ten-minute outage this way. Lock timeouts plus retry are the defence; also check for long-running transactions before starting.
- **Table rewrites**: type changes, some default additions on older versions, adding columns in certain positions, changing a table's storage options. Rewrites take time proportional to table size, double disk usage temporarily, and generate heavy replication traffic.
- **Long transactions**: a migration that runs a big `UPDATE` in one transaction holds row locks throughout, blocks vacuum/purge, and can bloat the database.
- **Replication lag**: heavy writes from backfills or rewrites delay replicas; reads from replicas become stale, and failover targets fall behind.
- **Foreign key checks**: adding a foreign key validates every row and may lock both tables.
- **Triggers and cascades**: existing triggers fire on backfill updates; cascading deletes can touch far more rows than expected.

## Backfills and data migrations

- **Batch it**: process rows in chunks (commonly 1,000–10,000 rows, tuned by measuring), iterating by primary key ranges (`WHERE id > last_id ORDER BY id LIMIT n`) rather than `OFFSET`, which gets slower as it goes.
- **Throttle**: pause between batches; watch replica lag and database load, and back off when they rise.
- **Make it idempotent and resumable**: each batch can be re-run safely (`WHERE new_col IS NULL` or upserts), and progress is recorded so the job can restart after interruption.
- **Run it as a job, not inside the migration** for large tables: a script, task, or background worker that can be monitored, paused, and resumed. Small backfills (thousands of rows) can live in a migration.
- **Handle concurrent writes**: rows written by the application during the backfill must also end up correct — which is why dual writes are deployed before the backfill begins.
- **Validate**: after the backfill, count rows that do not meet the target condition (should be zero), spot-check transformed values, and compare aggregates between old and new representations.
- **Mind side effects**: updates fire triggers, update `updated_at` timestamps, emit change events to downstream consumers, and invalidate caches. Decide whether that is desired; sometimes CDC consumers must be warned or filtered.
- **Dirty data**: expect values the schema "forbids". Decide in advance what to do with rows that cannot be converted: log them, put them in a quarantine table, or apply a documented default. Never silently drop them.

## Reversibility and recovery

| Step type | Reversible? | Recovery approach |
|---|---|---|
| Add table, column, index | Yes | Drop it (forward migration) |
| Add constraint | Yes | Drop the constraint |
| Backfill into a new column | Yes, if the old column is intact | Re-run or clear the new column |
| In-place data transformation | Only with a copy | Keep the original values (a backup table or column) until verified |
| Drop column/table | No | Restore from backup — slow and may lose data written since |
| Type change in place | Partially | Data may be truncated or rounded irreversibly |

Practices:

- Write down-migrations if the tool and team use them, but test them; an untested down-migration is a guess. For destructive steps, a down-migration that pretends to restore data is worse than one that raises an error explaining why it cannot.
- Before destructive steps in production, confirm a recent, restorable backup exists (and that someone has actually restored from that backup system recently), or copy the affected data to a retained table or export.
- Prefer delaying destruction: drop old columns a release or two after the code stopped using them.
- If a migration fails halfway in a non-transactional engine (e.g. MySQL DDL is not transactional; multi-statement migrations can partially apply), know how to detect the partial state and finish or undo it. Keep non-transactional migrations to one statement where possible.

## Coordinating with deploys

A typical safe sequence for a multi-phase change:

| Deploy | Schema | Code |
|---|---|---|
| 1 | Expand (additive only) | Old code unaffected |
| 2 | — | New code writes both / tolerates both |
| — | Backfill job runs | — |
| 3 | — | Code reads new |
| 4 | — | Code stops writing old |
| 5 | Contract (destructive) | — |

Rules:

- Migrations that run automatically before code deploys must be **backward-compatible with the currently running code**. Migrations that run after must be compatible with the new code. Additive changes are compatible with both, which is why expand/contract works with either ordering.
- Never bundle the expand and contract of the same change in one deploy.
- Feature flags help: the code path that uses the new schema can be switched on and off independently of deploys.
- With multiple services sharing a database, every service must reach the "tolerates both" state before any contract step. Shared databases make this coordination expensive — one reason to avoid them.
- Mobile or desktop clients and offline-capable apps may run old versions for months; schema changes visible through APIs need API versioning, not just database sequencing.

## Testing migrations

- **Run the full migration chain from an empty database in CI**, and check that the resulting schema matches the expected schema (many tools can diff or dump the schema). This catches migrations that only work on a developer's existing database.
- **Test up and down** (if down migrations are used) in CI.
- **Test against production-like data volume** for risky migrations: a sanitized snapshot or a generated dataset with realistic size and distributions. Measure time and locks.
- **Test data migrations with fixtures that include the weird cases**: nulls, empty strings, duplicates, max-length values, invalid encodings, orphaned references.
- **Test application compatibility**: run the old version's test suite against the new schema (for expand steps) to confirm backward compatibility.
- **Lint migrations**: tools exist that flag dangerous operations (e.g. strong_migrations, squawk, Atlas lint, django-migration-linter). Use them if the project does or would benefit.

Never use real production personal data in test environments without the sanitization and approvals the organization requires.

## Engine notes

Behaviour changes between versions; confirm in the documentation for the exact version in use. Indicative examples:

| Engine | Things to know |
|---|---|
| PostgreSQL | Transactional DDL (most migrations can be atomic). Adding a column with a constant default is metadata-only from v11. `CREATE INDEX CONCURRENTLY` and `REINDEX CONCURRENTLY` avoid write locks but cannot run in a transaction. `NOT VALID` + `VALIDATE CONSTRAINT` for constraints. Most `ALTER TABLE` forms take an `ACCESS EXCLUSIVE` lock, at least briefly — lock queueing is the main hazard. |
| MySQL / MariaDB | DDL is not transactional; a failed multi-statement migration leaves partial state. InnoDB online DDL (`ALGORITHM=INSTANT/INPLACE`, `LOCK=NONE`) covers many operations depending on version; others copy the table. Online schema change tools (gh-ost, pt-online-schema-change) handle the rest via shadow tables. Metadata locks can queue like PostgreSQL's. |
| SQLite | Limited `ALTER TABLE`; many changes require create-new-table, copy, drop, rename, ideally with foreign keys temporarily disabled and re-checked. Single-writer: long migrations block all writes. |
| SQL Server | Many operations online in Enterprise editions (`ONLINE = ON`); schema modification locks block readers. Adding NOT NULL with default is metadata-only in recent versions. |
| Distributed SQL (e.g. CockroachDB, Spanner, Vitess-backed MySQL) | Schema changes are often online and asynchronous by design, with their own rules, job tracking, and limitations on mixing DDL and DML in one transaction. Read the engine's schema-change documentation. |

## Worked example: enforcing a required column on a large table

Illustrative. A PostgreSQL `orders` table has 200 million rows and constant writes. Product wants `orders.currency` to be required; it has existed as nullable for a year, and about 3% of rows are null.

1. **Investigate**: query null counts by creation date. The nulls are all older than the date the checkout started sending currency, and all from one region — so the correct backfill value is known (that region's currency). Confirm with the data owner.
2. **Code first**: confirm every write path sets currency (search the code; add an application-level validation and deploy it). Otherwise new nulls arrive during the backfill.
3. **Backfill job**: batches of 5,000 by primary key range, `UPDATE ... SET currency = 'XYZ' WHERE id BETWEEN $1 AND $2 AND currency IS NULL`, sleeping between batches and pausing if replica lag exceeds a threshold. Rehearsal on a snapshot showed about 40 minutes total. Progress is logged so it can resume.
4. **Validate data**: `SELECT count(*) WHERE currency IS NULL` returns 0.
5. **Constraint without a long lock**: with `lock_timeout` set, add `CHECK (currency IS NOT NULL) NOT VALID` (brief lock), then `VALIDATE CONSTRAINT` (scans but allows reads and writes), then `ALTER COLUMN currency SET NOT NULL` (uses the validated check to skip the scan on supported versions), then drop the now-redundant check.
6. **Verify**: schema shows NOT NULL; application error rates unchanged; a test insert without currency is rejected.

Naively running `ALTER TABLE orders ALTER COLUMN currency SET NOT NULL` would have held an exclusive lock while scanning 200 million rows — and failed anyway because of the nulls.

## When a migration fails in production

1. **Stop making it worse.** If it is blocking traffic, cancel it (cancel the query/backend, or stop the job). Lock-waiting DDL can usually be cancelled safely.
2. **Determine the state**: which statements applied? Check the migration tool's tracking table and the actual schema; they can disagree after a partial failure on non-transactional engines.
3. **Decide between finishing and undoing**, choosing whichever is smaller and better understood. Prefer a reviewed forward migration over manual edits.
4. **Restore consistency** between the tracking table, the schema, and the code, so the next deploy does not re-run or skip steps unexpectedly.
5. **Communicate and follow up**: record what happened, and add a guard (lint rule, lock timeout, rehearsal requirement) so it does not recur. See `incident-response` and `postmortem`.

## Migrations in multi-environment and multi-developer workflows

- **Ordering conflicts**: two branches each add a migration; after merging, the tool may see two "latest" migrations or a broken chain. Follow the tool's mechanism (timestamped IDs, merge migrations, dependency declarations) and re-run the full chain in CI after merging.
- **Environment drift**: if a hotfix was applied by hand in production, capture it as a migration immediately so every environment converges. Periodically diff the production schema against the schema produced by the migration chain.
- **Squashing old migrations**: acceptable once every environment has applied them; replace the old chain with a baseline snapshot following the tool's documented procedure, never by deleting files that a lagging environment still needs.
- **Seed and reference data**: keep required reference rows (enumerations, default settings) in migrations or a dedicated idempotent seed step, not in manual scripts.

## Document stores and schemaless databases

"Schemaless" means the schema lives in the code. The same principles apply:

- Code must read both old and new document shapes during transition (version fields on documents help).
- Migrate lazily (on read/write) or eagerly with a batched backfill; lazy migration leaves old shapes around indefinitely unless a backfill finishes the job.
- Index builds on large collections have their own locking and resource costs; use the engine's background or rolling index build options.

## Pitfalls

- Renaming or dropping a column in the same deploy as the code change, breaking old instances during the rollout.
- Adding a NOT NULL column without a default to a populated table, or with a default on an engine version that rewrites the table.
- Creating an index without the online option on a large, busy table.
- No lock timeout, so a migration waits behind a long query and blocks the whole table.
- One giant `UPDATE` backfill in a transaction.
- Editing an already-applied migration instead of adding a new one.
- Data migrations that import current ORM models and break when replayed later.
- Unique index creation failing in production on duplicates nobody knew existed.
- Down-migrations assumed to work but never run.
- Dropping data without a verified backup or retained copy.
- Forgetting other consumers of the table: reports, ETL jobs, other services, replicas, CDC pipelines.
- Testing only on a tiny development database.
- Running ad hoc DDL against production by hand under pressure, leaving environments drifted from migration history.

## Quality bar and verification

Before declaring a migration done:

- Each step is backward-compatible with the code running at the moment it is applied; breaking changes are split into expand/contract phases with the plan written down.
- Lock behaviour for each statement on the target engine and version is known; lock timeouts are set for busy tables; large indexes and constraints use online/non-validating forms.
- Large data changes run as batched, throttled, idempotent, resumable jobs, with validation queries showing zero remaining unconverted rows.
- The migration chain runs from scratch in CI and produces the expected schema; risky migrations were rehearsed on production-like data with measured duration.
- Destructive steps have a verified backup or retained copy, occur only after code no longer uses the structure, and had explicit sign-off where policy requires.
- Post-run checks confirm schema, data correctness, application health, and replication health.

When reporting, list the phases (which are done and which are scheduled), measured durations from rehearsal, the recovery plan, and any data anomalies found and how they were handled. Do not run migrations against production, or any destructive step anywhere shared, without the user's explicit confirmation.
