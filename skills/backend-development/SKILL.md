---
name: backend-development
description: >-
  Build and change server-side services in any language or framework: the
  request lifecycle, input validation, where business logic belongs,
  transactions and data access, background jobs, configuration and secrets,
  statelessness, timeouts and resource limits, logging, and testing. Use when
  implementing an endpoint, handler, worker, or service; adding a feature to a
  server codebase; wiring up a database or queue; moving work to the
  background; or making a backend production-ready. For API contract design use
  api-design; for schema design use database-design; for structure across
  modules use software-architecture.
metadata:
  category: development
  related: api-design, database-design, sql-and-queries, software-architecture, error-handling, authentication-and-authorization, secure-coding, testing-strategy, observability, concurrency-and-async
---

# Backend Development

Backend code runs unattended, under concurrent load, against data that matters, while talking to dependencies that fail. Most backend bugs are not in the clever parts; they are at the edges — unvalidated input, missing timeouts, half-committed transactions, retries that duplicate work, configuration that differs between environments. This skill is about getting those edges right in whatever stack the project uses.

## Scope

Covers implementing server-side behaviour: HTTP/RPC handlers, workers and consumers, scheduled tasks, data access, integration with caches, queues, and external services, and the operational concerns that make a service production-ready.

Neighbouring skills:
- Contract design (URLs, payloads, errors, versioning) — `api-design`.
- Schemas, keys, and indexes — `database-design`; query writing — `sql-and-queries`.
- Module boundaries and layering across the codebase — `software-architecture`.
- Error strategy in depth — `error-handling`; concurrency primitives — `concurrency-and-async`.
- Identity and permissions — `authentication-and-authorization`; vulnerabilities — `secure-coding`.
- Metrics, logs, tracing — `observability`. Cron-style jobs — `scheduled-jobs`.

## Core principles

### 1. Trust nothing that crosses the boundary

Every input from outside the process — request bodies, headers, query strings, uploaded files, messages from queues, responses from other services, even rows written by other systems — may be malformed, oversized, or malicious. Validate at the boundary, convert to well-typed internal values once, and let the inside of the system work with values that are known to be valid. The "why": validation scattered throughout the code is always incomplete; validation at one choke point can be complete.

### 2. Keep handlers thin; put rules where they can be tested

A handler's job is to translate: parse and validate the request, call the operation that does the work, translate the result or error into a response. Business rules belong in code that does not know about HTTP, queues, or the framework, so they can be tested directly and reused from a handler, a worker, a CLI, or a test. Fat handlers duplicate rules across entry points and can only be tested through the transport.

### 3. Every external call can be slow, fail, or succeed without you knowing

Databases, caches, other services, and third-party APIs will time out, return errors, and occasionally complete work after you have given up waiting. Put a timeout on every call, decide what failure means for your operation, and make retried work safe (idempotency). A missing timeout is how one slow dependency exhausts every thread or connection in a service.

### 4. Statelessness is what makes scaling and recovery easy

A service instance that keeps no essential state in memory or on local disk can be restarted, replaced, or multiplied freely. Keep session data, uploads, job state, and caches that must be shared in external stores. In-process caches are fine as optimisations if every instance can rebuild them and staleness across instances is acceptable.

### 5. Data integrity outranks convenience

Use the database's guarantees — transactions, constraints, unique indexes, foreign keys — rather than application code that checks and then writes. "Check, then act" in application code races under concurrency; a unique constraint does not. Code can have bugs; constraints catch them.

### 6. Make it observable from the first commit

You will debug this code in production, from logs and metrics, without a debugger. Structured logs with request/correlation IDs, metrics on rate, errors, and latency for each endpoint and dependency, and traces across services are much cheaper to add while writing the code than during an incident.

## Discovering the project's conventions

Before writing backend code in an existing project, find out, and then follow:

- **Framework and layering**: how is a request routed? Where do handlers, services/use cases, repositories/data access live? Trace one existing endpoint end to end and copy its shape.
- **Validation approach**: schema library, framework validators, hand-written checks, generated types from an API spec.
- **Error handling**: custom error types, how they map to responses, the error envelope.
- **Data access**: ORM, query builder, raw SQL, stored procedures; transaction helpers; how migrations are written.
- **Dependency injection or wiring**: how services get their database handles, clients, and config.
- **Configuration**: environment variables, config files, a secrets manager; how environments differ.
- **Background work**: which job or queue system, how jobs are defined, retried, and monitored.
- **Logging and metrics**: logger, log format, what fields are always included, metric naming.
- **Testing**: unit vs. integration split, fixtures and factories, how the test database is set up, whether tests hit real dependencies or fakes.
- **Code style and lint rules**, and any checked-in scripts for running, testing, and formatting.

When conventions conflict with this skill, follow the project in the code you write and raise the concern separately, unless the convention creates a security or data-integrity bug — then raise it before proceeding.

## The request lifecycle

Walk through every stage for each new endpoint or handler:

1. **Transport and middleware**: TLS termination, request ID assignment or propagation, request size limits, timeouts, CORS (for browsers), compression. Usually configured once; verify the new route is covered.
2. **Authentication**: identify the caller. Reject early if required and missing.
3. **Parsing and validation**: parse the body and parameters into typed values; reject with field-level errors. Check types, required fields, ranges, lengths, formats, enum membership, and overall size. Strip or reject unknown fields according to the project's convention.
4. **Authorization**: can *this caller* perform *this action* on *this specific object*? Object-level checks require loading the object (or querying with the owner as a filter) — do not skip them because the route is "only used by our UI".
5. **Business operation**: the domain logic, usually inside a transaction if it writes.
6. **Side effects**: events, emails, calls to other services — ideally after commit, via an outbox or job, so they do not happen for rolled-back work (see below).
7. **Response mapping**: map the result to the response shape explicitly (do not serialise internal objects directly), set status codes and caching headers.
8. **Error mapping**: map known domain errors to appropriate responses; let unknown errors become a generic 500 with a correlation ID while the details go to logs.
9. **Telemetry**: log the outcome with request ID, user/tenant ID (if appropriate), duration, and status; record metrics.

## Where business logic goes

| Logic | Place it |
|---|---|
| Shape/format checks on input ("is a valid email", "1–100 items") | Boundary validation |
| Rules about the domain ("an order can't be cancelled after shipping") | Domain/service layer, independent of transport |
| Invariants that must hold under concurrency ("email unique", "stock ≥ 0") | Database constraints *and* domain code (domain code gives good errors, constraint guarantees correctness) |
| Orchestration ("reserve stock, charge card, create shipment") | Application/use-case layer, which owns the transaction boundary |
| Access rules ("only the owner or an admin") | An authorization layer or policy functions called from the use case, not scattered `if` checks |
| Presentation ("format price for display") | Response mapping or the client, not the domain |

Avoid two extremes: everything in handlers (untestable, duplicated), and an elaborate many-layer structure for simple CRUD (indirection without benefit). Match the depth to the complexity of the rules and to the project's existing structure.

## Data access and transactions

- **Transaction boundaries belong to the use case**, not to individual repository calls. One business operation that must be all-or-nothing runs in one transaction.
- **Keep transactions short.** Never make network calls to external services, send emails, or wait for user input inside a database transaction; it holds locks and connections while waiting on something slow and unreliable.
- **Know your isolation level.** Many databases default to read committed, which permits lost updates and write skew in read-modify-write sequences. Use atomic updates (`UPDATE ... SET balance = balance - ?  WHERE balance >= ?`), row locks (`SELECT ... FOR UPDATE`), optimistic version checks, or a stricter isolation level with retry on serialisation failure.
- **Let constraints do their job**, and translate constraint violations (e.g. unique violation) into domain errors (409 "email already registered") rather than 500s.
- **Avoid N+1 queries**: loading a list then querying per item. Use joins, batch loading (`WHERE id IN (...)`), or the ORM's eager loading. See `sql-and-queries`.
- **Bound every query**: paginate lists, limit result sizes, and never load an unbounded table into memory.
- **Use parameterised queries always.** String-built SQL is an injection vulnerability, regardless of how trusted the input seems.
- **Connection pools are finite.** Size pools against the database's connection limit divided by the number of instances; a fleet of autoscaled instances each with a large pool can exhaust the database.
- **Schema changes go through migrations**, written to be safe under live traffic (see `database-migrations`).

## Side effects and the dual-write problem

A common bug: the code commits a database transaction and then publishes a message (or sends an email, or calls another service). If the process crashes between the two, one happens without the other. If it publishes first and the transaction rolls back, consumers act on something that never happened.

Options, from most to least robust:
1. **Transactional outbox**: write the message to an outbox table in the same transaction; a separate relay publishes and marks it sent. Consumers must be idempotent because the relay may publish twice.
2. **Change data capture** from the database log, feeding a stream.
3. **Enqueue a job after commit** using a job system that stores jobs in the same database (so enqueueing is part of the transaction).
4. **Publish after commit with retries and reconciliation** — acceptable for low-stakes side effects (analytics), not for money or inventory.

## Background work

Move work out of the request path when it is slow (more than roughly a second or two), can fail transiently and should be retried, depends on unreliable third parties, or is triggered in bulk.

Design every job to be:
- **Idempotent**: running it twice has the same effect as once. Jobs *will* run more than once (retries after timeouts, redelivery after worker crashes). Use natural idempotency (upserts, "set status to X" rather than "toggle"), dedupe keys, or a processed-IDs table.
- **Small and resumable**: a job that processes a million rows should be split into batches or checkpoint progress, so a crash does not restart from zero and a deploy does not kill hours of work.
- **Bounded in retries**: exponential backoff with jitter, a maximum attempt count, then a dead-letter destination that someone monitors. Distinguish permanent failures (bad input — do not retry) from transient ones.
- **Time-limited**: a maximum runtime, after which it is killed and retried or failed.
- **Observable**: log start, finish, failure, and duration with the job ID; alert on queue age and failure rate.
- **Safe to deploy during**: workers should finish or release the current job on shutdown signals (graceful shutdown) rather than dying mid-write.

Pass job arguments by ID and re-load current state in the job, rather than serialising whole objects into the job payload — the object may have changed by the time the job runs.

## Calling other services

- **Timeouts** on every call, shorter than your own caller's timeout. If your endpoint must respond in 2 s, a dependency call cannot have a 30 s timeout.
- **Retries** only for idempotent operations or with idempotency keys; exponential backoff with jitter; small attempt count; retry at one layer only.
- **Circuit breaking / fail-fast** when a dependency is consistently failing, so you stop wasting resources and give it room to recover.
- **Fallbacks** where the business allows: cached data, a default, or a degraded response that omits the optional part.
- **Propagate context**: request/trace IDs, deadlines, and the caller's identity if the downstream service authorises on it.
- **Validate responses** from other services like any other input.
- **Wrap third-party clients** in a thin adapter you own, so their types and failure modes don't spread through your code and tests can substitute a fake.

## Configuration and secrets

- **Config from the environment** (environment variables, mounted files, a config service) — not hard-coded per environment, so the same build artifact runs everywhere.
- **Validate config at startup** and fail fast with a clear message if something required is missing or malformed. A service that starts with a missing database URL and fails on the first request is harder to diagnose.
- **Secrets** (database passwords, API keys, signing keys) come from a secrets manager or injected environment, never from source control, never logged, never returned in error messages or debug endpoints. Support rotation without redeploying code where possible.
- **Feature flags** for risky changes, with a plan to remove the flag once the change is settled.
- **Safe defaults**: debug modes, verbose errors, permissive CORS, and disabled auth must never be the default.

## Resource limits and robustness

Bound everything that can grow:
- Request body size, upload size, number of items in a list input.
- Query result sizes and page sizes.
- Concurrency per worker, connection pool sizes, queue sizes.
- Request processing time (server-side timeouts) and job runtime.
- Memory use in streaming and file processing — stream large data rather than loading it entirely.

And handle lifecycle properly:
- **Health checks**: a liveness check that only says the process is not deadlocked, and a readiness check that says it can serve (dependencies reachable, warm-up done). Do not make liveness depend on downstream services, or one dependency outage will restart your whole fleet.
- **Graceful shutdown**: on termination signal, stop accepting new work, finish in-flight requests and jobs within a deadline, close connections.
- **Startup**: run migrations as a separate deployment step rather than on every instance's startup, unless the project already handles concurrent startup migrations safely.

## Logging

- Log in the project's format; structured (key-value or JSON) logs are much easier to query.
- Include a request or correlation ID on every line, and propagate it to downstream calls and jobs.
- Log at boundaries: request outcome, dependency failures, job outcomes. Avoid logging in tight loops.
- **Never log secrets, tokens, passwords, full payment details, or unnecessary personal data.** Redact at the logger level if possible, because individual call sites will forget.
- Log enough to reproduce a failure (which operation, which entity ID, which input category), not entire request bodies.
- Error logs should be actionable; an error logged for an expected situation (a 404, a validation failure) trains people to ignore error logs.

## Testing backend code

See `testing-strategy` for the overall approach. Backend-specific guidance:

- **Unit-test domain rules** directly, without the framework, database, or network. This is where most logic tests should live.
- **Integration-test data access** against a real instance of the same database engine (e.g. via containers or a local service), not an in-memory substitute with different semantics. Constraint behaviour, query plans, transaction semantics, and SQL dialect differ.
- **Test handlers through the transport** for routing, validation, auth, status codes, and error mapping — a smaller number of tests covering each endpoint's contract.
- **Test the unhappy paths**: invalid input, unauthorised access to another user's object, dependency timeout, duplicate request with the same idempotency key, constraint violations, job retried after partial completion.
- **Fake external services** at your adapter boundary; contract-test the adapter against the real API (or its sandbox) separately.
- **Concurrency tests** for operations with invariants under contention (e.g. two simultaneous withdrawals) when the risk justifies it.
- **Isolate test data**: each test sets up what it needs and does not depend on order. Transaction rollback per test or unique tenant IDs per test are common techniques.

## Recurring backend concerns

### Multi-tenancy

If the service holds data for several customers (tenants), tenant isolation is a correctness and security property, not a feature:
- Derive the tenant from the authenticated identity, never from a request parameter the caller controls.
- Scope every query by tenant. The safest patterns make forgetting impossible: a repository or query layer that requires a tenant context, database row-level security policies, or separate schemas/databases per tenant.
- Include the tenant in cache keys, object storage paths, job payloads, and log context.
- Test cross-tenant access explicitly: a user in tenant A requesting tenant B's object must get a not-found response.
- Watch for noisy neighbours: per-tenant rate limits and quotas protect everyone else from one heavy tenant.

### File uploads and large payloads

- Enforce size and type limits before reading the whole body; check the actual content type, not just the file extension or declared header.
- Stream to storage instead of buffering in memory; for large files, prefer direct-to-object-storage uploads with short-lived pre-signed URLs so file bytes never pass through the application servers.
- Store files outside the web root with generated names; never use the client-supplied filename as a path (path traversal).
- Scan or sandbox processing of untrusted files (image decoding, document parsing, archive extraction) — parsers are a common attack surface; guard against decompression bombs.

### Time and dates

- Store instants in UTC with an explicit type; store the user's time zone separately if behaviour depends on local time.
- Use the database's or a monotonic clock consistently; do not mix clocks from several machines to order events.
- "Daily" logic (billing at midnight, "today's" totals) must define *whose* midnight. Daylight-saving transitions create 23- and 25-hour days and repeated or missing local times.
- Make time injectable in domain code so tests can control it.

### Pagination and exports

Endpoint pagination is covered in `api-design`. On the implementation side: use keyset queries (`WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT ?`) for large tables rather than large offsets, and move full exports to background jobs that write a file and notify when ready.

### Caching inside a service

- Cache at the level of the expensive thing (a computed result, a remote response), with a key that includes every input it depends on — including tenant and permissions.
- Decide what happens on cache failure: usually fall through to the source, with protection against a stampede.
- Never cache authorization decisions longer than you can tolerate a revoked permission still working.

## Worked reasoning example

*Illustrative.* Implement "place order": validate the cart, reserve stock, charge the card, confirm the order, email the customer.

1. **Boundary**: validate the request (cart ID, payment method ID, idempotency key). Authenticate; authorize that the cart belongs to the caller.
2. **Idempotency**: look up the idempotency key; if a completed result exists, return it. If one is in progress, return a conflict or wait.
3. **Stock**: reserve with an atomic conditional update per item (`... SET reserved = reserved + ? WHERE available - reserved >= ?`), inside a short transaction that also creates the order in `pending_payment`. Commit.
4. **Payment**: call the payment provider *outside* the transaction, with a timeout and the provider's own idempotency key derived from the order ID, so a retry cannot double-charge.
5. **Outcome**: on success, a second short transaction marks the order `confirmed` and writes an "order confirmed" outbox record. On a definite decline, release the reservation and mark `payment_failed`. On a timeout (unknown outcome), do not guess: mark `payment_unknown` and let a reconciliation job query the provider.
6. **Email**: sent by a worker reading the outbox; idempotent per order.
7. **Tests**: unit tests for the state transitions; integration tests for the conditional stock update under two concurrent orders for the last item; a test that a repeated request with the same idempotency key returns the same order and charges once; a test for the payment-timeout path.

The design keeps transactions short, never holds locks during the network call, and treats "don't know" as a real state rather than assuming success or failure.

## Decision guidance

### Synchronous handler vs. background job
Synchronous when the caller needs the result now and it completes reliably within the latency budget. Background when slow, flaky, bulk, or retry-worthy. A hybrid — do the essential part synchronously, enqueue the rest — is often best (create the order now, send the confirmation email in a job).

### ORM vs. query builder vs. raw SQL
Follow the project. Where you have a choice: ORMs speed up CRUD and keep mapping consistent, but hide query counts and generate inefficient SQL for complex reads. Query builders give control with composability. Raw SQL is clearest for complex reporting queries. Many healthy codebases use an ORM for writes and simple reads and hand-written SQL for complex reads. Whatever you use, inspect the generated SQL for hot paths.

### Validate with a schema library vs. by hand
A declarative schema (framework validators, a schema library, types generated from the API spec) keeps validation complete, consistent, and close to the documented contract; prefer it when the project already uses one. Hand-written checks are fine for a few fields but tend to drift from the spec and miss cases as payloads grow. Domain rules that need data ("this coupon is still valid") are not input validation — they belong in the domain layer either way.

### Monolith endpoint vs. new service
Adding an endpoint to the existing service is the default. A new deployable service is a `software-architecture` and `system-design` decision with operational costs (deploy pipeline, monitoring, on-call, network failure handling); do not create one as a side effect of implementing a feature.

### In-process cache vs. shared cache
In-process when data is small, read-heavy, and tolerable if slightly different between instances (config, reference data). Shared cache when consistency across instances matters or the data is large. Either way, define invalidation and TTLs (see `system-design`).

## Pitfalls

- **Missing object-level authorization**: checking that the user is logged in but not that the record belongs to them.
- **Check-then-act races**: "if not exists, insert" without a unique constraint; "if balance ≥ amount, subtract" without an atomic update or lock.
- **External calls inside transactions**, holding locks while waiting on the network.
- **Publishing events before commit**, or without an outbox, causing phantom or missing events.
- **Non-idempotent jobs and consumers**, producing duplicates on retry.
- **No timeouts**, or default timeouts of minutes.
- **Unbounded queries and payloads** that work in development and fall over with real data.
- **Serialising internal models directly to responses**, leaking fields.
- **Swallowing errors** (empty catch blocks, logging and continuing as if successful) or the opposite, letting expected domain errors become 500s.
- **Environment-specific code paths** (`if env == "prod"`) that mean production runs code never tested elsewhere.
- **Secrets in code, logs, or error messages.**
- **Time zone bugs**: store and compute in UTC, convert at the edges; be careful with "today" and date boundaries per user.
- **Floating point for money.**
- **Tests that mock the database** and therefore never test queries, constraints, or transactions.

## Safety

- Never run migrations, backfills, or bulk updates against production data without the user's explicit go-ahead, a backup or rollback plan, and ideally a dry run on a copy.
- Destructive endpoints and jobs (deletes, bulk updates) need authorization, confirmation semantics, and ideally soft-delete or an audit trail.
- When debugging with production data, use the minimum access needed and do not copy personal data into logs, tickets, or local files.

## Quality bar and verification

Before calling backend work done:

- [ ] The new code follows the structure of existing endpoints/jobs in this project.
- [ ] All inputs are validated at the boundary with clear field-level errors; sizes are bounded.
- [ ] Authentication and object-level authorization are enforced and tested with a "different user" case.
- [ ] Business rules live outside the handler and have unit tests.
- [ ] Writes that must be atomic are in one transaction; no network calls inside it.
- [ ] Concurrency-sensitive invariants are protected by constraints, atomic statements, locks, or version checks.
- [ ] Side effects happen after commit, via an outbox or job where they matter.
- [ ] Every external call has a timeout and a deliberate failure behaviour; retries are safe.
- [ ] Jobs and consumers are idempotent, bounded in retries, and have a dead-letter path.
- [ ] Config is externalised and validated at startup; no secrets in code or logs.
- [ ] Logs include correlation IDs and no sensitive data; key metrics exist for the new path.
- [ ] Tests cover happy path, validation failure, authorization failure, and at least one dependency failure; the full suite passes.
- [ ] If you can run the service, you exercised the endpoint or job for real (locally or in a test environment) and checked the response, the stored data, and the logs.

Report what you ran and observed, and what you could not verify.
