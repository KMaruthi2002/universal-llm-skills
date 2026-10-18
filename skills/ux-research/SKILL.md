---
name: ux-research
description: >-
  Plan, run, and synthesize user research: framing research questions,
  choosing methods (interviews, contextual inquiry, surveys, diary studies,
  usability tests, analytics, card sorts) by what you need to learn,
  recruiting and screening participants, interview technique without leading
  questions, affinity mapping and thematic synthesis, turning observations
  into insights, and research ethics and consent. Use when someone wants to
  understand users, validate a problem, write a discussion guide or survey,
  plan a study, recruit participants, or make sense of research notes. For
  evaluating a specific interface's usability use usability-evaluation; for
  controlled A/B tests use experiment-design.
metadata:
  category: design
  related: usability-evaluation, information-architecture, experiment-design, product-requirements, user-stories, data-analysis, statistical-analysis, competitive-analysis, requirements-analysis, accessible-design
---

# UX Research

User research exists to reduce the risk of building the wrong thing, or the right thing badly. It is not a ritual, a validation stamp, or a way to win arguments. Good research changes or sharpens a decision; research that could not have changed anything was a waste of participants' time and yours.

This skill covers generative and evaluative research end to end: deciding what to learn, picking the method, recruiting, collecting data, synthesizing, and reporting. It adapts to any domain (consumer, enterprise, internal tools, public services, hardware) and any team size, including the common case of one person doing research part time.

**Out of scope, handled elsewhere:**

- Running and scoring usability tests of a specific design in detail: `usability-evaluation`.
- Statistically powered A/B and multivariate experiments: `experiment-design`, `statistical-analysis`.
- Structuring navigation and taxonomy from card-sort results: `information-architecture`.
- Turning findings into requirements and stories: `product-requirements`, `user-stories`.
- Market sizing and competitor features: `competitive-analysis`.

## Core principles

**1. Start from the decision, not the method.** Ask "what will we do differently depending on what we learn?" before "should we do interviews?" A research question tied to a decision has a natural scope, a natural end, and an audience who cares about the answer. A method chosen first tends to produce interesting-but-useless data.

**2. Behavior beats opinion; past beats future.** People are unreliable narrators of their own preferences and terrible predictors of their future behavior. "Would you use a feature that…?" produces polite yeses. "Tell me about the last time you…" produces evidence. Observed behavior (what they do) outranks reported behavior (what they say they do), which outranks stated preference (what they say they would like).

**3. Match the method to the kind of knowledge.** Qualitative methods answer *why* and *how*, and discover things you did not know to ask. Quantitative methods answer *how many* and *how much*, and only measure things you already knew to ask about. Mixing them is powerful when each covers the other's blind spot; substituting one for the other is a category error.

**4. Small samples find problems; large samples measure them.** Five to eight participants per distinct user segment usually surface the major themes or usability problems, because recurring issues recur fast. That small sample cannot tell you prevalence. Do not report "60% of users want X" from five interviews.

**5. Separate observation from interpretation.** "Three of six participants exported to a spreadsheet before sharing" is an observation. "Users don't trust our charts" is an interpretation. Keep them distinct in notes and in synthesis so others can check your reasoning and so you notice when you have leaped.

**6. The participant is the expert; you are the student.** Your job in a session is to understand their world, not to pitch, teach, or defend the product. The moment you explain how something "should" work, the data becomes about your explanation.

**7. Research is a relationship with real people.** Participants give time, attention, and sometimes sensitive information. Consent, privacy, fair compensation, and honest use of their data are not paperwork; they are the conditions under which research is legitimate.

## Process

### 1. Frame the research question

Write down, with the stakeholders if possible:

- **The decision** this research informs ("whether to build bulk editing this quarter", "which of two onboarding directions to pursue").
- **What you already know**, with sources: analytics, support tickets, sales notes, previous studies, competitor patterns. Read prior research before planning new research; repeating a study someone already ran is common and avoidable.
- **What you need to learn**, as 3–6 specific questions. "How do finance teams currently reconcile invoices, and where does it break down?" is answerable. "What do users want?" is not.
- **Assumptions to test**, ranked by how much damage they would cause if wrong and how little evidence supports them. Research the risky, unsupported ones first.

If the stakeholder's real question is "prove my idea is good", say so gently and reframe toward "find out whether and for whom it would be valuable". Research designed to confirm will confirm.

### 2. Choose the method

Pick by the type of question, how much you already know, and constraints (time, budget, access to participants).

| You need to learn… | Strong methods | Why | Watch out for |
|---|---|---|---|
| How people currently do a job, their goals, workarounds, context | Semi-structured interviews, contextual inquiry (observe in their environment) | Rich, discovers unknown unknowns | Small samples; interviewer bias |
| What happens over time, in real life | Diary study, longitudinal check-ins | Captures moments interviews forget | Participant fatigue; dropout; heavy analysis |
| Whether people can use a design | Usability testing (moderated or unmoderated) | Direct behavioral evidence | Testing tasks you scripted, not their real goals |
| How many people have a trait or attitude | Survey (with a sound sample) | Prevalence and segmentation | Bad questions produce precise-looking garbage |
| What people actually do in the product, at scale | Product analytics, logs, funnel analysis | Real behavior, large N | Tells you what, never why; instrumentation gaps |
| How people group and name content | Open or closed card sort | Reveals mental models for IA | Results are input to IA, not an IA |
| Whether people can find things in a structure | Tree testing | Isolates navigation from visual design | Labels only; no context of a real page |
| Which variant performs better on a metric | A/B test | Causal evidence | Needs traffic; only compares what you built |
| What the competitive landscape offers | Competitive teardown, review mining | Cheap, fast | Copying competitors' mistakes |
| Unmet needs in a new space | Interviews + field observation, then a survey to size | Discovery then quantification | Skipping straight to the survey |

Combinations that work well:

- **Interviews → survey**: discover the dimensions qualitatively, then measure their distribution.
- **Analytics → interviews**: analytics shows where people drop off; interviews explain why.
- **Card sort → tree test**: generate a structure from mental models, then verify findability.
- **Diary study → follow-up interview**: diary captures moments; the interview probes them.

Choose a cheaper method when the decision is reversible and low stakes. Invest in heavier methods (field studies, diary studies, large surveys) when the decision is expensive to reverse.

### 2a. Write a short research plan

A plan is how stakeholders agree on scope before anyone is recruited. Keep it brief; its value is alignment, not documentation. It should make clear:

- the decision and the research questions;
- the method and why it fits those questions (and what it cannot answer);
- who participants are, how many, how they will be recruited and compensated;
- the timeline, including synthesis time (often as long as fieldwork);
- what will be delivered, to whom, and when;
- consent, recording and data-handling arrangements.

Share it with the people who will act on the findings and ask, explicitly, "If we learn X, would you do something different?" If the answer is no for every plausible X, rescope.

### 3. Define participants and recruit

**Who to talk to** depends on the question, not on who is easy to reach.

- Define criteria by **behavior** ("has submitted an expense report in the last month") rather than demographics or self-labels ("is a power user"). Behavior is verifiable and relevant; demographics usually are not, unless the question is about them.
- Include the edges deliberately: new users, churned users, non-users who chose a competitor, people using assistive technology, people in low-connectivity or low-literacy contexts if relevant. The center of your user base is the least informative group about what is broken.
- Segment where segments plausibly differ (e.g. admins vs. end users, small vs. large organizations) and recruit 5–8 per segment for qualitative work, rather than 8 total spread thin.

**Screeners** filter for the right people without revealing the "correct" answers. Ask about behavior with multiple-choice options that include decoys, and do not name the product or the feature being studied if that would let people self-select or game the screener. Include an articulation check (one open question) for interviews, because some participants cannot or will not talk at length.

**Sources**: existing customers (via the product, support, account managers), recruiting panels, community channels, intercepts, referrals. Customers recruited through sales or account managers skew toward happy, engaged accounts; correct for it.

**Compensation**: pay fairly for time, at rates appropriate to the participant's profession and locale. Under-paying skews the sample toward people with the most free time. For employees of customers, check whether they are permitted to accept incentives; offer an alternative (charity donation) if not.

**Over-recruit** by roughly 20–30% for no-shows, and schedule pilots.

### 4. Write the guide or instrument

**Interview guide**: a loose structure, not a script. Typical arc:

1. Warm-up: their role and context, easy questions that get them talking.
2. The core: walk through specific recent episodes of the behavior you care about. Most of the time goes here.
3. Probes into pain points, workarounds, tools, people involved, what "good" looks like for them.
4. (Optional) reaction to a concept or prototype, only after you have heard their unprompted world.
5. Wrap-up: "Is there anything I should have asked?" and thanks.

Write more questions than you need, mark the must-ask ones, and expect to skip and reorder. Follow the participant's story, not the list.

**Survey**: see `references/survey-design.md` for question construction, scales, sampling and bias. Key points: every question earns its place by mapping to a research question; pilot it on 3–5 people and watch them answer; put sensitive and demographic questions at the end; keep it short enough to finish without fatigue.

**Diary study**: define the trigger ("each time you…") or cadence, the minimum entry (a photo plus one sentence is often enough), the channel participants already use, and a check-in schedule to keep engagement. Plan for at least a week, longer for infrequent behaviors.

### 5. Run sessions well

**Interview technique** (the full question-craft guide is in `references/interview-technique.md`):

- Ask about specific past instances: "Walk me through the last time you…". Generalities ("How do you usually…?") produce idealized answers.
- Ask open, neutral questions. "How did that go?" not "Was that frustrating?"
- Use silence. After an answer, wait a few seconds. People fill silence with the interesting part.
- Probe with their words: "You said it was 'a mess' — what made it a mess?"
- Ask for demonstration where possible: "Could you show me?" Screens and artifacts (spreadsheets, sticky notes, printed forms) are gold.
- Do not pitch, defend, explain, or correct. If they misunderstand the product, that is a finding.
- When they propose a solution ("you should add a button for X"), ask what problem it would solve for them. Solutions from participants are clues to needs, not requirements.
- Note non-verbal cues and hesitation, but interpret them cautiously.

**Logistics**: one moderator, ideally one note-taker. Record (with consent) so you can quote accurately. Debrief for 10 minutes immediately after each session while memory is fresh: top surprises, notable quotes, what to change in the guide.

**Pilot** the guide with one person (a colleague will do in a pinch) to catch confusing questions, timing problems, and broken prototypes.

**Remote vs. in-person**: remote is cheaper, wider-reaching, and fine for most interviews and usability tests. In-person or in-context is worth the cost when environment matters (physical workflows, shared screens, noise, devices, workplaces), or for participants who are less comfortable with video tools.

### 6. Synthesize

Synthesis is where most research value is created or lost. Go from raw data to findings in stages, keeping the trail visible.

1. **Extract atomic observations.** One observation per note: a quote, an action, a context detail, tagged with the participant ID. Keep the participant's words where possible.
2. **Affinity map.** Group notes bottom-up by similarity, without starting from predefined categories. Name groups only after they form. Expect to regroup several times; the first grouping usually mirrors your guide's structure, which means you have not yet synthesized.
3. **Look across participants.** For each cluster, note how many participants and which segments contribute. A theme that comes from one vocal person is a hypothesis, not a theme.
4. **Find tensions and contradictions.** Where participants disagree, there may be a segment boundary or a hidden variable (company size, experience, role). These are often the most useful findings.
5. **Write insights.** An insight states a non-obvious truth about users, why it matters, and evidence for it. See the distinction below.
6. **Connect to the decision.** For each insight, state the implication: what it suggests the team should do, explore, or stop doing. Separate implications (your recommendations) from the insight itself.

**Observation → finding → insight**, illustrated:

- *Observation*: P2, P4 and P5 copied report figures into a separate spreadsheet before presenting to their managers.
- *Finding*: Most participants re-create reports outside the product before sharing upward.
- *Insight*: Participants don't trust that the in-product report will be understood by their managers, who never log in; the product's real output is a number pasted into someone else's slide. *Evidence*: 4 of 6, quotes from P2 and P5, observed in sessions.
- *Implication*: Investigate shareable, self-explanatory exports before investing further in in-product dashboards.

An insight that a stakeholder would read and say "obviously" is either not an insight or needs sharper framing of what is surprising about it.

**Synthesizing quantitative and behavioral data alongside qualitative.** When analytics, logs, or surveys are part of the study, use each to check the other. If interviews say "everyone exports to spreadsheets" and analytics show 4% of accounts ever export, the interviews over-sampled a segment or exports happen outside the instrumented path; find out which before reporting either. Triangulated findings (two independent sources agree) deserve more confidence than single-method ones, and the report should say which is which.

**Synthesizing at volume.** With dozens of sessions or thousands of open-text responses, build a codebook from a sample (tag names, definitions, inclusion and exclusion examples), apply it consistently, and have a second person code a subset to check agreement. Report code frequencies with the caveat that they reflect what people chose to mention, not true prevalence.

**Frameworks** (journey maps, jobs-to-be-done statements, personas, mental model diagrams, service blueprints) are communication tools for synthesized knowledge. Choose one only if it helps the audience act. Personas built on demographics and stock photos rather than behavior and goals mislead more than they help; if you make them, ground every attribute in data and state which segment and sample they represent.

### 7. Report and share

- Lead with what the audience needs to decide, then the insights that support it, then method and caveats.
- Make evidence inspectable: quotes, clips (with consent), counts, participant profiles (anonymized).
- State the limits: sample, segments not covered, method biases, what this cannot tell you.
- Match format to audience and the organization's existing habits (a short readout, a document, a workshop, a recorded walkthrough). A synthesis workshop where stakeholders handle the data themselves builds more buy-in than any deck.
- Store findings where they can be found later (the team's existing research repository, wiki, or docs), tagged by topic and date. Research nobody can find gets repeated.

## Discovering context

Before planning research in an existing organization or product:

- **Look for prior research**: research repositories, wiki pages, past readouts, persona documents, support ticket themes, NPS or CSAT verbatims, sales call notes. Ask who has talked to users recently.
- **Check the data that already exists**: analytics events, search logs (what people search for and fail to find), support tags, app-store reviews, community forums. These are cheap and often answer the question outright.
- **Find the constraints**: legal or privacy rules on contacting users, consent templates, approved recruiting channels, incentive policies, data-retention rules, whether recordings may be stored and where.
- **Learn the team's vocabulary and formats**: how they write up findings, whether they use personas or jobs, how decisions get made. Fit the output to how it will actually be consumed.
- **Identify the real audience** of the findings and involve them early: invite them to observe sessions. Stakeholders who watched a participant struggle need far less persuading.

## Ethics, consent, and data handling

Treat these as hard requirements, not suggestions.

- **Informed consent.** Before the session, tell participants in plain language: who you are, the purpose, what you will do, how long it takes, whether it is recorded, who will see the data, how long it is kept, that they can skip any question or stop at any time without losing their incentive. Get explicit agreement, recorded or written, per your organization's process. Re-confirm before starting recording.
- **Minimize data.** Collect only what the research question needs. Do not ask for sensitive data (health, finances, immigration status, sexuality, etc.) unless it is central to the question and you have appropriate approvals and safeguards.
- **Anonymize in outputs.** Use participant IDs. Remove names, employers, and identifying details from quotes and clips. Be careful with small populations where a role plus a company size identifies someone.
- **Secure storage.** Keep recordings and raw notes in access-controlled locations; delete them per the stated retention period. Never paste identifiable participant data into tools or services not approved for it, including AI tools, unless consent and policy cover that use.
- **No deception without justification.** If a study requires withholding its purpose (e.g. a fake-door test), keep it minimal, debrief afterwards, and get the review your organization requires.
- **Vulnerable participants.** Minors, people in crisis, patients, people with cognitive disabilities, and people in dependent relationships (employees evaluating their own employer's tools) need extra care: guardian consent, ethics review where required, a trained moderator, and an exit plan if a session becomes distressing.
- **Power dynamics.** Customers may fear that criticism affects their account; employees may fear their manager. Say explicitly that honest feedback is the goal and will not be attributed.
- **Analytics and observational data.** Using product data is research too. Respect what users agreed to in the privacy policy, aggregate where possible, and avoid singling out individuals.
- **Accessibility of the research itself.** Offer accommodations (captions, screen-reader-compatible materials, extra time, alternative formats). Excluding disabled participants because the session format is inaccessible biases every finding.

## Decision guidance

**Moderated vs. unmoderated sessions.** Moderated when you need to probe, the prototype is fragile, the domain is complex, or participants need support. Unmoderated when tasks are well-defined, you want more participants quickly, and you can live without follow-up questions.

**Interviews vs. survey for "what do users want?".** Interviews first if you do not yet know the dimensions of the answer. A survey only after you know what options to offer; otherwise you measure your own assumptions.

**How many participants?** Qualitative: 5–8 per segment, stop when new sessions stop producing new themes (saturation), go wider if segments diverge. Surveys: size by the precision you need and the population, see `references/survey-design.md`. Usability: see `usability-evaluation`.

**Lean vs. rigorous.** A two-day guerrilla round (quick intercepts, five informal sessions) is appropriate for early, reversible decisions. Be explicit about its limits. Use rigorous recruiting and analysis when the decision is costly, when the population is specialized, or when findings will be contested.

**Asking about price, willingness to pay, or future intent.** Stated intent is weak evidence. Prefer behavioral proxies: what they currently pay for alternatives, what they have tried, commitment signals (signing up for a pilot, pre-ordering), or real experiments.

**Generative vs. evaluative.** Generative research (what problems exist, for whom) comes before there is a solution and should not be anchored to one. Evaluative research (does this solution work) needs something concrete to test. Teams often run evaluative studies when they actually lack generative understanding; the symptom is tests where participants complete tasks fine but the team still cannot say whether anyone needs the feature.

**Continuous vs. project-based research.** A standing cadence (e.g. a few customer conversations every week, owned by the product team) keeps knowledge fresh and cheap per question but rarely goes deep. Project studies go deep on one question. Healthy teams have both; if only one is possible, match it to whether the team's uncertainty is broad (continuous) or concentrated in one big bet (project).

**In-house vs. external moderators.** Internal researchers know the product and context; external ones bring neutrality and are useful when participants might hold back with the vendor (e.g. competitive research, sensitive topics, churned customers).

## Adapting to context

- **B2B and enterprise.** The buyer, the admin, and the daily user are often different people with different goals; research each. Access goes through account owners, so plan lead time and agree on what you will and will not discuss (pricing, roadmap). Workflows span tools and teams; contextual inquiry and artifact review are especially valuable.
- **Internal tools.** Participants are colleagues, so power dynamics are acute: guarantee non-attribution, avoid having managers observe, and recruit beyond the loudest requesters.
- **Consumer products at scale.** Analytics and experiments are cheap; the risk is optimizing metrics without understanding motives. Keep a steady stream of qualitative sessions to explain the numbers.
- **Specialist domains (clinical, legal, financial, industrial).** Learn the domain vocabulary before sessions, involve a domain expert in guide review, and respect regulatory constraints on what can be observed or recorded.
- **International and multilingual.** Run sessions in participants' preferred language with native-speaking moderators or skilled interpreters; translate guides by meaning, not word for word; check that scales and examples make cultural sense; incentives and consent norms differ by country.
- **Disabled participants and assistive technology users.** Recruit them in every relevant study, not only in accessibility-specific ones; let them use their own setup; allow more time; pay for the time including setup. See `accessible-design`.
- **Early-stage or zero-user products.** Research the problem and current alternatives with people who have the problem; there are no "users" yet, and that is fine.

## Worked example: scoping a study

*Request*: "We need to research whether users want a mobile app."

1. **Reframe to the decision.** The real decision is whether to invest a team in native mobile next half-year versus improving the responsive web experience. The question is not "do they want an app" (most will say yes) but "what jobs do users need to do away from a desk, how often, and how well does the current experience serve those moments?"
2. **Check existing data.** Analytics: share of sessions on mobile browsers, which pages they hit, completion rates of key tasks on mobile vs. desktop. Support tickets mentioning phone or mobile. Prior research mentions.
3. **Identify the risky assumptions.** (a) Users have frequent away-from-desk moments; (b) those moments involve tasks the product supports; (c) the web experience fails them in ways only native solves (offline, notifications, camera).
4. **Pick methods.** Analytics for (a) and (b) quantitatively, a one-week diary study with 10–12 participants across two segments capturing each moment they wanted to use the product away from a desk, then follow-up interviews to probe. A short survey afterwards to size the moments the diary revealed, if the decision needs prevalence.
5. **Define what would change the decision.** If away-from-desk needs are rare or served adequately by the responsive web, invest in web. If they are frequent and blocked by native-only capabilities, build. If frequent but blocked by fixable web issues, fix those first.

Notice that the method fell out of the decision and the assumptions; nobody asked "should we do a survey?" first.

## When working as an AI assistant

An assistant can do much of the research craft — framing questions, drafting screeners and guides, critiquing questions for bias, structuring synthesis, clustering notes the user provides, and drafting reports — but it cannot substitute for participants.

- **Do not present generated "user responses" or synthetic personas as research findings.** A model's output reflects its training data, not this product's users, and it will confidently produce plausible, homogeneous, flattering answers. Synthetic responses can be used, clearly labelled, to pilot a guide or to brainstorm hypotheses to test, never as evidence.
- **When synthesizing transcripts or notes the user supplies**, keep every claim traceable to a participant ID and quote, flag single-source themes, and say what you could not verify (e.g. tone, non-verbal cues missing from transcripts).
- **Check data handling before processing participant data**: ask whether the user has consent and policy cover to share transcripts with an AI tool, and suggest removing names and identifying details first if unsure.
- **If you can browse or search**, review public sources (app-store reviews, forums, support communities) as secondary research, and label it as such; it over-represents vocal and unhappy users.

## Pitfalls

- **Leading questions.** "Don't you find it annoying when…?" Rewrite as "Tell me about the last time…". Signs: your questions contain the answer, an adjective, or the word "would".
- **Hypothetical questions as evidence.** "Would you use this?" Treat answers as near-zero signal.
- **Recruiting whoever is convenient.** Colleagues, friends, the five happiest customers. Results skew toward people who already understand or like the product.
- **Pitching in the session.** Explaining the vision converts research into a sales call; participants politely agree.
- **Synthesis by memory.** Writing findings from the moderator's impressions favours the most recent, most vivid, and most confirming sessions. Go back to the notes.
- **Counting qualitative data as statistics.** "67% of participants…" from six people invites misreading. Use counts ("4 of 6") and say what the sample can and cannot show.
- **Themes that mirror the discussion guide.** If your themes are "Onboarding", "Settings", "Reporting" — the sections of your guide — you have sorted notes, not synthesized.
- **Insights without implications, or recommendations without evidence.** Each needs the other.
- **Research theatre.** Studies run after the decision was made, to justify it. If the outcome cannot change anything, do not take participants' time.
- **Ignoring disconfirming evidence.** Track the observations that contradict your favourite theme as carefully as the ones that support it.
- **One-and-done.** A single study treated as permanent truth. Users, markets and products change; date findings and revisit.
- **Professional participants.** Panel regulars who have learned what researchers want to hear. Screen with behavioral questions, check consistency between screener and session, and cap how often one person can participate.
- **Treating support tickets and reviews as representative.** They come from people motivated to complain or praise. Use them to find issues, not to size them.
- **Synthesis outsourced to whoever was not in the room.** Handing notes to someone who never saw a session loses context; involve the moderator and note-taker.
- **Burying the lead.** A forty-slide readout where the decision-relevant insight is on slide thirty. Put it first.
- **Changing the guide every session.** Small fixes are fine; rewriting it each time makes sessions incomparable and themes impossible to count.
- **Observer overload.** Many silent observers on a call make participants guarded. Keep live observers few, or share recordings afterwards.
- **No time for synthesis.** Scheduling sessions back to back until the readout leaves no time to think. Budget synthesis time at least equal to fieldwork for qualitative studies.

**Recognising trouble early.** If after three sessions you are hearing nothing that surprises you, either your questions are too narrow (you are only confirming), your recruit is too homogeneous, or the question was already answered and you can stop early. If every session is wildly different, your segment is probably two or more segments; split the recruit.

## Quality bar and verification

Before calling the research done, check:

- [ ] Every research question maps to the decision, and every finding maps back to at least one research question (or is flagged as an unexpected discovery).
- [ ] Participants matched the screener criteria; the report states the sample and who was not included.
- [ ] Notes trace each insight to specific participants and observations; someone else could follow the trail.
- [ ] Insights are non-obvious, supported by more than one participant (or explicitly flagged as single-source), and separate from recommendations.
- [ ] Contradictions and segment differences are reported, not smoothed over.
- [ ] Quantitative claims match the method's power; no percentages from tiny samples.
- [ ] Consent was obtained and recorded; outputs are anonymized; raw data is stored and scheduled for deletion per policy.
- [ ] The intended audience has received the findings in a form they will use, and the findings are stored where they can be found.
- [ ] Secondary sources (reviews, tickets, public forums, any AI-generated material) are labelled as such and not mixed with primary findings.
- [ ] Open questions and recommended follow-up research are listed, so the next study starts where this one ended.
- [ ] Ask: "Would the team decide differently because of this?" If not, either the study answered the wrong question or the findings are not yet framed for the decision.

## Depth on demand

- `references/interview-technique.md` — question craft, probing, rewriting leading questions, handling difficult sessions. Read before writing a discussion guide or moderating.
- `references/survey-design.md` — question types, scales, wording bias, sampling and margin of error, analysis. Read before writing or analysing a survey.
