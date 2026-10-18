---
name: data-cleaning-and-validation
description: >-
  Profile, clean and validate data so it can be trusted: establish types and
  grain, handle missing values, duplicates and outliers, catch joins that
  multiply rows, fix encoding and unicode problems, normalise dates, timezones
  and units, write validation rules and data contracts, and document every
  transformation reproducibly. Use when data is messy, imported from CSV,
  Excel, APIs or scraped sources, numbers don't reconcile, a join produces too
  many rows, someone asks to "clean", "dedupe", "validate", "standardise" or
  "check the quality of" a dataset, or before any analysis on unfamiliar data.
  Works in SQL, pandas, R, spreadsheets or pipeline tools. Not for building
  scheduled pipelines (etl-pipelines) or schema design (database-design).
metadata:
  category: analysis
  related: data-analysis, etl-pipelines, sql-and-queries, statistical-analysis, text-processing-and-regex, database-design, spreadsheet-modeling
---

# Data Cleaning and Validation

Cleaning is the work of turning data as it arrived into data that means what everyone assumes it means. Validation is the work of proving it, and of making sure it stays that way. Together they decide whether every downstream number is right. They are unglamorous, they take most of the time in real analytical work, and when skipped they produce results that are confidently wrong.

## Scope

This skill covers profiling, cleaning decisions, validation rules, data contracts and transformation documentation, for one-off datasets and for data feeding recurring work. Neighbours:

- `etl-pipelines` — scheduling, orchestration, incremental loads and pipeline operations; this skill supplies the checks those pipelines should run.
- `database-design` — designing schemas and constraints that prevent bad data at the source.
- `text-processing-and-regex` — detailed pattern-matching and text normalisation.
- `data-analysis` and `statistical-analysis` — what to do with the data once it is trustworthy.
- `spreadsheet-modeling` — when the data lives in and is maintained in a spreadsheet.

## Core principles

### 1. Never modify the raw data

Keep the original input untouched and read-only. Every cleaning step produces a new derived version through code. **Why:** cleaning decisions are often wrong the first time, and you will need to revisit them. If raw data is overwritten, a mistake becomes permanent and unauditable.

### 2. Every transformation is a decision; record it

Dropping a row, imputing a value, merging two customer records, converting a currency — each changes the answer. Record what was done, why, and how many records it affected. **Why:** someone (often you, later) will ask why the numbers differ from the source system. The log of transformations is the answer, and it is also how errors get found.

### 3. Profile before you clean

Do not start fixing things you have not measured. Profile every column first: type, nulls, distinct values, ranges, patterns. **Why:** the obvious problem is rarely the only one, and fixing one problem in isolation can hide another (e.g., coercing invalid dates to null makes a parsing bug look like missing data).

### 4. Fix at the source when you can

A cleaning step downstream is a workaround that must be repeated forever and will drift. If the producer can fix it (form validation, a tracking bug, an export setting), report it to them. Clean locally only as a bridge, and say so.

### 5. Distinguish errors from surprises

An outlier, a null or an odd category may be a data error, or it may be the most important true fact in the dataset. The same value — an order of $250,000 — is an error in a consumer shop and a normal day in a B2B wholesaler. Investigate before deciding. **Why:** "cleaning" real but inconvenient values is a way of making the data agree with your expectations.

### 6. Validation is executable, not a one-time look

Write checks as code that runs every time the data is refreshed and fails loudly. **Why:** data that was clean last month will not necessarily be clean next month; producers change things without telling consumers.

## Process

### Step 1 — Establish what the data is supposed to be

Before looking at values, find out:

- **The grain.** One row per what? What uniquely identifies a row?
- **The producer.** Which system, form, API or person generated it, and how?
- **The expected schema.** Column names, types, allowed values, units, required fields — from documentation, API specs, source code or the owner.
- **The expected volume.** Roughly how many rows per day/week? What is the expected relationship to other tables?
- **Known issues.** Ask owners, read issue trackers, check prior analyses.

Write the expectations down. Profiling then becomes a comparison of expectation against reality, which is far more effective than staring at values.

### Step 2 — Profile

For each column, collect:

| Measure | What it reveals |
|---|---|
| Declared vs inferred type | Numbers stored as text, dates as strings, IDs read as numbers (losing leading zeros) |
| Null / empty / whitespace-only count | Missingness — and the many disguises it wears |
| Distinct count and top values with frequencies | Categorical noise, defaults, placeholders (`N/A`, `-`, `unknown`, `0`, `1900-01-01`, `999999`) |
| Min, max, percentiles | Impossible values, unit errors, sentinel values |
| String length distribution, character patterns | Truncation, mixed formats, encoding damage |
| Row counts over time | Gaps, spikes, partial loads, backfills |

For the table as a whole: row count, primary-key uniqueness, duplicate full rows, and relationships (foreign-key match rates to related tables).

Tools: SQL `GROUP BY` / `COUNT(DISTINCT)` queries; pandas `describe`, `value_counts`, `isna().sum()`; R `summary`, `skimr`; profiling libraries (e.g., ydata-profiling); BI tool column statistics; spreadsheet filters and pivot tables. The tool matters less than doing it for every column.

### Step 3 — Classify and decide

For each issue found, decide one of: **fix** (deterministically correct it), **flag** (keep it but mark it), **exclude** (remove it from the analysis, with a count), **escalate** (ask the owner), or **accept** (it is real). Record the decision and the number of affected rows. Prioritise issues by how much they could change the answer: a 0.01% encoding glitch in a free-text field matters less than 3% duplicate orders.

### Step 4 — Apply transformations in code, in order

Write the cleaning as an ordered, re-runnable script or query chain: raw → typed → standardised → deduplicated → validated → analysis-ready. Each stage should be inspectable. Order matters: trim whitespace before deduplicating; parse timezones before deriving dates; convert units before computing outliers.

### Step 5 — Validate the output

Run validation rules (below) on the cleaned output, and reconcile it to the input: rows in = rows out + rows excluded (by reason); key totals (sum of revenue, count of distinct customers) before and after, with every difference explained.

### Step 6 — Document and hand over

Produce, in whatever form the project uses (README, notebook section, data catalogue entry, model docs): the source, the grain, the list of transformations with affected counts, the validation rules, known remaining issues, and how to re-run it.

## Issue-by-issue guidance

### Types

- **Read everything as text first** when the source is untrusted (CSV, Excel, scraped data), then convert explicitly. Automatic type inference silently destroys data: leading zeros in postcodes, ZIP codes, phone numbers and account IDs; long IDs converted to floats and rounded (anything beyond ~15–16 significant digits); gene names and product codes turned into dates by spreadsheets (e.g., `MARCH1`, `1-5`).
- **IDs are strings**, even when they look numeric. You never do arithmetic on them.
- **Track conversion failures.** When coercing text to number or date, count the values that failed to parse and look at them. Silent coercion to null (`errors='coerce'`, `TRY_CAST`) is fine only if you inspect what was coerced.
- **Locale-specific number formats**: `1.234,56` vs `1,234.56`; currency symbols; thousands separators; parentheses for negatives in accounting exports; percentages stored as `45%`, `45` or `0.45`.
- **Booleans** arrive as `Y/N`, `yes/no`, `true/false`, `1/0`, `T/F`, blank. Map explicitly; decide what blank means.

### Missing values

Missing is not one thing. Distinguish:

| Kind | Example | Typical handling |
|---|---|---|
| Not applicable | "Spouse name" for single people | Keep as a distinct state, not an error |
| Not collected | Field added to the form in March | Restrict analysis to the period it exists, or model the gap |
| Unknown / refused | Survey "prefer not to say" | Keep as its own category |
| Lost in processing | Failed join, pipeline error | Fix the pipeline; do not impute |
| Disguised | `0`, `-1`, `999`, `N/A`, `""`, `1900-01-01`, `1970-01-01` (Unix epoch zero) | Convert to explicit null after confirming meaning |

Then consider the mechanism: if missingness is related to the outcome (e.g., dissatisfied customers skip the satisfaction survey), dropping missing rows biases results. Options, in increasing sophistication: complete-case analysis (state the bias risk); indicator for missingness plus a fill value (for modelling); simple imputation (median/mode — understates variance, use cautiously); model-based or multiple imputation (when missingness is substantial and plausibly random given observed variables). Never impute an identifier, a target variable you are trying to measure, or a value you will report as a fact.

Report the missing rate for every variable you use.

### Duplicates

- **Exact duplicates** (all columns identical) are usually load errors: double ingestion, retried API calls, overlapping exports. Remove, count, and find the cause.
- **Key duplicates** (same supposedly-unique ID, different content) mean either the key is not really unique (e.g., order ID reused across regions), or there are versions (updates over time — keep the latest by a reliable timestamp, not by file order), or there is a bug.
- **Fuzzy duplicates** (same real-world entity, different records: "Acme Corp", "ACME Corporation", "Acme Corp." at slightly different addresses). Resolve with normalisation (case, whitespace, punctuation, common suffixes, unicode normalisation) then matching rules (exact on a strong identifier like email or tax ID; fuzzy similarity on names with blocking on another field). Fuzzy matching has false positives — merging two different people is often worse than leaving a duplicate. Review a sample of matches and of near-misses by hand, and keep the mapping table so merges are reversible.
- **Event duplicates** in tracking data: client retries, double-fired tags. Deduplicate by event ID if one exists; otherwise by (user, event, timestamp within a small window) — and state the window.

### Joins that multiply rows

The single most common source of silently wrong totals. Before every join:

1. **State the expected cardinality**: one-to-one, many-to-one, one-to-many.
2. **Check key uniqueness** on the side that should be unique: `SELECT key, COUNT(*) FROM t GROUP BY key HAVING COUNT(*) > 1`.
3. **Count rows before and after.** A many-to-one join should not change the row count of the many side. A left join should never reduce it.
4. **Check match rates**: what fraction of keys found a partner? Unmatched rows are either expected (new products not yet in the catalogue) or a key-format mismatch (trailing spaces, case, leading zeros, type differences — `'00123'` vs `123`).
5. **Aggregate before joining** when combining two one-to-many relationships to the same parent (e.g., orders and support tickets per customer). Joining both to the customer and then summing produces a cross-product.

Many libraries can assert cardinality (e.g., pandas `merge(..., validate="many_to_one")`); use that when available. In SQL, wrap critical joins with a count check.

Also watch for **slowly changing dimensions**: joining facts to a dimension table that keeps history (one row per customer per validity period) without filtering on the effective date multiplies rows.

### Outliers and impossible values

Separate three things:

- **Impossible values** — violate a hard rule: negative ages, quantities, or durations; end before start; percentages over 100; dates in the future for past events; birth years before 1900. These are errors; fix if the correction is deterministic, otherwise null and flag.
- **Implausible values** — possible but suspicious: a 140-year-old customer, a 30-hour session, a $1M consumer order. Investigate a sample; often they are test data, bots, unit errors (cents vs dollars, ms vs s, kg vs g), or sentinel values.
- **Genuine extremes** — real and important (whale customers, viral posts). Keep them; use robust statistics or report them separately.

Detection heuristics: domain bounds first (most valuable); percentiles (inspect beyond p99.9 and below p0.1); IQR fences (values beyond Q3 + 3×IQR are worth a look, 1.5×IQR is too aggressive for skewed data); z-scores only for roughly symmetric data; per-segment rules (what is extreme for one product is normal for another). Unit errors often show up as a secondary cluster ~100× or ~1000× the main one.

### Text, encoding and unicode

- **Determine the encoding** rather than guessing. Mojibake patterns like `Ã©` for `é`, `â€™` for `'`, or `�` replacement characters indicate UTF-8 read as Latin-1/Windows-1252 or vice versa. Fix by decoding correctly from the original bytes, not by find-and-replace on the damaged text (once replacement characters exist, information is lost).
- **Byte-order marks** at the start of files can corrupt the first column name.
- **Unicode normalisation**: `é` may be one code point or two (e + combining accent). Normalise (NFC for storage/display; NFKC when you also want to fold compatibility forms like full-width characters) before comparing or deduplicating.
- **Invisible characters**: non-breaking spaces, zero-width spaces, tabs, carriage returns from Windows line endings, trailing whitespace. They make identical-looking keys fail to join. Strip or normalise.
- **Case**: decide case-folding rules per column (emails: case-insensitive domain, and in practice usually the whole address; names: preserve for display, fold for matching).
- **Free-text categories**: map variants to canonical values with an explicit mapping table (`"U.S.", "USA", "United States", "us"` → one code). Keep unmapped values visible rather than lumping them into "Other" silently.
- **Delimiters and quoting in CSV**: embedded commas, quotes and newlines inside fields break naive parsers. Use a real CSV parser; check that every row has the expected number of fields.

### Dates, times and timezones

- **Parse with an explicit format.** `03/04/2025` is 3 April or March 4 depending on locale; auto-parsers may choose differently row by row. If both interpretations are possible, find a value with day > 12 to determine the convention — and check it is consistent across the file.
- **Know what timezone each timestamp is in.** Many systems store UTC; some store server-local time; some store user-local time without an offset. Naive timestamps (no timezone) are ambiguous — find out from the producer.
- **Convert to one reference (usually UTC) for storage and joins; convert to the reporting timezone only when deriving calendar fields** (date, week, hour of day). "Orders per day" depends on whose day.
- **Daylight-saving transitions** create duplicated and missing local hours. Use timezone-aware libraries, not fixed offsets.
- **Epoch timestamps**: seconds vs milliseconds vs microseconds (a value around 1.7e9 is seconds in the 2020s; 1.7e12 is milliseconds).
- **Sentinel and default dates** (`1900-01-01`, `1970-01-01`, `9999-12-31`) usually mean unknown or open-ended.
- **Excel serial dates** (days since 1899-12-30 in the default system; the 1904 system on some older Mac files) appear as integers around 40,000–50,000.
- **Event time vs processing time**: when something happened vs when it was recorded. Late-arriving data makes recent periods look low.
- **Week and fiscal definitions**: ISO weeks vs Sunday-start weeks; fiscal years that do not start in January.

### Units and currencies

- Store the unit explicitly — in the column name or an adjacent column — and convert to one unit before aggregating.
- Currency conversion needs a rate *and a date* and a policy (transaction-date rate, month-average, fixed budget rate). Record which.
- Watch for minor units (cents, pence) mixed with major units, and for currencies with no minor unit or with three decimals.
- Percentages: ratio (0.45) vs percent (45). Check a few values against a known case.
- Mixed measurement systems (lb and kg, miles and km) — frequently a per-country or per-source issue.

### Categorical consistency

- Profile every categorical column's value list; it is usually short enough to read in full.
- Watch for categories that changed names over time, codes reused with different meanings, and hierarchies that do not roll up consistently (a city assigned to two regions).
- Maintain mapping tables as versioned data, not hard-coded branches in code.

### Source-specific hazards

| Source | What usually goes wrong |
|---|---|
| **Spreadsheets** | Merged cells and multi-row headers; totals and subtotals rows mixed into data; hidden rows and columns; values that are formulas with errors (`#N/A`, `#REF!`); dates and IDs auto-converted; colour-coding used as data (lost on export); several tables on one sheet; manual edits with no history |
| **CSV exports** | Delimiter and quoting problems; encoding (often Windows-1252 from older tools); truncation at row limits of the exporting tool (1,048,576 rows for Excel); locale-dependent number and date formats; trailing summary lines |
| **APIs** | Pagination silently stopping early (check total-count fields against rows received); rate-limit errors returned as empty pages; nested JSON flattened inconsistently; fields absent vs null vs empty; schema changes between versions; timestamps in mixed formats |
| **Scraped web data** | Layout changes producing shifted columns; HTML entities and whitespace; duplicated items across pages; localised content; partial loads (see `web-scraping`) |
| **Event / tracking data** | Bots and internal traffic; duplicate events from retries; clock skew on client devices (events "from the future"); events lost offline and arriving late in bursts; tracking-plan changes per app version |
| **Manually entered data** | Typos and variant spellings; free text in structured fields; default values left in place (first item of a dropdown is over-represented); copy-paste errors |
| **Merged sources** | Different definitions of the same field; different ID schemes needing a crosswalk; overlapping coverage producing duplicates |

### Working at scale

When data is too large to inspect fully:

- Profile with aggregate queries over the full data (counts, null rates, min/max, distinct counts — approximate distinct counts are fine) rather than on a sample, because rare problems hide in samples.
- Inspect rows with stratified samples: some from every source, partition, day and category, plus the extremes.
- Push checks down to where the data lives (warehouse SQL) rather than extracting it.
- Keep cleaning logic set-based and deterministic so it can run incrementally; avoid row-by-row loops and nondeterministic "first row" choices.

## Validation rules and data contracts

### Kinds of rules

| Rule type | Examples |
|---|---|
| Schema | Expected columns present, types correct, no unexpected columns (or explicitly allowed) |
| Completeness | Required fields non-null; null rate below a threshold |
| Uniqueness | Primary key unique; natural key unique within its scope |
| Validity | Values within allowed set or range; formats (email, ISO country code, postcode) |
| Referential integrity | Foreign keys exist in the parent table (or match rate above threshold) |
| Consistency | Cross-field logic: end ≥ start; total = sum of line items; shipped orders have a ship date |
| Volume | Row count within expected range versus history (e.g., within ±30% of the same weekday's median) |
| Freshness | Latest timestamp within expected lag |
| Distribution | Mean, null rate, category shares within historical bounds — catches silent upstream changes |
| Reconciliation | Totals match a source of record within tolerance |

Severity matters: some failures should stop the pipeline (key duplicates, schema change), others should warn (volume 20% low on a holiday). Set thresholds from history, not from guesses, and review them when they fire too often — a check that always warns is ignored.

Tools: SQL assertions, dbt tests, Great Expectations / Soda / pandera-style libraries, pipeline-native checks, or plain assertions in a script. Use what the project already has.

### Data contracts

A data contract is an agreement between a producer and its consumers about what the data will look like: schema, semantics (what each field means, units, timezone), guarantees (uniqueness, completeness, freshness), and the process for changing it (versioning, notice period). It is useful when several teams depend on a dataset and breakages are costly. Keep contracts in version control next to the code that produces the data, enforce them with automated checks at the boundary, and treat breaking changes the way you would treat a breaking API change (see `api-design`). A contract without enforcement is documentation; still valuable, but it will drift.

## Documenting transformations

For each transformation, record: what was changed, the rule (in code), why, the number of rows or values affected, and the date or version. Good forms: comments in the cleaning script next to each step plus a generated summary table of counts; a cleaning log in a notebook; model documentation in a transformation framework. Include a final reconciliation: input rows, output rows, and rows removed by each reason, summing exactly.

Version cleaned outputs and the code that produced them together, so any reported number can be traced back to the raw input.

## Discovering context

- Look for existing staging or cleaning layers, data catalogues, dbt models, or data dictionaries before writing new cleaning logic — reuse definitions so your numbers match everyone else's.
- Check whether validation tooling already exists in the project and follow its conventions.
- Ask the data owner about known quirks; they often know exactly why a field is weird.
- Find out the organisation's conventions for timezone, currency, fiscal calendar and exclusion rules (test accounts, internal users).
- Check privacy rules before inspecting personal data: work with the minimum fields needed, avoid copying personal data into logs, notebooks or tickets, and follow retention and masking policies.

## Pitfalls and anti-patterns

- **Cleaning in a spreadsheet by hand** for anything that will be repeated or audited. The steps are unrecorded and unrepeatable.
- **Dropping all rows with any null** (`dropna()` on the whole frame). Often discards most of the data and biases what remains.
- **Silent coercion.** Parsing that turns bad values into nulls without counting them.
- **Deduplicating on the wrong key** or keeping "the first" row where file order is arbitrary.
- **Fixing symptoms downstream** in many places instead of once upstream.
- **Over-cleaning.** Removing real extremes, smoothing genuine variation, or forcing data into expected categories.
- **Trusting column names.** `created_at` may be the update time; `revenue` may include tax; `user_id` may be a device ID.
- **Assuming a join key matches** across systems without checking format (case, padding, type).
- **Ignoring time-varying definitions**: a status code that meant one thing before a migration and another after.
- **Validation that only checks schema.** Data can be perfectly typed and completely wrong; include distribution and reconciliation checks.
- **Leaving cleaning decisions undocumented**, so the next person re-cleans differently and gets different numbers.
- **Copying sensitive data into ad-hoc files** during cleaning, creating uncontrolled copies.

## Quality bar and verification

- [ ] Raw data is preserved unchanged; all cleaning is in re-runnable code.
- [ ] Grain and primary key are stated and uniqueness is verified.
- [ ] Every column used has been profiled; types, nulls, ranges and top values are known.
- [ ] Disguised missing values and sentinels are converted to explicit nulls (or documented).
- [ ] Every join's cardinality was checked, with row counts before and after and match rates.
- [ ] Dates are parsed with explicit formats; timezones are known and handled; calendar fields derived in the reporting timezone.
- [ ] Units and currencies are consistent before aggregation.
- [ ] Encoding is correct; keys are normalised for whitespace, case and unicode where appropriate.
- [ ] Each transformation has a recorded reason and affected count; input rows = output rows + excluded rows by reason.
- [ ] Key totals reconcile to the source of record, with differences explained.
- [ ] Validation rules are automated where the data will be refreshed, with severity levels and thresholds based on history.
- [ ] Remaining known issues are listed for consumers.

## Worked reasoning: a customer export that "doesn't add up"

A CRM export of 48,210 customers is to be joined to 312,000 orders from the billing system to compute lifetime value. The first attempt gives total revenue 7% higher than finance reports.

1. **Grain and keys.** Customers: one row per customer supposedly; `customer_id` has 48,210 rows but 47,602 distinct values. 608 IDs appear twice. Inspection: the export included both active and archived versions of merged accounts. Decision: keep the active version, record the 608 removals, report the merge issue to the CRM owner.
2. **Join keys.** Billing stores `customer_id` as an integer; CRM as text with leading zeros (`004512`). Before normalising, only 81% of orders matched; after stripping zeros consistently on both sides (both are numeric IDs, confirmed with the owner), 99.4% matched. The remaining 0.6% are orders from customers created after the CRM export — expected, documented.
3. **Fan-out.** The duplicate customer rows had doubled their orders in the join; removing them took the excess from 7% to 1.2%.
4. **Currency.** Billing has mixed currencies; 1.2% excess traced to non-USD orders summed as USD. Converted at transaction-date rates per the finance policy.
5. **Reconciliation.** Total revenue now matches finance within 0.05% (timing of refunds posted after month end — explained and documented).
6. **Contract.** Added checks: `customer_id` unique in the CRM extract; order match rate ≥ 99%; all amounts carry a currency code; total revenue within 0.5% of the finance figure. The pipeline now fails if any is violated.

Every fix came from a check, every check came from an expectation, and every change has a count.

A quick spot-check that catches many problems: pick five records at random and five extreme ones, trace each from the raw input through every cleaning step to the output, and confirm each transformation did what you intended.
