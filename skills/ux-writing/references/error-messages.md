# Error, Warning, and Validation Messages

Read this when writing or auditing the messages a product shows when something goes wrong or might go wrong. Error copy is where products most often lose users' trust and where small wording changes most reliably reduce support load.

## Classify before you write

Different problems need different messages. Decide which kind you have:

| Kind | Cause | What the message must do |
|---|---|---|
| Validation | Input doesn't meet a rule | Say which field, what the rule is, how to fix it |
| User-recoverable | Something the user can change (wrong password, card declined, file too large) | Say what happened and the specific remedy |
| System-recoverable | Temporary system issue (timeout, offline, rate limit) | Say it's temporary, what the product is doing (retrying, saving locally), when to try again |
| System failure | Bug or outage the user cannot fix | Apologize briefly if the voice allows, say their work is safe (if true), give a way out (retry, contact support, status page) |
| Permission | User lacks access | Say access is restricted and how to get it (who to ask) |
| Warning (pre-emptive) | Action might have unwanted consequences | Say the consequence specifically and let them proceed or back out |
| Blocking state | Account or feature unavailable (suspended, expired, quota) | Say why and the path to resolve |

## Anatomy of a helpful error message

In order of importance:

1. **What happened**, from the user's point of view, in plain words.
2. **Why**, if it helps the user fix it or understand that it's not their fault. Skip it if the reason is irrelevant or would be jargon.
3. **What to do next**: the remedy, as specific as possible, ideally with an action button or link.
4. **Reassurance about their work or data**, if true and relevant.
5. **Reference information** (error code, request ID) for support, last and visually secondary.

Not every message needs all five. A field validation message may be just the remedy ("Enter a date after today").

## Worked rewrites

| Before | Problems | After |
|---|---|---|
| "Error 500" | No meaning, no remedy | "We couldn't load your projects. This is a problem on our side. Try again in a few minutes." [Try again] |
| "Invalid email" | Blames, doesn't say what's wrong | "Enter an email address like name@example.com" |
| "Password must meet complexity requirements" | Doesn't say what they are | Show requirements before typing; on error: "Add at least one number" |
| "Upload failed" | No cause, no remedy | "This file is 30 MB. The limit is 25 MB. Try compressing it or uploading a smaller file." |
| "You do not have permission to perform this action" | Dead end | "Only workspace admins can change billing. Ask an admin (Jordan, Sam) to make this change." |
| "Session expired" | Abrupt; implies loss | "You were signed out after 30 minutes of inactivity. Sign in again to continue — your draft has been saved." |
| "Are you sure?" | Doesn't say what will happen | "Remove Ali from this project? They'll lose access to its files. You can add them back later." |
| "Oops! Something broke 🙈" | Flippant, no information | Voice permitting light tone in general, still: "Something went wrong and we couldn't send your message. Try again." |

## Placement and timing

- **Inline field validation** appears next to the field, ideally after the user leaves the field (on blur) or on submit, not on every keystroke while they are still typing. Clear the message as soon as the input is valid.
- **Form-level summaries** at the top of long forms help users see all problems at once; each entry should link or move focus to the field.
- **Toasts and transient banners** are poor for errors that need action, because they disappear and screen-reader users may miss them. Use persistent messages for anything that needs a response.
- **Modal error dialogs** interrupt; reserve them for problems that truly block progress.
- **Don't clear the form.** Preserve everything the user entered except values that cannot be kept (e.g. a card security code).

## Accessibility of errors

- Associate the message with the field programmatically so assistive technologies announce it; mark the field as invalid.
- Don't rely on red color or an icon alone; include text.
- Move focus sensibly on submit failure (to the summary or the first invalid field).
- Use a live region or equivalent for asynchronous errors so they are announced.
- Keep messages concise; long messages are tiring with a screen reader.

## Security and privacy considerations

- Avoid revealing information attackers could use: for sign-in failures, a message such as "That email and password combination doesn't match our records" avoids confirming whether an account exists. Balance this with usability per the product's security requirements; coordinate with security owners (see `secure-coding`).
- Never echo sensitive values (full card numbers, passwords, tokens) in messages.
- Do not expose stack traces, internal hostnames, or query text to end users; log them server-side with a reference ID instead.

## Warnings

- Warn only when the consequence is real and the user might not expect it. Constant warnings get ignored.
- Be specific about the consequence and its scope: "Changing the URL will break existing links to this page" rather than "This may cause problems".
- Offer the safe alternative where one exists.

## Tone in errors

Errors call for the calmest, plainest end of the product's tonal range. Even playful voices drop the jokes here. Apologize when the product is at fault and the voice supports it, once and briefly; don't apologize for the user's mistakes, and don't apologize repeatedly. Avoid exclamation marks, which read as alarm.

## Auditing existing error messages

1. Extract all error strings from the codebase or string files, along with where each is triggered.
2. Classify each by kind (table above).
3. For each, check: does it say what happened, and what to do? Is it blameless? Is it specific? Is it consistent in terms and tone with the rest?
4. Find duplicates and near-duplicates for the same condition and consolidate.
5. Find conditions with no specific message (falling through to a generic one) and prioritize those with high frequency (from logs or support data).
6. Rewrite, review with engineering for accuracy (the message must be true about the cause), and test in context.
