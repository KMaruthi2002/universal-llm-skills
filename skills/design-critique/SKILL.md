---
name: design-critique
description: >-
  Give, structure, and receive critique of any design artifact — screens,
  flows, prototypes, visual designs, design systems, slides, diagrams,
  physical or service designs — by first understanding goals and
  constraints, separating personal taste from effectiveness, making feedback
  specific and actionable, prioritizing issues, running critique sessions,
  critiquing your own work, and responding well to critique. Use when asked
  for feedback on a design, to review a mockup or prototype, to run a design
  crit, to compare design options, or to improve a design before sharing it.
  For evidence from real users use usability-evaluation; for code use
  code-review; for WCAG conformance use accessibility-audit.
metadata:
  category: design
  related: usability-evaluation, ui-design-fundamentals, visual-design, interaction-design, accessible-design, ux-writing, design-systems, wireframing-and-prototyping, code-review, writing-review-and-editing, data-visualization, presentations
---

# Design Critique

Critique is a structured conversation about whether a design achieves its goals, and how it could achieve them better. It is not approval, not a vote, and not an opportunity to redesign someone else's work in your own taste. Good critique makes the design better and the designer more capable; bad critique makes the designer defensive and the design more like whoever spoke loudest.

This skill applies to any design artifact at any fidelity: sketches, wireframes, high-fidelity screens, prototypes, design-system components, data visualizations, slide decks, diagrams, illustrations, marketing layouts, physical products, services. It covers giving critique, running critique sessions, critiquing your own work, and receiving critique.

**Out of scope, handled elsewhere:**

- Evidence from observing real users: `usability-evaluation`. Critique is expert judgment; testing is evidence. They complement each other.
- Accessibility conformance against a standard: `accessibility-audit` (critique should still flag likely accessibility problems).
- Code review: `code-review`. Prose editing: `writing-review-and-editing`.
- Principles of good UI, visual and interaction design that critique draws on: `ui-design-fundamentals`, `visual-design`, `interaction-design`.

## Core principles

**1. Critique against goals, not against your preferences.** A design is good or bad *for something*: these users, this task, this brand, these constraints. Before judging, find out what it is trying to do. Feedback anchored in goals ("the main goal is quick reordering, but the reorder action is the least prominent thing on the screen") is useful. Feedback anchored in taste ("I'd use a different font") is noise unless taste is the goal.

**2. Separate observation, interpretation, and suggestion.** "I notice the price appears below the fold on mobile" (observation) → "so shoppers may not see it before deciding" (interpretation of effect) → "consider moving it near the product name" (suggestion). Keeping them separate lets the designer evaluate your reasoning and solve the problem their own way.

**3. Problems are more valuable than solutions.** The designer usually knows the constraints and context better than the critic. A clearly stated problem lets them find the best solution; a prescribed solution often solves the wrong problem or ignores a constraint. Offer suggestions as options, not instructions.

**4. Specific beats general.** "The hierarchy is off" cannot be acted on. "The secondary 'Save as draft' and primary 'Publish' buttons are the same size and color, so it's unclear which is the main action" can.

**5. Prioritize.** Not all issues are equal. A critique that lists twenty issues without ranking them leaves the designer to guess which matter. Lead with what most affects the goals.

**6. Critique the work, not the person.** "This layout makes the error easy to miss" not "You made the error hard to see". The distinction is not politeness for its own sake: people who feel attacked stop listening, and the design does not improve.

**7. Fit the critique to the stage.** Early concepts need feedback on direction and problem framing, not pixel alignment. Late-stage designs need feedback on details and edge cases, not a re-opening of settled direction (unless something serious was missed). Ask what stage it is at and what feedback is wanted.

**8. Taste is real but declared.** Aesthetic judgment matters, especially in visual and brand work. Offer it when relevant, labelled as such ("this is a matter of taste, but…"), and weigh it below effectiveness unless aesthetics is the goal.

## Before critiquing: understand the design

Ask, or find out from the brief, the following. If you can't, say what you assumed.

- **Goal**: what is this design meant to achieve? For the user (complete a task, understand something, feel something) and for the business (conversion, retention, compliance, brand perception).
- **Audience**: who will use it, with what expertise, on what devices, in what circumstances, with what access needs.
- **Context**: where it sits in the product or journey; what comes before and after.
- **Constraints**: brand guidelines, design system, technical limitations, content realities, legal requirements, deadlines, platform conventions.
- **Stage and fidelity**: exploratory, refining, or final; what has already been decided.
- **Feedback wanted**: what the designer wants input on, and what is out of scope for this round.
- **Success criteria**: how anyone will know if the design worked (metrics, research findings, stakeholder needs).

If the designer can't articulate the goal, that is itself the most important finding.

## A process for giving critique

### 1. Take in the whole first

Look at the design as its user would, before analysing. What is your first impression in a few seconds: what is it, what is the main thing to do, where does the eye go? Note it; first impressions are data, especially for landing pages, dashboards, and anything that must communicate quickly.

Walk through it as a user would: perform the main tasks, follow the flow, read the copy. If you can interact with a prototype or live build, do so rather than looking at static screens.

### 2. Evaluate systematically

Go through the dimensions relevant to the artifact and its goals. For an interface, a useful set:

| Dimension | Questions |
|---|---|
| Goal fit | Does it serve the stated goals? Does the most important thing get the most emphasis? |
| Clarity and comprehension | Is it obvious what this is, what to do, and what will happen? Is the language the user's? |
| Hierarchy and focus | Does the visual order match the importance order? Is there a clear primary action? |
| Flow | Do steps follow a sensible sequence? Are there dead ends, unnecessary steps, or missing steps? |
| Feedback and states | Are loading, empty, error, success, and edge states handled? |
| Consistency | Does it follow the product's patterns, the design system, and platform conventions? Where it deviates, is that justified? |
| Accessibility | Contrast, text size, target size, keyboard and screen-reader support, not relying on color alone, motion sensitivity |
| Content | Does it work with real content: long names, many items, none, translations? |
| Responsiveness | Does it work across the supported sizes and inputs? |
| Visual quality | Alignment, spacing rhythm, typographic hierarchy, color use — in service of clarity and the brand |
| Feasibility | Can this be built within the known constraints? What would be costly? |
| Ethics | Does it manipulate (dark patterns), exclude, mislead, or expose users to harm? |

For non-interface artifacts, adapt the dimensions: a data visualization needs accuracy, honest scales, and readability (`data-visualization`); a slide deck needs a clear argument and one idea per slide (`presentations`); a design-system component needs API clarity, states, and composability (`design-systems`).

### 3. Separate issues from preferences

For each thing you want to say, ask:

- **Does it affect a goal?** If yes, it's an issue; explain the effect.
- **Is it a violation of the product's own standards** (design system, brand, platform)? If yes, it's an issue of consistency; cite the standard.
- **Is it a likely accessibility barrier?** Always an issue.
- **Is it only that I would have done it differently?** Then it's a preference. Either drop it or offer it explicitly as one.

A useful self-check: could you explain *why* it matters to someone who doesn't share your taste? If not, it is probably taste.

### 4. Prioritize

Rank issues by their effect on the goals. A simple grouping:

- **Critical**: blocks the goal, misleads, excludes users, or creates risk (legal, financial, safety, privacy). Must address.
- **Important**: noticeably weakens effectiveness or consistency. Should address.
- **Minor / polish**: small refinements. Address if time allows.

Lead with critical issues. For a final-stage review, minor issues matter more; for an early concept, they hardly matter at all.

### 5. Phrase feedback well

Structure each point so it can be acted on:

- **Where**: the specific element, screen, or step.
- **What you observe**: neutral description.
- **Why it matters**: the effect on users or goals, linked to the stated goals where possible.
- **Optional suggestion**: a direction or a question, framed as one option.

Illustrative contrasts:

| Unhelpful | Helpful |
|---|---|
| "It's cluttered." | "The dashboard shows twelve equally weighted cards. Since the goal is spotting overdue invoices, the overdue count competes with eleven other numbers. Could overdue items be visually separated or placed first?" |
| "I don't like the colors." | "The status colors for 'pending' and 'failed' are close in hue and similar in lightness; people with color-vision deficiencies may not tell them apart. Adding an icon or label would help." |
| "Make the button bigger." | "On mobile the 'Confirm' button sits close to 'Cancel' and both are small; mis-taps seem likely at this step, which is irreversible." |
| "This is confusing." | "I wasn't sure whether 'Archive' hides the project for me or for everyone. A short description or a confirmation stating the scope would remove the doubt." |
| "Looks great!" | "The progress indicator makes it very clear how many steps remain — worth keeping as other steps change." |

Questions are powerful in critique, especially early: "What should people do first on this screen?" "What happens if there are no results?" They help the designer reason rather than defend.

### 6. Say what works

Specific positive feedback is not padding. It tells the designer what to preserve while changing other things, and makes the critique credible. Be as specific about strengths as about problems.

### 7. Close with the summary

End with the few points that matter most and, where relevant, what you would want to see in the next iteration. If you made many points, the designer should still be able to recall the top three.

### Feedback by stage

| Stage | Most useful feedback | Least useful feedback |
|---|---|---|
| Problem framing / concepts | Is this the right problem? Which direction best fits the goals? What assumptions are risky? | Visual detail, copy polish |
| Wireframes / structure | Priority, grouping, flow, missing states and content | Color, typography, imagery |
| Visual design | Hierarchy, brand fit, consistency, accessibility of the visual layer | Re-opening settled flow decisions |
| Pre-build / final | Edge cases, states, responsiveness, feasibility, consistency with the system, craft details | New directions, unless something serious was missed |
| Implemented | Fidelity to intent, real-content behavior, performance feel, accessibility in practice (see `design-to-code-handoff`) | Concept-level debate (save for the next iteration) |

### Ethical and inclusion checks

Always look for these, whether or not they are in the brief, and raise them clearly when present:

- **Deceptive patterns**: disguised ads, pre-checked consent, hidden costs revealed late, forced continuity (easy to subscribe, hard to cancel), confirmshaming, misdirection that steers users toward options against their interest, fake scarcity or urgency.
- **Exclusion**: designs that only work for some abilities, devices, languages, connection speeds, or levels of literacy.
- **Privacy**: collecting more than needed, exposing personal data in shared views, defaults that over-share.
- **Representation**: imagery and examples that stereotype or erase groups of users.
- **Harm under misuse**: features that could enable harassment, stalking, or fraud, and whether safeguards exist.

These are not matters of taste; treat them as critical or important issues and explain the consequence.

## Worked example: a written critique

*Context*: a designer shares a mid-fidelity mobile checkout screen for a grocery delivery app and asks for feedback on clarity and flow before visual design starts. Goal: reduce drop-off at checkout; most orders come from returning customers on phones.

A useful critique might read, in summary:

> **Most important**
> 1. *The delivery time slot is chosen after payment.* Returning customers told research they abandon when their preferred slot is gone; discovering that after entering payment is the worst moment. Could slot selection come before payment, or be shown in the cart?
> 2. *The total shown on the button ("Pay") omits the delivery fee, which appears only in the summary below.* People who notice the difference late may feel misled, and fee surprises are a common reason for abandonment. Showing the full total near or on the primary action would make the cost clear.
>
> **Also worth addressing**
> 3. The promo-code field is expanded by default and sits above the payment section, which invites people without a code to leave and search for one. Collapsing it behind a link is a common way to reduce that.
> 4. The saved address shows only the street; customers with several saved addresses (work, home) can't tell which is selected without opening it.
> 5. Substitution preferences are mentioned only in a tooltip; on touch devices tooltips are easy to miss.
>
> **Questions**
> - What happens if a cart item goes out of stock between cart and payment?
> - Is there an error state designed for a declined card?
>
> **Working well**
> - Reordering the previous basket from the top of the flow is clear and fast; worth protecting as the screen evolves.
> - Step labels make progress obvious.
>
> **Out of scope for this round, noted for later**: visual hierarchy will need checking once styling starts; the slot picker's touch targets look small in the wireframe.

Notice: it starts from the stated goal, ranks issues, explains effects, offers suggestions as options, asks about missing states, names strengths, and respects the requested scope.

## Handling conflicting feedback

When reviewers disagree:

- Trace each position to the goal or evidence it rests on. Disagreements often come from different assumptions about users or priorities; make those explicit.
- If the disagreement is about a fact (will users notice this?), it can be tested; propose the cheapest test.
- If it is about priorities (speed for experts vs. clarity for novices), escalate to whoever owns the product goals rather than averaging the designs.
- If it is about taste, the designer (or the brand owner) decides; record the decision so it isn't relitigated.

## Critiquing generated or templated designs

Designs produced by generators, templates, or AI tools need the same critique, with extra attention to:

- **Generic sameness**: does it reflect this product's brand and users, or a default look?
- **Plausible but wrong content**: placeholder copy that sounds real, invented data, icons that don't match actions.
- **Missing states and edge cases**: generated screens almost always show only the ideal case.
- **Consistency with the design system**: generated components often drift from established tokens and patterns.
- **Accessibility**: contrast, semantics, and focus order are frequently wrong in generated output.

## Running a critique session

- **Set up**: the designer presents the goal, audience, constraints, stage, and the feedback wanted. Keep it short; the design should mostly speak for itself.
- **Silent review first**: give everyone time to look and note thoughts independently before discussion. This prevents anchoring on the first speaker and gives quieter people space.
- **Clarifying questions** before critique.
- **Structured feedback**: go around, or go by dimension, or by priority. A facilitator keeps it on the goals and the requested scope, and redirects solutioning ("let's capture the problem; the designer can explore fixes").
- **Avoid design by committee**: the purpose is to inform the designer's decisions, not to vote. The designer (or the accountable person) decides what to act on.
- **Capture** feedback in writing, grouped and prioritized, with who raised it.
- **Close** with agreed next steps and what will be reviewed next time.
- **Keep it psychologically safe**: critique the work, invite dissent, and model receiving critique well if you are senior.

Asynchronous critique (comments on a file or document) works well for distributed teams; the same rules apply. Comment on specific elements, label priority, separate questions from requests, and summarize in one place so the designer isn't reconciling scattered comments.

## Critiquing your own work

Self-critique is hardest because you know what you meant. Techniques that help:

- **Restate the goal** and check each element against it. Delete or demote anything that doesn't serve it.
- **Change your view**: look at it at a distance or blurred (what stands out?), in grayscale (does hierarchy survive without color?), at the smallest supported size, with a screen reader, with keyboard only, with real content.
- **Walk the flow as a first-time user** with no context. Better: watch someone else do it (see `usability-evaluation`).
- **Take a break** before reviewing; distance reveals problems you were blind to.
- **Compare against alternatives** you rejected: is this one actually better on the goals?
- **Check against the product's standards**: design system, content guidelines, accessibility requirements.
- **List the edge cases** and confirm each is designed: empty, error, loading, long, many, none, no permission.
- **Ask the hard question**: what would the most critical person on the team say? Address it before they do.

## Receiving critique

- **Frame the session** so you get what you need: share goals, stage, and the specific feedback you want.
- **Listen for the problem behind the suggestion.** "Make it red" usually means "this doesn't stand out enough". Address the underlying problem, which may have a better solution.
- **Ask clarifying questions** rather than defending. "What made you expect that?" "Which part felt cluttered?"
- **Don't argue in the moment.** Capture feedback; decide later what to act on. Explaining your rationale is useful when the critic lacks context; repeatedly justifying is not.
- **Distinguish feedback types**: issues tied to goals, standards violations, accessibility barriers, preferences. Act on the first three; weigh the fourth.
- **Close the loop**: tell reviewers what you changed and why you didn't act on some points. It makes future critique better.
- **Remember the goal is the design, not your ego.** Critique of the work is information, not judgment of you.

## Discovering context

- Read the brief, requirements, and any research the design is based on.
- Look at the product's design system, brand guidelines, content guidelines, and existing patterns, so you can distinguish deliberate consistency from arbitrary choices and avoid proposing things that conflict with established standards.
- Ask about constraints you can't see: technical limits, legal wording, business requirements, deadlines.
- Find out what has already been decided and by whom, so you don't relitigate settled questions without reason.
- Check what platform conventions apply (mobile operating systems, web, desktop, TV, automotive); they shape what "good" means.

## Decision guidance

**Comparing options.** When asked to choose between alternatives, evaluate each against the goals and constraints, make the trade-offs explicit (A is clearer for new users; B is faster for experts), and recommend based on which goals take priority. If the choice depends on facts nobody has (e.g. how users will react), say so and suggest a test.

**When to escalate beyond critique.** If the critique reveals a problem with the goal itself (the brief is wrong, the feature shouldn't exist, the research doesn't support it), raise it explicitly with the people who own the goal, separately from design feedback.

**How much to say.** For early work, a few big points. For final review, a thorough pass. For a junior designer, focus on the most important learning points rather than every flaw. For a senior designer, be direct and thorough; they want the signal.

**Brand and visual taste.** When the critique concerns aesthetics in a branded context, judge against the brand's own guidelines and intent, not your preferred style. If the brand is undefined, say what impression the design gives and ask whether that is intended.

## Pitfalls

- **Critiquing before understanding**: judging a design against goals it doesn't have.
- **Taste disguised as principle**: "best practice says…" for a personal preference.
- **Redesigning in the critique**: presenting your alternative rather than identifying problems.
- **Vague feedback**: "make it pop", "feels off", "cleaner".
- **Unranked lists**: everything seems equally important; the critical issue gets lost.
- **Only negatives**: the designer doesn't know what to keep.
- **Only positives**: polite but useless; the design doesn't improve.
- **Stage mismatch**: pixel nitpicks on a concept; questioning the concept at final review without good reason.
- **Highest-paid-person's opinion**: a senior person's preference overrides evidence; facilitate so that goals and evidence lead.
- **Ignoring accessibility and ethics** because they weren't in the brief.
- **Bikeshedding**: long debates about trivial, easy-to-understand details (a button's corner radius) while complex, important issues go undiscussed.
- **Defensive receiving**: arguing every point, so reviewers stop giving honest feedback.
- **Critiquing screenshots of interactive work**: judging motion, responsiveness, or flow from static images. Say what you could not evaluate, or ask for the prototype.
- **Feedback with no follow-through**: critique given, never revisited. Ask to see the next iteration, and check whether the top issues were resolved.
- **Over-indexing on novelty**: praising or criticizing a design for being different from convention, rather than for how well it works. Convention is often a usability asset; novelty must earn its cost.

## Quality bar and verification

Before delivering critique, check:

- [ ] I know (or have stated my assumptions about) the goals, audience, constraints, stage, and feedback wanted.
- [ ] Every issue names the element, what I observe, and why it matters for the goals or standards.
- [ ] Issues are prioritized, and the most important appear first.
- [ ] Preferences are labelled as preferences or omitted.
- [ ] Suggestions are offered as options; the problem is stated independently of the suggestion.
- [ ] Accessibility, edge states, and ethical concerns were considered.
- [ ] Strengths are named specifically.
- [ ] The feedback fits the stage and the requested scope.
- [ ] The language critiques the work, not the person.
- [ ] Where my judgment is uncertain and evidence is cheap to get, I recommend testing rather than asserting.

## Depth on demand

- `references/critique-lenses.md` — lenses and question sets for critiquing specific kinds of artifacts (interfaces, visual and brand work, data visualizations, design systems, content-heavy pages, presentations), plus a note on critiquing as an AI assistant. Read when critiquing an artifact type you need more structure for.
