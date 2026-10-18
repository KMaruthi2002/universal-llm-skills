---
name: error-handling
description: >-
  Design how software detects, reports, propagates, and recovers from
  failures: exceptions versus result/error types, fail fast versus graceful
  degradation, validation at boundaries, retries with exponential backoff and
  jitter, idempotency, timeouts and deadlines, circuit breakers, partial
  failure, user-facing versus internal error messages, error codes and API
  error formats, and logging errors usefully without leaking secrets or
  swallowing them. Use when writing or reviewing error paths, adding retries
  or timeouts, designing an API's error responses, deciding whether to catch
  or propagate, or when failures are silent, noisy, or confusing. For finding
  the cause of a specific bug use debugging; for logging and metrics
  infrastructure use observability.
metadata:
  category: development
  related: debugging, observability, api-design, backend-development, concurrency-and-async, secure-coding, api-integrations-and-webhooks, ux-writing
---

# Error Handling

Error handling is the part of a program that runs when the world disagrees with the happy path: the file is missing, the network is down, the input is malformed, the disk is full, the downstream service is slow, the invariant you were sure of is violated. These paths run rarely in development and constantly in production. Good error handling makes failures **visible, contained, diagnosable, and recoverable where recovery is meaningful** — and never silent.

## Scope

Covers: designing error paths in code and APIs; choosing error mechanisms; deciding where to catch, wrap, propagate, retry, or fail; timeouts and resilience patterns; messages for users and operators; and logging errors.

Neighbours:

- Diagnosing a specific failure → `debugging`.
- Log pipelines, metrics, tracing, alerting → `observability`.
- API error response conventions in a broader API design → `api-design`.
- Concurrency-specific failure (cancellation, task groups, deadlocks) → `concurrency-and-async`.
- Not leaking sensitive information, input validation as a security control → `secure-coding`.
- Wording of user-facing error messages → `ux-writing`.

## Core principles

1. **Never swallow errors silently.** An empty `catch`, an ignored return code, or `except: pass` converts a loud, diagnosable failure into silent wrong behaviour, discovered later and far away. Every caught error must be handled meaningfully, propagated, or at minimum logged with context — and "logged and continued" must be a deliberate decision that continuing is correct.

2. **Handle an error where you can do something about it.** Catching makes sense where code has the context to recover (retry, fall back, ask the user, use a default that is genuinely valid) or to translate the error into the caller's vocabulary. Elsewhere, let it propagate. Catching everywhere produces duplicate logs and lost information; catching nowhere produces crashes with no context.

3. **Fail fast on programmer errors; handle expected failures gracefully.** Distinguish **bugs** (violated invariants, impossible states, null where none is allowed) from **expected operational failures** (network timeouts, invalid user input, file not found, conflicts). Bugs should crash loudly near their cause — continuing with corrupt state spreads damage. Operational failures are part of the domain and should be modelled and handled.

4. **Preserve the cause.** When wrapping or translating an error, keep the original as its cause (exception chaining, wrapped errors). The outermost message says what operation failed; the innermost says why. Losing the chain is a major source of undiagnosable incidents.

5. **Errors are part of the interface.** What a function can fail with — and what callers must handle — is as much a contract as its return type. Document it, keep it stable, and make it explicit in the type system where the language allows.

6. **Separate the audiences.** Users need to know what happened in their terms and what they can do. Operators need precise technical detail and correlation IDs. Attackers should learn nothing useful. One message rarely serves all three.

7. **Every remote call can hang.** Anything crossing a process boundary needs a timeout. A missing timeout is a latent outage: one slow dependency exhausts threads or connections and takes down the caller.

## Choosing an error mechanism

Use the project's and language's established idiom. Within that, the general trade-offs:

| Mechanism | Strengths | Weaknesses | Idiomatic in (examples) |
|---|---|---|---|
| **Exceptions** | Keeps happy path clean; propagates automatically; carries stack traces | Invisible in signatures (mostly); easy to forget what can be thrown; costly in some runtimes if used for control flow | Python, Java, C#, JavaScript/TypeScript, Ruby, C++ (in many codebases) |
| **Result / Either types** | Errors explicit in the type; compiler forces handling; composable | More verbose without language sugar; can tempt "unwrap everywhere" | Rust (`Result`), Haskell, Scala, Swift (`Result`, plus `throws`), TypeScript/Kotlin libraries |
| **Multiple return values / error values** | Explicit, simple, no hidden control flow | Verbose; easy to ignore if linters aren't enforced | Go (`val, err`), C (return codes + `errno`) |
| **Optional / nullable** | Simple for "absent" | Conveys no reason; overused for real errors | Most languages; fine for "not found" when absence is normal |
| **Panics / aborts** | Clear signal of a bug | Not for expected failures | Rust `panic!`, Go `panic`, assertions |

Guidance:

- **Expected, recoverable domain failures** (insufficient funds, validation failure, not found, conflict) are good candidates for explicit types — result types, error values, or a well-defined exception hierarchy the caller is expected to handle.
- **Unexpected failures and bugs** are best as exceptions/panics that propagate to a top-level handler.
- **Don't mix styles arbitrarily** within a module. If the codebase uses result types for domain errors and exceptions for bugs, follow that split.
- **Rust**: `?` for propagation; `thiserror`-style enums for libraries, `anyhow`-style context for applications; avoid `unwrap()` outside tests and truly-impossible cases (prefer `expect("reason")` to document why).
- **Go**: check every `err`; wrap with `fmt.Errorf("doing X: %w", err)`; compare with `errors.Is`/`errors.As`, not string matching; reserve `panic` for programmer errors.
- **Python/Java/C#/JS**: catch specific exception types, never bare catch-alls except at top-level boundaries; chain causes (`raise ... from err`, `new X(msg, cause)`, `{ cause }` in JS); use `finally`/context managers/`using`/try-with-resources for cleanup.
- **JavaScript/TypeScript async**: every promise must be awaited or have a rejection handler; unhandled rejections either crash the process or vanish depending on runtime. In TypeScript, caught values are `unknown` — narrow before using.

### Designing error types

- **Model by what the caller needs to decide**, not by where the error came from. Callers usually branch on a few categories: invalid input (don't retry; tell the user), not found, conflict/precondition failed, unauthorised/forbidden, transient/unavailable (retry may help), and internal/bug (alert).
- **Carry structured data**, not only a message: an error code, the offending field, the resource ID, whether it is retryable. Callers should never parse error message strings.
- **Keep hierarchies shallow.** A handful of well-chosen categories beats dozens of specific classes nobody catches individually.
- **Translate at boundaries.** A repository shouldn't leak driver-specific exceptions to the domain; the domain shouldn't leak domain exceptions as raw HTTP 500s. Each layer converts errors into its own vocabulary while preserving the cause.

## Process: designing the error paths for a feature

1. **Enumerate failure modes.** For each step: what can go wrong? Invalid input; missing/duplicate resources; permission denied; dependency unavailable, slow, or returning garbage; partial success; resource exhaustion (disk, memory, quota, rate limit); concurrent modification; cancellation by the user; bugs.
2. **Classify each**: bug vs expected; transient vs permanent; caller's fault vs ours vs a dependency's.
3. **Decide the response per class**:
   - Bug → fail fast; let it reach the top-level handler; alert.
   - Invalid input → reject at the boundary with a precise, actionable message; no retry.
   - Transient dependency failure → bounded retry with backoff if the operation is idempotent; then degrade or fail clearly.
   - Permanent dependency failure → fail clearly or degrade (cached data, reduced functionality) if that is genuinely acceptable to users.
   - Conflict → report so the caller can refresh and retry, or merge.
4. **Decide where each is handled** — the lowest layer with enough context to act.
5. **Ensure cleanup and consistency.** On failure, are resources released (files, locks, connections)? Is state consistent (transactions rolled back, partial writes compensated)? Is the operation safe to retry?
6. **Design the messages** for each audience (below).
7. **Test the error paths** — they are the least-exercised code and the most likely to be broken (see Verification).

## Validation at boundaries

- **Validate at the edges of trust**: user input, API requests, file contents, environment/config, messages from queues, responses from third parties. Inside the core, rely on types and invariants rather than re-validating everywhere.
- **Parse, don't just validate**: convert untrusted input into a type that can only hold valid values (an `EmailAddress`, a `PositiveAmount`), so downstream code cannot receive invalid data.
- **Report all field errors at once** for user input, rather than one per round trip.
- **Validate configuration at startup** and refuse to start with an invalid one; a missing setting discovered at the first request at 3 a.m. is much worse.
- **Allowlist, don't blocklist**, for security-relevant inputs (see `secure-coding`).

## Fail fast vs graceful degradation

| Fail fast when | Degrade gracefully when |
|---|---|
| An invariant is violated (bug) | An optional feature's dependency fails (recommendations, avatars) |
| Continuing could corrupt or lose data | A stale or default answer is genuinely acceptable and clearly labelled |
| Configuration is invalid at startup | Partial results are useful and the response says they are partial |
| Security checks can't be performed (fail closed) | The user can still complete their primary task |
| Money, legal, or safety outcomes depend on correctness | The degraded mode is observable (metric/log) so it doesn't hide a permanent outage |

**Fallbacks need care.** A fallback that silently substitutes a default (`0`, empty list, "unknown") can make a broken dependency look like real data. Make degraded responses distinguishable to the caller and visible to operators. And **fail closed** for authorisation: if a permission check errors, deny.

## Retries, backoff, and idempotency

Retry only when all of these hold:

- The failure is **plausibly transient**: timeouts, connection resets, 429 Too Many Requests, 503 Service Unavailable, deadlock/serialisation failures in databases, explicitly retryable error codes. Do *not* retry validation errors, 4xx client errors (other than 408/429 and documented cases), authentication failures, or bugs.
- The operation is **idempotent**, or made idempotent with an **idempotency key**: the client sends a unique key per logical operation; the server records the result for that key and returns it for duplicates. Essential for payments, order creation, and anything with side effects. A timeout doesn't mean the operation failed — it may have succeeded and the response was lost.
- There is a **budget**: limited attempts (often 3–5) and a limited total time, fitting within the caller's own deadline.

Backoff:

- **Exponential backoff with jitter**: delay = random between 0 and min(cap, base × 2^attempt) ("full jitter"). Jitter prevents synchronised retry waves from many clients.
- **Respect server hints**: `Retry-After` headers, rate-limit reset times.
- **Retry at one layer only.** If the HTTP client retries 3×, the service client retries 3×, and the job runner retries 3×, a single failure becomes 27 attempts — retry amplification that turns a slow dependency into a dead one. Decide which layer owns retries.
- **Retry budgets / circuit breakers** at the system level: if a large fraction of calls are failing, stop retrying and fail fast to let the dependency recover.

Illustrative (pseudocode):

```
for attempt in 0..max_attempts:
    try:
        return call(idempotency_key=key, timeout=remaining(deadline))
    except error if is_transient(error) and attempt < max_attempts - 1:
        sleep(random(0, min(cap, base * 2**attempt)))
raise  # last error, with context
```

## Timeouts and deadlines

- **Set a timeout on every network call, lock acquisition, queue wait, and external process.** Library defaults are often infinite or minutes long.
- **Choose values from data**: slightly above the dependency's p99 latency under normal load, and within your own caller's budget. Too short → spurious failures; too long → resource exhaustion during incidents.
- **Propagate deadlines**, not just per-hop timeouts: if the user request has 2 s total, downstream calls get the *remaining* budget. Many RPC frameworks and context/cancellation mechanisms support this (e.g. Go `context`, gRPC deadlines, cancellation tokens, abort signals).
- **Distinguish connect timeout from read/idle timeout**; they fail for different reasons.
- **On timeout, cancel the underlying work** if possible, or it continues consuming resources (see `concurrency-and-async`).

## Circuit breakers and bulkheads

- **Circuit breaker**: track failures to a dependency; after a threshold, "open" and fail immediately for a cool-down period; then allow a trial request ("half-open"); close on success. Prevents wasting resources on a dependency that is down and gives it room to recover.
- **Bulkheads**: separate resource pools (threads, connections, queues) per dependency or per workload, so one slow dependency cannot exhaust everything.
- **Load shedding**: under overload, reject excess work early (fast 503/429) instead of accepting it and timing out slowly.
- These are system-level patterns; use them for dependencies whose failure would otherwise cascade. Many service meshes, client libraries, and frameworks provide them — prefer an existing implementation.

## Partial failure and consistency

- **Batch operations**: decide and document whether a batch is all-or-nothing (transactional) or per-item (return per-item results with statuses). Never report overall success when some items failed.
- **Multi-step operations across systems** can't use a single transaction. Use idempotent steps with retries, a saga with compensating actions, or an outbox pattern so that database changes and messages are published consistently.
- **Cleanup on failure**: use language constructs that guarantee release (`finally`, `defer`, RAII, context managers, `using`). Errors *during* cleanup must not mask the original error — log the secondary error and re-raise the primary.

## Messages: users vs operators

**User-facing messages** (see `ux-writing` for wording):

- Say what happened in the user's terms, whether their data is safe, and what they can do next. "We couldn't save your changes because the connection was lost. Your draft is kept on this device — try again when you're back online."
- Don't blame the user; don't show stack traces, SQL, file paths, internal hostnames, or library names.
- Include a reference ID (correlation/request ID) for support when an internal error occurs.
- Keep validation messages specific and next to the field they concern.

**API error responses**:

- Use the protocol's status codes correctly (HTTP: 400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 semantic validation where the project uses it, 429 rate-limited, 500 internal, 503 unavailable).
- Return a consistent, machine-readable body: a stable error code, a human-readable message, field-level details, and a request ID. Follow the project's existing format or a standard such as RFC 9457 problem details. Clients branch on codes, never on message text.
- Don't distinguish "user doesn't exist" from "wrong password" in authentication errors (enumeration risk).
- Treat error codes as part of the API contract; changing them is a breaking change.

**Operator-facing (logs)** — next section.

## Logging errors usefully

- **Log once, at the point where the error is handled** (or at the top-level boundary), not at every layer it passes through. Duplicate logs of the same error inflate noise and confuse counts. Intermediate layers add context by wrapping, not by logging.
- **Include context**: operation, relevant IDs (request, user, order — but not secrets), inputs summarised, the full cause chain and stack trace, retry attempt number, elapsed time.
- **Use structured logging** (key-value or JSON) where the project does, so errors can be searched and aggregated.
- **Choose levels deliberately**: ERROR for failures needing attention; WARN for degraded but handled situations; INFO for expected business events (a validation rejection is usually INFO or not logged at all, not ERROR). Alert on rates of errors, not individual log lines.
- **Never log secrets or sensitive data**: passwords, tokens, API keys, full card numbers, session cookies, personal data beyond what policy allows. Be careful logging whole request objects or exception messages that embed them (connection strings in driver errors are a classic leak). Redact at the logging layer where possible.
- **Top-level handlers**: every process, thread, async task, job worker, and request pipeline needs a last-resort handler that logs unhandled errors with context and returns a safe response or exits cleanly. Background tasks that die silently are a common cause of "it just stopped working."

## Brief idioms by language (illustrative)

Wrapping with context while preserving the cause:

```python
# Python
try:
    config = load_config(path)
except FileNotFoundError as err:
    raise ConfigError(f"config file missing: {path}") from err
```

```go
// Go
cfg, err := loadConfig(path)
if err != nil {
    return fmt.Errorf("loading config %s: %w", path, err)
}
// callers: if errors.Is(err, fs.ErrNotExist) { ... }
```

```typescript
// TypeScript
try {
  config = await loadConfig(path);
} catch (err: unknown) {
  throw new ConfigError(`config file missing: ${path}`, { cause: err });
}
```

```rust
// Rust (application code with a context helper library)
let cfg = load_config(&path).with_context(|| format!("loading config {}", path.display()))?;
```

Expected domain failure modelled explicitly (pseudocode, adapt to the language's idiom):

```
withdraw(account, amount) -> Result<Receipt, WithdrawError>
WithdrawError = InsufficientFunds { available } | AccountFrozen | LimitExceeded { limit }
```

The caller is forced to decide what each case means for the user; a database outage is *not* in this type — it propagates as an unexpected failure to the top-level handler.

## Error handling in specific contexts

- **Command-line tools**: print a concise message to stderr (not stdout, which may be piped), exit with a non-zero status, and reserve stack traces for a verbose/debug flag. Distinguish usage errors (often exit code 2) from runtime failures (1) if the ecosystem has conventions. See `cli-development`.
- **Scripts and automation**: fail on the first unexpected error rather than continuing with bad state (in shell, `set -euo pipefail` and checking commands whose failure is expected). See `scripting-and-shell`.
- **Batch and data jobs**: decide per-record vs whole-job failure. Common pattern: process valid records, write invalid ones with reasons to a reject file or table, and fail the job if rejects exceed a threshold — so one bad record doesn't block everything, but a systemic problem still stops the run.
- **Message consumers**: a message that always fails ("poison message") will be retried forever and block the queue. Limit redeliveries, then move it to a dead-letter queue with the error attached, alert, and keep processing. Make handlers idempotent because redelivery is normal.
- **Webhooks and inbound integrations**: acknowledge quickly and process asynchronously; return error status only when you want the sender to retry; verify signatures before processing. See `api-integrations-and-webhooks`.
- **User interfaces**: keep the user's input on failure; show errors next to the cause; distinguish "you can fix this" from "we have a problem"; offer retry for transient failures; never leave a spinner running forever — every pending state needs a timeout and an error state.
- **Libraries**: never log-and-continue or exit the process on the caller's behalf; return or raise errors with stable, documented types so applications decide policy. Don't print to stdout/stderr from library code.
- **Startup**: validate configuration and required dependencies early, and exit with a clear message if they are missing. Decide deliberately whether an unavailable dependency at startup should block startup or be retried in the background.

## A worked example (illustrative)

A service endpoint creates an order: validate the cart, reserve stock (inventory service), charge the card (payment provider), save the order, and send a confirmation email.

- *Validation failures* (empty cart, bad quantity) → 400/422 with field details; no logging at ERROR; no retry.
- *Inventory service timeout* → transient; retry up to 2 times with jittered backoff using a reservation idempotency key, within a 1.5 s overall budget; then respond 503 with a retry-friendly message. Reservation expiry on the inventory side cleans up abandoned reservations.
- *Payment declined* → expected domain outcome; release the reservation; respond 402/422 per the project's convention with a user-safe reason category; log at INFO with order and request IDs (never card details).
- *Payment provider timeout* → the charge may have succeeded. Do not blindly retry without the idempotency key; query the provider by key or retry with the same key, which the provider deduplicates.
- *Database save fails after a successful charge* → the dangerous case. Use an outbox or a recorded "payment captured, order pending" state so a reconciler can complete or refund; alert on it. Never leave a captured charge with no record.
- *Email fails* → non-critical; enqueue for retry in the background; the order still succeeds. Degradation is logged at WARN and monitored.
- *Unexpected exception anywhere* → propagates to the request handler, which logs it once with context and the request ID, returns a generic 500 with the request ID, and increments an error metric.

The design question at each step was the same: is this a bug, invalid input, or an operational failure; is it transient; is the operation idempotent; and what does the user need to know.

## Making failures visible to operators

Handled errors still need to be seen in aggregate:

- **Count errors by category** (validation, dependency, internal) as metrics, so a rising rate is visible before users report it.
- **Alert on symptoms and rates** — error ratio, failed jobs, dead-letter queue depth, circuit breakers open — not on individual log lines, which produces alert fatigue.
- **Track degraded modes**: every fallback path should increment a metric; a fallback that silently runs for a week is an undetected outage.
- **Correlate**: request/trace IDs in every error log and user-facing reference let one failure be followed across services (see `observability`).

## Discovering context

- **Find the project's conventions**: error base classes or enums, result types, wrapping helpers, error codes registry, API error format, middleware that maps errors to responses, logging library and field conventions, retry/timeout utilities, resilience libraries in use.
- **Read how existing code handles similar failures** in the same layer and follow suit for consistency; flag dangerous existing patterns (swallowed errors, infinite retries, missing timeouts) to the user rather than silently rewriting them all.
- **Check dependency behaviour**: which exceptions or error codes a client library actually raises, its default timeouts and retry behaviour (some retry internally — don't add a second layer blindly), and whether operations are idempotent.
- **Ask about requirements** where they decide design: acceptable staleness for fallbacks, whether partial success is acceptable, SLOs that set timeout budgets, compliance rules on what may be logged.

## Pitfalls

- Empty catch blocks; catching the base exception type deep in the code; `catch (e) { return null }`.
- Logging and rethrowing at every layer (log spam), or logging at none (silent failures).
- Losing the original cause when wrapping; replacing a precise error with a generic "something went wrong" internally.
- Using exceptions or error returns for normal control flow in hot paths.
- Retrying non-idempotent operations, causing duplicate charges, emails, or records.
- Retrying without backoff/jitter, or at multiple layers, amplifying outages.
- No timeouts on network calls; timeouts longer than the caller's own deadline.
- Fallbacks that return plausible fake data without signalling degradation.
- Failing open on authorisation errors.
- Leaking internals in user/API messages (stack traces, SQL, paths) or secrets in logs.
- Parsing error message strings to decide behaviour.
- Unhandled promise rejections and background tasks with no top-level handler.
- Cleanup code that throws and hides the original error.
- Returning success for a batch where some items failed.

## Verification

- [ ] Every catch/handler either recovers meaningfully, translates with the cause preserved, or propagates; none silently swallow.
- [ ] Bugs fail fast; expected failures are modelled and handled at the layer with context to act.
- [ ] Error paths have tests: inject failures (fake dependency returning errors, timeouts, malformed data) and assert the behaviour — the message, status, retry count, cleanup, and state consistency.
- [ ] All remote calls and waits have timeouts within the caller's budget; deadlines propagate where supported.
- [ ] Retries are limited, backed off with jitter, only for transient errors, only for idempotent operations, and at a single layer.
- [ ] Resources are released and state is consistent on every failure path.
- [ ] User-facing messages are actionable and leak nothing internal; API errors follow the project's format with stable codes.
- [ ] Logs for errors have context and correlation IDs, appear once per error, and contain no secrets or disallowed personal data.
- [ ] Top-level handlers exist for processes, workers, and async tasks.
