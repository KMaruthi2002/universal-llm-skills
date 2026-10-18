# Query Plans and Indexing for Queries

Every relational engine turns SQL into a tree of operators. Reading that tree tells you where time goes. Operator names differ between engines, but the concepts below are shared.

## Getting a plan

- **Estimated plan** (e.g. `EXPLAIN`): shows the chosen strategy and estimated row counts and costs, without running the query. Safe on any query.
- **Actual plan** (e.g. `EXPLAIN ANALYZE`, actual execution plans, or profiling modes): runs the query and reports real row counts, loops, and timings per operator. Much more informative; it executes the statement, so for writes use a transaction you roll back, and be careful with heavy queries on production primaries.
- Include buffer or I/O statistics where the engine offers them; they distinguish "slow because it reads a lot from disk" from "slow because of CPU work".
- Use realistic data. Plans on a tiny development database often differ completely from production, because the optimiser correctly decides that scanning ten rows is cheapest.

Read plans from the innermost (most indented / leaf) operators outward; the leaves read data, the parents combine it.

## Access operators

| Operator (generic name) | What it does | Good when | Bad when |
|---|---|---|---|
| Sequential / full table scan | Reads every row | Small tables; queries returning a large fraction of rows | Large table, few rows needed |
| Index seek / index scan with condition | Navigates the index to matching keys | Selective predicates | Many matches, each requiring a random table lookup |
| Index-only / covering scan | Answers from the index without touching the table | Hot read paths | Visibility metadata stale (some engines must still check the table) |
| Bitmap index scan + heap scan | Collects matching locations, then reads table pages in order | Medium selectivity; combining multiple indexes | — |
| Range / partition pruning | Skips partitions not matching the filter | Time-partitioned tables queried by time | Filter does not include partition key |

A full scan is not automatically bad. Reading 40% of a table via an index is often slower than scanning it, because random lookups cost more than sequential reads.

## Join algorithms

| Algorithm | How | Efficient when |
|---|---|---|
| Nested loop | For each outer row, look up matching inner rows (ideally via index) | Outer side small, inner side indexed on the join key |
| Hash join | Build a hash table from one side, probe with the other | Large unsorted inputs, equality joins, enough memory for the build side |
| Merge join | Walk two inputs sorted on the join key | Both inputs already sorted (e.g. via indexes) or large inputs where sorting is acceptable |

The classic pathology: the optimiser estimates the outer side has 10 rows, picks a nested loop, and the outer side actually has 500,000 — producing 500,000 index lookups. The cause is almost always a bad row estimate.

## Row estimates and statistics

The optimiser chooses plans based on estimated row counts derived from statistics (histograms, distinct counts, most-common values). Estimates go wrong when:
- Statistics are stale after large data changes — refresh them (e.g. `ANALYZE` or the engine's equivalent) and see if the plan changes.
- Predicates involve correlated columns (`city = 'Paris' AND country = 'France'`): the optimiser often assumes independence and underestimates. Some engines support multi-column / extended statistics.
- Predicates use functions or expressions the optimiser cannot estimate; rewrite or add expression statistics or indexes.
- Parameter values vary wildly in selectivity (one tenant with 90% of rows) and a cached plan chosen for one value is reused for another. Engines handle this differently (custom vs. generic plans, parameter sniffing); options include query hints, plan guides, recompilation, or splitting queries for the large tenant.

**Compare estimated and actual rows at each operator.** A gap of 10× or more at a node near the bottom of the tree is usually the root cause of a bad plan above it.

## Sorting, grouping, and memory

- Sorts and hash aggregates that exceed working memory spill to disk and slow down sharply. The plan usually reports this.
- An index whose order matches `ORDER BY` lets the engine skip the sort entirely — especially valuable with `LIMIT`, where it can stop after the first N rows.
- `GROUP BY` can use a sorted (stream) aggregate if input arrives ordered, or a hash aggregate otherwise.

## Reasoning through an index for one query

Example query:
```sql
SELECT id, total, created_at
FROM orders
WHERE tenant_id = :t AND status = 'open' AND created_at >= :since
ORDER BY created_at DESC
LIMIT 50;
```

1. **Equality predicates**: `tenant_id`, `status`. Put them first.
2. **Range / sort column**: `created_at` is both the range filter and the sort key. Put it next, so matching rows are contiguous and already ordered.
3. Candidate: `(tenant_id, status, created_at)`. The engine seeks to `(t, 'open', since)` and reads backwards, stopping after 50 rows — no sort needed.
4. **Covering**: add `id, total` as included columns (or trailing key columns) if this query is hot, so the table is never touched.
5. **Partial alternative**: if almost all queries target `status = 'open'` and open orders are a small fraction, `(tenant_id, created_at) WHERE status = 'open'` is smaller and faster.
6. **Check existing indexes first**: an existing `(tenant_id, created_at)` index may already be nearly as good; adding another index costs writes and storage.
7. **Verify**: run the actual plan; confirm an index seek, no sort, and low rows examined. Measure before and after.

Rules of thumb:
- Column order in a composite index matters far more than which columns are included.
- One well-designed composite index often serves several queries; design for the set of queries on a table, not one at a time.
- Indexes on low-selectivity columns alone rarely help.
- Each extra index adds write cost; on write-heavy tables, be stingy.

## When the index exists but is not used

Check:
- A function or cast is applied to the indexed column in the predicate.
- Type mismatch between the column and the parameter (implicit conversion).
- Leading column of the composite index is not constrained.
- Collation mismatch for text comparisons.
- The optimiser estimates (correctly or not) that a scan is cheaper — look at estimates.
- `OR` conditions or `NOT` predicates that the engine cannot map to an index range.
- The query targets a different partition or view than you think.

## Beyond indexes

If indexing cannot fix it:
- Rewrite: pre-aggregate before joining, replace a correlated subquery with a join or lateral join, split an `OR` into `UNION ALL`, push filters into subqueries.
- Reduce the work: fewer columns, smaller time window, pagination.
- Precompute: summary tables, materialised views, incremental aggregates.
- Change the shape: partition large tables, archive cold data.
- Move analytical workloads to a replica or an analytics store.
