---
name: presentations
description: >-
  Build slide decks and talks that make one clear argument to a specific
  audience: storyline before slides, one idea per slide, evidence and visuals
  instead of text walls, data slides, speaker notes, fitting audience and time
  slot, and a visual style derived from the organisation's brand or the
  content itself rather than a default theme. Tool-neutral (PowerPoint,
  Keynote, Google Slides, HTML frameworks, LaTeX Beamer, or generated decks).
  Use when asked to make, outline, restructure, or improve a presentation,
  pitch deck, keynote, conference talk, lecture slides, board/QBR/status deck,
  demo-day deck, or speaker notes. Not for the mechanics of programmatically
  writing .pptx files (document-generation), standalone chart design
  (data-visualization), or written reports and memos (technical-writing,
  business-communication).
metadata:
  category: product-and-communication
  related: technical-writing, business-communication, data-visualization, visual-design, document-generation, copywriting, curriculum-design, writing-review-and-editing
---

# Presentations

A presentation is an argument delivered over time to people who cannot scroll back. That constraint shapes everything: the audience gets each point once, in the order you choose, at the speed you set, while splitting attention between your voice and the screen. A good deck works *with* that constraint — one idea at a time, in a deliberate sequence, with visuals that support what is being said rather than competing with it.

## Scope

This skill covers planning and building decks and talks: storyline, slide-level design, data slides, speaker notes, timing, and adapting to audience and setting. It applies whether the deck is built by hand in a slide tool or generated in code.

Neighbouring skills:

- `document-generation` — the mechanics of producing a .pptx/.pdf/HTML file programmatically, and verifying it renders.
- `data-visualization` — deep chart design; this skill covers how charts work *on slides*.
- `visual-design` — typography, colour, and composition in depth.
- `technical-writing` / `business-communication` — when the deliverable is a read document or memo, not a talk.
- `curriculum-design` — designing a whole course; this skill covers individual lecture decks.
- `copywriting` — persuasive language for sales and marketing decks.

## Core principles

### 1. Storyline before slides

The most common failure is opening the slide tool first. Slides built before the argument is clear become a pile of facts in roughly the order the author discovered them. Write the storyline first — in plain sentences, on paper or in a text file — and only then make slides that carry it. If the story doesn't work as a list of sentences, no amount of design will rescue it.

### 2. Know the one thing

State the single message the audience should leave with, in one sentence a listener could repeat to a colleague afterward. "Our churn is driven by onboarding, not pricing, and fixing onboarding is worth ~$2M/yr" is a message. "Q3 churn analysis" is a topic. Everything in the deck either supports the message, is necessary context for it, or should go.

### 3. One idea per slide

Each slide makes one point. The audience reads faster than you speak, so a slide with three ideas has them reading ahead to idea three while you're explaining idea one. One idea per slide keeps attention aligned with your voice, and it makes the deck easy to reorder and cut.

A strong test: can you write the slide's point as a full-sentence title (an "action title" or "assertion title")? "Onboarding drop-off accounts for 60% of churn" tells the audience what to conclude; "Churn breakdown" makes them work it out. Research on assertion–evidence slide design supports this: a sentence headline plus visual evidence improves comprehension over topic-title-plus-bullets. If you can't write the assertion, you don't yet know what the slide is for.

### 4. Evidence and visuals over text walls

A slide is not a document. Dense text forces the audience to choose between reading and listening, and they will read — badly, while ignoring you. Put the detail in your voice and the speaker notes; put on the slide what is better *seen* than heard: the chart, the diagram, the photo, the number, the quote, the before/after.

The exception is a deck designed to be **read, not presented** (sent ahead, read in a meeting, left behind). That is a different artifact — closer to a document in slide format — and may carry more text. Decide which you are building (see Decision guidance); a deck that tries to be both usually fails at both.

### 5. Fit the audience and the slot

The same content becomes a different deck for executives (decision first, five slides, appendix for detail), peers at a conference (narrative, insight, demo), a classroom (build up concepts, check understanding), or a sales prospect (their problem first, your product second). Time is a hard constraint: a rough planning rate is one to two minutes per content slide for talk-driven decks, faster for image-heavy keynote styles, slower for dense analytical slides. Plan to finish early — talks almost always run longer than rehearsal, and Q&A eats the margin.

### 6. Style comes from the brand or the content — never a default theme

Default templates signal "made in a hurry", and arbitrary styling choices (a trendy gradient, a random palette) distract from the content and clash with the organisation presenting it. Derive the visual system from:

1. **The organisation's brand** — existing templates, brand guidelines, logos, colour tokens, fonts, prior decks from the same team. Use the official template when one exists.
2. **The content and setting**, when no brand applies — a scientific talk wants restraint and legible charts; a product launch can carry more visual energy; a classroom deck for teenagers differs from a board deck. Choose deliberately and keep the choice consistent.

Never impose a personal or "house" aesthetic. A coherent, restrained system applied consistently beats a striking one applied unevenly.

## Process

### Step 1: Brief

Establish before outlining:

- **Audience**: who, how many, what they know, what they care about, what they're sceptical of, who the decision-maker is.
- **Goal**: what you want them to *do* or *believe* afterward (approve, buy, learn, adopt, fund, stop worrying).
- **Setting**: live in a room, remote video, recorded, conference stage, sent as a read-ahead; screen size and aspect ratio (16:9 is common, but check the venue or platform); whether slides will be shared afterward.
- **Time**: slot length, and how much is reserved for Q&A or discussion.
- **Constraints**: brand template, required sections (e.g. a funder's mandated pitch structure), confidentiality, tool the deck must be delivered in.
- **Material**: data, prior decks, docs, demos, people to quote.

Ask about anything that would change the structure — audience and goal especially. Make sensible assumptions about the rest and state them.

### Step 2: Write the message and the storyline

1. Write the one-sentence message.
2. Choose a narrative structure that fits the goal (see the table below).
3. Write the storyline as a sequence of full-sentence assertions — one per future slide. Read them aloud in order. They should form a coherent argument on their own, without any slides. This is sometimes called a "ghost deck" or "skeleton".
4. Check: does each sentence follow from the previous? Is any one unsupported? Is anything there just because you have the data?

| Goal | Structure that tends to work |
|---|---|
| Get a decision | Recommendation first → why (2–4 supporting points) → risks/alternatives → ask. Executives want the answer before the reasoning. |
| Persuade a sceptical audience | Shared situation → complication (what changed, what's at stake) → resolution → evidence → ask. (Often called situation–complication–resolution.) |
| Teach | Hook/question → concepts built in order, simple to complex → worked example → practice or check → recap. |
| Report status | Headline status → what changed since last time → risks and asks → details in appendix. |
| Pitch a product/startup | Problem → why now → solution → evidence (traction, demo) → market → business model → team → ask. Adapt to the audience's expected order. |
| Share research | Question and why it matters → approach → key findings (the few that matter) → implications → limitations → next steps. |
| Inspire / keynote | A tension or story → a reframing insight → what it means for the audience → a memorable close. |

These are lenses, not mandatory templates; mix them where the content demands.

### Step 3: Design each slide around its assertion

For each storyline sentence, ask: *what would the audience need to see to believe this?* That's the slide's evidence:

- A trend or comparison → a chart designed to show exactly that comparison.
- A process or system → a diagram.
- A claim about people → a quote, photo, or short clip.
- A single striking number → the number, large, with context.
- A change → before/after.
- A demo → the demo, with a fallback recording.

If the only evidence is more text, reconsider: maybe the point belongs in your voice, or the slide should be merged with another.

### Step 4: Build the visual system

Before making many slides, set the system: slide masters/layouts, title style, body text size, colour roles (text, background, one or two accents, a highlight colour, chart series colours), font pairing, grid and margins, how charts and code are styled. Pull every value from the brand where it exists. Building the system first means changes propagate and slides stay consistent; styling slide-by-slide guarantees drift.

Use the tool's own layout/master system (slide masters in PowerPoint and Keynote, themes in Google Slides, a stylesheet in HTML frameworks such as reveal.js or Marp, a theme in LaTeX Beamer) rather than hand-formatting each text box. It keeps decks editable by others.

### Step 5: Draft slides, then speaker notes

Build slides from the storyline. Then write notes for each: what you'll say, the transition to the next slide, numbers or names you need at hand, and timing cues. Notes are where the detail lives that you took off the slide.

### Step 6: Rehearse and cut

Run the talk aloud with a timer — at least once, ideally twice. Rehearsal reveals what reading never does: slides that need too much explaining, transitions that don't connect, and the fact that you are 40% over time. Cut whole slides rather than talking faster. Move supporting detail to an appendix (backup slides) you can pull up in Q&A.

If you can't rehearse (e.g. you're generating a deck for someone else), estimate timing from the notes (roughly 130–160 spoken words per minute) and tell the user.

### Step 7: Verify the artifact

See Quality bar. Open or render the actual file; check it on the delivery setup if possible.

## Slide-level guidance

### Titles

- Use assertion titles for analytical, persuasive, and teaching decks: a full sentence stating the takeaway, ideally on one or two lines.
- Topic titles ("Agenda", "Q&A", "Appendix: methodology") are fine for navigational slides.
- Reading only the titles in sequence should tell the whole story. This "title test" is the fastest check of a deck's logic.

### Text on slides

- Prefer a few words that cue your speech over sentences you will read aloud. Reading slides verbatim is the most reliably disliked presenter behaviour.
- If bullets are needed, keep them short and parallel; three to five is a ceiling, not a target. Nested bullets on a presented slide are almost always a sign the slide is a document.
- Text must be legible from the back of the room or on a small video tile. As a rough guide, body text below ~18 pt (in a 16:9 deck at standard size) is hard to read when projected; titles larger. Remote audiences often view slides in a small window, so lean larger, not smaller.
- Reveal content progressively (builds) when a slide has a sequence and you want attention on one part at a time — but use builds for pacing, not decoration.

### Visual hierarchy

Each slide should have one obvious place to look first. Use size, contrast, position, and colour to direct attention to the point that matters — highlight the one bar, the one line, the one cell. Grey out context. Leave space; crowding makes everything equally loud.

### Images

Use images that carry information or emotion relevant to the point; avoid generic stock photos that decorate without meaning. Check image rights and licences. Ensure resolution holds up on a large screen. Never stretch images out of aspect ratio.

### Code on slides

Show only the lines that matter — a few, not a file. Use a legible monospace size, syntax highlighting with sufficient contrast, and highlight the line under discussion. For live coding, have a pre-recorded or pre-built fallback.

### Diagrams

One concept per diagram, consistent shapes for consistent meanings, labelled arrows, and build complex diagrams up in stages so the audience follows the construction.

## Data slides

Data slides are where decks most often fail, because analysts paste the chart they used for exploration rather than designing one for the point.

1. **The title states the finding.** "Mobile conversion fell 18% after the redesign" — not "Conversion by platform".
2. **One chart, one message.** If the chart supports two points, make two slides or highlight differently on each.
3. **Choose the chart for the comparison**: change over time → line; comparing categories → bar (sorted, usually horizontal if labels are long); part-to-whole with few parts → stacked bar or, sparingly, a pie/donut with very few slices; relationship → scatter; distribution → histogram or box plot. See `data-visualization`.
4. **Strip the clutter**: remove gridlines that don't help, redundant legends (label lines directly), 3D effects, unnecessary decimals. Keep axis labels, units, and the source.
5. **Highlight the point**: accent colour on the series or data point that matters, everything else muted; annotate directly ("Redesign launched").
6. **Make it honest**: start bar axes at zero; label truncated axes clearly; don't cherry-pick time windows; show uncertainty where it's material; keep comparisons on the same scale.
7. **Cite the source and date** in small text on the slide. Audiences ask, and decks get forwarded.
8. **Simplify tables**: a presented table should have few rows and columns, with the key cell highlighted. Put full tables in the appendix or a handout.
9. **Big numbers** work when one figure carries the point — but give it context (compared to what? over what period?).

## Speaker notes

Good notes contain:

- The point of the slide in one line (so you never lose the thread).
- What you'll say — as prompts or a script, depending on the speaker's preference and the stakes (keynotes and recorded talks often warrant a fuller script; internal updates rarely do).
- The transition to the next slide — the sentence that connects them. Transitions are where talks feel coherent or fragmented.
- Exact figures, names, and citations you may be asked about.
- Timing checkpoints ("should be at ~10 min here").
- For decks someone else will present: enough context that they can deliver it without you, including the "why" behind each slide.

## Decision guidance

### Presented deck vs. read deck

| Factor | Presented (talk) | Read (document in slides) |
|---|---|---|
| Who carries the explanation | The speaker | The slide |
| Text density | Low; cues and evidence | Higher; complete sentences, self-explanatory charts |
| Titles | Assertions | Assertions, plus clear body text |
| Notes | Essential | Optional |
| Typical use | Conferences, pitches, all-hands, lectures | Pre-reads, board packs, leave-behinds, async updates |

If the deck must serve both, build the presented version and put the detail in notes or an appendix — or produce two artifacts. Some organisations prefer a written memo over slides for decisions precisely because read decks fragment reasoning; if that's the culture, follow it.

### Tool choice (when the user hasn't chosen)

| Need | Reasonable options |
|---|---|
| Organisation's standard, editable by colleagues | Whatever they use: PowerPoint, Keynote, Google Slides |
| Real-time collaboration | Cloud slide tools (e.g. Google Slides, PowerPoint online) |
| Version control, text-based, developer audience | Markdown/HTML frameworks (e.g. reveal.js, Marp, Slidev) |
| Heavy mathematics, academic setting | LaTeX Beamer, or HTML with math rendering |
| Generated from data, repeated regularly | Programmatic generation (see `document-generation`), from a template the org owns |
| Must open anywhere, no editing needed | Export to PDF (check fonts and builds flatten acceptably) |

Respect the format the recipient needs. Delivering a beautiful HTML deck to someone who must edit it in PowerPoint fails the brief.

### Depth vs. breadth

Under time pressure, cover fewer points well rather than many points shallowly. Audiences retain few points from any talk; three well-supported ideas outlast ten rushed ones. Everything else goes to an appendix or a follow-up document.

## Discovering context

- Ask for or look for the organisation's slide template, brand guidelines, or recent decks by the same team. Match layouts, colours, fonts, logo placement, and title conventions. If the template is missing a layout you need, extend it in the same visual language.
- Look for conventions in the audience's world: some boards expect a specific order; some conferences mandate templates, aspect ratios, or a title slide format; academic venues have norms about citations on slides.
- Check fonts are available on the presenting machine, or embed them / choose fonts that are; missing fonts reflow text and break layouts.
- Check accessibility requirements (organisational policy or the audience's needs).

When no brand exists, derive a small system from the content: one typeface family (or a pairing) chosen for legibility, a neutral text/background pair with strong contrast, one or two accent colours used purposefully, and consistent spacing. State the choice so the user can swap in their brand later.

## Adapting to setting

- **Remote/video**: slides appear in a small window beside faces and chat. Use larger text, fewer elements, higher contrast, and more frequent visual changes (a static slide for four minutes loses a remote audience faster than a room). Build in explicit interaction points — a question, a poll — because you can't read the room. Share the deck link in chat if appropriate.
- **Recorded**: tighter scripting, no references to "this room", and captions. Pace slightly slower than live.
- **Large stage**: fewer words, bigger visuals; assume the back row can see only the largest elements. Confirm aspect ratio and confidence-monitor setup with the organisers.
- **Small meeting / discussion**: the deck is a prop for conversation. Fewer slides, more time for discussion, an appendix to answer questions on the spot.
- **Hybrid**: design for the remote viewers (their experience is the weakest) and repeat in-room questions aloud.

## Working from an existing deck

Many requests are "improve this deck" or "turn these 40 slides into 10". Approach it as an edit of the argument, not a reformatting job:

1. Extract the current titles in order and read them as a storyline. Identify the message (or note that there isn't one).
2. Re-establish the brief: audience, goal, time — it may differ from what the deck was originally built for.
3. Write the new storyline; map existing slides onto it. Many will become appendix, merge, or disappear.
4. Rework surviving slides: assertion titles, one idea each, redesigned charts.
5. Restyle using the organisation's template, preserving any content the owner will expect to find.

Tell the user what you cut and why; owners are attached to their slides, and a short rationale prevents unnecessary back-and-forth.

## Accessibility

- Sufficient colour contrast between text and background, including text on images (WCAG's 4.5:1 for normal text is a sensible floor; projectors wash out contrast, so exceed it).
- Don't encode meaning by colour alone; add labels, patterns, or position.
- Use real slide titles in the tool's title placeholders (screen readers and navigation depend on them) and a logical reading order.
- Alt text for informative images and charts; mark decorative images as decorative.
- Avoid rapid flashing animation; keep motion purposeful and modest.
- Provide captions for embedded video; share slides in advance for audiences who need them.
- Readable fonts at sufficient size; avoid long passages in all caps or italics.

## Pitfalls

- **Slides first, story never.** A sequence of unrelated facts. Fix by writing the storyline and the title test.
- **The text wall.** Paragraphs or ten bullets per slide; the audience reads instead of listening. Move text to notes.
- **Topic titles everywhere.** "Results", "Findings", "Data" — the audience must infer what to conclude, and often infers wrong.
- **Exploration charts.** Default chart output pasted in, with eight series, a legend, and no highlighted point.
- **Too many slides for the slot.** Leads to rushing and skipping the conclusion. Cut, don't accelerate.
- **Burying the ask.** Decision-makers leave before slide 30. Put the recommendation or ask early and repeat it at the end.
- **Inconsistent styling.** Fonts, colours, and alignment drift slide to slide, signalling carelessness and pulling attention. Use masters.
- **Default theme or arbitrary decoration.** Generic templates and ornamental flourishes that don't come from the brand or content.
- **Gratuitous animation and transitions.** Movement attracts attention; spend it only where it helps the audience follow.
- **Unreadable on the actual screen.** Small fonts, low contrast, thin lines that vanish on a projector or video call.
- **Untested demo.** Live demos fail at the worst moment. Rehearse on the actual setup and keep a recording.
- **Copying content without permission** — images, logos, other people's charts. Use licensed material and cite sources.
- **Unverified numbers.** One wrong figure discredits the whole deck in the audience's mind. Check every number against its source (see `fact-checking`).
- **Ending on "Questions?"** with no summary. Close on the message and the ask; take questions after.

## Quality bar

Before handing over:

- [ ] The one-sentence message is clear, and the deck's first and last content slides reinforce it.
- [ ] Reading only the slide titles tells the story in a logical order.
- [ ] Each slide has one idea and one obvious focal point.
- [ ] Evidence (charts, diagrams, examples) supports each assertion; data slides state the finding, highlight it, cite the source.
- [ ] Every number is verified against its source.
- [ ] Slide count and notes fit the time slot with margin for Q&A.
- [ ] The visual system comes from the brand or a deliberate content-derived choice, applied consistently via the tool's masters/themes.
- [ ] Text is legible at presentation size; contrast passes; colour is not the only carrier of meaning.
- [ ] Speaker notes exist for presented decks, including transitions.
- [ ] The file has been opened/rendered in the delivery format and checked slide by slide: no overflowing text, missing fonts, broken images, misaligned elements, or stray placeholder text.
- [ ] Confidential or draft material is removed if the deck will be shared.

When reporting back, include the storyline (titles in order), estimated runtime, any assumptions about audience and setting, and anything unverified.

## Illustrative example: from topic deck to argument

*Illustrative only.* A user asks for "a deck on our Q3 support metrics" for a 15-minute leadership meeting.

A topic-driven first draft would have slides titled "Ticket volume", "Response time", "CSAT", "Top categories", "Staffing", each with a default chart — twelve slides of facts and no point.

Applying this skill: the brief reveals leadership must decide whether to fund two more support hires. The message becomes "Ticket volume is growing faster than headcount, and response times will breach our SLA by Q1 unless we add two agents or cut the top driver of tickets." Storyline titles:

1. Recommendation: fund two agents now, and invest in fixing billing confusion, the top ticket driver.
2. Ticket volume grew 34% in Q3 while headcount was flat.
3. Median first response time has doubled since Q1 and crosses the SLA in January at the current trend.
4. Billing questions are 40% of tickets — most are about one confusing invoice line.
5. Two options: hire (cost, time to ramp) vs. fix billing UX (cost, uncertainty) — we recommend both.
6. Ask: approve two hires and a billing UX sprint.

Six slides for fifteen minutes, with an appendix holding CSAT and category breakdowns for questions. Each data slide highlights the one series that matters, and the response-time chart annotates the SLA line and the projected crossing.
