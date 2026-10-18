---
name: web-scraping
description: >-
  Extract structured data from websites responsibly and reliably: checking
  terms of service, robots.txt and legal constraints, preferring official APIs
  and data exports, choosing plain HTTP versus a headless browser, parsing
  HTML/JSON, pagination and crawling, rate limiting and politeness, resilience
  to layout changes, deduplication, and storing provenance. Never bypasses
  CAPTCHAs, logins or paywalls. Use when asked to scrape, crawl, harvest, or
  "pull data from" a website, monitor pages for changes, build a scraper or
  spider, or fix a scraper that broke.
metadata:
  category: automation
  related: browser-automation, api-integrations-and-webhooks, text-processing-and-regex, etl-pipelines, data-cleaning-and-validation, scheduled-jobs, web-research
---

# Web Scraping

Scraping is reading a website the way a program would rather than a person would. Technically it is usually easy; what makes it hard is that you are a guest on someone else's infrastructure, the data's structure is not a contract, and the legal and ethical status varies by site, data type and jurisdiction. A good scraper is polite, narrow, honest about what it is, and built expecting the page to change.

## Scope

Covers: one-off extraction, recurring scrapes, multi-page crawls, change monitoring, and maintaining scrapers.

Not covered:
- Driving a browser to test your own app or complete interactive tasks: `browser-automation` (it also covers the headless mechanics referenced here).
- Consuming official APIs: `api-integrations-and-webhooks`.
- Turning scraped data into a maintained dataset with loads, schemas and quality checks: `etl-pipelines`, `data-cleaning-and-validation`.
- Answering a research question by reading the web: `web-research`.

## Hard limits

These are not judgment calls:

- **Do not bypass access controls.** No solving or outsourcing CAPTCHAs, no evading bot-detection challenges, no circumventing logins, paywalls, IP blocks, or rate limits that a site has put in place. A block is the site saying no.
- **Do not log in to scrape with someone's credentials** unless the user owns the account, the site's terms permit automated access for that account, and the user has explicitly asked. Never create accounts to gain access.
- **Do not collect personal data at scale** (names plus contact details, profiles, photos of identifiable people) without a clear lawful basis, and never to build profiles of private individuals.
- **Do not republish copyrighted content** wholesale. Extracting facts and metadata differs from copying articles, images or reviews.
- **Do not degrade the site.** If your traffic could noticeably load the server, slow down or stop.

If a user's request requires crossing one of these lines, say so plainly and offer the legitimate alternatives: an official API, a data export, a licensed dataset, contacting the site owner, or doing the task manually.

## Core principles

1. **Ask for the data before you take it.** Many sites offer an API, bulk download, RSS/Atom feed, sitemap, or open-data portal. These are stable, sanctioned, and usually easier. Scraping HTML is the fallback, not the first move.

2. **Respect the site's stated rules.** Terms of service, `robots.txt`, rate-limit headers, and explicit "no scraping" notices express the operator's wishes. Legal enforceability varies by jurisdiction and is contested; ethical and practical reasons to respect them do not vary. Ignoring them also gets you blocked.

3. **Fetch the minimum.** Request only the pages and fields you need, as rarely as is useful. Fewer requests means less load, less blocking risk, less data to protect, and less to break.

4. **The page structure is not a contract.** Selectors break when the site redesigns. Write extraction that fails loudly when expected fields are missing, prefers stable hooks, and is easy to update.

5. **Record where every value came from.** URL, fetch time, and ideally the raw response. Without provenance you cannot debug, re-parse, defend the data, or honour deletion requests.

6. **Identify yourself honestly.** Use a descriptive User-Agent with contact information where appropriate. Pretending to be a regular browser to evade a policy is deception; spoofing to work around a block is circumvention.

## Process

### 1. Clarify the goal

- What fields, from which pages, how many records, how fresh, how often?
- What will the data be used for (internal analysis, product feature, republication, training data)? The use affects legal risk and what is acceptable.
- Is this one-off or recurring? One-off can be scrappier; recurring needs monitoring and maintenance.
- Is a sample enough? Many questions can be answered with hundreds of records rather than millions.

### 2. Check permission and alternatives

Work through in order:

1. **Official API or export?** Look for developer docs, "API" in the footer, `/api/` paths, data download pages, open-data portals, or a feed. Check the API's terms too.
2. **Terms of service.** Search for "automated", "scrape", "crawl", "robot", "data mining". Note explicit prohibitions and any permitted-use clauses.
3. **robots.txt** (`https://site/robots.txt`). Check `Disallow` rules for your user agent and `*`, and any `Crawl-delay`. Sitemaps listed there are a gift: they enumerate pages without crawling.
4. **Data type.** Personal data triggers privacy law (e.g. GDPR, CCPA and equivalents) regardless of whether it is publicly visible. Copyrighted text/images carry their own restrictions. Facts (prices, schedules, specifications) are generally lower risk, but database rights exist in some jurisdictions.
5. **Access type.** Public, no login: lowest risk. Behind login: governed by the account's terms, often prohibited. Behind a CAPTCHA, paywall or explicit block: stop.

If the situation is ambiguous and the stakes are real (commercial use, personal data, large scale), recommend the user consult their legal counsel. Do not present legal conclusions as certain; the law in this area is unsettled and jurisdiction-dependent.

### 3. Investigate how the page delivers data

Before writing parsing code, look at what the server actually sends:

- **View the raw HTML** (fetch with a plain HTTP client, or view-source). Is the data in the initial HTML?
- **Check the browser's network panel.** Modern sites often load data from a JSON endpoint (XHR/fetch). Calling that endpoint directly is faster, lighter on the server, and more stable than parsing rendered HTML. Respect the same rules: it is still the site's infrastructure, and some of these endpoints are covered by terms.
- **Look for embedded structured data**: `<script type="application/ld+json">` (schema.org), Open Graph meta tags, microdata, or a JSON state blob assigned to a global variable in a `<script>` tag (common in server-rendered frameworks). These are often cleaner than visible markup.
- **Note pagination style**: page numbers, offset/limit, cursor tokens, "load more" buttons, infinite scroll.

### 4. Choose the fetch method

| Situation | Approach | Why |
|---|---|---|
| Data in initial HTML or in a JSON endpoint | Plain HTTP client (e.g. `requests`/`httpx`, `fetch`, `curl`) | 10–100× cheaper and faster; simpler to debug |
| Data rendered by JavaScript with no usable endpoint | Headless browser (e.g. Playwright, Puppeteer, Selenium) | Executes scripts; see `browser-automation` |
| Requires interaction (expand, select options) | Headless browser, but first check if the interaction just calls an endpoint | Interaction often maps to a parameterised request |
| Many pages, crawl structure | A crawling framework (e.g. Scrapy, Crawlee, Colly) | Built-in scheduling, dedup, throttling, retries |
| One-off, small | Simplest thing that works | Do not build infrastructure for 50 pages |

Headless browsers are heavier on both sides: they download every asset unless you block images/fonts/media, and they are easier for the site to detect as automation. Use them when needed, not by default.

### 5. Fetch politely

- **Rate limit.** Start slow: one request every one to several seconds per host for small sites; follow `Crawl-delay` if present. Large sites tolerate more, but you do not know their capacity. Concurrency per host should usually be 1–2.
- **Respect server signals.** On HTTP 429 or 503, back off exponentially and honour `Retry-After`. Repeated 403s mean you are blocked: stop, do not rotate around it.
- **Schedule off-peak** for large jobs when practical.
- **Cache.** Store responses locally during development so you iterate on parsing without re-fetching. Use conditional requests (`If-None-Match` / `If-Modified-Since`) on recurring scrapes.
- **Set timeouts** on every request; a hung connection stalls the whole job.
- **Send a truthful User-Agent**, e.g. `projectname/1.0 (+https://example.org/bot; contact@example.org)`.
- **Do not use residential proxy pools or IP rotation to evade blocks.** If a site blocks you at polite rates, that is the answer.

Illustrative polite fetch loop (Python):

```python
import time, httpx

client = httpx.Client(
    headers={"User-Agent": "price-monitor/1.0 (+mailto:ops@example.org)"},
    timeout=20, follow_redirects=True,
)

def get(url, min_interval=2.0, _last=[0.0]):
    wait = _last[0] + min_interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    for attempt in range(5):
        r = client.get(url)
        _last[0] = time.monotonic()
        if r.status_code in (429, 503):
            delay = float(r.headers.get("Retry-After", 2 ** attempt * 5))
            time.sleep(delay)
            continue
        if r.status_code == 403:
            raise RuntimeError(f"Blocked at {url}; stopping rather than evading")
        r.raise_for_status()
        return r
    raise RuntimeError(f"Gave up on {url} after retries")
```

### 6. Parse robustly

Prefer, in order of stability:

1. JSON from an API/XHR endpoint or embedded structured data (JSON-LD, state blobs).
2. Semantic hooks: `id`s, `data-*` attributes, `itemprop`, ARIA labels, `<table>` headers, `<dl>` term/definition pairs.
3. Text anchors: "find the label 'Price', take the adjacent value".
4. Structural CSS/XPath selectors.
5. Generated class names (`.css-1x2y3z`, `.sc-bdVaJa`) — these change on every build; avoid.

Rules:
- **Use an HTML parser** (e.g. BeautifulSoup/lxml, parsel, cheerio, html5ever-based libraries), not regex, for HTML structure. Regex is fine for cleaning a value you already isolated. See `text-processing-and-regex`.
- **Scope selectors** to a container (each product card, each row) and extract fields relative to it, so a missing field in one card does not shift values into the next record.
- **Validate each record** against an expected schema: required fields present, types parse (numbers, dates, currencies), values in plausible ranges. Count and report failures rather than silently dropping them.
- **Normalise carefully**: whitespace, HTML entities, Unicode normalisation, locale-specific numbers ("1.234,56"), currencies, relative dates ("3 days ago" relative to fetch time — store fetch time).
- **Keep raw and parsed separate.** Store raw HTML/JSON (compressed) for recurring jobs where possible, so a parser fix can be replayed without re-fetching.

### 7. Handle pagination and crawling

- **Prefer enumerations** the site provides: sitemaps, API cursors, listing pages with stable page parameters.
- **Detect the end correctly**: empty page, missing "next" link, cursor absent, or a repeated page (some sites return the last page for any page number beyond it). Put a hard cap on pages as a safety net.
- **Deduplicate URLs** with canonicalisation: lowercase host, strip fragments and tracking parameters, sort query params, respect `<link rel="canonical">`.
- **Constrain the crawl**: allowed domains, path prefixes, maximum depth, maximum pages. Unbounded crawls wander into calendars, faceted search combinations and infinite URL spaces ("crawler traps").
- **Make it resumable**: persist the frontier (to-visit queue) and the visited set, so a crash does not mean starting over and re-hitting the server.
- **Offset pagination over changing data** skips or duplicates items when records are inserted during the crawl; dedupe by item ID and prefer cursors or sorted-by-ID listings.

### 8. Store with provenance

For each record, keep at least: source URL, fetch timestamp (UTC), scraper version, and a stable item key. Useful extras: HTTP status, a content hash, the raw response's storage location.

Choose storage by use: JSON Lines or CSV for small one-offs; a database table with a unique constraint on the item key for recurring jobs (upsert, so reruns update rather than duplicate). Track `first_seen` and `last_seen` for change detection.

Protect what you store: if it includes personal data, apply minimisation (drop fields you do not need), access controls, retention limits, and a way to delete on request.

### 9. Make it maintainable

Recurring scrapers break. Plan for it:

- **Monitor yield**: records per run, field fill rates, validation failure rate. Alert when they move sharply (zero records, or a field suddenly 100% empty, usually means a layout change).
- **Fixture tests**: save representative pages (including edge cases: missing price, sold out, multi-variant) and test the parser against them. When the site changes, add the new page as a fixture.
- **Isolate selectors** in one place per site so updates are small.
- **Version the parser** and record the version with the data.
- **Fail loudly**: a parser that returns empty strings on failure produces quietly wrong datasets. Raise or flag.

## Decision guidance

**Scrape or not?**

| Signal | Lean toward |
|---|---|
| Official API/export covers the need | Use it, even if it needs a key or costs money |
| ToS explicitly forbids automated access | Do not scrape; seek permission or a licensed source |
| robots.txt disallows the paths | Do not fetch them |
| Data is personal information about individuals | Avoid unless there is a clear lawful basis and minimal collection |
| Content is behind login/paywall/CAPTCHA | Do not scrape |
| Public factual data, permissive or silent ToS, small polite volume | Generally reasonable |
| You would be uncomfortable explaining the scraper to the site owner | Reconsider |

**Change monitoring vs full scrape**: if the goal is "tell me when X changes", fetch only the relevant page(s), hash the extracted region (not the whole page, which changes with ads and timestamps), and alert on hash change. Far fewer requests than recurrent full scrapes.

**Build vs buy**: commercial data providers and scraping APIs exist. Evaluate their own legal basis and terms; outsourcing the fetching does not outsource responsibility for how data was obtained, and services that advertise CAPTCHA solving or block evasion are doing what this skill prohibits.

## Discovering context

- Is there an existing scraper or data pipeline in the project? Reuse its HTTP client settings, storage, and conventions.
- Does the organisation have a policy on scraping, data acquisition, or approved data sources?
- Where will the data land, and what schema does downstream expect?
- Has anyone already contacted the site, or is there a data-sharing agreement?

## Worked examples

Illustrative Python; the same approach works with other languages and libraries.

### Checking robots.txt programmatically

```python
from urllib import robotparser
from urllib.parse import urljoin

UA = "price-monitor/1.0 (+mailto:ops@example.org)"

def allowed(base_url: str, path: str) -> bool:
    rp = robotparser.RobotFileParser()
    rp.set_url(urljoin(base_url, "/robots.txt"))
    rp.read()
    return rp.can_fetch(UA, urljoin(base_url, path))
```

Read robots.txt once per host per run, cache it, and honour `crawl_delay(UA)` if it returns a value. robots.txt does not grant permission that the terms withhold; it is one input among several.

### Preferring embedded structured data

Many product and article pages carry JSON-LD that is cleaner than the visible markup:

```python
import json
from bs4 import BeautifulSoup

def product_from_jsonld(html: str) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data])
        for item in items:
            if item.get("@type") == "Product":
                offer = item.get("offers") or {}
                if isinstance(offer, list):
                    offer = offer[0] if offer else {}
                return {
                    "name": item.get("name"),
                    "sku": item.get("sku"),
                    "price": offer.get("price"),
                    "currency": offer.get("priceCurrency"),
                }
    return None
```

Fall back to HTML selectors only when the structured data is absent or incomplete, and record which path produced each record.

### Scoped extraction that cannot misalign

```python
def parse_listing(html: str, url: str, fetched_at: str) -> tuple[list[dict], list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    records, problems = [], []
    for card in soup.select("[data-product-id]"):          # one container per item
        pid = card["data-product-id"]
        name = card.select_one("[itemprop=name]")
        price = card.select_one("[itemprop=price]")
        if not name or not price:
            problems.append(f"{url}#{pid}: missing {'name' if not name else 'price'}")
            continue
        records.append({
            "id": pid,
            "name": name.get_text(strip=True),
            "price_raw": price.get("content") or price.get_text(strip=True),
            "source_url": url,
            "fetched_at": fetched_at,
        })
    return records, problems
```

Each field is read relative to its own card, so a missing price affects one record and is reported rather than silently shifting all later prices. `problems` feeds the run summary and the yield alert.

### Fixture test for the parser

```python
def test_parse_listing_handles_sold_out_card():
    html = open("tests/fixtures/listing_2026-03_sold_out.html").read()
    records, problems = parse_listing(html, "https://example.com/c/shoes", "2026-03-02T10:00:00Z")
    assert len(records) == 23
    assert any("missing price" in p for p in problems)   # the sold-out card
```

Fixtures are saved pages from real fetches (scrub any personal data). When the site changes and the scraper breaks, save the new page as a fixture first, then fix the parser until both old and new fixtures pass.

### Sizing the job before running it

Before a crawl, estimate: pages needed × delay per request = wall time. 20,000 product pages at one request every 2 seconds is about 11 hours. If that is too slow, the answer is a sitemap, an API, a narrower scope or a data provider — not more concurrency against someone else's server.

## Pitfalls and anti-patterns

- **Starting with a headless browser** when the data is in a JSON endpoint or the initial HTML.
- **Hammering**: parallel requests with no delay, retrying 429s immediately.
- **Evasion**: rotating proxies/user agents to beat blocks, solving CAPTCHAs, replaying session cookies from a logged-in browser. All prohibited here.
- **Selector brittleness**: depending on generated class names or deep `div > div > div:nth-child(3)` chains.
- **Silent nulls**: missing fields become empty strings and nobody notices for months.
- **Field misalignment**: extracting lists of names and lists of prices separately and zipping them; one missing price shifts every subsequent record.
- **No provenance**: cannot tell which run or URL a bad value came from.
- **Infinite crawls** through faceted filters or calendars.
- **Ignoring encodings**: mojibake from wrong charset assumptions; respect the `Content-Type` charset and `<meta charset>`.
- **Relative dates and prices without context**: "yesterday", "$10" without currency or fetch time.
- **Storing personal data indefinitely** "just in case".
- **Testing parsers only against today's live page**, so the test passes and tells you nothing about tomorrow.

## Verification

- [ ] Checked for an API/export first, and documented why scraping was still needed.
- [ ] ToS and robots.txt reviewed; fetched paths are allowed; no access controls bypassed.
- [ ] Request rate and concurrency are bounded; 429/503 handled with backoff; 403 stops the job.
- [ ] Parser tested against saved fixture pages, including at least one edge case.
- [ ] Spot-checked a random sample of output records against the live pages by eye.
- [ ] Record count matches expectation (e.g. listing says "248 results" and you have 248).
- [ ] Every record carries source URL and fetch time; reruns do not create duplicates.
- [ ] Validation failures are counted and reported, not dropped silently.
- [ ] Personal data minimised or absent; storage and retention appropriate.
- [ ] For recurring jobs: yield monitoring and alerting in place.

## Reporting back

Tell the user: where the data came from and how (API, endpoint, HTML), what permission checks you did and what you found, volume and rate used, record counts and known gaps or parse failures, how to rerun, and any legal or ToS uncertainty they should resolve. If you declined part of the request (e.g. a login-walled site), say what you did instead.
