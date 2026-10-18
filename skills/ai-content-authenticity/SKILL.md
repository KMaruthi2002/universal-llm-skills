---
name: ai-content-authenticity
description: >-
  Review text for generic, formulaic, or AI-sounding patterns — filler
  phrases, empty intensifiers, false balance, hedging stacks, stock
  metaphors, listicle and triad structure tics, vague unsupported claims, and
  tone that sounds like nobody in particular — and revise it into writing that
  is specific, substantive, accurate, and recognizably the author's own.
  Focuses on improving substance (concrete detail, real examples, actual
  positions, verified facts), not on disguising origin or evading detectors.
  Use when asked to "make this sound less like AI", "less generic", "more
  human", "remove the fluff", "this sounds robotic/corporate", review
  AI-assisted drafts before publishing, or audit content quality. Not for
  academic dishonesty, passing off work where disclosure is required, or
  impersonating real people. For general editing use
  writing-review-and-editing; for verifying claims use fact-checking.
metadata:
  category: quality
  related: writing-review-and-editing, fact-checking, copywriting, technical-writing, business-communication, prompt-engineering, seo, ux-writing
---

# AI Content Authenticity

Text reads as "AI-generated" for the same reasons bad human writing reads as corporate filler: it says little, in a voice that belongs to nobody, with structure that follows a formula rather than the content. The fix is not cosmetic. Swapping "delve" for "explore" leaves the text just as empty. The fix is to give the text something to say — specifics, evidence, a position, a reader in mind — and then to say it plainly in the author's voice.

## Scope and honest use

This skill helps people produce writing that is genuinely better: more specific, more accurate, more useful to the reader, and authentically theirs. It applies to any text, whether drafted by a person, a language model, or both.

It is for:

- Editing AI-assisted drafts into publishable work the author stands behind.
- Making marketing, documentation, reports, and posts concrete instead of generic.
- Auditing a content library for low-value, templated pages.
- Teaching writers (and prompting models) to avoid formulaic patterns.

It is not for, and should be declined or redirected when the purpose is:

- **Academic or assessment dishonesty:** making machine-written work pass as a student's own where the rules require original work or disclosure. Offer help that stays within the rules instead: feedback on the student's own draft, explanation of concepts, editing for clarity of their writing.
- **Evading required disclosure:** contexts where policy or law requires labelling AI-generated content (some publications, platforms, advertising, legal filings, journalism).
- **Deceptive impersonation:** writing to pass as a specific real person, fake reviews or testimonials, astroturfing, or fabricated "personal experience" presented as real.
- **Defeating detectors as the goal.** AI-text detectors are unreliable in both directions (they flag human writers, particularly non-native English speakers, and miss machine text), so optimizing against them is neither a sound quality goal nor an honest one. Improve the writing; do not game classifiers.

When the purpose is unclear and the context suggests one of these, ask. When it is ordinary (a professional polishing their own AI-assisted draft), proceed without lecturing.

Also out of scope: deciding whether a given text *was* AI-written. No reliable method exists for that from text alone; patterns in this skill indicate weak writing, not provenance. Do not accuse anyone of using AI on the basis of style.

## Core principles

**1. Substance first, style second.** Most generic-sounding text has a content problem: no specific claim, no example, no number, no stance, no new information. Style fixes on contentless text produce better-sounding emptiness. Always ask "what does this sentence tell the reader that they did not know?" before polishing how it says it.

**2. Specific beats general.** "Our tool saves teams time" could describe any product. "Support teams using the tool closed tickets in a median of 4 hours instead of 11, in a three-month pilot with 40 agents" could describe only one. Specifics are evidence of knowledge, and readers trust them because they are falsifiable.

**3. The author's voice, not a different generic voice.** Removing one set of tics and installing another ("punchy" fragments, forced casualness, manufactured anecdotes) is not authenticity. Find out how the author actually writes and talks, and edit toward that.

**4. Structure should follow content.** Three bullet points because the content has three parts is good; three bullet points because lists of three feel complete is a tic. Headings, bold, lists, and summaries should exist only when they help the reader navigate or remember.

**5. Never invent to sound authentic.** Adding a fake personal anecdote, made-up statistic, invented customer quote, or fictional expert makes text worse, not more human, and can be deceptive or defamatory. Specifics must be real: supplied by the author, drawn from sources, or clearly marked as hypothetical examples. Where specifics are missing, ask for them or leave a visible placeholder.

**6. Accuracy is part of authenticity.** Generated drafts often contain confident errors and fabricated citations. A text that sounds human and is wrong has failed. Hand claims to `fact-checking`.

## Patterns to look for

These patterns are common in model output and in templated human writing. One instance is rarely a problem; density is. Treat the list as a set of questions to ask, not words to ban mechanically (a banned-word list just produces new tics).

### Filler and throat-clearing

- Openers that announce rather than say: "In today's fast-paced world", "In the ever-evolving landscape of", "When it comes to", "It's important to note that", "It's worth mentioning".
- Restating the question before answering it.
- Closers that summarize what was just said or wish the reader well: "In conclusion", "Ultimately", "By following these tips, you'll be well on your way", "I hope this helps".
- Meta-commentary: "Let's dive in", "Let's explore", "Here's the thing".

**Fix:** delete, then start with the first sentence that contains information. Endings should end: on the last useful point, the action to take, or an implication the reader had not considered.

### Empty intensifiers and inflated vocabulary

- Adjectives that claim importance without showing it: crucial, vital, pivotal, essential, robust, seamless, cutting-edge, game-changing, revolutionary, powerful, comprehensive, transformative.
- Verbs and nouns of grandeur: leverage, harness, unlock, empower, elevate, foster, navigate (the landscape), delve, embark, tapestry, realm, journey, testament.
- Stacked modifiers: "a truly comprehensive and robust solution".

**Fix:** replace the claim of importance with the reason for it. Not "a crucial step" but what goes wrong if the step is skipped. Not "robust" but what load or failure it withstands. If no reason exists, cut the adjective.

### False balance and reflexive hedging

- "While X has benefits, it also has drawbacks" with no assessment of which matters more.
- "There are many perspectives on this" as a substitute for presenting them or taking one.
- Equal space to unequal evidence.
- Hedge stacks: "may potentially help to some extent".
- Universal disclaimers appended to everything ("it's always best to consult a professional") where they add nothing.

**Fix:** decide what the text actually claims, then state it with the confidence the evidence supports. Present real trade-offs concretely ("faster to set up, but costs roughly twice as much per user above about 50 seats"). Keep hedges where uncertainty is real and specific ("the trial was small, 60 participants"), and keep safety disclaimers where they matter, stated specifically.

### Structural tics

- Everything in bullet lists, even narrative or argument that needs connected sentences.
- Lists and adjective strings in threes by reflex.
- Headings on every two paragraphs; bold on random phrases.
- Each paragraph the same length and shape: topic sentence, three supports, wrap-up.
- The "not X, but Y" contrast frame ("It's not just a tool, it's a partner") used repeatedly.
- Rhetorical questions as transitions ("So what does this mean for you?").
- Colon-and-reveal constructions and em-dash asides used as a rhythm habit.
- A summary at the end of every section.
- Symmetric "pros and cons" or "on one hand, on the other" frames whatever the content.

**Fix:** let the content's shape determine the form. Arguments want paragraphs with real logical connections ("because", "so", "but this fails when"). Procedures want numbered steps. Comparisons want tables. Vary sentence length because the thought varies, not to a pattern.

### Vague claims and missing specifics

- Unattributed authority: "studies show", "experts agree", "research suggests" with no study or expert.
- Unquantified claims: "significantly improves", "many users", "a growing number".
- Abstract benefits: "streamline your workflow", "drive results", "enhance efficiency".
- Generic examples: "for example, a business might want to improve its operations".
- Content that would be equally true of any company, product, city, or person.

**Fix:** for each, ask what the specific version is: which study, how much, which users, what workflow step, what result, which business. Get it from the author or sources. If nobody knows, the claim should be softened or removed, not decorated.

### Voice and tone problems

- Relentless positivity and enthusiasm regardless of subject.
- Customer-service register in contexts that need expertise, or vice versa.
- Second-person cheerleading ("You've got this!").
- Avoiding any opinion, humor, or first person where the genre welcomes them.
- Sycophantic framing ("Great question!").
- Uniform polish with no rough edges, no idiosyncratic word choices, no references to the author's own experience or context.

**Fix:** establish the author's actual voice and the genre's norms, then edit toward them. This is where the author must contribute: their opinions, their experience, the example they would actually use.

### Content-level emptiness

- Answering a generic version of the question rather than the reader's actual situation.
- Covering everything at the same shallow depth, rather than going deep on what matters.
- Definitions of terms the audience already knows.
- Advice that is true but useless because it is obvious ("communicate clearly with your team").

**Fix:** identify the reader's real problem and the two or three points an expert would actually make about it, including the non-obvious ones. Cut the rest.

## Process

### 1. Understand the piece and the author

- What is the piece for, who reads it, where will it appear?
- Who is the author, and how do they write? Ask for samples of their own writing, or look for the passages in the draft that sound most like a person. A style guide or brand voice document, if one exists, governs.
- What does the author know that the draft does not contain? Real numbers, customer stories (with permission), opinions, failures, local details. This is usually the biggest source of improvement.
- Check the honest-use boundaries above.

### 2. Diagnose: substance pass

Read through and, for each paragraph, note: what is the specific claim? Is there evidence or an example? Would the paragraph be true of any similar topic? Is there a position? Mark paragraphs as substantive, thin (has a point but no support), or empty (no point).

Often the honest finding is that the draft has one or two real ideas buried in a lot of filler. Say so; that is useful.

### 3. Diagnose: pattern pass

Mark instances of the patterns above. Look at density and clustering rather than single words. A useful quick read: highlight every sentence that could be deleted without the reader losing information. If more than a quarter of sentences are highlighted, the draft needs restructuring, not polishing.

### 4. Gather specifics

Before rewriting, collect what the text needs: ask the author targeted questions ("What was the actual result of the pilot?", "Which customer type benefits most, and how do you know?", "What do you disagree with in the usual advice on this?"), or find sources. Where a specific cannot be obtained, leave a clear placeholder such as [number needed] rather than inventing.

### 5. Revise

- Restructure first: put the real point first (for most nonfiction), cut empty sections, merge thin ones, expand the substantive ones with the specifics gathered.
- Then line-edit: remove filler, replace inflated words with plain ones or with the reason behind them, collapse hedge stacks, convert reflexive lists into connected prose where the content is an argument.
- Then voice: adjust toward the author's samples. Keep their idiosyncrasies; do not add new ones they would not use.
- Keep meaning stable: do not strengthen claims beyond the evidence while removing hedges.

The general editing process in `writing-review-and-editing` applies throughout; this skill adds the diagnosis of generic patterns and the emphasis on substance.

### 6. Verify facts

Generated drafts may include invented statistics, quotes, studies, and references. Check every one (`fact-checking`). Remove or correct anything unverified.

### 7. Explain the changes

Tell the author what you changed and why, in terms they can apply next time: "Most of the generic feel came from three things: the opening paragraph announcing the topic, unattributed 'studies show' claims, and every section ending in a summary. I cut the opening, replaced two claims with the figures from your pilot, and removed the summaries." If you used placeholders, list them.

## Worked example

Draft:

> In today's rapidly evolving digital landscape, cybersecurity has become more crucial than ever. Small businesses, in particular, face a myriad of challenges when it comes to protecting their sensitive data. By leveraging robust security practices, organizations can unlock peace of mind and foster a culture of resilience. In this article, we'll delve into the key strategies that can help you navigate this complex terrain.

Diagnosis: four sentences, no information. Filler opener, empty intensifiers ("crucial", "robust"), grand verbs ("leverage", "unlock", "foster", "delve", "navigate"), an abstract benefit ("peace of mind"), and a meta closing sentence. The only real idea: small businesses need security practices. Nothing here is specific to the author, their readers, or this year.

Questions for the author: Who exactly are the readers (a five-person accounting firm? a shop with a website?). What is the most common way such businesses actually get compromised in your experience? What one thing would you tell them to do first?

Suppose the author answers: readers are owners of firms under 20 people; most incidents the author's company handles start with a stolen email password; the first step is turning on multi-factor authentication for email.

Revision:

> Most of the break-ins we clean up at small firms start the same way: someone's email password is guessed or phished, and the attacker uses the mailbox to send fake invoices to clients. If you run a business with fewer than 20 people and do only one thing after reading this, turn on two-step sign-in for every email account. It takes about ten minutes per person.

Every sentence now carries information, comes from the author's real experience, and gives the reader something to do. The voice is plain and direct because the author said they talk to clients that way. Note that the revision depends on facts only the author could supply; without them, the right output would have been the questions, not an invented anecdote.

### A second example: technical explanation

Draft:

> Caching is a powerful technique that can significantly improve the performance of your application. By storing frequently accessed data, caching reduces the load on your database and enhances the user experience. However, it's important to note that caching also comes with its own set of challenges, such as cache invalidation. Overall, when implemented correctly, caching can be a game-changer.

Diagnosis: accurate but generic to the point of uselessness for anyone who already knows what caching is. "Significantly", "powerful", "game-changer" signal importance without showing it; "comes with its own set of challenges" names a problem without explaining it; "when implemented correctly" is a non-statement.

If the piece is for developers deciding whether to cache a specific endpoint, the substance they need is: when caching helps (read-heavy, tolerant of staleness), what it costs (staleness, memory, complexity), and the decision rule. A revision built on the author's actual case:

> Our product-listing endpoint gets about 200 reads for every write, and a listing that is up to a minute old is acceptable to the business. That makes it a good candidate for a cache with a 60-second expiry: database reads for listings dropped by about 95% in staging. The cost is that a price change can take up to a minute to appear, so we bypass the cache on the checkout page, where prices must be current.

The revision states the conditions, the result, the trade-off, and the mitigation, with numbers the author supplied. It contains no adjective of importance because the numbers make the importance obvious.

## Genre notes

- **Marketing and product copy:** the generic version praises; the specific version shows what changes for the customer, with proof (numbers, named customers with permission, concrete features). See `copywriting`.
- **SEO content:** pages written to cover a keyword with no original information are the clearest case of templated emptiness, and search engines increasingly reward original expertise and first-hand experience over coverage. Add what only this author knows: data, testing, real examples, opinions. See `seo`.
- **Business communication:** generic emails bury the request in pleasantries. Lead with the ask, give the context needed to act, end. See `business-communication`.
- **Technical documentation:** formulaic introductions and "powerful features" language waste developers' time. Get to the task, the code, and the edge cases. See `technical-writing`.
- **Personal writing** (cover letters, bios, personal statements): generic phrasing hides exactly what readers want, the person. Here the specifics must come from the person; never invent experiences. For admissions and similar assessed writing, follow the institution's rules on assistance.
- **Interface text:** short, plain, consistent labels and messages; see `ux-writing`.

## Auditing content at scale

For a library of pages (a blog, a help center, product pages), review a sample rather than everything, then generalize:

- Pick pages across templates, authors, ages, and traffic levels.
- For each, rate substance (does it contain information specific to this organization or topic, and is it accurate?) and pattern density.
- Look for templated families: pages that differ only by a swapped keyword or city name. These are usually the lowest-value content and the best candidates to merge, rewrite with real local or specific information, or remove.
- Recommend priorities by traffic and business value: improve high-traffic thin pages first, consolidate duplicates, retire pages with no unique value.
- Propose prevention: briefs that require specifics and sources before drafting, a review checklist based on the patterns above, and a fact-check step for any AI-assisted content.

## Prompting to avoid generic output

When text will be generated by a model (yours or another), prevention is cheaper than repair. Effective inputs (see `prompt-engineering` for more):

- Provide the specifics: data, examples, quotes, the author's opinions, notes from interviews, the audience description.
- Provide samples of the target voice and say what is characteristic about them.
- Ask for the content's natural form ("write connected paragraphs; use a list only for the steps").
- Ask the model to flag where it lacks specifics instead of filling the gap ("mark [needs example] rather than inventing one").
- Specify what to omit: no introduction restating the topic, no concluding summary, no disclaimers unless relevant.
- Review the output with the diagnostic passes above anyway; instructions reduce patterns but rarely remove them.

## When you are the one generating the text

If you are a language model writing for a user, apply this skill to your own drafts before returning them:

- Start with the answer or the first substantive point, not a restatement of the request.
- Use the specifics the user gave you; if you need more to be useful, ask, or mark the gap, instead of filling it with generalities.
- Match the user's register and the destination's genre, not a default assistant voice.
- Choose form by content: a two-sentence answer does not need headings; a comparison may need a table.
- Do not end with a summary of what you just said or an offer of generic further help unless there is a specific next step worth offering.
- Do not fabricate citations, quotes, statistics, or experiences. If you are unsure of a fact, say so.
- Reread once looking only for the patterns above, and cut what carries no information.

## Quick diagnostic table

| You notice | Ask | Usual fix |
|---|---|---|
| The first sentence could open any article on the topic | Where does the information start? | Delete up to there |
| An adjective of importance | Why does it matter, concretely? | Replace with the reason or cut |
| "Studies show" / "experts say" | Which, and do they actually say it? | Cite, or soften to the author's own claim, or cut |
| Three parallel items | Are there really three? | Use the real number |
| "On the other hand" with no verdict | Which side does the evidence favor? | State the assessment |
| A paragraph true of any company | What is specific to this one? | Get the specific from the author |
| A summary closing a short section | Does the reader need reminding? | Cut |
| Uniform, frictionless enthusiasm | Would the author say this aloud? | Edit toward the author's samples |

## Decision guidance

**Rewrite or edit?** Edit when the draft has real substance and the problem is surface patterns. Rewrite (with the author's input) when most paragraphs are empty: editing empty text produces shorter empty text.

**Keep or cut a "tic" word?** Keep it when it is the precise word for the meaning ("robust statistics" is a technical term; "navigate" is right for actual navigation) or when it is genuinely the author's habit and the audience does not mind. Cut it when it signals importance without demonstrating it.

**Lists or prose?** Lists for items that are parallel, separable, and scannable (steps, options, requirements). Prose for reasoning, causation, narrative, and anything where the connections between points matter.

**When the author cannot supply specifics.** Say so. A shorter, honest piece with fewer claims is better than a longer one padded with generalities. Suggest what research or data would strengthen it.

## Discovering context

- Ask for writing samples by the author, a brand voice guide, or published pieces from the same venue; analyze their sentence length, vocabulary, formality, use of first person, humor, and structure.
- Check the venue's policy on AI assistance and disclosure, and follow it.
- Identify the audience's expertise, so you know which explanations are padding and which are needed.
- Look at the strongest competing or peer content on the topic: the bar for "specific" is whatever the best existing piece offers.

## Pitfalls

- **Synonym swapping.** Replacing flagged words with near-synonyms while leaving the empty content.
- **Ban lists as style.** Mechanically avoiding a list of words produces stilted text and new tics.
- **Fake humanizing.** Adding invented anecdotes, typos, slang, or forced informality. This is deceptive and reads as fake anyway.
- **Overcorrecting into choppiness.** Removing all transitions and hedges, leaving abrupt, overconfident prose.
- **Stripping legitimate structure.** Technical docs and reference material benefit from headings and lists; do not convert a good reference page into an essay.
- **Flattening the author's voice** into the editor's preferences.
- **Ignoring accuracy** because the text now sounds convincing.
- **Accusing people.** Pattern density is not proof of AI use; many people write this way, and detectors are unreliable.
- **Helping with deception** because the request was framed as style editing. Check the purpose when context suggests misuse.

## Quality bar and verification

- [ ] Every paragraph makes a specific point a reader could not have predicted from the topic alone.
- [ ] Claims have evidence or attribution; vague authority ("studies show") is replaced or removed.
- [ ] No invented facts, anecdotes, quotes, or statistics; placeholders mark missing specifics.
- [ ] Filler openers, empty closers, and summary-of-the-summary sections are gone.
- [ ] Intensifiers either earn their place with a reason or are cut.
- [ ] Structure (lists, headings, bold) follows the content's shape.
- [ ] Hedges match real uncertainty; trade-offs are concrete and assessed.
- [ ] The voice matches the author's samples or the stated guide, not a new generic voice.
- [ ] Facts were checked or handed to fact-checking.
- [ ] The use is honest: no disclosure requirements evaded, no impersonation, no academic dishonesty.
- [ ] Read the revision aloud: it should sound like a specific person who knows the subject talking to a specific reader.
