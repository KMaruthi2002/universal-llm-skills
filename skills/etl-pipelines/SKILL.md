---
name: etl-pipelines
description: >-
  Design, build and operate data pipelines that move and transform data
  between systems: ETL vs ELT, batch vs streaming, full vs incremental loads,
  change data capture, idempotent and re-runnable loads, schema evolution,
  orchestration (e.g. Airflow, Dagster, Prefect, dbt, cloud schedulers), data
  quality checks, backfills, late-arriving data, lineage and monitoring. Use
  when asked to build or fix a data pipeline, sync data into a warehouse or
  lake, schedule transformations, backfill historical data, handle schema
  changes from a source, or investigate missing, duplicated or stale data.
metadata:
  category: automation
  related: data-cleaning-and-validation, database-design, sql-and-queries, scheduled-jobs, api-integrations-and-webhooks, observability, database-migrations, data-analysis
---

# ETL Pipelines

A data pipeline is a promise: "the table downstream reflects the source, correctly, as of a known time." Pipelines rarely fail by crashing; they fail by quietly producing numbers that are slightly wrong — a day missing, a row doubled, a currency unconverted, a column that started arriving null. Good pipeline engineering is mostly about making reruns safe, making the state of the data explicit, and checking the data itself rather than only whether the job exited zero.

## Scope

Covers: extracting from databases, APIs, files and event streams; loading into warehouses, lakes, lakehouses, operational stores; transformations; orchestration; quality checks; backfills; operating pipelines.

Related:
- Validating and cleaning datasets in depth (rules, profiling, deduplication logic): `data-cleaning-and-validation`.
- Schema design of the target models: `database-design`; query writing: `sql-and-queries`.
- Pulling from third-party APIs (auth, pagination, rate limits): `api-integrations-and-webhooks`.
- Cron/scheduler mechanics: `scheduled-jobs`.
- Analysing the resulting data: `data-analysis`.

## Core principles

1. **Every load must be safe to rerun.** Jobs fail halfway, schedulers retry, people rerun last Tuesday by hand. If rerunning a load for the same window produces duplicates or gaps, every incident becomes a data-repair project. Design loads as "make the target for this partition equal to the source for this partition" (overwrite/merge), not "append whatever I read".

2. **Separate raw from modelled.** Land source data as close to raw as possible (with load metadata), then transform in later layers. Why: when a transformation bug is found, you can rebuild from raw without re-extracting from a source that may have changed, rate-limited, or deleted history.

3. **Make time explicit.** Distinguish event time (when it happened), ingestion time (when you received it), and processing window (which run handled it). Most pipeline bugs around duplicates, late data, timezones and backfills come from conflating them.

4. **Check the data, not just the job.** A green run that loaded zero rows, or loaded yesterday's file again, is a failure. Assert on row counts, freshness, uniqueness, nulls, referential integrity and business invariants.

5. **Contracts at the boundaries.** Sources change without telling you. Detect schema and semantic changes at ingestion and decide deliberately whether to adapt, quarantine or fail, rather than letting changes propagate silently to dashboards.

6. **Simple beats clever.** A daily batch full refresh of a small table is more reliable than a streaming CDC setup. Add incremental logic, streaming and complex orchestration only when volume, latency or cost requires them.

## Discovering context

Before building or changing a pipeline:

- **Existing stack**: orchestrator, transformation framework, warehouse/lake, file formats, naming conventions for layers (e.g. raw/staging/marts, bronze/silver/gold), how secrets and connections are configured. Follow it.
- **Source characteristics**: volume, growth rate, update pattern (append-only? updates? hard deletes?), availability of `updated_at` columns or change logs, rate limits, maintenance windows, and whether reading puts load on a production database (use a replica if so).
- **Consumers and SLAs**: who uses the output, how fresh it must be, what breaks if it is late or wrong, and when they look at it (a dashboard checked at 9 a.m. defines your deadline).
- **Data sensitivity**: PII, financial, health data; masking, access controls, retention and residency rules.
- **Existing quality checks and alerting**, and who is on call.

## Key decisions

### ETL vs ELT

| | ETL (transform before load) | ELT (load raw, transform in target) |
|---|---|---|
| Where compute happens | Pipeline workers | Warehouse/lakehouse engine |
| Raw history kept | Often not | Yes, by design |
| Reprocessing after a logic fix | Re-extract needed | Rebuild from raw |
| Good for | Strict privacy filtering before landing, constrained targets, heavy non-SQL transforms | Modern columnar warehouses, SQL-centric teams, auditability |
| Risk | Logic bugs destroy information irrecoverably | Raw layer grows; sensitive data lands before masking |

Many real systems mix them: light ETL at ingestion (type casting, PII hashing, decompression), ELT for business logic. If sensitive fields must never land in the target, mask or drop them in the extract step.

### Batch vs streaming

| Choose batch when | Choose streaming when |
|---|---|
| Consumers tolerate minutes to hours of latency | Seconds matter to an operational decision (fraud, alerts, inventory) |
| Sources are files, APIs, or databases queried periodically | Source is already an event stream or log |
| Team is small; simplicity and cost matter | You can staff the operational complexity (offsets, state, exactly-once semantics, reprocessing) |

Micro-batching (every few minutes) covers many "real-time" requests at a fraction of the complexity. Ask what decision the latency serves before committing to streaming.

### Full refresh vs incremental vs CDC

| Strategy | How | Use when | Pitfalls |
|---|---|---|---|
| Full refresh | Reload everything each run, swap atomically | Small/medium tables, sources without reliable change markers | Cost grows with size; loses history unless snapshotted |
| Incremental by watermark | Fetch rows with `updated_at > last_watermark` | Source has a reliable, indexed modification timestamp | Misses hard deletes; clock skew and same-timestamp ties; updates that do not bump `updated_at` |
| Incremental by append key | Fetch rows with `id > last_id` | Append-only sources (logs, events) | Misses updates; non-monotonic IDs |
| CDC (log-based) | Read the database's change log (e.g. via Debezium, native replication, vendor CDC) | Large tables, need deletes and every change, low latency | Operational complexity; schema changes in the log; initial snapshot coordination |
| Snapshot + diff | Periodic full extract, compare with previous | No change markers, need deletes, moderate size | Compute cost; needs stable keys |

Watermark tips: use a small overlap (re-read the last N minutes) and dedupe on the primary key in the merge, because transactions commit out of timestamp order and clocks skew. Store the watermark only after the load commits, so a failed run does not advance it.

## Idempotent load patterns

The target operation should be determined by the window being processed, so running it twice gives the same result.

- **Partition overwrite**: each run owns a partition (e.g. a date). Delete-and-insert or atomically replace that partition. Natural for event data by event date.
- **Merge/upsert on a key**: `MERGE` into the target on the business or primary key, updating changed rows and inserting new ones. Natural for dimension/entity tables.
- **Staging-then-swap**: load into a staging table, validate, then swap or rename into place in one transaction. Consumers never see partial data.
- **Append with dedup**: append raw records with an ingestion ID, and dedupe in the next layer by key and latest version. Useful in raw layers where you want every version.

Illustrative merge (syntax varies by engine):

```sql
MERGE INTO analytics.customers AS t
USING staging.customers_batch AS s
  ON t.customer_id = s.customer_id
WHEN MATCHED AND s.source_updated_at > t.source_updated_at THEN
  UPDATE SET email = s.email, plan = s.plan,
             source_updated_at = s.source_updated_at,
             loaded_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
  INSERT (customer_id, email, plan, source_updated_at, loaded_at)
  VALUES (s.customer_id, s.email, s.plan, s.source_updated_at, CURRENT_TIMESTAMP);
```

The `s.source_updated_at > t.source_updated_at` guard prevents an older replayed batch from overwriting newer data.

Anti-pattern: `INSERT INTO target SELECT * FROM source WHERE date = today()` with no delete or key — a retry doubles the day.

Also make runs **parameterised by window**, not by "now". A task that computes "yesterday" from the wall clock cannot be rerun for last month. Pass the logical date/interval in from the orchestrator.

## Handling deletes, late data and history

- **Deletes**: decide whether consumers need them. Options: CDC delete events, soft-delete flags in the source, periodic full key comparison, or accept that deletes are not reflected (document it).
- **Late-arriving data**: events can arrive hours or days after their event time (mobile clients offline, partner files resent). Reprocess a trailing window (e.g. last 3 days) on each run, or trigger reprocessing of affected partitions when late data lands. Define and document how late is "too late".
- **Slowly changing dimensions**: if analysts need "what was the customer's plan at the time of the order", keep history (valid_from / valid_to rows, a.k.a. type-2) rather than overwriting. Decide per attribute; history everywhere is expensive and confusing.
- **Timezones**: store timestamps in UTC with an explicit type; convert at presentation. Daily partitions need a defined timezone ("day" in UTC vs local business day). DST transitions create 23- and 25-hour days; do not assume 24.

## Schema evolution

Sources add, remove, rename and retype fields. Decide a policy per layer:

| Change | Raw layer | Modelled layers |
|---|---|---|
| New column | Accept automatically (schema-on-read formats or auto-add) | Ignore until deliberately modelled |
| Removed column | Keep column, nulls going forward; alert | Alert; consumers may break |
| Type change (int → string) | Land as source type or string; alert | Fail or quarantine; never silently coerce |
| Renamed column | Looks like remove + add; alert | Map deliberately |
| Semantic change (cents → dollars, new enum values) | Undetectable by schema; needs value checks | Quality checks on ranges and accepted values |

Practices: capture the source schema with each load; diff it against the previous one; fail loudly on breaking changes in modelled layers; version data contracts with important source owners where you can. For your own target schema changes, follow `database-migrations` (expand-and-contract, backfill, then remove).

## Data quality checks

Run checks at ingestion and after transformation, and decide the response for each: fail the pipeline (block publishing), warn, or quarantine bad rows.

| Check | Example | Typical response |
|---|---|---|
| Freshness | max(event_time) within 2 hours of now | Alert |
| Volume | row count within ±30% of trailing 7-day median for this weekday | Warn; fail on zero |
| Uniqueness | primary key unique in target | Fail |
| Not null | required columns non-null | Fail or quarantine rows |
| Referential integrity | every order.customer_id exists in customers | Warn (late dimension) or fail |
| Accepted values | status in a known set | Warn on new values |
| Ranges | amount >= 0; dates not in the future | Quarantine |
| Reconciliation | sum(amount) in target equals sum in source for the window | Fail |
| Distribution drift | null rate or mean shifts sharply | Warn |

Tools such as dbt tests, Great Expectations, Soda, or engine-native constraints implement these; plain SQL assertions work too. Prefer a few high-value checks that block bad data over dozens of warnings everyone ignores. See `data-cleaning-and-validation` for rule design.

**Write-audit-publish**: write to a staging location, run checks, publish (swap) only if they pass. This keeps bad data from ever reaching consumers.

## Orchestration

An orchestrator schedules tasks, manages dependencies, retries, passes the logical run window, and records history. Examples: Airflow, Dagster, Prefect, Argo Workflows, cloud-native schedulers and step-function services, dbt for in-warehouse transformation DAGs.

Design guidance:
- **Tasks should be idempotent and atomic** units: extract one source window, load one table, run one model. Small tasks are retriable; giant tasks are not.
- **Pass the logical interval** to every task; never compute "now" inside.
- **Dependencies on data, not just on tasks**: an upstream system that is not orchestrated by you needs a sensor or a freshness check before downstream runs.
- **Retries with backoff** for transient errors; no retries for logic or data-quality failures (they will fail again).
- **Concurrency limits** per source to respect rate limits and database load; prevent overlapping runs of the same pipeline window.
- **Catch-up behaviour**: when a schedule is paused or deployed late, decide whether missed intervals should run (catch-up/backfill) or be skipped. Defaults differ by tool; set it explicitly.
- **Keep business logic out of DAG definition files**; put it in modules or SQL models that can be tested independently.
- **SLAs/deadlines** on the critical outputs, alerting when they are at risk, not only when they fail.

## Backfills

Backfills rewrite history; treat them as a deployment.

1. **Define scope**: which tables, which date range, why. Estimate the cost (compute, API calls, source load).
2. **Check idempotency**: confirm the load pattern overwrites/merges per window. If it appends, fix that first.
3. **Check source availability**: does the source still have the history (API retention limits, log retention for CDC)? If not, rebuild from your raw layer.
4. **Run on a sample** (one day/partition) into a non-production target, compare with current data, review differences.
5. **Throttle**: limit concurrency to protect the source and the warehouse; schedule off-peak.
6. **Communicate** to consumers: numbers will change for the period; dashboards may be inconsistent during the run.
7. **Run, verify** with reconciliation and quality checks per partition, and record what was backfilled and when.

Never run a large backfill directly against production targets without a sample run and a rollback plan (snapshot or time-travel feature, or a copy of the affected partitions).

## Lineage, metadata and observability

- **Load metadata columns** on every row or partition: source system, extract timestamp, load timestamp, run ID, pipeline/code version. They make debugging possible.
- **Lineage**: know which upstream tables and columns feed each output. Many orchestration and transformation tools derive it; at minimum, document it. It answers "what breaks if this source changes?" and "where did this number come from?"
- **Run metrics**: duration, rows read/written/rejected per task, bytes scanned, cost. Trend them; a slowly growing duration predicts a future SLA miss.
- **Alert on outcomes** (freshness, volume, failed checks) routed to an owner, with runbooks for common failures. See `observability`.

## Cost and performance

Pipelines tend to get more expensive quietly, as data grows and schedules get more frequent. Keep an eye on:

- **Partitioning and clustering** target tables by the columns used to filter (usually a date), so incremental loads and queries scan only what they need.
- **Incremental models** for large transformations instead of rebuilding everything each run, once a full rebuild becomes slow or costly. Keep a periodic full rebuild (e.g. weekly) to correct drift if incremental logic can miss changes.
- **Columnar file formats** (e.g. Parquet, ORC) with compression for lake storage; avoid many tiny files, which slow every reader, by compacting.
- **Schedule frequency matched to need**: hourly refreshes of a table read once a day waste compute.
- **Extract pressure on sources**: read from replicas, use indexed filters, limit concurrency, and avoid `SELECT *` across wide tables you only partly use.
- **Track cost per pipeline** where the platform exposes it, and review the top consumers periodically.

## Process for building a pipeline

1. **Specify the output**: grain (one row per what?), columns and meaning, freshness requirement, consumers.
2. **Profile the source**: sample data, volume, keys, nulls, update and delete behaviour, timezone of timestamps, quirks.
3. **Choose strategy**: batch/stream, full/incremental/CDC, ETL/ELT, using the tables above. Start with the simplest that meets requirements.
4. **Land raw** with metadata; make the extract window-parameterised.
5. **Transform** in testable steps; keep each model's purpose single and named.
6. **Load idempotently** (overwrite partition, merge, or swap).
7. **Add quality checks** on the outputs that matter, with explicit fail/warn behaviour.
8. **Orchestrate** with retries, concurrency limits, catch-up policy and alerts.
9. **Test**: unit-test transformation logic on small fixtures; run end-to-end on a sample window; rerun the same window and confirm identical results.
10. **Document**: grain, sources, refresh schedule, known limitations (e.g. deletes not tracked), owner.

## Worked examples

Illustrative; adapt syntax to your engine and orchestrator.

### Window-parameterised, idempotent daily load

The orchestrator passes the logical date; the task owns exactly that partition.

```python
def load_orders(ds: str) -> None:              # ds = "2026-03-01", supplied by the orchestrator
    start, end = f"{ds}T00:00:00Z", next_day_utc(ds)
    rows = extract_orders(updated_from=start, updated_to=end, overlap_minutes=15)
    stage_table = f"staging.orders_{ds.replace('-', '')}"
    write_table(stage_table, rows, metadata={"run_ds": ds, "extracted_at": utcnow()})
    run_checks(stage_table, checks=["pk_unique:order_id", "not_null:customer_id", "row_count>0"])
    merge_into("analytics.orders", stage_table, key="order_id", version_col="source_updated_at")
```

Running `load_orders("2026-03-01")` today, tomorrow, or twice in a row leaves `analytics.orders` in the same state for that day. The checks run before the merge, so bad data never reaches consumers (write-audit-publish).

### Watermark handling that does not lose rows

```python
wm = read_watermark("crm_contacts")                     # e.g. 2026-03-01T10:00:00Z
rows = fetch_contacts(updated_since=wm - timedelta(minutes=10))  # overlap for late commits
max_seen = max((r["updated_at"] for r in rows), default=wm)
upsert("raw.crm_contacts", rows, key="contact_id")
commit()
write_watermark("crm_contacts", max_seen)               # only after the load committed
```

Two details matter: the overlap window re-reads rows that committed late with older timestamps, and the watermark comes from the data (`max_seen`), not from the wall clock, so clock skew between your worker and the source cannot create a gap.

### Row-count reconciliation query

```sql
-- Compare source extract with target for one day; non-zero diff fails the run
SELECT s.cnt AS source_rows, t.cnt AS target_rows, s.cnt - t.cnt AS diff,
       s.amt - t.amt AS amount_diff
FROM (SELECT COUNT(*) cnt, SUM(amount) amt FROM staging.orders_20260301) s
CROSS JOIN (SELECT COUNT(*) cnt, SUM(amount) amt
            FROM analytics.orders
            WHERE order_date = DATE '2026-03-01') t;
```

### Diagnosing "the dashboard number doubled"

1. Check uniqueness of the key in the target table for the affected period. Duplicates → which load runs wrote them (use run-ID metadata columns)?
2. Common causes, in rough order of frequency: an append-only load retried; a join to a dimension with duplicate keys (fan-out); a backfill overlapping with a regular run without partition overwrite; a source that started emitting updates as new rows.
3. Fix the load pattern first (merge/overwrite, dedupe in staging, enforce a uniqueness check that fails the run), then repair the affected partitions by rerunning them — which is safe only once the load is idempotent.

## Pitfalls and anti-patterns

- **Append-only loads without dedup**, doubling data on every retry.
- **"Now"-relative logic** inside tasks, making reruns and backfills wrong.
- **Advancing the watermark before the load commits**, losing data on failure.
- **Trusting `updated_at`** without checking that every write path updates it.
- **Silent type coercion** turning bad values into nulls or zeros.
- **Fan-out joins** duplicating rows (joining to a non-unique key); always check row counts before and after joins.
- **Timezone confusion**: mixing local and UTC timestamps; daily partitions in an undefined zone.
- **Reading from the primary production database** during peak hours, degrading the application.
- **Monolithic tasks** that do extract, transform and load of twenty tables in one step.
- **Only alerting on job failure**, missing empty or stale loads.
- **PII copied into every layer** and every developer's sandbox.
- **Backfilling straight into production** without a sample comparison.
- **Ignoring cost**: full scans of huge tables every hour; unpartitioned tables; streaming where hourly batch would do.

## Verification

- [ ] Rerunning the same window twice yields identical target state (counts and checksums match).
- [ ] A forced failure mid-run followed by a rerun produces correct results with no duplicates or gaps.
- [ ] Row counts and key aggregates reconcile with the source for a sample window.
- [ ] Primary key uniqueness and not-null checks pass on outputs.
- [ ] Freshness and volume alerts exist and were tested (e.g. by pausing the source in a test environment).
- [ ] Late-arriving and deleted records behave as documented.
- [ ] Schema change in the source (add a column, change a type in a test copy) produces the intended behaviour.
- [ ] Timestamps are UTC/explicitly zoned; daily boundaries are defined.
- [ ] Secrets come from the configured secret store, not code; sensitive data masked where required.
- [ ] Backfill procedure tried on at least one historical partition.

## Reporting back

State: what the pipeline moves and at what grain, load strategy and why, schedule and freshness guarantees, quality checks and what they block, known limitations (deletes, late data, history), how to rerun or backfill a window, cost/volume expectations, and what you could not verify (e.g. no access to production source).
