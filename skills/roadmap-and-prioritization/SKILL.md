---
name: roadmap-and-prioritization
description: >-
  Decide what to work on and in what order, and communicate it as a roadmap:
  use prioritization frameworks (RICE, ICE, MoSCoW, Kano, cost of delay /
  WSJF, opportunity scoring) as lenses with known failure modes rather than
  oracles, build outcome-based instead of output-based roadmaps, sequence by
  dependency, risk and learning, say no well, and communicate confidence and
  uncertainty honestly. Use when someone asks to "prioritize the backlog",
  "build a roadmap", "score these features", "what should we do next quarter",
  "how do I say no to this request", or must present plans to stakeholders.
  Not for writing the spec of a chosen item (product-requirements), running
  delivery (project-management), or sizing work (estimate-effort).
metadata:
  category: product-and-communication
  related: product-requirements, user-stories, project-management, estimate-effort, technical-decision-making, competitive-analysis, experiment-design, business-communication, presentations
---

# Roadmap and Prioritization

Prioritization is the work of **choosing what not to do** so that limited capacity goes where it creates the most value. A roadmap is the **communication of those choices over time**, with honest confidence levels. Both exist to align people and enable good local decisions, not to predict the future.

**Not covered here:**

- Specifying a chosen item — see `product-requirements`.
- Breaking it into deliverable stories — see `user-stories`.
- Estimating effort and forecasting dates — see `estimate-effort`.
- Running the delivery — see `project-management` and `release-management`.
- Market and competitor research feeding the decisions — see `competitive-analysis`, `ux-research`.

## Core principles

### 1. Strategy comes first; prioritization serves it

You cannot rank items without knowing what you are optimizing for. Before scoring anything, state the goal (or the two or three goals) the work should advance, and the constraints (capacity, commitments, regulation). Why: frameworks applied without a goal reward whatever the scoring inputs happen to favour — usually the loudest request or the easiest work.

### 2. Frameworks are lenses, not oracles

Every framework simplifies. Its value is in forcing explicit assumptions that can be debated; its danger is false precision. Use a framework to structure the conversation and expose disagreements, then make a judgment and own it. Why: a ranked spreadsheet feels objective, but the numbers were guesses; treating the output as an answer launders opinion into apparent fact.

### 3. Prioritize problems and outcomes, not features

Rank the outcomes you want or the problems you will solve, then choose solutions. Why: comparing features directly mixes "is this problem important?" with "is this the best solution?", and teams end up building a mediocre answer to an important problem or a perfect answer to a trivial one.

### 4. Cost of delay is the hidden variable

The value of an item often depends on *when* it lands: a seasonal feature, a contract renewal, a regulatory date, a competitor window. Why: two items with equal total value but different time sensitivity should not be treated the same, and most simple scoring methods ignore time entirely.

### 5. Sequence to learn

Early in a product or initiative, the highest-value work is often what reduces uncertainty fastest — a prototype, an experiment, a thin slice to real users. Why: building the "most valuable" item on an untested assumption risks wasting the whole investment; a cheap test first can redirect it.

### 6. Roadmaps communicate intent and confidence, not promises

Near-term items can be specific and committed; later items should be expressed as problems or goals with lower confidence. Why: committing to detailed features months out forces you either to ship the wrong thing when you learn more or to break promises. Honest uncertainty preserves trust; false precision spends it.

### 7. Saying no is part of the job

Every yes is an implicit no to something else. Make the trade-off visible. Why: when trade-offs are invisible, people assume capacity is infinite and every request is a matter of willingness.

## The frameworks, as lenses

Choose a lens based on the question you are trying to answer. Using two lenses that disagree is often more informative than perfecting one.

| Framework | What it does | Good for | Failure modes | Mitigations |
|---|---|---|---|---|
| **RICE** (Reach × Impact × Confidence ÷ Effort) | Scores items on expected value per unit effort | Comparing many similar-sized candidates in one product area | Impact scale is subjective; Reach favours mass features over strategic niches; Confidence gets inflated; Effort underestimated for unfamiliar work; ignores timing and dependencies | Calibrate Impact with examples; have several people score independently; treat scores as bands, not ranks; check top items against strategy |
| **ICE** (Impact, Confidence, Ease) | Quick 1–10 scores, multiplied or averaged | Fast triage of experiments or growth ideas | Extremely subjective; easy to game; scores drift between sessions | Use only for coarse sorting; re-score as a group; never present ICE scores as evidence |
| **MoSCoW** (Must, Should, Could, Won't) | Buckets scope for a fixed time or release | Negotiating scope for a deadline | Everything becomes a Must; "Won't" ignored; no ordering within buckets | Cap Musts (e.g. at what fits in a conservative estimate); define Must as "release is pointless or illegal without it"; rank within buckets |
| **Kano** | Classifies features as basic expectations, performance (more is better), delighters, indifferent, or reverse | Understanding how features affect satisfaction; balancing a release | Requires real user research to be meaningful; categories shift over time (delighters become basics) | Base on survey or interview data; revisit periodically; use alongside a value/effort lens |
| **Cost of delay / CD3 / WSJF** (value lost per unit time ÷ duration) | Orders work to minimize total value lost while waiting | Time-sensitive items; queues of work competing for one team; portfolio sequencing | Cost-of-delay estimates are hard; WSJF's composite scoring (business value + time criticality + risk reduction) can become as subjective as ICE | Estimate cost of delay in rough money or outcome terms per week/month; use urgency profiles (see below); focus on relative ordering |
| **Value vs. effort (2×2)** | Plots items into quick wins, big bets, fill-ins, money pits | Workshops; a first visual sort | Crude; everything clusters in the middle; effort guesses biased | Use for discussion, then refine top-right and top-left items with better estimates |
| **Opportunity scoring** (importance vs. current satisfaction) | Finds needs that are important and poorly served | Choosing which problems to address | Needs survey data; measures stated, not revealed, importance | Combine with behavioural data |
| **Buy-a-feature / budget allocation** | Stakeholders spend a limited budget on items | Revealing stakeholder preferences and trade-offs | Measures politics and persuasion as much as value | Use for input, not as the decision |
| **Weighted scoring against strategic criteria** | Scores items against explicit weighted goals | Making strategy alignment explicit | Weights are opinions; criteria overlap and double-count | Agree weights before scoring; keep criteria few and distinct |

### Urgency profiles (for cost of delay)

A simple way to reason about time without precise numbers:

| Profile | Shape | Illustrative | Implication |
|---|---|---|---|
| Expedite | Large, immediate loss | Security vulnerability being exploited; outage | Interrupts planned work |
| Fixed date | Value drops sharply after a date | Regulatory deadline; event launch; contract term | Schedule backwards from the date with buffer |
| Standard | Value lost roughly linearly while waiting | Most product improvements | Order by value ÷ duration |
| Intangible | Little cost now, large later | Tech debt, platform upgrades, capability building | Reserve some capacity, or it never happens |

### A note on doing the arithmetic

When you compute RICE-style scores, keep inputs and assumptions visible next to the result, round to a sensible precision, and present items in bands ("clearly high", "contested middle", "clearly low"). The contested middle is where the real conversation should happen. Re-ranking items that differ by 5% in score is noise.

Illustrative RICE reasoning:

> Item A: Reach 4,000 users/quarter, Impact 1 (medium), Confidence 50%, Effort 2 person-months → 4000 × 1 × 0.5 ÷ 2 = 1,000.
> Item B: Reach 600 users/quarter, Impact 3 (massive), Confidence 80%, Effort 1 person-month → 600 × 3 × 0.8 ÷ 1 = 1,440.
>
> B scores higher, but note: B's 600 users are the enterprise admins whose renewals depend on it (a cost-of-delay issue RICE ignores), and A's 50% confidence means its score could plausibly be anywhere from ~400 to ~2,000. The scores alone do not decide; they reveal that the real questions are "how confident are we in A's impact?" and "what is the renewal timing for B?". A cheap test of A's impact might be the best next step.

## Outcome vs. output roadmaps

| Aspect | Output (feature) roadmap | Outcome roadmap |
|---|---|---|
| Items are | Features and dates | Problems to solve or metrics to move, with candidate solutions |
| Strengths | Concrete, easy to understand, easy to track | Leaves room for discovery; aligns on why; survives learning |
| Weaknesses | Locks in solutions early; success = shipping; brittle to change | Can feel vague to sales, customers, and executives; harder to track |
| Fits when | Work is well understood; contractual commitments; dependent teams need specifics | Uncertain problem space; empowered teams; goal is impact |

Most organizations need a blend: outcome framing for the team and leadership, with the nearest-term solutions named concretely, and a translation layer for audiences that need dates. A common structure is horizons — **now / next / later**, or committed / planned / exploring — where specificity and confidence decrease with distance.

Illustrative outcome item:

> Goal: Reduce time for new teams to reach first value (median time from sign-up to first shared project) from 6 days to 3.
> Now: guided setup for imported data (in build; confidence high).
> Next: template gallery; inviting teammates during setup (in discovery; confidence medium).
> Later: role-based onboarding paths (idea; confidence low).
> Measured by: activation dashboard, reviewed monthly.

## Sequencing

Ranking is not the same as ordering. After rough prioritization, sequence by:

1. **Hard dependencies** — what must exist first (platform capabilities, data, contracts, other teams' work). Map them; dependency chains often dominate the schedule.
2. **Risk and learning** — put the riskiest assumptions early, tested as cheaply as possible. Why: discovering a fatal flaw late wastes everything built on it.
3. **Time sensitivity** — fixed-date items are scheduled backwards with buffer.
4. **Value per duration** — among the remaining, do short high-value items before long ones (the CD3 insight: a short valuable item delayed by a long one loses value for the whole duration).
5. **Capacity and focus** — limit work in progress. Running many priorities in parallel slows all of them; finishing one before starting the next delivers value sooner.
6. **Balance** — reserve capacity deliberately for categories that never win head-to-head scoring: maintenance, tech debt, quality, small customer asks, experiments. A fixed allocation (whatever ratio the organization agrees) is more reliable than hoping they win on merit.

## How context changes the weighting

The same lenses apply everywhere, but what deserves weight shifts with the situation:

| Situation | Weight more heavily | Watch out for |
|---|---|---|
| Early-stage product, searching for fit | Learning speed, risk reduction, depth for a narrow segment | Building for every prospect; scoring by reach when reach is tiny |
| Growing product | Activation, retention, scalability of what works | Neglecting reliability and debt accumulated during the search phase |
| Mature product | Efficiency, retention, quality, adjacent opportunities | Incremental tweaks crowding out any larger bet |
| Platform / internal tools team | Unblocking other teams, adoption, reliability | Prioritizing by who asks loudest instead of by downstream impact |
| Regulated or contract-bound work | Fixed dates and compliance obligations first | Treating compliance work as optional because it scores low on "value" |
| Crisis (outage trend, security, churn spike) | Stabilization, even at the cost of planned work | Staying in crisis mode after the crisis ends |

## Handling incoming requests

Most prioritization pressure arrives as a steady stream of requests from sales, support, leadership, partners, and other teams. Without a system, each is decided ad hoc by whoever is asked, and the roadmap erodes one exception at a time.

- **Have one intake path** that the organization knows about (a form, a board, a channel, a recurring triage slot — whatever fits). Why: requests sent privately to individuals bypass comparison with everything else.
- **Capture the problem, not just the ask**: who needs it, what they are trying to do, what happens if it is not done, and how many others are affected. A request without a problem cannot be ranked.
- **Link requests to existing items** rather than creating duplicates; the count and value of linked requests is evidence.
- **Triage on a cadence**: classify each request as expedite (interrupt), consider at next planning, park, or decline, and tell the requester which and why.
- **Close the loop.** Requesters who never hear back escalate or route around the process. A short "parked, here is why, here is what would change it" preserves goodwill.

## Prioritizing across teams and portfolios

When several teams share goals or dependencies, local prioritization can be individually sensible and collectively incoherent: team A's top item depends on team B's tenth.

- **Align on shared goals first**, then let each team prioritize toward them.
- **Surface cross-team dependencies during planning**, not after. A simple dependency list per team, reviewed jointly, catches most conflicts.
- **Resolve conflicts at the level that owns the shared goal.** If two teams cannot both do their top items, the person accountable for the shared outcome decides.
- **Limit the number of initiatives in flight at portfolio level.** Starting many cross-team initiatives at once spreads shared specialists (security, data, design, platform) thin and delays all of them.
- **Fund capacity, not just projects**, where work is ongoing: a team owning an outcome over time adapts better than one handed a sequence of fixed projects.

## Worked reasoning: from a list to a decision (illustrative)

> Context: a team of five has one quarter. Goal: improve retention of small-business accounts. Candidates:
>
> 1. Rebuild reporting (large; many requests; unclear retention impact).
> 2. Fix the invoice sync failures (medium; affects 9% of accounts; support data shows these accounts churn at twice the rate).
> 3. In-app onboarding checklist (small; activation correlates with retention; a similar test elsewhere showed modest lift).
> 4. Upgrade the payment library (small; current version loses vendor support in four months).
> 5. Partner integration requested by one large prospect (medium; sales says it is a deal-breaker).
>
> Coarse cut: item 5 is a new-customer item, not retention. It may still matter, but it competes with the goal; escalate the trade-off to whoever owns both goals rather than silently absorbing or dropping it.
>
> Lenses: value vs. effort puts 2 and 3 as clear wins. Cost of delay flags 4 as fixed-date (intangible now, expensive later) — schedule it, small and early. Item 1 has high reach but low confidence in retention impact; RICE with honest Confidence drops it to the middle.
>
> Sequence: 4 early (small, date-bound, unblocks nothing but removes risk); 2 next (strongest evidence); 3 in parallel if capacity allows (cheap, learnable). For 1, run interviews with churned accounts this quarter to test whether reporting is actually a churn driver; decide next quarter.
>
> Communicate: "This quarter: invoice sync reliability and onboarding checklist, plus a required payment library upgrade. Reporting rebuild is deferred pending research; the partner integration needs a decision from <owner> because it serves acquisition, not this quarter's retention goal."
>
> Note what made this work: a single explicit goal, honest confidence, attention to timing, and turning the biggest uncertainty into a learning task instead of a bet.

## Saying no

How to decline or defer well:

- **Acknowledge the problem**, not just the request. Show you understood the need.
- **Explain the trade-off** in terms of goals: "Doing this now would delay X, which is our main lever for Y this quarter."
- **Offer what you can**: a smaller version, a workaround, a later window, a path for the requester to provide evidence that changes the calculation.
- **Be clear about status**: "not this quarter" and "not ever" are different; ambiguity creates repeated asks.
- **Keep a visible record** of requests and decisions so the same debate is not repeated and patterns across requests become visible (ten small asks for the same underlying problem may be a top priority in disguise).
- **Escalate trade-offs, not complaints**: if a senior stakeholder insists, frame the decision as "which of these should we drop?" and let the person with authority choose.

Illustrative phrasing (adapt to the sender's voice and relationship):

> "I can see why this matters for the Northwind renewal. Right now the team is focused on the onboarding work tied to our activation goal, and adding this would push that out by about three weeks. Two options: we can ship the export as a CSV workaround next sprint, or schedule the full integration for the next planning cycle. If the renewal risk is bigger than I think, can we look at it together with the account lead?"

## Communicating uncertainty

- **Use horizons or confidence labels**, not precise dates, beyond the near term.
- **Give ranges** for dates ("late Q2 to early Q3") and say what would narrow them.
- **Separate commitments from intentions.** Make it unmistakable which items are promised (and to whom) and which are plans.
- **Version the roadmap** and show what changed and why since the last version. Silent changes destroy trust faster than changes themselves.
- **Tailor the view to the audience**:

| Audience | Usually needs | Avoid |
|---|---|---|
| Executives / leadership | Goals, outcomes, major bets, risks, trade-offs needing decision | Feature-level detail |
| The team | Why, near-term specifics, open questions, how success is measured | Only dates |
| Other internal teams | Dependencies, timing ranges, what they must provide | Internal debate |
| Sales / customer-facing | What is coming with what confidence; what to say to customers | Unhedged dates they will repeat as promises |
| Customers / public | Themes and direction; committed near-term items | Anything you are not prepared to be held to |

External roadmaps are effectively commitments once published. Confirm with the owner before sharing any roadmap outside the team that made it.

## Process

### 1. Establish the frame

Clarify: what period, what capacity, what goals, what constraints and existing commitments, and who decides. If goals are unclear, surface that first — prioritizing without them produces a ranking nobody trusts.

### 2. Gather candidates

Collect from all sources: strategy, research, customer requests, support and sales signals, data, tech debt lists, team ideas, commitments. Normalize them into problems or opportunities where possible. Merge duplicates; note the source and evidence for each.

### 3. Do a coarse cut

Remove or park items that clearly do not serve the goals or are infeasible. Do this explicitly and record why. Most candidate lists are far longer than capacity, and detailed scoring of everything wastes time.

### 4. Apply one or two lenses to the remainder

Pick lenses fit for the question (see table). Score independently where possible, then compare and discuss differences — the disagreements are the valuable output. Check assumptions behind the top items: is the evidence real? Is the effort estimate from the people who would do the work?

### 5. Sequence

Order by dependencies, risk, time sensitivity, value per duration, and capacity limits. Reserve capacity for maintenance and other non-competing categories.

### 6. Decide and record

The accountable person decides. Record what was chosen, what was not, and the reasoning. Why: future you, and newcomers, will need to know why, especially when circumstances change.

### 7. Communicate

Produce views for each audience. Lead with goals and trade-offs. Show confidence. Say what is not being done. See `business-communication` and `presentations` for delivery.

### 8. Revisit on a cadence and on triggers

Review regularly (e.g. monthly or quarterly) and when something material changes: a big learning, a market shift, a missed assumption, a capacity change. Update the roadmap and communicate the delta. Do not reprioritize so often that nothing finishes.

## Discovering context

- **Find the current roadmap and planning cycle.** Most organizations have an existing format, tool, cadence, and audience expectations. Fit into them.
- **Find the stated strategy and goals** (company objectives, team goals, OKRs or equivalents). Use their language.
- **Identify existing commitments** — contracts, promised customer features, regulatory dates. These constrain everything.
- **Understand who decides** and how disagreements are settled. A prioritization nobody with authority endorses is a suggestion.
- **Check how the organization uses frameworks.** If a team already uses RICE or WSJF, use theirs — but point out failure modes if inputs look unreliable.
- **Ask about capacity honestly**: holidays, support load, on-call, ongoing maintenance. Plans built on 100% capacity always slip.

## Pitfalls and anti-patterns

- **Spreadsheet theatre.** Elaborate scores used to justify decisions already made. Recognize when scores are adjusted until the preferred item wins. Fix by agreeing scales and inputs before scoring, and by being open that judgment decided.
- **Highest-paid opinion.** Ranking defaults to the most senior voice. Fix by making evidence and trade-offs explicit and asking the senior person to decide between named options rather than dictate a list.
- **Loudest customer.** One large customer's request dominates. Fix by asking how many customers share the problem, and what the cost of not doing it is.
- **Everything is P1.** No real prioritization happened. Fix with forced ranking or capped buckets.
- **Feature factory roadmap.** A list of features with dates and no goals. Fix by grouping items under the outcomes they serve and asking which items do not serve any.
- **Ignoring the invisible work.** Maintenance, tech debt, and operational load are never prioritized until they cause an incident. Fix with reserved capacity.
- **Too much in progress.** Many priorities started at once, none finished. Fix by limiting parallel initiatives.
- **Date-driven fiction.** Dates set top-down without estimates, then treated as commitments. Fix by showing scope/date trade-offs and ranges (see `estimate-effort`).
- **Stale roadmap.** A document nobody updates, which then misleads. Fix with a cadence and a visible "last updated" note.
- **Reprioritizing constantly.** Weekly reshuffles prevent anything from finishing. Fix by protecting committed near-term work and channelling changes through the regular review, except true emergencies.
- **Confusing ranking with sequencing.** The top-scored item is started first despite depending on something not yet built. Fix by mapping dependencies before committing.
- **Over-trusting a framework's inputs.** Reach and Impact numbers that nobody can trace. Fix by noting the source for each input and lowering confidence where there is none.

## Quality bar and verification

- [ ] The goals and constraints used for prioritization are written down and match the organization's stated strategy.
- [ ] Each prioritized item is linked to a goal or a named problem, with its evidence source.
- [ ] Frameworks used are named, their inputs visible, and their limitations acknowledged; the decision is attributed to people, not to a score.
- [ ] Time sensitivity and dependencies were considered, not just value and effort.
- [ ] Capacity assumptions are realistic and include maintenance and operational load.
- [ ] What is *not* being done is listed, with reasons.
- [ ] The roadmap distinguishes commitments from intentions, and confidence decreases visibly with distance.
- [ ] Each audience's view gives them what they need without making promises the team cannot keep.
- [ ] There is a stated cadence and trigger for revisiting.

Stress tests:

- **Capacity halves**: does the plan say what to drop first?
- **The top assumption is wrong**: what changes, and is there an early test of it?
- **A stakeholder asks "why not X?"**: is there a recorded answer?
- **Six months later**: could someone reconstruct why these choices were made?

## Working as an assistant

- When asked to "prioritize this list", ask what the goals and constraints are if not given; if you proceed without them, state the assumed goals explicitly.
- Present prioritization outputs as recommendations with reasoning and named uncertainties, leaving the decision to the accountable person.
- Do not publish or send a roadmap to stakeholders or customers on someone's behalf without explicit confirmation.

## Related skills

- `product-requirements` — specifying a prioritized item.
- `estimate-effort` — the effort side of value/effort, and date ranges.
- `experiment-design` — cheap tests to raise confidence before committing.
- `technical-decision-making` — recording consequential choices.
- `competitive-analysis` — market inputs.
- `business-communication` and `presentations` — communicating the roadmap.
- `project-management` — delivering what was chosen.
