---
name: test-driven-development
description: >-
  Write code test-first using the red-green-refactor cycle: pick the next
  smallest test, watch it fail for the right reason, make it pass with the
  simplest change, then refactor with the tests as a safety net. Covers
  choosing the next test, fake-it versus obvious implementation versus
  triangulation, outside-in versus inside-out, characterization tests for
  untested legacy code, test-first bug fixing, and when TDD helps or doesn't.
  Use when the user asks for TDD or test-first development, when building
  well-specified logic, when fixing a bug with a failing test first, or when
  adding tests around legacy code before changing it. For deciding overall
  test levels and suite design use testing-strategy.
metadata:
  category: development
  related: testing-strategy, refactoring, debugging, legacy-modernization, software-architecture, api-design, code-review
---

# Test-Driven Development

TDD is a design and feedback technique that happens to produce tests. You state, in executable form, the next small thing the code should do; you watch the statement fail; you make it true as simply as possible; you then clean up. The rhythm keeps you working on one thing at a time, guarantees every line of production code was demanded by a test, and gives you a refactoring safety net that grows with the code.

## Scope

Covers: the red/green/refactor loop, choosing and ordering tests, implementation strategies within the loop, outside-in and inside-out styles, characterization tests for legacy code, test-first bug fixing, and judging when TDD is a good fit.

Neighbours:

- Which kinds and levels of test a system needs overall, test doubles, flakiness, coverage → `testing-strategy`.
- The refactoring step in depth, code smells and named refactorings → `refactoring`.
- Large-scale work on untested legacy systems → `legacy-modernization`.
- Root-causing a bug before writing the failing test → `debugging`.

## Core principles

1. **Never write production code without a failing test that demands it.** This is what makes the tests a complete specification of what the code does and guarantees each test can fail. The rule is strict inside the loop so that it can be relaxed knowingly outside it (spikes, see below).

2. **Watch the test fail, and fail for the right reason.** A test that passes immediately either tests nothing new or tests nothing at all. A test that fails for the wrong reason (import error, typo, missing fixture) hasn't yet told you anything about behaviour. Read the failure message every time — it is also how you check that the message will be useful to the next person.

3. **Take steps as small as your confidence requires.** When the path is clear, take bigger steps. When surprised (an unexpected failure, a test that passes too early), shrink the steps. Step size is a dial, not a dogma.

4. **Green first, clean second, never both at once.** Getting to green with ugly code and then refactoring under green tests is faster and safer than designing the clean version while also making the test pass. Mixing them means that when something breaks you don't know whether it was the new behaviour or the restructuring.

5. **Refactor is not optional.** Skipping the third step yields code that works but accretes duplication and awkward structure test by test. Most of TDD's design benefit comes from the refactor step, informed by the pain of writing the tests.

6. **Tests specify behaviour through the public interface.** Tests written against internals make refactoring painful, which defeats the purpose of having them. If something is hard to test through the interface, that is design feedback.

7. **Test pain is design feedback.** Difficulty writing a test — massive setup, many mocks, hidden dependencies, needing to reach into private state — reflects coupling in the design. Respond by changing the design (inject the dependency, split the class, separate the pure logic from the I/O), not by building heroic test scaffolding.

## The loop

### Red: write one failing test

- Write the test you wish you could write, using the API you wish existed. This is where interface design happens: names, argument order, return types, error behaviour. Calling code is written before called code, so the API is shaped by use.
- Make it **compile/load** with the minimum stubs needed (empty function, class with no behaviour) so the failure is an assertion failure, not a syntax or import error.
- Run it. Confirm it fails, and that the failure message says what you expect ("expected 3, got 0" — not "NameError").

### Green: make it pass with the simplest change

Three strategies, from most cautious to most direct:

| Strategy | What you do | Use when |
|---|---|---|
| **Fake it** | Return a constant or hard-coded value that makes this test pass | You're unsure of the general solution; you want to get to green immediately and let more tests force generality |
| **Triangulate** | Add a second example that the fake can't satisfy, forcing the general rule | Fake-it is in place and the generalisation is not yet obvious |
| **Obvious implementation** | Write the real code directly | The solution is clear and small; if a surprise failure appears, drop back to fake-it |

The simplest change means simplest to *make pass*, not most elegant. Duplication and hard-coding are permitted here — the refactor step removes them.

Run the full fast test set, not only the new test, to confirm nothing else broke.

### Refactor: improve the design with tests green

- Remove duplication — including duplication between test and code (a hard-coded constant that also appears in the test is a sign generalisation is due).
- Improve names now that you understand the concept better.
- Extract functions, introduce types for primitive-obsessed values, simplify conditionals.
- Refactor the **tests** too: extract builders for repeated setup, clarify names. But keep tests readable on their own; don't abstract them into riddles.
- Run tests after each small refactoring. If they go red, undo the last step rather than debugging forward.

Then pick the next test.

### Cycle length

A loop typically takes from under a minute to a few minutes. If you have been red for more than ~10 minutes, the step was too big: revert to the last green state (version control or undo) and take a smaller step. Reverting feels wasteful but is usually faster than debugging a large, half-working change.

## Choosing the next test

The order of tests shapes the design and the pace. Keep a **test list** — a running list of behaviours, edge cases, and questions you have thought of but not yet tested. Add to it whenever something occurs to you, so you can keep focus on the current test without losing ideas.

Heuristics for picking from the list:

- **Start with the degenerate case** that forces the API to exist: empty input, zero, no items. It establishes signatures without demanding logic.
- **Then the simplest interesting case**: one item, the most common happy path.
- **Grow by one dimension at a time**: one → two → many; one rule → two rules; valid → invalid.
- **Pick a test you're confident you can make pass**, and that teaches you something. If none on the list qualifies, find a smaller one.
- **Leave the hardest, most general cases for when the code has grown towards them.** Jumping to them early forces you to write the whole algorithm in one step.
- **Error and boundary cases** come once the main shape exists: invalid input, limits, exceptions, overflows.
- **If two tests are equally plausible, pick the one that drives the more uncertain part of the design** — reducing risk early.

A useful ordering mnemonic for collections and algorithms is **Zero, One, Many** (and then boundaries, interfaces, exceptions).

When a test passes immediately without code changes, ask why: either the behaviour was already implied (fine — keep it as documentation if it adds clarity, or delete it), or the test is wrong. Make it fail by temporarily breaking the code to confirm it is real.

## A worked example (illustrative)

Building a function that formats a list of names for display: `[]` → `""`, `["Ann"]` → `"Ann"`, `["Ann","Bo"]` → `"Ann and Bo"`, three or more → `"Ann, Bo and Cy"`.

Test list: empty; one; two; three; many; (later) names containing commas? trimming? locale-specific conjunctions?

1. **Red:** `format_names([]) == ""`. Fails: function doesn't exist. Add an empty function → fails with "None != ''". Good failure.
   **Green:** `return ""`. **Refactor:** nothing yet.
2. **Red:** `format_names(["Ann"]) == "Ann"` fails ("'' != 'Ann'").
   **Green:** `return names[0] if names else ""`.
3. **Red:** two names → "Ann and Bo". **Green:** add a branch for length 2.
4. **Red:** three names → "Ann, Bo and Cy". **Green:** for three or more, `", ".join(names[:-1]) + " and " + names[-1]`.
   **Refactor:** the length-2 branch is a special case of the general rule (joining one element with ", " is just that element). Remove it; all tests stay green. Now the code is two cases: empty-or-one, and general.
5. The questions on the list (commas inside names, localisation) go to the user rather than being silently decided — TDD surfaces requirement questions early, which is one of its benefits.

The point is not that this code needed TDD, but the shape: degenerate first, grow by one, let the refactor step find the general rule.

## Situations inside the loop and what to do

| Situation | Likely meaning | Response |
|---|---|---|
| New test passes immediately | Behaviour already exists, or the test asserts the wrong thing | Break the code temporarily to prove the test can fail; keep it only if it documents something not already covered |
| Can't get the test to fail for the right reason | Setup is wrong or the API doesn't exist yet | Add minimal stubs until the failure is an assertion about behaviour |
| Red for more than ~10 minutes | Step too large | Revert to last green; write a smaller test (or fake it) |
| Making one test pass breaks others | Hidden coupling, or the new rule conflicts with an earlier one | Revert; check whether the requirements conflict (ask the user) or the design needs a refactor first, with tests green |
| Setup is growing with every test | The unit has too many dependencies | Refactor: extract the logic into a smaller unit with fewer collaborators; introduce builders |
| You need to mock five things | Design is coupled; or you're testing at the wrong level | Separate pure decision logic from coordination; test logic directly, coordination at integration level |
| You want to test a private method | It's a separate concept | Extract it into its own unit with a public interface, or test it through the public behaviour |
| Test needs the real time / random / network | Hidden nondeterministic dependency | Inject a clock, seed, or adapter; keep real I/O at the edges |
| The general solution is obvious but you've been faking | You're being over-cautious | Write the obvious implementation; drop back if surprised |
| You discover a new requirement mid-loop | Normal | Add it to the test list; finish the current cycle first |
| You discover the requirement is ambiguous | Normal, and valuable | Ask the user; don't silently choose and encode a guess as a test |

## Growing the implementation: prefer simple transformations

When going from red to green, prefer the transformations that change the code least. Roughly in order of simplicity:

1. nothing → return a constant,
2. constant → variable or argument,
3. add an unconditional statement,
4. split the flow with a conditional,
5. a conditional → a loop or recursion,
6. a value → a collection,
7. a statement → a function call that encapsulates it,
8. assignment and mutation of state.

The idea (sometimes called the transformation priority premise) is a heuristic, not a law: if passing the next test requires a "complex" transformation when a simpler one would do, a different next test may lead to a cleaner algorithm. When you find yourself writing a loop before any conditional exists, consider whether you skipped a test.

## TDD with dependencies: ports and adapters

Business logic test-driven in isolation needs its collaborators to be replaceable. A structure that makes TDD easy:

- **Core**: pure or mostly-pure domain logic. Test-driven with real objects, no mocks, millisecond tests.
- **Ports**: interfaces the core needs (a repository, a clock, a payment gateway, a notifier), defined in the core's own vocabulary.
- **Adapters**: implementations of ports over real technology (SQL, HTTP clients, queues). Test-driven or tested with integration tests against the real technology.
- **Fakes** of the ports for core tests: an in-memory repository, a fixed clock.

You don't have to adopt a named architecture to benefit; just introducing a seam (constructor parameter, function argument) for each external dependency as tests demand it produces the same effect. Avoid creating interfaces with a single implementation *only* for mocking unless that dependency is genuinely external or slow.

## TDD across paradigms and kinds of code

- **Functional code**: TDD is natural — functions of inputs to outputs. Property-based tests (see `testing-strategy`) complement example-driven TDD well: test-drive with examples, then generalise with a property once the shape is clear.
- **Object-oriented code**: tests drive messages between objects. Classicist TDD asserts on resulting state; mockist TDD asserts on messages sent to collaborators. Use the latter only where the message is the important outcome (e.g. "emits OrderShipped").
- **HTTP APIs**: write the request/response test first using an in-process test client; drive the handler, then push logic into the core as it grows.
- **Asynchronous code**: drive with tests that await completion explicitly; use fake timers/schedulers to control time. Never use sleeps in TDD loops — they make the loop slow and the tests flaky.
- **Database access**: test-drive queries against a real database engine of the same kind used in production, using transactions or per-test schemas for isolation. The loop is slower; keep these tests focused and few.
- **Command-line tools**: drive the core parsing and logic with unit tests; add a few tests that run the CLI end to end with arguments, capturing stdout/stderr and exit codes (see `cli-development`).
- **Frontend components**: drive behaviour (what happens when the user clicks, types, submits) through rendered-component tests that query by visible text and roles; leave visual layout to human review.

## A second worked example: outside-in (illustrative)

Feature: "`POST /orders/{id}/cancel` cancels an order that hasn't shipped and refunds the payment."

1. **Outer test (red):** with a test client, create an unshipped paid order, call the endpoint, expect 200, order status `CANCELLED`, and a refund recorded via a fake payment gateway. Fails: route doesn't exist.
2. **Inner loop — domain:** test-drive `Order.cancel()`: unshipped order becomes cancelled; shipped order raises a domain error; already-cancelled order is idempotent (or errors — ask the user which). Pure, fast tests with real objects.
3. **Inner loop — application service:** test-drive `CancelOrder` with an in-memory order repository and a fake payment gateway: loads the order, cancels it, requests a refund, saves. Here the fake gateway's recorded call *is* the observable outcome.
4. **Inner loop — handler:** map domain error for shipped orders to the project's error response convention (e.g. 409), not-found to 404.
5. **Outer test goes green.** Add outer tests for the shipped-order and not-found cases only if lower tests don't already make you confident the wiring maps them.
6. **Adapter:** the real payment gateway adapter gets its own integration test against the provider's sandbox, run in the slower tier.
7. **Refactor** across the slice with everything green.

The outer test kept the work focused on the user-visible goal; the inner loops gave precise, fast feedback on each piece.

## Outside-in vs inside-out

| | Inside-out (classicist) | Outside-in (London / mockist / double-loop) |
|---|---|---|
| Start from | Core domain objects and logic | An acceptance test of user-visible behaviour |
| Collaborators | Built first, then composed; real objects in tests | Discovered from the outside; mocked until implemented |
| Strengths | Tests use real objects, survive refactoring well; good for algorithmic and domain-heavy code | Builds only what the feature needs; interfaces are shaped by callers; clear progress toward the user goal |
| Risks | Can build components that don't fit together or aren't needed | Heavy mocking couples tests to collaboration design; refactoring across boundaries breaks many tests |

**Double-loop TDD** combines them: write a failing acceptance/integration test for the feature (outer loop), then use inner unit-level red/green/refactor loops to build the pieces until the outer test passes. The outer test stays red for a while; that's expected. It prevents gold-plating and verifies the pieces actually integrate.

A pragmatic default: outer acceptance test for the feature, inside-out with real collaborators for the domain logic, mocks only at boundaries you own that front external systems (see `testing-strategy` on test doubles).

## Test-first bug fixing

Every bug fix is a natural TDD loop:

1. Root-cause the bug (see `debugging`).
2. Write a test that reproduces it at the lowest level that can express it. Run it; it must fail, and the failure must be the bug (not a setup error).
3. Fix the cause. The test goes green.
4. Refactor if the fix revealed a design weakness.
5. Optionally also add a test at the level where the bug was reported if the low-level test wouldn't catch reintroduction through a different path.

This is the most universally applicable form of TDD; even teams that don't practise TDD broadly benefit from it.

## Characterization tests for legacy code

When code has no tests and you need to change it, you can't test-drive the existing behaviour — it already exists. Instead, **pin down what it currently does**, right or wrong, so that changes that alter behaviour are detected.

1. **Find a seam** — a place where you can call the code and observe its output without changing its behaviour: a function boundary, a command-line entry point, an HTTP endpoint, a substitutable dependency.
2. **Write a test with a placeholder expectation**, run it, and copy the actual output into the assertion. The test now documents current behaviour.
3. **Cover the paths you're about to touch**, using inputs that exercise each branch (coverage tools help find which branches you have reached).
4. For large outputs, **golden-master / approval tests**: capture the full output for a range of inputs to files, and diff against them on every run.
5. **Mark surprising behaviour** you capture — it may be a bug, but changing it is a separate, deliberate decision with the user. A characterization test asserts what *is*, not what *should be*.
6. **Break dependencies minimally** to get the code under test: extract a method to isolate logic from I/O, parameterise a constructor to inject a dependency, wrap a static/global call. Use the safest, most mechanical refactorings (ideally automated by the IDE) since you have no safety net yet.

Once characterized, proceed with normal TDD for the change: new behaviour gets new failing tests first.

See `legacy-modernization` for broader strategy and `refactoring` for safe dependency-breaking moves.

## When TDD helps and when it doesn't

TDD tends to pay off well for:

- Business rules, calculations, parsers, validators, state machines — logic with clear inputs and outputs.
- Bug fixes (reproduce first).
- Library and API design, where writing the caller first improves the interface.
- Code that will be maintained for a long time by several people.
- Work where requirements are clear in examples but the implementation is not obvious.

It is weaker or needs adaptation for:

- **Exploratory spikes**, where you don't yet know what you're building or whether an approach works. Spike without tests in a throwaway branch, learn, then delete the spike and rebuild test-first (or add tests before merging). The failure mode is keeping the spike.
- **UI layout and visual design**, where the "correct" output is judged by eye. Test the behaviour and state logic test-first; review visuals by looking or with visual regression snapshots.
- **Thin glue over frameworks or external systems**, where most of the risk is in configuration and integration. Integration tests (written first or immediately after) give better return than unit-level TDD.
- **Highly uncertain research or data-science code**, where the question changes daily. Test the stable, reusable pieces.
- **Performance-critical inner loops**, where the design is driven by measurement; TDD the correctness, then optimise against tests and benchmarks.

Experts genuinely disagree on how strictly to apply TDD. Evidence from studies is mixed on productivity and generally positive on defect rates, with large variance depending on experience and context. Treat it as a tool, use it where the feedback is valuable, and be honest about where you are not using it.

## Discovering context

- **Find the project's test runner, structure, and naming conventions** before writing the first test. Put tests where the project puts them, use its assertion style and fixtures.
- **Get a fast loop.** Discover how to run a single test or file, and whether there's a watch mode. TDD with a 2-minute test run is miserable; look for the project's fast tier or run targeted tests.
- **Check the existing test style** — classicist or mockist, use of factories, use of test doubles — and match it, unless the user asks to change it.
- **If the user asked for TDD explicitly**, show the loop: mention or commit the failing test before the implementation if they want to see that evidence. If they didn't ask, apply TDD's habits where useful without ceremony.
- **If you can't execute tests**, still write the test first and reason explicitly about what it will report before and after the change; tell the user what to run to confirm each stage.

## Showing the work

When TDD was requested, the evidence matters as much as the result:

- Report the cycle at a useful granularity: the tests written, the failure each produced before the implementation, and the change that made it pass. A summary such as "test X failed with `expected 3, got 0`; implemented Y; all 42 tests pass" is more trustworthy than "added tests".
- If the project or user values history, commit in a rhythm that shows it (for example a failing test and its implementation in adjacent commits, or one commit per green step) — but follow the repository's commit conventions, and don't commit a red test to a shared branch where CI would break for others.
- Be explicit about any part not done test-first (a spike, generated code, UI layout) and how it was verified instead.
- Keep the test list visible to the user when it contains open requirement questions; those are decisions for them, not for you.

## Checking the tests themselves

TDD guarantees each test failed once, but not that the suite is sensitive to every important change. Periodically, and especially for critical logic:

- Flip a comparison (`>` to `>=`), remove a branch, or return a constant, and confirm a test fails. If none does, a behaviour is unspecified.
- Where a mutation-testing tool exists for the language, run it on the module to find surviving mutants systematically.
- A surviving mutant means either a missing test or dead code; resolve it as one or the other.

## Readability of test-driven tests

Because TDD tests double as the specification, invest in their readability:

- Name each test as a sentence about behaviour; reading only the names should describe the unit.
- Show the relevant inputs in the test body; hide irrelevant setup behind builders with defaults.
- Prefer literal expected values over computed ones.
- One behaviour per test; group related tests by scenario rather than by method name.

## Pitfalls

- **Writing several tests before any code.** You lose the incremental feedback, and when the batch goes green or red you can't tell which piece mattered. One failing test at a time (a written test *list* is fine).
- **Skipping the "watch it fail" step**, especially when tests are written slightly after the code. Unseen failures hide vacuous tests.
- **Skipping the refactor step**, producing a pile of special cases that each made one test pass.
- **Refactoring while red.** You can't distinguish refactoring breakage from incomplete behaviour.
- **Testing implementation details** to drive code — private methods, specific internal calls — so that the design can't change without rewriting tests.
- **Over-mocking in outside-in TDD**, leading to a suite that passes while the integrated system fails. Keep an outer integration/acceptance test.
- **Giant steps**: writing the whole algorithm to satisfy the first test. If you're writing more than a few lines to go green, the test was too big or the strategy should be fake-it.
- **Gold-plating**: adding behaviour no test demands "because we'll need it." Add it to the test list instead and decide later.
- **Treating TDD as a reason not to think about design.** TDD gives feedback on design; it does not replace knowing the domain, considering architecture, or talking to the user about requirements.
- **Keeping the spike.** Exploratory code that becomes production code without tests is the most common way "we'll add tests later" becomes "never."
- **Dogmatic application** to tasks where it doesn't fit, burning time and goodwill.

## Verification

- [ ] Every new behaviour has a test that was observed failing before the implementation existed (or, for characterization, was observed to fail when the code was deliberately altered).
- [ ] Failures were for the right reason (assertion on behaviour, not setup errors).
- [ ] All tests pass after the final refactor; the suite was run, not just the newest test.
- [ ] Tests exercise the public interface and would survive an internal restructuring.
- [ ] No production code exists that no test demands (a quick check: deleting a branch should fail some test).
- [ ] The refactor step happened: no obvious duplication, names reflect the domain.
- [ ] Remaining items on the test list are either done, consciously dropped, or raised with the user as open questions.
- [ ] Tests follow the project's conventions and run in its normal test command.
