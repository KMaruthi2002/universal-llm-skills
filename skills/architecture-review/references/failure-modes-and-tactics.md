# Failure Modes and Tactics for Architecture Review

A catalogue for reviewing designs with multiple services, queues, caches, data stores or regions. For each failure mode: what it looks like, the question that exposes whether the design has considered it, and the usual mitigations. Mitigations have their own costs; a design does not need all of them, only those its requirements justify.

## Dependency failures

### Slow dependency (worse than a dead one)

- **What happens**: a downstream service responds slowly; callers hold threads, connections or memory waiting; pools exhaust; the caller becomes slow or fails too. A slow dependency often causes a wider outage than one that fails fast.
- **Question**: "What is the timeout on each outbound call, and what happens to the caller's resources while it waits?"
- **Mitigations**: explicit timeouts shorter than the caller's own deadline; deadline propagation; bulkheads (separate pools per dependency); circuit breakers; load shedding.

### Cascading failure and retry storms

- **What happens**: a dependency falters, every client retries, load multiplies, and the dependency cannot recover. Layers of retries (client, gateway, service, library) multiply each other.
- **Question**: "Which layers retry, how many times, with what backoff? What is the worst-case amplification?"
- **Mitigations**: retry at one layer only; exponential backoff with jitter; retry budgets; circuit breakers; idempotency so retries are safe.

### Hard dependency on a non-critical service

- **What happens**: a nice-to-have feature (recommendations, analytics, avatars) is called synchronously on the critical path, so its outage takes down the critical flow.
- **Question**: "If this dependency is down, which user-facing functions stop working? Should they?"
- **Mitigations**: graceful degradation with defaults; asynchronous calls; caching last known good values; moving the call off the critical path.

### Third-party limits and outages

- **What happens**: provider rate limits, quota exhaustion, API deprecations, regional outages, or price changes.
- **Question**: "What is the plan when the provider rate-limits us at peak, or is down for an hour?"
- **Mitigations**: client-side rate limiting; queues to smooth bursts; fallbacks or secondary providers for critical functions; contractual SLAs understood; abstraction where switching is a realistic need.

## Data and consistency

### Dual writes

- **What happens**: the service writes to its database and publishes an event (or writes to two stores) as separate operations; one succeeds and the other fails, leaving them inconsistent.
- **Question**: "What happens if the process crashes between these two writes?"
- **Mitigations**: transactional outbox; change data capture; making one store the source of truth and deriving the other; idempotent consumers with reconciliation.

### Cache divergence and stampedes

- **What happens**: cached data is stale or never invalidated; or a popular key expires and many requests hit the backing store at once.
- **Question**: "What is the invalidation strategy, how stale may data be, and what happens when a hot key expires?"
- **Mitigations**: explicit staleness budget; write-through or event-driven invalidation; request coalescing; jittered expiry; serving stale while revalidating.

### Read-your-writes and replication lag

- **What happens**: a user writes, is routed to a replica that has not caught up, and sees old data, often interpreted as "my change was lost".
- **Question**: "After a user saves, which store serves their next read?"
- **Mitigations**: route a user's reads to the primary for a window after writes; session consistency tokens; designing the UI to tolerate lag.

### Distributed transactions across services

- **What happens**: a business operation spans services (order, payment, inventory) and partially completes.
- **Question**: "What state is left if step 2 of 3 fails? Who notices and who fixes it?"
- **Mitigations**: sagas with compensating actions; a single owner of the workflow; idempotent steps; periodic reconciliation jobs; reconsidering the service boundary if the operation is fundamentally transactional.

### Ordering and duplicates in messaging

- **What happens**: messages are delivered more than once, out of order, or not at all (depending on guarantees); consumers assume exactly-once in-order delivery.
- **Question**: "What does the consumer do with a duplicate, or with an update that arrives before the create?"
- **Mitigations**: idempotent consumers keyed by message ID; per-entity ordering via partition keys; version numbers to discard stale updates; dead-letter queues with alerting.

### Poison messages

- **What happens**: one malformed message fails processing, is retried forever, and blocks the queue or partition.
- **Question**: "What happens to a message that always fails?"
- **Mitigations**: bounded retries then dead-letter; alerting on dead-letter volume; tooling to inspect and replay.

### Schema evolution

- **What happens**: a producer changes a message or API schema; consumers on the old version break; or a database migration is incompatible with code still running during a rolling deploy.
- **Question**: "Can the old and new versions run side by side during deploy? In which order are producers and consumers upgraded?"
- **Mitigations**: backward- and forward-compatible changes; expand-and-contract migrations; schema registries with compatibility checks; versioned APIs.

## Capacity and load

### Unbounded queues and backlogs

- **What happens**: producers outpace consumers; the queue grows until memory, disk, or message age limits are hit; latency for every message rises.
- **Question**: "What happens when consumers fall behind by an hour? Is there backpressure?"
- **Mitigations**: bounded queues; backpressure to producers; autoscaling consumers on lag; shedding or sampling low-value work; alerting on age of oldest message.

### Hot partitions and hot keys

- **What happens**: load is not evenly distributed (one big tenant, one celebrity account, a timestamp-ordered key), so one shard saturates while others idle.
- **Question**: "What is the partition key, and what happens when one customer is 100x larger than average?"
- **Mitigations**: better key choice; key salting; dedicated capacity for large tenants; per-tenant rate limits.

### Fan-out amplification

- **What happens**: one request triggers calls to many services or many items, multiplying load and tail latency (the slowest of N calls dominates).
- **Question**: "How many downstream calls does one top-level request make in the worst case?"
- **Mitigations**: batching; precomputation; caching; hedged requests for tail latency; limiting fan-out width.

### Thundering herd on recovery

- **What happens**: after an outage, all clients reconnect or retry at once and knock the service over again.
- **Question**: "What happens in the first minute after this service comes back?"
- **Mitigations**: jittered reconnects; gradual traffic ramp; admission control; warming caches before taking traffic.

## Infrastructure and operations

### Single points of failure

- **What happens**: one instance, zone, region, DNS provider, certificate, or credential whose failure stops the system. Often hidden: a single shared database behind "independent" services, a single person who can deploy.
- **Question**: "List every component that, if lost, stops the service. Which of those are acceptable?"
- **Mitigations**: redundancy proportional to the availability target; multi-zone by default for critical stateful components; documented manual recovery for accepted SPOFs.

### Deploy and configuration changes

- **What happens**: a large share of incidents are caused by changes. Bad config pushed everywhere at once, migrations that lock tables, incompatible versions mid-rollout.
- **Question**: "How is a change rolled out, how fast is it detected if bad, and how fast is it rolled back?"
- **Mitigations**: progressive delivery (canaries, staged rollouts); feature flags; config validation; automated rollback on health signals; separating schema migrations from code deploys.

### Resource exhaustion

- **What happens**: disks fill with logs, connection limits are reached, file descriptors run out, certificates and credentials expire, quotas are hit.
- **Question**: "Which finite resources does this consume, and what alerts before they run out?"
- **Mitigations**: capacity alerts with lead time; log rotation and retention; connection pooling with limits; automated certificate renewal with expiry monitoring.

### Region or zone loss

- **What happens**: a whole zone or region becomes unavailable or partitioned.
- **Question**: "What is the recovery time and data loss objective, and has failover been tested?"
- **Mitigations**: matching the availability target to an appropriate topology (multi-zone, active-passive region, active-active); tested failover runbooks; awareness that active-active multiplies consistency complexity.

### Observability gaps

- **What happens**: the system fails in a way no metric, log or trace shows; or the alerting is so noisy it is ignored.
- **Question**: "For each of the top scenarios, which signal tells on-call it is failing, and how quickly?"
- **Mitigations**: service-level indicators on user-facing scenarios; distributed tracing across service boundaries; alerting on symptoms, not just causes; runbooks linked from alerts.

## Security-relevant architecture failures

- **Flat trust**: internal services trust any caller on the network. Question: "If one service is compromised, what else can it reach?" Mitigations: service identity and authentication; network segmentation; least-privilege credentials.
- **Tenant isolation in one layer only**: isolation depends entirely on every query remembering a filter. Question: "What stops a single missing filter from leaking data across tenants?" Mitigations: enforcement in the data-access layer or database policies; per-tenant encryption keys or storage where risk warrants.
- **Secrets sprawl**: credentials copied into many configs and environments. Question: "How do we rotate this credential, and how long does it take?" Mitigations: central secret management; short-lived credentials; workload identity.

## Evolution and organisational failures

- **Distributed monolith**: services that must be deployed together or share a database, combining the costs of both architectures. Question: "Can each service be deployed independently today?"
- **Boundaries against the grain of change**: a frequently-changing concept split across services and teams. Question: "Which recent feature would have needed changes in more than one service under this design?"
- **Ownership gaps**: shared components nobody owns. Question: "Who is paged when this breaks? Who approves changes to it?"
- **Irreversible early choices**: vendor-specific features or data models adopted before requirements settle. Question: "What would it cost to move off this in two years?"
