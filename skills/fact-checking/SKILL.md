---
name: fact-checking
description: >-
  Verify the factual claims in a document, article, report, speech, social
  post, or AI-generated answer: extract checkable claims, trace each to
  primary sources, verify numbers, statistics, quotes, dates, names, and
  attributions, detect claims that are technically true but misleading
  through missing context, rate confidence, and document sources so others
  can audit the result. Includes catching hallucinated or misattributed
  citations, fabricated quotes, and invented references in LLM output. Use
  when asked to "fact-check", "verify this", "is this true", "check these
  sources/citations", "are these references real", "check the numbers", or
  before publishing anything that makes factual claims. For broad topic
  research use web-research; for editing prose use writing-review-and-editing.
metadata:
  category: quality
  related: web-research, literature-review, writing-review-and-editing, ai-content-authenticity, statistical-analysis, data-analysis, llm-evaluation, technical-writing
---

# Fact-Checking

Fact-checking is the disciplined attempt to find out whether each claim in a piece is true, as stated, in context, and supported by evidence someone else can inspect. It is adversarial toward the text and neutral toward its conclusions: the checker's job is to try to break each claim, not to agree or disagree with the argument.

## Scope

Covers verifying existing claims in any text: journalism, reports, marketing copy, academic and technical writing, speeches, social media posts, internal documents, and outputs from language models. Covers citations and references, numbers and statistics, quotations, dates, names, titles, images and their captions at the level of provenance, and context.

Not covered:

- Researching a topic from scratch to produce new findings — `web-research`, `literature-review`.
- Re-analysing data to produce new statistics — `data-analysis`, `statistical-analysis` (a checker re-derives a number to confirm it, not to make new claims).
- Editing for clarity and style — `writing-review-and-editing`.
- Forensic image and video verification beyond basic provenance checks; specialist tools and training exist for that.

## Core principles

**1. Check claims, not topics.** A claim is a specific, checkable statement: "Unemployment fell to 3.9% in March." "Experts warn the economy is fragile" is barely checkable; "The central bank's governor said on 12 March that growth would slow" is. Break text into atomic claims before checking anything, or you will verify the gist and miss the wrong detail.

**2. Go to the primary source.** The primary source is the original origin of the information: the dataset, the study, the official record, the full transcript or recording, the court filing, the press release, the company filing. Secondary sources (news coverage, summaries, Wikipedia, blog posts, other AI answers) are useful for finding primary sources, not for confirming claims. Errors propagate: a mistake in one widely-copied article appears in hundreds of others, which then look like independent confirmation.

**3. Independent confirmation means independent origins.** Ten articles that all cite the same press release are one source. When a primary source is unavailable, look for sources that obtained the information independently.

**4. True words can mislead.** A claim can be literally accurate and still deceptive: a percentage increase from a tiny base, a cherry-picked time window, a quote stripped of the sentence that reversed it, a correlation presented as cause, an old photo presented as new. Checking includes asking whether the claim, as a reader would understand it, matches reality.

**5. Absence of evidence is a finding, not a verdict.** "I could not find a source" does not mean the claim is false. Report what was searched and found, and rate accordingly. Equally, do not upgrade a claim to "true" because it sounds plausible or nobody has disputed it.

**6. Show your work.** A check is only as useful as its documentation. Record for every claim what was checked, against what source (with a specific locator: page, table, timestamp, URL, access date), and what was found, so an editor or reader can audit the result without redoing it.

**7. Calibrated confidence.** State how sure you are and why. Distinguish "confirmed by primary source", "supported by reliable secondary sources", "unverified", "disputed", "contradicted by evidence", and "misleading in context". Overconfident verdicts damage trust as much as errors in the original.

## Process

### 1. Clarify the task

- What is the piece, who publishes it, and to whom? The bar is higher for publication, legal, medical, financial, and safety-related claims.
- Check everything, or only certain claims (numbers, quotes, the key claims, anything about named people)? With limited time, prioritize (step 3).
- What access do you have? Web browsing, databases, paywalled journals, the author's notes and sources, the ability to contact people? If you cannot browse, say so plainly; you can still extract claims, flag implausible ones, check internal consistency, and list what needs verification, but you must not present recall as verification.
- What date is the piece "as of"? Facts change: officeholders, prices, records, populations, laws.

### 2. Extract the claims

Read the text and list every checkable assertion, split into atoms. One sentence often contains several:

> "Founded in 1998 by two Stanford students, the company now handles more than 8.5 billion searches a day, roughly 90% of the global market."

Contains: founding year 1998; founders were two people; they were Stanford students (at founding? graduate students?); "now" handles over 8.5 billion searches daily (as of when, by whose measure?); global market share about 90% (which market definition, which measurer, which date?).

Include implicit claims: "the first", "the only", "the largest", "record", "unprecedented", "studies show", "experts agree", superlatives, and causal language ("led to", "because of"). These are high-risk because they are easy to write and hard to support.

Also extract claims carried by visuals and their captions, charts (does the chart match the data, are axes honest?), headlines (which often overstate the body), and links (does the linked page say what the text says it does?).

### 3. Prioritize

Check first:

- Claims central to the argument, headline, or conclusion.
- Claims about named people or organizations (defamation and fairness risk).
- Numbers, especially ones that drive decisions.
- Quotes, attributions, and citations.
- Surprising claims, superlatives, and claims that conveniently support the author's thesis. Surprise is a signal: things that are surprising are more often wrong.
- Claims in high-stakes domains: health, law, safety, finance, elections.

Lower priority: well-established background facts, though even these deserve a quick check when cheap (the boiling point of water at altitude, the year of a famous event, a commonly misquoted line).

### 4. Find and evaluate sources

For each claim, ask: who would know this first-hand, and where would they have recorded it?

| Claim type | Primary sources to look for |
|---|---|
| Official statistics | National statistics offices, central banks, international bodies (their own tables and releases, with revision dates) |
| Research findings | The paper itself (not the press release or abstract alone), its data and supplementary materials, registered protocols |
| Company facts | Regulatory filings, annual reports, official investor materials, company press releases (as the company's claim, not independent fact) |
| Laws and legal facts | The statute or regulation text, official gazettes, court records and judgments |
| Quotes and statements | Full recording or transcript, official transcript, the original publication where the statement first appeared |
| Historical events and dates | Archives, contemporaneous records, reputable reference works with citations, scholarly histories |
| Biographical facts | Official records, the person's own verified statements (weighed as self-reporting), reputable profiles with sourcing |
| Scientific consensus | Systematic reviews, consensus statements from major scientific bodies, not single studies |

Evaluate each source for: authority (are they positioned to know?), independence (do they have a stake?), method (how did they find out?), currency (is it the latest version, and has it been corrected, revised, or retracted?), and corroboration. Check retraction databases and journal notices for research. Check whether official figures have been revised since first release; first estimates of economic data often change.

Lateral reading is the most effective way to evaluate an unfamiliar source: rather than studying the site itself, leave it and search for what others say about the organization, its funding, and its track record.

### 5. Verify numbers and statistics

Numbers are where most errors live. For each one:

- **Find the exact figure in the source,** with its unit, date, geography, and definition. "Unemployment" has several official measures; "users" may be monthly active or registered; "revenue" may be gross or net.
- **Recompute derived figures:** percentages, changes, ratios, sums, per-capita values, conversions, inflation adjustments. Check percentage versus percentage-point confusion ("rose from 10% to 15%" is 5 points, 50%).
- **Check the base:** a 200% increase from 1 to 3 cases is true and almost meaningless. Ask for absolute numbers when only relative changes are given, and vice versa.
- **Check the comparison:** same definitions, same period lengths, same populations, same methods? Year-over-year versus quarter-over-quarter? Nominal versus real?
- **Check the window:** would a different start or end date change the story? Cherry-picked baselines are a common distortion.
- **Check precision:** "4.27 million" implies a precision the source may not have; estimates have uncertainty ranges, and surveys have margins of error. A difference smaller than the margin is not a difference.
- **Check correlation versus causation:** the source may show association; the text may claim cause. See `statistical-analysis`.
- **Check plausibility by order of magnitude:** does the number make sense given what you know (population sizes, typical prices, physical limits)? A per-person figure larger than plausible incomes or a market share above 100% when segments are summed signals an error.
- **Check rounding and consistency within the piece:** totals that do not add up, the same figure stated differently in two places.

### 6. Verify quotes and attributions

- Find the original: recording, transcript, original article, book page. Quotes drift as they are copied; famous quotes are frequently misattributed (to Einstein, Twain, Churchill, Lincoln, and others) or invented.
- Check the exact wording. Paraphrase presented in quotation marks is a misquote. Minor edits (removing "um") are conventional in many outlets; meaning-changing edits are not. Ellipses must not remove words that change meaning.
- Check the context: what came before and after, what question was being answered, whether the speaker was quoting someone else, being sarcastic, or hypothetical.
- Check the speaker, date, and venue.
- For translated quotes, check the original language where possible and whether the translation is fair.

### 7. Verify dates, names, and descriptions

- Dates: event date versus announcement date versus publication date; time zones for events near midnight; calendar differences for historical dates.
- Names: spelling (including diacritics), titles and roles as of the date referred to, organizations' current versus former names.
- Descriptions: "former" versus current roles, "only" and "first" claims, locations, ages (as of when?).

### 8. Check context and framing

For each claim that survives the literal check, ask:

- Would a reasonable reader come away with an accurate picture?
- Is anything important omitted that would change the interpretation (the drug reduced risk, but the absolute risk was tiny; crime rose this year, but is far below the decade average)?
- Is an old fact presented as current, or a local fact presented as general?
- Are images, videos, or charts from the event they claim to show? Reverse image search and checking metadata where available help with basic provenance; flag anything uncertain for specialist verification.
- Is a single study presented as settled science, or a fringe view presented as one side of an even debate?
- Is the claim framed with loaded language that the evidence does not support?

### 9. Rate each claim

Use a scale the publication or team uses, if any. Otherwise a clear set of categories works, applied consistently:

| Rating | Meaning |
|---|---|
| Confirmed | Matches a primary or authoritative source, in context |
| Supported | Consistent with reliable secondary sources; primary not located |
| Needs correction | Substantively right, but a detail is wrong (date, number, name, wording) — give the correction |
| Misleading | Literally accurate but creates a false impression — explain the missing context |
| Unsupported | No adequate source found after a reasonable search — state what was searched |
| Disputed | Credible sources disagree — summarize the positions and the state of evidence |
| False | Contradicted by reliable evidence |
| Opinion / not checkable | Value judgments, predictions, or claims too vague to verify — note if presented as fact |

Avoid inventing a confident rating to fill the column. "Unsupported" with a clear search record is a valid, useful result.

### 10. Document and report

For each claim record: the claim as written, its location, the rating, the source(s) with specific locators and access dates, a brief note on what the source says, and the suggested correction or rewording if needed. Archived copies of web sources (via web archive services) protect against later changes.

Report in a form the author or editor can act on: corrections and their sources first, misleading framings with suggested rewording, unsupported claims with what would support them, and confirmed claims briefly. Distinguish clearly between "this is wrong" and "I could not confirm this".

## Search techniques that find primary sources

When you can search, these methods locate originals faster than general queries:

- **Search exact phrases** in quotation marks: the precise statistic, a distinctive phrase from a quote, the exact title of a paper. Variations in wording across copies help trace a claim back to its earliest appearance.
- **Restrict by site or domain** to official sources (a statistics office's domain, a government domain, a court's site, a company's investor-relations site).
- **Restrict by date** to find the earliest mention, which is often the origin, and to see whether a figure has been updated.
- **Use scholarly indexes** for research claims: DOI resolvers and registries (e.g. doi.org, Crossref) to confirm a DOI belongs to the cited paper; bibliographic databases and search engines (e.g. PubMed, Google Scholar, Semantic Scholar, OpenAlex, discipline-specific indexes) to confirm a paper exists and find its full text; retraction databases to check status.
- **Use official legal databases** for statutes, regulations, and case law in the relevant jurisdiction; confirm case names, citations, courts, and dates match.
- **Use web archives** to see a page as it was when quoted, and to recover deleted pages.
- **Use reverse image search** and image metadata where available to find the earliest appearance of a photo.
- **Follow the citation chain** backwards: from the article to what it cites, to what that cites, until you reach the data or the original statement. Note where the chain breaks; that is often where the error entered.
- **Read the method section and tables,** not only the abstract or conclusions. Search the full text for the specific number.

Record the queries you ran for claims you could not verify; it shows the search was reasonable and saves the next person from repeating it.

## Worked example

Text to check: "A 2019 Harvard study found that remote workers are 47% more productive, which is why most Fortune 500 companies have now made remote work permanent."

Extracted claims: (a) a study exists, from 2019; (b) it was from Harvard; (c) it measured productivity of remote workers; (d) the effect was 47%; (e) most Fortune 500 companies have made remote work permanent; (f) the second fact happened because of the first.

Checking:

1. Search for the 47% figure with remote work and productivity terms. Suppose the figure traces to a survey by a software vendor reporting time spent on tasks, widely misreported as a "Harvard study" because a business-school publication wrote about it. Claims (a)–(c) need correction: wrong origin, and the measure was self-reported time on task, not productivity.
2. Look for peer-reviewed research on remote work productivity. Suppose it shows mixed results that depend on the job and how productivity is measured. The 47% figure is not representative; rating: misleading.
3. For (e), look for a primary survey of Fortune 500 policies with a date. Suppose the best source found shows most large companies use hybrid arrangements, with a minority fully remote. Rating: false as stated, with the correction.
4. Claim (f) asserts causation with no support. Rating: unsupported.

Suggested rewording for the author: describe the survey accurately with its source and measure, note that research findings on productivity are mixed, and state current corporate policy with a dated source.

The example shows the pattern: atomize, trace each atom to its origin, check what was actually measured, then check the logic connecting the claims.

## Scientific and health claims

These are among the most commonly distorted claims, because research is nuanced and coverage is not. Check:

- **Study type.** A lab or animal study does not show an effect in humans. An observational study shows association, not causation. A single trial is weaker than a systematic review or meta-analysis. Preprints have not been peer reviewed (which is not proof of quality either, but changes how claims should be phrased).
- **Population and dose.** Who was studied (age, condition, size of sample) and at what dose or exposure, versus who the text implies the result applies to.
- **Effect size and absolute risk.** "Doubles the risk" may mean from 1 in 100,000 to 2 in 100,000. Report absolute numbers alongside relative ones.
- **Endpoints.** A change in a biomarker is not the same as a change in illness or death.
- **Conflicts of interest and funding,** stated in the paper's disclosures.
- **Consistency with the wider evidence.** Does this result agree with reviews and major health bodies' guidance? If not, the text should say it is an outlier.
- **Whether the paper says what the press release says.** Press releases routinely exaggerate; check the results and limitations sections.

Health claims can cause direct harm; a misleading claim about treatment deserves a higher priority and more conservative rating than most other errors.

## Charts and visual data

A chart can misstate data without a single false number. Check:

- The chart's data matches the cited source, for the stated period and units.
- The y-axis: truncated baselines exaggerate small differences in bar charts (bars should start at zero); dual axes can manufacture apparent correlations.
- Selective time windows, missing data points, or smoothing that hides variation.
- Area or 3D effects that distort proportions.
- Labels, legends, and titles that claim more than the data shows ("soaring" over a flat-ish line).
- Maps that show raw counts where rates per population are the meaningful measure.

See `data-visualization` for what honest charts look like.

## Technical and code claims

Claims about software (a function exists, an option does what the text says, a version supports a feature, a command produces a given output) are checkable by the most primary source there is: the software itself. If you can execute code, run it in a safe, isolated environment; otherwise check the official documentation and release notes for the specific version. Model-generated technical text frequently names plausible functions, flags, and configuration keys that do not exist.

## Corrections and fairness

When a check finds an error in published work, the correction should be specific (what was wrong, what is right, source), proportionate (as visible as the error where possible), and dated. When claims concern a named person or organization and are negative, the bar is higher: confirm with the strongest available source, and recommend giving the subject a chance to respond before publication. Fact-checking findings about individuals are themselves claims and must meet the same standard.

## Checking AI-generated content

Language-model outputs need checking with particular attention to failure modes that human writers rarely produce at the same rate:

- **Fabricated citations.** References with plausible authors, titles, journals, years, volumes, and DOIs that do not exist, or that exist but say something else. Check every reference: search the exact title; resolve the DOI (a DOI that resolves to a different paper is a strong sign of fabrication); confirm authors, year, and venue match; then open the source and confirm it supports the specific claim it is cited for. A real paper cited for a claim it does not make is as bad as a fake one.
- **Fabricated or blended quotes.** Quotes that sound like the person but cannot be found, or that merge two statements. Treat any quote from an AI output as unverified until found in an original source.
- **Plausible but invented specifics.** Statistics, dates, case names, legal citations, product features, API functions, version numbers, and URLs that fit the pattern of real ones. Invented URLs and legal case citations are common; check that each one exists and says what is claimed.
- **Confident outdated information.** Training data has a cutoff; officeholders, prices, versions, laws, and records may have changed. Check anything time-sensitive against a current source.
- **Conflation.** Two similarly named people, organizations, studies, or places merged into one.
- **Consensus misstatements.** Presenting a contested view as settled, or settled science as contested, or inventing a consensus ("most experts agree").
- **Self-consistency is not evidence.** Asking the same model again, or asking it whether its citation is real, does not verify anything; it may confidently confirm a fabrication. Verification requires an external source.

If you are a model checking your own or another model's output and you cannot access external sources, say so explicitly, flag every citation, quote, statistic, and specific detail as unverified, and do not "confirm" from memory. Your recall is the same kind of evidence that produced the error.

## Decision guidance

**How much checking is enough?** Scale to stakes and reach:

| Situation | Depth |
|---|---|
| Internal draft, low stakes | Key numbers and any named-person claims |
| Published article, report, or marketing | Every factual claim, with priority on central claims, numbers, quotes |
| Legal, medical, financial, safety, or election-related content | Every claim against primary sources; second reviewer; legal review for claims about individuals |
| AI-generated content to be used as fact | Every citation, quote, statistic, and specific detail, regardless of how plausible |

**When sources conflict:** prefer the source closer to the event or data, with better method, more independence, and more recent correction status. If the conflict is genuine (expert disagreement, uncertain data), report it as disputed rather than picking a side, and say which way the weight of evidence leans and why.

**Correct, soften, or cut?** Correct when the right fact is known. Soften (add hedges, attribution, or context) when the claim is plausible but not fully supported: "according to the company" rather than stating it as fact. Cut when the claim cannot be supported and is not essential, or when it concerns a person and cannot be substantiated.

**Contacting people.** Professional fact-checkers often verify with the subjects and sources. If you are working on someone's behalf, suggest which people or organizations could confirm specific claims; do not contact anyone yourself without explicit permission.

## Discovering context

- Ask for the author's source notes, links, and data; checking against the author's own sources first is fast and reveals misreadings.
- Find the publication's standards: rating scales, correction policy, attribution rules, style for citing sources.
- Note the piece's date and the jurisdiction or region it addresses, since facts and laws are local and time-bound.
- Identify the audience's likely interpretation, which defines what "misleading" means.

## Pitfalls

- **Checking the gist instead of the details.** "The study showed it works" passes; the specific "40% reduction" is wrong.
- **Citation laundering.** Accepting a secondary source that cites another secondary source that misread the original.
- **Circular confirmation.** Many outlets repeating one origin.
- **Confirmation bias.** Checking claims you doubt more rigorously than claims you agree with. Apply the same standard to both.
- **Trusting the abstract or press release.** Results, limitations, and effect sizes in the paper often differ from the summary.
- **Missing revisions and retractions.** Statistics revised, papers retracted, articles corrected after first publication.
- **Search-engine authority.** Top-ranked is not the same as reliable; AI-generated summaries in search results can repeat errors.
- **Recall as verification.** Especially for models: "I believe this is correct" is not a check.
- **Overreaching verdicts.** Calling a claim "false" when it is unsupported, or "true" when it is literally accurate but misleading.
- **Ignoring visuals and headlines,** where distortion is often greatest.
- **Undocumented checks** that cannot be audited or reused.
- **Checking only what is stated.** The most misleading pieces often mislead through what they leave out; ask what a fair account would add.
- **Fatigue at the end.** Claims in the last third of a long piece get less scrutiny. Track claims in a list so none is skipped.
- **Treating a model's citation format as evidence.** A correctly formatted reference with a DOI and page numbers is no more likely to be real than a sloppy one.

## Quality bar and verification

- [ ] Every checkable claim was extracted, including implicit claims, superlatives, numbers, quotes, captions, and links.
- [ ] Each claim has a rating from a consistent scale, with the reason.
- [ ] Each confirmation cites a specific primary or authoritative source with a locator and access date.
- [ ] Numbers were recomputed, with definitions, units, dates, and bases checked.
- [ ] Quotes were found in original form and checked for context.
- [ ] Every citation was resolved and confirmed to exist and to support the specific claim.
- [ ] Context and framing were assessed, and misleading claims have suggested rewording.
- [ ] "Could not verify" is clearly distinguished from "false".
- [ ] Time-sensitive facts were checked against current sources, with the as-of date noted.
- [ ] If external sources were unavailable, the report says so and marks claims unverified rather than confirming from memory.
