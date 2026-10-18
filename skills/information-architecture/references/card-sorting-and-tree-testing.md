# Card Sorting and Tree Testing

Read this before running a card sort or tree test. Card sorting generates and compares structures from users' mental models; tree testing verifies whether a structure lets people find things. They answer different questions and work best in sequence.

## Card sorting

### Choosing the type

| Type | Question it answers | When |
|---|---|---|
| Open | How do people group these items, and what do they call the groups? | Early, before a structure exists, or when rethinking from scratch |
| Closed | Do people agree on which of our categories each item belongs to? | When you have candidate categories to compare |
| Hybrid | Do our categories fit, and what is missing? | When you have a draft but expect gaps |

### Preparing cards

- Use 30–60 cards for most studies. Fewer gives thin patterns; many more fatigues participants and degrades quality.
- Choose a representative sample of content, not everything: include top-task items, ambiguous items, and items from every area.
- Write cards as short, plain descriptions of the content, not current navigation labels. If cards reuse the label "Billing", people will create a "Billing" group because they match words. Describe instead: "See past payments", "Change payment card".
- Each card should be one concept at the same level of granularity. Mixing "Account" with "Change your password" confuses the task.
- Avoid cards that share a striking keyword unless that grouping is what you intend to test.

### Running

- Moderated (in person or remote) when you want to hear the reasoning; unmoderated online tools when you want more participants. A mix — a few moderated to understand, more unmoderated to quantify — works well.
- Instruct participants to group in the way that makes sense to them, that there are no wrong answers, and (for open sorts) to name groups using their own words. Allow an "I don't know / doesn't fit" pile.
- Ask afterwards which cards were hard to place and why. Those are your ambiguous items.

### Sample size

- Moderated open sort: around 15 participants per distinct user group often reveals stable patterns; insights start emerging from fewer.
- Unmoderated: more participants (often 30 or more per group) smooth out noise in the similarity data.
- Segment by user group if mental models plausibly differ; pooling different groups can produce a structure that fits neither.

### Analysis

- **Similarity matrix**: shows the percentage of participants who put each pair of cards together. Clusters of high agreement suggest robust groupings; cards with weak agreement everywhere are ambiguous.
- **Dendrogram / hierarchical clustering**: visualizes clusters at different agreement thresholds. Useful, but it is an algorithmic summary; it can suggest clusters no participant actually made.
- **Category names** (open sorts): standardize similar names ("Money", "Payments", "Billing") into themes and count them. The most common names are candidate labels.
- **Placement agreement** (closed sorts): for each card, what share placed it in each category. High agreement confirms; split placements identify items needing a cross-link or a clearer category scope.
- **Qualitative notes**: participants' reasoning often explains splits (e.g. "I put it under Account because I'd only do it once").

Interpretation rules:

- Look for patterns, not consensus. Perfect agreement is rare; robust clusters with 60–80% pairwise agreement are a strong signal.
- Expect experts and novices to sort differently. Decide whose model the structure should primarily serve, and support the other with search, cross-links, or shortcuts.
- Card sorting tells you how people think about the items, not where they will look for them in practice. Validate with a tree test.

## Tree testing

### Preparing the tree

- Use the full text hierarchy for the areas under test, or the whole structure if feasible. Text only: no visuals, no descriptions (unless descriptions will appear in the real navigation).
- Labels should be final candidates; tree tests are the best place to compare label variants.
- To compare structures, run separate tests (different participants per tree) with the same tasks.

### Writing tasks

- Write 8–10 tasks per participant; more causes fatigue and learning effects. Randomize task order.
- Base tasks on top tasks, plus risky areas (renamed sections, ambiguous items, new features).
- Phrase tasks as realistic scenarios in the user's words, without using the target label's words: not "Find Billing settings", but "Your card expired. Where would you update it?"
- Each task should have one or more correct destinations defined in advance. Decide whether multiple locations count as success.

### Sample size

Around 50 participants per tree gives reasonably stable success percentages for comparisons; fewer (e.g. 20–30) can still surface major problems. Recruit from the real audience.

### Metrics

- **Success rate**: share ending at a correct destination. The headline metric.
- **Directness**: share who reached the destination without backtracking. Low directness with high success means scent is weak but people eventually recover.
- **First click**: where people go first. A wrong first click strongly predicts failure; first-click data tells you which top-level label is stealing traffic.
- **Time**: secondary; useful to compare variants.
- **Path analysis**: common wrong paths show which labels mislead and suggest where cross-links would help.

### Interpreting and iterating

- Compare tasks against targets agreed before testing. Top tasks warrant high bars; rare tasks can tolerate lower ones.
- For each failed task, look at first clicks and wrong destinations. Typical fixes: rename the misleading label, move the item, add a cross-link from the wrong destination, or clarify a category's scope.
- Change one or two things, retest. Tree tests are cheap enough to iterate two or three times.
- Combine with a baseline: tree-test the current structure first so improvements are measurable.

## Common mistakes

- Using current navigation labels as card text, then "discovering" users agree with the current structure.
- Including many near-duplicate cards, which forces arbitrary splits.
- Tree-test tasks that give away the answer through matching words.
- Treating a dendrogram cut as the final IA.
- Testing with colleagues who know the product's internal vocabulary.
- Running one round and not iterating when results are mediocre.
- Ignoring the "don't know" pile and abandoned tasks, which often show the most important vocabulary gaps.
