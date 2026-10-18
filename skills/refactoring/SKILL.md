---
name: refactoring
description: >-
  Change the structure of existing code without changing its behaviour:
  establishing a safety net, moving in small verified steps, recognising code
  smells, applying common refactorings (extract, inline, rename, move,
  replace conditional, introduce parameter object), planning large-scale
  refactors with branch-by-abstraction, expand-contract and strangler-fig
  patterns, and judging when not to refactor. Use when code is hard to read
  or change, before adding a feature to messy code, when cleaning up after
  getting tests green, when asked to "clean up", "simplify", "restructure",
  or "pay down tech debt". For replacing whole legacy systems use
  legacy-modernization; for reviewing others' code use code-review.
metadata:
  category: development
  related: test-driven-development, testing-strategy, legacy-modernization, software-architecture, code-review, database-migrations, git-workflow, performance-optimization
---

# Refactoring

Refactoring is a disciplined change of a program's internal structure that leaves its observable behaviour unchanged. The discipline is the point: by moving in small steps that each preserve behaviour, you can make large structural improvements while keeping the system working at every moment. "Refactoring" that changes behaviour, or that leaves the code broken for hours, is rewriting — sometimes justified, but a different activity with different risks.

## Scope

Covers: behaviour-preserving restructuring at every scale, from renaming a variable to migrating an architecture incrementally; the safety nets that make it safe; smells that indicate where to refactor; and when to stop.

Neighbours:

- Replacing or modernising whole legacy systems, platform migrations → `legacy-modernization`.
- Writing tests first, characterization tests → `test-driven-development`.
- Schema changes in live databases → `database-migrations`.
- Larger architectural direction → `software-architecture`.
- Making code faster (which often *does* change structure but is driven by measurement) → `performance-optimization`.

## Core principles

1. **Behaviour preservation is the invariant.** Every step must leave the program doing exactly what it did before, as observed by its callers and users. That is what lets you stop at any point, ship any intermediate state, and isolate any breakage to the last step. Define "observable" for the context: for a library, the public API and its documented behaviour; for a service, its responses and side effects.

2. **Never refactor and change behaviour in the same step.** Separate them in time and ideally in commits ("two hats"). When a change both restructures and alters behaviour, reviewers cannot see the behaviour change, and if something breaks you cannot tell which part caused it.

3. **Small steps, verified each time.** Run tests after every step. Small steps feel slower but are faster overall: when a test fails you know the cause is in the last few lines, and you can undo instead of debugging.

4. **A safety net first.** Refactoring without tests (or equivalent verification) is guessing. If the code lacks tests, add characterization tests over the area you'll touch before restructuring, or restrict yourself to refactorings your tools perform provably safely.

5. **Refactor toward a purpose.** "Make the change easy, then make the easy change." The best refactoring is in service of an imminent change — a feature, a fix, comprehension. Refactoring with no destination tends to churn code to suit taste and creates review burden without payoff.

6. **Respect the codebase's conventions.** Refactoring toward your preferred style in someone else's codebase is not improvement; it's inconsistency. Improve within the established idioms unless the user agrees to change them.

## Process

### 1. Clarify the goal and boundary

- What change are you trying to enable, or what comprehension problem are you solving?
- What is the boundary — which modules, which public interfaces must not change?
- Is this preparatory refactoring for a feature (do it first, separately), clean-up after a feature (do it once tests are green), or a dedicated effort (needs agreement on scope)?

If the user asked for a feature, don't embark on a broad refactor unasked. Do the minimal preparatory refactoring needed, mention further opportunities, and let them decide.

### 2. Establish the safety net

- Run the existing tests; confirm they pass *before* you start. A refactor started on a red suite can't distinguish your breakage from existing failures.
- Check coverage over the code you'll touch. If thin, add tests through the public interface (see characterization tests in `test-driven-development`).
- Other nets, in decreasing strength: a type checker/compiler (catches many mistakes in rename/move/signature changes); automated refactoring tools in an IDE or language server (rename, extract, inline, move — these are designed to preserve behaviour, though dynamic features like reflection, string-based lookups, and templating can escape them); golden-master comparisons of output; careful manual review.
- For dynamic languages, be extra cautious about names referenced as strings (serialisation keys, ORM fields, routing, dependency injection, templates, configuration). Search for them textually, not just via the symbol index.

### 3. Take small, behaviour-preserving steps

- One refactoring at a time. Run the tests. Commit when green if the step is meaningful (small commits make bisection and review easy).
- If tests fail, **undo** rather than fixing forward, then take a smaller step.
- Prefer **parallel change** for anything with callers: add the new form alongside the old, migrate callers one by one, remove the old form when unused. This keeps every intermediate state working.

### 4. Review the result

- Diff the whole change. Look for accidental behaviour changes: altered evaluation order with side effects, changed exception types, changed default values, changed iteration order, lost null handling, changed rounding, logging changes that break downstream parsers.
- Ensure the result is actually better by the goal you set — clearer, easier to change in the intended direction — not merely different.

### 5. Then make the behaviour change

With the structure prepared, the feature or fix becomes a small, clearly visible change in a separate commit.

## Code smells: signals, not rules

A smell is a symptom that *may* indicate a design problem. It is a prompt to look, not an automatic trigger to change.

| Smell | Signals | Typical refactorings |
|---|---|---|
| **Long function** | Needs comments to explain sections; scrolls; many local variables | Extract function (one per commented section), replace temp with query, decompose conditional |
| **Large class/module** | Many fields used by disjoint subsets of methods; name ends in Manager/Util/Helper | Extract class along the field/method clusters; move function |
| **Long parameter list** | 4+ parameters, especially several of the same type; boolean flags | Introduce parameter object; preserve whole object; split function per flag value |
| **Duplicated code** | Same logic in several places, often slightly varied | Extract function; pull up to shared location; but see "wrong abstraction" below |
| **Divergent change** | One module changes for several unrelated reasons | Split by reason to change |
| **Shotgun surgery** | One logical change requires edits in many places | Move the scattered pieces together; inline small classes |
| **Feature envy** | A function uses another object's data more than its own | Move function to where the data lives |
| **Data clumps** | The same group of values travels together | Introduce a type/record for the group |
| **Primitive obsession** | Strings/ints for domain concepts (money, email, IDs, units) | Introduce value type; enums for closed sets |
| **Repeated switch/if-chains on type** | The same type check in many places | Replace conditional with polymorphism, or a lookup table/map of handlers |
| **Speculative generality** | Hooks, abstract bases, parameters with one implementation or caller | Inline, collapse hierarchy, remove parameter |
| **Message chains** | `a.b().c().d()` | Hide delegate; move function |
| **Mutable shared data** | Global or widely shared mutable state | Encapsulate variable; make immutable; pass explicitly |
| **Dead code** | Unused functions, branches, flags, parameters | Delete (version control remembers it) |
| **Comments explaining what** | Comments narrating obscure code | Rename and extract until the code says it; keep comments that explain *why* |
| **Nested conditionals** | Arrow-shaped code | Guard clauses (early return), decompose conditional, consolidate conditions |

**Duplication caution.** Not all similar-looking code is duplication of the same *knowledge*. Two functions that look alike today but change for different reasons should stay separate; merging them creates a "wrong abstraction" sprouting flags and special cases. A useful threshold: tolerate the second occurrence; consider extracting at the third, once you can see what really varies. If an existing abstraction has become a tangle of parameters and conditionals, inlining it back into its callers and re-extracting is a legitimate refactoring.

## Common refactorings (language-agnostic)

These are the workhorses. Each has a mechanical recipe; IDEs automate many of them.

- **Rename** (variable, function, class, module). The cheapest, most valuable refactoring: a good name removes the need for a comment. For public APIs, rename via parallel change (new name, deprecate old, migrate, remove).
- **Extract function/method.** Move a coherent fragment into a named function. Name it for *what* it does or *why*, not *how*. Pass in what it reads; return what it computes.
- **Inline function/variable.** The reverse — when the indirection adds nothing, or as a step before re-extracting differently.
- **Extract variable / introduce explaining variable.** Name a complex expression: `is_eligible = age >= 18 and not suspended`.
- **Change function signature.** Add, remove, reorder parameters. For widely-called functions: create the new signature, have the old one delegate to it, migrate callers, delete the old.
- **Introduce parameter object / value type.** Replace clumps of primitives with a type that can carry validation and behaviour.
- **Move function/field.** Put behaviour next to the data it uses.
- **Extract class / split module.** Separate responsibilities along clusters of data and methods.
- **Replace conditional with polymorphism or a dispatch table.** When the same type-based branching recurs.
- **Decompose conditional / guard clauses.** Name the condition and branches; return early for special cases.
- **Replace magic literal with named constant.**
- **Encapsulate variable/collection.** Route access through functions so you can later change representation or add invariants.
- **Separate query from modifier.** A function that both returns a value and mutates state is hard to reason about; split it.
- **Split phase.** Separate a computation into stages with an explicit intermediate data structure (parse → validate → transform → render). Excellent for untangling long procedures.
- **Replace loop with pipeline** (map/filter/reduce) where the project's idioms favour it — and leave loops where they're clearer or faster.
- **Pure core, imperative shell.** Extract decision logic from I/O so the logic can be tested without mocks; the I/O becomes a thin wrapper.

Short illustration of "decompose conditional" (pseudocode, any language):

```
# before
if date < summer_start or date > summer_end:
    charge = qty * winter_rate + winter_fee
else:
    charge = qty * summer_rate

# after
charge = winter_charge(qty) if not is_summer(date) else summer_charge(qty)
```

The behaviour is identical; the business concept ("summer pricing") now has a name and a single place to change.

## Mechanics of a few key refactorings

Mechanical recipes matter because they keep each step behaviour-preserving even when you are tired or the code is unfamiliar. Automated tools perform many of these; when doing them by hand, follow the steps.

**Extract function**

1. Pick a fragment with a single purpose; name the purpose.
2. Identify variables the fragment reads (become parameters) and writes (become return values). If it writes several, consider extracting a smaller piece first or returning a small record.
3. Create the new function, copy the fragment, adjust variable references.
4. Replace the original fragment with a call. Run tests.
5. Look for other places with the same fragment and replace them too, if they truly represent the same knowledge.

**Change function signature (widely used function)**

1. If the change is simple and all callers are in your codebase with good tooling, use the automated refactoring and run tests.
2. Otherwise: create a new function with the new signature containing the body; make the old function delegate to the new one.
3. Run tests. Migrate callers one at a time (or one module at a time), running tests and committing as you go.
4. When no callers remain, delete the old function. For public libraries, deprecate first and remove in a later major version.

**Move function between modules**

1. Check what the function uses from its current context; those become parameters or move with it.
2. Copy the function to the target; adjust it to the new context.
3. Make the original delegate to the new location. Run tests.
4. Update callers to use the new location; remove the delegating original once unused.
5. Watch for import cycles introduced by the move — a cycle is a sign the function belongs elsewhere or the modules need splitting.

**Replace conditional with polymorphism / dispatch table**

1. Ensure the branching is on a type-like value (a kind, status, or class).
2. Create the variants (subtypes, strategy objects, or a map from key to handler). Start with one variant; move its branch body into it.
3. Route that case through the new structure; run tests. Repeat per branch.
4. Remove the original conditional when all branches are moved. Keep a clear default/unknown case behaviour identical to the old `else`.

**Introduce value type for a primitive**

1. Create a small type wrapping the primitive, initially with no behaviour.
2. Change one producer to create the type and one consumer to accept it; run tests; spread outward.
3. Move validation and related behaviour (formatting, comparison, arithmetic with units) into the type.
4. Watch serialisation boundaries: the wire and storage format usually must remain the primitive.

## Refactoring with no tests

Sometimes you must improve code before tests are possible — for example, to break a dependency so that tests *can* be written. Restrict yourself to moves that are safe by construction:

- Automated refactorings by a tool that understands the language (rename, extract, inline, move) in statically typed code.
- Lean on the compiler: change a signature and let compile errors enumerate every call site.
- **Preserve signatures** when breaking dependencies: add a parameter with a default that preserves existing behaviour; extract an interface from a concrete class without changing callers; wrap a global call in a function you can later substitute.
- Make one move, review the diff carefully, run whatever checks exist (build, type check, lint, a smoke run), and commit.
- As soon as a seam exists, write characterization tests (see `test-driven-development`) and continue with the normal discipline.

In dynamic languages without these aids, rely on textual search for all references, smaller steps, and a golden-master comparison of outputs over a broad input set.

## Choosing where to refactor

Refactoring budget is limited; spend it where it returns most.

- **Hotspots**: files that change often *and* are complex. Version control history (commits per file over the last months) multiplied by a complexity measure (length, nesting, cyclomatic complexity) produces a short list. Code that is ugly but stable rarely deserves attention.
- **Change coupling**: files that always change together but live apart suggest a misplaced boundary.
- **Defect density**: modules with recurring bugs usually have a structural cause.
- **Upcoming work**: the code the next features will touch.
- **Onboarding pain**: code that every new team member finds confusing.

Present the candidates and the expected benefit to the user rather than starting a large clean-up unasked.

## A worked example at module scale (illustrative)

A 900-line `ReportGenerator` mixes querying the database, computing aggregates, and rendering HTML and CSV. A new PDF format is requested.

1. *Goal:* make adding a format a matter of writing one renderer.
2. *Safety net:* there are few tests. Write golden-master tests: for six representative report configurations (including empty data and a large dataset), capture the HTML and CSV output to files and assert equality.
3. *Split phase:* extract the query section into `load_report_data(params)` returning a plain data structure. Run golden tests. Extract aggregation into `compute_summary(data)`. Run tests. The renderer now receives `(data, summary)`.
4. *Separate renderers:* extract `render_html(data, summary)` and `render_csv(data, summary)`; the old method becomes a dispatcher on format. Run tests after each extraction.
5. *Introduce an interface:* a renderer map from format name to function. The dispatcher becomes a lookup.
6. *Now the behaviour change:* add `render_pdf` and its tests in a separate commit. The feature diff is small and easy to review.
7. *Follow-up:* now that `compute_summary` is pure, add unit tests for its edge cases, and replace some golden tests with focused ones.

Every intermediate commit produced byte-identical HTML and CSV, verified by the golden tests.

## Reviewing a refactoring

When reviewing (your own or someone else's) refactor:

- Confirm the tests weren't changed in ways that weaken them; in a pure refactor, test *assertions* should mostly be unchanged (test structure may change if APIs moved).
- Read the diff commit by commit if it was built in small steps; mechanical steps are quick to verify.
- Look for semantic traps: changed exception types, short-circuit evaluation changes, side effects reordered, mutable default arguments, changed equality or hashing, lost thread-safety.
- Ask whether the stated goal was reached and whether old paths were actually removed.

## Large-scale refactoring

Refactors that span many files, teams, or weeks need different tactics, because you cannot hold the system broken while you work, and long-lived branches diverge and become merge nightmares.

### Principles at scale

- **Keep main shippable.** Every merge leaves the system working. Prefer many small merges to one large branch.
- **Make the old and new coexist.** Every large technique below is a variation on this.
- **Measure progress** (count remaining old-style call sites, percentage of traffic on the new path) so the effort can be paused and resumed without losing its state.
- **Plan the finish.** The most common failure of large refactors is stopping at 80%, leaving two ways of doing everything — worse than either alone. Budget for the tail and the removal of the old path.

### Techniques

- **Parallel change / expand–migrate–contract.** Expand: add the new interface alongside the old. Migrate: move callers over incrementally. Contract: remove the old. Works for function signatures, APIs, configuration, and database schemas (for schema-specific procedures see `database-migrations`).
- **Branch by abstraction.** Introduce an abstraction (interface) over the component to be replaced; make all callers use the abstraction; build the new implementation behind it; switch over (possibly per caller or via a flag); remove the old implementation and, if no longer useful, the abstraction.
- **Strangler fig.** For replacing a subsystem or service: route requests through a facade; implement functionality piece by piece in the new system; redirect each piece's traffic as it's ready; the old system shrinks until it can be removed. Good for UI rewrites (route by page), APIs (route by endpoint), and monolith decomposition. See `legacy-modernization`.
- **Feature flags / toggles** to switch implementations at runtime, enabling gradual rollout and instant rollback. Remove flags once the switch is complete — stale flags are their own tech debt.
- **Dark launching / shadow comparison.** Run the new implementation alongside the old on real inputs, compare outputs, and log mismatches without affecting users. Powerful for verifying behaviour preservation of rewrites of calculations, queries, or parsers.
- **Automated codemods.** For mechanical changes across hundreds of files (API renames, import moves), write a transformation using an AST-based tool rather than regex — it respects syntax and avoids changing strings and comments. Review a sample of results and run the full suite. Split the resulting change into reviewable chunks by directory or owner where possible.

### Coordinating with others

- Agree on the destination and the migration path before starting; large refactors in shared code affect everyone's work in progress.
- Announce freezes or conflict-prone periods if a mechanical change touches many files.
- Keep refactor PRs free of behaviour changes so reviewers can review quickly ("pure rename; no logic changes" with tests unchanged is very fast to approve).

## When not to refactor

- **The code works, is rarely changed, and is not in your path.** Refactoring has a cost and a risk; spend it where change happens. Hotspot analysis (files with high churn × high complexity) shows where refactoring pays.
- **You don't have a safety net and can't build one cheaply**, and the change isn't urgent. Add tests first, or leave it.
- **A rewrite or replacement is already planned and imminent.**
- **Close to a release or freeze**, unless the refactoring is needed for a fix. Structural churn right before shipping raises risk with no user-visible benefit.
- **Purely to match personal taste.** If the codebase consistently uses a pattern, follow it.
- **When you don't understand the code yet.** Read, test, and characterize first; refactoring code you don't understand is how behaviour changes slip in. (Exploratory refactoring to *learn* — then discarding it — is a valid technique, as long as you discard it.)
- **The user asked for a specific minimal change.** Offer the refactoring; don't impose it.

## Refactoring and performance

Refactoring for clarity occasionally costs performance (an extra function call, an extra pass over a list). In most code this is negligible and the clarity makes later, *measured* optimisation easier. Don't avoid clear structure for imagined performance costs; do measure if the code is a known hot path (see `performance-optimization`). Conversely, don't claim a performance-motivated restructuring is a "refactor" if it changes behaviour, such as ordering or precision.

## Discovering context

- **Learn the project's idioms** — naming, error handling, module layout, preferred abstractions — by reading neighbouring code, linters, formatters, and style docs. Refactor toward them.
- **Find the test commands and how long they take**; you'll run them constantly. Identify the fastest subset that covers the area.
- **Check for tooling**: IDE/language-server refactoring support, codemod tools used before in the repo, type checkers, linters with autofix.
- **Look at history and ownership.** `git log`/blame show why code is shaped as it is; an odd structure may encode a fixed bug or a requirement. Ask before "simplifying" something deliberate.
- **Find all references, including dynamic ones**: string lookups, reflection, configuration files, templates, SQL, external consumers of public APIs, serialised data in storage or queues that encodes class or field names.
- **Ask about the review culture.** Some teams want refactors in separate PRs; some want them in the same PR in separate commits.

## Pitfalls

- **Mixing behaviour changes into a refactor**, so the behavioural change hides in a huge diff.
- **Big-bang refactors** on long-lived branches that can't be merged, then rot.
- **Fixing forward when a step breaks tests**, compounding errors instead of undoing.
- **Breaking public contracts unknowingly**: renaming a field that is serialised to storage or sent over the wire, changing an exception type callers catch, changing default argument values.
- **Overlooking dynamic references** (reflection, string-based dispatch, templates), so automated renames miss them.
- **Premature abstraction**: extracting a shared helper from two coincidentally similar pieces of code.
- **Refactoring tests into unreadable abstractions** — tests should remain obvious.
- **Changing evaluation order or laziness** in ways that alter side effects, error behaviour, or performance characteristics.
- **Leaving it at 80%**: two parallel ways of doing things, an abstraction with one implementation, a feature flag that's always on.
- **Reformatting a whole file** alongside a small refactor, burying the real change in whitespace diffs. Format separately or not at all.

## Verification

- [ ] Tests passed before starting and pass after every step and at the end.
- [ ] Coverage over the touched area was adequate, or characterization tests were added first.
- [ ] Public interfaces, serialised formats, error types, and side effects are unchanged (or changed deliberately via parallel change with the user's agreement).
- [ ] Dynamic and textual references were searched, not just symbol references.
- [ ] The diff contains no behaviour change; any behaviour change is in a separate, clearly described commit.
- [ ] The code is measurably better against the stated goal (the intended change is now easy; the confusing part is clear).
- [ ] No half-finished migration is left without a plan; temporary flags and shims are tracked for removal.
- [ ] Changes follow the project's conventions and formatting tools.
