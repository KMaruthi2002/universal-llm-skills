---
name: full-stack-app-build
description: >-
  Generate a complete, working full-stack application from a description:
  capture requirements, choose a stack by constraints rather than taste, design
  the data model first, build in vertical slices, add authentication, seed
  realistic data, run it end to end, define a deploy path, and hand it over
  with clear run instructions. Use when asked to "build an app", "make me a
  web app that...", "create a SaaS / CRUD / internal tool / portal", or to
  turn a spec or idea into a running product with a frontend, backend and
  database. Not for throwaway idea tests (mvp-prototyping), static marketing
  sites (website-and-landing-pages), or native mobile/desktop clients.
metadata:
  category: app-generation
  related: clarify-requirements, plan-and-decompose, project-scaffolding, software-architecture, database-design, api-design, frontend-development, backend-development, authentication-and-authorization, testing-strategy, end-to-end-testing, verify-before-done, ci-cd-pipelines, mvp-prototyping
---

# Full-Stack App Build

## Purpose and scope

This skill covers producing a whole application — data store, server logic, user interface, authentication, and a way to run and deploy it — from a description that may be one sentence or twenty pages. The deliverable is not "code that looks like an app". It is **an application someone else can start with documented commands, log into, and use to complete the core jobs it was built for.**

Boundaries:

- Testing whether an idea is worth building at all, with fakes and shortcuts on purpose: `mvp-prototyping`.
- Content-led marketing sites, docs and landing pages: `website-and-landing-pages`, `documentation-site`.
- Native mobile or desktop clients: `mobile-app-development`, `desktop-app-development` (this skill can still build their backend).
- Deep dives on any single layer: `database-design`, `api-design`, `frontend-development`, `backend-development`, `authentication-and-authorization`. This skill is the conductor; those are the sections of the orchestra.
- Setting up an empty repository and toolchain: `project-scaffolding`.

## The failure this skill exists to prevent

The most common outcome of "generate me an app" is a large pile of plausible files that **do not run**: a frontend calling endpoints that do not exist, an ORM model that disagrees with the migration, an auth flow that was never exercised, environment variables nobody documented, a dependency that was imagined. Each file looks fine in isolation. The system fails at the seams.

Everything below is organised around one idea: **seams first, and prove each seam works before building on it.** That is why the data model comes first (it is the seam every layer shares), why work proceeds in vertical slices (each slice crosses every seam), and why "run it" is a step in every slice rather than a phase at the end.

## Core principles

1. **Running beats complete.** A small app that starts and works end to end is worth more than a large one that does not. Why: a running app can be extended and verified; a non-running one must be debugged across every layer at once, and the cost of that grows with its size.

2. **Choose the stack by constraints, not taste.** The right stack is the one that fits where it will be deployed, who will maintain it, what the existing systems are, and what the app must do. Why: an elegant stack that the owner cannot host, maintain, or hire for is a liability handed over with a bow on it.

3. **The data model is the spine.** Model entities, relationships, ownership and lifecycle before writing screens or endpoints. Why: UI and API are views over the data; changing them is cheap, changing the data model after data exists is the most expensive change in the system.

4. **Vertical slices, not horizontal layers.** Build one feature through database, API and UI, run it, then build the next. Why: a horizontal approach (all models, then all endpoints, then all screens) defers integration — and therefore discovery of mismatch — to the end, when it is most expensive.

5. **Boring where it does not matter, careful where it does.** Use mainstream, well-documented choices for everything that is not the app's differentiator. Why: every unusual choice costs maintenance and documentation; spend that budget only where it buys something.

6. **Security and data integrity are not features to add later.** Authorization checks, input validation, secret handling and safe defaults go in with the first slice. Why: retrofitting authorization onto an app that assumed a single user requires touching every query.

7. **The handover is part of the product.** Someone who did not watch you build it must be able to install, configure, run, seed, test and deploy it. Why: an app only its author can start is not delivered.

## Process

### 1. Capture requirements just enough

Turn the description into a short working spec. You need answers to these; infer what you safely can, and ask about the ones where a wrong guess is expensive (see `clarify-requirements`):

- **Users and roles.** Who uses it? Are there distinct roles with different permissions (admin, member, viewer, customer, staff)? Is it single-user, multi-user within one organisation, or multi-tenant (many organisations whose data must never mix)? Multi-tenancy is the single most consequential answer here — it changes the data model, every query and the auth design.
- **Core jobs.** The three to seven things users must be able to do for the app to have succeeded. Phrase them as user outcomes ("a manager approves a timesheet"), not screens.
- **Data.** What things exist, who owns them, what must be kept, what is sensitive (personal data, payment data, health data).
- **Integrations.** Email, payments, file storage, third-party APIs, existing databases or identity providers.
- **Constraints.** Where it must run, budget, expected scale, who maintains it, existing languages and infrastructure, compliance needs, deadline.
- **Non-goals.** What it explicitly does not do in this version. Write these down; they protect scope.

Questions worth asking because a wrong guess is costly: multi-tenant or not; where it will be hosted; whether there is an existing system or database to integrate with; whether real users' personal or payment data is involved; what the maintainer already knows. Questions not worth blocking on: colours, exact copy, which icon set — pick sensible, neutral defaults that fit any brand guidance you were given and note them as easy to change.

Write the result down (a short `SPEC` section in the README or a planning note). It is the reference you will verify against at the end.

### 2. Discover context before choosing anything

If this extends an existing project or organisation, its conventions win (see `explore-codebase`):

- Existing language, framework, ORM, test runner, linter, formatter, package manager and lockfile.
- Existing auth provider, design system, component library, API style (REST, GraphQL, RPC), error format.
- Existing deployment target and CI configuration.
- Naming conventions for files, routes, database tables and columns.

If a repository exists, read its README, dependency manifest, configuration, a representative route, a representative model and a representative test before writing anything. Match them. A new app that ignores the organisation's existing stack creates a second system to maintain.

### 3. Choose the stack by constraint

Decide in this order, because earlier answers constrain later ones:

1. **Deployment target** — what can actually run this? (A managed platform, a container host, serverless functions, a company VM, an on-premises server, the user's laptop.)
2. **Maintainer skills** — what language does whoever inherits this know?
3. **Data shape and integrity needs** — relational, document, time-series, search, files.
4. **Interaction model** — mostly forms and lists; highly interactive client; real-time collaboration; offline.
5. **Framework** — the most mainstream option in the chosen language that fits the above.

| Constraint | Leans toward | Why |
|---|---|---|
| Mostly CRUD, forms, admin screens, small team | A batteries-included server-rendered framework (e.g. Django, Rails, Laravel, Phoenix) or a full-stack JS meta-framework | Auth, ORM, migrations, validation and admin come built in; least glue code to get wrong |
| Highly interactive UI (editors, drag-and-drop, dashboards with live filtering) | A component-based client framework with a separate or co-located API | Client state management is the core problem; server rendering alone fights it |
| Must deploy as static files plus functions, or to an edge platform | A framework with first-class support for that platform's adapter | Avoids fighting the host's runtime limits (no long processes, cold starts, no local disk) |
| Real-time collaboration or live updates for many users | A stack with mature WebSocket or server-sent-event support and a pub/sub layer | Polling does not scale and bolted-on sockets leak connections |
| Strong relational integrity (money, inventory, bookings, permissions) | A relational database with transactions and constraints (e.g. PostgreSQL, MySQL, SQLite for single-node) | Constraints catch bugs the application layer misses; transactions prevent double-booking |
| Heterogeneous, schema-light records with few cross-record invariants | A document store, or JSON columns in a relational DB | Flexibility where it is actually needed, without giving up joins elsewhere |
| Single user / single machine / internal tool with low traffic | SQLite, a single process, minimal infrastructure | Nothing to operate; backup is copying a file |
| Organisation already standardised on a stack | That stack | Consistency beats local optimisation |
| Typed end-to-end contract matters (many developers, long life) | A typed language on both sides, or a schema-generated client (OpenAPI, GraphQL codegen, tRPC-style) | Seam mismatches become compile errors instead of runtime bugs |

Do not choose a stack because it is new, because it is your favourite, or because a tutorial used it. If two options are genuinely close, pick the one with better documentation and a larger community, because the maintainer will need answers you are not there to give. State the choice and the deciding constraints in one or two sentences in the handover — see `technical-decision-making`.

**Monolith first.** Unless constraints demand otherwise, build one deployable application with a clear internal module structure. Splitting into services multiplies the seams this skill is trying to control. See `software-architecture`.

### 4. Model the data first

Before any screens or endpoints:

- **List entities** from the core jobs. Nouns in the job statements are candidates ("manager", "timesheet", "project").
- **Define relationships and cardinality** (one-to-many, many-to-many via join tables).
- **Assign ownership.** For each entity: which user or tenant owns it? This field is what authorization will check. In multi-tenant apps, every tenant-owned table carries a tenant identifier, and every query filters by it.
- **Define lifecycle and state.** What states can a record be in (draft, submitted, approved, archived)? Which transitions are legal and who may make them? A small state machine written down now prevents contradictory flags later (`is_approved` and `is_rejected` both true).
- **Decide deletion semantics.** Hard delete, soft delete (an `archived_at` or `deleted_at` column), or retention rules. Soft delete must then be honoured by every query — note this as a risk.
- **Put constraints in the database**: not-null, unique, foreign keys, check constraints where supported. The application layer will have bugs; the database is the last line of defence.
- **Standard columns**: a stable primary key (consider non-guessable IDs for anything exposed in URLs), created and updated timestamps, and the owner/tenant reference.
- **Indexes** on foreign keys and on columns used in common filters and sorts.

Express the model as migrations from the start, not as an ORM's "sync schema" shortcut, so that the deploy path and the local path create the same database. See `database-design` and `database-migrations`.

Sanity check: walk each core job against the model. "A manager approves a timesheet" — can the model represent which manager, which timesheet, when it was approved, and prevent an unauthorised user doing it? If not, fix the model now.

### 5. Define the API contract

For each core job, list the operations needed and their shape: method and path (or query/mutation name), request fields, response fields, errors, and **who is allowed to call it**. Choose one error format and use it everywhere. Decide pagination for every list that can grow. See `api-design`.

If the frontend and backend live in one framework (server actions, server-rendered forms), the "contract" is still real — it is the set of server functions and their inputs. Write it down anyway; it is what you will test.

### 6. Scaffold and prove the skeleton runs

Create the project with the chosen framework's standard generator or the existing repository layout (see `project-scaffolding`). Then, before any features:

- Install dependencies and commit the lockfile.
- Configure environment variables via a documented example file (e.g. `.env.example`) with every variable listed, safe placeholder values, and a comment on each. Never commit real secrets.
- Connect to the database and run the first migration.
- Get a trivial page rendering data from the database through the real server.
- Get one test running in the test runner.
- Add a health-check route.

This "walking skeleton" proves every seam exists. If it does not run now, nothing built on top of it will.

### 7. Build vertical slices

Order the core jobs so the earliest slices unlock the rest. A typical order:

1. **Authentication and the user/tenant model** — almost everything else depends on knowing who is asking.
2. **The primary entity's create and list** — the thing the app is about.
3. **View, edit, delete** of that entity, with authorization.
4. **The main workflow** (state transitions, approvals, checkout, booking).
5. **Secondary entities and relationships.**
6. **Integrations** (email, payments, uploads), each behind an interface so it can be stubbed locally.
7. **Admin and reporting.**

For each slice, the definition of done is:

- Migration (if any) applied and reversible.
- Server logic with input validation and an authorization check.
- UI that calls it, with loading, empty, error and success states.
- At least one automated test at the level that best protects it (usually an integration/API test; see `testing-strategy`).
- **You ran it** — started the app and did the job through the UI as a user would.

Only then start the next slice. When a slice reveals a model problem, fix the model with a new migration now; do not paper over it in the UI.

Keep slices thin. "Create a project" with name only, working end to end, beats "create a project" with twelve fields where the save button does not work.

### 8. Authentication and authorization

Prefer a well-maintained library or managed identity provider over hand-rolled auth. Hand-rolled password storage, session handling and reset flows are where the most damaging bugs live. See `authentication-and-authorization` and `secure-coding`.

Non-negotiables regardless of approach:

- Passwords hashed with a slow, salted algorithm designed for passwords (e.g. Argon2, bcrypt, scrypt), never reversible encryption or a fast hash.
- Session cookies `HttpOnly`, `Secure` in production, sensible `SameSite`; or tokens stored and rotated according to the chosen library's guidance.
- CSRF protection for cookie-authenticated state-changing requests.
- **Authorization on the server for every operation**, checking ownership or role against the data — not just hiding buttons in the UI. The canonical bug: `GET /invoices/123` returns invoice 123 to any logged-in user.
- Rate limiting on login, signup and password reset.
- Password reset tokens single-use, short-lived and unguessable; responses that do not reveal whether an email is registered.
- In multi-tenant apps, tenant scoping enforced in one central place (a query scope, a repository layer, row-level security) rather than remembered in every handler.

Write at least one test per role that proves a user **cannot** access another user's or tenant's data. Tests that only prove the happy path miss the bug that matters.

### 9. Seed data

Provide a seed script that creates a realistic, deterministic dataset:

- One account per role, with documented test credentials stored in the seed file or example config (development only, clearly marked, never valid in production).
- Enough records to exercise lists, pagination, search and empty states (some users with no records).
- Records in each lifecycle state, so every screen and transition can be seen without manual setup.
- Edge cases: long names, unicode, missing optional fields, boundary dates.

Make the seed idempotent or provide a reset command, so anyone can get back to a known state. Guard it so it refuses to run against a production database (check an environment flag). Why seed data matters: it is what makes the app demonstrable, testable, and debuggable by the next person.

### 10. Run it end to end

Before calling anything done, from a clean state:

1. Fresh clone (or clean directory), install dependencies with the documented command.
2. Copy the example environment file; fill only what the docs say to fill.
3. Create the database, run migrations, run the seed.
4. Start the app with the documented command.
5. Log in as each role and perform every core job from the spec through the UI.
6. Try the obvious unhappy paths: invalid input, unauthorised access by URL manipulation, double-submit, refresh mid-flow, back button, empty states.
7. Run the full test suite.
8. Check server logs and browser console for errors and warnings you have not explained.

If you can execute code and drive a browser, do this yourself (see `end-to-end-testing`, `browser-automation`). If you cannot, give the user the exact commands and a checklist of what they should see, and say plainly that you have not run it. Never claim an app works when you have only written it.

### 11. Deploy path

Define how it gets to production even if you are not deploying it now:

- Target platform and why (from constraints in step 3).
- Build command, start command, required environment variables, and which are secrets.
- How migrations run on deploy (a release step, not on every app start for multi-instance setups, to avoid races).
- Database provisioning and backups.
- Static asset and file upload storage (local disk does not survive container restarts or scale across instances).
- Health check endpoint for the platform.
- Logging and error reporting (see `observability`).
- A CI pipeline that runs tests on every change (see `ci-cd-pipelines`) and, optionally, a container definition (`containerization`).

Production configuration must differ from development: debug off, secure cookies on, real secret values from the platform's secret store, seed data and test accounts absent.

**Do not deploy, provision paid resources, or push to production without explicit confirmation from the user.** Prepare everything; let them press the button or approve it.

### 12. Hand over

The README (or equivalent) must let a stranger succeed. It contains:

- What the app does, and the spec's core jobs and non-goals.
- Stack and the one-line reason for each major choice.
- Prerequisites with versions.
- Setup, seed, run, test and build commands — exactly as you ran them.
- Environment variables table: name, purpose, example, required or optional, secret or not.
- Test accounts (development only).
- Project structure: where models, routes, UI, tests and migrations live.
- Deploy instructions.
- Known limitations, shortcuts taken, and the next most valuable work.

Report results honestly (see `report-results`): what works and was verified, what was built but not verified, what was deferred.

## Decision guidance

### Server-rendered vs. client-rendered vs. hybrid

| Choose | When |
|---|---|
| Server-rendered pages with progressive enhancement | Content and forms dominate; SEO or first-load speed matters; small team; fewer moving parts |
| Single-page client app plus API | Rich, stateful interaction; the API will also serve other clients (mobile, partners) |
| Hybrid meta-framework | You need both, and the team is comfortable with its server/client boundary rules |

### Build auth vs. use a library vs. use a managed provider

| Choose | When |
|---|---|
| Framework's built-in auth | It exists and is mature; requirements are standard (email/password, sessions) |
| Dedicated auth library | Framework lacks it; you need OAuth/social login, MFA, or passkeys |
| Managed identity provider | Enterprise SSO, compliance requirements, many apps sharing one identity, or no capacity to operate auth safely |
| Hand-rolled | Almost never; only for genuinely unusual requirements, with a security review |

### Where business logic lives

Put rules that protect data integrity in the database (constraints) and the server (validation, authorization, state transitions). The client may duplicate validation for user experience, but never be the only check. Why: anyone can call your API without your UI.

### Synchronous vs. background work

Move anything slow, flaky or retryable out of the request: sending email, generating reports, calling slow third parties, processing uploads. Use a job queue or scheduled task (see `scheduled-jobs`, `concurrency-and-async`). For a first version, a simple database-backed queue is often enough; do not introduce a message broker for three jobs a day.

### When to split into multiple services

Only when a real constraint forces it: a component needs a different runtime, scaling profile, team ownership or security boundary. "It might need to scale" is not a reason in version one.

## Extending an existing application

Much "build an app" work is really "add a substantial capability to an app that exists". The process compresses but the order holds:

- Read before writing: how are models, routes, permissions, forms, tests and migrations done here? Find the closest existing feature and use it as the pattern for yours.
- Reuse the existing auth, error format, component library, validation approach and test helpers. A second way of doing any of these is a maintenance cost the owner did not ask for.
- Add migrations that are backward compatible with the running version where deploys are rolling (add columns nullable first, backfill, then constrain) — see `database-migrations`.
- Run the existing test suite before you change anything, so you know which failures are yours.
- Keep the change reviewable: one capability per change set, with the slices visible in history (see `git-workflow`, `pull-request-workflow`).

## Working with limited execution ability

If you cannot run code, install packages or open a browser in your environment:

- Reduce invention: prefer the framework's documented generators and idioms you are confident exist in the stated version; pin versions in the manifest so the user installs what you wrote against.
- Deliver in slices anyway, and give the user a short command list and expected output after each slice so they can run it and report back. Ask for errors verbatim.
- Mark every unverified claim as unverified in the handover. "This should work" and "this works" are different statements; use the one that is true.
- Prefer fewer, larger-scope dependencies you are sure about over many small ones you are not.

## Worked reasoning: choosing for a constraint set

Illustrative only — the point is the reasoning, not the answer.

Request: "An internal tool for our 15-person clinic to track equipment maintenance. Staff log in, see due items, mark work done, managers get a weekly summary. Our IT person knows Python and runs a single Linux VM."

- Multi-tenant? No — one organisation. Roles: staff, manager.
- Deployment: one VM the organisation already runs. Maintainer: Python. So a Python batteries-included framework, one process behind a reverse proxy; no container orchestration.
- Data: equipment, maintenance tasks with due dates and recurrence, completion records with who/when. Strong integrity matters (audit trail of who did what), so relational. Traffic is tiny; SQLite would work, but if the VM already hosts PostgreSQL or backups are easier with it, that wins — ask.
- Interaction: lists and forms. Server-rendered pages; no SPA needed.
- Weekly summary: a scheduled job sending email via the organisation's existing mail relay; stubbed to the console locally.
- Sensitive data? Equipment records, not patient data — confirm that no patient identifiers will be entered, because that changes the compliance picture.
- Slices: auth with two roles → equipment CRUD (manager) → task list with due/overdue (staff) → mark done with audit record → recurrence → weekly summary job → admin.

A different constraint set — "public consumer app, expected to grow, team of JavaScript developers, deploying to a managed edge platform" — would lead to different choices through the same reasoning, not through a different preference.

## Pitfalls and anti-patterns

- **The app that does not run.** Symptoms: invented package names or APIs, imports of files never created, environment variables read but never documented, migrations out of sync with models. Prevention: walking skeleton first; run after every slice; verify every dependency exists and the version supports the API you used.
- **Hallucinated APIs.** Calling a framework or library function that does not exist in the installed version. Check against the installed version's documentation or source; run the code.
- **Frontend and backend disagree about the contract.** Field named `userId` on one side and `user_id` on the other; dates as strings vs. timestamps. Use a shared schema or generated types where possible; test the integration, not just each side.
- **UI-only authorization.** Hiding the delete button but leaving the endpoint open. Test by calling the endpoint as the wrong user.
- **Missing tenant filter.** One query that forgets `WHERE tenant_id = ?` leaks data across customers. Centralise the scoping.
- **Schema drift.** Using the ORM's auto-sync in development and migrations in production, so they diverge. Use migrations everywhere.
- **Mass assignment.** Passing the whole request body into a model update, letting users set `role = admin` or `owner_id`. Whitelist fields.
- **N+1 queries.** Lists that run a query per row. Fine with three seed rows, terrible with three thousand. Seed enough data to notice; eager-load relations.
- **Happy-path-only UI.** No loading, empty or error states, so the first network hiccup produces a blank screen or a silent failure.
- **Secrets in the repository** or in client-side bundles. Anything shipped to the browser is public. Keep secret keys server-side only.
- **Local-only assumptions.** Writing uploads to local disk, storing sessions in memory, relying on a single process — all break on most hosting platforms.
- **Scope creep during build.** Adding features not in the spec while core jobs are unfinished. Finish the slices; list ideas as next steps.
- **Gold-plated infrastructure.** Kubernetes, microservices and event sourcing for an internal tool with twenty users. Match infrastructure to the constraints you captured.
- **Over-generation.** Producing dozens of files in one pass without running anything. Generate a slice, run it, then continue.
- **A default "look".** Shipping the same palette, fonts and layout regardless of who the app is for. Derive visual direction from any brand guidance, existing design system or the users' context; when none exists, keep the UI neutral and accessible and say that visual design is open (see `ui-design-fundamentals`, `design-systems`).

## Quality bar and verification

The app is done when every item below is true, and you can say how you know:

- [ ] A clean setup from the README succeeds with only the documented steps.
- [ ] Migrations create the schema from empty; the seed populates it; both are repeatable.
- [ ] Every core job in the spec can be completed through the UI by the appropriate role.
- [ ] Every role has been logged in as and exercised.
- [ ] A user cannot read or modify another user's (or tenant's) data, proven by a test and by manual URL tampering.
- [ ] Invalid input is rejected with a clear message on the server, not only in the client.
- [ ] Loading, empty, error and success states exist for each screen that fetches or mutates data.
- [ ] The test suite passes, and covers the core jobs and the authorization boundaries.
- [ ] No unexplained errors or warnings in server logs or the browser console during the walkthrough.
- [ ] No secrets in the repository; every environment variable is documented.
- [ ] Production configuration is defined and differs from development in the ways that matter (debug off, secure cookies, no seed accounts).
- [ ] Keyboard navigation, labels and contrast are acceptable on the main flows (see `accessible-design`).
- [ ] The handover states clearly what was verified, what was not, and what was deferred.

"I wrote it" is not verification. "I ran these commands and completed these jobs as these users" is.

## Safety notes

- Never put real credentials, API keys or personal data into code, seeds, fixtures or commits. Use placeholders and the platform's secret store.
- Never run seeds, resets or destructive migrations against a database you have not confirmed is a local or disposable one.
- Ask before creating paid cloud resources, sending real email or SMS, charging real cards (use providers' test modes), or deploying.
- If the app handles personal, financial or health data, flag the regulatory implications (data retention, consent, encryption at rest, access logging) to the user rather than silently deciding.
- Run a dependency audit before handover and note any known-vulnerable packages (see `dependency-management`).

## Related skills

- `project-scaffolding` for the empty-repo-to-skeleton step.
- `database-design`, `database-migrations`, `sql-and-queries` for the data spine.
- `api-design`, `backend-development`, `frontend-development` for each layer.
- `authentication-and-authorization`, `secure-coding` for the security-critical slices.
- `testing-strategy`, `end-to-end-testing` for verification depth.
- `ci-cd-pipelines`, `containerization`, `cloud-architecture`, `observability` for the deploy path.
- `mvp-prototyping` when the real question is "should this exist", not "build it properly".
