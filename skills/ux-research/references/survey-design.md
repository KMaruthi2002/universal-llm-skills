# Survey Design

Read this before writing, fielding, or analysing a survey. Surveys are deceptively easy to make and very easy to make badly; the output always looks precise, which hides how wrong it can be.

## When a survey is the right tool

Use a survey when you already know **what dimensions matter** and need to know **how they are distributed** across a population, or to track an attitude over time. Do not use a survey to discover what matters (interview first), to judge usability (observe instead), or to predict behavior (people are poor forecasters).

## Plan from the analysis backwards

Before writing questions, write down the analyses you will run: "compare satisfaction between admins and end users", "rank the five pain points by frequency", "estimate the share of teams using a spreadsheet workaround". Every question should feed one of these. Questions that do not are cut; they cost completion rate.

## Question types

| Type | Use for | Notes |
|---|---|---|
| Single choice | Mutually exclusive categories | Make options exhaustive and non-overlapping; add "Other (please specify)" and "Not applicable" where relevant |
| Multiple choice | Non-exclusive behaviors | Consider "select up to three" to force prioritization |
| Rating scale (Likert-style) | Agreement, satisfaction, frequency | Label every point or at least the ends and midpoint; keep the direction consistent |
| Ranking | Relative priority | Hard beyond 5–7 items; consider max-diff or "pick top three" instead |
| Numeric | Counts, amounts | Ask for a reasonable unit and range; validate input |
| Open text | Explanations, unexpected answers | Use sparingly; one or two per survey; costly to analyse |
| Behavioral frequency | How often something happens | Use concrete periods ("in the last 30 days") rather than "often/sometimes" |

## Wording bias and how to avoid it

- **Leading wording**: "How much do you enjoy our new design?" presumes enjoyment. Use "How would you rate…".
- **Loaded terms**: "bloated", "simple", "powerful" carry judgments. Use neutral descriptions.
- **Double-barrelled**: "How satisfied are you with the speed and reliability?" Split it.
- **Acquiescence bias**: people tend to agree with statements. Balance agree/disagree items, or prefer item-specific scales ("How easy or difficult was…").
- **Social desirability**: people over-report virtuous behavior. Ask about specific recent behavior, assure anonymity, and avoid judgmental framing.
- **Recall limits**: "In the last year, how many times…" is unreliable for frequent events. Shorten the window.
- **Jargon**: test that participants understand every term the way you do.
- **Order effects**: earlier questions prime later ones. Put general questions before specific ones; randomize option order for lists without natural order.
- **Missing options**: if a respondent's true answer is absent, they pick something wrong. Include "Don't know" / "Not applicable" where genuine.

## Scales

- Five or seven points are common and adequate. Odd numbers allow a neutral midpoint; remove it only when you deliberately want to force a lean, and say so.
- Keep polarity and direction consistent through the survey to reduce errors.
- Standardized instruments (e.g. SUS for perceived usability, other validated questionnaires) are worth using as-is when they fit, because you can compare with benchmarks. Do not modify their wording if you want comparability.
- A single-question metric (NPS-style "likelihood to recommend") is widely used but contested; it is a weak proxy for most product questions. Use it if the organization already tracks it, and pair it with a "why" question and behavioral data.

## Sampling

- **Define the population** precisely ("active accounts in the last 90 days, all plans").
- **Sampling frame**: the list you actually draw from. Mismatches between frame and population are the most common source of bias (e.g. surveying only users who open marketing emails).
- **Non-response bias**: the people who answer differ from those who do not, usually being more engaged or more upset. Compare respondent characteristics against the population where possible, and report response rate.
- **In-product intercepts** reach active users and miss lapsed ones. Emailed surveys reach whoever reads email. Panels reach panelists. Say which you used.

**Margin of error, roughly**: for a proportion near 50% from a simple random sample, the 95% margin of error is about ±1/√n. So n=100 gives about ±10 points, n=400 about ±5, n=1,000 about ±3. This assumes random sampling, which most product surveys do not achieve; real uncertainty is larger. Subgroup comparisons need adequate n *in each subgroup*. See `statistical-analysis` for rigorous treatment.

## Length and completion

- Aim for a survey a typical respondent finishes in a few minutes. Completion drops and answer quality degrades as length grows; straight-lining (same answer down a grid) is a symptom.
- Show progress. Avoid large grids on mobile.
- Put screening questions first (to end early for ineligible respondents), sensitive and demographic questions last.

## Piloting

Pilot with 3–5 people from the target population, ideally with them thinking aloud while answering. Watch for hesitation, re-reading, and answers that do not match what they say aloud. Then soft-launch to a small slice of the sample and check data for problems (unexpected skews, a broken skip logic, a dominant "Other").

## Analysis

- Clean first: remove speeders (impossibly fast completions), straight-liners, duplicates, and ineligible respondents; document how many and why.
- Report distributions, not just means, for rating scales. Means of ordinal scales hide polarization.
- Report n for every figure, especially subgroups.
- Code open-text responses with a codebook built from a sample, then applied consistently; report code frequencies and illustrative quotes.
- Distinguish statistically meaningful differences from noise; small differences between subgroups are often within error.
- Never weight, filter, or slice repeatedly until a desired result appears. Decide key analyses up front.

## Ethics specific to surveys

- State purpose, length, anonymity or confidentiality, and data use at the start.
- Do not collect identifying data unless needed; if you link responses to accounts, say so.
- Keep sensitive questions optional.
- Do not survey the same people repeatedly in short periods; coordinate with other teams to avoid fatigue.
