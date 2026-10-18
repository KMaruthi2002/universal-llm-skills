---
name: usability-evaluation
description: >-
  Evaluate how usable an interface, flow, or prototype is: expert reviews
  (heuristic evaluation using Nielsen's heuristics or other lenses, cognitive
  walkthroughs), moderated and unmoderated usability tests, task and scenario
  design, think-aloud, metrics (task success, time on task, errors,
  post-task and SUS-style questionnaires), severity rating, benchmarking, and
  reporting findings that get fixed. Use when asked to test or review a
  product's usability, plan a usability study, write test tasks, find UX
  problems in a screen or flow, rate issue severity, or compare usability
  before and after a change. For open-ended discovery research use
  ux-research; for WCAG conformance use accessibility-audit; for opinion-based
  design feedback use design-critique.
metadata:
  category: design
  related: ux-research, design-critique, accessibility-audit, accessible-design, wireframing-and-prototyping, interaction-design, information-architecture, ux-writing, experiment-design, statistical-analysis, qa-test-planning, llm-evaluation
---

# Usability Evaluation

Usability evaluation asks whether specific people can achieve specific goals with a specific interface effectively, efficiently, and with acceptable effort and confidence. It produces evidence about where and why an interface fails its users, ranked by how much each failure matters, so a team can fix the right things first.

There are two families of methods: **inspection** (experts reason about the interface without users) and **testing** (observe representative users attempting real tasks). Inspection is fast and cheap and finds many problems, but is also prone to false alarms and misses problems that only real users' knowledge and expectations reveal. Testing is slower and costs more, but its evidence is far stronger. Use inspection to clean up obvious issues before testing, and testing to find out what actually matters.

**Out of scope, handled elsewhere:**

- Discovery research into needs and contexts: `ux-research`.
- Formal accessibility conformance audits (WCAG or similar): `accessibility-audit`. Usability testing with disabled participants is in scope here.
- Structured design feedback and critique sessions: `design-critique`.
- Controlled experiments measuring business metrics: `experiment-design`.
- Functional QA (does it work as specified): `qa-test-planning`, `end-to-end-testing`.

## Core principles

**1. Usability is relative to users, tasks, and context.** An expert tool can be highly usable for trained operators and impenetrable to novices. Always state who, doing what, in what situation. "Is this usable?" has no answer; "Can first-time admins set up single sign-on without help?" does.

**2. Observe behavior; treat opinion as secondary.** What people do (succeed, fail, hesitate, backtrack, misinterpret) is the primary evidence. What they say about it is useful context, but participants routinely rate an interface favourably after failing to use it.

**3. A problem found by inspection is a hypothesis; a problem observed in testing is evidence.** Expert reviews produce candidate issues. Some are real; some never trouble actual users. Report them with appropriate confidence.

**4. Severity, not count, is what matters.** Thirty cosmetic issues matter less than one that stops people completing checkout. Rank by impact on users and the business, and report that ranking first.

**5. Small qualitative rounds find problems; larger samples measure.** Around five participants per distinct user group typically reveals most of the serious problems in a flow, because serious problems recur. That sample cannot estimate success rates precisely. Run several small rounds and iterate for finding problems; use larger samples when you need to measure or compare.

**6. Test the design, not the participant.** Participants are never wrong; when they fail, the interface (or the task, or the prototype) failed. Say so to them, and mean it in analysis.

**7. Findings exist to be fixed.** A report nobody acts on was a waste. Make findings specific, evidenced, prioritized, and tied to recommendations that the people who can fix them understand.

## Choosing a method

| Situation | Method | Why |
|---|---|---|
| Early design, no time for users, want obvious issues found | Heuristic evaluation by 2–5 evaluators | Cheap, fast, broad coverage |
| Need to know if novices can learn a flow step by step | Cognitive walkthrough | Focuses on learnability from the user's knowledge |
| Need evidence of real problems and why they happen | Moderated usability test, think-aloud | Rich behavioral and explanatory data |
| Need many participants quickly on well-defined tasks | Unmoderated remote test | Scale and speed; less depth |
| Need to compare two designs or measure improvement | Benchmark study with metrics, larger samples | Quantitative comparison |
| Need to find where users first go wrong in navigation | First-click test or tree test | Isolates navigation decisions (see `information-architecture`) |
| Need to know what users notice or remember on a page | Five-second / first-impression test | Clarity of purpose and visual hierarchy |
| Need real-world usage evidence after launch | Analytics, session replays (with privacy safeguards), support data | Behavior at scale; tells you where, not why |
| Need to know if it works for assistive-technology users | Usability testing with disabled participants using their own setup | Conformance alone doesn't guarantee usability |

Combine them: an expert review to fix the obvious, then a moderated test to find what matters, then a benchmark to show improvement.

## Inspection methods

### Heuristic evaluation

Evaluators examine the interface against a set of recognized usability principles and record violations. Nielsen's ten heuristics are the most widely used lens:

1. **Visibility of system status** — the system keeps users informed about what is happening, through timely feedback.
2. **Match between system and the real world** — it speaks the users' language, with familiar concepts and natural ordering.
3. **User control and freedom** — users can undo, cancel, and exit unwanted states easily.
4. **Consistency and standards** — the same words and actions mean the same thing; platform and industry conventions are followed.
5. **Error prevention** — the design prevents problems (constraints, defaults, confirmations for risky actions) rather than only reporting them.
6. **Recognition rather than recall** — options, actions, and information are visible or easily retrievable; users don't have to remember things across screens.
7. **Flexibility and efficiency of use** — accelerators for experts (shortcuts, defaults, personalization) without burdening novices.
8. **Aesthetic and minimalist design** — no irrelevant or rarely needed information competing with the relevant.
9. **Help users recognize, diagnose, and recover from errors** — plain-language error messages that state the problem and suggest a solution.
10. **Help and documentation** — when needed, help is easy to find, task-focused, and concise.

These are one lens, not the only one. Others worth using where they fit: domain-specific guidelines (e.g. for e-commerce, forms, data visualization), platform human-interface guidelines, cognitive-load principles, accessibility principles (perceivable, operable, understandable, robust), and the product's own design-system guidelines. Choose the lens that matches the risks of the interface; a medical device and a game need different lenses.

**Running it well:**

- Use 2–5 independent evaluators; a single evaluator typically finds only a fraction of the issues, and different evaluators find different ones. Evaluators with both usability and domain expertise find the most.
- Define the scope (which flows, which user type, which device) and the tasks evaluators should walk through; reviewing "the app" generally yields shallow, random findings.
- Each evaluator works alone first, going through the interface at least twice: once to get the feel, once to inspect specific elements and flows.
- Record each issue with: location, description, the heuristic or principle violated, evidence (screenshot), and an initial severity.
- Merge findings in a debrief, deduplicate, and rate severity jointly.
- Report heuristic findings as likely issues, not proven ones.

### Cognitive walkthrough

Focuses on learnability: whether a new user, with stated knowledge and goals, can figure out each step. For each step of a task, ask:

1. Will the user try to achieve the right effect? (Do they know this step is needed?)
2. Will the user notice that the correct action is available? (Is it visible?)
3. Will the user associate the correct action with the effect they want? (Does the label or icon communicate it?)
4. If the correct action is performed, will the user see that progress is being made? (Is there feedback?)

A "no" or "maybe" at any question marks a likely failure point; record why. Define the user persona's prior knowledge explicitly before starting, or the walkthrough defaults to the evaluator's knowledge, which is always too much.

### Problem patterns worth checking in any review

Regardless of lens, these recur across products and are quick to check:

- Primary action not visually or verbally distinguishable from secondary ones.
- No feedback after an action (did it save? is it loading?), or feedback that disappears before it can be read.
- Labels that use internal terms, or the same word meaning different things in different places.
- Required information revealed only through errors (password rules, file limits, format rules).
- Destructive actions without undo or clear confirmation; irreversible actions one click from routine ones.
- Lost work: forms clearing on error, navigation away without warning, sessions expiring silently.
- Hidden functionality: hover-only controls, gestures with no visible alternative, features only in overflow menus.
- State ambiguity: users can't tell what is selected, filtered, saved, published, or shared.
- Dead ends: empty states, errors, or permission blocks with no next step.
- Inconsistent behavior between similar components or between platforms of the same product.
- Keyboard traps, missing focus indicators, and content that doesn't adapt to zoom or small screens (also check with `accessible-design`).

### Inspection pitfalls

- Treating the evaluator's preferences as usability issues ("I'd prefer a dropdown").
- Inflating severity of minor violations because a heuristic was technically broken.
- Missing domain-specific problems because evaluators lack domain knowledge.
- Reviewing without tasks, which produces scattered, surface-level findings.

## Usability testing

### 1. Define goals and scope

Write: what you are testing (product, prototype, flow), the questions you need answered, the participant profile, whether the goal is formative (find and fix problems) or summative (measure against a benchmark or compare designs). This determines sample size, metrics, and moderation.

### 2. Design tasks

Tasks are the instrument. Bad tasks invalidate the whole study.

- **Base tasks on real top tasks** and the risky parts of the design, not on features you are proud of.
- **Write scenarios with a goal and a motive**, not instructions: "Your manager asked for last quarter's numbers in a format she can open on her phone. Get them to her." Not: "Use the export feature to export a PDF."
- **Don't reveal the answer** by using interface labels in the task wording.
- **Make success criteria explicit** before testing: what end state counts as success, what counts as partial, and the time limit after which a task is stopped.
- **Order tasks** realistically (setup before use), and randomize independent tasks to reduce learning effects in summative studies.
- **Pilot the tasks** with one person to catch ambiguity, impossible tasks, and prototype gaps.
- For participants' own goals, consider an open task at the start ("Show me how you would normally…") before scripted tasks, so you see their real approach.

### 3. Recruit

- Recruit to the participant profile by behavior, not demographics (see `ux-research` for screeners and incentives).
- For formative tests, about five per distinct user group per round. Run more rounds rather than more participants per round.
- For summative or comparative studies, larger samples (often 20 or more per group, more for small differences) and consistent conditions; consult `statistical-analysis` for confidence intervals.
- Include participants with disabilities who use assistive technology, in their own setup, wherever the product serves them, which is almost always.

### 4. Moderate

- **Brief**: purpose, think-aloud request, recording consent, that you are testing the design not them, that they can stop any time.
- **Think-aloud**: ask participants to say what they're looking for, thinking, and expecting. Prompt neutrally when they go quiet ("What are you thinking now?"). Concurrent think-aloud slows people down; for timed summative measures, use retrospective probing instead.
- **Stay neutral**: don't help, hint, or react to success or failure. Answer questions with questions ("What would you expect?").
- **Intervene by rule**: decide beforehand when to step in (e.g. stuck for a set time, or about to make the rest of the session impossible). Record any assistance; an assisted completion is not a success.
- **Probe after each task**: what was easy or hard, what they expected, how confident they are they succeeded. Confidence matters; a "success" the participant isn't sure of is fragile.
- **Observers** watch silently, ideally from another room or muted, and take notes on issues by task.

**Unmoderated testing**: write tasks even more carefully, since nobody can clarify; include post-task questions to capture success self-reports and reasons; screen recordings with think-aloud audio where the tool allows; expect some low-quality sessions and plan to exclude them by predefined criteria.

### 5. Collect metrics

Pick metrics that answer the study's questions; see `references/metrics-and-scales.md` for definitions, calculation, and interpretation.

- **Effectiveness**: task success rate (binary or graded), error counts and types.
- **Efficiency**: time on task (for successful attempts), number of steps or clicks relative to the optimal path, assists.
- **Satisfaction and perceived ease**: a single post-task ease question; a standardized post-study questionnaire (e.g. SUS) for overall perceived usability.
- **Confidence**: participants' confidence that they completed the task correctly.

For formative studies, metrics support the narrative (e.g. "4 of 5 failed task 3"); don't over-interpret. For summative studies, report with confidence intervals.

### 6. Analyse

- **Per task**: success, time, errors, and the observed problems that caused failure or friction.
- **Per issue**: description, where it occurs, how many participants it affected, which tasks, evidence (quotes, timestamps, clips), the likely cause (why the design led to it), and severity.
- **Find root causes**: the same underlying issue (e.g. an ambiguous label) may surface in several tasks. Group by cause, not symptom, so a single fix addresses all of them.
- **Note positives**: what worked well, so the team doesn't break it while fixing other things.

### 7. Rate severity

Rate each issue on a consistent scale based on:

- **Impact**: does it prevent task completion, cause significant delay or errors, cause minor friction, or is it cosmetic?
- **Frequency**: how many participants (or what share of users) encounter it.
- **Persistence**: do users overcome it once learned, or does it bother them every time?
- **Business or safety consequences**: data loss, financial errors, security, legal exposure, harm. These can raise severity regardless of frequency.

A practical four-level scale:

| Level | Meaning | Typical action |
|---|---|---|
| Critical | Prevents task completion, or causes data loss, financial, safety, or legal harm | Fix before release |
| Major | Significant delay, errors, or frustration; many users affected; workaround is hard | Fix soon; high priority |
| Minor | Small friction or confusion; users recover easily | Fix when convenient |
| Cosmetic | Noticeable but no effect on task performance | Fix if time allows |

Have two or more people rate independently and reconcile, to reduce individual bias. Keep the scale definitions written down so ratings are consistent across studies.

### 8. Report

Write for the people who will fix things. See `references/writing-up-issues.md` for structure and examples. Essentials:

- Lead with the top issues (by severity) and what to do about them.
- For each issue: what happened, evidence, why it likely happened, severity, recommendation.
- Recommendations should state the problem to solve, optionally with a suggested direction, not prescribe a pixel-level solution; designers need room to solve it well.
- Include what worked.
- State method, participants, and limitations honestly.
- Follow up: track issues to resolution, and retest fixes.

## Evaluating particular kinds of interfaces

- **Forms and transactional flows**: watch for abandonment points, re-entry of data, validation surprises, and uncertainty about whether submission worked. Measure errors and time; check recovery from mistakes.
- **Data-heavy tools and dashboards**: tasks should require interpreting data ("Which region missed its target last month?"), not just navigating. Check whether participants read the data correctly; misreading with confidence is a severe issue.
- **Expert and professional software**: novices' struggles may be irrelevant; recruit trained users, include efficiency and error-rate measures, and test with realistic workloads. Learnability for new staff may still matter — test it separately.
- **Mobile apps**: test on real devices in realistic postures (one-handed, on the move if relevant); watch reach, target size, keyboard overlap, interruptions, and connectivity changes.
- **Search and recommendation features**: success depends on result quality; use real queries and a realistic corpus. Distinguish interface problems from relevance problems.
- **AI and conversational features**: evaluate whether users form accurate expectations of what the system can do, notice and correct wrong outputs, and recover from failures or refusals. Over-trust (accepting wrong output) is a usability failure, not a success. Pair with `llm-evaluation` for output quality.
- **Onboarding and first-run**: recruit genuinely new users; one participant's prior exposure contaminates the round. Measure time-to-first-value and whether they reach the moment that makes the product useful.
- **Physical or embedded interfaces** (kiosks, devices, vehicles): test in the real environment or a faithful simulation; lighting, noise, gloves, and time pressure change everything. Safety-critical contexts require formal human-factors processes beyond this skill.

## Worked example: planning a quick evaluation

*Request*: "Can you tell us what's wrong with our signup flow? Conversion is low."

1. **Clarify the context**: who signs up (self-serve small businesses), on what devices (analytics show about half on mobile), where people drop (analytics funnel shows the biggest loss at company details and at email verification).
2. **Expert review first** (a day): two evaluators walk the flow on mobile and desktop using Nielsen's heuristics plus form-design guidelines. Candidate issues: a long company-details form requiring tax ID before any value is shown; the verification email step gives no indication of which address it was sent to and no resend option; error messages appear only after submit and clear the password field.
3. **Fix the obvious**: the error-clearing and missing resend are cheap and almost certainly harmful; recommend fixing immediately without waiting for testing.
4. **Test what's uncertain**: a moderated remote test with five recent prospects who did not complete signup, on their own phones. Tasks: "You've decided to try this for your shop's bookings. Get set up so you could take a booking tomorrow." Measure completion, time, points of hesitation; probe why they would or would not continue at the tax-ID step.
5. **Outcome and severity**: three of five stopped at the tax-ID field, saying they didn't have it handy and didn't know why it was needed (major; directly tied to the observed drop-off). Recommendation: defer the field until it's needed, or explain why it's required and allow saving progress. Expert-review issues that participants never encountered are reported separately as lower-confidence items.
6. **Follow-up**: after changes ship, compare funnel data (an experiment if traffic allows, see `experiment-design`) and rerun the same test tasks.

## When working as an AI assistant

- You can perform a heuristic evaluation or cognitive walkthrough of screenshots, a live site you can browse, a prototype, or code. State the lens you used, the user and tasks you assumed, and label every finding as an expert-inspection hypothesis.
- If you can operate a browser, walking the flow yourself catches broken states, missing feedback, and keyboard traps — but your experience is not a user's; you lack their goals, vocabulary, and constraints, and you never "fail" for the reasons humans do.
- Never invent participant data, quotes, or metrics. You can design tasks, screeners, scripts, and questionnaires, and analyse real session notes or recordings the user provides.
- When analysing session data, keep participants anonymized and remove identifying details before quoting.

## Discovering context

Before evaluating an existing product:

- **Learn the users and their top tasks** from existing research, analytics, and support data. Tasks you invent without this risk testing irrelevant paths.
- **Check prior evaluations** and known issues so you don't rediscover the same things or can measure progress against a previous benchmark.
- **Gather constraints**: platforms and devices, supported browsers, accessibility commitments, regulatory requirements (e.g. medical, financial, public sector), release timing.
- **Understand the design system and guidelines**, so recommendations fit existing patterns.
- **Know who will act** on findings and how the team tracks work, so findings arrive in a usable form (tickets in their tracker, a readout, a document).
- **Agree on success targets** where possible (e.g. "most first-time users complete setup without help").

## Decision guidance

**Inspection or testing?** Inspection when time is very short, the design is early, or you need to clear obvious issues before spending on participants. Testing whenever the stakes justify it and real users can be reached, and always before treating findings as proven.

**Moderated or unmoderated?** Moderated for complex domains, early prototypes, need for probing, or participants who need support. Unmoderated for straightforward tasks, larger samples, geographic reach, and speed.

**Formative or summative?** Formative during design to find and fix problems. Summative to benchmark a release, compare against competitors or previous versions, or prove a target was met. Don't mix their methods carelessly: think-aloud inflates time; helping participants invalidates success rates.

**Lab, remote, or field?** Remote is the default for most software. In-person or in-context when the physical environment, devices, or collaboration matter, or when participants are less comfortable with remote tools.

**Prototype or live product?** Test prototypes to avoid building the wrong thing; test the live product to find what real data, performance, and integrations do to the experience. See `wireframing-and-prototyping` for prototype testing specifics.

**How many tasks?** As many as fit in the session with time to probe: often 5–8 for an hour-long moderated session. Fewer, better tasks beat many rushed ones.

## Ethics

- Obtain informed consent for participation and recording; explain how data is used and stored; let participants stop or skip anything without penalty.
- Never make participants feel stupid. Reassure them when they struggle, and pay the full incentive regardless of performance.
- Protect privacy: no real personal or financial data entered into test environments; anonymize reports and clips; restrict access to recordings.
- Session replays and analytics on live products must respect the product's privacy policy and applicable law: mask sensitive fields, avoid recording sensitive screens, aggregate where possible.
- For participants with disabilities, provide accommodations and let them use their own technology; budget extra time and pay for it.
- Observers must not identify or discuss participants outside the study.

## Pitfalls

- **Leading tasks** that name the target button or describe the steps.
- **Testing what you're proud of** rather than what users need.
- **Helping during tasks**, then reporting success.
- **Over-reading small samples**: percentages and statistical claims from five participants.
- **Under-reading small samples**: dismissing an issue because "only two of five" hit it; a serious problem affecting 40% of users is serious.
- **Severity by loudness**: rating issues by how vocal the participant was or how much a stakeholder dislikes them.
- **Laundry-list reports**: a hundred issues with no prioritization; teams fix the easy cosmetic ones and ignore the critical one.
- **Prescriptive recommendations**: "Make the button blue" instead of "Users don't notice the primary action; it needs to stand out from secondary ones."
- **Confusing preference with usability**: "I don't like the color" is not a usability issue unless it affects performance.
- **Not retesting fixes**: a fix may not solve the problem or may create a new one.
- **Accessibility as an afterthought**: assistive-technology users excluded from tests, so their blocking issues surface after launch.

## Quality bar and verification

- [ ] Users, tasks, and context are specified; tasks reflect real top tasks and risky areas.
- [ ] Task wording doesn't give away answers; success criteria were defined before testing.
- [ ] Participants match the profile; sample size fits the study goal (formative vs. summative).
- [ ] Moderation stayed neutral; assists are recorded and not counted as successes.
- [ ] Each issue has evidence, a likely cause, a severity from a written scale, and a recommendation.
- [ ] Issues are grouped by root cause; the top issues are clear in the first page of the report.
- [ ] Metrics match the study type; quantitative claims include sample sizes and, for summative studies, confidence intervals.
- [ ] Inspection findings are labelled as such and distinguished from observed problems.
- [ ] Consent and privacy safeguards were followed; reports are anonymized.
- [ ] Findings are delivered where the team works, and a retest is planned for critical and major fixes.

## Depth on demand

- `references/metrics-and-scales.md` — definitions and calculation of task success, time, errors, efficiency, single-ease questions, SUS-style questionnaires, benchmarks, and confidence intervals. Read for summative studies or whenever you report numbers.
- `references/writing-up-issues.md` — structuring a usability write-up, writing issues and recommendations, and getting them fixed. Read when writing up results.
