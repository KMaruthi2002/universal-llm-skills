# Writing Up Usability Issues

Read this when writing up an expert review or usability test. The goal of a write-up is not to document the study; it is to get the most important problems fixed. Shape every choice around the readers who will make or approve fixes.

## Know the readers

- **Decision-makers** need the top issues, their impact, and what is recommended, in a few minutes.
- **Designers** need the evidence and the cause of each issue, to design a good fix.
- **Developers** need precise locations, reproduction details, and the expected behavior.
- **Future teams** need method, participants, and dates, to compare or repeat.

Match the format to how the team already consumes information: a short readout, a document, tickets in their tracker, a recorded walkthrough, or a combination. Many teams act faster on tickets than on long documents; consider both.

## What a good write-up contains

In roughly this order of prominence:

1. **The headline**: the few issues that matter most, their severity, and the recommended direction. If the reader stops here, they should know what to do.
2. **Overall picture**: how participants fared across tasks (e.g. a compact table of task success), and what worked well.
3. **Issues**, grouped by root cause or by flow, ordered by severity.
4. **Method and participants**: method, dates, number and profile of participants, tasks, environment, prototype or build version.
5. **Limitations**: what the study could not show, sample constraints, prototype artifacts.
6. **Appendix**: full task wording, detailed metrics, links to recordings (with access controls).

## Writing an issue

Each issue should make sense on its own, since it may be copied into a ticket. Include:

- **A specific title** that states the problem, not the location: "Users can't tell whether 'Select all' includes filtered-out rows" rather than "Select all issue".
- **Where**: screen, element, flow step, and build or prototype version.
- **What happened**: the observed behavior, with counts ("4 of 6 participants…").
- **Evidence**: brief quotes, timestamps or clips, screenshots with the relevant area marked.
- **Why it likely happened**: the design cause (ambiguous label, hidden control, missing feedback, conflicting mental model). This is what designers need most.
- **Severity**, from the written scale, with the reason.
- **Recommendation**: the problem to solve and, optionally, a suggested direction. Leave room for the designer to find the best solution; prescribe specifics only when the fix is obvious and small.
- **For inspection findings**: the principle or heuristic involved and a note that it is an expert judgment, not observed.

### Illustrative example

> **Users can't tell whether "Select all" includes rows outside the current filter** — *Major*
>
> *Where*: Customers table, bulk actions bar (prototype v3).
>
> *What happened*: 4 of 6 participants, asked to reassign all accounts in one region, used "Select all" and believed every customer in the system was selected. Two hesitated and abandoned the action for fear of changing other regions' accounts.
>
> *Evidence*: P3: "Wait — is this all of them, or just these?" (12:40). P5 cancelled at the confirmation step (18:05).
>
> *Why*: The label doesn't state its scope, and the confirmation shows a count without saying what it counts.
>
> *Recommendation*: Make the selection's scope explicit at the point of selection and at confirmation (e.g. state the count and the filter it applies to). Retest with the same task.

## Prioritization

- Present issues by severity, then by how many tasks or users they affect.
- Distinguish quick wins (high impact, low effort) from structural problems; teams benefit from knowing both. Effort estimates come from the team, not the evaluator; involve them.
- Don't hide critical issues among cosmetic ones. If there are many minor issues, summarize them in a single list.

## Tone

- Neutral and evidence-based. Describe what happened and why; avoid judgmental language about the design or its designers.
- Never mock participants or quote them in ways that embarrass them.
- Acknowledge what works, specifically. Teams need to know what to preserve, and balanced write-ups are more credible.

## Getting issues fixed

- Hold a readout or working session with the team; invite people who observed sessions to share what they saw.
- Agree on owners and next steps for critical and major issues during the session.
- Put issues where work is tracked, linked back to the evidence.
- Schedule a retest for the important fixes, ideally with new participants on the same tasks.
- Revisit the issue list after the next release: what was fixed, what was deferred, what got worse.

## Common write-up mistakes

- Burying the most important issue.
- Listing symptoms without causes, so fixes treat symptoms.
- Prescriptive pixel-level solutions that a designer would have solved better.
- Percentages from tiny samples.
- Missing version information, so nobody can reproduce the issue.
- Write-ups that only exist as a long document no one reopens after the readout.
- Sharing recordings or identifiable details beyond the people who need them.
