# Estimation and Reference Numbers

Back-of-the-envelope estimation exists to rule designs in or out by order of magnitude. Every figure below is approximate and hardware-dependent; treat them as starting points, and prefer measurements from the actual environment whenever you have them. When a decision hinges on a number within a factor of 2–3 of a threshold, measure instead of estimating.

## Handy conversions

- 1 day ≈ 86,400 s ≈ 10^5 s (use 10^5 for mental arithmetic; it overstates rates by ~15%).
- 1 month ≈ 2.6 × 10^6 s. 1 year ≈ 3.15 × 10^7 s.
- 1 M requests/day ≈ 12 requests/s average.
- 1 B requests/day ≈ 12,000 requests/s average.
- Powers of two: 2^10 ≈ 10^3 (KB), 2^20 ≈ 10^6 (MB), 2^30 ≈ 10^9 (GB), 2^40 ≈ 10^12 (TB).

## Latency orders of magnitude

| Operation | Rough latency |
|---|---|
| CPU cache / main memory reference | ~1–100 ns |
| Read 1 MB sequentially from memory | ~tens of µs |
| Round trip within a data centre / zone | ~0.1–0.5 ms |
| Round trip between zones in a region | ~0.5–2 ms |
| SSD random read | ~0.1 ms |
| Read 1 MB sequentially from SSD | ~0.5–1 ms |
| HDD seek | ~5–10 ms |
| Round trip across a continent | ~30–80 ms |
| Round trip intercontinental | ~100–250 ms |
| TLS handshake on a new connection | 1–2 extra round trips |

Implications:
- Memory is ~1,000× faster than SSD random access, which is far faster than a cross-region round trip. Cross-region synchronous calls on a hot path usually blow a tight latency budget on their own.
- Sequential I/O vastly outperforms random I/O; append-only designs exploit this.
- Connection reuse matters: new TLS connections add round trips.

## Rough per-component throughput

Highly variable with payload size, hardware, query complexity, and configuration. Use only to decide "one node or many?".

| Component | Order of magnitude per node |
|---|---|
| Stateless web/API instance, simple handlers | 1,000–10,000s req/s |
| Relational database, simple indexed point reads | 10,000s queries/s |
| Relational database, writes with durable commit | 1,000s–10,000s/s (batching helps a lot) |
| In-memory key-value cache | 100,000s ops/s |
| Partitioned log, per partition | 10,000s–100,000s msgs/s (depending on size) |
| Single-threaded consumer doing a DB write per message | ~100s–1,000s msgs/s |

If an estimate lands within ~5× of a single node's capacity, plan for scaling (replicas, partitioning, batching) or at least a clear path to it.

## Availability arithmetic

| Target | Downtime per month | Per year |
|---|---|---|
| 99% | ~7.3 h | ~3.65 days |
| 99.9% | ~43 min | ~8.8 h |
| 99.95% | ~22 min | ~4.4 h |
| 99.99% | ~4.3 min | ~53 min |
| 99.999% | ~26 s | ~5.3 min |

- **Serial dependencies multiply**: availability ≈ product of each. Five dependencies at 99.9% → ~99.5%.
- **Parallel redundancy**: two independent replicas at 99% each → 1 − (0.01 × 0.01) = 99.99%, *if* failures are independent and failover is automatic and instant. Correlated failures (same zone, same bad deploy, same config) break this assumption — which is why redundancy must span failure domains.
- At 99.99%, there is not enough time for a human to notice and fix a problem; recovery must be automatic.

## Worked capacity estimate (illustrative)

A photo-sharing feature: 10 M daily active users; each views 50 photos and uploads 0.2 photos per day; average photo 2 MB stored, 200 KB thumbnail served in feeds; keep forever; growth 50%/year.

1. **Write rate**: 10 M × 0.2 = 2 M uploads/day ≈ 23/s average. Assume 5× peak → ~120/s.
2. **Read rate**: 10 M × 50 = 500 M views/day ≈ 5,800/s average; peak ~30,000/s.
3. **Read/write ratio**: ~250:1 → optimise reads heavily (CDN, caching).
4. **New storage per day**: 2 M × (2 MB + 200 KB) ≈ 4.4 TB/day → ~1.6 PB/year before replication. Object storage, not a database. Metadata (~1 KB per photo) is 2 GB/day → ~730 GB/year: fits in a relational store with a replica for a while; plan partitioning by owner or photo ID within a couple of years.
5. **Egress bandwidth**: 30,000/s × 200 KB ≈ 6 GB/s at peak. This must come from a CDN; origin servers should see only cache misses.
6. **Upload bandwidth**: 120/s × 2 MB ≈ 240 MB/s at peak — upload directly to object storage with pre-signed URLs rather than through application servers.
7. **Conclusion**: the hard problems are storage cost and edge delivery, not application compute. Metadata writes are trivial. The design should spend its complexity on media storage, CDN caching, and thumbnail generation (async jobs triggered by upload).

## Estimation habits

- Write every assumption down next to the number it produces, so reviewers can challenge the assumption instead of the arithmetic.
- Keep units in every step; most estimation errors are unit errors (bits vs. bytes, per-second vs. per-day, MB vs. MiB is usually irrelevant at this precision but KB vs. MB is not).
- Estimate peak, not just average; size for peak with headroom (commonly 30–50% spare capacity).
- Include replication factor, indexes, and overhead in storage.
- Round aggressively; a design that only works if an estimate is accurate to 20% is too fragile anyway.
