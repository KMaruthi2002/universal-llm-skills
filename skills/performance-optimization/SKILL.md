---
name: performance-optimization
description: >-
  Make software measurably faster or leaner, driven by measurement rather
  than guesswork: define the goal, profile CPU, memory, I/O and lock
  contention, find the real hot spot, apply the right fix (algorithmic
  complexity, data layout, caching, batching, lazy or avoided work,
  concurrency, database and network round trips), write benchmarks that
  don't lie, and guard against regressions with budgets. Use when code,
  queries, services, jobs or builds are slow, use too much memory or CPU,
  miss latency or throughput targets, cost too much to run, or when asked to
  "optimize", "speed up", or "profile". For browser page-load and Core Web
  Vitals audits use web-performance-audit; for SQL tuning specifics see
  sql-and-queries.
metadata:
  category: development
  related: debugging, sql-and-queries, database-design, concurrency-and-async, observability, system-design, web-performance-audit, refactoring
---

# Performance Optimization

Performance work is an empirical science. The system is the experiment; profilers and benchmarks are the instruments; intuition supplies hypotheses but never conclusions. Programmers' guesses about where time goes are wrong often enough that the first rule is simply: **measure before you change anything, and measure again after.**

## Scope

Covers: improving latency, throughput, memory use, startup time, resource cost, and efficiency of code, services, queries, batch jobs, and builds, in any language.

Neighbours:

- Page load, rendering, Core Web Vitals, bundle size from the browser's perspective → `web-performance-audit`.
- Query plans, indexes, SQL rewriting → `sql-and-queries`; schema decisions → `database-design`.
- Capacity planning, scaling architecture, caching tiers across systems → `system-design`.
- Parallelism and async mechanics → `concurrency-and-async`.
- Production metrics, tracing, and dashboards → `observability`.

## Core principles

1. **Have a target.** "Faster" is not a goal; "p95 latency of the search endpoint under 200 ms at 500 requests/second" is. A target tells you when to stop, which metric matters (latency vs throughput vs memory vs cost), and which percentile. Without one, optimisation never ends and trades clarity for unmeasured gains.

2. **Measure, don't guess.** Profile the real workload before choosing what to optimise. The hot spot is frequently somewhere unexpected: logging, serialisation, a regex compiled in a loop, an N+1 query, lock contention, GC pressure, a misconfigured pool.

3. **Optimise the bottleneck, and only the bottleneck.** By Amdahl's law, speeding up a part that takes 5% of the time by infinity gains at most 5%. Find the dominant cost, fix it, re-measure — the bottleneck moves.

4. **Algorithms and round trips before micro-tuning.** Changing O(n²) to O(n log n), or 1,000 queries to 1, routinely yields 10–1000×. Micro-optimisations typically yield 1.1–2× and cost readability. Exhaust the big levers first.

5. **The fastest work is work not done.** Avoid, defer, batch, or cache before trying to make the work itself faster.

6. **Correctness first, then speed.** An optimisation that changes results is a bug. Keep tests green, and compare outputs before and after for anything numeric or order-sensitive.

7. **Performance is a feature that regresses.** Without automated checks (benchmarks with thresholds, latency SLO alerts), gains erode silently. Lock in what you win.

## Process

### 1. Define the problem precisely

- **What is slow, for whom, and how slow?** Specific operation, input size, environment, percentile. "Exporting a 50k-row report takes 90 s; users time out at 60 s."
- **Which metric?** Latency (per-request time; look at percentiles, not averages — p50 hides tail pain, p99 reveals it), throughput (operations per second), resource use (CPU, memory, I/O, network, money), startup time, or perceived performance (time to first useful output).
- **What is the target and the budget?** How much effort and complexity is acceptable? Is a 2× improvement enough, or is 10× needed (which usually implies an algorithmic or architectural change)?
- **Has it regressed?** If it used to be fast, this is a debugging problem — bisect to the change (see `debugging`).

### 2. Build a reproducible measurement

- Reproduce with **realistic data volume and shape**. Many performance bugs appear only at production scale (N+1 queries look fine with 3 rows) or with production distributions (skewed keys, very long strings).
- Make the measurement **repeatable**: same input, same environment, warmed up where relevant, multiple runs, report median and spread.
- Record the **baseline** before changing anything.

### 3. Profile to find where the cost is

Choose the instrument for the resource:

| Question | Instrument (examples) |
|---|---|
| Where does CPU time go? | Sampling CPU profiler: `perf`, `py-spy`, `async-profiler`, `pprof`, Instruments, browser/Node DevTools, dotnet-trace. Render as a flame graph. |
| Where does wall time go (including waiting)? | Wall-clock / off-CPU profiling, tracing spans, request timing breakdowns. A request that is slow but CPU-idle is waiting on I/O, locks, or downstream services. |
| Why is memory high or growing? | Heap profilers and snapshots (allocation sites, retained size), GC logs. Compare two snapshots to find growth. |
| How much are we allocating? | Allocation profilers; high allocation rate drives GC pauses even when heap size is fine. |
| Is it the database? | Query logs with timings, slow-query logs, `EXPLAIN (ANALYZE)` plans, ORM query counting. |
| Is it the network or downstream service? | Distributed tracing, client-side timing per call, connection pool metrics. |
| Is it lock contention? | Lock/mutex profilers, thread dumps taken repeatedly (the same stack appearing in many threads = contention point). |
| Is it the disk? | I/O stats (`iostat`, per-process I/O), syscall tracing (`strace`, `dtruss`, ETW). |
| Is it the system as a whole? | USE method per resource: Utilization, Saturation, Errors — for CPU, memory, disk, network. |

**Reading a flame graph:** width is proportion of samples (time); the y-axis is stack depth. Look for wide plateaus — functions where much time is spent *themselves* (self time) rather than in children. A wide frame in a library you call (JSON encoding, regex, hashing, logging) often means you are calling it too often or with too much data.

**Profiling pitfalls:** profiling a debug build (different optimisations); profiling with tiny inputs; instrumentation overhead distorting short functions (prefer sampling); a profiler attached to the wrong process or thread; JIT languages not warmed up.

If you cannot run a profiler, use coarse timing: timestamps around phases (load, compute, serialise, write), logged per run. Bisecting time across phases finds the hot area quickly.

### 4. Form a hypothesis and pick the lever

With the hot spot identified, ask *why* it is expensive and which lever addresses that cause. See the catalogue below. Estimate the potential gain: if the hot function is 40% of time, even eliminating it yields 1.67×; if the target is 5×, you need a different approach (architectural, algorithmic, or parallel).

### 5. Change one thing, measure again

- Make a single change, re-run the same measurement, compare with the baseline (median and spread). If the difference is within noise, it isn't an improvement.
- Keep a log: change → result. It prevents re-trying ideas and documents the reasoning for reviewers.
- Revert changes that didn't help; they add complexity without benefit.

### 6. Verify correctness and side effects

- Tests pass; outputs match the old implementation on a representative set (exactly, or within an agreed tolerance for floating point).
- Check other metrics didn't worsen: memory traded for speed, latency traded for throughput, a cache that serves stale data, increased load on a downstream system.

### 7. Lock it in

- Add a benchmark or performance test for the path, with a threshold that fails CI (or alerts) on significant regression.
- Document non-obvious optimisations in code comments: *why* the code is shaped this way, the measurement that justified it, and what would invalidate it. Otherwise the next refactor will undo it.

## The catalogue of levers

Roughly in order of typical payoff.

### Do less work

- **Better algorithm / data structure.** Nested loops searching lists → hash map lookups (O(n²) → O(n)). Repeated sorting → maintain a sorted structure or heap. Linear scans for membership → sets. Recomputing aggregates → maintain them incrementally.
- **Avoid unnecessary work.** Remove redundant computation, duplicate validation, repeated parsing, conversions back and forth, logging of large objects at levels that are then discarded (construct log messages lazily).
- **Early exit.** Short-circuit when the answer is known; stop scanning after the first match; paginate.
- **Lazy evaluation / deferral.** Compute only when needed; stream rather than materialise; move non-urgent work (emails, thumbnails, analytics) to background jobs.
- **Reduce data volume.** Select only needed columns, fetch only needed rows, compress payloads, avoid over-fetching in APIs, use projections.

### Do work fewer times: caching and memoisation

Caching is powerful and dangerous. Before adding a cache, answer:

- **What is the hit rate likely to be?** A cache with a 5% hit rate adds cost and complexity for little benefit. Measure access patterns (key repetition) first.
- **How is it invalidated?** Time-to-live (simple, tolerates staleness up to the TTL), explicit invalidation on write (fresh but easy to get wrong), versioned keys (write a new key; old ones expire). "There are only two hard things…" — invalidation bugs produce wrong data, which is worse than slow data.
- **How stale may data be?** Ask the user/product owner; the answer differs for prices, permissions, and avatars.
- **Where does it live?** In-process (fastest; per-instance, inconsistent across instances, lost on restart, memory-bound), shared (e.g. Redis/Memcached; consistent across instances; network hop), HTTP/CDN (for public, cacheable responses), database-level (materialised views, query caches).
- **Is it bounded?** Unbounded caches are memory leaks. Use size limits and an eviction policy (LRU/LFU).
- **Stampede protection.** When a hot key expires, many requests recompute simultaneously. Use request coalescing (single flight), early probabilistic refresh, or stale-while-revalidate.
- **Key correctness.** Include every input that affects the result in the key (user, locale, permissions, version). A key missing a dimension serves one user's data to another — a security bug.

Never cache permission or authentication decisions without careful invalidation; never cache personal data in shared/CDN caches.

### Do work in bulk: batching

- **N+1 queries**: loading a list then querying per item. Fix with joins, `IN (...)` batch loads, ORM eager loading, or a data loader that batches within a request.
- **Chatty network calls**: combine into batch APIs, pipeline requests, or bulk endpoints.
- **Writes**: bulk inserts/updates, batched commits (fewer fsyncs), buffered writes.
- **Trade-off**: batching raises latency of the first item and memory use; choose batch sizes empirically (often a few hundred to a few thousand rows), and bound them.

### Do work faster: efficiency of the code itself

- **Avoid repeated allocation** in hot loops: reuse buffers, pre-size collections, avoid creating intermediate lists/strings.
- **String building**: use builders/joins instead of repeated concatenation in loops (quadratic in many languages).
- **Data layout**: contiguous arrays of values are far faster to scan than linked structures of pointers (CPU cache locality). Struct-of-arrays can beat array-of-structs for column-wise processing.
- **Hoist invariants** out of loops: compiled regexes, lookups, configuration reads.
- **Use the platform's optimised primitives**: vectorised numerical libraries, built-in sort, bulk copy, native JSON parsers.
- **Reduce serialisation cost**: choose efficient formats for internal high-volume paths; avoid serialising the same object repeatedly.
- **Avoid exceptions for control flow** in hot paths in languages where they are expensive.
- **GC tuning** comes after reducing allocation; tuning flags rarely beats allocating less.

### Do work concurrently

- **Overlap I/O**: issue independent network/database calls concurrently rather than sequentially. Total latency becomes the max, not the sum.
- **Parallelise CPU-bound work** across cores when the work is divisible and large enough to amortise coordination overhead; mind the language runtime's model (e.g. a global interpreter lock means CPU parallelism requires processes or native code).
- **Pipeline** stages so each runs while others do.
- **Concurrency adds risk** (races, contention, nondeterminism) and can *reduce* performance via contention and context switching. Measure; see `concurrency-and-async`.

### Database and network hot spots

- **Count queries per request.** A simple per-request query counter often reveals N+1 problems instantly.
- **Look at query plans** for the slowest and most frequent queries: missing indexes (sequential scans on large tables), wrong join order, functions on indexed columns preventing index use, implicit casts, `OFFSET` pagination over large offsets (prefer keyset/cursor pagination). See `sql-and-queries`.
- **Connection pools**: too small → waiting; too large → database overload. Size to the database's capacity, not the number of app threads.
- **Round-trip latency dominates** for small requests: 1 ms × 1,000 sequential calls = 1 s. Reduce round trips before optimising the server side.
- **Payload size**: compress, paginate, and avoid returning fields nobody uses.
- **Timeouts and retries** affect tail latency; retry storms can turn a slowdown into an outage (see `error-handling`).

### Memory

- **Leaks** in managed languages are retained references: growing caches, listeners never removed, static collections, closures capturing large objects. Find with snapshot diffs.
- **Peak usage**: stream large files/results instead of loading them whole; process in chunks.
- **Representation**: compact types (ints vs boxed objects, arrays vs maps of small objects), interning repeated strings, avoiding per-object overhead for millions of tiny objects.
- **Memory vs speed trade-offs**: caches and precomputation spend memory to save time; make the trade explicit and bounded.

## Benchmarks that don't lie

A benchmark is an experiment; most bad benchmarks fail as experiments.

- **Use a benchmark harness** where available (e.g. JMH for the JVM, BenchmarkDotNet, Go's `testing.B`, Criterion for Rust, `pytest-benchmark`/`pyperf`, `hyperfine` for commands). Harnesses handle warm-up, iteration counts, and statistics that hand-rolled loops get wrong.
- **Warm up** JIT-compiled and cached systems; measure steady state unless cold start is the metric.
- **Defeat dead-code elimination**: the compiler may remove work whose result is unused. Consume results (harnesses provide "black hole" helpers).
- **Control the environment**: same machine, quiet system, fixed CPU frequency where possible, no thermal throttling, no other heavy processes. Cloud and laptop environments are noisy — expect variance of several percent.
- **Repeat and report distributions**: median plus spread (interquartile range or confidence interval). A 3% difference with 5% noise is no difference.
- **Use realistic inputs**: sizes and distributions like production. A benchmark on sorted input says little about random input.
- **Benchmark the whole operation the user experiences**, not only the micro-step, before claiming user-visible gains. A 10× faster function that is 2% of request time is a 2% gain.
- **Beware caching effects**: the second run reads from warm caches (OS page cache, CPU cache, database buffer pool). Decide which state you are measuring and control it.
- **Load tests**: ramp gradually; measure latency percentiles at each load level; find the knee where latency rises sharply (saturation). Avoid coordinated omission — tools that wait for a slow response before sending the next request under-report tail latency; use open-model load generators for latency SLOs.
- **Never benchmark in production without agreement** — load tests can cause outages.

## Regression budgets

- **Set budgets** for key operations: latency percentiles, memory ceilings, bundle sizes, startup times, query counts per request. Derive them from the target, with some headroom.
- **Automate checks**: benchmarks in CI comparing against a baseline with a tolerance above the noise floor (e.g. fail on > 10% regression if noise is ~3%); query-count assertions in integration tests; production SLO alerts.
- **Treat noise carefully**: CI machines are noisy. Use relative comparison on the same machine in the same run (baseline vs change), multiple repetitions, or dedicated runners. A flaky performance check gets ignored like a flaky test.
- **Track trends**: small regressions accumulate; dashboards over releases reveal slow drift no single PR shows.

## Queueing intuition

Latency under load is dominated by queueing, not by service time. As utilisation of a resource approaches 100%, waiting time grows sharply — in simple models proportionally to ρ / (1 − ρ), so going from 50% to 90% utilisation multiplies the wait by about 9, and from 90% to 95% roughly doubles it again. Practical consequences:

- **Keep headroom.** Systems that must hold tail latency targets typically run key resources well below saturation (often 60–75%).
- **Small reductions in service time give large tail gains near saturation**, because they reduce utilisation.
- **Variance hurts.** Occasional very slow requests (large payloads, cold caches, GC pauses) inflate everyone's waiting time behind them. Isolating slow work (separate pools or queues) protects fast work.
- **Little's law** (in-flight = throughput × latency) helps size pools and check that load-test results are consistent.

## Specific targets

- **Startup / cold start**: profile startup itself; defer initialisation until first use; avoid loading large modules, configurations, or datasets eagerly; reuse connections; for serverless, keep deployment artifacts small and initialise clients outside the handler.
- **Batch jobs**: measure throughput per stage; overlap reading, processing, and writing; use bulk database operations; parallelise across partitions; checkpoint so reruns don't redo work.
- **Builds and test suites**: measure where time goes (most build tools emit timing reports); cache dependency installs and intermediate artefacts; parallelise; avoid rebuilding unchanged modules; move slow tests to a later tier (see `testing-strategy`, `ci-cd-pipelines`).
- **Memory-constrained environments** (containers, mobile, embedded): measure peak resident memory under realistic load; stream; prefer compact representations; set limits that match the runtime's own heap settings.
- **Client-side computation** (heavy UI rendering, large lists): virtualise long lists, avoid unnecessary re-renders, move heavy computation off the main thread; for page-load metrics see `web-performance-audit`.
- **Cost**: CPU-seconds, memory-hours, egress, and per-request pricing of managed services. Sometimes the optimisation goal is the bill rather than latency; measure cost per unit of work.

## A worked example (illustrative)

Problem: an "order history" endpoint has p95 of 2.4 s; target is 300 ms.

1. *Baseline*: load test at production-like traffic with a copy of production-shaped (sanitised) data: p50 900 ms, p95 2.4 s.
2. *Profile*: tracing shows 85% of time in database calls; a per-request query counter reports 1 + 2N queries (N ≈ 50 orders): one per order for items and one for shipping status. CPU profile shows 8% in JSON serialisation.
3. *Lever 1 — round trips*: batch-load items and statuses with two `IN (...)` queries. Result: p95 420 ms. The bottleneck has moved.
4. *Re-profile*: the orders query sorts the user's full history and applies `OFFSET` pagination; the plan shows a sequential scan and sort.
5. *Lever 2 — query/index*: add a composite index on (user_id, created_at) and switch to keyset pagination. Result: p95 180 ms. Target met.
6. *Stop*: serialisation at 8% is not worth touching now.
7. *Lock in*: an integration test asserts the endpoint issues at most 4 queries for a 50-order user; the load test runs before releases with a p95 budget of 300 ms.

No caching was introduced; the problem was work multiplied by N, not work repeated.

## Decision guidance

| Situation | Likely best lever |
|---|---|
| Time grows faster than linearly with input | Algorithm/data structure |
| Many small queries or calls per operation | Batching, joins, eager loading |
| Same expensive result computed repeatedly with same inputs | Caching/memoisation (with invalidation plan) |
| Slow but CPU idle | I/O, locks, or downstream latency — overlap or reduce waits |
| CPU at 100% on one core, others idle | Parallelism, if work is divisible |
| High GC time / pauses | Reduce allocation rate before tuning the collector |
| Slow only at high load | Contention, pool sizes, queueing; load-test and profile under load |
| Slow only on first request | Cold start: lazy initialisation, warm-up, connection setup, JIT |
| Need 10× and profiling shows evenly spread cost | Architectural change (precompute, different storage, async processing), not tuning |
| Gain would be < noise or < 5% of user-visible time | Stop; not worth the complexity |

## Discovering context

- **Find existing performance tooling**: benchmark suites, load-test scripts, profiling configs, APM/tracing dashboards, query logs. Use what the team already trusts.
- **Learn the targets**: SLOs, SLAs, budgets in docs or CI. If none exist, ask the user what "fast enough" means before investing.
- **Understand production shape**: data sizes, traffic patterns, hardware, deployment topology. Ask for representative (sanitised) data if local data is toy-sized.
- **Match the codebase's idioms** when optimising; a hand-rolled exotic structure in a codebase that uses standard library collections needs strong justification and comments.
- **Check for known constraints**: memory limits of containers, cold start limits of serverless platforms, rate limits of downstream APIs.

## Trade-offs to surface to the user

Most optimisations buy speed with something else. Name the trade before committing to it:

- **Freshness** — caches and precomputation serve older data. How old is acceptable?
- **Memory and cost** — caches, replicas, larger instances, precomputed tables.
- **Complexity** — new infrastructure (a cache cluster, a queue), harder-to-read code, more failure modes to operate.
- **Consistency** — async processing and eventual consistency mean users may briefly see old state.
- **Latency vs throughput** — batching improves throughput but delays individual items; parallelism improves latency but may lower total throughput through contention.
- **Precision** — approximate algorithms (sketches, sampling, lower-precision numbers) are fast but inexact; acceptable for analytics, rarely for money.
- **Portability** — platform-specific intrinsics, native extensions, or vendor features tie you to an environment.

If the gain is modest and the cost is ongoing complexity, recommend against it, and say why.

## Reporting performance work

A good report lets a reader trust the numbers:

- The target, the baseline, and the result in the same metric and percentile, with the environment and data size.
- What the profile showed (the hot spot and its share of time), so the choice of lever is justified.
- Each change and its measured effect, including changes that were tried and reverted.
- Any trade-offs introduced (memory, staleness, complexity) and how they are bounded.
- What guards against regression, and what was not measured (e.g. "not tested at 10× traffic").

Avoid unqualified claims like "3× faster" from a single run or a micro-benchmark; state the conditions.

## Pitfalls

- **Optimising without profiling** — speeding up code that wasn't the bottleneck.
- **Micro-optimising before fixing algorithms or round trips.**
- **Measuring averages** and missing tail latency; or measuring once and believing noise.
- **Benchmarking toy data** and extrapolating.
- **Caches without invalidation, bounds, or correct keys**, producing stale or leaked data.
- **Parallelising contended work**, making it slower.
- **Sacrificing correctness**: changing ordering, precision, or semantics silently.
- **Obscuring code** for negligible gains, with no comment explaining why.
- **Optimising the wrong environment**: debug builds, local SSDs vs network storage, single-user vs concurrent load.
- **Ignoring cost of the optimisation itself**: memory for caches, operational complexity of new infrastructure, load moved to another system.
- **Declaring victory without a regression guard**, so the gain disappears in a month.

## Verification

- [ ] A target and a baseline measurement exist, recorded before changes.
- [ ] The hot spot was identified by profiling or timing, not assumption.
- [ ] Each change was measured against the baseline with repeated runs; improvements exceed noise.
- [ ] The improvement is reported in the user-visible metric (e.g. end-to-end p95), not only a micro-benchmark.
- [ ] Tests pass and outputs match the previous implementation (or agreed tolerance).
- [ ] Other resources and downstream systems were checked for adverse effects.
- [ ] Caches have bounded size, correct keys, and a defined invalidation/staleness policy.
- [ ] A benchmark, budget, or alert guards against regression.
- [ ] Non-obvious optimisations are commented with the reason and the measurement.
