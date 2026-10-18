---
name: software-architecture
description: >-
  Structure a codebase so it stays understandable and changeable: modules and
  boundaries, layering, dependency direction, coupling and cohesion, monolith
  vs. modular monolith vs. services, when to apply (and when to avoid) common
  patterns, and how to evolve an architecture incrementally. Use when starting
  a new codebase, deciding where code should live, splitting or merging
  modules or services, untangling a "big ball of mud", introducing a pattern
  (hexagonal, CQRS, events, plugins), or when a change keeps touching too many
  files. For distributed scale and reliability design use system-design; for
  reviewing an existing design use architecture-review.
metadata:
  category: development
  related: system-design, api-design, backend-development, refactoring, legacy-modernization, technical-decision-making, architecture-review, explore-codebase, database-design
---

# Software Architecture

Architecture is the set of decisions that are expensive to change later: how the code is divided, which parts may depend on which, where data and behaviour live, and how the pieces communicate. Good architecture is not a diagram or a pattern name. It is the property that **the changes the business actually needs are cheap, local, and safe to make**.

## Scope

This skill covers the *internal* structure of a software system: modules, layers, boundaries, dependencies, and the choice of deployment units (one process or several). It does not cover:

- Scaling, replication, caching, and failure handling across machines — see `system-design`.
- The shape of an interface between components — see `api-design`.
- Restructuring code without changing behaviour, step by step — see `refactoring`.
- Migrating an old system to a new one — see `legacy-modernization`.
- Evaluating someone else's architecture — see `architecture-review`.
- Framing and recording a contested decision — see `technical-decision-making`.

## Core principles

### 1. Optimise for the changes you expect

Every structure makes some changes cheap and others expensive. A layered "controllers / services / repositories" split makes it cheap to swap the database and expensive to add a feature (one feature touches every layer). A feature-sliced layout makes features cheap and cross-cutting changes expensive. There is no universally good structure; there is only a structure that fits the **axis of change** of this system.

So before arranging anything, ask: *what will change most often over the next year?* New features in a growing product? New integrations? New tenants with custom rules? Regulatory changes to one calculation? Arrange the code so the most frequent change touches the fewest modules.

### 2. Cohesion high, coupling low — and know what those words mean

- **Cohesion**: things in a module change for the same reason. A module named `utils` has near-zero cohesion; a module named `pricing` that holds everything about computing a price has high cohesion.
- **Coupling**: how much one module must know about another to work. Coupling has *kinds*, from worst to least bad:
  1. Shared mutable state (global variables, a shared database table written by two modules).
  2. Knowledge of internal structure (reaching into another module's private classes or tables).
  3. Temporal coupling (A must be called before B, but nothing enforces it).
  4. Data-shape coupling (both depend on the same large data structure).
  5. Contract coupling through a small, explicit interface.

You will never reach zero coupling; the goal is to make every coupling **explicit, narrow, and in one direction**. The "why": change propagates along coupling. Every hidden coupling is a place a change will break something nobody expected.

### 3. Dependencies point toward stability

A module should depend only on modules that change *less* often than it does. Business rules change less often than UI frameworks, delivery mechanisms, and vendors, so the core domain should not import the web framework, the ORM, or an SDK. Outer layers depend inward; the inner core depends on abstractions it owns.

This is the shared idea behind hexagonal / ports-and-adapters, onion, and "clean" architectures. You do not need the full ceremony of any of them to benefit; you need the dependency rule. A quick test: *can I unit-test the core business rule without starting a web server, a database, or a network connection?* If not, the core depends on something volatile.

### 4. Boundaries are where you pay for decoupling — draw few, draw them well

Every boundary (an interface, a module API, a network hop) has a cost: indirection, translation code, harder navigation, and for network boundaries, latency and partial failure. Boundaries pay off where they separate things that change independently, are owned by different people, or need to be swapped. They are pure cost elsewhere.

Heuristic: a boundary is justified when at least one of these is true:
- Two sides change at clearly different rates or for different reasons.
- Two sides are owned by different teams.
- One side has a realistic chance of being replaced (a vendor, a storage engine) — "realistic" means someone can name the scenario.
- One side needs to be tested in isolation and the other is slow or non-deterministic.

### 5. Make the architecture visible in the code

An architecture that lives only in a wiki diagram decays within months. Encode it: directory structure that mirrors the modules, public/private visibility (package-private, `internal/`, explicit `__all__` or index exports), and where available, automated dependency rules (e.g. import-linting tools, ArchUnit-style tests, module systems, build-graph constraints). The "why": rules that are not checked are suggestions, and suggestions lose to deadlines.

### 6. Defer decisions that are cheap to defer, make early the ones that are not

Some decisions are cheap to change later (which logging library, which HTTP client). Others become load-bearing quickly (the primary data model, the unit of deployment, the identity scheme, sync vs. async communication between core components). Spend design effort in proportion to reversal cost. For reversible decisions, pick the simplest option and move on.

## Discovering the existing architecture first

Never impose a structure on an existing codebase before you understand the one it already has. Do this before proposing anything:

1. **Read the top-level layout and build configuration.** Workspaces, packages, modules, solution files, and dependency manifests reveal the intended units far better than a README.
2. **Find the entry points**: HTTP routers, CLI mains, job schedulers, message consumers. Trace one real request end to end. Note every layer it passes through.
3. **Map dependencies between top-level modules.** If you can run a tool that prints an import graph, do; otherwise grep for import statements across module directories. Look for cycles and for "everything imports X" hubs.
4. **Look at recent change history** if version control is available. Files that always change together reveal the real modules, which may differ from the directory structure. Files that change in nearly every commit are hotspots.
5. **Find the written conventions**: architecture decision records, CONTRIBUTING files, lint configs with import rules, code-owner files.
6. **Identify the dominant style** (layered, feature-sliced, hexagonal, framework-default MVC, plugin-based) and follow it for new code, even if you would have chosen differently. Consistency beats local optimality: a codebase with two competing structures is harder to work in than one with a mediocre consistent structure.

If the existing structure is genuinely harmful, propose a change explicitly, with a migration path, rather than starting a second style silently in the files you touch.

## Process for designing or changing structure

### Step 1: Understand the forces

Collect, briefly:
- **Domain**: what are the core concepts and rules? Which parts are the business's differentiator and which are generic (auth, billing, notifications)?
- **Change**: what kind of change is most frequent? What is expected to be added?
- **Team**: how many people, how many teams, how independently must they ship?
- **Quality attributes** that actually matter here: latency, throughput, availability, auditability, data residency, offline support, extensibility by third parties. Ask the user which ones are real requirements; do not assume all of them.
- **Constraints**: language, platform, existing infrastructure, compliance, budget.

If the user cannot answer some of these, state the assumptions you are making and design so they are easy to revisit.

### Step 2: Find the modules by grouping behaviour and data

Good modules usually align with **business capabilities** (ordering, inventory, invoicing, identity) rather than technical roles (controllers, models, helpers). Technique:

1. List the main nouns (entities) and verbs (use cases).
2. Group use cases that read and write the same data and are governed by the same rules.
3. Where the same word means different things to different groups ("account" in billing vs. "account" in identity), that is a natural boundary. Give each side its own model rather than one shared god-object.
4. Check each candidate module: can you describe what it does in one sentence without "and"? Does it own its data, or does it need another module's tables?

**Data ownership is the strongest boundary signal.** If two modules both write the same table, they are one module or the boundary is wrong.

### Step 3: Define module interfaces

For each module, decide what it exposes: a small set of operations and data types. Everything else is private. Prefer:
- Interfaces expressed in domain terms (`reserveStock(orderId, items)`) over generic data access (`updateRow(table, id, fields)`).
- Passing identifiers or small value objects across boundaries rather than rich mutable entities, which leak internal structure.
- One direction of calls between any two modules. If A calls B and B needs to tell A something, use a callback interface owned by B, an event, or move the logic.

### Step 4: Choose the layering inside modules

Inside a module, separate at least:
- **Domain logic**: rules and invariants. Pure where possible.
- **Application / use-case orchestration**: transactions, calling the domain, calling ports.
- **Adapters**: HTTP handlers, database access, message consumers, external clients.

Smaller modules can collapse application and domain. Very simple CRUD modules can be little more than an adapter over a table — do not build four layers for a settings page. Match the depth of layering to the complexity of the rules, not to a template.

### Step 5: Choose the deployment shape

See the decision table below. Default to one deployable unit with strong internal module boundaries unless there is a specific force that requires separate deployment.

### Step 6: Encode and verify

Create the directory structure, visibility rules, and if possible a dependency check that fails the build on violations. Write a short decision record of *why* the structure is as it is (see `technical-decision-making`), because the reasons are what future maintainers need when the forces change.

### Step 7: Plan evolution

Note which decisions you expect to revisit and what signal would trigger it ("split notifications into its own service if its deploy cadence diverges or its load starts affecting checkout latency").

## Decision guidance

### Monolith, modular monolith, or services

| Shape | Choose when | Costs you accept |
|---|---|---|
| Simple monolith (one unit, light internal structure) | Small team (≤ ~5 devs), early product, domain still being discovered, low traffic | Structure can erode; needs discipline as it grows |
| Modular monolith (one unit, enforced internal boundaries, module-owned data) | Most products with 1–5 teams; domain reasonably understood; you want the option to split later | Requires boundary enforcement tooling and review discipline |
| A few coarse services | Clear parts with very different scaling, availability, security, or technology needs; teams that must deploy independently | Network calls, distributed failure, data consistency across services, more ops |
| Many fine-grained microservices | Large organisation (many teams), mature platform (CI/CD, observability, service discovery, on-call), strong need for independent deploys | High operational overhead, distributed debugging, versioning between services, eventual consistency everywhere |

Points experts largely agree on:
- **Services do not fix bad module boundaries; they freeze them.** If you cannot draw clean boundaries inside one process, splitting into services gives you a distributed big ball of mud, which is strictly worse.
- **The main legitimate driver for services is organisational**: independent teams needing independent deploys. Secondary drivers are divergent runtime needs (one component needs GPUs, one must be isolated for security or compliance, one has 100× the load).
- **A shared database between services** removes most of the benefit of services. If you split, split the data too, or accept that you have a distributed monolith.

Where experts disagree: whether to start with services in a greenfield project if you "know" you will need them. The argument for: avoids a painful later split. The argument against: early boundaries are usually wrong, and moving a boundary inside a monolith is a refactor while moving it between services is a migration. Unless the forces are already present on day one, favour the modular monolith.

### Layered vs. feature-sliced organisation

| | Layered (by technical role) | Feature/capability-sliced |
|---|---|---|
| Cheap change | Swap a technical layer | Add or change a feature |
| Navigation | Easy to find "all controllers" | Easy to find "everything about invoices" |
| Risk | Features smeared across layers; layers become dumping grounds | Duplication of technical plumbing across slices |
| Fits | Small apps, framework-default projects, teams used to it | Growing products, multiple teams, domain-heavy code |

A common, sensible hybrid: slice by capability at the top level, layer inside each slice.

### Synchronous calls vs. events between modules

- **Direct call** when the caller needs the result now, the operation must succeed or fail together, and there is one obvious owner.
- **Event / message** when the caller does not need the result, several independent consumers react, or you want to decouple availability (the producer should not fail because the consumer is down).
- Events hide the control flow: "what happens when an order is placed?" can no longer be answered by reading one function. Use them where the decoupling pays for that, not everywhere. Document who publishes and who consumes each event.

### Where does this new piece of code go?

The most frequent architectural decision is the smallest one: placing a new function, class, or file. Ask, in order:

1. Which module **owns the data** this code reads or writes most? Put it there.
2. If it coordinates several modules, it belongs to the use-case / application layer of the module that initiates the flow — not in a new "shared" place.
3. If it is a pure, domain-free utility (string formatting, retry helper), put it in a foundational package with no dependencies on business modules — and only if at least two modules need it now.
4. If none of these fit, the module boundaries may be missing a concept. Consider whether a new module is warranted before adding to a dumping ground.
5. Match the existing project's placement for similar code; consistency is what lets the next reader find it.

### Shared library vs. duplication

Sharing code across modules creates coupling: a change to the shared code affects everyone. Share when the code represents **the same concept that must stay identical** (a money type, a date-handling rule, a protocol). Duplicate when the code is **coincidentally similar** today but belongs to concepts that will evolve independently. "Don't repeat yourself" is about knowledge, not characters. Three similar-looking functions in three modules are often fine.

## Patterns and when NOT to use them

Use a pattern when you can name the force it resolves in *this* codebase. If the only justification is "it's best practice", don't.

| Pattern | Resolves | Do not use when |
|---|---|---|
| Ports and adapters / hexagonal | Core logic must be testable and independent of I/O and vendors | The app is thin CRUD over a database with few rules; the indirection costs more than it saves |
| Repository | Domain code should not know storage details; you need in-memory fakes for tests | It merely wraps an ORM that already is a repository, adding a pass-through layer |
| Dependency injection (container or manual) | Swapping implementations, testing with fakes, managing lifecycles | A small program where passing arguments explicitly is clearer. Prefer constructor injection by hand before reaching for a container |
| CQRS (separate read and write models) | Read and write needs diverge sharply: complex validation on write, many denormalised views on read | Reads and writes look alike; it doubles the model for no gain |
| Event sourcing | Full audit history is a requirement; need to rebuild state as of any time; domain is naturally event-shaped | Ordinary CRUD; teams unfamiliar with it; heavy need for ad hoc queries over current state. Very hard to retrofit out of |
| Domain events (in-process) | Decoupling side effects (send email, update stats) from core transactions | One consumer that could simply be called directly |
| Plugin / extension architecture | Third parties or many variants must add behaviour without changing the core | Only the core team ever extends it; YAGNI |
| Microkernel / pipeline | Processing steps that are composed differently per case | The order and set of steps is fixed |
| Strategy / polymorphism instead of conditionals | Variation that grows (new providers, new rule sets) | Two cases that are unlikely to grow — an `if` is clearer |
| Generic "base" classes / frameworks inside the app | Real repeated structure across many modules | Fewer than three concrete uses; you are guessing the abstraction |

The general failure: **speculative generality** — abstractions built for variation that never arrives. The cost is paid every day by every reader; the benefit may never come. The opposite failure — no abstraction where variation already exists, so every change edits a growing switch statement — is easier to fix later, which is why erring slightly toward concrete code is usually the better default.

## Evolving architecture

Architecture is never finished. Treat it as something you steer:

- **Fitness functions**: automated checks that protect important properties — dependency rules, max module size, no cycles, startup time, p95 latency of a key path. They turn architectural intent into failing builds.
- **Strangler approach**: to replace a part, route traffic or calls through a seam, build the new part behind it, and move callers over incrementally. Never plan a big-bang rewrite of a working system without an exceptionally good reason (see `legacy-modernization`).
- **Extract module before extracting service**: first make the candidate a clean module in-process with its own data and narrow interface. Run it that way. Only then, if the forces still justify it, move it out of process. The in-process step reveals hidden coupling cheaply.
- **Merge modules that always change together.** If two modules co-change in most commits, the boundary is in the wrong place. Merging is a legitimate architectural improvement.
- **Record decisions with context.** A decision record that says "we chose X because of forces A and B" lets a future team know when to revisit it — when A and B no longer hold.

## Measuring structural health

Numbers do not replace judgment, but they make vague complaints concrete and let you track whether a change helped. Useful signals, with rough thresholds to treat as prompts for a closer look rather than hard limits:

| Signal | How to get it | Look closer when |
|---|---|---|
| Import cycles between top-level modules | Import-graph tool, or grep imports and sketch the graph | Any cycle at module level |
| Fan-in to a single module | Count modules importing it | A non-foundational module (not a money type or logging) is imported by most others |
| Co-change rate | Version history: how often files in A and B change in the same commit | Two "separate" modules co-change in a majority of commits |
| Change hotspots | Commit counts per file over the last few months | A handful of files take a large share of all changes, especially if they are also long |
| File / class size | Line counts | A single unit of thousands of lines that changes often — size alone is fine for stable code |
| Test setup weight | Read test fixtures | Unit-testing one rule requires a database, network, or dozens of collaborators |
| Lead time for a typical feature | Ask the team, or look at PR sizes | Small product changes routinely produce PRs spanning many modules |

Combine signals. A large file that never changes is not a problem; a medium file that changes in every PR and has high fan-in is.

## Architecture in different kinds of software

The principles are the same; the forces differ.

- **Libraries and SDKs**: the public API *is* the architecture. Minimise exposed surface, because every public symbol is a compatibility promise. Keep internals in clearly private packages. Avoid pulling in heavy dependencies that become your users' dependencies.
- **Web backends**: the main risk is business logic leaking into handlers and ORM models. Keep the request/response layer thin (see `backend-development`).
- **Client and frontend apps**: the axis of change is usually screens and features; state management and data fetching are the main coupling risks (see `frontend-development`).
- **Data pipelines**: structure around stages with explicit, versioned data contracts between them; each stage should be re-runnable on its own (see `etl-pipelines`).
- **CLIs and tools**: separate argument parsing and output formatting from the operations themselves, so operations can be tested and reused (see `cli-development`).
- **Embedded and resource-constrained systems**: indirection has real runtime cost; prefer compile-time composition over runtime abstraction, and keep hardware access behind a thin layer for testability.
- **Plugin hosts and platforms**: the extension contract is the hardest thing to change. Version it explicitly and design it narrower than you think you need.

## Communicating architecture

When you propose or document a structure, make it usable by someone who has not seen the code:

- Describe it at two or three levels at most: the system in its environment, the main deployable units, and the modules inside the one being discussed. Deeper levels belong in the code.
- For each module, give its responsibility, the data it owns, and what it may depend on. That is more useful than a box-and-line diagram whose lines have no defined meaning.
- If you draw diagrams, label what an arrow means (calls, depends on, sends data to). Ambiguous arrows cause most diagram misunderstandings.
- State the forces and the decisions alongside the structure. Structure without reasons cannot be safely changed.
- Mark what is current and what is target state; mixing them misleads readers about what exists.

## Worked reasoning example

*Illustrative.* A team of four has a single web application. Every new "report" feature requires edits to the controller layer, a service class with 3,000 lines, the ORM models, and the templates. Someone proposes moving to microservices.

Reasoning:
1. The pain is that one feature touches many files — a cohesion problem along the feature axis, not a deployment problem.
2. Four developers do not need independent deploys; microservices would add network calls and ops overhead without addressing the cohesion issue.
3. Better: reorganise into capability modules (`reporting`, `accounts`, `billing`), each with its own handlers, logic, and data access. Split the 3,000-line service along those lines.
4. Add an import rule that `reporting` may read from `accounts` only through its public interface.
5. Revisit deployment shape only if, e.g., report generation's heavy load starts degrading interactive requests — and then the first step might be moving report generation to a background worker in the same codebase, not a new service.

## Pitfalls and anti-patterns

- **Big ball of mud**: no discernible structure; everything imports everything. Recognise it by cycles in the import graph and by "small" changes requiring edits in many directories. Fix incrementally by carving out one cohesive module at a time.
- **Distributed monolith**: services that must be deployed together, share a database, or call each other synchronously in long chains. All the costs of services, none of the benefits.
- **Anaemic layers**: a "service layer" that only forwards calls to the repository, and "domain objects" that are data bags while all logic lives in procedures elsewhere. Not wrong for simple CRUD, but a smell if the domain is rich.
- **God module / god object**: a `core`, `common`, `shared`, or `manager` that everything depends on and that changes constantly. Split it by reason-to-change.
- **Leaky boundaries**: one module returns its ORM entities to another, which then lazily loads relations — the second module now depends on the first's schema.
- **Architecture by framework default**: accepting the framework's folder layout as the architecture for a complex domain. Fine for small apps; becomes a constraint as the domain grows.
- **Resume-driven design**: choosing patterns or service counts because they are fashionable. Ask: what force does this resolve here?
- **Premature abstraction**: interfaces with a single implementation and no test fake, "for future flexibility". Exception: a port at a true I/O boundary, which is cheap and aids testing.
- **Circular dependencies between modules**: they make modules impossible to understand or test alone. Break them by moving the shared concept down, inverting one dependency with an interface, or merging the modules.
- **Diagram-only architecture**: rules that exist in documentation but not in tooling. They will be violated.
- **Big-bang restructuring**: moving every file in one change. Hard to review, conflicts with all in-flight work, and hard to roll back. Restructure in small, behaviour-preserving steps.

## Safety and practical notes

- Restructuring touches many files. Before moving code, make sure tests exist for the behaviour you are preserving (see `refactoring`, `testing-strategy`), and move in small commits.
- Changing deployment shape (splitting or merging services) affects production operations: deploy pipelines, monitoring, on-call, data migration. Do not do this on your own initiative; propose it with a plan and get agreement.
- Moving data ownership between modules or services usually requires a data migration; treat it with the care described in `database-migrations`.

## Quality bar and verification

Before declaring a structural change or proposal done, check:

- [ ] You can state the main axis of change, and the structure makes that change touch few modules. Try it: walk through two or three realistic upcoming changes and list the files each would touch.
- [ ] Every module has a one-sentence purpose without "and", a clear owner of its data, and a small public interface.
- [ ] The dependency graph between modules has no cycles and points from volatile to stable. If tooling is available, run an import-graph or dependency check; otherwise grep imports across module boundaries.
- [ ] The core business rules can be tested without real I/O.
- [ ] Every boundary and pattern introduced has a named force that justifies it.
- [ ] New code follows the project's existing conventions, or the deviation is explicit and agreed.
- [ ] Rules are enforced by tooling where possible, not only described.
- [ ] The reasons for key decisions are recorded somewhere the team will find them.
- [ ] The existing test suite still passes after any restructuring, and behaviour is unchanged.

If you could not run tools, say which of these checks you performed by reading and which remain for the user to run.
