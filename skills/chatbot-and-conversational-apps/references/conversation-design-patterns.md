# Conversation design patterns

Read this when writing or reviewing the actual turns of a conversation: openings, questions, re-prompts, confirmations, disambiguation, errors and handoffs. Examples are illustrative — adapt wording to the product's voice and channel; do not copy them as templates.

## Openings

Goals: identify as a bot, set scope, make the first step easy.

- State capability concretely ("I can check orders, start returns and answer delivery questions") rather than generically ("How can I help?"), which invites requests the bot cannot handle.
- On rich channels, offer two to four quick replies for the most common tasks, plus free text.
- If the user arrives with context (from a specific page, after a failed payment, replying to a notification), use it: start where they are.
- Returning user mid-task: offer to resume ("Still want to finish the return for the blue jacket?").

## Asking for information

- One question per turn. Explain why if the reason is not obvious ("I need the order number to find it — it starts with #").
- Tell users where to find what you ask for.
- Accept the value in any reasonable format and normalise it in code (dates, phone numbers, order numbers with or without prefixes).
- Accept over-answering: if the user gives three slots at once, take all three.
- Accept corrections at any point ("actually, the other order") and reflect them.

## Re-prompting and repair

Escalating repair sequence for a failed or invalid answer:

1. **Rephrase with a hint**: a different wording plus an example of a valid answer.
2. **Offer options**: constrain the answer (buttons, numbered choices, yes/no).
3. **Offer an exit**: a human, a link to a form, or skipping the step if possible.

Never repeat the identical prompt twice. Never blame the user ("invalid input"). Treat "I don't know" as a real answer and offer a path forward (another way to identify the order, a human).

For voice, add silence handling: reprompt once more briefly, then offer the operator or end politely with next steps.

## Confirmation

| Risk | Pattern | Example of the idea |
|---|---|---|
| Low (searches, navigation) | Implicit — state what you're doing and continue | "Here are your orders from March." |
| Medium (saving preferences, booking that can be changed) | Summarise and proceed, with easy undo | "Booked Tuesday 3 pm — reply 'change' to pick another time." |
| High (payments, cancellations, deletions, sending messages) | Explicit yes/no with all key details | Read back amount, item, recipient; require an affirmative answer |

Interpret confirmations strictly for high-risk actions: anything other than a clear yes is not a yes.

## Disambiguation

When a request matches more than one task or entity:

- If one interpretation is much more likely and cheap to undo, proceed and state the assumption.
- Otherwise ask, offering the specific candidates ("Do you mean the order from 3 May or 12 May?").
- Limit choices to what the channel supports (about three for voice, a short list for SMS).

## Topic switches and interruptions

- Users change topic mid-task. Decide per task whether to suspend (keep slots, offer to resume later) or abandon.
- After answering a side question, offer to return ("Back to your return — which item was it?").
- Allow global commands from anywhere: help, start over, human, stop/cancel.

## Errors from systems

- Say what happened in user terms, what it means, and what to do next ("I can't reach the order system right now. You can try again in a few minutes, or I can pass this to the team.").
- Do not expose internal error messages or codes, except a short reference ID that support can use.
- Do not pretend an action succeeded when its result is unknown; say it is unconfirmed and how the user will find out.

## Handoff to a human

The user-facing message should cover: that a person is being brought in, roughly how long it will take (or the hours if offline), whether the user needs to stay in the conversation, and reassurance that they will not need to repeat themselves — only if that is true.

The agent-facing package should include: user identity and verification status, the task, collected details, what the bot already tried or told the user, sentiment signals, and the transcript.

Once a human is engaged, the bot stays quiet unless the agent hands back.

## Closings

- Confirm outcome with references (ticket number, booking time, confirmation number).
- Mention the next event the user should expect (an email, a refund timeline).
- Ask "anything else?" only if the bot can plausibly help with more; otherwise close cleanly.
- Offer feedback collection sparingly (one tap), not after every exchange.

## Reviewing transcripts

When reading real conversations, tag each failure with one cause, then fix the largest clusters:

| Tag | Typical fix |
|---|---|
| Not understood (in scope) | Add examples/training data; improve routing instructions |
| Out of scope, handled badly | Better out-of-scope response; consider adding the task |
| Wrong answer | Fix knowledge source or grounding; add a regression test |
| Unclear bot question | Rewrite the prompt; add hint or options |
| Missing capability | Product decision: add, or route to human earlier |
| Back-end failure | Reliability work; better error messaging |
| Handoff friction | Faster routing; context transfer |
| Tone mismatch | Adjust persona guidance for this context |

Add every fixed failure to the automated scenario suite so it stays fixed.
