---
name: end-to-end-testing
description: >-
  Write, stabilize, and run reliable end-to-end and UI automation tests for
  web, mobile, and desktop apps with tools such as Playwright, Cypress,
  Selenium/WebDriver, WebdriverIO, Appium, Detox, or XCUITest/Espresso.
  Covers choosing what deserves an E2E test, resilient selectors, test
  isolation and data setup, waiting correctly instead of sleeping, diagnosing
  and fixing flaky tests, page objects and fixtures, running in CI with
  parallelism and artifacts, and visual regression testing. Use when asked to
  "write an E2E test", "add Playwright/Cypress tests", "our UI tests are
  flaky", "test this user flow in the browser", set up visual snapshots, or
  run browser tests in CI. For overall test-suite strategy use
  testing-strategy; for one-off browser scripting use browser-automation.
metadata:
  category: quality
  related: testing-strategy, qa-test-planning, ci-cd-pipelines, browser-automation, frontend-development, debugging, accessibility-audit, test-driven-development
---

# End-to-End Testing

End-to-end (E2E) tests drive the real application the way a user does, through the UI or the public interface, with real or realistic backends. They give the strongest evidence that a flow works and they are the most expensive tests to write, run, and keep green. The craft is in making a small number of them extremely reliable.

## Scope

Covers automated tests that exercise a running app through its user interface: browser tests, mobile UI tests, desktop UI tests, and API-level journey tests that span services. Covers tool choice, test design, selectors, data, waiting, flakiness, CI, and visual regression.

Not covered here:

- How many tests of each kind a codebase should have overall, and where unit and integration tests fit — `testing-strategy`.
- Deciding *what* to test across a release, including manual and exploratory testing — `qa-test-planning`.
- Scripting a browser to perform a task (scraping, form-filling automation) — `browser-automation` / `web-scraping`.
- Pipeline mechanics beyond test-specific concerns — `ci-cd-pipelines`.

## Core principles

**1. Reserve E2E for what only E2E can prove.** Every E2E test costs seconds to minutes per run, depends on many moving parts, and fails for reasons unrelated to the code under test. Put a behavior in an E2E test when the risk is in the integration: the critical user journeys (sign-up, sign-in, checkout, core create/save flows), wiring between frontend, backend, auth, and third parties, and things that only break in a real browser (routing, cookies, file upload, rendering). Push logic permutations (validation rules, calculations, formatting) down to unit and component tests, where they run in milliseconds and fail precisely.

**2. A flaky test is worse than no test.** When a test fails randomly, people learn to rerun and ignore failures, and then they ignore real ones too. Reliability is the first quality requirement of an E2E suite, ahead of coverage. Fix or quarantine flaky tests immediately.

**3. Test behavior through the user's eyes.** Interact the way a user does (click the button labelled "Save", type into the field labelled "Email") and assert what a user can observe (a heading appears, a message is shown, the URL changes, the item is in the list). Tests coupled to implementation details (CSS classes, DOM structure, internal state) break on every refactor without catching more bugs.

**4. Each test owns its world.** A test must not depend on another test having run, on the order of tests, or on leftover data. Isolation is what makes parallelism possible and failures diagnosable.

**5. Never sleep; wait for a condition.** Fixed delays are either too short (flaky) or too long (slow), and usually both on different machines. Wait for the observable state that means "ready".

**6. Failures must explain themselves.** When an E2E test fails in CI at 3 a.m., the artifacts (trace, screenshot, video, logs, network) should let someone diagnose it without rerunning locally. Configure that from the start.

## Process

### 1. Discover the existing setup

Before writing anything, look for:

- Existing E2E framework, config files, and folder conventions (e.g. `playwright.config.*`, `cypress.config.*`, `wdio.conf.*`, Appium capabilities, `e2e/` or `tests/` directories).
- Helpers already present: custom commands, fixtures, page objects, login shortcuts, data factories, seed scripts, test IDs convention.
- How tests are run locally and in CI, which browsers/devices, how the app is started (dev server, built preview, deployed environment, containers).
- Known flaky tests or quarantine lists, retry settings.

Follow what is there. Introducing a second framework or a parallel helper style fragments the suite. If no framework exists, choose one (see Decision guidance) and keep the initial setup minimal.

### 2. Choose the journeys

List the critical user journeys and rank them by business impact and integration risk. For each, write one E2E test that walks the main path with a meaningful assertion at the end, then add only the variations whose risk lies in integration (e.g. a declined payment returned from the real payment sandbox). Leave field-level validation variants to lower levels.

A useful sanity check: if the test's name describes a business outcome ("guest can buy a product with a card"), it probably belongs in E2E. If it describes a rule ("postcode must be 5 digits"), it probably does not.

### 3. Design the test

Structure each test as arrange, act, assert, with the arrange step done as cheaply as possible:

- **Arrange through the back door.** Create users, seed data, and log in via API calls, database fixtures, or programmatic auth (storing an authenticated session state and reusing it), not by clicking through the UI every time. Only the flow under test should go through the UI. Test the login UI itself once, in its own test.
- **Act through the front door.** Perform the user's actions in the UI.
- **Assert on outcomes.** Check what the user sees and, where valuable, the durable effect (record exists via API). Do not stack dozens of incidental assertions; each extra assertion is another reason to fail for unrelated changes.

Keep tests short and independent. A 40-step test that covers five features fails often, and its failures are hard to localize. Prefer several focused journeys that share setup helpers.

### 4. Select elements resiliently

Prefer, in roughly this order:

1. **Accessible roles and names** — e.g. "the button named Submit", "the textbox labelled Email", "the heading Order confirmed". Playwright's role locators, Testing Library-style queries (available for Cypress, WebdriverIO, and others), and accessibility IDs on mobile support this. These survive markup refactors, mirror how users and assistive technology find elements, and fail when accessibility regresses, which is a useful side effect.
2. **Visible text and labels** — for links, menu items, and content, when text is stable. Be careful with localized apps: run tests in a fixed locale, or use keys.
3. **Dedicated test IDs** (`data-testid`, `data-test`, `accessibilityIdentifier`, `testID`) — for elements with no stable accessible name, repeated items, or canvases. They are explicit contracts that survive copy and style changes. Use the project's existing attribute name.
4. **CSS or XPath structure** — last resort. Long chains such as `div > div:nth-child(3) .btn-primary` break with any layout change.

Scope locators to a region when the page has repeats: "within the row containing 'Invoice 1042', click 'Download'". Avoid index-based selection ("the third button") unless order is the thing being tested.

If the app lacks accessible names, adding them helps both tests and users; propose that rather than writing brittle selectors around it.

### 5. Wait correctly

Modern tools (Playwright, Cypress, WebdriverIO, Detox, Espresso with idling resources) auto-wait for elements to be attached, visible, stable, and enabled before acting, and retry assertions until a timeout. Use that:

- Use web-first / retrying assertions ("expect locator to have text", "should contain") rather than reading a value once and comparing.
- Wait for the user-visible signal of completion: the success message, the updated row, the spinner disappearing, the URL changing.
- When you must wait for network, wait for the specific request or response the action triggers, set up *before* the action to avoid races, not for "network idle" across the whole page (analytics, polling, and websockets keep networks busy forever).
- Never use fixed sleeps (`sleep(2000)`, `cy.wait(2000)`, `Thread.sleep`). If you find yourself needing one, you have not identified the readiness condition yet.
- In Selenium, use explicit waits with expected conditions; avoid mixing implicit and explicit waits, which compound timeouts unpredictably.
- On mobile, synchronization frameworks (Espresso, XCUITest, Detox) wait for the app's main thread and animations; custom async work may need registering (idling resources) so the framework knows the app is busy.

Timeouts: keep defaults sensible (seconds, not minutes) so failures are fast. Raise a timeout for a specific known-slow operation rather than globally.

### 6. Manage test data and isolation

- Create the data each test needs, with unique identifiers (e.g. a random suffix or the worker index) so parallel tests do not collide.
- Clean up when cheap, but design so leftovers do not matter: tests should not query "all items" and expect an exact count from a shared database.
- Prefer a fresh environment per run (containers, ephemeral databases, per-branch preview environments) when feasible. Shared long-lived staging environments are a major source of flakiness because other people and other runs change them.
- Reset client state between tests: cookies, local storage, service workers, IndexedDB. Most frameworks give each test a fresh browser context; do not disable that for speed without understanding the cost.
- Control time and randomness where the app depends on them (fake the clock, seed random generators) for date-sensitive features.
- Mock or stub third-party services you do not own and cannot rely on (rate-limited APIs, email, SMS, payments in some cases), but keep at least one path against a realistic sandbox where the integration itself is the risk. Network interception (route mocking) is good for error states that are hard to produce for real: 500 responses, timeouts, malformed payloads.
- Never put real credentials in test code or logs. Use environment-provided secrets for test accounts, scoped to test environments.

### Illustrative example

The following sketch (Playwright-style TypeScript, purely to show the shape; translate to the project's tool and conventions) puts the principles together:

```ts
test('member can reorder a past purchase', async ({ page, api }) => {
  // Arrange through the back door: unique data, programmatic login.
  const user = await api.createUser({ tier: 'member' });
  const order = await api.createOrder(user, { items: ['SKU-123'] });
  await api.loginAs(page, user);

  // Act through the front door.
  await page.goto('/orders');
  const row = page.getByRole('row', { name: new RegExp(order.number) });
  await row.getByRole('button', { name: 'Reorder' }).click();

  // Assert on what the user sees, with retrying assertions.
  await expect(page.getByRole('heading', { name: 'Your cart' })).toBeVisible();
  await expect(page.getByRole('listitem').filter({ hasText: 'SKU-123' })).toHaveCount(1);
});
```

Notice what is absent: no sleeps, no CSS paths, no dependence on any other test's data, no UI login, and no assertions about unrelated parts of the page.

### Awkward cases

- **New tabs and popups:** wait for the new page event triggered by the click, then operate on that page; do not assume the active tab switched.
- **Iframes** (payment fields, embedded editors): locate the frame first, then elements inside it. Cross-origin payment iframes may be impossible to drive reliably; use the provider's test mode and documented test hooks, and keep such tests few.
- **File upload and download:** set files directly on the input rather than driving the OS dialog; for downloads, wait for the download event and assert on the file name and content.
- **Email, SMS, one-time codes:** route messages to a test inbox service or capture them via a test-only API, then read the code programmatically. Never disable security checks in production builds to make tests pass; use test-environment configuration.
- **Third-party sign-in (OAuth/SSO):** do not drive the real identity provider's login page in routine tests; it changes, rate-limits, and may block automation. Use a test identity provider, a mocked auth server, or session injection, and test the real integration in a small, separate, monitored check.
- **CAPTCHAs and bot detection:** disable or bypass them in test environments through configuration, never by trying to solve them.
- **Canvas, maps, charts:** assert on the underlying data or accessible alternatives, or use visual comparison; DOM assertions cannot see inside a canvas.
- **Websockets and live updates:** assert on the resulting UI with retrying assertions; trigger server events through a test API rather than waiting for real ones.
- **Mobile system dialogs** (permissions, notifications): pre-grant permissions through device or simulator settings where possible, or handle the dialog explicitly with the framework's system-alert support.

### Worked reasoning: a flaky test

Symptom: "add to cart" fails about one run in ten in CI with "expected cart count 1, received 0", never locally.

1. The failure is an assertion, not a locator timeout, so the click happened. Either the request was not sent, did not complete, or the UI did not update.
2. The trace shows the click occurred while a product-recommendations panel was still loading and shifting layout; the click landed on the panel, not the button.
3. Root cause: layout shift, more likely on slower CI machines. The test is not wrong to fail: real users on slow devices can misclick too.
4. Options: wait for the panel to finish loading before clicking (test fix), or reserve space for the panel so the button does not move (product fix, also improves layout stability metrics). Prefer the product fix and tell the team; apply the test fix only if the product fix is not accepted.
5. Verify by running the test 50 times under CPU throttling before and after.

The pattern: read the artifacts, find what the user would have experienced, decide whether the bug is in the test or the product.

### 7. Organize the code

- **Page objects or screen models** encapsulate how to interact with a screen ("login as", "add item to cart") so a UI change is fixed in one place. Keep assertions mostly in tests, not in page objects, so tests read as specifications. Avoid giant inheritance hierarchies; composition of small components ages better.
- **Fixtures** (Playwright fixtures, Cypress commands, pytest fixtures with Selenium) provide set-up resources such as an authenticated page, a seeded account, or an API client, with automatic teardown.
- **Name tests by behavior,** so a failure list reads as a list of broken capabilities.
- Do not abstract too early. Duplicate a few lines across two tests; extract on the third.

### 8. Debug failures and flakiness

When a test fails, first decide which of these it is:

| Cause | Typical signs | Fix |
|---|---|---|
| Real product bug | Reproducible manually; fails consistently since a commit | Report or fix the bug; the test did its job |
| Race in the test (acted before ready) | Passes locally, fails under CI load; failure on click or read | Wait for the right condition; use retrying assertions |
| Race in the app | Fails intermittently even with correct waits; a double-render or out-of-order responses | A real bug users can hit; fix the app |
| Shared or leaked state | Fails only when run with others or in a certain order; passes alone | Isolate data and browser state; unique IDs |
| Environment | Fails on one CI runner, at certain times, or when a dependency is slow | Stabilize the environment; mock the unstable dependency; health check before tests |
| Brittle selector | Fails after an unrelated UI change | Switch to role/label or test ID locators |
| Animation or layout shift | Click lands on the wrong element or "element intercepted" | Wait for stability; disable animations in test mode |
| Test-order dependency or time/date | Fails on certain days, near midnight, in other time zones | Control the clock; avoid date assumptions |

Practical steps:

- Reproduce under stress: run the test many times in a loop, in parallel, with CPU throttling or a slowed network. Most tools have a repeat option.
- Read the trace or video at the moment of failure, not just the error message. Traces showing DOM snapshots and network per step (e.g. Playwright's trace viewer, Cypress's time-travel) diagnose most flakes in minutes.
- Check console errors and failed network requests during the test.
- Retries: a small number of retries in CI is a reasonable safety net, but track tests that only pass on retry and treat them as flaky bugs. Retries that hide flakiness silently erode trust.
- Quarantine: if a flaky test cannot be fixed today, move it to a non-blocking quarantine with an owner and a deadline, rather than deleting it or leaving it to fail the build randomly.

### 9. Run in CI

- **Start the app deterministically:** build once, start it, wait for a health check before starting tests. Testing a production-like build catches issues a dev server hides.
- **Parallelize:** shard across workers or machines; isolation from step 6 is the prerequisite. Balance shards by duration if the tool supports it.
- **Choose what runs when:** a fast smoke subset on every pull request, the full suite on merge or nightly, the cross-browser/device matrix less often if it is slow. Tag tests to select subsets.
- **Pin versions:** browser and driver versions, container images, and the test tool, so upgrades are deliberate. Upgrade regularly, since browsers move fast.
- **Collect artifacts on failure:** traces, screenshots, videos, console and server logs, and test reports (JUnit XML or HTML) attached to the run. Keep them on failure only if storage is a concern.
- **Headless vs headed:** headless is standard in CI; behavior is nearly identical in modern browsers, but if something only fails headless, check viewport size, fonts, GPU features, and timing.
- **Track suite health:** duration, pass rate, flaky rate per test over time. A suite that grows slowly in duration and flakiness until nobody trusts it is the common failure; dashboards make the trend visible.
- **Fail fast but report fully:** stop the job on catastrophic setup failure; otherwise let the suite run so one failure does not hide others.

### 10. Visual regression testing

Visual tests compare screenshots against approved baselines to catch unintended visual changes (layout breaks, missing styles, overlapping text) that functional assertions miss.

- Use them for stable, high-value surfaces: design-system components (often via a component workshop such as Storybook), key pages, and templates. Not for every page and state.
- Control the rendering environment: same OS image, browser version, fonts, viewport, device scale factor. Run baselines and comparisons in the same container. Baselines generated on a laptop and compared in CI will differ.
- Remove sources of noise: freeze time, seed data, disable animations and carets, mask dynamic regions (dates, avatars, ads, maps), wait for fonts and images to load.
- Choose a sensible diff threshold; zero tolerance produces noise from antialiasing, and a large tolerance hides real regressions. Tune per suite.
- Review diffs as a human step; approving baselines without looking turns the suite into a rubber stamp. Hosted visual review services and built-in snapshot comparisons (e.g. Playwright's screenshot assertions) both work; choose by team workflow and budget.
- Cover responsive breakpoints and themes (dark mode, right-to-left) that matter.

### 11. Accessibility checks in E2E

Running an accessibility rule engine (e.g. axe-core integrations) inside E2E tests on key pages and states catches regressions in machine-checkable criteria cheaply. Scan after the page reaches the state of interest (dialog open, error shown). It does not replace manual auditing (`accessibility-audit`), and using role-based locators already enforces some accessibility.

### 12. Cross-browser and device coverage

Run the full suite on one primary browser and a critical-path subset on the others, choosing engines and devices from real usage data (see `qa-test-planning` for building the matrix). Emulated mobile viewports in a desktop browser catch responsive layout problems but not touch behavior, mobile Safari quirks, virtual keyboards, or performance; run a small set on real devices or a device cloud for those. When a test needs different behavior per platform, branch on capability ("is the menu collapsed?") rather than on browser name where possible.

### 13. API-level journey tests

Not every end-to-end test needs a UI. A journey test that calls the public API in sequence (create account, add payment method, place order, receive webhook, query order status) across real services verifies integration at a fraction of the cost and flakiness of the UI version. Use them for backend-heavy flows, for services without a UI, and to cover variants of a journey whose UI path is already covered once.

### 14. Keep the suite healthy over time

- Review E2E tests in code review like product code: is this the right level, are selectors resilient, is setup cheap?
- Delete tests that duplicate coverage at a lower level or test features that no longer exist. A suite only grows unless someone prunes it.
- Set a duration budget per stage (for example, the pull-request smoke suite must stay under about ten minutes) and treat breaches like any other regression.
- Assign ownership of failing and quarantined tests; unowned failures become permanent.
- When a production bug escapes, ask whether an E2E test at the journey level would have caught it, or whether a lower-level test is the better guard. Add the cheapest test that would have failed.

## Decision guidance

**Choosing a web tool** (all are capable; existing use wins):

| Factor | Leans toward |
|---|---|
| Multiple browser engines including WebKit, multi-tab/origin flows, strong tracing, parallelism built in | Playwright |
| Developer-friendly interactive runner, large plugin ecosystem, team already fluent | Cypress (check its current cross-origin and multi-tab support for your flows) |
| WebDriver standard, broad language support, existing grid infrastructure, real-device clouds | Selenium / WebdriverIO |
| Testing component behavior in isolation in a real browser | Component testing modes of the above, or a component workshop with interaction tests |

**Mobile:** Appium for cross-platform and black-box testing with one language; Espresso (Android) and XCUITest (iOS) for fast, stable native tests owned by app developers; Detox for React Native with built-in synchronization; Maestro and similar for simple declarative flows. Native frameworks are usually faster and less flaky; cross-platform tools trade that for one codebase.

**Real backend vs mocked backend:**

| Use the real backend when | Mock the backend when |
|---|---|
| The integration is the risk being tested | Testing UI behavior in states hard to produce (errors, empty, huge lists) |
| You own the services and can seed them | The service is third-party, rate-limited, costly, or unreliable |
| Few, critical journeys | Many UI variations that would be slow end to end |

A healthy suite usually has a small set of fully integrated journeys plus a larger set of UI tests with network stubs. Be explicit about which is which, because a mocked test passing says nothing about the contract with the real API (contract tests address that gap).

**Through the UI vs through the API:** test the flow through the UI only for the step whose UI matters. Everything else (setup, verification of side effects) through the API.

## Safety

E2E tests create, change, and delete data and can send messages or charge money. Guard against running them where they cause harm:

- Point tests at test environments by default; require an explicit, deliberate configuration to target anything shared or production-like.
- Production smoke tests (synthetic monitoring) should be read-only or use dedicated synthetic accounts that are flagged and excluded from billing, analytics, and emails to real people.
- Use payment providers' test modes and published test card numbers only; never real payment details.
- Keep secrets for test accounts in the CI secret store, never in the repository, screenshots, videos, or traces (traces can capture request headers and form values: mask or exclude sensitive fields).
- Cleanup routines that delete data must be scoped to data the test created (e.g. by a unique prefix), never "delete all users".

## Pitfalls

- **Inverted pyramid.** Hundreds of E2E tests covering logic that unit tests should cover; the suite takes an hour and is always red.
- **Sleeps.** The single most common cause of flaky and slow suites.
- **Logging in through the UI in every test.** Slow and multiplies failure points.
- **Chained tests.** Test B uses the order created by test A; one failure cascades into many and parallelism is impossible.
- **Brittle selectors** tied to classes generated by CSS-in-JS or build tools, or to deep DOM paths.
- **Asserting on incidental details** like exact pixel positions or full page text, which change for unrelated reasons.
- **Retries as a cure.** Raising retries to five makes the build green and the suite meaningless.
- **Shared staging data.** Someone deletes the test product and every run fails.
- **Testing third parties.** Your suite fails when an external sandbox is down; you learn nothing about your code.
- **Ignoring test code quality.** Test code is production code for your confidence; duplication and unclear names cost the same as anywhere else.
- **No artifacts.** "Timed out waiting for selector" with nothing else is undiagnosable.
- **Visual baselines from mixed environments,** producing constant false diffs that teach people to approve blindly.
- **Tests that never fail.** An assertion on something always true (an element that exists on every page), or a swallowed error in a helper, gives green builds and no protection. Prove each new test can fail.
- **Over-mocking the journey.** If every network call is stubbed, the "end-to-end" test is a component test with a slower runner; label it honestly and keep at least one truly integrated path.

## Quality bar and verification

Before calling a new or fixed E2E test done:

- [ ] It tests a behavior whose risk is in integration or the real UI, not logic that belongs lower.
- [ ] Locators use roles, labels, text, or test IDs; no structural CSS chains.
- [ ] No fixed sleeps; all waits are on observable conditions.
- [ ] Setup uses API or fixtures; only the flow under test goes through the UI.
- [ ] It creates its own data with unique identifiers and does not depend on other tests or order.
- [ ] It passes when run alone, in the full suite, in parallel, and repeatedly (run it many times in a loop, ideally under throttling; one green run proves little).
- [ ] It fails for the right reason: temporarily break the behavior (or invert the assertion) and confirm the test goes red with a clear message.
- [ ] Failure artifacts (trace/screenshot/logs) are produced and readable.
- [ ] It runs in CI with the same configuration as locally, and its duration is acceptable for the stage it runs in.
- [ ] It follows the project's existing conventions for structure, naming, and helpers.

If you cannot execute the tests in your environment, say so, deliver the code, and list the exact commands the user should run and what a passing run looks like.
