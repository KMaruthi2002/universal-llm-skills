---
name: dashboard-building
description: >-
  Design and build dashboards that people actually use: start from the
  audience and the decisions they make, define every metric precisely, lay out
  by priority, choose filters and drill-downs deliberately, show freshness and
  data quality, keep it fast, and pick the tool (BI platform, notebook app,
  custom code, spreadsheet) by constraint. Use when someone asks for a
  dashboard, KPI view, metrics page, monitoring or reporting screen, executive
  scorecard, an admin analytics page in an app, or wants an existing dashboard
  fixed because it is slow, ignored, cluttered or untrusted — in Looker, Power
  BI, Tableau, Metabase, Superset, Grafana, Streamlit, a web framework or a
  spreadsheet. For single charts see data-visualization; for a one-off answer
  see data-analysis.
metadata:
  category: analysis
  related: data-visualization, data-analysis, sql-and-queries, frontend-development, observability, etl-pipelines, information-architecture, accessible-design
---

# Dashboard Building

A dashboard is a standing answer to recurring questions. Its value is measured by how often it changes what someone does, not by how many charts it contains. Most dashboards fail quietly: they are built from a list of available metrics rather than a list of decisions, nobody trusts the numbers because definitions differ from finance's, they are slow, and within months they are ignored and replaced by another one. Building a good one is mostly about scoping, definitions and maintenance; visual polish is the last 20%.

## Scope

This skill covers dashboards for business metrics, product analytics, operations and executive reporting, built in BI tools or code. Neighbours:

- `data-visualization` — choosing and styling each chart on the dashboard.
- `data-analysis` — answering a one-time question; many dashboard requests are really analysis requests.
- `observability` — system monitoring dashboards and alerting for software services (this skill's principles apply, but that skill covers metrics, logs, traces and SLOs).
- `sql-and-queries` and `etl-pipelines` — building the data models and pipelines underneath.
- `frontend-development` — when the dashboard is a custom web application.
- `information-architecture` — organising many dashboards and navigation between them.

## Core principles

### 1. Design for decisions, not data

Start with who uses the dashboard and what they decide with it: "the support lead decides each morning whether to pull agents onto the backlog queue", "the regional manager decides weekly which stores need a visit". Each element should support one of those decisions. **Why:** a dashboard built from "what data do we have" becomes a data dump; one built from decisions stays small, focused and used.

### 2. A dashboard is only as good as its metric definitions

Every number must have a single, written, agreed definition: the formula, the filters, the grain, the timezone, the source, and the owner. If the dashboard's "active users" differs from the board deck's, people stop trusting both. **Why:** trust is the scarcest resource a dashboard has, and it is lost on the first unexplained discrepancy.

### 3. Hierarchy: the most important thing is the most visible thing

Readers scan top-left first (in left-to-right languages), and many look at only the top of the page. Put the few numbers that answer the primary question there, with context; put diagnostic detail below; put reference tables last or on separate pages. **Why:** a flat grid of equally sized tiles gives no guidance on what matters.

### 4. Numbers need context to mean anything

A tile reading "4,312" is useless. Compared with what? Show a comparison (previous period, same period last year, target, forecast) and direction. Make clear whether up is good. **Why:** context turns a number into a signal the reader can act on.

### 5. Freshness and trust are features

Show when the data was last updated, what period it covers, and any known issues. Fail visibly when the data is stale rather than showing old numbers as current. **Why:** an outdated dashboard that looks current causes worse decisions than no dashboard.

### 6. Fewer, better dashboards

Every dashboard has a maintenance cost: queries break, definitions drift, owners leave. Prefer extending a trusted dashboard to creating a new one, and retire dashboards that nobody opens. **Why:** dashboard sprawl produces contradictory numbers and wastes everyone's time finding the "right" one.

## Process

### Step 1 — Understand audience, decisions and cadence

Interview (or reason about) the users:

- **Who** will use it? Executives, managers, operators, analysts, customers (embedded analytics)? Their data fluency differs widely.
- **What decisions or actions** does it support? What would they do if a number moved?
- **How often** do they look — continuously (operations wall display), daily, weekly, monthly? This sets refresh frequency and the default time window.
- **Where** do they look — desktop, laptop, phone, TV wall, emailed snapshot, embedded in an app?
- **What do they use today?** Spreadsheets, existing reports, asking an analyst? The new dashboard must be better than that, and must reconcile with it.

Classify the dashboard type, because it sets the design:

| Type | Purpose | Design implications |
|---|---|---|
| **Strategic / executive** | Track a few top metrics against targets over weeks and months | Few KPIs, trends and targets, minimal interaction, very high trust bar |
| **Operational** | Monitor current state and act now (queues, incidents, inventory) | Real-time or near-real-time, thresholds and alerts, large readable numbers, exception highlighting |
| **Analytical / exploratory** | Let analysts or managers investigate drivers | Rich filters, drill-downs, segment breakdowns, tolerance for complexity |
| **Tactical / team** | Track a team's or initiative's metrics weekly | Funnel or process views, comparisons to plan, owner-specific |

Trying to serve all four in one dashboard produces something that serves none. Split by audience when necessary.

### Step 2 — Write the questions and metric list

List the specific questions the dashboard answers, in priority order. For each, the metric(s) that answer it. Then cut: if a metric does not support a listed decision, leave it out (it can go in an analytical drill-down or a separate reference page).

A useful pattern for the primary metrics: one or a few **headline metrics** (outcomes the audience owns), a handful of **driver metrics** that explain movements in the headline (inputs, funnel steps, segments), and **health / guardrail metrics** that warn when something is breaking (error rates, data quality, costs).

### Step 3 — Define every metric

For each metric, write down:

- **Name** as users will see it, and plain-language description.
- **Formula**, including numerator and denominator for ratios.
- **Grain and aggregation** (sum, distinct count, average of what).
- **Filters and exclusions** (test accounts, refunds, internal users, cancelled orders).
- **Time semantics** — by event date or processing date, timezone, how partial periods are shown, attribution windows.
- **Source** — table/model and owner.
- **Direction** — is up good, bad, or neither?
- **Targets or thresholds**, and where they come from.

Reuse existing definitions from the organisation's metric layer, semantic model or data dictionary wherever they exist. If you must create a new one, put it in the shared layer (semantic model, metrics store, dbt metric, documented view), not inside a single chart's query, so every consumer uses the same logic.

Reconcile each headline metric to the system of record (finance, billing, CRM) before launch and document any intended differences.

### Step 4 — Model the data underneath

- Build dashboards on curated, documented models (views, tables, semantic layer) rather than raw tables queried ad hoc in each chart. This keeps definitions consistent and queries fast.
- Pre-aggregate to the grain the dashboard needs (daily by region by product, for example) when raw data is large; aggregate tables or materialised views make dashboards fast and cheap.
- Decide the refresh strategy: scheduled extracts, incremental refresh, live queries, streaming. Match it to the cadence — a weekly executive dashboard does not need live queries against production.
- Add data-quality checks upstream (see `data-cleaning-and-validation`) so the dashboard can surface failures.

### Step 5 — Sketch the layout before building

Sketch on paper or a wireframe tool (see `wireframing-and-prototyping`). A layout that tends to work:

1. **Top band:** title, date range and key filters, freshness indicator; then headline KPIs with comparison and trend (e.g., a number, change vs comparison period, small sparkline).
2. **Middle:** the main explanatory charts — trends of headline metrics, breakdowns by the most important dimension, funnel or process view.
3. **Lower:** diagnostic breakdowns, segment comparisons, lists of exceptions needing action (e.g., the stores below target).
4. **Bottom or separate page:** detailed tables, definitions, notes.

Group related items visually and label groups. Align to a grid. Keep a consistent time window across tiles unless clearly labelled otherwise. Make "what needs attention" pop out: highlight exceptions rather than everything.

Get the sketch reviewed by real users before building; changing a sketch costs minutes, changing a built dashboard costs days.

### Step 6 — Build

- Use the chart form that fits each question (see `data-visualization`). Common dashboard elements: KPI tiles with comparisons, time series lines, sorted bars for breakdowns, tables with conditional formatting for lists, bullet charts for actual vs target, heatmaps for hour × day patterns.
- Consistent color semantics across the whole dashboard: one meaning per color. Reserve alert colors (often red/amber) for genuine exceptions; if everything is red, nothing is.
- Consistent number formats, units and time zones across tiles.
- Titles that say what the chart shows, including the time window if not global.
- Tooltips for precise values and definitions, but never hide essential information in them.

### Step 7 — Filters, interactivity and drill-down

- **Few global filters**, placed consistently (usually top). Typical: date range, a primary dimension (region, product, team). More than ~5 filters suggests the dashboard is serving too many audiences.
- **Sensible defaults.** The default view should answer the main question with no clicks. Default to the period matching the cadence (last 7 complete days, last full month).
- **Make filter state obvious.** Users misread dashboards because a filter was set by someone else or persisted from last time. Show active filters clearly and offer a reset.
- **Drill-down paths** should follow the questions users ask next: from a KPI to its trend, to its breakdown by segment, to the list of underlying records. Each level should keep the context (filters) of the previous one.
- **Cross-filtering** (clicking one chart filters others) is powerful for analysts and confusing for casual users; enable it deliberately.
- **Links out** to the detailed analysis, the runbook, the ticket queue — dashboards should lead to action.

### Step 8 — Performance

Slow dashboards are abandoned. Rules of thumb: initial load within a few seconds; filter changes within a couple of seconds. Techniques:

- Pre-aggregate; query summary tables, not event-level data.
- Limit the number of tiles per page (each is usually at least one query).
- Cache results; align cache expiry with data refresh.
- Avoid high-cardinality filters on raw data and unbounded date ranges by default.
- Push computation to the database; avoid pulling raw rows into the BI layer to compute there.
- Index or partition by the common filter columns (date, tenant).
- Measure: most BI tools and web profilers show per-query timings; fix the slowest first.

### Step 9 — Validate, launch and maintain

- **Validate numbers** against the system of record and against the previous report it replaces. Document known, intended differences.
- **Test with users**: can they answer their questions without help? Watch them use it (see `usability-evaluation`).
- **Document** each metric's definition in or linked from the dashboard, plus owner and contact.
- **Monitor usage** (most BI tools report views per dashboard) and data freshness; alert the owner when refreshes fail.
- **Review periodically**: remove unused tiles, update targets, retire dashboards with no viewers.

## Element-level guidance

### KPI tiles

A KPI tile should answer "how are we doing on X?" in a glance. It usually contains: the metric name (as users say it), the current value for a clearly stated period, the comparison (change vs the reference period, target, or both, with the reference named — "vs last week", "vs plan"), a direction cue whose meaning is unambiguous (up is not always good: costs, churn, latency), and optionally a sparkline for recent trend. Avoid:

- Percent change on tiny bases ("+300%" from 2 to 8).
- Comparisons between periods of different lengths or maturity (this partial month vs last full month).
- Colors that only encode direction rather than goodness; an increase in errors should not be green.
- Gauges and dials: they use a lot of space to show one number and a target, which a bullet chart or a number with "of target" shows more compactly.

### Comparisons that make sense

| Cadence | Useful comparisons |
|---|---|
| Real-time / intraday | Same time yesterday, same weekday last week, expected range for this hour |
| Daily | Same weekday last week, trailing 7- or 28-day average |
| Weekly | Previous week, same week last year, target |
| Monthly / quarterly | Plan or forecast, same period last year, year-to-date vs plan |

Week-over-week comparisons in seasonal businesses mislead around holidays; show year-over-year or expected ranges alongside them.

### Exception lists

Tables of items needing action (accounts at risk, stores below target, overdue tickets) are often the most-used part of an operational dashboard. Sort by urgency or impact, show only the columns needed to decide and act, link each row to the system where action happens, and cap the list (top 20) with a link to the full set. An empty list should say so explicitly ("No stores below target this week") rather than showing a blank table that could mean broken data.

### Thresholds and alerts

- Set thresholds from historical variation and business impact, not round numbers. A threshold crossed every other day trains people to ignore it.
- Distinguish warning from critical, and use the same colors for each everywhere.
- Where action is needed outside working hours or faster than people look at dashboards, use an alert (push, email, chat) rather than relying on someone noticing a red tile — and send it to an owner who can act.
- Every alert should say what crossed which threshold, since when, and where to look.

### Empty, loading and error states

Design for the cases where there is no data yet, the query is running, or the data failed to load. Distinguish "zero" from "no data" from "error". A dashboard that shows zeros when the pipeline fails is actively dangerous.

### Text on dashboards

A short description under the title (what this dashboard is for, who owns it), definitions on hover or in a linked glossary, and human-written commentary where numbers need interpretation. Keep text brief, but do not remove the explanation of what a metric means — undefined metrics are the main source of misreading.

### Building in code

When the dashboard is built in code (a data-app framework or custom web app):

- Keep metric logic in a single tested layer (SQL views, a metrics module), not in UI components.
- Cache query results server-side keyed by filter values; invalidate on data refresh.
- Paginate or virtualise large tables.
- Treat permissions server-side; never filter sensitive rows only in the browser.
- Version the dashboard definition in source control, including queries, so changes are reviewable.
- Write tests for metric calculations against small fixtures with known answers.

## Tool choice

Choose by constraint, not preference. Use what the organisation already runs unless it truly cannot meet a requirement.

| Option | Strengths | Weaknesses | Choose when |
|---|---|---|---|
| **BI platform** (e.g., Looker, Power BI, Tableau, Metabase, Superset, Qlik) | Self-serve, semantic layers, permissions, scheduling, sharing, fast to build | Licence cost, limited custom interaction, styling constraints, governance overhead | Internal business reporting, many consumers, need for self-serve and access control |
| **Observability / time-series tools** (e.g., Grafana, Datadog, Kibana) | Real-time metrics, alerting, time-series focus | Weak for relational business data and complex joins | Operational and system monitoring |
| **Notebook / data-app frameworks** (e.g., Streamlit, Dash, Shiny, Evidence, Observable) | Full analytical flexibility in code, version control, custom logic, quick for data teams | Hosting, auth and scaling are on you; less self-serve for non-coders | Analytical tools for internal teams, models and simulations, prototypes |
| **Custom web app** (charting libraries in a web framework) | Total control of UX, embeds into products, brand-consistent | Highest build and maintenance cost; you own performance, permissions and data APIs | Customer-facing analytics, embedded in a product, unusual interactions |
| **Embedded BI** (BI vendor's embedding) | Faster than custom for customer-facing analytics | Licensing per viewer, styling and multitenancy limits | Customer-facing analytics without a large front-end investment |
| **Spreadsheet** | Universal, flexible, no new tools | Fragile, manual refresh, poor access control and scale | Small teams, small data, early prototypes, finance-style models (see `spreadsheet-modeling`) |

Other deciding factors: where the data lives and how the tool connects to it; row-level security and multi-tenant needs; who maintains it after you; export and scheduling needs (emailed PDFs, alerts); cost per viewer; accessibility support; and whether definitions can live in a shared semantic layer.

## Discovering context

- **Find existing dashboards** on the topic. Check usage; find out why the old one is not enough before building another.
- **Find existing metric definitions** — semantic models, metric stores, data catalogue, finance definitions. Reuse them.
- **Find the design conventions** — the BI tool's org theme, the product's design system for embedded dashboards, existing color meanings and number formats.
- **Find the data models** and their refresh schedules; know the upstream latency before promising freshness.
- **Check access rules**: who may see which rows (region, customer, salary data)? Implement row-level security from the start, not as a retrofit. Never expose personal or sensitive data beyond what the audience needs; aggregate or mask where possible.
- **Ask about the display context**: meeting-room screen, laptop, mobile, printed pack, email.

## Special cases

### Executive scorecards

Keep to a handful of metrics with targets, trend and a short commentary field written by a human ("Revenue below plan due to delayed enterprise deals; expected to recover in Q3"). The commentary often matters more than the charts. Ensure numbers match the board pack exactly.

### Operational and wall displays

Large, high-contrast numbers readable from a distance; limited text; clear thresholds; auto-refresh with a visible timestamp; a clear "stale data" state. Exceptions should be noticeable from across the room. Avoid relying on hover or small labels.

### Customer-facing and embedded analytics

Higher bar for performance, correctness, tenant isolation and design consistency with the product. Explain metrics in the customer's language. Handle empty states (new customer, no data yet), loading states and errors gracefully. Test permissions so one tenant can never see another's data.

### Self-serve exploration

Provide a curated, documented data model with clear names, hidden technical columns and pre-defined metrics, so users can build their own views without reinventing definitions. Pair it with a few canonical dashboards that represent the official numbers.

## Pitfalls and anti-patterns

- **The metric zoo**: 40 tiles of everything available. Nobody can find the signal.
- **Vanity metrics**: cumulative totals that always go up, raw counts without rates or context.
- **Definitions in chart queries**: each chart implements "active user" slightly differently.
- **No comparison**: numbers without previous period, target or benchmark.
- **Unmarked partial periods**: today's or this month's incomplete data plotted as if complete, showing a false drop.
- **Mixed time windows** across tiles without labels.
- **Hidden filter state** causing people to read filtered numbers as totals.
- **Alert fatigue**: thresholds so sensitive that everything is red.
- **Unbounded default queries** making every load slow.
- **No owner**: the dashboard silently breaks and keeps showing stale numbers.
- **Building before agreeing**: building the dashboard first and debating definitions later.
- **Building a dashboard for a one-off question**, or a one-off analysis when the question recurs weekly.
- **Copying a dashboard to make a variant**, creating forks that drift apart.
- **Pie charts and gauges** taking space that a number with a trend line would use better.

## Quality bar and verification

- [ ] The audience, the decisions supported and the viewing cadence are written down.
- [ ] Every metric has a written definition (formula, filters, grain, time semantics, source, owner) and reuses shared definitions where they exist.
- [ ] Headline numbers reconcile with the system of record and with any report being replaced; intended differences are documented.
- [ ] The top of the dashboard answers the primary question with no interaction.
- [ ] Every KPI has context: comparison, target or trend, and direction of good.
- [ ] Partial periods are excluded or marked; time windows and timezones are consistent and labelled.
- [ ] Filters are few, defaults are sensible, active filter state is visible and resettable.
- [ ] Drill-down paths follow the users' next questions.
- [ ] Freshness is visible, and stale or failed data is shown as such.
- [ ] Loads and filter changes are fast enough for the use (measured, not assumed).
- [ ] Access control and data sensitivity are handled; row-level security is tested with real user roles.
- [ ] Color semantics and number formats are consistent across the dashboard and with the destination's conventions; it is legible on the target display and accessible (contrast, not color-only, keyboard where interactive).
- [ ] Real users tested it and could answer their questions unaided.
- [ ] An owner, a refresh schedule, a data-quality check and a review date exist.

Before launch, pick three numbers from the dashboard and trace each back to the underlying records by an independent query. If any does not match, do not launch.

## Worked reasoning: "We need a sales dashboard"

1. **Clarify.** Talking to the head of sales: weekly pipeline review with regional managers; they decide which deals to escalate and whether regions need help to hit quarterly targets. Viewed on laptops on Monday mornings, and screen-shared in the meeting.
2. **Type.** Tactical/strategic hybrid; weekly cadence; no need for live data — a daily refresh is ample.
3. **Questions → metrics.** Are we on track for the quarter? (bookings to date vs target, forecast) Where is the gap? (by region) Is the pipeline healthy enough? (pipeline coverage = open pipeline / remaining target, by region) Which deals need attention? (large deals with close dates slipping or stalled for 30+ days).
4. **Definitions.** "Bookings" taken from finance's definition (signed contract value, net of discounts, in the reporting currency at the plan rate). "Pipeline" uses the CRM stages agreed with sales ops; stage probabilities from the existing forecast model.
5. **Layout.** Top: quarter-to-date bookings vs target, forecast, coverage — each with last week's value. Middle: bookings vs target by region (bullet charts, sorted by gap). Lower: table of at-risk deals with owner and link to the CRM record.
6. **Filters.** Quarter and region only. Default: current quarter, all regions.
7. **Validate.** Quarter-to-date bookings match finance's weekly flash within rounding; a manager confirms the at-risk list matches their view of their deals.
8. **Maintain.** Owner: sales ops analyst. Freshness indicator; refresh failure alert; review at quarter end.

Result: one page, eight elements, every one tied to a decision taken in the Monday meeting.
