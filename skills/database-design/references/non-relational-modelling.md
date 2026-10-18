# Modelling for Non-Relational Stores

In relational design you normalise and let the query planner find a path. In most non-relational stores there is no planner to save you: **the schema is shaped by the queries**, and a query you did not design for may be impossible without a full scan. Always start by listing access patterns with their frequency and latency needs.

Product names below are examples, not recommendations; capabilities vary widely between products and versions, so check the specific engine's documentation.

## Document stores

**Core idea**: store an aggregate — the data read and written together — as one document.

- **Embed** when the child data belongs to one parent, is read with the parent, is bounded in size, and is not queried independently (an order's line items, a user's addresses).
- **Reference** (store IDs) when the child is shared by many parents, grows without bound (comments on a popular post), is updated independently and often, or is queried on its own.
- **Bounded growth rule**: never embed an array that can grow without limit; document size limits and rewrite costs will eventually bite.
- **Duplicate selectively**: copying a few fields of a referenced entity (author name on a post) avoids lookups, but you must update copies when the source changes, or accept staleness. Prefer duplicating fields that rarely change.
- **Transactions**: many document stores now offer multi-document transactions, but they are typically more expensive than single-document writes. Model so that most invariants live within one document, where single-document atomicity applies.
- **Validation**: use the store's schema validation features where available; schemaless storage does not mean schemaless data — the application still assumes a shape. Version documents (`schema_version`) so code can handle old shapes during migrations.
- **Indexes**: secondary indexes exist in most document stores; design them for the query patterns just as in relational stores, including compound index order.

## Key-value stores

- Design the **key** as the query: `session:{id}`, `user:{id}:profile`, `rate:{api_key}:{minute}`.
- Use consistent key naming with namespaces, so keys can be inspected, scanned by prefix (if supported), and expired together.
- Set **TTLs** on anything that should expire (sessions, caches, rate-limit windows, idempotency keys).
- Keep values small; large values hurt latency and memory. Store large blobs in object storage and keep a reference.
- Be explicit about durability: some key-value stores are memory-first and may lose recent writes on failure. Do not make them a source of truth unless their persistence configuration guarantees what you need.
- Use atomic operations (increment, compare-and-set, set-if-not-exists) for counters and locks instead of read-modify-write.

## Wide-column stores

**Core idea**: data is grouped by a partition key and sorted by clustering columns within the partition. Queries must specify the partition key.

- **One table per query pattern** is normal. Writing the same data into several tables (each keyed for a different query) is the expected design, not a smell.
- **Partition key** determines distribution and must spread load evenly. **Clustering columns** determine order within a partition and enable range queries ("latest 50 messages in this conversation").
- **Bound partition size**: a partition that grows forever (all events for one device since the beginning) becomes a hotspot and slow. Add a time bucket to the partition key (`(device_id, day)`).
- Avoid patterns the engine handles poorly, often including large numbers of deletes (tombstones), secondary indexes on high-cardinality columns, and read-before-write.
- Use lightweight transactions / conditional writes sparingly; they are much slower than plain writes.

## Graph databases

- Model **entities as nodes** and **relationships as edges** with types and properties; relationships are first-class and traversals are cheap per hop.
- They shine when queries traverse variable-depth relationships (recommendations, fraud rings, network dependencies, access-control graphs) — queries that in SQL need recursive CTEs over large tables.
- They are less suited to bulk aggregation over all nodes, or to simple tabular data with fixed relationships.
- Watch for **supernodes** (a node with millions of edges, like a celebrity or a country), which make traversals through them expensive; model them specially or filter early.
- Many teams keep the source of truth relational and project relationship data into a graph store for specific queries. Recursive queries in a relational engine may be sufficient for modest depth and size; try that first.

## Time-series stores

- Data is (timestamp, series identity, values). **Series identity** is a set of tags/labels (`host`, `region`, `metric`).
- **Cardinality is the main risk**: every distinct combination of tag values is a separate series. Putting unbounded values (user IDs, request IDs, raw URLs) in tags can create millions of series and overwhelm the store. Keep high-cardinality data in fields/values or in a different store.
- Plan **retention and downsampling**: raw data for days or weeks, rolled-up aggregates (per minute, per hour) for months or years.
- Writes are mostly appends; updating or deleting past points is often expensive or unsupported.
- A relational engine with time-based partitioning (or a time-series extension) can serve moderate volumes well and keeps relational joins available.

## Search engines

- A search index is a **derived store**: the source of truth lives elsewhere, and the index must be rebuildable from it. Design the indexing pipeline (change capture or outbox → indexer) and a full reindex path from day one.
- Design the **document shape for search**: denormalise everything needed for matching, filtering, faceting, and display into one document.
- Choose **analysers** (tokenisation, stemming, lowercasing, synonyms) per field and language; they decide what matches. Keep exact-match fields (IDs, codes, enums) as non-analysed keyword fields.
- Changing mappings often requires reindexing; use index aliases so you can build a new index and switch atomically.
- Expect **eventual consistency**: newly written data appears after a refresh interval. Don't use the search index for read-after-write flows.
- Enforce **authorization** in queries (filter by tenant and permissions) — a shared index without filters leaks data across tenants.

## Vector stores and vector indexes

- Store each vector with its **source ID**, the **embedding model and version** that produced it, and the **metadata** needed for filtering (tenant, document type, date, permissions).
- **Embeddings from different models or versions are not comparable**. Changing the model means re-embedding everything; plan for a parallel index and cut-over.
- **Approximate nearest-neighbour indexes** (e.g. graph-based or cluster-based) trade recall for speed; tune parameters against a labelled evaluation set, not by feel. Measure recall at the k you actually use.
- **Filtering**: combining a metadata filter with similarity search can degrade recall or latency depending on whether filtering happens before or after the vector search. Test with your real filter selectivity, especially per-tenant filters.
- **Chunking and what to embed** are retrieval-quality decisions — see `rag-systems`.
- Many relational and document engines now support vector columns and indexes; at moderate scale (up to millions of vectors) this keeps metadata filtering, joins, and transactions in one place. Move to a dedicated vector store when scale, latency, or features demand it.
- Treat vectors derived from sensitive text as sensitive: they can leak information about the source, and deletion obligations apply to them too.

## Columnar analytics stores and warehouses

- Model for **analysis**: wide fact tables of events or transactions with foreign keys to dimension tables (star schema), or wide denormalised tables, depending on the engine and tooling.
- Partition and cluster by the most common filters (date first, almost always).
- Load in batches; avoid many small single-row writes and updates.
- Keep the operational store as the source of truth and load via ETL/ELT (see `etl-pipelines`); do not run the application's transactions against the warehouse.
