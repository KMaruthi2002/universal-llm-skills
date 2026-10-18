# Testing Prototypes

Read this before putting a prototype in front of users. It covers what is specific to testing unfinished artifacts; the broader method (recruiting, metrics, severity, reporting) is in `usability-evaluation`, and interview craft is in `ux-research`.

## Prepare the prototype for testing

- **Walk every task path yourself** on the device and setup participants will use, at least twice. Broken links and missing hotspots are the commonest way to waste a session.
- **Make start states repeatable**: a reset link, a fresh copy, or seed data, so each participant starts identically.
- **Make dead ends graceful**: a neutral screen ("This part isn't built for today's session") rather than nothing happening, which participants interpret as their own failure.
- **Use realistic data** matched to the participant where possible (their kind of company, their kind of items); generic data makes tasks feel artificial.
- **Check hotspot hints**: many prototyping tools flash clickable areas when users click elsewhere; decide whether to disable it, since it guides participants.
- **Fake typing carefully**: if a task requires text entry and the tool cannot accept it, use a coded prototype or accept that you are not testing input.
- **Test on the target device and size**: a desktop prototype on a large monitor tests a different design than the same one on a laptop.
- **Version and freeze**: no edits during a round, unless a blocking bug makes sessions useless; log any change.

## Write tasks for prototypes

- Base tasks on the question the prototype was built to answer.
- Write scenarios with a goal and a reason, not instructions: "You've just been told your team's budget was cut. Find out which subscriptions you could cancel." not "Click Billing, then Subscriptions."
- Avoid words that appear on the target button or link, or you test word matching.
- Order tasks so early ones don't teach the answers to later ones, or randomize when possible.
- Define success criteria for each task before testing.
- Keep the set achievable in the session time with buffer for discussion; typically fewer tasks than you want.

## Running the session

- Frame it: "This is an early design. Some parts aren't built. We're testing the design, not you. Please think aloud."
- Let participants struggle a little before helping; the struggle is the data. Agree beforehand on when to intervene (e.g. after a set time stuck, or when stuck on a part not under test).
- When they hit a deliberate gap, acknowledge it neutrally and ask what they expected to happen there. Expectations at gaps are useful findings.
- Ask about expectations before actions: "What do you think will happen if you click that?" then let them click.
- Resist explaining the design. If you need to explain, the design needs work.
- For comparative tests of several alternatives, vary the order across participants and ask for comparisons only after they have used each.

## Distinguishing design problems from prototype problems

Some failures are artifacts of the prototype, not the design:

| Symptom | Likely prototype artifact if… | Likely design issue if… |
|---|---|---|
| Participant clicks something non-interactive | It would be interactive in the real product | They expected it to do something the design doesn't offer |
| Confusion about data | Data is generic or inconsistent | Real data would cause the same confusion |
| Slow or awkward input | The tool faked input poorly | The form itself asks too much or is unclear |
| Lost in navigation | Prototype lacks global nav that the product has | The structure itself is unclear |

Note which category each issue falls into in your notes. Don't discard prototype artifacts entirely: they may indicate expectations (e.g. people expect a list item to be clickable).

## From observations to iterations

- Debrief after each session; after the round, cluster issues by task and by screen.
- Rate severity (impact × frequency × persistence; see `usability-evaluation`).
- Fix the high-severity issues and retest them in the next round with new participants; don't retest what passed unless it changed.
- Track issues across rounds so you can see whether fixes worked or introduced new problems.
- Decide when the prototype has done its job: the original question is answered with enough confidence for the decision. Then raise fidelity, move to build, or drop the idea.

## Ethics

The standard research ethics apply (informed consent, recording consent, anonymization, fair pay; see `ux-research`). Prototype-specific points:

- If a prototype simulates functionality (Wizard-of-Oz, fake data), say so at the end if not at the start.
- Do not let participants enter real personal or financial data into a prototype; provide test values.
- Do not leave prototypes containing real customer data on public links.
