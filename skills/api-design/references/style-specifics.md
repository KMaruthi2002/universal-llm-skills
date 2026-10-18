# Style-Specific API Guidance

Read the section for the style you are working in. The general principles in the main skill apply to all of them.

## HTTP / REST-style APIs

### Method semantics

| Method | Safe | Idempotent | Typical use |
|---|---|---|---|
| GET | Yes | Yes | Read a resource or collection. Never change state |
| HEAD | Yes | Yes | Like GET without a body (existence, metadata) |
| POST | No | No | Create in a collection; trigger an action |
| PUT | No | Yes | Replace a resource entirely (or create at a known ID) |
| PATCH | No | Not by definition | Partial update. Define the format (merge-patch or JSON Patch) |
| DELETE | No | Yes | Remove. A repeat DELETE should not error in a way that confuses retries — returning 404 or 204 are both defensible; document it |

"Safe" means callers, crawlers, prefetchers, and proxies may issue the request freely. A GET that changes state will eventually be triggered by something you did not expect.

### Status codes worth getting right

- `201 Created` with a `Location` header for creates; `200` or `204` for successful updates and deletes, consistently.
- `202 Accepted` for work queued asynchronously, with a way to check status.
- `304 Not Modified` for conditional GETs.
- `400` vs `422`: pick one convention for validation failures and stick to it.
- `401` must mean "not authenticated" (include the authentication challenge); `403` means "authenticated, not allowed". Return `404` instead of `403` when revealing existence is itself a leak.
- `409 Conflict` for state conflicts (duplicate unique value, invalid state transition); `412 Precondition Failed` for failed `If-Match`.
- `429 Too Many Requests` with `Retry-After`.
- `503 Service Unavailable` with `Retry-After` for planned or overload unavailability.

### Caching

- Use `Cache-Control` deliberately on GET responses: `no-store` for sensitive data, `private` for per-user data, `public, max-age=...` only for genuinely shared content.
- `ETag` and `Last-Modified` enable conditional requests, saving bandwidth, and double as concurrency tokens for `If-Match` on updates.
- `Vary` must list every request header the response depends on (e.g. `Authorization`, `Accept-Language`), or shared caches may serve the wrong variant.

### URL design details

- Lowercase paths, hyphens or the existing convention for multi-word segments, plural collections.
- Query parameters for filtering, sorting, pagination, and field selection; path segments for identity.
- Keep URLs free of file extensions and verbs for plain CRUD; use content negotiation for formats if you support several.
- Don't put secrets, tokens, or personal data in URLs.

### PATCH semantics

Choose and document one:
- **JSON Merge Patch** (RFC 7396): send the fields to change; `null` deletes. Simple; cannot express "set to null" separately from "remove", and cannot modify individual array items.
- **JSON Patch** (RFC 6902): a list of operations (`add`, `remove`, `replace`, `test`). Precise and supports conditional `test` ops; more verbose.
- **Custom partial update**: absent = unchanged, present = set. Most common in practice; define null handling explicitly.

## GraphQL

### Schema design

- Design the schema around the client's domain graph, not the database. Types are nouns; queries are entry points; mutations are domain actions (`cancelSubscription`, not `updateSubscription(status: CANCELLED)`).
- Use non-null (`!`) deliberately. Non-null fields that fail null out their parent, potentially the whole response; nullable fields are more resilient. Common practice: non-null for IDs and fields that truly always exist, nullable for anything backed by a service that can fail.
- Mutations take a single input object and return a payload type (the changed object plus user-facing errors), which leaves room to evolve both.
- Use connection-style pagination (edges/nodes/pageInfo with cursors) or a simpler cursor pattern consistently for lists that can grow.
- Global object IDs and a node lookup pattern help client caches; follow whatever the client tooling expects.

### Evolution

GraphQL is usually evolved without versions: add fields freely; mark old fields `@deprecated(reason: ...)`; track field usage from query logs; remove only when usage reaches zero. Never change a field's type or meaning in place.

### Performance and safety

- **N+1 resolution**: resolving a list of 100 items, each with a related object, can produce 101 backend queries. Batch and cache per request (the "data loader" pattern).
- **Query cost limits**: depth limits, complexity scoring, maximum list sizes, timeouts. Without them, one query can request an exponentially large graph.
- **Persisted / allow-listed queries** for first-party clients reduce attack surface and enable caching.
- **Authorization in resolvers or a shared layer**, per field where fields differ in sensitivity. Hiding a field from the UI is not authorization.
- **Errors**: distinguish unexpected errors (top-level `errors`) from expected domain outcomes (modelled in the payload type), so clients can handle the latter in a typed way.

## gRPC and protobuf

- **Field numbers are the contract**, not names. Never change or reuse a field number; when removing a field, mark its number and name `reserved`.
- Adding fields is compatible; old clients ignore unknown fields. Changing a field's type is generally not, apart from a few documented wire-compatible changes — check the language guide before relying on one.
- In proto3, scalar fields have no presence by default (zero value is indistinguishable from unset). Use `optional` or wrapper types when "not set" must differ from zero/empty.
- Enums: the first value should be an `UNSPECIFIED = 0` sentinel, because unknown and default values decode to 0.
- Use request and response message types per RPC (`GetInvoiceRequest`/`GetInvoiceResponse`) even if they are small now; it allows evolution without changing method signatures.
- Use deadlines on every call and propagate them across services; use standard status codes consistently (`INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`, `UNAVAILABLE` for retryable, etc.), with structured error details if needed.
- Streaming (server, client, bidirectional) suits large result sets, live updates, and uploads; define flow control and what happens on reconnect.
- Browser clients need a bridge (e.g. a gRPC-web proxy or a transcoding gateway); plan for it if browsers are callers.
- Run a breaking-change checker on `.proto` files in CI if your toolchain offers one.

## Webhooks (events you send to others)

- **Subscription management**: let receivers register URLs and choose event types; provide a way to test and to view recent deliveries.
- **Payload**: event ID, type, creation time, API version, and either the object or a reference to it. Version payloads like any other API.
- **Signing**: sign each delivery (e.g. HMAC-SHA256 over timestamp + body with a per-endpoint secret); include the timestamp; tell receivers to reject old timestamps to prevent replay and to compare signatures in constant time. Support secret rotation with overlapping validity.
- **Delivery**: at-least-once with retries and exponential backoff over hours to days; disable endpoints after sustained failure and notify the owner. Receivers must dedupe by event ID.
- **Ordering**: generally not guaranteed; tell receivers to rely on timestamps or versions, or to fetch the current state.
- **Timeouts**: expect receivers to respond quickly (seconds) with 2xx and process asynchronously; treat slow responses as failures.
- **Safety**: validate subscriber URLs to avoid server-side request forgery into your internal network (block private address ranges, resolve and check at send time).

## Event and message schemas (internal or external)

- Use a schema format with evolution rules (e.g. Avro, protobuf, JSON Schema) and, at scale, a schema registry that checks compatibility on publish.
- Choose a compatibility mode deliberately: backward (new consumers read old data), forward (old consumers read new data), or full. Producers and consumers deploy independently, so you usually need at least forward compatibility for live consumers.
- Keep a topic or stream to one event type or a closely related family; mixing unrelated types complicates consumers and evolution.
- Partition by the entity whose events must stay ordered.
