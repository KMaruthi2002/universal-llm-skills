---
name: system-design
description: >-
  Design distributed systems that meet scale, latency, and reliability goals:
  gather functional and non-functional requirements, estimate capacity, shape
  data flow, and choose caching, queues, replication, partitioning, and
  consistency models while reasoning explicitly about failure modes and
  trade-offs. Use when designing a new service or platform, preparing for
  growth (more users, data, regions), deciding between sync and async
  processing, adding a cache or queue, choosing consistency guarantees,
  writing a design doc, or practising a system-design interview. For code
  structure inside one service use software-architecture; for provider-specific
  infrastructure use cloud-architecture.
metadata:
  category: development
  related: software-architecture, database-design, api-design, cloud-architecture, performance-optimization, observability, concurrency-and-async, technical-decision-making, estimate-effort
---

# System Design

System design is deciding how a system's components, data, and communication are arranged across machines so that it does what it must, as fast as it must, as reliably as it must, at a cost that is acceptable — and keeps doing so as load grows and parts fail.

The craft is not knowing the names of building blocks. It is **turning vague goals into numbers, letting those numbers rule out options, and being explicit about what you give up for what you get.**

## Scope

Covers: requirements and capacity estimation, high-level architecture, data flow, storage choice at the system level, caching, asynchronous processing, replication, partitioning, consistency, availability, failure handling, and design documentation.

Does not cover in depth:
- Internal module structure of one codebase — `software-architecture`.
- Detailed schema and index design — `database-design`.
- Interface contracts — `api-design`.
- Provider-specific services, networking, and cost tooling — `cloud-architecture`.
- Making a specific hot path faster — `performance-optimization`.
- Metrics, logs, traces, alerting — `observability`.

## Core principles

### 1. Requirements before boxes

Drawing components before you know the read/write ratio, the data size, the latency target, and what "available" means is guessing. Most bad designs are correct answers to the wrong question. Spend the first part of any design pinning down requirements, and revisit them when a number surprises you.

### 2. Numbers rule out designs

A back-of-the-envelope estimate is the cheapest design tool there is. "100 writes/s, 1 KB each" fits on one database node for years. "500,000 writes/s" does not, and rules out a single-primary relational store immediately. Estimate first, then choose. Precision does not matter — orders of magnitude do.

### 3. Every choice is a trade-off; name both sides

Caching trades freshness for latency. Replication trades consistency or write latency for availability and read scale. Queues trade immediacy for resilience and smoothing. Partitioning trades query flexibility and operational simplicity for scale. If you cannot name what a component costs, you do not understand it well enough to add it.

### 4. Design for failure as the normal case

At scale, something is always broken: a disk, a node, a network link, a dependency, a deploy. Ask for each component: *what happens when this is slow? when it is down? when it returns garbage? when it comes back and everyone retries at once?* A system's reliability is decided by its failure behaviour, not its happy path.

### 5. Simplest design that meets the requirements, with a path to the next step

A single well-provisioned database with a replica and a cache handles far more than most people assume. Distributed designs bring partial failure, consistency puzzles, and operational load. Choose the least distributed design that meets the numbers with headroom, and know what you would change at 10× load.

### 6. State is the hard part

Stateless compute scales by adding copies behind a load balancer. State — databases, caches, queues, sessions, files — is where scaling, consistency, and recovery get difficult. Push state into a small number of purpose-built stores and keep everything else stateless.

## Discovering context

Before designing, find out what already exists and what the organisation can operate:

- **Existing systems**: what stores, queues, caches, and platforms are already in use? Reusing a well-operated component usually beats introducing a theoretically better one nobody knows how to run.
- **Operational maturity**: is there on-call, observability, automated deploys, infrastructure as code? A design that needs a 24/7 SRE team is wrong for a team of three.
- **Constraints**: cloud or on-prem, regions, data residency and compliance (personal data, payments, health data), budget, required vendors.
- **Existing design docs and decision records**: follow the house format if there is one.
- **Real traffic data**: if the system exists, current metrics beat estimates. Ask for peak QPS, data size, growth rate, and latency percentiles.

## Process

Adapt the depth to the stakes. An interview answer runs through these in under an hour; a production design doc may spend days on steps 1–3.

### Step 1: Functional requirements

List the core operations from the user's perspective, then cut to the few that drive the design. "Users post messages, follow others, read a timeline" — the timeline read is what shapes everything. Explicitly park out-of-scope features so they do not leak in.

### Step 2: Non-functional requirements — make them numbers

| Quality | Turn into |
|---|---|
| Scale | Daily/monthly active users, requests per second (average *and* peak), data volume and growth per year |
| Latency | Target percentiles per operation (e.g. p50 and p99 for read, write) |
| Availability | Target (99.9% ≈ 43 min/month downtime, 99.99% ≈ 4.3 min/month) and which operations it applies to |
| Durability | Can any acknowledged write be lost? How much (RPO)? How fast must service resume (RTO)? |
| Consistency | Must a user see their own write immediately? Must all users see the same value? Where can staleness be tolerated, and for how long? |
| Cost | Budget envelope, or "minimise" |
| Compliance | Residency, retention, deletion, audit requirements |

Push back on "it must never go down and always be consistent". Each extra nine of availability roughly multiplies cost and complexity; ask what the business loses per minute of downtime.

### Step 3: Capacity estimation

Work out, roughly:
- **Request rate**: DAU × actions per user per day ÷ 86,400 ≈ average QPS. Peak is commonly 2–10× average depending on how spiky the traffic is; use a stated assumption.
- **Read/write ratio**: shapes whether to optimise reads (caches, replicas, precomputation) or writes (append-only logs, partitioning, batching).
- **Storage**: writes/day × size × retention × replication factor. Add indexes and overhead (often 1.5–3× raw).
- **Bandwidth**: QPS × payload size, in and out.
- **Working set**: the fraction of data that is hot. Determines cache size.

See `references/estimation-and-numbers.md` for latency reference figures, per-component rough throughput, and a worked estimate.

Then sanity-check: does this fit on one machine? One database? If yes with comfortable headroom, a simple design is likely correct.

### Step 4: API and data model sketch

Define the main operations as interfaces (see `api-design`) and the main entities and their access patterns (see `database-design`). Access patterns — "fetch the 50 newest items for user X", "count events per minute per tenant" — decide storage and partitioning far more than the entity diagram does.

### Step 5: High-level architecture

Draw the request paths for the critical operations: client → edge (CDN, load balancer, gateway) → services → stores, plus any asynchronous paths (queues, workers, streams). Keep it to the components the requirements need.

### Step 6: Deep-dive on the bottlenecks

Pick the two or three hardest parts — usually the hottest read path, the highest write path, and the strictest consistency requirement — and design them in detail: data layout, partitioning key, caching strategy, failure behaviour.

### Step 7: Failure modes and operations

Walk each component through its failure cases (see the failure section below). Define how the system degrades, how it is monitored, how it is deployed without downtime, and how data is backed up and restored.

### Step 8: Trade-offs, alternatives, evolution

Record the alternatives you rejected and why, what assumptions the design rests on, and what you would change at 10× scale. That is what makes the design reviewable and maintainable.

## Building blocks and when to use them

### Load balancing and stateless services

Put stateless service instances behind a load balancer; scale by adding instances. Keep sessions out of process memory (in a store, or in signed tokens) so any instance can serve any request. Layer 4 balancers are faster and protocol-agnostic; layer 7 can route by path or header, terminate TLS, and do retries. Health checks must reflect the ability to serve, not just "process is alive" — but a health check that fails when a shared dependency is down can remove every instance at once; make dependency failures degrade rather than de-register.

### Caching

| Pattern | How | Fits | Watch out |
|---|---|---|---|
| Cache-aside (lazy) | App reads cache; on miss reads store and populates cache | General-purpose read caching | Stale data after writes unless invalidated; stampede on popular misses |
| Read-through | Cache layer fetches from store on miss | Same, centralised logic | Cache becomes a critical dependency |
| Write-through | Writes go to cache and store synchronously | Read-after-write freshness | Slower writes; caches data that may never be read |
| Write-behind | Writes go to cache, flushed to store later | Very high write rates, tolerable loss | Data loss on cache failure; complex |
| CDN / edge | Cache responses near users | Static assets, public or per-segment content | Invalidation latency; never cache personalised responses publicly |

Decisions to make for any cache:
- **What is the key**, and does it include everything the value depends on (user, locale, version, permissions)? A key missing a dimension serves one user's data to another — a security bug, not just a staleness bug.
- **TTL vs. explicit invalidation.** TTLs are simple and bound staleness. Explicit invalidation is fresher but every write path must remember to do it. Many systems use both: invalidate on write, TTL as a safety net.
- **Stampede protection**: when a hot key expires, thousands of requests miss at once. Use request coalescing (one fetch per key), jittered TTLs, or serving stale while refreshing.
- **Cold start**: after a cache flush or restart, can the backing store survive the full load? If not, the cache is not an optimisation, it is load-bearing, and its failure is an outage.
- **Hit rate** needs to be measured; a cache with a low hit rate is pure cost and complexity.

There are only a few hard problems, and cache invalidation is one because every write path and every derived value must be accounted for. Prefer caching data that is naturally immutable or versioned (content-addressed assets, `entity:id:version` keys) where possible.

### Asynchronous processing: queues, logs, and streams

Use asynchronous processing when work does not need to complete before responding, when you need to absorb bursts, or when you need to decouple producers from consumers' availability.

| | Work queue (e.g. a message broker with acknowledgements) | Log / stream (e.g. a partitioned append-only log) |
|---|---|---|
| Model | Each message processed by one consumer, then removed | Messages retained; many consumer groups read independently at their own offsets |
| Ordering | Usually none, or per-group with limits | Ordered within a partition |
| Replay | Typically no | Yes, within retention |
| Fits | Background jobs, task distribution | Event pipelines, change data capture, multiple downstream consumers, audit |

Key properties to design for:
- **Delivery semantics**: assume **at-least-once**. Exactly-once delivery end-to-end is rarely achievable in practice; what you can achieve is exactly-once *effect*, by making consumers idempotent (dedupe by message ID, conditional writes, upserts).
- **Ordering**: if order matters, partition by the entity whose events must be ordered (e.g. account ID), and accept that throughput per entity is then bounded by one consumer.
- **Poison messages**: a message that always fails will block or loop forever. Cap retries with backoff and move failures to a dead-letter queue that someone monitors.
- **Backpressure**: if producers outpace consumers, queue depth grows without bound. Monitor queue age (oldest message), not just length; autoscale consumers or shed load at the producer.
- **Dual writes**: writing to a database and publishing a message as two separate steps will eventually do one without the other. Use a transactional outbox (write the event to a table in the same transaction; a relay publishes it) or change data capture.

### Replication

- **Single-leader**: all writes to one primary, replicated to followers. Simple, strong consistency on the leader. Reads from followers may be stale (replication lag). Failover must avoid two leaders (split brain).
- **Multi-leader**: writes accepted in several places (e.g. per region). Lower write latency across regions, but concurrent conflicting writes must be resolved — last-writer-wins silently loses data; application-level merge or conflict-free data types are safer.
- **Leaderless / quorum**: writes and reads go to several replicas; with N replicas, W write acks and R read acks, R + W > N gives overlap so reads see the latest acknowledged write in the absence of failures and concurrency edge cases. Tunable, but subtle.

Synchronous replication protects against data loss at the cost of write latency and availability (a slow replica slows writes). Asynchronous replication is faster but loses the unreplicated tail on leader failure. Many systems use one synchronous replica and the rest async.

### Partitioning (sharding)

Partition when one node cannot hold the data or handle the write rate. Choosing the key is the decision that matters:

- **Hash partitioning** spreads load evenly but destroys range queries across keys.
- **Range partitioning** keeps ranges together (good for time or alphabetical scans) but concentrates load on hot ranges — e.g. "now" in time-keyed data.
- **Choose a key that matches the dominant access pattern** so most queries hit one partition. Queries that must scatter to all partitions get slower and less available as partition count grows.
- **Hot keys**: a celebrity user or a viral item can overload one partition regardless of scheme. Mitigate with key salting (spread one logical key over several physical ones and merge on read), dedicated handling, or caching.
- **Rebalancing**: use many more logical partitions than nodes (or consistent hashing) so adding nodes moves a fraction of data, not all of it.
- **Cross-partition operations** (transactions, joins, unique constraints across keys) become expensive or impossible. Design the data so invariants live within a partition when you can.

### Consistency models

From strongest to weakest, roughly:
- **Linearizable**: every operation appears to happen at one instant; everyone sees the latest value. Needed for locks, leader election, uniqueness, balances that must not go negative. Costly across regions.
- **Serializable transactions**: transactions behave as if run one at a time. The strongest isolation for multi-item operations.
- **Causal**: if A caused B, everyone sees A before B. Often enough for social and collaboration features.
- **Read-your-writes / session**: a user sees their own changes immediately. Often the guarantee users actually notice. Achievable by routing a user's reads to the leader for a short time after a write, or by tracking version tokens.
- **Eventual**: replicas converge if writes stop. Fine for counters, feeds, analytics, search indexes.

Decide consistency **per operation**, not per system. A shop needs strong consistency for stock reservation and payment, read-your-writes for the cart, and eventual consistency for product reviews and recommendations.

CAP in practice: during a network partition you choose between rejecting some requests (consistency) and serving possibly stale or conflicting data (availability). PACELC adds the everyday trade-off: even without partitions, stronger consistency costs latency. Use these as reminders to ask the question, not as labels for products.

### Coordination

Avoid distributed locks and consensus where you can; they are subtle and slow. When needed (leader election, unique sequence allocation, distributed cron), use a proven consensus-backed system rather than building your own, and use **fencing tokens** so a process that paused and lost its lease cannot still write.

## Failure modes and resilience

Walk every dependency through these questions:

| Failure | Defence |
|---|---|
| Dependency slow | Timeouts on every network call, set from the latency budget, not defaults. A missing timeout turns one slow dependency into exhausted threads everywhere |
| Dependency down | Fallbacks (cached or default responses), graceful degradation (hide the recommendations panel, keep checkout working), circuit breakers that fail fast |
| Transient errors | Retries with exponential backoff and jitter, capped in count, **only for idempotent operations** or with idempotency keys |
| Retry storms | Retry budgets (e.g. retries ≤ 10% of requests), retry at one layer only — retries at every layer multiply (3 layers × 3 retries = 27× load) |
| Overload | Load shedding (reject early with 429/503), rate limiting per client, bounded queues, priority for critical traffic |
| Thundering herd after recovery | Jittered reconnects, gradual traffic ramp, cache warming |
| Node / zone failure | Redundancy across failure domains; capacity to lose one zone (N+1 or N+2) |
| Region failure | Multi-region only if the availability target demands it; decide active-active vs. active-passive and test failover regularly |
| Data corruption / bad deploy | Backups with tested restores, point-in-time recovery, gradual rollouts, fast rollback |
| Clock skew | Do not order events across machines by wall-clock time; use logical versions or a single sequencer where order matters |
| Split brain | Consensus-based leadership, fencing tokens, quorum |

Two rules that prevent many outages:
- **Bound everything**: queue sizes, connection pools, retries, timeouts, payload sizes, result set sizes. Unbounded resources are how small problems become total failures.
- **Avoid cascading failure**: a failure in a non-critical dependency must not take down a critical path. Isolate pools (bulkheads) so the slow recommendations service cannot consume the threads checkout needs.

Availability composes: a request that depends serially on five services each at 99.9% is at most about 99.5% available. Reduce serial hard dependencies on critical paths, or make them soft (degrade when unavailable).

## Decision guidance

### Sync request vs. async job

Choose **synchronous** when the user needs the result to continue and it completes within the latency budget. Choose **asynchronous** (accept, return a job ID or 202, process in background, notify or let the client poll) when the work is slow (seconds or more), bursty, can be retried, or depends on unreliable third parties.

### Precompute vs. compute on read

Precompute (fan-out on write, materialised views, rollups) when reads vastly outnumber writes and the read latency target is tight. Compute on read when writes are frequent, the read is rare, or the precomputed set would be enormous. Hybrids are common: precompute for most users, compute on read for pathological cases (e.g. accounts with millions of followers).

### One region vs. multi-region

Multi-region adds major complexity: data replication across high-latency links, conflict handling or leader placement, and failover testing. Choose it when the availability target exceeds what one region can offer, when users are global and latency matters, or when residency law requires it. Otherwise, use multiple zones in one region and good backups.

### Build vs. use a managed service

Managed services trade cost and some control for not operating the thing yourself. For small teams, operating your own distributed database, queue, or search cluster is usually a poor use of time. See `cloud-architecture` and `technical-decision-making`.

## Worked reasoning example

*Illustrative.* Design a URL shortener: 100 M new links per month, 10:1 read/write, links kept 5 years, redirect latency p99 < 50 ms.

- Writes: 100 M / (30 × 86,400) ≈ 40/s average; assume 5× peak ≈ 200/s. Reads ≈ 400/s average, ~2,000/s peak.
- Storage: 100 M × 12 months × 5 years = 6 B links × ~500 B ≈ 3 TB raw; with replication and indexes, ~10 TB. Too much for comfortable single-node in-memory, fine for a partitioned key-value store or a sharded relational store.
- Access pattern: lookup by short code only → key-value access, hash-partition by code, no cross-key queries.
- Read path: the link → URL mapping is immutable once created, so it caches perfectly. A cache holding the hot fraction (say, 20% of recent links) absorbs most reads, which keeps p99 well under 50 ms.
- ID generation: random codes need a uniqueness check (conditional insert); counter-based codes need a coordinated sequence (allocate ranges per instance to avoid a hot coordinator). Random with conditional insert is simpler; collision probability is negligible with enough characters (7 base-62 characters ≈ 3.5 trillion codes).
- Analytics (click counts) are eventually consistent: emit click events to a log, aggregate asynchronously — never update a counter row synchronously on the redirect path.
- Failure: if the store is down, cached hot links still redirect; new link creation fails cleanly.

The numbers drove every choice: the write rate is tiny, so the challenge is storage size and read latency, not write throughput.

## Pitfalls and anti-patterns

- **Skipping estimation** and designing for an imagined scale, usually far too large (complexity with no benefit) or occasionally far too small.
- **Distributed by default**: microservices, multiple data stores, and event streams for a system one database would serve. Every network hop is latency and a failure point.
- **Ignoring the p99**: averages hide the tail. With fan-out to many backends, the slowest one sets the response time; tail latency compounds.
- **Caching without an invalidation story** or without measuring hit rate.
- **Assuming exactly-once delivery** and writing non-idempotent consumers.
- **Dual writes** to a database and a queue or a second store without an outbox or CDC.
- **Retries without backoff, jitter, or budgets**, especially for non-idempotent operations.
- **No timeouts**, or timeouts longer than the caller's own timeout, so work continues after nobody is waiting.
- **Hot partitions** from a key that concentrates load (timestamp, popular tenant).
- **Strong consistency everywhere** "to be safe", paying latency and availability where users would never notice staleness — or the reverse, eventual consistency on money and inventory.
- **Untested failover and backups.** A backup that has never been restored is a hope, not a backup.
- **Single points of failure hidden in "shared" infrastructure**: one DNS provider, one secrets store, one config service every request reads synchronously.

## Safety

- Designs that handle personal, financial, or health data must address encryption in transit and at rest, access control, retention and deletion, and residency. Flag these explicitly if requirements do not mention them.
- Do not recommend load tests, failover drills, or chaos experiments against production without the owners' explicit agreement and a rollback plan.
- When proposing changes to an existing production system, include the migration and rollback path; a design that cannot be reached safely from the current state is incomplete.

## Quality bar and verification

A design is ready for review when:

- [ ] Functional scope is explicit, including what is out of scope.
- [ ] Non-functional requirements are numbers, with stated assumptions where numbers were not available.
- [ ] Capacity estimates exist and each major component choice is consistent with them (re-check the arithmetic; unit errors of 1,000× are common).
- [ ] Critical read and write paths are traced end to end, with a latency budget that adds up.
- [ ] Consistency requirements are stated per operation, and the design meets each.
- [ ] Every network call has a timeout, a retry policy (or a reason for none), and defined failure behaviour.
- [ ] Every asynchronous consumer is idempotent, and poison messages have somewhere to go.
- [ ] Single points of failure are listed and either removed or accepted with reasons.
- [ ] Backup, restore, deploy, and rollback are addressed.
- [ ] Alternatives considered and rejected are recorded with reasons.
- [ ] The design states what changes at 10× load.
- [ ] It fits the team's ability to operate it.

Where possible, validate assumptions empirically: load-test the risky component in a non-production environment, measure a prototype's latency, or check real traffic metrics. State which numbers were measured and which were estimated.

## Depth on demand

- `references/estimation-and-numbers.md` — latency and throughput reference figures, availability arithmetic, and a step-by-step capacity estimate. Read when doing step 3, or whenever a design's feasibility hinges on a number.
