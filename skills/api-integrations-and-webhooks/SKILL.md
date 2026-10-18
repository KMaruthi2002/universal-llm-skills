---
name: api-integrations-and-webhooks
description: >-
  Integrate with third-party APIs and receive webhooks reliably and securely:
  reading API docs critically, choosing and implementing auth (API keys, OAuth
  2.0 flows, signed requests), rate limits, timeouts, retries with exponential
  backoff and jitter, pagination, idempotency keys, webhook signature
  verification, deduplication, replay and reconciliation, sandbox vs
  production, versioning, and secret storage. Use when asked to connect to,
  sync with, or call an external service's API, build a client or SDK wrapper,
  receive or debug webhooks, handle OAuth, or fix an integration that drops,
  duplicates, or gets rate-limited.
metadata:
  category: automation
  related: api-design, authentication-and-authorization, error-handling, secure-coding, workflow-automation, etl-pipelines, observability, backend-development
---

# API Integrations and Webhooks

Integrating with someone else's API means depending on a system you do not control, over a network that fails, under limits you did not set, documented by people who may not have tested their examples. The work is less about making the first request succeed and more about what happens on the ten-thousandth: the timeout after the payment was taken, the webhook delivered twice, the token that expired at 2 a.m., the field that changed type in a minor version.

## Scope

Covers: consuming REST, GraphQL and RPC-style third-party APIs; OAuth and other auth schemes from the client side; receiving and processing webhooks; keeping local state in sync with a remote system.

Related:
- Designing your own API for others to consume: `api-design`.
- Building your own login/authorization system: `authentication-and-authorization`.
- Orchestrating multi-step business processes around integrations: `workflow-automation`.
- Bulk extraction into a warehouse: `etl-pipelines`.
- General error-handling design: `error-handling`.

## Core principles

1. **The network will fail in every possible way.** Requests time out, connections reset, responses arrive after you gave up, servers return 200 with an error body. Design each call assuming its outcome may be unknown, and decide in advance what "unknown" means for your data.

2. **Retries require idempotency.** Retrying a non-idempotent call (create payment, send message) after an ambiguous failure can do it twice. Use the provider's idempotency key mechanism, or make the operation idempotent on your side by checking before acting.

3. **Webhooks are at-least-once, unordered, and forgeable.** Every provider redelivers on failure; most do not guarantee order; anyone can POST to your endpoint. Verify signatures, deduplicate by event ID, and treat the webhook as a notification to reconcile rather than the source of truth when stakes are high.

4. **Respect limits proactively.** Rate limits protect the provider and are part of your contract. Pace requests below the limit and back off on signals; do not treat 429s as a normal control mechanism.

5. **Secrets are the integration's crown jewels.** API keys and OAuth tokens grant access to customer data or money. Store them in a secret manager, scope them minimally, never log them, and plan rotation.

6. **Isolate the integration behind your own interface.** Wrap the third-party client in a thin module that speaks your domain. Why: provider changes, version upgrades, mocking in tests, and switching providers then touch one place.

## Process

### 1. Read the docs like a sceptic

Gather before coding:
- **Auth model** and scopes/permissions available.
- **Rate limits**: per key, per user, per endpoint; burst vs sustained; how signalled (headers such as `X-RateLimit-Remaining`, `Retry-After`).
- **Pagination** style and maximum page sizes.
- **Idempotency** support (header name, key lifetime, which endpoints).
- **Error format** and which errors are retryable.
- **Webhooks**: event types, payload shape, signature scheme, retry schedule, ordering guarantees, how to replay missed events.
- **Versioning** and deprecation policy; how the version is selected (URL, header, account setting).
- **Sandbox/test mode** and how it differs from production (often: different keys, different base URL, some features missing, fake data).
- **Terms of use**: caching limits, data retention, display requirements, prohibited uses.

Then verify the docs against reality with a few exploratory calls in the sandbox. Note discrepancies; docs are frequently out of date. Check the provider's official SDK: it may already handle retries, pagination and signatures correctly — or it may be unmaintained. Decide based on its quality, not on reflex.

### 2. Choose and implement auth

| Scheme | Typical use | Key points |
|---|---|---|
| API key / bearer token | Server-to-server, single account | Store as a secret; send in header, never in URLs (URLs are logged); restrict by scope/IP if supported |
| OAuth 2.0 Authorization Code (+ PKCE) | Acting on behalf of users of another service | Validate `state` against CSRF; PKCE for public clients; store refresh tokens encrypted; request minimal scopes |
| OAuth 2.0 Client Credentials | Server-to-server with a provider that uses OAuth | Cache the access token until near expiry; refresh proactively |
| Signed requests (HMAC, AWS SigV4-style) | Providers requiring request signing | Use the provider's or a well-tested library; clock skew breaks signatures |
| mTLS | High-security B2B | Certificate rotation and expiry monitoring |
| Basic auth | Legacy | Only over TLS; treat as a password |

OAuth specifics that bite:
- **Refresh token rotation**: some providers issue a new refresh token on each refresh and invalidate the old one. Concurrent workers refreshing at once can lock each other out. Serialise refreshes (a lock per account) and persist the new token atomically.
- **Expiry and revocation**: users revoke access, admins remove apps, tokens expire after inactivity. Detect `invalid_grant` / 401, mark the connection as needing reauthorisation, and notify the user; do not retry forever.
- **Redirect URIs** must match exactly; keep separate app registrations for sandbox and production.
- **Scopes**: request the least needed. Broad scopes increase the blast radius of a leak and may trigger lengthy provider reviews.

Never ask users to give you their password for another service so you can call its API as them; use the provider's delegated auth.

### 3. Make calls robust

**Timeouts.** Set connect and read timeouts on every request. Library defaults are often infinite. Pick values from the provider's typical latency (e.g. connect 5 s, read 30 s), and longer only for known slow endpoints.

**Classify responses.**

| Response | Retry? | Notes |
|---|---|---|
| Connection error, timeout | Yes, if the operation is idempotent or has an idempotency key | Outcome unknown: the request may have succeeded |
| 408, 429 | Yes, after `Retry-After` or backoff | 429 means slow down globally for that key |
| 500, 502, 503, 504 | Yes, with backoff | Cap attempts |
| 400, 422 | No | Fix the request; log the error body |
| 401 | Refresh token once, then no | Persisting 401 means re-auth needed |
| 403 | No | Permissions/scopes; alert |
| 404 | Usually no | Unless eventual consistency is documented |
| 409 | Depends | Conflict, often "already exists" — may mean a previous attempt succeeded |
| 200 with error in body | Inspect | Some APIs (and GraphQL) report errors with 200 |

**Exponential backoff with jitter.** Wait `base * 2^attempt`, capped, with randomness, so many clients do not retry in lockstep:

```python
import random, time

def backoff_delays(base=0.5, cap=30.0, attempts=6):
    for n in range(attempts):
        yield random.uniform(0, min(cap, base * 2 ** n))  # "full jitter"

def call_with_retries(do_request, is_retryable):
    last_exc = None
    for delay in backoff_delays():
        try:
            resp = do_request()
        except (TimeoutError, ConnectionError) as exc:
            last_exc = exc
        else:
            if not is_retryable(resp):
                return resp
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                delay = max(delay, float(retry_after))  # may also be an HTTP date
        time.sleep(delay)
    raise RuntimeError("retries exhausted") from last_exc
```

Bound the **total** time spent retrying, not just the attempt count, especially inside user-facing requests. For high-volume integrations, add a circuit breaker so a provider outage does not exhaust your workers.

**Idempotency keys.** For create/charge/send operations, generate a key per logical operation (not per attempt), persist it with your local record *before* calling, and send the same key on every retry. If the provider has no idempotency support, look up by a client reference (many APIs accept an external ID/metadata) before re-creating.

**Rate limiting on your side.** Use a token bucket or the provider's documented quota to pace requests; share the limiter across all workers using the same key (e.g. in a shared store). Read remaining-quota headers and slow down before hitting zero. Batch endpoints, where offered, reduce call counts dramatically.

### 4. Paginate correctly

| Style | How to iterate | Pitfalls |
|---|---|---|
| Cursor / next token | Follow `next` until absent | Do not construct cursors yourself; they may expire |
| Offset/limit or page number | Increment until fewer than `limit` returned | Items shift if data changes during iteration → duplicates/skips |
| Link header (`rel="next"`) | Follow URLs | Preserve auth; URLs may point to different hosts |
| Time-window | Query by `updated_since` slices | Boundary items: use inclusive/exclusive consistently and dedupe |

Always cap total pages as a guard against loops, dedupe by ID, and checkpoint progress for long syncs so they resume rather than restart.

### 5. Receive webhooks safely

An endpoint receiving webhooks should:

1. **Verify authenticity** before anything else. Typically an HMAC signature over the raw request body (and often a timestamp) using a shared secret. Compute over the **raw bytes** — parsing and re-serialising JSON changes them. Compare with a constant-time function. Reject timestamps outside a tolerance window (e.g. 5 minutes) to block replays.
2. **Respond fast.** Acknowledge with 2xx within the provider's timeout (often a few seconds), after durably storing the event. Do heavy processing asynchronously via a queue. Slow endpoints cause provider retries, duplicates, and eventually the provider disabling your endpoint.
3. **Deduplicate** by the provider's event ID (store processed IDs with a retention longer than the provider's retry window). Make handlers idempotent as well, because dedup storage can fail.
4. **Handle disorder.** Events can arrive out of order (`updated` before `created`). Use timestamps/versions in the payload, or treat the event as a trigger to fetch the current state of the object from the API.
5. **Ignore unknown event types** gracefully (return 2xx, log) so new provider events do not cause retries.
6. **Return errors deliberately**: non-2xx tells the provider to retry. Return 2xx for events you have stored even if processing later fails; handle that failure internally.

Illustrative HMAC verification (adapt to the provider's exact scheme — header names, encoding, and what is signed vary):

```python
import hmac, hashlib, time

def verify(raw_body: bytes, header_sig: str, header_ts: str, secret: bytes) -> bool:
    if abs(time.time() - int(header_ts)) > 300:
        return False
    signed = header_ts.encode() + b"." + raw_body
    expected = hmac.new(secret, signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header_sig)
```

Additional hardening: HTTPS only; a hard-to-guess path is not a substitute for signatures; restrict by provider IP ranges only as an extra layer (they change); limit body size; never execute or follow URLs from payloads blindly. If a provider offers no signatures, fetch the referenced object from the API using your credentials instead of trusting the payload.

### 6. Reconcile and replay

Webhooks get lost: your endpoint was down beyond the retry window, a deploy broke verification, the provider had an incident. Plan for it:

- **Periodic reconciliation**: a scheduled job lists recently changed objects via the API and compares with local state. This is the safety net that makes webhook loss recoverable.
- **Replay**: know how to request redelivery from the provider (dashboard or API), and keep your own stored raw events so you can reprocess after fixing a handler bug.
- **Event log**: store raw payloads (with retention appropriate to their sensitivity) with receipt time, verification result, and processing status.

### 7. Sandbox, production and versioning

- Keep **separate credentials, base URLs, webhook endpoints and secrets** per environment, selected by configuration. Make it hard to send production requests from a dev machine: production keys live only in production.
- **Test-mode data is not production data**: rate limits, latency, available features and edge cases differ. Plan a careful first production run (small volume, monitored).
- **Pin the API version** explicitly where possible. Read changelogs; schedule upgrades; test against the new version in sandbox before switching.
- **Tolerant reading**: ignore unknown fields; do not fail on new enum values without a plan (map to "unknown" and alert). Strict on what you send, tolerant on what you receive.

### 8. Secrets

- Store keys and tokens in a secret manager or the platform's encrypted secret store; inject at runtime. Never commit them, including in test fixtures and example configs (use placeholders).
- Scope keys to the minimum permissions and, where supported, to IPs or specific resources. Use restricted/sub-keys for components that need less.
- Never log secrets, full auth headers, or URLs with keys in query strings. Configure HTTP client logging to redact.
- Plan rotation: support two valid keys during a changeover; know how to revoke quickly if leaked.
- Per-user OAuth tokens are user data: encrypt at rest, delete on disconnect, and honour the provider's data policies.

## Shaping the wrapper module

What a thin integration layer should own, so the rest of the codebase does not have to:

- **One configured HTTP client** per provider: base URL, auth injection, timeouts, user agent, redacted logging.
- **Retry, backoff and rate limiting** applied consistently, with per-endpoint exceptions where needed.
- **Pagination helpers** that return an iterator over items, hiding cursors and pages.
- **Error translation** from provider errors into a small set of your own (e.g. `NotFound`, `RateLimited`, `AuthExpired`, `InvalidRequest`, `ProviderUnavailable`) so callers can react without parsing provider bodies.
- **Domain mapping**: convert provider objects into your own types at the boundary, keeping the raw payload available for debugging.
- **Metrics**: request counts, latency, error rates and rate-limit headroom per endpoint.

Keep it thin: business decisions (what to sync, when to charge) belong to callers, not to the client. A wrapper that grows business logic becomes hard to test and hard to replace.

## Acting on users' behalf

When an integration sends messages, posts content, makes purchases, or changes records in a third-party system on a user's behalf:
- Make the action visible and attributable (the user knows what will be sent where).
- Get explicit consent for the scope of actions, and per-action confirmation for high-impact ones (payments, mass messages, public posts, deletions).
- Rate-cap outbound messaging and dedupe to avoid accidental spam.
- An assistant or agent building or testing such an integration should use sandbox accounts and test recipients, and must not trigger real outbound actions without the user's explicit go-ahead.

## Discovering context

- Is there already a client wrapper, HTTP utility, retry helper, or secret-loading convention in the codebase? Use it.
- How do existing integrations handle webhooks (shared endpoint and dispatcher, queue)?
- Which environments exist, and how are provider credentials provisioned to each?
- Are there organisational rules on approved vendors, data sharing, or required security review?

## Testing

- **Unit tests** against your wrapper with the HTTP layer mocked: success, each error class, timeouts, pagination end, malformed payloads.
- **Recorded fixtures** (real sandbox responses saved and replayed) catch shape mismatches better than hand-written mocks; scrub secrets and personal data from recordings.
- **Contract tests** in sandbox on a schedule to detect provider changes early.
- **Webhook tests**: valid signature, invalid signature, stale timestamp, duplicate event, out-of-order events, unknown event type. Many providers offer a CLI or dashboard to send test events.
- **Failure injection**: simulate timeouts after the provider accepted a request, and verify no duplicate side effects.

## Worked examples

### The ambiguous timeout on a create call

You call `POST /charges` and the read times out after 30 seconds. Did the charge happen? You cannot know from the client side. Options, best first:

1. **The provider supports idempotency keys**: you sent `Idempotency-Key: order-8812-charge` (generated and stored with the order before the first attempt). Retry with the same key; the provider returns the original result if the first attempt succeeded, or performs it once if not.
2. **No idempotency keys, but client references**: you set `metadata.order_id = 8812`. Before retrying, query for charges with that reference. If one exists, record it and stop; otherwise retry.
3. **Neither**: do not retry automatically. Mark the order "payment status unknown", alert, and reconcile against the provider's records (dashboard, reports, or a list endpoint) before acting. Accepting this manual step is better than charging twice.

### A webhook handler shape

```python
@app.post("/webhooks/provider")
def provider_webhook(request):
    raw = request.body                                  # raw bytes, before any JSON parsing
    if not verify(raw, request.headers["X-Signature"], request.headers["X-Timestamp"], SECRET):
        return Response(status=400)
    event = json.loads(raw)
    inserted = events_table.insert_if_absent(            # unique constraint on event_id
        event_id=event["id"], type=event["type"], payload=raw, received_at=utcnow())
    if inserted:
        queue.enqueue("process_provider_event", event["id"])
    return Response(status=200)                         # fast ack; duplicates are acked too

def process_provider_event(event_id):
    event = events_table.get(event_id)
    if event.status == "processed":
        return
    obj = provider.get_object(event.object_id)          # fetch current state; tolerate disorder
    apply_state_locally(obj)                            # idempotent upsert keyed by provider id
    events_table.mark_processed(event_id)
```

Design notes: storage happens before the ack, so a crash after the ack loses nothing; the handler is idempotent even if dedup fails; fetching the current object makes ordering irrelevant (at the cost of an extra API call, which is often worth it for correctness).

### Pacing to a documented limit

A provider allows 100 requests per minute per key, and three workers share the key. Giving each worker its own 100/minute limiter produces 300/minute and constant 429s. Use one shared limiter (e.g. a token bucket in a shared cache or database), set somewhat below the limit (say 90/minute) to leave headroom for retries and manual use, and still handle 429 with backoff, because limits can change or be shared with other applications on the same account.

### Syncing a large collection the first time

An initial sync of 2 million records through a list endpoint at 100 records per page and 90 requests per minute takes about 3.7 hours. Plan for it: check whether a bulk export endpoint exists; checkpoint the cursor after each page so a failure resumes rather than restarts; run the initial sync separately from incremental syncs; and start consuming webhooks *before* the initial sync begins so changes made during the sync are not missed (dedupe and version checks make the overlap harmless).

## Pitfalls and anti-patterns

- **No timeouts**, so one slow provider hangs your workers.
- **Retrying non-idempotent calls** without idempotency keys, creating duplicate charges or messages.
- **Retry storms**: immediate retries without jitter from many workers, worsening the provider's outage.
- **Verifying signatures over parsed JSON** instead of raw bytes; or using `==` instead of constant-time comparison.
- **Doing slow work inside the webhook handler** and timing out.
- **Treating webhooks as reliable and ordered**, with no reconciliation.
- **Secrets in code, URLs, logs, or error trackers.**
- **One shared OAuth refresh race** invalidating tokens.
- **Ignoring pagination**: only the first page synced, discovered months later.
- **Assuming sandbox behaviour equals production.**
- **Leaking provider types** throughout your codebase, so an API version change touches hundreds of files.
- **Silent partial failures**: a batch call that returns per-item errors which you never inspect.

## Verification

- [ ] Every outbound call has timeouts; retryable vs non-retryable errors are classified.
- [ ] Retries use backoff with jitter and a total time cap; writes use idempotency keys or pre-checks.
- [ ] Pagination iterates to completion on a dataset larger than one page.
- [ ] Rate limits are respected under realistic concurrency (tested or reasoned with numbers).
- [ ] Webhook endpoint verifies signatures on raw bytes, rejects stale timestamps, dedupes, and acks quickly.
- [ ] A duplicate and an out-of-order webhook were tested and handled.
- [ ] Reconciliation or replay path exists for missed events.
- [ ] Token expiry/revocation produces a clear "reconnect needed" state, not an infinite retry loop.
- [ ] Secrets are in the secret store, redacted from logs, separate per environment.
- [ ] Ran end-to-end in sandbox; first production run planned with low volume and monitoring.

## Reporting back

Report: what the integration does, auth method and scopes requested, how retries/idempotency/rate limits are handled, webhook events handled and how they are verified, reconciliation strategy, environments and where secrets live, what was tested in sandbox, and anything needing the user's action (registering the app, approving scopes, configuring the webhook URL, rotating a key).
