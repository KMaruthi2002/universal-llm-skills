---
name: mvp-prototyping
description: >-
  Build the smallest thing that tests an idea: identify the riskiest
  assumption, decide what to fake and what to make real, choose throwaway vs
  evolvable code on purpose, time-box the build, make it demo-able, and
  document what was deliberately skipped. Use when asked for an MVP, a
  prototype, a proof of concept, a spike, a demo for investors or users, "a
  quick version to see if this works", a hackathon build, or a clickable
  mock to validate demand or feasibility before investing in a full build.
  Not for production-grade applications (full-stack-app-build) or design-only
  mockups with no working logic (wireframing-and-prototyping).
metadata:
  category: app-generation
  related: full-stack-app-build, product-requirements, experiment-design, wireframing-and-prototyping, ux-research, roadmap-and-prioritization, estimate-effort, project-scaffolding, technical-decision-making, usability-evaluation
---

# MVP Prototyping

## Purpose and scope

An MVP or prototype exists to **answer a question cheaply**. The question might be "will anyone pay for this?", "can this be built at all?", "do users understand this workflow?", or "will this technology perform well enough?". The deliverable is not an application — it is **evidence**, delivered through the smallest artefact that can produce it, plus an honest record of what the artefact is and is not.

This skill covers deciding what to build, what to fake, how long to spend, how to make it demonstrable, and how to leave it so that the next decision (kill, iterate, or build properly) is easy.

Boundaries:

- Building a real, maintainable product: `full-stack-app-build`.
- Non-functional design mockups and clickable wireframes made in a design tool: `wireframing-and-prototyping`.
- Designing the measurement itself (hypotheses, sample sizes, metrics): `experiment-design`.
- Running sessions with users to observe them: `ux-research`, `usability-evaluation`.
- Writing the full product spec once the idea is validated: `product-requirements`.

## Core principles

1. **Start from the question, not the feature list.** Name the single riskiest assumption and build only what tests it. Why: every feature that does not bear on the question delays the answer and dilutes the signal (users react to the polish, the extra features, the bugs — not to the idea).

2. **Fake everything that is not under test.** If the question is "will people sign up?", the backend can be a spreadsheet and the "AI" can be a human. Why: real infrastructure is expensive to build and teaches you nothing about demand.

3. **Make real the thing under test.** If the question is "can we get latency under 200 ms?", the fast path must be real and measured on realistic data; the UI can be a command line. Why: a faked answer to the actual question is worse than no answer — it creates false confidence.

4. **Decide throwaway or evolvable up front, and say so.** Why: the worst outcome is a throwaway prototype that silently becomes production because it "already works", carrying every shortcut with it.

5. **Time-box, then cut scope — never extend the box.** Why: prototypes expand to fill time; the deadline is what forces you to find the minimum. If the box is too small to answer the question, change the question.

6. **Demo-ability is a feature.** The prototype must be showable reliably to the people whose reaction is the evidence. Why: a prototype that crashes in the demo produces evidence about your demo, not about the idea.

7. **Document the shortcuts.** Every fake, hardcode and skipped concern is written down. Why: it lets stakeholders interpret the evidence correctly and lets whoever builds the real thing know what is missing.

## Process

### 1. Frame the question

Turn the idea into a testable statement. Useful shapes:

- **Desirability:** "Target users will [do the behaviour] when offered [the value]." Evidence: sign-ups, pre-orders, repeat use, time spent, willingness to pay, qualitative reaction.
- **Usability:** "Users can complete [the core job] without help in under [time]." Evidence: task completion and observed confusion.
- **Feasibility:** "We can achieve [capability] at [quality/speed/cost] with [approach]." Evidence: measurements on realistic inputs.
- **Viability:** "The unit economics work at [price] given [cost per use]." Evidence: measured costs, conversion at a stated price.

Ask the user (see `clarify-requirements`) when unclear:

- What decision will this prototype inform, and who makes it?
- What result would make you stop? What result would make you invest? If no result would change the decision, the prototype is theatre — say so gently.
- Who will see it: internal team, a few friendly users, investors, the public?
- How much time is acceptable — hours, days, two weeks?
- Is there anything that must be real for legal or ethical reasons (real payments, real personal data)?

Write the question, the success and failure criteria, and the audience at the top of the project's README. This is the prototype's reason to exist.

### 2. Find the riskiest assumption

List the assumptions the idea depends on. For each, estimate: how likely is it wrong, and how bad is it if it is? The riskiest one — likely wrong and fatal if so — is what the prototype tests. Others are assumed true for now and listed as such.

If several assumptions are equally risky, prefer the one that is cheapest to test first, or design the prototype to test two at once only if that does not muddy either signal.

### 3. Choose the cheapest artefact that answers it

Before writing code, consider whether code is needed at all:

| Question | Often answered by | Code needed? |
|---|---|---|
| Is there demand? | Landing page with a sign-up or pre-order, a waitlist, an ad test, a concierge offer | Minimal: a page and a form |
| Will they pay? | Real price on a checkout that collects intent (with honest disclosure) or real pre-orders | Minimal, plus payment provider's hosted checkout if taking real money |
| Do they understand the workflow? | Clickable prototype, paper prototype, or a thin UI over fake data | Low |
| Does the core value land? | "Wizard of Oz" (a human performs the service behind a real-looking interface) or concierge (do it manually, openly) | Low |
| Can it be built / is it fast enough? | Technical spike: a script, notebook or benchmark on realistic data | Yes, for the risky part only |
| Will it integrate with system X? | A spike that calls X's real API end to end with one real case | Yes, narrowly |
| Will people keep using it? | A working single-feature app used for days or weeks | Most — this is the closest to a real build |

Pick the lowest row that genuinely answers the question. Going further down the table costs more and is only justified when the cheaper artefact cannot produce valid evidence.

### 4. Decide fake vs. real, item by item

Go through every component the prototype will appear to have and classify it:

- **Real** — under test, or required for the evidence to be valid, or required for safety/legality.
- **Faked** — appears to work; behind it is hardcoded data, a manual process, a canned response, or a third-party tool.
- **Absent** — not present at all, and the demo avoids it.

Common fakes, and when each is acceptable:

| Component | Fake options | Acceptable when |
|---|---|---|
| Backend / database | Hardcoded JSON, a spreadsheet, a no-code database, local storage, an in-memory store | Data persistence is not under test and demo data is small |
| Authentication | A single shared login, a name field, no auth at all, magic link via a hosted service | Only invited testers; no real personal data stored |
| AI / ML capability | Canned responses for a scripted demo, a human in the loop, an off-the-shelf API instead of a custom model | Quality of the AI is not what is being tested — or you say clearly that a human is involved |
| Payments | "Buy" button that records intent then explains it is pre-launch; hosted checkout in test mode | You are measuring intent, and users are told honestly before any charge would occur |
| Integrations | Recorded responses, a manual import, a mock server | The integration is not the risk |
| Email / notifications | Manual sending, logged to console, a single hosted form tool | Volume is tiny |
| Admin tools | Direct database edits, a spreadsheet | Only the team needs them |
| Scale, performance | Ignored | Fewer users than a single machine handles trivially — unless performance is the question |

Rules for fakes:

- **Fake the back of house, not the evidence.** If users' behaviour is the evidence, what they interact with must behave plausibly; what happens after can be manual.
- **Never fake in a way that deceives users to their harm.** Taking money for something that does not exist without disclosure, claiming automation where humans read private data, or collecting personal data under false pretences are not "lean" — they are ethical and often legal problems. When a human is behind the curtain and sees users' data, tell the users or use only consenting testers.
- **Keep fakes behind a seam** (one function, one module, one config flag) when the prototype is evolvable, so they can be replaced without rewriting callers.

### 5. Choose throwaway or evolvable

| Throwaway | Evolvable |
|---|---|
| Purpose is to learn, then discard | Purpose is to learn, and if positive, grow into the product |
| Optimise purely for speed of learning | Optimise for speed, but keep a clean core |
| Any tool: notebook, no-code, single file, hardcoded everything | The stack you would plausibly use for real (see `full-stack-app-build` stack choice) |
| No tests, or a few to protect the demo | Tests on the core logic that will survive |
| Hardcoded data and config inline | Config externalised, fakes behind interfaces |
| Lives in a scratch repo or folder clearly named as a prototype | Lives where the product will live, on a branch or behind a flag |

Choose throwaway when the question is likely to come back "no" or the eventual product will look very different. Choose evolvable when the question is mostly about refinement, the eventual stack is already known, and time pressure after validation will be high.

Say which one it is in the README, in the first line, in plain words. If it is throwaway, also say what must be rebuilt before real use. Experts disagree on how often evolvable prototypes are a good idea; the honest position is that they work when the shortcuts are recorded and paid down, and fail when they are forgotten.

### 6. Set the time-box

Estimate the build at the level of the fake/real list (see `estimate-effort`). Then set a box that is shorter than feels comfortable — hours for a spike, days for a demo, one or two weeks for a usable single-feature product.

Inside the box:

- **First 10–20%:** get the end-to-end demo path working ugly. Every screen in the demo exists and connects, even if each is crude.
- **Middle:** make the part under test good enough that it is the thing users react to.
- **Last 20%:** demo hardening (see step 8) and documentation. Do not spend this on new features.

When you hit the halfway point, check: will the core path be demo-ready by the end? If not, cut scope now. Candidates to cut, in order: secondary screens, settings, edge-case handling outside the demo path, visual polish not related to the question, any automation that can be manual.

### 7. Build the thin path

Build only what the demo path and the measurement need:

- A single happy path through the core job, done well enough to be believable.
- The measurement: analytics events, a sign-up counter, timing logs, a survey link, a spreadsheet of observations — whatever produces the evidence defined in step 1. A prototype without measurement is a demo, not an experiment.
- Realistic content and data. Placeholder text and toy data distort reactions; users judge "lorem ipsum" products as unfinished rather than as ideas. Use plausible, representative content, never real people's personal data without consent.
- Visual direction appropriate to the audience and question. If the question is about trust (finance, health), the prototype must look trustworthy enough not to confound the answer; if it is an internal feasibility spike, it needs no visual design at all. Derive the look from the brand or context provided; do not apply a default style. When there is no guidance, keep it plain and neutral so the look does not become the variable.

If you can run the code, run the demo path after every meaningful change. A prototype that breaks is cheap to fix when you notice within minutes and expensive the morning of the demo.

### 8. Make it demo-able

Demo reliability is its own work:

- **Script the demo path** — the exact clicks and inputs — and rehearse it at least once on the setup that will be used.
- **Pre-load demo data** with a seed or reset command so every demo starts from the same state.
- **Remove live dependencies on the demo path where possible.** Flaky networks, rate-limited APIs and slow model calls fail at the worst time. Cache, record or pre-compute where the dependency is not under test.
- **Host it somewhere stable** if others will try it unsupervised: a shareable URL, a build installed on test devices, or a recorded walkthrough as a fallback.
- **Have a fallback**: screenshots or a short screen recording of the working path.
- **Handle the obvious off-path actions gracefully** — a "coming soon" message is better than a crash when someone clicks the button you did not build.

### 9. Document what was skipped

Maintain a "Prototype limitations" section in the README as you go, not at the end. It lists:

- What is faked and how (e.g. "recommendations are hand-curated for the three demo accounts").
- What is absent (e.g. "no password reset, no account deletion, no email verification").
- Known risks if this were used for real: security (no authorization checks, no rate limiting), data (no backups, data lost on restart), privacy (where testers' data is stored and who can see it), legal (terms, consent).
- Assumptions taken as true without testing.
- What would be needed to make it production-ready, roughly sized.

Why this matters: stakeholders who see a working demo naturally assume it is nearly done. This section is how you prevent a two-day prototype being promised to customers next week.

### 10. Run the test and report the evidence

Collect the evidence defined in step 1 against the success and failure criteria set before building — not new criteria chosen after seeing the results. Report:

- The question, the criteria, and what happened.
- Caveats: sample size, who the testers were, what the fakes might have distorted.
- The recommended next decision: stop, iterate on the prototype, test the next riskiest assumption, or proceed to a real build — and what the real build must change from the prototype.

See `experiment-design` for interpreting results without fooling yourself, and `report-results` for the handback.

## Decision guidance

### Code vs. no-code vs. design tool

| Use | When |
|---|---|
| A design tool's clickable prototype | The question is comprehension or flow; no real data or logic needed |
| No-code / low-code builders, forms, spreadsheets | Desirability or concierge tests; workflows that a person can run behind the scenes; non-developer owners |
| A single-file app or notebook | Feasibility spikes, algorithm or data tests, internal demos |
| A small real app on a plausible stack | Retention tests, evolvable prototypes, integrations that must be real |

### When a prototype should not be built

- The question can be answered by talking to five users, reading existing research, or checking a competitor (`competitive-analysis`, `ux-research`).
- No outcome would change the decision.
- The "prototype" is really the product with a smaller name, and the time-box is the full build's timeline. Use `full-stack-app-build` and be honest about it.

### When to throw the prototype away even though it "works"

- It was built throwaway (shared logins, no authorization, hardcoded data).
- The validated idea differs meaningfully from what was prototyped.
- The stack was chosen for speed and does not fit production constraints.
- Nobody can list its shortcuts with confidence.

Rebuilding a validated idea properly usually takes less time than the original exploration did, because the hard question — what to build — is now answered.

### Audience changes what "done" means

| Audience | What matters most | What can be rough |
|---|---|---|
| The team itself (feasibility spike) | Correct measurement on realistic inputs; reproducible numbers | Everything visual; usability; error handling |
| Friendly test users, supervised | The core job is believable; you can observe and ask | Off-path screens; settings; performance at scale |
| Real users, unsupervised | Stability, clear onboarding, a way to give feedback, honest disclosure of fakes | Admin tooling; scale; secondary features |
| Investors or executives | A reliable scripted story that shows the value in minutes; a credible path to the real thing | Breadth; anything not in the story |
| Public launch (demand test) | Clear value proposition, working sign-up, measurement, privacy basics, spam protection | The product behind the page may not exist yet — say "coming soon" honestly |

### Common prototype shapes and their honest minimum

| Shape | Minimum that still produces valid evidence | Usually unnecessary |
|---|---|---|
| Waitlist / smoke test | Clear offer, one sign-up form, source tracking, a thank-you message that sets expectations | A product behind it |
| Concierge service | A way for users to request, a person to fulfil, a log of requests and outcomes | Automation of any step |
| Single-feature tool | The one feature working on real inputs, a way to come back, feedback capture | Accounts beyond a link or email, settings, billing |
| Marketplace | Supply seeded by hand, a way for demand to request, manual matching | Payments between parties, ratings, search |
| AI-powered assistant | Real model on realistic inputs, logged outputs, a way to rate them, guardrails on obviously harmful output | Fine-tuning, custom infrastructure, history management |
| Internal workflow tool | The one workflow end to end for one team, using their real (non-sensitive) data | Permissions matrix, reporting, integrations |
| Hardware or API integration | One real round trip, measured and logged | UI |

## Running the test

Once the prototype is in front of people:

- **Freeze the build** during a test round, or record exactly which version each participant saw. Changing it mid-test mixes two experiments.
- **Watch, do not sell.** In supervised sessions, give the task and stay quiet; the evidence is what users do without help. See `usability-evaluation`.
- **Log everything the measurement needs** and check the log daily; a tracking bug discovered after the test ends wastes the whole round.
- **Separate signal from noise.** One enthusiastic friend is not demand; a stranger returning unprompted a week later might be. Weight behaviour over opinion.
- **Keep a decision log** of what you changed between rounds and why.

## Technical spikes in particular

A spike answers "can this be done, and how well?" Its rules differ from user-facing prototypes:

- **Define the metric and threshold first**: latency at a percentile, accuracy on a labelled set, throughput, cost per call, memory footprint.
- **Use realistic inputs.** Toy inputs make almost anything look feasible. If real data cannot be used, build a synthetic set that matches its size, shape and messiness, and say how it differs.
- **Measure, do not eyeball.** Repeat runs, report variance, note hardware and versions. See `performance-optimization` for measurement discipline.
- **Try the obvious approach first.** The spike's job is to find out whether the simple way is good enough; only explore clever approaches when it is not.
- **Record negative results.** "Approach A could not exceed X because Y" is valuable and prevents someone repeating the work.
- **Stop when the question is answered.** A spike that has shown feasibility is finished, even if it is tempting to keep going.

## Evolvable prototype hygiene

If the prototype is meant to grow, a few cheap habits keep that option open without slowing the build much:

- Keep the data model honest even if storage is faked — real entity names, real relationships — so the eventual schema is not a rewrite.
- Put every fake behind one named module or flag (`fake_payments`, `canned_recommendations`), and grep-able markers on every shortcut.
- Externalise configuration and secrets from day one; it costs minutes now and hours later.
- Write tests for the core logic that is under test, since that is the code most likely to survive.
- Use the version control workflow the product will use, so history is meaningful.
- Do not add abstractions for futures you have not validated; evolvable means clean, not elaborate.

## Worked reasoning

Illustrative scenarios — the reasoning generalises, the specifics do not.

**"Build an MVP of an app that turns meeting recordings into action items for small agencies."** Riskiest assumptions: (a) agencies will upload recordings, (b) the extracted action items are good enough to act on. (b) is a feasibility-and-value question; (a) is desirability. A sensible first prototype: an upload page and a results page; extraction done by an off-the-shelf model API with a tuned prompt; no accounts (each upload gets an unguessable link); a feedback button on each action item ("useful / wrong / missing"). Real: the extraction, because its quality is under test. Faked or absent: teams, integrations with task tools, billing. Measurement: feedback ratios and whether the same users return with a second recording. Disclose that recordings are processed by a third-party service; delete them after a stated period.

**"Prove we can sync 50,000 records from the partner API nightly within 10 minutes."** Pure feasibility spike. No UI. A script that pulls a realistic page of data, measures per-page time and rate limits, extrapolates, then runs the full set once against the partner's sandbox. Deliverable: numbers, the bottleneck, and a recommendation. Throwaway.

**"We need something to show investors next Thursday."** First ask what the investors must believe after the demo. Build exactly that story: a scripted path with seeded data, offline-safe, rehearsed, with a recorded fallback. Document honestly which parts are real if asked; misrepresenting a mock as a working product to investors is a serious problem, not a growth hack.

## Choosing tools for speed

Speed in a prototype comes from familiarity and from not building things, not from novelty:

- Use the tools you (or the owner) already know well. A new framework's learning curve eats the time-box.
- Prefer hosted services for commodity parts: forms, sign-up, email, hosted checkout, file storage, analytics. Each one is a component you do not write.
- Prefer one process, one repository, one deploy target. Every extra moving part is a demo-day failure mode.
- Use generators and starter kits only if you can explain what they produced; an unfamiliar starter with forty dependencies is a liability when it breaks at midnight.
- Check every library or API you plan to rely on actually exists and does what you need, with a two-minute experiment, before building on it.

## From prototype to product

When the evidence says "build it", plan the transition explicitly rather than continuing to add features:

1. Re-read the limitations section; each line is either a work item or an accepted risk with an owner.
2. Decide what survives: often the validated flow, the content and the core logic; rarely the auth, data layer or infrastructure of a throwaway.
3. Write the real requirements from what was learned, including what users ignored (see `product-requirements`).
4. Start the real build with `full-stack-app-build`, using the prototype as a reference implementation and a source of test cases, not as the foundation, unless it was built evolvable and its shortcuts have been paid down.
5. Migrate any test users' data only with their knowledge, and delete what is no longer needed.

## Discovering context

- If an existing product or codebase is involved, a prototype that tests a new feature should usually live as a flag or a branch in it, using its components and conventions, so the evidence reflects the real product context.
- Check for brand guidelines, an existing design system or a style the target audience expects; use them when the look could affect the evidence.
- Ask who owns the prototype afterwards. An engineer, a founder with no technical background, and a design team need different handovers.

## Pitfalls and anti-patterns

- **Building the product and calling it an MVP.** Symptom: the feature list is long and the question is vague. Fix: return to step 1; if no question can be named, say so.
- **Testing the wrong thing.** Spending the time-box on a polished UI when the risk is technical, or on infrastructure when the risk is demand.
- **Faking the thing under test.** Hand-picking AI outputs for a demo intended to show the AI's quality, without saying so. The evidence is void.
- **No measurement.** A prototype ships, people use it, nobody recorded anything. Build the measurement into the thin path.
- **Moving the goalposts.** Deciding success criteria after seeing the data.
- **Prototype-to-production drift.** The throwaway quietly becomes the product. Prevent it with the limitations section and an explicit decision point.
- **Real personal data in a toy system.** Prototypes rarely have proper security; keep real personal or financial data out, or protect it properly and get consent.
- **Demo-day failure.** Untested demo environment, live API dependency, no seed reset, no fallback recording.
- **Polishing outside the demo path.** Settings pages and error edge cases nobody will see while the core path is still rough.
- **Default visual style.** A generic look that signals "template" can bias user reactions; choose visual direction for the audience or keep it deliberately plain.
- **Too many questions at once.** A prototype that tests pricing, onboarding and a new feature simultaneously cannot attribute a bad result to any of them. Test one primary question per round.
- **Over-recruiting friends.** Friendly testers are kind; their enthusiasm predicts little. Include people who match the target audience and owe you nothing.
- **Generated code nobody ran.** A prototype produced in one pass and never started is not a prototype. Run the demo path before showing anyone.
- **Hidden cost traps.** Pay-per-call APIs, uncapped cloud resources or ad spend without limits; set budget caps and alerts before opening a prototype to the public.
- **Sunk-cost continuation.** Iterating forever on a prototype whose evidence already said "no". Respect the stop criteria set in step 1.
- **"It was just a prototype" as a security excuse.** If it is publicly reachable, it can be abused: open forms get spammed, exposed keys get used, unauthenticated endpoints leak data. Basic hygiene still applies.

## Quality bar and verification

- [ ] The README begins with the question, success and failure criteria, audience, and throwaway-or-evolvable.
- [ ] Every component is classified real, faked or absent, and the classification is documented.
- [ ] The thing under test is real and measured; nothing that is evidence has been faked without disclosure.
- [ ] The scripted demo path has been run start to finish on the actual demo setup, from a reset state.
- [ ] Measurement is in place and has been checked to record correctly (do a test run and confirm the data arrives).
- [ ] Off-path clicks do not crash the app.
- [ ] No secrets in client code or the repository; no real personal or payment data unless consented and protected.
- [ ] The limitations section lists fakes, absences, risks and what production would need.
- [ ] Time spent is within the box, or the overrun and its reason are reported.

## Safety notes

- Do not take real money without clear disclosure of what users are buying and when it will be delivered; use payment providers' test modes during development.
- Do not let a human read users' private inputs behind a "Wizard of Oz" front without consent.
- Do not deploy publicly with exposed API keys; even a prototype's keys can be abused and billed.
- Ask before publishing a prototype, sending outreach to recruit testers, or spending on ads for a demand test.
- If the domain is regulated (health, finance, children's data), flag the implications even for a prototype.

## Related skills

- `experiment-design` for turning the question into a valid test.
- `product-requirements`, `user-stories` for writing up what to build once validated.
- `wireframing-and-prototyping` when no working logic is needed.
- `full-stack-app-build` for the real build afterwards.
- `estimate-effort`, `roadmap-and-prioritization` for sizing and sequencing the next step.
