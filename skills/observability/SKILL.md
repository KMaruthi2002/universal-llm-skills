---
name: observability
description: >-
  Instrument and monitor software so its behaviour in production can be
  understood and acted on: structured logging, metrics, distributed tracing
  (e.g. OpenTelemetry), what to instrument, SLIs, SLOs and error budgets,
  dashboards, alerting that pages on user-facing symptoms rather than causes,
  cardinality, sampling, retention, and observability cost. Use when someone
  asks to add logging, metrics, or tracing, set up monitoring or dashboards,
  define SLOs, reduce alert noise or pager fatigue, figure out why they could
  not see a problem coming, or cut a logging/monitoring bill. Not for
  handling a live outage (see incident-response) or for one-off debugging of
  a known bug (see debugging).
metadata:
  category: devops
  related: incident-response, debugging, performance-optimization, error-handling, postmortem, kubernetes, cloud-architecture, dashboard-building
---

# Observability

Observability is the ability to answer new questions about a running system from the outside, using the telemetry it emits, without shipping new code to ask them. Monitoring tells you *that* something is wrong; observability lets you find out *why*, including for failure modes no one predicted. In practice it rests on three main signals — logs, metrics, traces — tied together by shared context, plus the discipline of defining what "working" means (SLOs) and alerting only when users are hurt or soon will be.

Tools are named as examples: OpenTelemetry for instrumentation; Prometheus, Grafana, Datadog, New Relic, Honeycomb, Elastic, Splunk, Loki, Tempo, Jaeger, and cloud-native suites (CloudWatch, Cloud Monitoring/Logging, Azure Monitor) as backends.

## Scope

Covers: instrumentation strategy, logs, metrics, traces, correlation, SLIs/SLOs/error budgets, alerting design, dashboards, cardinality, sampling, retention, cost, and privacy in telemetry.

Hands off to:

- Responding to a live outage → `incident-response`.
- Finding the cause of a specific bug → `debugging`; of a systemic failure → `root-cause-analysis`.
- Improving speed once measured → `performance-optimization`.
- Building BI-style dashboards for business data → `dashboard-building`.

## Core principles

**1. Start from questions, not tools.** What do on-call engineers need to know at 3 a.m.? Is the service up for users? Which users, which endpoints, since when, after which change? Instrument to answer those. Collecting everything "in case" produces a huge bill and still misses context.

**2. Alert on symptoms, investigate with causes.** Users experience symptoms: errors, slowness, unavailability, wrong results. Causes (high CPU, a full disk, a restarted pod) may or may not hurt users. Page on symptoms; use cause-level signals on dashboards and in investigation. This is the single most effective way to reduce alert fatigue without missing incidents.

**3. Every alert must be actionable and urgent, or it is not a page.** If the response to an alert is "look, shrug, and wait", it trains people to ignore pages. Non-urgent signals become tickets or dashboard items.

**4. Context is what makes telemetry useful.** A log line saying "payment failed" is weak; one with request ID, trace ID, user/tenant identifier (where allowed), endpoint, version, region, and error class is strong. Consistent attribute names across services make correlation possible.

**5. Cardinality is the cost and performance limit.** Every unique combination of metric labels is a separate time series. Unbounded labels (user IDs, request IDs, full URLs, timestamps) explode storage and query cost. High-cardinality detail belongs in logs and traces; metrics carry low-cardinality aggregates.

**6. Reliability targets are business decisions.** 100% is the wrong target for almost everything: it is unachievable, and the pursuit freezes change. SLOs make the acceptable level of unreliability explicit, and error budgets turn it into a tool for balancing speed and stability.

**7. Telemetry is data, with privacy and security obligations.** Logs and traces routinely capture personal data, tokens, and secrets by accident. Scrub at the source.

## Discovering context first

1. **What exists already?** Logging library and format, metrics library and naming conventions, tracing setup (OpenTelemetry SDKs, vendor agents), collectors (OpenTelemetry Collector, Fluent Bit, Vector, vendor agents), backends, dashboards, alert rules (often in IaC or a monitoring repo), on-call tool (e.g. PagerDuty, Opsgenie, incident.io).
2. **Conventions:** field names (e.g. `trace_id` vs `traceId`), log levels policy, metric naming (`http_server_request_duration_seconds` style vs vendor conventions), OpenTelemetry semantic conventions adoption, required tags (service, env, version).
3. **Who consumes it:** on-call rotation size and how often they get paged, support teams, product analytics (which should usually be a separate pipeline).
4. **Constraints:** budget for telemetry, retention requirements (security/audit logs often require long retention; debug logs do not), data residency, PII policies.
5. **Pain points:** recent incidents that were detected late or diagnosed slowly are the best guide to what is missing.

Extend the existing stack; introducing a second logging format or metrics library in one codebase fragments queries.

## The three signals, and when to use each

| Signal | Best for | Strength | Weakness | Cost driver |
|---|---|---|---|---|
| Metrics | Trends, rates, alerting, SLOs, capacity | Cheap to store and query at scale; fast | Low detail; no per-request context | Number of time series (cardinality) |
| Logs | Discrete events, errors with detail, audit | Arbitrary detail | Expensive at volume; hard to aggregate unless structured | Bytes ingested and retained |
| Traces | Request flow across services, latency breakdown | Shows where time goes and causal paths | Requires propagation everywhere; sampling needed at scale | Spans ingested |

Other useful signals: continuous profiling (CPU/memory hot spots in production), real-user monitoring (browser/mobile performance), synthetic checks (scripted probes from outside), and events (deploys, config changes, feature-flag flips) overlaid on graphs — the last is cheap and enormously helpful, since many incidents start with a change.

## What to instrument

### For every service

- **The four golden signals** for each externally facing operation: **latency** (distribution, split by success and failure), **traffic** (request rate), **errors** (rate and ratio, by class), **saturation** (how full the constrained resource is: CPU, memory, connection pools, queue depth, thread pools).
- Request-level structured logs or traces for errors and slow requests, with correlation IDs.
- Version/build info as a metric or attribute, so regressions can be tied to deploys.
- Dependency calls (databases, caches, other services, third-party APIs): latency, errors, timeouts, retries — as client-side metrics and child spans.
- Health of internal resources: pool usage, queue lengths, cache hit ratio, GC pauses, event-loop lag (for single-threaded runtimes).

### Method shortcuts

- **RED** (Rate, Errors, Duration) for request-driven services.
- **USE** (Utilisation, Saturation, Errors) for resources (CPU, disks, network, pools).

### For asynchronous and batch work

- Queue depth and age of oldest message (age is often the better alerting signal, as it captures user-visible delay).
- Processing rate, failure rate, retries, dead-letter counts.
- For scheduled jobs: last successful run timestamp, duration, records processed. Alert on "no success in N hours", which catches jobs that silently stop running (see `scheduled-jobs`).

### Business-level signals

A handful of business metrics (orders placed, sign-ups, messages delivered) catch failures that technical metrics miss — a bug that returns 200 OK with an empty cart shows as a drop in orders, not an error spike.

## Structured logging

- Emit logs as structured events (JSON or the platform's structured format), one event per line, to stdout/stderr in containers; let the platform ship them.
- Include consistently: timestamp (UTC, ISO 8601 or epoch with precision), level, service, environment, version, message, trace ID and span ID, request ID, and relevant domain identifiers.
- Messages describe events; fields carry data. Prefer `{"msg":"payment declined","reason":"insufficient_funds","amount_cents":1250}` over interpolating everything into the message string, which prevents filtering and aggregation.
- **Levels:** ERROR for failures needing attention (and only those — a validation error caused by a user typo is not an ERROR); WARN for unexpected but handled situations; INFO for significant lifecycle events (startup, config loaded, job completed); DEBUG for detail usually disabled in production. Inconsistent levels make severity filtering useless.
- Log once at the boundary where an error is handled, with full context, rather than at every layer it passes through (see `error-handling`). Duplicate logs inflate cost and confuse counts.
- Avoid logging inside hot loops or per item in large batches; aggregate.
- **Never log secrets, tokens, passwords, full card numbers, or session cookies.** Redact or hash identifiers per policy. Be careful with logging whole request/response bodies or headers (Authorization headers end up in logs this way). Use allow-lists of fields rather than deny-lists where feasible.
- Make log level adjustable at runtime or per component for debugging, with automatic reversion.

## Metrics

- Use counters for things that only increase (requests, errors), gauges for current values (queue depth, memory), histograms for distributions (latency, payload size). Prefer histograms for latency so you can compute percentiles across instances; averaging precomputed percentiles across instances is mathematically wrong.
- Choose histogram buckets around your SLO thresholds (e.g. if the SLO is 300 ms, have buckets at 250, 300, 400 ms) so the SLI can be computed accurately. Native/exponential histograms where the backend supports them reduce this tuning.
- **Label discipline:** labels should be bounded and low-cardinality: service, endpoint *route template* (`/users/{id}`, not `/users/48213`), method, status class or code, region, version. A useful check: series ≈ product of label value counts; keep it in the hundreds or thousands per metric, not millions.
- Name metrics with units and consistent conventions (follow the backend's or OpenTelemetry's semantic conventions).
- Record rates and ratios at query time from counters, not by exporting pre-computed rates.

## Distributed tracing

- Use a standard (OpenTelemetry, W3C Trace Context headers) so traces propagate across languages, proxies, and vendors.
- Auto-instrumentation for frameworks and clients gets most of the value quickly: inbound HTTP/gRPC, outbound calls, database queries, message publish/consume. Add manual spans for significant internal operations and attributes for domain context.
- **Propagation must not break:** every hop — load balancers, gateways, queues, async workers, thread pools — must pass the context along. A trace that stops at the queue is the most common gap. For messaging, put trace context in message headers/attributes and link consumer spans to producer spans.
- **Sampling:**
  - Head sampling (decide at the start, e.g. 1–10%) is cheap but discards most error traces at low rates.
  - Tail sampling (decide after the trace completes, in a collector) keeps all errors and slow traces plus a sample of normal ones. More infrastructure (collector must buffer traces), much more useful.
  - Low-traffic services can often keep 100%.
- Put trace IDs in logs and expose them in error responses (as a support reference) so a user report leads straight to the trace.

## SLIs, SLOs, and error budgets

**SLI (service level indicator):** a measurement of user experience, usually a ratio of good events to valid events. Examples:

- Availability: proportion of requests that succeed (non-5xx, excluding client errors), measured at the load balancer or edge, ideally close to the user.
- Latency: proportion of requests faster than a threshold (e.g. < 300 ms) — expressed as a proportion, not an average.
- Freshness (data pipelines): proportion of time data is newer than N minutes.
- Correctness: proportion of outputs validated as correct (by sampling or checksums).
- For async processing: proportion of messages processed within N seconds of enqueue.

**SLO (objective):** target for an SLI over a window, e.g. "99.9% of checkout requests succeed over 28 days", "99% of search requests complete under 400 ms".

**Error budget:** 1 − SLO. At 99.9% over 30 days, the budget is about 43 minutes of full outage or the equivalent in partial failures (0.1% of requests).

Setting SLOs:

1. Pick the few user journeys that matter (sign in, search, checkout, API calls by customers). Two to five SLOs per service is plenty.
2. Measure current performance for a few weeks before committing to a number. An SLO above what the system achieves today will be violated immediately; one far below it is meaningless.
3. Choose the target with the business: what level of failure do users notice and tolerate? Each extra nine costs roughly an order of magnitude more effort.
4. Remember dependencies: a service cannot be more available than the product of its hard dependencies' availability unless it degrades gracefully without them.
5. Agree what happens when the budget is exhausted (e.g. prioritise reliability work, slow risky launches). An SLO with no policy attached is decoration.
6. Review SLOs quarterly; adjust as the product and users change.

Formal SLAs (contracts with penalties) should be looser than internal SLOs, so the SLO is breached and acted on well before the SLA is.

### Error budget arithmetic, worked

Suppose checkout has an SLO of 99.9% success over 30 days and serves 10 million requests in that window.

- Budget: 0.1% of 10 million = 10,000 failed requests allowed.
- A burn rate of 1 spends exactly the budget over 30 days (an error ratio of 0.1%).
- An incident producing a 2% error ratio burns at 20× (2% / 0.1%). At that rate the whole monthly budget is gone in 30 days / 20 = 1.5 days, and 1 hour consumes about 2.8% of it — fast enough to page.
- A steady 0.15% error ratio burns at 1.5×: no page, but it exhausts the budget in 20 days, which a slow-burn ticket alert should catch.

Doing this arithmetic with real traffic numbers makes it clear which alert windows and thresholds make sense, and helps explain the alerts to the people who will be paged by them.

| SLO | Allowed downtime per 30 days (full outage equivalent) |
|---|---|
| 99% | ~7.2 hours |
| 99.5% | ~3.6 hours |
| 99.9% | ~43 minutes |
| 99.95% | ~22 minutes |
| 99.99% | ~4.3 minutes |

## Alerting

### What should page

Page when users are being hurt now, or will be soon enough that a human must act before business hours:

- **SLO burn-rate alerts:** alert when the error budget is being consumed fast. A common multi-window, multi-burn-rate approach for a 30-day SLO:
  - Page: burn rate ≥ 14.4 over 1 hour (and ≥ 14.4 over 5 minutes to confirm it is still happening) — spends ~2% of the monthly budget in an hour.
  - Page: burn rate ≥ 6 over 6 hours (with a 30-minute confirmation window) — ~5% of the budget in 6 hours.
  - Ticket: burn rate ≥ 1 over 3 days — slow leak.
  These thresholds are a widely used starting point; tune to your traffic and tolerance.
- **Hard symptoms** not covered by SLOs: synthetic check failing from multiple locations, zero traffic where traffic is expected, data pipeline staleness beyond tolerance, certificate expiry within days.
- **Imminent saturation** that will cause user impact with near certainty and no automatic remediation: disk will be full within hours on a database, queue age growing unbounded.

### What should not page

- Single-host CPU or memory spikes, pod restarts, individual instance failures handled by redundancy. Dashboard or ticket them.
- Warnings that resolve themselves (flapping). Add duration conditions (`for: 5m`) and hysteresis.
- Anything without a clear owner or runbook.

### Good alert hygiene

- Every alert has: a clear name stating the symptom, severity, the affected service and scope, a link to a dashboard pre-filtered to the problem, and a runbook link with first steps.
- Route alerts to the team that owns the service; deduplicate and group related alerts so one incident produces one page.
- Measure the pager: pages per on-call shift, percentage actionable, time to acknowledge. Common targets: fewer than about two pages per on-call shift on average, and the large majority actionable. Review alert quality regularly and delete or demote alerts that never lead to action.
- Low-traffic services make ratio alerts noisy (one failure out of three requests is 33%). Require a minimum request count, use longer windows, or add synthetic traffic.
- Test alerts: verify they fire (inject a failure in staging, or use the backend's rule-testing tools) and that notifications reach the right people.

## Dashboards

- Design top-down: a service overview first (SLOs and golden signals, current vs. recent baseline, deploy markers), then drill-down dashboards per dependency or component.
- Every graph should answer a question someone actually asks. Remove graphs no one looks at.
- Show percentiles (p50, p95, p99) and error ratios, not only averages; averages hide tail latency that users feel.
- Use consistent time ranges and units; label axes; show thresholds/SLO lines.
- Keep dashboards in code (JSON/YAML in git, or IaC providers for the monitoring tool) so they are reviewed and recoverable.
- A dashboard is not an alert. Nobody watches dashboards continuously; anything requiring attention must alert.

## Cost and retention

Observability bills can rival compute bills. Control them deliberately:

- **Logs:** drop or sample high-volume low-value logs (health check access logs, debug output) at the collector; keep error logs. Tier retention: hot searchable storage for days to weeks, cheap archive (object storage) for longer compliance needs.
- **Metrics:** control cardinality; remove unused metrics (many backends can report which series are never queried); be wary of auto-instrumentation that emits per-path or per-pod series multiplied by many labels.
- **Traces:** tail sampling; keep errors and slow traces; shorter retention.
- **Per-team attribution:** label telemetry with service/team so cost can be attributed and owners can act.
- Estimate before enabling: events per second × bytes per event × retention, or series count × scrape interval. A single verbose log line in a hot path at 5,000 requests/second is over 400 million lines a day.

## Privacy and security

- Scrub PII and secrets at the source (logging libraries' redaction hooks, collector processors), not just in the backend; data that reaches a third-party backend has already left your control.
- Restrict access to logs containing sensitive data; audit access where required.
- Respect data residency for telemetry backends and their retention.
- Security/audit logs (authentication events, admin actions, permission changes) need integrity protection and retention per policy, often separate from operational logs.
- Treat dashboards and alert messages that go to chat tools as potentially widely visible; keep sensitive values out of them.

## Process: instrumenting a service from little or nothing

1. Identify the critical user journeys and the service's dependencies.
2. Add or confirm structured logging with request/trace IDs and consistent fields.
3. Add RED metrics for inbound operations and dependency calls (auto-instrumentation first).
4. Add tracing with propagation across every hop, including async.
5. Emit deploy events and version info.
6. Build an overview dashboard; check it against a recent real incident or a staged failure — could you have seen and diagnosed it?
7. Measure baseline SLIs for a few weeks, then set SLOs and burn-rate alerts with runbooks.
8. Prune: remove noisy logs, unused metrics, and non-actionable alerts. Revisit after each incident.

## Decision guidance: pipeline and backend

| Choice | Option A | Option B | Decide by |
|---|---|---|---|
| Instrumentation | OpenTelemetry SDKs and collector | Vendor agent/SDK | OTel keeps you portable across backends and is now broadly supported; vendor agents can offer deeper auto-instrumentation and less setup. Many teams use OTel for traces/metrics and keep vendor agents only where they add unique value |
| Collection | Direct export from apps | Collector/agent tier (sidecar, node agent, or gateway) | A collector centralises sampling, scrubbing, batching, routing, and retries, and lets you switch backends without redeploying apps. Use it at anything beyond small scale |
| Backend | Self-hosted open source (e.g. Prometheus + Grafana + Loki + Tempo) | Managed/SaaS | Self-hosting trades licence cost for engineering time and on-call for the monitoring itself; SaaS trades money for convenience and usually scales cost with volume. Make sure the monitoring system does not fail at the same time as what it monitors |
| Metrics model | Pull (scraping) | Push (OTLP, StatsD) | Pull gives automatic "target down" detection and is natural in Kubernetes; push suits short-lived jobs, serverless, and networks where scraping is hard |

Whatever the stack, the monitoring of last resort (synthetic checks, "is the alerting pipeline alive" heartbeats) should run independently of the primary infrastructure, so an outage of the platform does not also silence the alerts about it.

## Clients: browsers and mobile apps

Server-side telemetry misses everything that happens on users' devices: slow rendering, JavaScript errors, crashes, failed network calls that never reached the server.

- Real-user monitoring (RUM) for web: Core Web Vitals, page load and interaction timings, JS errors, with release version attached.
- Mobile: crash reporting with symbolication, app start time, network error rates, ANR/hang detection, segmented by app version and OS (old versions linger for months).
- Propagate trace context from client to server where possible so a slow user action can be followed into the backend.
- Sample and scrub aggressively: client telemetry volume scales with users, and it is easy to capture form contents or personal data.

## Worked example: from 40 pages a week to 4

Situation: a team gets around 40 pages a week; most auto-resolve; on-call engineers have started muting their phones overnight. Two real outages last quarter were noticed by customers first.

Analysis of a month of alert history: 60% of pages are host-level CPU, memory, or pod-restart alerts that never correlated with user impact; 25% are an error-ratio alert on a low-traffic admin endpoint where a single failure crosses the threshold; the remainder are genuine. Both missed outages were a dependency returning HTTP 200 with empty results, invisible to error-rate alerts, and a regional DNS problem invisible from inside the network.

Changes:

- Demote cause-level alerts to dashboards and tickets.
- Define SLOs for the three key journeys from measured baselines, with multi-window burn-rate paging.
- Add a minimum-request-count condition to ratio alerts for low-traffic endpoints.
- Add a business-level alert on a sudden drop in completed orders compared with the same hour last week.
- Add external synthetic checks from several regions.
- Attach runbook and dashboard links to every remaining page; review page quality every two weeks.

Result after a month: about four pages a week, nearly all actionable, and a staged dependency failure and a simulated DNS failure both page within minutes.

The reasoning to copy: use alert history as data, page on what users feel, and add signals specifically for the failure modes that slipped through.

## Pitfalls and anti-patterns

- **Paging on causes** (CPU > 80%, a pod restarted) → alert fatigue and ignored pages.
- **No alert on absence:** dashboards look green because the metric stopped reporting. Alert when expected data is missing.
- **Averages everywhere,** hiding a p99 that is ten times worse.
- **Unbounded label values** (user IDs, raw URLs) → cardinality explosion and huge bills.
- **Unstructured logs** that need regexes to query, with inconsistent formats across services.
- **Broken trace propagation** at queues or proxies, giving fragmentary traces.
- **Logging secrets or personal data,** often via full request/response dumps.
- **SLOs set without measuring,** or set at 100%, or with no budget policy.
- **Monitoring only from inside:** everything is green internally while DNS, certificates, or the CDN are broken. Add external synthetic checks.
- **Dashboard sprawl:** hundreds of unowned dashboards nobody trusts.
- **Treating observability as a project** finished once, instead of something improved after each incident.

## Safety notes

- Changes to alert routing or silencing can hide real incidents. Confirm with the user before deleting alerts, muting, or changing on-call routing, and prefer demoting (page → ticket) over deleting while gathering evidence.
- Never add instrumentation that logs credentials or personal data; if you find such logging, flag it and recommend scrubbing plus rotation of any exposed secrets.
- Enabling new telemetry at scale can cost real money quickly; estimate volume and tell the user before turning on verbose logging, full tracing, or high-cardinality metrics in production.

## Verification

- [ ] For a sample request, you can go from an error log to its trace, and from the trace to the logs of every service involved.
- [ ] Golden-signal metrics exist for each critical operation and dependency, with bounded labels (estimate series counts).
- [ ] Dashboards show SLOs, percentiles, error ratios, and deploy markers; they reveal a staged failure quickly.
- [ ] Each paging alert is symptom-based, has a runbook and dashboard link, and was tested to fire and route correctly.
- [ ] Alert on missing data exists for critical signals.
- [ ] No secrets or disallowed personal data in a sample of logs and spans.
- [ ] Telemetry volume and cost estimated; retention configured per data type.
- [ ] SLOs reflect measured baselines and have an agreed error-budget policy.

Report what is now instrumented, the SLOs and alerts in place, expected telemetry volume/cost, and remaining gaps (e.g. "async worker traces not yet linked to producers").
