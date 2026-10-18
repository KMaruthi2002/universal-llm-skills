---
name: wireframing-and-prototyping
description: >-
  Turn ideas into sketches, wireframes, mockups, and interactive prototypes
  at the right fidelity to answer a specific question: choosing low- vs.
  high-fidelity, paper sketches vs. design-tool prototypes vs. coded
  prototypes, what to prototype for which question, using realistic content,
  annotating for stakeholders and developers, testing prototypes with users,
  and avoiding premature polish. Use when exploring layout or flow options,
  sketching screens, building a clickable prototype for a test or demo,
  deciding how much fidelity is needed, or annotating wireframes. For final
  visual styling use visual-design; for a working MVP product use
  mvp-prototyping; for testing method detail use usability-evaluation.
metadata:
  category: design
  related: ui-design-fundamentals, interaction-design, information-architecture, usability-evaluation, ux-research, visual-design, mvp-prototyping, design-to-code-handoff, frontend-development, design-critique, ux-writing, accessible-design, layout-and-responsive-design
---

# Wireframing and Prototyping

A wireframe or prototype is an instrument for answering a question cheaply before answering it expensively in production. Its value is entirely in what it lets you learn or decide: whether a flow makes sense, whether people can find the thing, whether the idea is worth building, whether stakeholders agree on the direction, whether a technical approach is feasible.

The central skill is **matching the artifact to the question**. Too little fidelity and the question cannot be answered; too much and you have spent days polishing something you will throw away, and the polish distracts everyone from the question.

**Out of scope, handled elsewhere:**

- Visual styling, color, typography, imagery: `visual-design`, `ui-design-fundamentals`.
- Detailed interaction behaviors and micro-interactions: `interaction-design`, `motion-design`.
- Building a minimum viable product that real users use in production: `mvp-prototyping`.
- How to run and analyse usability tests rigorously: `usability-evaluation`.
- Specifying finished designs for implementation: `design-to-code-handoff`.

## Core principles

**1. Every prototype answers a question. Write it down first.** "Can new users find where to add a payment method?" "Does this dashboard layout make the overdue items obvious?" "Will the sales team accept a two-step quote flow?" A prototype without a question becomes a demo that can only be admired or disliked.

**2. Fidelity is multi-dimensional.** Visual polish, interactivity, content realism, breadth (how many screens and paths), and depth (how fully each path works) are separate dials. Turn up only the dials the question needs. A usability test of a checkout flow needs realistic content and deep interactivity along the main path, but can have rough visuals; a stakeholder review of brand direction needs high visual fidelity and almost no interactivity.

**3. Low fidelity invites the right feedback.** Rough artifacts signal "this is open to change", so people comment on structure, flow, and concept. Polished artifacts signal "this is nearly done", so people comment on colors and copy and hesitate to question the premise. Match the signal to the stage.

**4. Explore wide before going deep.** Early on, many rough alternatives beat one refined option. Comparing options exposes trade-offs and assumptions; a single option gets defended. Diverge, then converge.

**5. Real content beats placeholder text.** Lorem ipsum and "Product name" hide the problems that real content causes: long names, missing images, numbers with many digits, empty lists, translations. Use realistic content at any fidelity where layout or comprehension matters.

**6. Prototypes are disposable; learning is not.** Build to throw away. Once the question is answered, keep the findings and decisions and let the artifact go, unless it has been deliberately built as the start of production work.

**7. Fit the medium to the team and product.** Use the tools, components, and conventions the team already has. A prototype built from the team's design-system components or code components tests closer to reality and transitions faster. A prototype in a tool nobody else can open blocks collaboration.

## Fidelity: what it is and what it is for

| Fidelity | Typical form | Answers | Doesn't answer | Cost to change |
|---|---|---|---|---|
| Sketch | Paper, whiteboard, quick digital sketch | Concept, rough structure, which ideas to pursue | Detailed usability, visual appeal | Seconds |
| Low-fi wireframe | Grayscale boxes, real or near-real labels | Layout, hierarchy, content priority, flow | Visual design, micro-interactions | Minutes |
| Mid-fi | Real components (often design-system), realistic content, little styling | Comprehension, findability, task flow | Brand response, motion | Minutes to hours |
| High-fi mockup | Final visuals, static | Visual direction, brand fit, stakeholder sign-off | Interaction feasibility | Hours |
| Clickable prototype | Linked screens in a design tool | Navigation, flow, task success along scripted paths | Free exploration, real data, performance | Hours |
| Coded prototype | Throwaway code, real browser or device | Complex interactions, real data, responsiveness, performance, feasibility | Production quality (by design) | Hours to days |
| Wizard-of-Oz / concierge | A human behind the curtain fakes the system | Whether the concept is valuable before building the hard part (e.g. AI, automation) | Whether it can be built | Varies |

**Choose fidelity by question:**

- "Which of these ideas is worth pursuing?" → sketches, many of them.
- "Does this layout put the right things first?" → low-fi wireframes with real content.
- "Can people complete this task?" → clickable or coded prototype with realistic content and the main paths working.
- "Do people understand what this feature is for?" → mid-fi screens with real copy; interactivity optional.
- "Does this interaction feel right?" (drag-and-drop, gestures, animations, live search) → coded prototype or an interaction-capable tool; static screens cannot answer it.
- "Will this work on real data / real devices / at real speed?" → coded prototype.
- "Do stakeholders agree on direction?" → whatever fidelity matches their decision; for concept agreement, low-fi with a narrative; for brand sign-off, high-fi.
- "Would anyone actually want this?" → sometimes no prototype at all: a fake-door test, a landing page, a concierge pilot (see `mvp-prototyping`, `experiment-design`).

## Process

### 1. Frame the question and the audience

Write: the question; who will use the artifact (test participants, stakeholders, developers); the decision it informs; the deadline. This determines fidelity, breadth, and format before anything is drawn.

### 2. Gather inputs

- Requirements and constraints (see `product-requirements`, `user-stories`): what must be possible, what is out of scope.
- Research: user goals, top tasks, vocabulary (`ux-research`).
- Structure: where this fits in the product's IA (`information-architecture`).
- Existing patterns: the design system's components, existing screens doing similar things, platform conventions. Reuse before inventing; a new pattern must earn its novelty.
- Real content: actual data samples, real names and lengths, actual copy if it exists, edge cases (empty, one, many, error).

### 3. Diverge: sketch alternatives

- Produce several distinct approaches, not variations of one. Vary something fundamental: the organizing principle (list vs. map vs. calendar), the flow (one page vs. steps), the entry point, the primary action.
- Time-box it. Quantity is the point; quality comes later.
- Sketch flows, not just screens: what happens before and after, and on error.
- Involve others (developers, product, support) in sketching sessions; they bring constraints and ideas, and shared sketching builds alignment.

**Useful sketching formats** (pick by what you need to see):

- **User or task flows**: boxes and arrows for steps, decisions, and outcomes, including error branches. Draw these before screens when the problem is mostly about sequence; many design problems disappear once the flow is right.
- **Storyboards**: a few frames showing the user's situation before, during, and after using the product. Good for concepts where context matters (where they are, what triggered the need) and for aligning stakeholders on the "why".
- **Rapid multi-option sketching**: fold a page into panels and fill each with a different idea in a short fixed time per panel. Forces variety past the first obvious idea.
- **Thumbnail layouts**: tiny rectangles exploring placement and priority before any detail.
- **Content-first sketches**: list the content and actions a screen must contain, in priority order, before drawing any layout. The priority list often settles layout debates.

### 4. Converge: pick and refine

- Evaluate alternatives against the question and requirements: which best supports the top tasks? What are each one's risks?
- Combine strengths where coherent; avoid Frankenstein merges that lose each option's logic.
- Get quick feedback (`design-critique`) before investing in fidelity.

### 5. Build the artifact at the chosen fidelity

**Wireframes**

- Focus on hierarchy, grouping, and priority: what is first, what is grouped together, what is secondary.
- Use real or realistic labels and content. Placeholders hide length and comprehension problems.
- Keep visual treatment neutral (grayscale, a single typeface, simple shapes) so reviewers focus on structure. Use the product's actual components if they exist and help realism.
- Show states: empty, loading, partial, error, full, overflow. A wireframe set showing only the happy path with ideal data is incomplete.
- Consider the screen sizes the product supports; at least sketch the narrowest and widest (`layout-and-responsive-design`).

**Clickable prototypes**

- Build the paths the question needs, deeply; leave the rest shallow and clearly marked ("not part of this prototype").
- Make the main path forgiving: participants will click things you did not expect. Decide in advance how to handle dead ends (a "not available in this prototype" screen is better than nothing happening).
- Include realistic data, and enough of it, so scanning and searching behave believably.
- Prefer real form inputs where typing matters; faking text entry hides friction.
- Version it, so you know which version each participant saw.

**Coded prototypes**

- Use them when interaction, data, responsiveness, performance, or feasibility is the question.
- Write throwaway code deliberately: skip production concerns that do not affect the question (auth, persistence, edge-case hardening), but be honest about what was skipped.
- If the team's real component library is available, use it; the prototype will look and behave like the product and may transfer.
- Decide up front whether any of it will become production code. If yes, it is not a throwaway prototype; apply the relevant engineering standards (`frontend-development`, `testing-strategy`). If no, protect it from accidentally shipping.

**Wizard-of-Oz**

- A person simulates the system's intelligence (writing the "AI" responses, doing the "automatic" matching) behind a realistic interface.
- Useful for testing whether a concept is valuable before investing in the hard part. Ethically, debrief participants afterwards that a person was involved, unless consent covered it from the start.

### 6. Annotate

Annotations explain what the picture cannot. Write them for their audience:

- **For stakeholders**: the question being answered, the rationale for key decisions, alternatives considered, open questions.
- **For test facilitators**: what works, what does not, the tasks it supports.
- **For developers**: behavior, states, data sources, rules, edge cases, and what is intentionally unresolved (see `design-to-code-handoff` for full specs).

Good annotations are specific ("List sorts by due date, overdue first; ties by created date") and tied to a precise element. Number them or place them adjacent to the element, consistently with whatever convention the team uses. Mark the difference between decided and exploratory.

### 7. Test or review

- For usability questions, test with representative users (see `usability-evaluation`). Five or so participants per round finds most major issues in a prototype; iterate between rounds.
- Introduce prototypes honestly: it is unfinished, some things will not work, you are testing the design, not them.
- Watch behavior more than you listen to opinion. "I like it" is weak evidence; completing the task without hesitation is strong.
- For stakeholder reviews, restate the question and the decision you need from them, so feedback stays on topic.

### 8. Decide and move on

- Record what was learned, what was decided, and what is still open.
- Iterate on what failed; do not re-test what passed unless it changed.
- Increase fidelity only when the questions at the current fidelity are answered.

## States and content to cover

A wireframe set or prototype that only shows the ideal case hides most of the design work. For each key screen or component, decide which of these states the question requires, and at least list the rest for later:

| State | What to show | Why it matters |
|---|---|---|
| First use / empty | What is shown before any data exists, and the path to create the first item | Often the first impression; frequently forgotten |
| Loading | Skeletons, spinners, progressive loading, optimistic updates | Perceived speed and layout stability |
| Partial | One item, a handful, a half-completed form | Layouts tuned for "many" can look broken with one |
| Full / overflow | Hundreds of items, very long names, large numbers, many tags | Truncation, pagination, scanning, performance |
| Error | Failed load, failed save, validation errors, offline | Recovery paths; where messages appear |
| Permission | Read-only views, disabled actions, restricted content | Who sees what; how they ask for access |
| Success / done | Confirmation, next steps, undo | Closure and continuity |
| Responsive | Narrowest and widest supported sizes | Priority and reflow decisions |
| Localization | Longest likely translation, right-to-left if supported | Text expansion and mirroring |

**Realistic content checklist**: real or realistic names (short, long, non-Latin characters), real numbers (zero, negative, very large, decimals, currencies), real dates (today, overdue, far future, time zones), real images (missing, wrong aspect ratio, low quality), real copy (first drafts from `ux-writing` rather than placeholders).

## Prototyping particular kinds of features

- **Forms and data entry**: typing and validation are the experience; use a coded prototype or a tool that supports real inputs. Prototype errors and recovery, not only the filled-in form.
- **Data-heavy screens (tables, dashboards, analytics)**: use real or realistically distributed data; synthetic data that is too clean hides scanning, sorting, and outlier problems. Prototype filtering and sorting if the question is about finding things. See `dashboard-building`, `data-visualization`.
- **Direct manipulation (drag-and-drop, canvas editors, gestures)**: static screens cannot answer whether it feels right; prototype in code or an interaction-capable tool and test on target devices and input methods (mouse, touch, keyboard alternatives).
- **Search and recommendations**: the quality of results drives the experience. Use a realistic corpus and real queries from logs; hand-curate results for scripted tasks if real ranking is unavailable, and say so.
- **AI and automation features**: output quality, latency, and failure modes are central. A Wizard-of-Oz or a coded prototype calling a real model often answers more than polished static screens. Prototype what happens when the output is wrong, slow, or refused, and how users correct it. See `llm-application-development`.
- **Onboarding and multi-session flows**: the experience spans time; storyboards or a series of prototypes representing day 1, day 7, and day 30 can show it. Diary studies with prototypes are possible but heavy.
- **Notifications and cross-channel flows**: prototype the message in its real channel (email client, lock screen, chat) and the landing point in the product; the transition is often where it breaks.
- **Voice and conversational interfaces**: script dialogues and test them by reading them aloud or role-playing (one person plays the system); flow diagrams for intents and fallbacks serve as the wireframe.

## Asking for the right feedback at each fidelity

Reviewers comment on whatever is most visible. Steer them toward what the stage can still change:

| Stage | Ask reviewers about | Ask them to hold for later |
|---|---|---|
| Sketches | Which ideas solve the problem; missing ideas; risky assumptions | Layout detail, wording, visuals |
| Low-fi wireframes | Priority and grouping; flow; missing content or states | Colors, typography, imagery |
| Mid-fi / clickable | Comprehension; task completion; labels; edge cases | Pixel alignment, final illustration |
| High-fi | Visual hierarchy, brand fit, consistency with the system, accessibility of the visual layer | Re-opening the core flow (unless a serious problem emerged) |
| Coded prototype | Interaction feel, responsiveness, performance, feasibility | Code quality, unless it is meant to become production |

If a reviewer raises a stage-inappropriate point, note it for later rather than dismissing it; occasionally a "visual" comment reveals a structural problem (e.g. "this button looks too important" may mean the primary action is wrong).

## Managing prototype artifacts

Prototypes multiply quickly. Keep them useful:

- **Name and date versions** and record which version was used in which test or review; findings are meaningless if nobody knows what was tested.
- **Separate exploration from the source of truth.** Keep rough explorations in a clearly labelled area; when a direction is chosen, move it into wherever the team keeps current designs. Stakeholders and developers should never have to guess which file is current.
- **Archive, don't delete, abandoned directions**, with a note on why they were dropped. The same idea will be proposed again; the note saves the debate.
- **Watch access and data.** Shared prototype links often outlive their purpose. Remove real customer data, restrict access to unreleased features per the organization's confidentiality rules, and revoke public links after testing.
- **Link prototypes to decisions**: from the decision record or ticket to the artifact, and from the artifact to the findings.

## Presenting prototypes to stakeholders

- Open with the question and the decision you need. "We need to choose between a single-page and a stepped setup flow today."
- Show alternatives side by side with their trade-offs, not only your favorite.
- Walk through a realistic scenario (a named user with a goal) rather than screen by screen.
- Say what is rough on purpose and what feedback is out of scope at this stage.
- End with the decision and next steps written down; circulate them.

## Worked example: choosing fidelity

*Request*: "Make a prototype of the new bulk-edit feature for the customer table."

1. **What question?** Asking the requester reveals two: (a) will users discover and understand bulk edit, and (b) can the table handle selecting thousands of rows without confusion about what is selected (all on this page, or all matching the filter).
2. **Fidelity per question.** (a) needs mid-fi screens with real labels in the context of the real table, and a few clickable paths; visuals can follow the existing design system without new styling. (b) is about interaction and scale: selection across pages, "select all 4,312 matching", partial failures when some rows can't be edited. That needs real data volume and real behavior — a coded prototype using the existing table component.
3. **Breadth and depth.** Deep on selection and one edit type (change owner); shallow on the other edit types, labelled as such.
4. **States.** Selection of zero, one, a page, all matching; edit in progress for a large batch; partial failure ("Updated 4,290 customers. 22 couldn't be updated because they're locked." with a way to see which); undo.
5. **Testing.** Five participants who manage customer lists weekly; tasks framed as real goals ("Your colleague left; reassign all their accounts in the Northeast region to yourself").
6. **Outcome.** Participants found bulk edit quickly, but three of five believed "select all" selected every customer, not just the filtered ones; the label and confirmation copy changed, and the next round confirmed the fix. The coded prototype was discarded; the selection logic insights went into the spec.

## When working as an AI assistant

- If you can write code, coded prototypes (for example a single HTML page or a small app using the project's existing framework and components) are often the fastest way to answer interaction and content questions. Keep them obviously throwaway unless asked otherwise, and reuse the project's existing styling and components rather than inventing a look.
- When generating wireframes as text, diagrams, or simple markup, keep them visually neutral so feedback stays on structure, and use realistic content.
- Do not fabricate test results; you can prepare tasks, scripts, and prototypes, and analyse real session notes the user provides.
- State which fidelity dials you turned up and why, and what the artifact cannot tell the user.

## Discovering context

- **Tools and file conventions**: what the team uses for design files, prototypes, and code. Make artifacts others can open, comment on, and reuse.
- **Design system**: components, patterns, and tokens available in the design tool and in code. Prototyping with them is faster and more realistic.
- **Existing flows**: screenshots or the live product for the areas you are touching; new screens should fit them.
- **Constraints**: platforms, devices, accessibility requirements, technical limitations (data availability, API latency), localization.
- **Stakeholder expectations**: what fidelity they expect for what decision; some organizations equate polish with progress. Set expectations explicitly ("rough on purpose, because we're deciding the flow").

## Decision guidance

**Design tool vs. code.** Design-tool prototypes are faster for static layout and linear flows, easy to comment on, and accessible to non-developers. Code wins when the interaction is complex (drag, gestures, real-time updates), when real data or responsiveness matters, when testing accessibility with assistive technology, or when the designer and team are fluent in code. Many teams use both at different stages.

**Paper vs. digital sketches.** Paper and whiteboards are fastest and most inviting for group ideation, and nobody mistakes them for finished. Digital sketches are easier to share remotely and evolve. Use what helps the group generate ideas fastest.

**One prototype or several?** For concept-stage questions, testing two or three alternatives with each participant (in varied order) yields comparative insight and frees participants to criticize. For later stages, one refined prototype per round is typical.

**Breadth vs. depth.** A broad, shallow prototype (many screens, little works) suits concept and navigation questions. A narrow, deep one (one flow that fully works) suits task-success questions. Do not try to make everything work.

**When to skip prototyping.** For small changes using existing patterns with low risk, prototyping may cost more than building and observing. For changes that are cheap to reverse in production (feature flags, small audiences), shipping and measuring can be faster. Prototype when building is expensive, risky, or hard to reverse.

**Who builds the prototype?** Designers in design tools for layout and flow; designers or developers in code for interaction and data; pairs for feasibility questions. A designer–developer pair building a coded prototype together often resolves feasibility and design questions in one pass and makes handoff almost unnecessary.

**Reuse the prototype or rebuild?** Rebuild by default: the prototype was optimized for learning speed, not maintainability. Reuse only if it was built on production components and standards from the start, with that intention agreed.

**Responsive and multi-device.** Prototype the narrowest and widest supported sizes when layout is at stake; the in-between often reveals itself in code. For native mobile, test on a real device; desktop previews hide reach, thumb zones, and keyboard overlap.

## Pitfalls

- **Prototyping without a question**: produces a demo that is admired or disliked, not learned from.
- **Premature polish**: hours spent on visuals for a flow that will be redesigned after the first test; stakeholders anchoring on colors.
- **Lorem ipsum layouts**: break as soon as real content arrives.
- **Happy-path only**: no empty, error, loading, or overflow states; the design then fails in implementation.
- **Too many paths half-working**: participants wander into dead ends, and the session tests the prototype's gaps rather than the design.
- **Falling in love with the first idea**: no alternatives explored.
- **The prototype becomes production**: a throwaway is shipped with no tests, no accessibility, no error handling. Decide its fate up front.
- **Testing the wrong fidelity**: asking users whether they "like" a grey wireframe, or asking stakeholders to approve a flow from a mood board.
- **Over-trusting a clickable prototype**: perfect click targets, no latency, no real data, no typing. Real use will be messier.
- **Ignoring accessibility until later**: structural decisions in wireframes (heading order, focus order, touch target size, reliance on hover) are expensive to retrofit. Consider them from the first wireframe (`accessible-design`).
- **Inventing patterns that already exist** in the product or design system, creating inconsistency.
- **Stakeholder approval of a prototype mistaken for a specification**: the prototype shows one path with ideal data; the build needs rules, states, and edge cases it never had. Close the gap with a spec (`design-to-code-handoff`).
- **Fidelity mismatch within one artifact**: one pixel-perfect screen next to rough boxes draws all attention to the polished one. Keep fidelity consistent unless the contrast is intentional.
- **Testing too late**: waiting until the prototype is "ready" means changes have become expensive. Test the roughest version that can answer the question.
- **Annotations nobody reads**: walls of text detached from elements. Keep them specific and placed.

## Quality bar and verification

- [ ] The question, audience, and decision are written down, and the artifact's fidelity matches them (dial by dial).
- [ ] Alternatives were explored before converging, and the reasons for the choice are recorded.
- [ ] Content is realistic, including long, short, empty, and many-items cases where layout or comprehension matters.
- [ ] Non-happy states are represented where they affect the question.
- [ ] The paths needed for the question work end to end; everything else is clearly marked out of scope.
- [ ] Existing design-system components and product patterns are reused where they fit.
- [ ] Annotations are specific, attached to elements, and distinguish decided from open.
- [ ] Basic accessibility structure is considered (reading and focus order, headings, target sizes, no hover-only or color-only meaning).
- [ ] Versions are labelled, the current direction is unambiguous, and shared links do not expose real user data or confidential plans.
- [ ] If the prototype is code, its throwaway or production status is explicit to everyone who might touch it.
- [ ] After testing or review, findings and decisions are recorded, and the next step (iterate, raise fidelity, build, or drop) is explicit.

Before sharing, ask: if someone looked at this with no explanation, would they understand what question it is answering and what kind of feedback is wanted? If not, add the framing.

## Depth on demand

- `references/prototype-testing.md` — preparing a prototype for a test session, task scripts, handling prototype limitations live, and turning observations into iterations. Read before testing a prototype with users.
