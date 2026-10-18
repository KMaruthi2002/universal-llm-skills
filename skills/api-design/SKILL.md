---
name: api-design
description: >-
  Design interfaces between software components that are easy to use correctly,
  hard to misuse, and safe to evolve: REST/HTTP, GraphQL, gRPC and other RPC,
  and event/message contracts. Covers resource and operation modelling,
  naming, request/response shapes, errors, pagination, filtering, idempotency,
  concurrency control, authentication and authorization at the API surface,
  rate limiting, versioning, backward compatibility, deprecation, and
  machine-readable specs (OpenAPI, protobuf, GraphQL SDL, AsyncAPI as
  examples). Use when creating or changing an endpoint, schema, or message
  format, reviewing an API proposal, choosing between API styles, planning a
  breaking change, or writing an API spec. For consuming third-party APIs use
  api-integrations-and-webhooks; for implementing handlers use
  backend-development.
metadata:
  category: development
  related: backend-development, system-design, software-architecture, authentication-and-authorization, error-handling, code-documentation, api-integrations-and-webhooks, secure-coding, mcp-server-development
---

# API Design

An API is a promise. Once someone depends on it, every name, field, status code, and quirk becomes something you have to keep working. Good API design is therefore mostly about two things: **making the right usage obvious to the caller**, and **leaving room to change without breaking them**.

## Scope

Covers designing the contract of an interface: HTTP/REST-style APIs, GraphQL schemas, gRPC and other RPC services, and asynchronous event or message schemas. Applies to public APIs, partner APIs, and internal service-to-service APIs (internal APIs deserve the same care; "we can just update the callers" stops being true faster than expected).

Not covered here:
- Implementing the handlers, validation, and data access — `backend-development`.
- Calling and integrating someone else's API, webhooks — `api-integrations-and-webhooks`.
- Detailed authentication and authorization mechanisms — `authentication-and-authorization`.
- Library/function-level API design within one codebase is touched on, but its structure is mostly `software-architecture`.
- MCP tool and resource design — `mcp-server-development` (the principles here still apply).

## Core principles

### 1. Design from the caller's use cases, not your data model

An API that mirrors internal tables forces callers to understand your storage and makes every schema change a breaking change. Start from what callers need to accomplish: "list a customer's unpaid invoices", "cancel a subscription at period end". Model resources and operations around those tasks. Internal structure can then change freely behind the contract.

### 2. Consistency beats cleverness

Callers learn an API's patterns once and apply them everywhere. One endpoint that paginates differently, names IDs differently, or reports errors in another shape costs every caller time and bugs. Pick conventions — naming, casing, pagination, errors, timestamps, IDs — and apply them uniformly. In an existing API, the existing conventions win over your preferences.

### 3. Make correct use easy and incorrect use hard

- Required things are required; optional things have safe defaults.
- Dangerous operations are explicit (a `DELETE` or a clearly named `cancel` action, never a side effect of an innocuous-looking update).
- Types are precise: enums instead of free strings, structured money (amount in minor units plus currency) instead of floats, timestamps with time zones.
- Names say what things are. `expires_at` beats `exp`; `amount_cents` or a typed money object beats `amount`.

### 4. Every addition is forever; additions are cheap, removals are expensive

You can add optional fields, new endpoints, and new enum values (if clients were told to expect them) without breaking anyone. You cannot remove, rename, retype, or change the meaning of anything without a migration. So: **start small**. Expose the minimum that serves the known use cases. It is easy to add a field later and nearly impossible to remove one.

### 5. Assume the network fails and callers retry

Requests time out after the server has acted. Clients retry. Messages arrive twice or out of order. An API that is unsafe to retry will cause duplicate charges, duplicate emails, and duplicate orders. Design idempotency in from the start (see below).

### 6. The contract is the spec, not the implementation

Write the contract down in a machine-readable form when the ecosystem supports one (e.g. OpenAPI for HTTP, protobuf for gRPC, SDL for GraphQL, AsyncAPI or JSON Schema for events). A spec enables review before code, generated clients and docs, contract tests, and breaking-change detection. Whether the spec is written first or generated from code is a team choice; what matters is that it is accurate and reviewed.

## Discovering existing conventions

Before designing anything in an existing system:

1. **Find existing APIs and specs**: spec files, generated clients, route definitions, schema files, API docs, gateway configuration.
2. **Extract the conventions** actually in use: URL structure, casing (`snake_case` vs `camelCase` in payloads), ID format, timestamp format, pagination style, error envelope, auth scheme, versioning scheme, how list filters are expressed.
3. **Look for a style guide** or linting rules for specs (many organisations publish one; spec linters often encode it).
4. **Check who consumes the API**: web front end, mobile apps (which cannot be force-upgraded — old versions live for years), partners, internal services. Consumer type sets how conservative you must be about change.
5. **Follow what you find.** If existing conventions are inconsistent, follow the most common or most recent pattern and note the inconsistency rather than introducing a third variant.

## Process

1. **List the use cases** with the caller: who calls, what they are trying to do, how often, with what latency and data-volume expectations.
2. **Choose the style** (see decision table) — usually already decided by the existing system.
3. **Model the resources or operations**: nouns, their relationships, their lifecycle states, and the transitions between states.
4. **Define the shapes**: request and response bodies, field names and types, required vs. optional, nullability, enums.
5. **Define behaviour at the edges**: errors, pagination, filtering and sorting, limits, idempotency, concurrency, partial failure.
6. **Define security**: authentication, per-operation authorization, which fields are sensitive, rate limits.
7. **Write the spec and examples**, including error examples.
8. **Review against the checklist** at the end, ideally with an actual consumer, and by writing a short piece of client code against the spec.
9. **Plan evolution**: what is likely to change, and how it can change compatibly.

## Choosing a style

| Style | Strengths | Weaknesses | Choose when |
|---|---|---|---|
| REST-style HTTP + JSON | Universal tooling, caching via HTTP semantics, easy to explore and debug, works everywhere | Over/under-fetching for complex UIs; verbs can be awkward for non-CRUD operations | Public and partner APIs, CRUD-heavy domains, broad client diversity |
| GraphQL | Clients fetch exactly the shape they need in one round trip; strongly typed schema; good for many UI variants | Harder HTTP caching; query cost control needed; authorization per field; N+1 risk on server | Many clients with differing data needs over a rich graph of related data, usually first-party UIs |
| gRPC / protobuf RPC | Compact binary, fast, strongly typed, streaming, codegen in many languages | Less browser-friendly (needs a proxy/bridge), harder to inspect manually | Internal service-to-service calls, low latency, polyglot back ends, streaming |
| JSON-RPC or simple RPC over HTTP | Simple, action-oriented | Fewer shared conventions; caching and semantics are up to you | Action-heavy internal APIs, tool/agent interfaces |
| Events / messages (pub-sub, streams) | Decouples producers from consumers in time and availability; multiple consumers | Eventual consistency; harder to trace; schema evolution must be managed carefully | Notifying others that something happened; async workflows; integration between systems |
| Webhooks | Push notifications to external parties over HTTP | Delivery, retries, security (signatures) and ordering are your problem | Telling external integrators about events in your system |

Mixing is normal: REST for the public surface, gRPC internally, events for integration.

## Modelling resources and operations

- **Resources are nouns** with stable identity: `customers`, `invoices`, `invoices/{id}/line-items`. Use plural collection names consistently.
- **Nest only for true containment**, and rarely more than one level deep. `/customers/{id}/invoices` is fine for "invoices of this customer"; deep nesting like `/a/{id}/b/{id}/c/{id}` makes URLs brittle. Provide top-level access by ID when the child has global identity.
- **Model state transitions explicitly.** For a domain action that is not simple field editing (cancel, approve, refund, publish), prefer either an action sub-resource (`POST /orders/{id}/cancel`) or creating a resource that represents the action (`POST /refunds`). Letting callers `PATCH status: "cancelled"` hides business rules, side effects, and validation behind a field write.
- **Long-running operations** return quickly with an operation resource (`202 Accepted` plus a status URL, or an operation ID) that callers poll or are notified about. Do not hold connections open for minutes.
- **Bulk operations**: if callers need to act on many items, provide a batch endpoint with per-item results rather than forcing thousands of calls. Define whether the batch is atomic (all-or-nothing) or partial, and report per-item outcomes either way.
- **IDs**: opaque strings to the caller, even if numeric inside. Opaque IDs let you change generation schemes and avoid callers doing arithmetic on them. Avoid sequential IDs in public APIs where enumeration is a risk; prefixed IDs (`inv_...`) help humans and logs.

## Shapes and naming

- **One casing convention** for fields across the whole API.
- **Timestamps**: an unambiguous format with time zone (e.g. RFC 3339 / ISO 8601 in UTC). Name them for what they mean: `created_at`, `cancelled_at`, `expires_at`.
- **Money**: integer minor units plus currency code, or a decimal string plus currency. Never binary floating point.
- **Enums**: strings, not integers, so they are readable. Document that new values may be added and clients must handle unknown values.
- **Booleans**: name positively (`is_active`, not `is_not_disabled`). If a boolean is likely to grow a third state, use an enum from the start.
- **Null vs. absent**: define the meaning. Commonly: absent = not provided / unchanged (in PATCH), `null` = explicitly cleared. Be consistent.
- **Envelopes**: decide whether responses are bare resources or wrapped (`{ "data": ..., "meta": ... }`). Wrapping lists is valuable because it leaves room for pagination metadata; wrapping single resources is optional. Be consistent.
- **Expansion**: if callers often need related objects, consider an `expand`/`include` parameter rather than always embedding (which bloats responses) or never embedding (which forces many calls).
- **Response for writes**: return the resulting resource from create and update; it saves a round trip and shows server-computed fields.

## Errors

Errors are part of the contract and the part callers most often handle badly because the API was vague.

- **Use the transport's status semantics correctly** (for HTTP): 400 malformed/invalid input, 401 not authenticated, 403 authenticated but not allowed, 404 not found (also used to avoid revealing existence of resources the caller may not see), 409 conflict with current state, 412 precondition failed (version mismatch), 422 semantically invalid (if your convention distinguishes it from 400), 429 rate limited, 5xx server-side failures. gRPC has its own status codes with similar categories; map consistently.
- **One error body shape everywhere**, containing at least: a stable machine-readable code (`card_declined`, `insufficient_funds`), a human-readable message for developers, and where relevant the field(s) at fault. A standard such as RFC 9457 "problem details" is one option.
- **Codes are the contract, messages are not.** Callers branch on codes; messages can be reworded. Document the codes each operation can return.
- **Validation errors** list every invalid field at once, not just the first, so clients can show all problems in one pass.
- **Say whether to retry.** Distinguish transient (retry with backoff; include `Retry-After` when known) from permanent errors.
- **Never leak internals**: no stack traces, SQL, internal hostnames, or messages that reveal whether an account exists (for login and password-reset flows). Log details server-side with a correlation ID and return the ID to the caller.

## Pagination, filtering, sorting

Any list that can grow must be paginated from day one; adding pagination later is a breaking change.

| Method | How | Good for | Problems |
|---|---|---|---|
| Offset/limit | `?offset=200&limit=50` | Small, stable datasets; jump to page N | Slow on large offsets (database scans skipped rows); items shift when data changes, causing duplicates or gaps |
| Cursor (keyset) | Opaque cursor encoding the last item's sort key | Large or changing datasets, infinite scroll, sync | No random page access; cursor must encode sort key and tie-breaker |
| Page token from server | Server returns `next_page_token` | Same as cursor; hides mechanism | Same as cursor |

Default to cursor-based pagination for anything that may become large. Rules:
- Make cursors **opaque** to the caller so you can change their encoding.
- Sort must be **deterministic**: include a unique tie-breaker (usually ID) in the sort key.
- Enforce a **maximum page size**, and a sensible default.
- Total counts are expensive on large tables; make them optional or approximate.
- **Filtering**: explicit, documented parameters (`?status=open&created_after=...`) are safer than a general query language. If you need a query language, constrain it and cost-limit it.
- **Sorting**: allow only indexed sort fields; arbitrary sorting on large datasets is a performance and denial-of-service risk.

## Idempotency and concurrency

- **Safe and idempotent methods**: in HTTP, `GET`, `HEAD`, `PUT`, `DELETE` are defined as idempotent; `POST` and `PATCH` generally are not. Honour these semantics — intermediaries and clients rely on them.
- **Idempotency keys** for non-idempotent creates and actions with side effects (payments, orders, messages): the client sends a unique key (e.g. an `Idempotency-Key` header); the server stores the key with the result and returns the same result for repeats within a retention window. Reject a reused key with a different payload. This is what makes retries safe.
- **Optimistic concurrency** for updates: return a version (an ETag or `version` field); require it on update (`If-Match` or a body field); reject with 409/412 when stale. This prevents lost updates when two clients edit the same resource.
- **Events**: include a unique event ID and a per-entity sequence or version so consumers can deduplicate and detect out-of-order delivery.

## Security at the API surface

- **Authenticate every request** unless the endpoint is deliberately public. Use standard mechanisms (e.g. OAuth 2.0 / OIDC bearer tokens, mutual TLS between services, signed requests); details in `authentication-and-authorization`.
- **Authorize per operation and per object.** The most common API vulnerability is broken object-level authorization: `GET /invoices/123` returns invoice 123 to anyone authenticated. Every handler must check that the caller may access *that specific* object.
- **Do not over-expose fields.** Response shapes should be explicit allow-lists, not serialised internal objects, which leak fields (password hashes, internal flags) as soon as they are added to the model.
- **Prevent mass assignment.** Request bodies should accept only the fields callers may set; ignore or reject `role`, `owner_id`, `is_admin` and the like.
- **Validate input strictly**: types, ranges, lengths, formats, sizes. Cap request body size and list lengths.
- **Rate-limit and quota** per client; return 429 with retry information. Rate limiting protects availability and slows credential-stuffing and scraping.
- **Secrets never in URLs** (URLs end up in logs, browser history, and referrer headers). Credentials and tokens go in headers.
- **Webhooks you send**: sign payloads (e.g. an HMAC with a per-subscriber secret and a timestamp to prevent replay), and tell receivers how to verify.
- **GraphQL specifics**: limit query depth and complexity, disable or protect introspection in public production if your threat model requires it, and authorize at the field/resolver level.

## Versioning and backward compatibility

### What breaks callers

Breaking changes include: removing or renaming a field, endpoint, or enum value; changing a field's type or format; making an optional input required; adding a required input; changing default behaviour; changing error codes or status codes for an existing situation; tightening validation; changing the meaning of a value; changing pagination or ordering guarantees.

Usually compatible: adding an optional input; adding an output field; adding a new endpoint or operation; adding an enum value *if* clients were told to tolerate unknown values; loosening validation (with care).

Note "usually": a client that deserialises strictly and rejects unknown fields will break on an added field. Document from the start that clients must ignore unknown fields and handle unknown enum values; this is what makes additive change safe.

### Versioning strategies

| Strategy | Example | Notes |
|---|---|---|
| URL path major version | `/v1/...` | Visible and simple; encourages big-bang versions |
| Header or media-type version | `Accept: application/vnd.example.v2+json` | Keeps URLs stable; less visible |
| Date-based versions pinned per client | `API-Version: 2024-06-01` | Allows many small breaking changes with per-client upgrade; needs a compatibility layer server-side |
| Schema evolution without versions | protobuf field numbers, GraphQL field deprecation | Never reuse field numbers or names; deprecate and add new instead |

Whatever the strategy: avoid breaking changes whenever an additive alternative exists (add `full_name` alongside `name` rather than changing `name`). Reserve new major versions for changes that cannot be made additively.

### Deprecation

Announce, mark in the spec and docs, signal at runtime where possible (e.g. `Deprecation` and `Sunset` headers, warnings in responses or logs), measure usage of the deprecated element, contact remaining users, and only remove after usage is zero or the published sunset date has passed. Mobile and partner clients need long windows — months to years.

## Events and messages

- Name events in the past tense for things that happened (`order.placed`, `invoice.paid`), distinct from commands (`PlaceOrder`).
- Include an event ID, type, schema version, timestamp, the entity ID, and a correlation/causation ID for tracing.
- Decide between **thin events** (IDs only; consumers fetch current state) and **fat events** (full state snapshot). Thin events avoid stale data and coupling to the full schema but cost a fetch; fat events are self-contained but expose more contract surface.
- Treat event schemas like any other API: versioned, documented, evolved additively, with a registry or spec where possible.
- Document delivery guarantees (usually at-least-once), ordering guarantees (usually per key only), and retention.

## Cross-cutting conventions worth deciding once

Settle these for the whole API early; changing them later touches every endpoint:

- **Request and correlation IDs**: accept a client-supplied request ID or generate one, return it in a response header, and include it in error bodies, so support conversations can find the exact request in logs.
- **Partial responses / field selection**: whether callers can ask for a subset of fields (`?fields=id,name`). Useful for bandwidth-sensitive clients; adds testing surface.
- **Localisation**: whether human-readable messages are localised (via `Accept-Language`) or always in one language with codes for clients to localise. Codes-plus-client-localisation is usually more robust.
- **Metadata and extension fields**: a free-form `metadata` map on key resources lets integrators attach their own IDs without you adding fields; cap its size and never use it for anything you authorise on.
- **Soft-deleted and archived resources**: whether they appear in lists, return 404, or return with a status. Pick one behaviour.
- **Empty values**: empty list `[]` rather than `null` or omission for collections, so clients need not null-check.
- **Ordering guarantees** of every list, documented, even if only "by creation time, newest first".
- **Sandbox and test modes**: separate credentials or environments that behave like production without real side effects (no real charges, no real emails), so integrators can test safely.

## Designing for different consumers

How conservative to be depends on who calls the API and how quickly they can change:

| Consumer | Upgrade speed | Implications |
|---|---|---|
| Your own web front end, deployed with the back end | Minutes to days | Can evolve fast, but old browser tabs and cached bundles still call old shapes for a while — keep compatibility across at least one deploy |
| Your own mobile apps | Months to years (users don't update) | Treat as external: additive change only, long deprecation, server-driven feature flags |
| Internal services owned by other teams | Weeks | Contract tests between producer and consumer; announce changes; avoid lockstep deploys |
| Partners and public developers | Months to years | Formal versioning, changelogs, deprecation policy, sandbox environments, generous sunset windows |
| LLM agents and automated tools | Varies | Very explicit names and descriptions, strict validation with helpful error messages, small focused operations, idempotency (agents retry), conservative defaults for destructive actions |

A backend-for-frontend (a thin API tailored to one client) can absorb UI-specific churn and keep the core API stable; it is worth it when several clients with different needs share one core.

## Rate limits and quotas

- Decide the unit (per API key, per user, per IP, per tenant) and the window (per second for burst, per day for quota).
- Tell callers where they stand: return remaining allowance and reset time in headers on every response, not just on 429, so well-behaved clients can pace themselves. Follow the project's or an emerging standard header scheme consistently.
- Apply stricter limits to expensive or abuse-prone operations (login, search, exports, sending messages).
- Make limits part of the documented contract; changing them downward is effectively a breaking change for heavy users.

## Long-running and asynchronous operations

When an operation can take longer than a normal request timeout (exports, video processing, provisioning):

1. Accept the request, validate it synchronously, and return immediately with an operation identifier and a status location.
2. Model the operation as a resource with states (`pending`, `running`, `succeeded`, `failed`, maybe `cancelled`), progress if meaningful, the result or a link to it on success, and a structured error on failure.
3. Let callers poll with sensible guidance (`Retry-After`), and optionally subscribe to a webhook or event on completion.
4. Make the initiating request idempotent, so a retry after a timeout does not start a second job.
5. Define retention: how long completed operation records and results remain available.

## Worked reasoning example

*Illustrative.* A team wants an endpoint to let customers "update their subscription". The first draft is `PATCH /subscriptions/{id}` accepting any field, including `status`, `plan_id`, and `price`.

Reasoning:
1. Use cases, once listed, are distinct actions: change plan (with proration), cancel at period end, cancel immediately, pause, resume. Each has different rules, side effects (invoices, emails), and permissions.
2. Exposing `price` lets a caller set their own price — a mass-assignment vulnerability. `status` writes bypass the cancellation rules.
3. Better: keep `PATCH` for genuinely free-form fields (e.g. a billing email or metadata), and add explicit actions: `POST /subscriptions/{id}/cancel` with `{ "at": "period_end" | "now" }`, `POST /subscriptions/{id}/plan-changes` returning the proration preview and result, and pause/resume actions.
4. Each action is idempotent with an idempotency key, returns the updated subscription, and documents its error codes (`already_cancelled`, `plan_not_available`, `payment_method_required`).
5. Status values are an enum documented as extensible, so adding `paused` later is not a break.

The contract got slightly larger, but every operation now carries its rules, is safe to retry, and cannot be misused to bypass billing.

## Documentation and specs

Good API documentation contains, for each operation: purpose, auth requirements, parameters with types and constraints, request and response examples, every error code it can return and why, rate limits, and idempotency behaviour. Beyond reference docs, callers need a short getting-started path and explanations of cross-cutting concepts (pagination, errors, versioning, webhooks). Examples must be real and tested — stale examples are worse than none. See `code-documentation` and `technical-writing`.

## Pitfalls and anti-patterns

- **Database-shaped APIs**: exposing tables and columns one-to-one, so every schema change breaks clients.
- **Chatty APIs**: a screen needs 20 calls to render. Provide expansion, composite endpoints for real use cases, or a query layer.
- **Inconsistent conventions** across endpoints (pagination, casing, errors, IDs).
- **Verbs in REST paths for plain CRUD** (`/getUser`, `/createOrder`), or the opposite — forcing a real domain action into a field update.
- **200 OK with an error body**, which breaks every client, proxy, and monitor that relies on status codes.
- **Unpaginated lists** that work in development and time out in production.
- **No idempotency** on payment-like operations.
- **Leaking internals** in errors or responses; serialising whole model objects.
- **Missing object-level authorization checks.**
- **Silent breaking changes**, including "small" ones like tightening validation or changing a default.
- **Booleans that become tri-state**, strings that should be enums, floats for money, timestamps without zones.
- **Premature generality**: a generic "query anything" endpoint that is impossible to secure, optimise, or evolve.
- **Versioning everything** at the first small change instead of evolving additively.

## Quality bar and verification

Before declaring an API design done:

- [ ] Each operation maps to a named caller use case; nothing is exposed "just in case".
- [ ] Conventions (casing, IDs, timestamps, money, pagination, errors, envelopes) match the rest of the API.
- [ ] Every list operation is paginated with a maximum page size and deterministic order.
- [ ] Every non-idempotent operation with side effects supports idempotency keys or is otherwise safe to retry.
- [ ] Updates that can race have optimistic concurrency control.
- [ ] Every operation documents its auth requirement and the authorization rule, including object-level checks.
- [ ] Request bodies accept only fields the caller may set; responses expose only intended fields.
- [ ] Every operation documents its error codes; error bodies share one shape; no internals leak.
- [ ] The spec is machine-readable where the ecosystem allows, validates with a linter if one is available, and matches the implementation (run contract tests or compare generated output if you can).
- [ ] Changes to an existing API have been checked against the breaking-change list; if a breaking-change detector for the spec format is available, run it against the previous version.
- [ ] You (or a consumer) wrote a small client against the spec and the common use cases were straightforward.
- [ ] Deprecations have a timeline and a way to measure remaining usage.

If you could not run linters or contract tests, say so and list what the user should run.

## Depth on demand

- `references/style-specifics.md` — style-specific guidance: HTTP method and status semantics, caching headers, GraphQL schema design and N+1, gRPC/protobuf evolution rules, and webhook delivery design. Read when working in that particular style.
