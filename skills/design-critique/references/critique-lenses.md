# Critique Lenses by Artifact Type

Read this when critiquing an artifact type that needs more structure than the general dimensions in the main skill. Each lens is a set of questions; use the ones that matter for the design's goals, and skip the rest.

## Interfaces (screens and flows)

- **First glance**: in five seconds, can you tell what this is and what to do? Where does the eye land first, second, third — and is that the intended order?
- **Primary action**: is there one, is it visually and verbally distinct, and is it where users will look when ready to act?
- **Task flow**: count steps for the top task. Which steps could be removed, combined, defaulted, or deferred?
- **Decisions**: at each decision point, does the user have the information needed to choose?
- **Feedback**: after each action, is it clear what happened?
- **Reversibility**: can mistakes be undone? Are irreversible actions clearly marked and protected?
- **States**: empty, loading, partial, error, success, no permission, offline — are they designed?
- **Content stress**: long text, large numbers, missing images, many items, translations.
- **Consistency**: matching patterns elsewhere in the product and the design system; justified deviations only.
- **Input methods**: mouse, touch, keyboard, screen reader, voice; hover-only interactions; target sizes.

## Visual and brand work

- **Intent**: what impression should this create, and for whom? Does it?
- **Brand fit**: consistent with the brand's own guidelines and existing expressions — judged against the brand's identity, not the critic's taste.
- **Hierarchy**: size, weight, color, and space order the content by importance.
- **Typography**: legible at intended sizes and distances; a clear, limited set of styles; comfortable line length and spacing.
- **Color**: purposeful, consistent semantics, sufficient contrast, works for people with color-vision deficiencies, survives the media it will appear in (print, dark mode, projectors).
- **Composition**: alignment, grouping, balance, and rhythm support the reading order.
- **Imagery**: relevant, representative, consistent in style, appropriately licensed, and inclusive.
- **Craft**: alignment errors, inconsistent spacing, orphaned words, pixelation. Important at final stage; less so earlier.

## Data visualizations

- **Message**: what should the reader conclude? Is that the most visible thing?
- **Chart type**: matches the comparison (change over time, part-to-whole, distribution, correlation, ranking).
- **Honesty**: axes start where they should, scales are consistent, areas are proportional, uncertainty is shown where relevant, nothing is cherry-picked.
- **Labeling**: direct labels where possible, clear units, readable axis text, meaningful title.
- **Color**: encodes data meaningfully, accessible, not relied on alone.
- **Density**: no chart junk; enough context to interpret.
- See `data-visualization` for depth.

## Design-system components and patterns

- **Purpose**: is it clear when to use this component and when not to?
- **API and variants**: a minimal, coherent set of options; no variants that exist for one use case.
- **States**: default, hover, focus, active, disabled, loading, error, selected — all defined and accessible.
- **Composability**: works with other components; spacing and sizing follow system tokens.
- **Content resilience**: long labels, icons with and without text, translations.
- **Accessibility**: semantics, keyboard behavior, focus management, announcements.
- **Documentation**: usage guidance, do and don't examples, code parity.
- See `design-systems` for depth.

## Content-heavy pages (articles, documentation, marketing pages)

- **Purpose and audience**: does the structure match what readers come for?
- **Scannability**: headings that summarize, front-loaded paragraphs, lists where appropriate.
- **Calls to action**: clear, appropriately placed, not competing with each other.
- **Navigation within the page**: anchors, tables of contents for long pages.
- **Readability**: line length, type size, contrast, spacing.
- **Trust**: dates, authorship, sources where relevant.

## Presentations and slides

- **Argument**: is there a clear point, and does the sequence build it?
- **One idea per slide**: can each slide's point be stated in a sentence?
- **Text density**: readable from the back of the room or on a small screen; speaker detail kept in notes.
- **Visuals**: charts and diagrams that clarify rather than decorate.
- **Consistency**: layouts and styles used consistently, following the organization's template where one exists.
- See `presentations` for depth.

## Physical, service, and multi-channel designs

- **Context of use**: environment, posture, lighting, noise, time pressure.
- **Touchpoints**: does the experience hold together across channels (app, email, in person, phone)?
- **Handoffs**: where the user moves between people, systems, or channels, is anything lost?
- **Failure recovery**: what happens when something goes wrong mid-journey?
- **Inclusivity**: physical reach, strength, dexterity, language, literacy.

## Critiquing as an AI assistant

- State the goals, audience, and constraints you assumed, and invite correction before or alongside the critique.
- Work from what you can actually see or test. If you only have a static image, say that interaction, motion, and responsive behavior were not evaluated. If you can interact with a live build or prototype, do so.
- Don't present taste as fact, and don't impose a generic "modern" aesthetic: judge visual choices against the product's own brand and design system.
- Be specific about locations (element, screen, step), since the designer can't point at what you mean.
- Flag where real-user testing would settle a question better than your judgment.
- Keep feedback proportionate: the top issues first, then a compact list of the rest.
