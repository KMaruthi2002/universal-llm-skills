---
name: financial-modeling
description: >-
  Build, review, and explain business and financial models: identifying the
  question the model answers, choosing drivers, unit economics (contribution
  margin, customer acquisition cost, lifetime value, payback), bottom-up and
  top-down revenue builds, cost and headcount builds, linking income
  statement, balance sheet, and cash flow at a conceptual level, working
  capital and runway, scenarios and sensitivity analysis, documenting
  assumptions, and sanity checks. Use when asked to build a financial model,
  forecast, budget, business plan numbers, pricing or unit-economics
  analysis, runway or burn calculation, break-even, market sizing, or
  "what happens to profit if…". Does not give personalised investment, tax,
  or legal advice. For spreadsheet mechanics use spreadsheet-modeling; for
  statistical forecasting methods use statistical-analysis.
metadata:
  category: analysis
  related: spreadsheet-modeling, data-analysis, statistical-analysis, competitive-analysis, technical-decision-making, presentations, roadmap-and-prioritization, business-communication
---

# Financial Modeling

A financial model is a structured argument about how a business works, expressed in numbers. Its value is not the precision of its outputs — those are always wrong to some degree — but the clarity it brings to which assumptions matter, how they interact, and what has to be true for a plan to work. A good model is transparent, driven by a small number of explicit assumptions, internally consistent, and easy to interrogate.

## Scope

Covers: operating models, forecasts and budgets, unit economics, pricing analysis, startup and business-plan models, runway and break-even, scenario and sensitivity analysis, three-statement logic at a conceptual level, and simple valuation concepts used for business decisions.

Does not cover:

- Spreadsheet structure, formulas, and formatting mechanics → `spreadsheet-modeling` (use together).
- Statistical forecasting techniques (time series, regression) → `statistical-analysis`.
- Exploring historical data to inform assumptions → `data-analysis`.
- Market and competitor research feeding assumptions → `competitive-analysis`, `web-research`.

**Boundaries on advice.** Models and analysis are informational. Do not give personalised investment advice (whether a particular person should buy, sell, or hold a security or asset), and do not present tax, accounting, or legal conclusions as authoritative; describe the general concept, flag that rules vary by jurisdiction and situation, and recommend a qualified professional for decisions that depend on them. When a model will be used to raise money, report to regulators, or inform lending, say that it should be reviewed by an appropriately qualified person.

## Core principles

1. **Start from the decision.** "Should we hire three salespeople?", "What price makes this profitable?", "How long does our cash last?" determine what the model must contain and what it can leave out. *Why:* models built "to have a model" grow until no one understands them and still fail to answer the question asked.

2. **Drive outputs from a small set of explicit assumptions.** Revenue, costs, and cash should be calculated from drivers (customers, prices, conversion rates, salaries, unit costs), not typed in as numbers. *Why:* hardcoded outputs cannot be stress-tested, and no one can tell which beliefs produced them.

3. **Separate inputs, calculations, and outputs.** Assumptions live in one clearly marked place; calculations reference them; outputs summarise. *Why:* this is what makes a model auditable and safe to change.

4. **Model the mechanism, not just the trend.** Extrapolating last year's growth rate says nothing about why growth happens. Building revenue from the actual engine — traffic × conversion × price, or reps × quota × attainment — exposes what has to change for the forecast to come true. *Why:* mechanism-based models reveal constraints (capacity, hiring lead times, market size) that trend lines ignore.

5. **Cash is not profit.** Timing differences between earning revenue and receiving cash, and between incurring costs and paying them, determine survival. *Why:* profitable businesses run out of cash when they grow fast, collect slowly, or buy inventory ahead of sales.

6. **Uncertainty is the point.** Every assumption is a guess with a range. Scenarios and sensitivity analysis show which guesses matter. *Why:* a single-point forecast invites false confidence and hides the assumptions on which the decision really hinges.

7. **Simple and right beats complex and wrong.** Add detail only where it changes the decision. *Why:* every additional line is another place for an error, and complexity makes errors harder to find.

## Process

### 1. Frame the question and the audience

Clarify:

- **The decision and its options** (e.g. hire now vs. in six months; price A vs. price B).
- **The audience**: founders, management, a board, investors, lenders, a non-financial team. This sets the level of detail and the format of outputs.
- **The time horizon and granularity**: monthly for runway and early-stage plans (cash can run out between annual snapshots); quarterly or annual for longer-range strategy.
- **What exists already**: historical financials, an existing model, a chart of accounts, a budget, data on customers and costs. Build on these and match their definitions.
- **Conventions** of the organisation or audience: fiscal year, currency, accounting basis, line-item names, formatting standards.

### 2. Map the business mechanics

Before opening a spreadsheet, sketch how the business makes and spends money:

- How customers are acquired (channels, sales motion), and what it costs.
- How revenue is generated (one-off sales, subscriptions, usage, transactions, licensing, advertising, services) and when it is recognised and collected.
- What each unit costs to deliver (cost of goods, hosting, payment fees, support, fulfilment).
- What the fixed and semi-fixed costs are (people, rent, software, overhead) and what drives them.
- What capital investments are needed (equipment, inventory, capitalised development), and the financing (equity, debt, revenue-based).
- What constraints exist: capacity, hiring speed, market size, regulatory limits, supplier terms.

A driver tree — the output metric at the top, decomposed into the drivers that determine it — is a useful way to make this explicit and to find the few drivers that matter most.

### 3. Get unit economics right first

For most businesses the unit economics determine whether scaling helps or hurts. Common measures (definitions vary; state yours):

| Measure | Concept | Watch out for |
|---|---|---|
| Contribution margin per unit/customer | Revenue minus the variable costs of serving it | Omitting costs that scale with customers: support, payment fees, onboarding, hosting |
| Gross margin % | (Revenue − cost of revenue) / revenue | Definitions of cost of revenue differ across companies and industries |
| Customer acquisition cost (CAC) | Sales and marketing cost to acquire one customer | Blended vs. paid-channel CAC; excluding salaries; time lag between spend and acquisition |
| Customer lifetime value (LTV) | Margin-based value of a customer over their expected life | Using revenue instead of margin; assuming churn stays low forever; ignoring discounting |
| LTV / CAC | Return on acquisition spend | Easily inflated by optimistic lifetimes; check alongside payback |
| CAC payback | Months of contribution margin to recover CAC | More robust than LTV for young businesses with little churn history |
| Churn / retention | Share of customers or revenue lost (or retained) per period | Customer vs. revenue churn; gross vs. net (including expansion); cohort differences |

If unit economics are negative, growth makes losses larger. Many plans fail because the model scales volume without checking whether each unit makes money once all variable costs are counted.

Worked reasoning (illustrative numbers): a subscription at 50 per month, with variable costs of 10 per month (hosting, support, payment fees), gives 40 contribution per month. With 2% monthly customer churn, the expected life is roughly 1 / 0.02 = 50 months, so undiscounted lifetime contribution is about 2,000. If CAC is 600, payback is 600 / 40 = 15 months and LTV/CAC is about 3.3. Now test fragility: at 4% churn, life halves to 25 months and LTV/CAC falls to about 1.7; payback is unchanged at 15 months but now consumes more than half of the customer's expected life. The churn assumption, not the price, is what the plan depends on — which tells you where to focus validation.

### 4. Build revenue

Choose the approach based on what you know:

| Approach | How | Good for | Risk |
|---|---|---|---|
| Bottom-up (capacity / funnel) | Units of capacity or funnel stages × conversion × price | Operating plans; early-stage businesses; anything with a clear acquisition engine | Overly optimistic conversion; missing ramp-up time |
| Cohort-based | Each period's new customers tracked with their own retention and expansion over time | Subscriptions, repeat purchase, marketplaces | Requires retention data or defensible assumptions |
| Top-down (market share) | Market size × share captured | Sanity-checking bottom-up; very early ideas | Share is a guess dressed as analysis; "if we get 1% of a huge market" is not a plan |
| Historical trend | Prior periods' growth extended, adjusted for known changes | Stable, mature businesses; short horizons | Misses structural change; hides drivers |

Build bottom-up wherever possible, and use top-down as a cross-check: if the bottom-up forecast implies an implausible share of the reachable market, one of them is wrong.

Include ramp-up and lags: new salespeople take months to reach full productivity; marketing spend converts with a delay; new products and markets start slowly. Include seasonality where it exists. Distinguish bookings, billings, recognised revenue, and cash collected when the timing differs (e.g. annual prepaid subscriptions).

### 5. Build costs

- **Variable costs** scale with volume: tie them to the revenue or unit drivers.
- **Headcount** is usually the largest cost for service and software businesses. Build it as a plan of roles with start dates and fully loaded costs (salary plus taxes, benefits, equipment, and overheads); link hiring to the drivers that justify it (e.g. support staff per thousand customers, salespeople per quota target).
- **Fixed and step costs**: rent, software, insurance, professional fees; note where they step up at thresholds (a new office, a larger plan).
- **Marketing and acquisition spend**: link to the funnel or CAC assumption so that growth and its cost stay consistent.
- **Capital expenditure**: equipment, capitalised development; it affects cash immediately and profit over time through depreciation or amortisation.

Check that cost growth is consistent with revenue growth: revenue doubling with flat support and infrastructure costs is a red flag.

### 6. Connect the three statements (conceptually)

For decisions about cash, financing, or valuation, link the statements:

- **Income statement**: revenue, costs, and profit over a period (accrual basis).
- **Balance sheet**: what the business owns and owes at a point in time.
- **Cash flow statement**: how cash changed, reconciling profit to cash.

The key links:

- Net profit flows into retained earnings (equity) on the balance sheet.
- Non-cash expenses (depreciation, amortisation, share-based compensation) are added back to profit in operating cash flow.
- Changes in working capital (receivables, inventory, payables, deferred revenue) adjust cash: growing receivables or inventory consumes cash; growing payables or deferred revenue provides it.
- Capital expenditure is an investing cash outflow and increases fixed assets.
- Borrowing, repayments, and equity raised are financing cash flows that change debt or equity.
- The cash at the end of the cash flow statement equals cash on the balance sheet.

**The balance sheet must balance** (assets = liabilities + equity) every period. If it does not, there is an error — usually a cash flow item without its balance sheet counterpart. Find it; never plug the difference.

Many operating decisions do not need full three-statement models. A profit-and-loss forecast plus a simple cash view (profit adjusted for major timing items and capital spending) is often enough. Build the full linkage when financing, working capital, or valuation is part of the question.

### 7. Cash, runway, and break-even

- **Burn rate**: net cash outflow per period. Distinguish gross burn (total spend) from net burn (spend minus cash in).
- **Runway**: cash on hand divided by net burn — but compute it month by month from the forecast, because burn changes as hiring and revenue change. Include a minimum cash buffer; running to zero is not a plan.
- **Break-even**: the volume or revenue at which contribution covers fixed costs (fixed costs / contribution per unit). Also identify *cash* break-even, which may differ.
- **Funding needs**: the low point of the cumulative cash curve, plus a buffer, plus time to raise.

Worked reasoning (illustrative numbers, in thousands): cash is 900 and current net burn is 60 per month, so the naive runway is 15 months. The plan adds two hires in month 3 (burn rises to 80), and revenue growth then reduces net burn by about 3 per month. Month by month, cumulative burn reaches about 732 by month 11 and 785 by month 12, leaving roughly 168 and 115. Cash would hit zero around month 14 or 15 — close to the naive figure — but with a minimum buffer of about three months' burn (~150), the *usable* runway ends around month 11. If raising money typically takes six months, fundraising must start by about month 5. The useful outputs are the buffer-adjusted date and the start-raising date, not "15 months of runway".

### 8. Scenarios and sensitivity

- **Sensitivity analysis**: change one assumption at a time across a plausible range and observe the output. Rank assumptions by how much they move the result (a tornado-style ranking). Focus validation effort on the top few.
- **Scenarios**: coherent sets of assumptions that move together (e.g. a downturn: lower conversion, longer sales cycles, higher churn, slower hiring). Typical sets are base, downside, and upside, but name them by their story rather than by optimism level, and make sure each is internally consistent.
- **Break-even or threshold analysis**: solve for the value of an assumption at which the decision flips (e.g. "the new product line is worth it if conversion exceeds 2.1%"). This is often the most useful output: the decision-maker can judge whether that threshold is plausible.
- **Probabilistic analysis** (simulation over assumption distributions) can help when many uncertainties interact and you have a basis for the distributions; without that basis, it adds false precision. Use sparingly and explain.

Present the range, not just the base case. Show what has to be true for the plan to work.

### 9. Document assumptions

For each key assumption, record: the value, the unit and period, the source or rationale (historical data, benchmark, quote, expert judgment, pure guess), the confidence, and the date. Mark which assumptions are the most sensitive. *Why:* six months later, no one will remember why churn was set to 2%, and a reviewer cannot evaluate the model without knowing which numbers are evidence-based.

Benchmarks from industry reports or other companies are useful starting points but vary widely by segment, stage, and definition; cite them with their source and date, and do not treat them as facts about this business.

### 10. Sanity-check and review

Run checks at three levels:

**Mechanical integrity**
- Balance sheet balances in every period; cash flow ending cash matches the balance sheet.
- No hardcoded numbers inside calculation rows; all inputs in the inputs area.
- Totals equal the sum of their parts; subtotals are not double-counted.
- Units and periods are consistent (monthly vs. annual rates, percentages vs. decimals, currencies).
- Signs are consistent (costs as negatives or positives, consistently).
- Changing an input changes the outputs as expected (spot-test a few).
- No circular references unless deliberate and controlled (e.g. interest on average cash balances); prefer to avoid them.

**Reasonableness**
- Growth rates, margins, and ratios compared with history and with credible benchmarks.
- Implied metrics: revenue per employee, implied market share, implied conversion rates, customers per support person, sales productivity — do they look like any real business?
- Ramp-up: does revenue appear before the capacity to deliver it?
- Extreme cases: set key drivers to zero or to high values; the model should behave sensibly.

**Narrative**
- Can you explain, in a few sentences, why the outputs come out as they do?
- Does the story match what the team believes about the business, and where it does not, which is wrong?

If you can execute code or a spreadsheet, actually run these checks; if not, walk through the arithmetic for a representative period explicitly and tell the user which checks to run.

## Business model patterns

Different business models have different engines and different places where models typically go wrong:

| Model | Core revenue engine | Key drivers to model | Common modelling mistakes |
|---|---|---|---|
| Subscription / SaaS | Customers × price, with retention and expansion by cohort | New customers per channel, churn (gross and net), expansion, price per seat or tier, sales capacity | Revenue churn vs. logo churn confused; deferred revenue ignored; annual prepay cash timing missed |
| Usage-based | Active customers × usage per customer × unit price | Activation, usage growth curves, price tiers, committed vs. on-demand | Assuming linear usage growth; ignoring usage volatility and concentration in a few large customers |
| E-commerce / retail | Traffic × conversion × average order value × repeat rate | Acquisition cost per channel, return rates, fulfilment and shipping costs, inventory | Ignoring returns, discounts, and inventory cash; treating repeat rate as constant |
| Marketplace | Gross transaction value × take rate | Supply and demand acquisition, liquidity, take rate, incentives and subsidies | Modelling one side without the other; counting gross value as revenue |
| Services / agency | Billable staff × utilisation × rate | Utilisation, hiring and ramp, rate card, project mix, bench time | Assuming full utilisation; ignoring non-billable time and payment terms |
| Hardware / manufacturing | Units × price, constrained by production capacity | Bill of materials, yield, capacity, lead times, inventory, warranty | Missing working capital for inventory; ignoring minimum order quantities and supplier terms |
| Advertising / media | Audience × engagement × monetisation (e.g. revenue per thousand impressions) | Audience growth, engagement, fill rate, pricing seasonality | Treating monetisation rates as stable; ignoring platform dependency |
| Nonprofit / grant-funded | Grants, donations, and earned income vs. programme costs | Funding pipeline and probability, restricted vs. unrestricted funds, programme cost per beneficiary | Counting pledged or restricted money as freely available cash |

Use the pattern that matches the business, combine patterns for hybrid models, and model each revenue stream with its own drivers rather than one blended growth rate.

## Communicating model outputs

The audience usually needs three things: the answer to the question, the range around it, and the assumptions it depends on.

- Lead with the decision-relevant outputs (e.g. cash low point and when it occurs; profit under each pricing option; the threshold at which the decision flips).
- Show the sensitivity ranking and the scenarios, not only the base case.
- Show the key assumptions next to the outputs, with their sources and confidence.
- Round to a precision the assumptions justify.
- Use charts for trajectories (cash over time, revenue by stream) and tables for comparisons (see `presentations` and `data-visualization`).
- State limitations plainly: what is not modelled, which assumptions are guesses, and any accounting or tax simplifications.

## Valuation concepts (for business decisions)

When a decision involves comparing investments or projects:

- **Net present value (NPV)**: the value today of future cash flows discounted at a rate reflecting the risk and the cost of capital. Positive NPV at an appropriate rate suggests a project creates value.
- **Internal rate of return (IRR)**: the discount rate at which NPV is zero; useful for comparison but misleading for projects with unusual cash flow patterns or different scales.
- **Payback period**: time to recover the investment; simple, ignores later cash flows and the time value of money.
- **Discounted cash flow valuation of a business**: projected free cash flows plus a terminal value, discounted. The terminal value often dominates the result, and small changes to growth or discount rate move it a lot — show the sensitivity.
- **Comparables**: valuation multiples of similar companies or transactions; quick but dependent on genuine comparability and market conditions.

Present valuations as ranges with the assumptions that drive them. This is analysis for the user's business decision, not a recommendation to buy or sell any security.

## Discovering context

- **Existing financials and models**: actuals, budgets, prior forecasts. Reconcile the model's starting point to actuals; mismatched definitions are a common source of error.
- **Accounting basis and policies**: revenue recognition, capitalisation, fiscal year. Ask an accountant where these materially affect the answer.
- **Organisation conventions**: how they name lines, structure sheets, colour inputs, and present outputs. Follow them.
- **Data available** for assumptions: customer data, funnel metrics, cohorts, cost records. Use `data-analysis` to derive assumptions from it rather than guessing.
- **The audience's expectations**: an investor deck, a board pack, an internal decision memo — each expects different outputs.

## Working with and without tools

**With a spreadsheet or code environment:** build the model with separated inputs, calculations, and outputs (see `spreadsheet-modeling`); compute the checks programmatically; generate sensitivity tables automatically. Do not store credentials or sensitive financial data in places they should not go; treat company financials as confidential.

**Without execution:** reason through the model in text — list drivers and assumptions, show the formulas, and calculate representative periods step by step so the user can verify. Be explicit about rounding and arithmetic; double-check multiplication and unit conversions, which are where errors hide.

**When given a model to review:**

1. Read the question it answers and its outputs first, so you know what matters.
2. Trace the two or three most important outputs back to their inputs; note every hardcoded value and every step you cannot follow.
3. Run the mechanical checks (balancing, totals, units, signs, periods).
4. Identify the most sensitive assumptions and compare each with evidence — history, benchmarks, customer data.
5. Check implied metrics for realism.
6. Check internal consistency of scenarios.
7. Report findings by severity: errors that change the decision first, then fragile assumptions, then structural and presentation issues. Suggest specific fixes, and respect the author's conventions when proposing changes.

## Pitfalls

- **Hockey-stick revenue** with no mechanism: growth that accelerates without any driver changing.
- **Top-down only**: "1% of a large market" with no route to acquiring those customers.
- **Revenue up, costs flat.** Ignoring the variable and semi-variable costs of growth.
- **Ignoring ramp time and lags** in hiring, sales productivity, and marketing.
- **Profit mistaken for cash.** Missing receivables, inventory, prepayments, capital spending, debt repayment.
- **Annual granularity for runway**, hiding a cash crunch mid-year.
- **LTV inflated** by revenue instead of margin, by ignoring churn, or by assuming lifetimes longer than the business has existed.
- **Hardcoded numbers** buried in formulas; outputs typed over calculations.
- **Unit and period mismatches**: monthly churn applied as annual, percentages entered as whole numbers.
- **Plugs** to make the balance sheet balance.
- **Single-scenario thinking** and false precision (forecasts to the unit five years out).
- **Inconsistent scenarios**, e.g. a downside with lower revenue but unchanged hiring.
- **Benchmark misuse**: citing averages from different segments or stages as if they apply.
- **Over-engineering**: hundreds of lines no decision depends on, making errors hard to find.
- **Undocumented assumptions**, so no one can update or challenge the model.
- **Ignoring taxes, fees, and financing costs** that are material to the decision (sales taxes, payment processing, interest), or modelling them without flagging that the rules depend on jurisdiction.
- **Anchoring on the plan.** Treating last quarter's forecast as the baseline instead of re-forecasting from actuals; compare forecast to actuals regularly and learn which assumptions were wrong.
- **Model-as-advocacy.** Tuning assumptions until the model supports a conclusion already reached; keep a record of assumption changes and their reasons.

## Quality bar and verification

Before delivering, check:

- [ ] The decision and audience are stated; the model contains what that decision needs and little more.
- [ ] Outputs are driven by explicit, documented assumptions with sources, units, and confidence.
- [ ] Inputs, calculations, and outputs are separated; no hardcoded numbers in calculations.
- [ ] Unit economics are computed with all variable costs and are positive (or the implication is clear).
- [ ] Revenue is built from a mechanism and cross-checked top-down.
- [ ] Costs scale consistently with volume; ramp-up and lags are included.
- [ ] Cash is modelled at sufficient granularity; runway and minimum cash are shown if relevant.
- [ ] If three statements are linked, the balance sheet balances every period without plugs.
- [ ] Sensitivity identifies the few assumptions that matter; scenarios are internally consistent.
- [ ] Implied metrics have been compared with reality and history.
- [ ] Limitations and advice boundaries (investment, tax, legal) are stated where relevant.

A useful final test: ask "what would have to be true for this plan to fail?" If the model cannot answer that quickly — by showing the sensitive assumptions and their thresholds — it is not yet doing its job.

## Related skills

- `spreadsheet-modeling` — structuring and building the model in a spreadsheet.
- `data-analysis` — deriving assumptions from historical data.
- `statistical-analysis` — forecasting methods and uncertainty.
- `competitive-analysis` and `web-research` — market and pricing inputs.
- `technical-decision-making` — framing build-vs-buy and investment decisions.
- `presentations` and `business-communication` — presenting model results.
