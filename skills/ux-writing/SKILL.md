---
name: ux-writing
description: >-
  Write and edit interface copy and microcopy: button and link labels, form
  labels and hints, error and validation messages, empty states,
  confirmations, notifications, onboarding, tooltips, and settings
  descriptions; build consistent terminology; adapt tone to the product's
  existing voice; and prepare strings for localization. Use when writing or
  reviewing any text that appears inside a product UI, naming a feature or
  action, fixing confusing or unhelpful messages, or creating a content style
  guide for an interface. For marketing pages and persuasive copy use
  copywriting; for long-form docs use technical-writing; for navigation
  structure and taxonomy use information-architecture.
metadata:
  category: design
  related: copywriting, technical-writing, information-architecture, interaction-design, accessible-design, design-systems, error-handling, usability-evaluation, writing-review-and-editing
---

# UX Writing

Interface copy is part of the interface. A label is a control's affordance in words; an error message is the product's recovery mechanism; an empty state is the first page of an onboarding flow. Most usability problems that look like design problems are partly words problems, and many are fixed by changing a few of them.

This skill covers the words inside products: what they need to do, how to write them so people can act, how to keep them consistent, how to fit them to a product's voice without inventing one, and how to make them survive translation.

**Out of scope, handled elsewhere:**

- Marketing, landing pages, ads, persuasive and brand storytelling: `copywriting`.
- Documentation, help-center articles, API references: `technical-writing`.
- Navigation structure and the taxonomy behind labels: `information-architecture`.
- Proofreading and editing of long-form prose: `writing-review-and-editing`.
- The engineering side of errors (codes, retry logic, logging): `error-handling`.

## Core principles

**1. Copy exists to help someone do something.** Every string should answer a question the user has at that moment: What is this? What will happen if I press it? What went wrong? What do I do now? Text that answers no question is noise, and noise trains people to stop reading.

**2. Clarity beats cleverness, every time it matters.** Wit can be lovely in low-stakes moments when the product's voice calls for it. In moments of confusion, risk, money, data loss, or frustration, it reads as dismissive. A user who cannot understand a message fails regardless of how charming it is.

**3. People scan; they do not read.** Users look at the first couple of words of a line and the labels on buttons. Put the most important information first, keep it short, and make it make sense even if that is all they read.

**4. Be specific.** Vague copy ("Something went wrong", "Submit", "Are you sure?") shifts the work of figuring out what is happening onto the user. Specific copy ("We couldn't save your changes because you're offline", "Send invoice", "Delete 3 files permanently?") does that work for them.

**5. Consistency is a usability feature.** If the same thing has two names, users assume they are two things. If the same action has three verbs, users wonder whether they differ. A consistent vocabulary lets users transfer learning from one screen to the next.

**6. Voice belongs to the product; tone adapts to the moment.** Voice is the product's stable personality, defined by the brand or by the existing UI. Tone is how that voice adjusts to context: more direct in errors, more reassuring in destructive confirmations, lighter in a success state. Your job is to discover the voice and modulate tone, not to impose your own.

**7. Write for everyone who will read it.** That includes people using screen readers, people reading in a second language, people under stress, people with cognitive disabilities, and the translators who will localize it. Plain language serves all of them and costs experts nothing.

## Discovering context first

Before writing a word for an existing product:

- **Find the content guidelines**: a content or voice-and-tone guide, the design system's writing section, a glossary or terminology list, localization style guides. If they exist, they win over anything here.
- **Read the existing UI**: collect the labels, messages, and headings already in the product (the string files in the codebase are often the fastest way). Note capitalization style (sentence case vs. title case), person (you/your vs. my, we vs. the product name), punctuation habits (periods on single sentences, exclamation marks, ellipses), contractions, how numbers and dates are formatted, and the verbs used for core actions.
- **Infer the voice** from that sample if no guide exists: formal or casual, terse or explanatory, playful or neutral, technical or lay. Describe it in a few words and write to match. When the existing voice is inconsistent, follow the dominant pattern in the area you are touching and flag the inconsistency rather than unilaterally rewriting the product.
- **Know the audience and domain**: their expertise, their vocabulary, the stakes of what they are doing (a medical dosage screen is not a photo filter), and the platforms (platform conventions for button order, capitalization, and system dialogs vary between operating systems).
- **Check constraints**: character limits, truncation behavior, small screens, notification length limits, legal or regulatory wording that must appear verbatim, and which languages the product ships in.

## What each kind of copy needs to do

### Buttons and action labels

- **Name the outcome, usually with a verb.** "Save draft", "Send invoice", "Create project" tell users what happens. "OK", "Submit", "Yes", "Continue" make them reread the surrounding text.
- **Match the label to the heading or question.** If a dialog asks "Delete this project?", the button is "Delete project", not "Yes" or "Confirm".
- **Keep the same verb through a flow.** If the entry point says "Publish", the confirmation says "Publish", and the success message says "Published". Switching to "Post" or "Go live" midway creates doubt.
- **Make the destructive or irreversible action unmistakable** in wording ("Delete permanently", "Cancel subscription"), not only in color, so it is clear to people who cannot perceive color.
- **Distinguish the two buttons in a choice.** "Cancel" next to "Cancel subscription" is ambiguous; use "Keep subscription" and "Cancel subscription".
- **Links say where they go.** "View billing history", not "Click here" or "Learn more" (or, if a short "Learn more" is a convention in the product, make its accessible name specific, e.g. via visually hidden text).

### Form labels, hints, and placeholders

- **Labels are always visible.** Placeholder text that disappears on focus is not a label; users lose it the moment they start typing, and it is often low-contrast.
- **Label with what the field is**, in the user's terms: "Work email", not "Email address (primary contact identifier)".
- **Hints explain format or purpose before the error happens**: "We'll use this to send receipts", "Must be at least 12 characters". Put requirements up front instead of revealing them one error at a time.
- **Mark optional or required consistently**, using whichever convention the product uses; if most fields are required, marking the optional ones is less noisy.
- **Ask only what is needed, and say why for sensitive fields.** Explaining why you need a phone number increases completion and trust.

### Error and validation messages

The full guide is in `references/error-messages.md`. The essentials:

- **Say what happened, in plain terms, and what to do next.** "Your card was declined. Check the number or try a different card." beats "Payment error (code 402)".
- **Don't blame the user.** "That password is too short" not "You entered an invalid password". Avoid words like "invalid", "illegal", "fatal", "failed" aimed at the person.
- **Be precise about the problem.** "Enter a date in the future" is better than "Invalid date".
- **Put the message where the problem is**: next to the field for validation, in context for inline failures, at the top only for page-level issues (with links to each field).
- **Preserve the user's work.** The message is pointless if the form wipes their input.
- **Include codes only when they help** (support can look them up); put them after the human explanation.
- **Distinguish the user's problem from the system's.** If it is the product's fault, say so and say what is happening about it ("We're having trouble connecting. Your changes are saved on this device and will sync when we reconnect.").

### Empty states

An empty state is shown when there is no content yet, no results, or everything is done. Each kind needs a different message:

| Kind | User's question | Copy should |
|---|---|---|
| First use | What goes here, and how do I start? | Explain the value briefly; give one clear primary action |
| No results (search/filter) | Did I do something wrong? Is there anything? | Say no matches for the query; suggest broadening, clearing filters, or checking spelling |
| User cleared everything (inbox zero, all tasks done) | Am I done? | Confirm completion; optional next step |
| Error masquerading as empty (failed load) | Is it really empty? | Do not show "nothing here"; say it failed to load and offer retry |
| No permission | Why can't I see this? | Say access is restricted and how to request it |

Do not show the same generic "Nothing here yet" in all five cases.

### Confirmations and destructive actions

- Ask for confirmation only when the action is consequential and not easily undone. Confirming everything trains users to click through without reading. Prefer undo where possible; it is better for users and makes confirmation unnecessary.
- State specifically what will happen and what cannot be recovered: "Delete 'Q3 report'? This also deletes its 12 comments. You can't undo this."
- Name the consequence for others if relevant: "Everyone in this workspace will lose access."
- For very high-stakes actions, requiring the user to type the item's name is appropriate; say why.

### Success messages and feedback

- Confirm what happened, briefly: "Invoice sent to dana@example.com".
- Include the next useful action if there is one ("View invoice"), or an undo for reversible actions.
- Do not over-celebrate routine tasks. Match the tone to the significance of the moment and the product's voice.

### Notifications

- Lead with what changed and why it matters to this person: "Maya assigned you 'Fix login bug'" beats "You have a new notification".
- Make them actionable and specific; respect length limits on each platform; avoid urgency inflation that the content does not justify.
- Consider who might see the text (lock screens, shared displays) and avoid exposing sensitive content there.

### Onboarding and first-run

- Teach through doing, not reading. People skip tours; they learn when the copy appears at the moment they need it.
- Lead with the user's goal ("Invite your team to start collaborating"), not feature names.
- Keep each step short; let people skip and come back.
- Use progressive disclosure: explain advanced concepts when they become relevant, not on day one.

### Tooltips, help text, and descriptions

- A tooltip supplements; it never contains information required to complete a task (touch users and many keyboard users never see it).
- Settings descriptions explain the effect of the setting, especially who it affects and what happens when turned off: "Members can invite guests. When off, only admins can."
- If a concept needs more than two sentences, link to help instead of cramming.

### Loading, progress, and waiting

- Say what is happening when it takes more than a moment ("Importing 2,400 contacts…"), and how long it will take if you can estimate it honestly.
- If the user can leave and come back, say so.

### Titles and headings

- Headings tell users where they are and what they can do; make them descriptive ("Payment methods"), not decorative.
- Page titles and window titles should match the navigation label that led there (see `information-architecture`).

### Permission, consent, and privacy prompts

- Before a system permission dialog (camera, location, notifications, contacts), explain in the product's own UI why it is needed and what the user gets, at the moment it becomes relevant. Requests out of context get denied, and many platforms only let you ask once.
- Consent copy must be honest and specific: what data, for what purpose, shared with whom, and how to change the choice later. Make "no" as easy to choose and as plainly worded as "yes".
- Never disguise consent as something else, pre-select optional consent, or bury the meaningful part in a link. Beyond ethics, consent obtained that way may not be valid under privacy laws; involve legal owners for regulated wording.

### Pricing, billing, and plan limits

- State amounts, frequency, and what triggers a charge plainly: "You'll be charged $12 per member per month, starting March 3."
- When a limit is hit, say which limit, the current usage, and the ways forward (upgrade, remove items, wait for reset).
- Cancellation and downgrade flows deserve the same clarity as sign-up. Retention offers are fine; obstruction and guilt are not.

### Copy for AI-generated or automated content

When the product shows output produced by a model or an automated system:

- Make clear which content was generated or automated, in terms users understand, consistently across the product.
- Set expectations honestly: what it is good at, that it can be wrong, and how to check or correct it. Avoid both overclaiming ("always accurate") and blanket disclaimers so long nobody reads them.
- Label actions precisely: "Generate summary", "Regenerate", "Use this draft" rather than vague or anthropomorphic labels, unless the product's voice deliberately uses a persona.
- Write errors and refusals that explain what the user can do instead.

## Terminology and consistency

Build or extend a **terminology list** (glossary) for the product. For each term: the preferred word, its definition, words not to use for the same concept, and usage notes (capitalization, plural, whether it is a product-specific term).

- **One concept, one word.** Pick "workspace" or "team" or "organization", not all three for the same thing. If the codebase uses a different internal name, keep it internal.
- **One word, one concept.** Do not use "project" for both a container and a type of task.
- **Verbs for core actions**: decide pairs like add/remove, create/delete, archive/restore, and use them everywhere. "Remove" implies the thing still exists elsewhere; "delete" implies it is gone. Users notice.
- **User-facing vocabulary comes from users**: research, search logs, and support conversations show the words they use.
- **Branded feature names** should be few. Each one is a word users must learn. Pair them with descriptive text where they appear, at least at first.
- **Capitalization**: follow the product's existing convention. Mixing sentence case and title case in the same UI looks careless and slows scanning.

## Tone adaptation

Discover the voice; vary the tone by situation. A useful way to reason about tone is along a few dimensions, choosing a point for each moment within the range the voice allows:

| Situation | Adjust toward |
|---|---|
| Error, data loss risk, security, money | Direct, calm, specific, serious; no jokes |
| Destructive confirmation | Plain, explicit about consequences |
| Routine success | Brief, neutral or lightly warm per voice |
| Milestone or celebration | Warmer, if the voice allows it |
| First-run, empty states | Encouraging, oriented to value |
| Legal, compliance, consent | Plain and precise; never coy |
| Frustration (repeated failures, waiting) | Empathetic, honest, actionable |

Even in a playful product, the error that tells someone their payment failed should be plain. Even in a formal product, a success message can be friendly within the voice's range.

Avoid tone that patronizes ("Oops! Looks like you made a boo-boo"), anthropomorphizes inappropriately ("I'm so sad you're leaving"), or guilt-trips ("No thanks, I don't want to save money"). These manipulative patterns erode trust and in some jurisdictions run into consumer-protection rules.

## Writing process

1. **Understand the moment**: who is here, what they are trying to do, what they know, what is at stake, what happens next.
2. **Write the plainest version first**: the information the user needs, in order of importance. Do not decorate yet.
3. **Cut**: remove words that do not change meaning ("please note that", "in order to", "simply", "just"). "Simply" and "just" also imply the task is easy, which stings when it is not.
4. **Front-load**: move the key information to the first few words.
5. **Check terms against the glossary** and the surrounding UI.
6. **Apply the voice and tone** appropriate to the moment.
7. **Read it in context**: in the actual layout, at real sizes, with real data (long names, large numbers, zero, one), on a small screen. Copy that reads well in a document can truncate badly or wrap awkwardly in a button.
8. **Read it aloud** (or with a screen reader). Awkward phrasing, ambiguity, and missing context become obvious.
9. **Test the important ones**: show the screen to someone unfamiliar and ask what they think will happen if they press the button, or what the message means.

## Writing for accessibility and plain language

- Use common words, short sentences, and active voice. Explain unavoidable jargon.
- Do not rely on color, position, or icons alone to carry meaning ("click the green button", "see the right panel").
- Make link and button text meaningful out of context; screen-reader users often navigate lists of links or buttons.
- Provide text alternatives for meaningful icons and images; keep them concise and functional (what it does, not what it looks like).
- Error messages must be programmatically associated with their fields and announced; coordinate with developers (see `accessible-design`).
- Avoid directional or sensory instructions that do not apply to everyone ("swipe", "see below") when alternatives exist.
- Avoid idioms, sarcasm, and culturally specific references in functional copy; they confuse second-language readers and translators.

## Localization readiness

Copy that ships in several languages, or might one day, needs to be written so translation is possible without engineering changes. See `references/localization-readiness.md` for detail. The essentials:

- Never concatenate strings to build sentences ("You have " + n + " items"). Use full sentences with placeholders, and plural-aware formatting, because word order and plural rules vary by language.
- Leave room: text often expands substantially in translation (short strings expand proportionally the most). Do not design buttons that only fit the source-language word.
- Give translators context: where a string appears, what placeholders contain, character limits, and whether a word is a noun or a verb ("Archive" can be either).
- Format dates, times, numbers, currencies, and names through locale-aware formatting, not hand-written strings.
- Avoid embedding text in images.

## Naming features and objects

Names are the most durable copy in a product; they appear in navigation, docs, support, sales, and other languages.

- Prefer descriptive names ("Scheduled reports") over invented ones unless the feature is a deliberate brand asset; invented names must be learned and translated.
- Check that a new name does not collide with an existing term in the product or a common term in the domain that means something else.
- Check how the name behaves grammatically: as a noun, as a verb, in plural, with articles, and in the main target languages.
- Test candidate names with users: ask what they expect the feature to do from the name alone.
- Once shipped, renaming is expensive (docs, screenshots, support macros, user habit). Get it reasonably right before launch, and plan migrations when it must change.

## Worked example: rewriting a failing flow

*Situation*: a team-invite dialog has a low completion rate. Current copy:

> Heading: "Invite" · Field placeholder: "Email" · Button: "Submit" · On error: "Invalid input" · On success: toast "Success!"

Reasoning through it:

1. **Moment**: an admin wants teammates to get access. They may paste several addresses; they may not know what invitees can see.
2. **Heading**: "Invite people to Acme workspace" names the outcome and the scope.
3. **Field**: a visible label, "Email addresses", with a hint "Separate multiple addresses with commas". The placeholder can show an example, but not replace the label.
4. **Role choice**, if it exists, needs a one-line description of each role's effect: "Member — can view and edit projects", "Guest — can view only the projects you share".
5. **Button**: "Send invites" (plural-aware: "Send invite" for one address, if the product's string system handles it).
6. **Errors**: specific per case — "'dana@exmple' doesn't look like a complete email address", "sam@example.com is already a member", "You've reached your plan's 10-member limit. Upgrade or remove a member to invite more." Keep the valid addresses in the field.
7. **Success**: "Invites sent to 3 people. They'll get an email with a link to join." with an action to copy an invite link, if available.
8. **Voice**: if the product is terse and neutral, keep these neutral; if it is warmer, the success message may be warmer. The error messages stay plain either way.

Every change answers a question the admin had; none adds decoration.

## When working as an AI assistant

- Before writing copy for an existing product, read its string files or screenshots to infer conventions, and state the conventions you are following in one line so the user can correct you.
- Offer alternatives for important strings (names, headlines, key buttons) with a sentence on the trade-off of each, rather than a single "best" version.
- Flag copy that makes claims you cannot verify (accuracy, security, legal effect) and recommend review by the relevant owner.
- When editing strings in code, keep keys, placeholders, and plural syntax intact, and do not translate or alter strings in other locales unless asked.

## Decision guidance

**Short vs. explanatory.** Shorter is better until it stops being clear. Add words when the action is unfamiliar, consequential, or ambiguous; remove them when the action is routine and the context makes it obvious. For expert tools, terseness is often appropriate; for occasional-use services, err toward explanation.

**"You/your" vs. "my".** Most interfaces address the user as "you" ("Your projects"). "My" ("My account") is common in navigation where the user is labeling their own things. Mixing them in one context ("Change your settings in My account") is awkward; follow the product convention and be consistent within a view.

**"We" vs. the product name vs. passive.** "We couldn't connect" takes responsibility and reads as human; the product name is more formal; passive voice ("The connection could not be established") hides who is responsible and is harder to read. Use the product's convention; when there is none, active voice with "we" is usually clearest for system-caused problems.

**Error codes.** Include them if support or documentation uses them, or if users need to report issues; never as the only content.

**Exclamation marks and emoji.** Voice-dependent. Even in voices that allow them, keep them out of errors, warnings, and anything to do with money, privacy, or loss.

**Confirmation vs. undo.** Prefer undo for reversible actions (it respects the user's intent and keeps the flow fast); use confirmation for irreversible or high-impact actions, and don't use both for the same action.

## Pitfalls

- **Generic labels**: "Submit", "OK", "Yes/No", "Click here".
- **The useless error**: "An error occurred." Says nothing about cause or remedy.
- **Blame and alarm**: "Invalid input", "Illegal operation", "Fatal error" aimed at people.
- **Placeholder-as-label**: disappears when needed most.
- **Synonym drift**: different words for the same thing across screens.
- **Jargon leakage**: internal names, database field names, or engineering terms in the UI ("null", "sync token expired", "entity").
- **Cleverness in the wrong moment**: jokes in error states or during data loss.
- **Confirmation fatigue**: confirming every action until people stop reading.
- **Manipulative copy**: guilt-tripping opt-outs ("confirmshaming"), fake urgency, misleading defaults. Unethical, often counterproductive, and sometimes unlawful.
- **Writing without the design**: copy written in a spreadsheet without seeing the layout truncates, wraps, or conflicts with visual hierarchy.
- **Rewriting voice unilaterally**: imposing a new tone on one area of a product makes it inconsistent with the rest. Propose voice changes at the level they belong (a style guide), not one screen at a time.
- **Hard-coded, concatenated strings** that cannot be translated correctly.

## Quality bar and verification

For each piece of copy, check:

- [ ] It answers the user's question at that moment (what is this, what happens, what went wrong, what next).
- [ ] The key information is in the first few words.
- [ ] Buttons name the outcome and match the heading or question they respond to.
- [ ] Errors say what happened and how to fix it, without blame, and appear where the problem is.
- [ ] Terms match the glossary and the rest of the product; the same verb is used across a flow.
- [ ] Tone fits both the product's voice and the moment's stakes.
- [ ] It works in the real layout with real data: long values, zero/one/many, small screens, truncation.
- [ ] It makes sense to a screen-reader user and out of visual context; nothing depends on color or position alone.
- [ ] It is free of idioms and concatenation that would break localization; placeholders and plurals are handled properly; translators have context.
- [ ] Someone unfamiliar with the feature can predict what each action does after reading it.

For larger copy reviews, run a pass per dimension (accuracy, clarity, consistency, tone, accessibility, localization) rather than trying to catch everything at once, and keep a list of new terms to add to the glossary.

## Depth on demand

- `references/error-messages.md` — a fuller guide to error, warning, and validation messages, with worked rewrites. Read when writing or auditing error handling copy.
- `references/localization-readiness.md` — string construction, plurals, expansion, formatting, and translator context. Read when copy will be translated or the product is internationalizing.
