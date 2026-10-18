---
name: concurrency-and-async
description: >-
  Write and debug correct concurrent and asynchronous code: choosing between
  threads, processes, async/await and event loops, actors, and worker pools;
  avoiding data races, race conditions, deadlocks, livelocks and starvation;
  managing shared state with locks, atomics, immutability or message passing;
  structured concurrency, cancellation and timeouts; backpressure and bounded
  queues; and testing concurrent code. Use when code runs in parallel or
  asynchronously, when adding async/await, threads, goroutines, workers or
  background jobs, when results are nondeterministic, something hangs or
  deadlocks, an event loop is blocked, or throughput under load is poor. For
  distributed-system consistency use system-design; for job scheduling use
  scheduled-jobs.
metadata:
  category: development
  related: debugging, performance-optimization, error-handling, testing-strategy, backend-development, system-design, scheduled-jobs, database-design
---

# Concurrency and Async

Concurrency is about structuring a program as multiple tasks whose execution can overlap; parallelism is about actually running them at the same time. Async is a way of expressing concurrency in which tasks voluntarily yield while waiting. All three trade simplicity for throughput or responsiveness, and all three introduce a class of bugs — races, deadlocks, lost updates, leaks of unfinished work — that are rare, timing-dependent, and hard to reproduce. The craft is choosing the simplest model that meets the need and confining shared mutable state so the hard bugs cannot occur.

## Scope

Covers: in-process concurrency models, synchronisation, shared state, cancellation, backpressure, async runtimes, and how to test and debug concurrent code, across languages.

Neighbours:

- Consistency across machines, distributed locks, consensus, replication → `system-design`.
- Database transaction isolation and locking → `database-design`, `sql-and-queries`.
- Making work faster in general → `performance-optimization`.
- Retries, timeouts, and failure semantics → `error-handling`.
- Cron-like and queued background work → `scheduled-jobs`.

## Core principles

1. **Shared mutable state is the root of most concurrency bugs.** A race requires two tasks touching the same data, at least one writing, without coordination. Remove any one of those three conditions — don't share, don't mutate, or coordinate — and the bug class disappears. Prefer the first two; coordination is the hardest to get right.

2. **Choose the model by the bottleneck.** I/O-bound work (waiting on network, disk, databases) benefits from concurrency — async or many threads — because tasks mostly wait. CPU-bound work benefits only from parallelism across cores — threads (in runtimes that allow true parallel execution), processes, or native code. Async does nothing for CPU-bound work and can make it worse by blocking the event loop.

3. **Every task needs an owner and a lifetime.** A task started without anyone waiting for it, cancelling it, or collecting its errors is a leak: its failures vanish and it may outlive the request that started it. Structured concurrency — tasks scoped to a block that waits for all of them — makes lifetimes explicit.

4. **Bound everything.** Unbounded queues, unbounded task spawning, and unbounded pools turn overload into memory exhaustion or latency collapse. Bounds create backpressure, which is how a system says "slow down" instead of falling over.

5. **Correctness can't be established by testing alone.** Interleavings are combinatorially many; a test passing 1,000 times proves little. Reason about invariants, use designs that make races impossible, and use tools (race detectors, model checkers, deterministic schedulers) that explore interleavings systematically.

6. **Simpler beats faster.** Fine-grained locking, lock-free structures, and clever memory-ordering tricks are expert territory. Use them only when profiling shows coarse synchronisation is the bottleneck — and prefer battle-tested library implementations to your own.

## Concurrency models

| Model | How it works | Good for | Watch out for |
|---|---|---|---|
| **OS threads + shared memory** | Preemptively scheduled threads share an address space | CPU parallelism (where runtime permits); blocking libraries | Races, deadlocks; ~MBs of stack per thread; thousands of threads get expensive |
| **Thread / worker pools** | Fixed set of threads consuming tasks from a queue | Bounded parallelism; reuse | Pool starvation when tasks block waiting on other tasks in the same pool |
| **Processes** | Separate address spaces; communicate via IPC | CPU parallelism in runtimes with a global interpreter lock; isolation of crashes | Startup cost; serialisation overhead; memory duplication |
| **Async / await on an event loop** | Cooperative tasks yield at `await`; one (or few) threads run many tasks | Very high numbers of concurrent I/O-bound operations | Any blocking call stalls everything; "function colouring" (async spreads through call chains) |
| **Green threads / goroutines / virtual threads** | Runtime-scheduled lightweight threads; blocking-style code | Massive I/O concurrency with simple sequential code | Still shared memory — races remain; pinning or blocking native calls can starve the scheduler |
| **Actors** | Isolated state per actor; communicate only by asynchronous messages | Stateful concurrent entities; fault isolation and supervision | Mailbox growth (needs backpressure); request–response via messages adds complexity; ordering assumptions |
| **CSP / channels** | Tasks communicate over channels; "share memory by communicating" | Pipelines, fan-out/fan-in, worker coordination | Deadlocks from unbuffered channels with no reader; goroutine leaks on abandoned channels |
| **Data parallelism** | Same operation over partitions of data (parallel map, SIMD, GPU) | Numeric and bulk data processing | Partitioning overhead; reduction correctness |

Examples by ecosystem (not mandates): Python — `asyncio`/`trio`/`anyio`, `threading` (I/O-bound), `multiprocessing`/`concurrent.futures` (CPU-bound); JavaScript — the event loop, Promises, `worker_threads`/Web Workers for CPU; Go — goroutines, channels, `sync`, `context`; Java/Kotlin — executors, virtual threads, `CompletableFuture`, coroutines; C# — `async`/`await`, `Task`, TPL; Rust — threads with `Send`/`Sync`, `tokio`/`async-std`, `rayon` for data parallelism; Erlang/Elixir — processes and supervision trees.

### Choosing

- **Mostly waiting on I/O, many concurrent operations** → async or lightweight threads, whichever the codebase uses.
- **CPU-heavy work that can be split** → a pool sized to core count (threads or processes depending on runtime); keep it off the event loop.
- **A few independent background activities** → plain threads or tasks with clear ownership.
- **Many stateful entities processing events** (sessions, devices, game objects) → actors or one task per entity with a mailbox.
- **Streaming pipelines** → channels/queues with bounded buffers between stages.
- **Simple scripts** → sequential code; add concurrency only when measurements show waiting dominates.

Mixing models (e.g. calling blocking code from async, or async from threads) is common and is where many bugs arise. Use the runtime's bridges deliberately: run blocking work in a thread pool from async (`run_in_executor`, `spawn_blocking`, `Task.Run`), and run async code from sync contexts through a single entry point rather than nested event loops.

## Hazards and how to recognise them

**Data race**: unsynchronised concurrent access to the same memory with at least one write. In some languages (C, C++, Go, Rust-unsafe) this is undefined or unspecified behaviour; in managed languages it produces torn reads, lost updates, or stale values. Detect with race detectors (e.g. Go `-race`, ThreadSanitizer for C/C++/Rust, Java tools) running your tests.

**Race condition (higher-level)**: correctness depends on timing even when each access is individually synchronised. The classic is **check-then-act**:

```
if not exists(key):        # two tasks both see "not exists"
    create(key)            # both create → duplicate
```

and **read-modify-write**:

```
balance = get_balance()    # both read 100
set_balance(balance - 10)  # both write 90; one withdrawal lost
```

Fixes: make the compound operation atomic (a lock around both steps, an atomic primitive like compare-and-swap or `fetch_add`, a database constraint or conditional update such as `UPDATE ... SET balance = balance - 10 WHERE balance >= 10`, an upsert, or optimistic concurrency with version numbers). Note that in async code, races occur across `await` points: state read before an `await` may have changed after it, even on a single thread.

**Deadlock**: tasks each hold a resource and wait for another's. Requires (Coffman conditions) mutual exclusion, hold-and-wait, no preemption, and circular wait. Prevent by breaking one:

- **Global lock ordering**: always acquire locks in a consistent order (e.g. by account ID).
- **Don't hold a lock while calling unknown code** (callbacks, virtual methods, I/O, other services).
- **Acquire with timeouts** (try-lock) and back off.
- **Use one coarser lock** instead of several fine ones.
- **Async variants**: awaiting a task that awaits you; a bounded channel where the producer waits for space while the consumer waits for the producer; synchronously blocking on an async result inside the event loop (`.Result`, `block_on` in an async context).

**Livelock**: tasks keep responding to each other without progress (both back off and retry in lockstep). Fix with randomised backoff.

**Starvation**: a task never gets the resource — unfair locks, priority inversions, a reader-preferring lock with constant readers, a pool full of tasks waiting on tasks queued behind them.

**Blocked event loop**: a synchronous CPU-heavy or blocking call (file I/O, `sleep`, a sync HTTP client, a heavy JSON parse, a tight loop) inside async code stalls every other task. Symptoms: latency spikes across unrelated requests, timeouts, health checks failing. Many runtimes offer slow-callback or blocked-loop detection in debug mode.

**Lost or leaked tasks**: fire-and-forget tasks whose exceptions are never observed, that keep running after their parent returned, or whose results are discarded. Often visible as "Task exception was never retrieved" warnings, growing goroutine counts, or memory growth.

**Memory visibility and ordering**: without synchronisation, one thread may not see another's writes, or may see them in a different order. Locks, atomics, volatile/acquire-release semantics, and channels establish "happens-before" relations. Double-checked locking without proper memory ordering is a classic bug. When in doubt, use higher-level primitives that handle this for you.

## Managing shared state

In order of preference:

1. **Don't share.** Give each task its own data; partition work so tasks touch disjoint data; combine results at the end (map-reduce).
2. **Share only immutable data.** Immutable values can be read concurrently with no synchronisation. Copy-on-write and persistent data structures make "modification" produce new versions.
3. **Transfer ownership via messages.** Send data through a channel or to an actor; the sender stops using it. Only one task owns it at a time. Rust's ownership system enforces this; elsewhere it's a discipline.
4. **Confine state to one task.** One task owns the state; others ask it to act via messages (the actor pattern, or a single "owner" goroutine/task).
5. **Use concurrent data structures and atomics** from the standard library for simple shared counters, maps, and queues — but remember a concurrent map makes individual operations safe, not compound check-then-act sequences.
6. **Use locks.** Keep critical sections small, never do I/O or call unknown code inside them, always release (use scoped constructs: `with lock:`, `defer mu.Unlock()`, RAII guards, `lock` statements), and document which lock guards which data. Readers–writer locks help only when reads dominate and critical sections are non-trivial; measure.

**Locks vs message passing.** Message passing scales better in reasoning: each piece of state has one owner, and interactions are explicit. Locks are simpler for small, local shared structures and have less overhead. A common good design: message passing between components, small locks inside a component.

**Database as the shared state.** Many "concurrency" bugs in web services are races on database rows across requests or instances. In-process locks don't help across instances. Use transactions with the right isolation level, row locks (`SELECT ... FOR UPDATE`), conditional updates, unique constraints, or optimistic concurrency (version columns). See `database-design`.

## Structured concurrency and cancellation

**Structured concurrency**: child tasks are started within a scope that does not exit until all children finish; if one fails, the others are cancelled and the error propagates. Examples: Python `asyncio.TaskGroup`/trio nurseries, Kotlin `coroutineScope`, Swift task groups, Java structured task scopes, Go `errgroup` with `context`. Benefits: no leaked tasks, errors are never lost, cancellation propagates naturally. Prefer it over ad-hoc spawning.

**Cancellation** must be designed in:

- **Propagate a cancellation signal** through call chains (context objects, cancellation tokens, abort signals, scope cancellation). Accept it in every long-running or blocking function.
- **Check it at safe points**: between iterations, before expensive steps, at every await (where the runtime does this automatically).
- **Clean up on cancellation**: release locks, close connections, roll back partial work. In runtimes where cancellation is delivered as an exception (e.g. `CancelledError`), don't swallow it — catch-all handlers that suppress cancellation break shutdown and timeouts.
- **Make cancellation safe for state**: an operation cancelled midway must not leave shared state inconsistent. Group mutations so that cancellation points don't fall in the middle of an invariant-breaking sequence.
- **Timeouts are cancellation on a clock.** Every wait on another task, queue, lock, or I/O should have a timeout or be under a cancellable scope with a deadline (see `error-handling`).
- **Graceful shutdown**: on termination signals, stop accepting new work, cancel or finish in-flight work within a deadline, flush buffers, then exit.

## Backpressure and flow control

When producers outpace consumers, something must give. The options are to **buffer** (bounded — otherwise memory grows until crash), **block or slow the producer** (backpressure), **drop** (newest, oldest, or sampled — acceptable for metrics, not for orders), or **scale consumers** (if the bottleneck parallelises).

- **Use bounded queues and channels.** Choose the bound from latency tolerance: a queue of 10,000 items processed at 100/s means a 100 s delay for the last item — often worse than rejecting.
- **Limit concurrency explicitly**: semaphores around outbound calls, a fixed worker count, connection pool limits. Spawning one task per incoming item without a limit is a common way to overwhelm a downstream service or exhaust file descriptors.
- **Propagate pressure upstream**: when the internal queue is full, return 429/503 to clients, pause consuming from the message broker, or stop reading from the socket — rather than accepting work you cannot do.
- **Streams and reactive pipelines** usually have built-in demand signalling; respect it rather than collecting everything into memory.
- **Measure queue depth and wait time**; they are the earliest signal of overload.

## Async-specific guidance

- **Never block the loop.** Use async versions of I/O libraries; move CPU-bound or blocking calls to a thread or process pool. Even logging to a slow sink can block.
- **Await everything you start**, or hand it to a scope/group that will. Keep references to background tasks so they are not garbage-collected mid-flight (a real issue in some runtimes).
- **Concurrency is not automatic**: `await a(); await b()` runs sequentially. For independent operations, start both and await together (`gather`, `Promise.all`/`allSettled`, `WhenAll`, `join!`) — with a concurrency limit if there are many.
- **Choose the right combinator for failures**: "fail fast and cancel the rest" vs "wait for all and collect results and errors". `Promise.all` rejects on the first error but does not cancel the others; know your runtime's semantics.
- **Re-check state after await.** Anything read before an `await` may be stale after it.
- **Avoid sync-over-async and async-over-sync** wrappers inside libraries; they cause deadlocks (synchronisation-context deadlocks in some UI frameworks) and thread-pool starvation.
- **Mind per-task context**: request-scoped values must use the runtime's context mechanism (context variables, async-local storage), not globals or thread-locals that tasks share.

## Process: adding or reviewing concurrency

1. **Justify it.** What is the bottleneck — waiting or computing? Measure (see `performance-optimization`). If sequential code meets the need, stop.
2. **Pick the model** that the codebase already uses, unless it fits poorly; mixing models needs strong reasons.
3. **Map the shared state.** List every piece of data accessed by more than one task, who reads and writes it, and how access is coordinated. If you can't fill this in, you aren't ready to write the code.
4. **Define lifetimes and ownership** of every task: who starts it, who waits for it, who cancels it, where its errors go.
5. **Set bounds**: concurrency limits, queue sizes, timeouts, retry budgets.
6. **Design failure and cancellation behaviour**: what happens when one of N tasks fails? On shutdown? On timeout?
7. **Implement with the highest-level primitives available** — task groups, executors, channels, concurrent collections — before hand-rolled locks and condition variables.
8. **Test** (next section), including with race detection and under load.
9. **Document** concurrency invariants in code: which lock guards which field, which methods must be called from which context, thread-safety guarantees of public types.

## Testing and debugging concurrent code

- **Run tests with a race detector** where available, in CI. It finds real data races with low false-positive rates, but only on paths the tests execute.
- **Stress tests**: run the operation thousands of times with many concurrent tasks, assert invariants afterwards (total balance conserved, no duplicates, counts match). Run on machines with different core counts; add randomised delays at suspicious points to widen race windows.
- **Deterministic testing**: inject the scheduler, clock, and executor so tests control ordering. Fake timers let you advance time instantly. Some ecosystems have tools that systematically explore interleavings (e.g. `loom` for Rust, deterministic simulation frameworks, model checkers such as TLA+ for designs).
- **Test cancellation and timeouts explicitly**: cancel mid-operation and assert resources were released and state is consistent.
- **Test shutdown**: start work, signal shutdown, assert it completes within the deadline and nothing is lost that shouldn't be.
- **Avoid sleeps in tests** to "wait for" concurrent work; wait on explicit signals (futures, latches, events, polling with a timeout).
- **Hangs**: take a thread dump / goroutine dump / async task dump of the stuck process. It shows exactly what every task is waiting on; deadlocks appear as cycles. For async, enable the runtime's debug mode to list pending tasks and slow callbacks.
- **Heisenbugs**: logging changes timing. Log to in-memory buffers, record traces with timestamps and task IDs, or use record-replay debugging. See `debugging` for intermittent-failure method and the statistics of "fixed".

## Sizing pools and limits

- **Little's law**: concurrency in the system = arrival rate × time in system. If a downstream call takes 200 ms and you need 500 calls/s, you need about 100 concurrent calls in flight. Use this to size connection pools, worker counts, and semaphores, then validate with load tests.
- **CPU-bound pools**: about one worker per core; more adds context switching without throughput. Leave headroom for the rest of the process.
- **I/O-bound pools**: can be much larger than core count, but are bounded by what the downstream can handle (database connection limits, rate limits) — the downstream's capacity, not your machine's, is usually the real limit.
- **Database connection pools**: the sum across all instances must stay below the database's connection limit, with room for administration and migrations. More connections than the database has cores often *reduces* throughput.
- **Separate pools for separate workloads** (bulkheads): a pool shared by fast and slow work lets the slow work starve the fast.
- **Never block a pool's thread waiting for work submitted to the same pool**; with all threads waiting, nothing runs (pool-induced deadlock).

## Common recipes (illustrative)

Bounded concurrent fan-out with structured lifetimes and fail-fast cancellation:

```python
# Python asyncio (3.11+)
sem = asyncio.Semaphore(10)

async def fetch_one(url):
    async with sem:
        async with asyncio.timeout(5):
            return await client.get(url)

async with asyncio.TaskGroup() as tg:          # waits for all; cancels siblings on error
    tasks = [tg.create_task(fetch_one(u)) for u in urls]
results = [t.result() for t in tasks]
```

```go
// Go: errgroup with a context and a concurrency limit
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10)
results := make([]Result, len(urls))
for i, u := range urls {
    i, u := i, u
    g.Go(func() error {
        r, err := fetch(ctx, u) // fetch honours ctx cancellation and deadline
        if err != nil { return err }
        results[i] = r          // each goroutine writes its own index: no shared write
        return nil
    })
}
if err := g.Wait(); err != nil { return err }
```

```typescript
// JavaScript/TypeScript: limit concurrency without a library
async function mapLimit<T, R>(items: T[], limit: number, fn: (t: T) => Promise<R>): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;            // safe: single-threaded between awaits
      results[i] = await fn(items[i]);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```

Fixing a lost update without in-process locks (works across instances):

```sql
-- atomic conditional update; check affected row count
UPDATE accounts SET balance = balance - :amount
WHERE id = :id AND balance >= :amount;

-- or optimistic concurrency with a version column
UPDATE documents SET body = :body, version = version + 1
WHERE id = :id AND version = :expected_version;   -- 0 rows → conflict; reload and retry or report
```

Single owner of state (actor style, pseudocode):

```
loop:
    msg = inbox.receive()          # bounded inbox
    match msg:
        Deposit(amount)            -> balance += amount
        Withdraw(amount, reply)    -> if balance >= amount: balance -= amount; reply.send(ok)
                                      else: reply.send(insufficient)
        Shutdown                   -> break
```

No locks are needed because only this loop touches `balance`; every compound operation is naturally atomic.

## A worked example (illustrative)

Symptom: "Under load, some users receive two welcome emails; also occasionally none."

1. *Map the shared state.* A `users.welcome_sent` flag. Handler: read user → if not sent, send email → set flag. Runs in a worker pool across three instances.
2. *Duplicates*: check-then-act race across instances — two workers both see `false`. A process-local lock can't fix it (three instances).
3. *None sent*: the email call runs as a fire-and-forget task; when it fails, the exception is unobserved, but the flag was already set by the time the failure happens.
4. *Fix*: claim atomically in the database (`UPDATE users SET welcome_state='sending' WHERE id=? AND welcome_state='pending'`; proceed only if one row changed); send the email awaited, with a timeout; on success set `sent`; on failure revert to `pending` for a bounded retry with backoff, or move to `failed` and alert after the limit.
5. *Verify*: a stress test runs 50 concurrent handlers for the same user against a real database and asserts exactly one send; a fault-injection test makes the email client fail and asserts the state returns to `pending` and the error is logged.

## Discovering context

- **Identify the runtime and concurrency model** in use: web framework's request model (thread per request, async, worker processes), background job system, async library, executor configuration.
- **Find existing primitives and conventions**: shared executors, semaphore helpers, task-group utilities, cancellation/context passing style, lock naming and documentation, thread-safety annotations.
- **Check deployment topology**: how many instances, processes, and threads run — an in-process lock or cache is per-process, and a fix that works locally may fail with several replicas.
- **Check library thread-safety**: database clients, HTTP clients, and SDKs vary in whether instances may be shared across threads or tasks.
- **Follow the project's patterns** for spawning and awaiting work; flag risky existing patterns (unbounded spawning, missing timeouts, blocking in async) to the user.

## Pitfalls

- Using async for CPU-bound work, or blocking calls inside async code.
- Check-then-act and read-modify-write without atomicity, including across `await` points and across service instances.
- Locks held during I/O or callbacks; inconsistent lock ordering.
- Fire-and-forget tasks with unobserved errors and unbounded lifetimes.
- Unbounded queues, task spawning, or parallel fan-out against downstream services.
- Swallowing cancellation exceptions in catch-all handlers.
- Assuming a thread-safe collection makes compound operations safe.
- Sharing non-thread-safe clients or objects across threads.
- Sleeps as synchronisation, in code or tests.
- In-process locks used to protect cross-instance resources (use the database or a proper distributed mechanism — see `system-design`).
- Adding parallelism that increases contention and makes things slower; not measuring.
- Declaring a race fixed because a stress test passed a few times.

## Verification

- [ ] The reason for concurrency is stated and backed by measurement or a clear I/O-bound workload.
- [ ] All shared mutable state is identified, and each piece has a documented coordination strategy (or was eliminated).
- [ ] Compound operations on shared state are atomic at the right level (in-process, database, or distributed).
- [ ] Every spawned task has an owner that awaits it or a scope that bounds it; errors are propagated or logged.
- [ ] Concurrency limits, queue bounds, and timeouts are set and justified.
- [ ] Cancellation and shutdown are handled and tested; resources are released and state stays consistent.
- [ ] No blocking calls run on an event loop; CPU-heavy work is offloaded.
- [ ] Tests pass under a race detector (where available) and under stress with invariant checks; no sleeps used for synchronisation.
- [ ] Behaviour is correct with multiple instances/processes if the deployment runs them.
