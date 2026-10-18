---
name: database-design
description: >-
  Choose the right kind of data store and design the data model inside it:
  relational, document, key-value, wide-column, graph, time-series, search,
  and vector stores; entities and relationships; normalization vs.
  denormalization; primary and foreign keys; data types; constraints and
  integrity; indexes for access patterns; multi-tenancy, history, soft
  deletion, and evolution of the model. Use when starting a schema, adding
  tables or collections, picking a database, modelling a new feature's data,
  deciding what to index, fixing integrity problems or duplicated data, or
  reviewing a data model. For writing and tuning queries use sql-and-queries;
  for changing a live schema safely use database-migrations.
metadata:
  category: development
  related: sql-and-queries, database-migrations, system-design, backend-development, software-architecture, data-cleaning-and-validation, performance-optimization, rag-systems
---

# Database Design

Data outlives code. Applications get rewritten; the data model, and the data in it, usually survives. A good design makes **invalid data impossible to store**, makes **the common queries cheap**, and can **evolve without rewriting everything**. A poor one produces bugs that no amount of application code can fully contain, because the store itself lets contradictions in.

## Scope

Covers choosing a store type, conceptual and logical modelling, physical schema (types, keys, constraints, indexes), and design patterns for recurring needs (tenancy, history, soft delete, hierarchies, polymorphism, money, time).

Neighbours:
- Writing correct and efficient queries, reading query plans — `sql-and-queries`.
- Changing a schema that is already in production — `database-migrations`.
- Replication, partitioning, consistency across machines — `system-design`.
- Cleaning or validating existing data — `data-cleaning-and-validation`.
- Vector stores in the context of retrieval systems — `rag-systems`.

## Core principles

### 1. Model the domain truthfully, then optimise for access

First capture what is true about the world: which things exist, what identifies them, how they relate, what rules always hold. Then shape the physical design around how the data is read and written. Skipping the first step leads to models that encode one screen's needs and break with the next feature. Skipping the second leads to elegant models that are too slow.

### 2. Let the database enforce what must always be true

Uniqueness, required values, valid references, allowed ranges, and allowed states are best enforced by the store itself (unique constraints, `NOT NULL`, foreign keys, check constraints, enum or domain types, schema validation in document stores). The "why": application code has many paths — handlers, jobs, scripts, admin consoles, future services, manual fixes — and every one of them will eventually skip a check. A constraint applies to all of them, and under concurrency it is the only check that is reliable.

### 3. Every fact in one place, unless you have a reason

Normalisation exists to avoid update anomalies: if a customer's address is stored in five places, an update will eventually miss one. Store each fact once and derive the rest. Denormalise deliberately, for measured read performance or for history (see below), and know who keeps the copies consistent.

### 4. Design from access patterns, especially for non-relational stores

Write down the queries before the schema: "fetch a user's 20 most recent orders with totals", "find all open tickets assigned to team X ordered by priority", "count events per device per minute". Relational stores tolerate unanticipated queries reasonably well; document, key-value, and wide-column stores often do not — their schema *is* their query plan.

### 5. Choose boring technology unless the problem demands otherwise

A mainstream relational database handles a remarkably wide range of workloads — transactional data, JSON documents, full-text search, geospatial data, moderate time-series, even vector similarity with extensions — with mature tooling, strong integrity, and well-understood operations. Add a specialised store when a measured requirement exceeds what the general one does well, not because the data "looks like" a graph or a document.

### 6. Names and types are part of the contract

Columns and tables are read by many people and tools for years. Clear, consistent names and precise types (not strings for everything) prevent whole classes of bugs and make the model self-documenting.

## Discovering context

Before designing or changing a model:

- **Find the existing schema**: migration files, schema dumps, ORM model definitions, or (with permission) introspect the database's catalog. The migrations history shows how the model evolved and which decisions were deliberate.
- **Learn the conventions**: table naming (singular/plural, case), primary key type and naming, foreign key naming, timestamp columns, soft-delete approach, tenant column, enum handling, index naming. New tables should be indistinguishable in style from existing ones.
- **Identify the engine and version**: features (partial indexes, generated columns, JSON operators, check constraints, deferrable constraints) differ by engine and version.
- **Find the access patterns**: the queries the application runs (repository code, ORM usage, slow-query logs, query statistics views), and their frequency.
- **Learn data volumes and growth**: rows per table, growth per month, largest tenants. Design choices differ for thousands vs. billions of rows.
- **Check retention, privacy, and compliance** requirements for the data: personal data, deletion obligations, audit needs, residency.

## Choosing a store

| Store type | Strong at | Weak at | Choose when |
|---|---|---|---|
| Relational (row store) | Integrity constraints, transactions across entities, flexible ad hoc queries and joins, mature tooling | Horizontal write scaling (without sharding or distributed SQL), very wide sparse records | Default for business data: users, orders, accounts, anything with relationships and invariants |
| Distributed SQL | Relational semantics with horizontal scale and multi-region | Higher latency per transaction, operational and cost complexity | Relational needs that genuinely exceed one primary's capacity or need multi-region writes |
| Document | Hierarchical records read and written as a unit, flexible per-record shape | Cross-document joins and transactions (limited or costly), enforcing references | Self-contained aggregates (a product catalogue entry, a content item, a form submission) with varied shape |
| Key-value | Extremely fast get/put by key, simple scaling | Anything but key lookup; secondary queries | Caches, sessions, feature flags, idempotency keys, counters |
| Wide-column | Massive write throughput, predictable queries by partition key, time-ordered data within a partition | Ad hoc queries, joins, transactions across partitions | Very large-scale event, messaging, or IoT data with known query shapes |
| Graph | Multi-hop relationship traversal with variable depth | Bulk analytics over all data, simple tabular access | Queries like "friends of friends who…", fraud rings, dependency graphs, where traversal depth is variable and central |
| Time-series | High-rate timestamped appends, downsampling, retention, time-window aggregation | Updating past data, relational lookups | Metrics, sensor data, monitoring, financial ticks |
| Search engine | Full-text relevance, faceting, fuzzy matching | Being the source of truth, transactions, strong consistency | Search over text, product search, log exploration — fed from the source of truth |
| Vector store / index | Nearest-neighbour similarity over embeddings | Exact filtering at scale (varies), transactional updates | Semantic search, recommendation, retrieval for LLM applications |
| Columnar analytics warehouse | Aggregations over billions of rows, compression | Single-row lookups and updates, high-rate small transactions | Reporting and analytics, separate from the operational store |

Practical guidance:
- Start with one relational store as the source of truth for most products. Add a cache, a search index, or an analytics warehouse as *derived* stores fed from it.
- **Keep one source of truth per fact.** Derived stores (search, cache, warehouse) can be rebuilt from the source; if they cannot, they have become a second source of truth and need the same care.
- **Polyglot persistence has a cost**: more operations, more failure modes, and synchronisation between stores (see the dual-write discussion in `system-design`).
- Many relational engines offer JSON columns, full-text search, and vector extensions; these often suffice at moderate scale and avoid a second store.

For modelling in document, key-value, wide-column, graph, time-series, and vector stores, read `references/non-relational-modelling.md`.

## Process for relational modelling

### Step 1: Entities, identity, and relationships

List the entities (nouns the business cares about), what uniquely identifies each in the real world (if anything), and the relationships: one-to-one, one-to-many, many-to-many. For each relationship, ask whether it is required, whether it can change over time, and whether its history matters.

### Step 2: Attributes and rules

For each entity, list attributes with their type, whether they are required, allowed values or ranges, and rules that involve several attributes ("`ends_at` after `starts_at`", "exactly one of `user_id` or `team_id`"). These become types and constraints.

### Step 3: Normalise

Aim for third normal form as the default — informally, *every non-key column describes the key, the whole key, and nothing but the key*:
- No repeating groups or lists packed into a column (comma-separated IDs, `phone1`, `phone2`, `phone3`). Use a child table.
- No columns depending on only part of a composite key.
- No columns depending on other non-key columns (storing `country_name` next to `country_code` in every row).

### Step 4: Map access patterns and decide denormalisation

Walk each important query against the model. Where a hot query needs many joins or aggregations over large data and is measured (or confidently estimated) to be too slow, consider: an index first; then a materialised view or summary table; then a denormalised column maintained by the application or a trigger. Document every denormalisation and how it is kept consistent.

### Step 5: Physical design

Choose types, keys, constraints, and indexes (sections below). Name everything per the project's conventions.

### Step 6: Plan evolution

Consider which parts are likely to change (new states, new relationship cardinalities, new tenants) and make those changes additive where you can. Write the schema as migrations (see `database-migrations`).

### Step 7: Review with real or realistic data

Load representative data volumes if you can and run the key queries. Check plans and timings (see `sql-and-queries`).

## Keys

- **Every table has a primary key.** Without one, duplicates creep in and rows cannot be reliably referenced or updated.
- **Surrogate vs. natural keys**: real-world identifiers (emails, tax numbers, product codes) change, get reused, have formatting variants, and are sometimes personal data. Use a surrogate primary key (auto-increment integer, UUID, or similar) for identity, and enforce real-world uniqueness with a separate unique constraint. Natural keys are fine for truly stable codes (ISO currency codes, country codes) and for join tables.
- **Integer vs. UUID-style keys**:
  - Sequential integers are compact and index-friendly, but reveal volumes and creation order, can be enumerated in URLs, and require coordination to generate across systems.
  - Random UUIDs can be generated anywhere and are not guessable, but are larger and scatter inserts across the index (page splits, cache misses) in B-tree-based stores.
  - Time-ordered unique IDs (e.g. UUIDv7, ULID-style, or snowflake-style IDs) combine distributed generation with mostly sequential insertion; a good default for new systems if the engine supports them well.
  - Follow the project's existing choice; mixing key types complicates joins and tooling.
- **Use the right integer width**: a 32-bit key can run out (about 2.1 billion signed); use 64-bit for any table that could grow large. Running out of key space is an outage.
- **Composite keys** suit join tables (`(user_id, group_id)`) and child rows identified within their parent. Keep foreign keys to composite keys manageable.
- **Foreign keys** declare and enforce relationships. Choose the delete behaviour deliberately: `RESTRICT`/`NO ACTION` (default, safest), `CASCADE` (only for true ownership, e.g. order lines with their order), `SET NULL` (optional relationships). Unchecked cascading deletes can remove far more than intended.
- Some large-scale systems drop foreign keys for write performance or because data is sharded across databases; this trades guaranteed integrity for throughput and must be compensated by application checks and periodic consistency jobs. Do not drop them by default.

## Data types

- **Use the most specific type**: dates as date types, instants as timestamp-with-time-zone (or UTC-normalised timestamps, per engine semantics), booleans as booleans, fixed-precision decimals or integer minor units for money, UUID types for UUIDs, enums or reference tables for closed sets, JSON types (not text) for JSON.
- **Never use binary floating point for money** or other values that need exact decimal arithmetic.
- **Strings**: decide on length limits where the domain has them; be aware of collation (case sensitivity, accent sensitivity) for uniqueness and sorting — "Alice@x.com" and "alice@x.com" may or may not be the same user depending on collation. Normalise (e.g. lowercase emails) or use a case-insensitive type or index.
- **Enums**: a native enum type is compact but adding/removing values is a schema change (and removing is often hard); a check constraint on a text column is easier to change; a reference table allows metadata (labels, ordering, active flags) and foreign-key enforcement. Choose by how often the set changes and whether values carry data.
- **NULL means "unknown or not applicable"**, and it has three-valued logic consequences in queries (see `sql-and-queries`). Make columns `NOT NULL` unless absence is meaningful. Avoid using magic values (`''`, `0`, `1900-01-01`) to mean "missing".
- **JSON columns** are useful for genuinely schemaless, rarely-queried, or externally-defined payloads (webhook bodies, user preferences, sparse attributes). They are a poor substitute for columns you filter, join, or constrain on regularly — you lose type checking, constraints, and usually statistics. If a JSON field becomes important, promote it to a column.

## Constraints and integrity

Use, in roughly this order of value:
1. `NOT NULL` on every column that must have a value.
2. Primary keys and unique constraints (including composite and, where supported, partial unique constraints such as "one active subscription per user").
3. Foreign keys.
4. Check constraints for ranges, formats, and cross-column rules (`quantity > 0`, `ends_at > starts_at`, "exactly one of these columns is set").
5. Exclusion constraints, where supported, for non-overlap rules (no two bookings for the same room overlap in time).
6. Triggers, sparingly, for invariants that cannot be expressed declaratively — they are hidden logic, so document them.

Translate constraint violations into meaningful application errors rather than treating them as server failures.

## Indexes

Indexes make reads faster and writes slower, and they consume storage and memory. Index for the queries you actually run.

- **Primary key and unique constraints** create indexes automatically in most engines.
- **Foreign key columns** usually need an index (many engines do not create one automatically); without it, joins and parent deletes scan the child table.
- **Composite indexes** follow the left-prefix rule: an index on `(tenant_id, status, created_at)` serves filters on `tenant_id`, on `tenant_id + status`, and on all three, plus ordering by `created_at` within them — but not a filter on `status` alone. Order columns by: equality filters first, then range filters or sort columns. Among equality columns, order to maximise reuse across queries.
- **Covering indexes** (including extra columns so the query never touches the table) can eliminate lookups for hot read paths.
- **Partial / filtered indexes** index only rows matching a condition (`WHERE deleted_at IS NULL`, `WHERE status = 'open'`), keeping them small and fast for the common query.
- **Expression indexes** for queries on computed values (`lower(email)`).
- **Specialised index types**: inverted/GIN-style for JSON containment, arrays, and full-text; GiST/spatial for ranges and geometry; BRIN-style for huge append-only tables ordered by time; vector indexes for similarity search.
- **Selectivity matters**: an index on a column with few distinct values (a boolean) rarely helps on its own, except as part of a composite or partial index.
- **Don't index everything**: each index slows inserts and updates and must be maintained. Find unused indexes via the engine's statistics and remove them (after confirming they are not used by rare but important jobs).

Verify index usage with the query plan, not intuition (see `sql-and-queries`).

## Recurring design patterns

### Multi-tenancy

| Approach | Isolation | Cost / complexity | Fits |
|---|---|---|---|
| Shared tables with a `tenant_id` column | Logical only — every query must filter | Cheapest; one schema to migrate | Many small tenants; SaaS default |
| Schema per tenant | Stronger; per-tenant backup/restore easier | Migrations run per schema; catalog bloat with many tenants | Tens to low thousands of tenants with isolation needs |
| Database per tenant | Strongest; per-tenant scaling and residency | Highest operational cost | Few large tenants, strict compliance, residency |

With shared tables: put `tenant_id` on every tenant-owned table (including child tables, so queries need not join to find the tenant), lead composite indexes and unique constraints with it (`UNIQUE (tenant_id, email)`), and consider database-enforced row-level security as a safety net.

### History and auditing

- **Audit log table**: who changed what, when, with old and new values. Append-only. Good for compliance and debugging.
- **Effective dating / temporal tables**: rows with `valid_from` / `valid_to` to answer "what was the price on date X?". Some engines offer system-versioned temporal tables.
- **Snapshots on the transaction**: an order stores the price, tax rate, and address *as they were at purchase*. This is denormalisation done for correctness — the order must not change when the product price changes later.
- **Event sourcing**: store events as the source of truth; see `software-architecture` for when it is warranted.

### Soft deletion

A `deleted_at` column keeps data recoverable and preserves references, but every query must exclude deleted rows (easy to forget), unique constraints must account for them (use partial unique indexes on non-deleted rows), and it can conflict with legal obligations to actually erase personal data. Alternatives: move deleted rows to an archive table, or hard-delete with an audit record. Choose per table, based on recovery needs and privacy obligations.

### Hierarchies and trees

| Technique | Read subtree | Move subtree | Notes |
|---|---|---|---|
| Adjacency list (`parent_id`) | Recursive query | Cheap | Simplest; recursive CTEs make reads feasible |
| Materialised path (`/1/4/9/`) | Prefix match, fast | Rewrite descendants' paths | Good for read-heavy, shallow-ish trees |
| Closure table (ancestor, descendant, depth) | Fast join | Many row changes | Flexible queries; more storage |
| Nested sets | Fast range query | Expensive | Rarely worth it for trees that change |

### Polymorphic relationships

When a comment can belong to a post, a photo, or a video:
- **Separate foreign key columns** (`post_id`, `photo_id`, `video_id`) with a check that exactly one is set — keeps foreign keys enforceable. Good for a small, stable set.
- **Separate join tables per parent type** — clean and enforceable.
- **A shared parent table** (all commentable things have a row in `commentables`) — enforceable, more joins.
- **Generic `(parent_type, parent_id)`** columns — flexible, but the database cannot enforce the reference. Common in ORMs; accept the integrity risk knowingly.

### Many-to-many with attributes

A join table often turns out to be an entity in its own right (a `membership` with role and joined date). Give it its own attributes, constraints, and possibly its own surrogate key.

### Status and lifecycle

Model status as a constrained set, with timestamps for key transitions (`submitted_at`, `approved_at`), and consider a status history table if transitions must be audited. Avoid multiple booleans (`is_paid`, `is_shipped`, `is_cancelled`) that can contradict each other.

### Money, quantities, and units

Store amount in integer minor units or a fixed decimal, plus a currency code column. Store units explicitly when quantities can be in different units. Never mix currencies in one column without a currency column next to it.

## Normalisation vs. denormalisation: deciding

Denormalise when **all** of these hold:
- A specific, important query is measurably too slow, and indexing or query rewriting does not fix it.
- The data is read far more often than it is changed.
- There is a clear, single mechanism to keep the copy consistent (same transaction, trigger, or a rebuildable derived table), and staleness, if any, is acceptable.

Prefer, in order: better indexes → rewriting the query → materialised views or summary tables refreshed on a schedule → denormalised columns maintained transactionally → separate read models.

Distinguish denormalisation for **performance** (a copy that must stay in sync) from snapshots for **correctness** (a copy that must *not* change, like the price on an invoice). The second is not a compromise; it is the correct model.

## Naming

- Follow the existing schema's conventions exactly; where there are none, choose one scheme and apply it everywhere: singular or plural table names, one case style, `id` or `<table>_id` for keys, `<referenced>_id` for foreign keys, `_at` for instants and `_on` or `_date` for dates, `is_`/`has_` for booleans.
- Name constraints and indexes explicitly and predictably (e.g. including table and columns), so error messages and migrations are readable and portable across environments.
- Avoid reserved words, abbreviations only the author understands, and names that encode a current UI label likely to change.
- Name for meaning, not type: `shipped_at`, not `date2`; `amount_minor` plus `currency`, not `value`.

## Worked reasoning example

*Illustrative.* Model room bookings for a co-working product with several locations, where a room cannot be double-booked, prices change over time, and customers are businesses with several members.

1. **Entities**: organisation (tenant), member, location, room, booking, price list. Membership links members to organisations with a role — a join table that is an entity.
2. **Identity**: surrogate keys everywhere; `UNIQUE (organisation_id, email)` for members, because the same person may belong to two organisations with the same email.
3. **The key invariant** — no overlapping bookings per room — cannot be enforced by a plain unique constraint. Where the engine supports exclusion constraints over ranges, use one on `(room_id, time_range)` for non-cancelled bookings. Otherwise, serialise booking creation per room (lock the room row) and check overlap inside the transaction. Application-only checks would race.
4. **Price history**: prices change, but a booking must keep the price it was sold at. Store `price_minor` and `currency` on the booking (a correctness snapshot) and keep effective-dated price lists for future quotes.
5. **Status**: `booking.status` constrained to `confirmed | cancelled | completed`, with `cancelled_at` and a check that it is set iff status is cancelled.
6. **Access patterns**: "room availability for a day" → index on `(room_id, starts_at)`; "an organisation's upcoming bookings" → `(organisation_id, starts_at)`. Booking rows carry `organisation_id` directly so tenant-scoped queries don't need joins.
7. **Retention**: completed bookings kept for invoicing obligations; member personal data anonymised on account deletion while bookings remain for accounting.

The design pushed the critical invariant into the database and separated "price at time of sale" from "current price", which removes two of the most common bug sources in booking systems.

## Pitfalls

- **No constraints**, relying on application code for uniqueness and references; duplicates and orphans accumulate.
- **Entity-attribute-value tables** (`entity_id, attribute_name, value`) used to avoid schema design: no types, no constraints, painful queries. Use JSON columns or real columns instead, unless you truly need user-defined attributes at scale.
- **Lists in columns** (comma-separated IDs) — cannot be indexed, joined, or constrained.
- **One giant "god table"** with hundreds of nullable columns for different kinds of things.
- **Strings for everything**: dates as text, numbers as text, booleans as `'Y'/'N'`.
- **Floats for money.**
- **Timestamps without time zone semantics**, mixed local and UTC values.
- **Missing indexes on foreign keys**, or indexes on everything.
- **Natural keys as primary keys** that later change (emails, usernames).
- **32-bit keys** on tables that grow without bound.
- **Unbounded growth** of logs, events, and sessions without a retention or partitioning plan.
- **Designing a document or wide-column schema like a relational one**, then discovering the queries you need are impossible without scans.
- **Adding a second database** for a feature the primary handles adequately.
- **Storing secrets or sensitive personal data in plain text** — passwords must be hashed with a password-hashing function, and sensitive fields considered for encryption, masking, or separate storage with tighter access.

## Safety

- Never run schema changes, data fixes, or index builds against a production database without the user's explicit approval, a backup or rollback path, and an understanding of locking impact (some operations lock tables for their duration). See `database-migrations`.
- Inspect production data only with appropriate access and minimise copying personal data elsewhere.
- Design for privacy obligations: know which columns hold personal data, how they will be deleted or anonymised on request, and how long they are retained.

## Quality bar and verification

Before calling a data model done:

- [ ] Each entity has a primary key; real-world identifiers have unique constraints; key types match project conventions and won't overflow.
- [ ] Every rule that must always hold is enforced by a constraint where the engine allows it; the rest are documented with where they are enforced.
- [ ] Columns use precise types; no floats for money; time zone semantics are clear; `NOT NULL` is the default.
- [ ] The model is normalised, and every denormalisation is documented with its consistency mechanism.
- [ ] The important queries were written against the model, and each has a supporting index (verified with a query plan on realistic data if possible).
- [ ] Foreign key columns are indexed where joins or parent deletes need it.
- [ ] Tenancy, soft delete, history, and retention decisions are explicit.
- [ ] Naming and style match the existing schema.
- [ ] The change is expressed as migrations that are safe to run on the existing data (see `database-migrations`).
- [ ] Personal and sensitive data is identified, with protection and deletion addressed.

If you validated with real data or plans, say so; if only by reasoning, say that too and list the queries the user should check.

## Depth on demand

- `references/non-relational-modelling.md` — modelling for document, key-value, wide-column, graph, time-series, search, and vector stores. Read when the chosen store is not relational, or when evaluating whether a non-relational store fits.
