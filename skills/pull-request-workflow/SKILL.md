---
name: pull-request-workflow
description: >-
  Prepare, open, shepherd and land a code change through review: scoping a
  pull/merge request to one reviewable purpose, writing a description that
  explains why, self-reviewing before asking others, stacking dependent
  changes, responding to review feedback, keeping CI green and trustworthy,
  choosing a merge strategy (merge, squash, rebase), and cleaning up after.
  Use when the user says "open a PR", "write the PR description", "split this
  into smaller PRs", "address the review comments", "CI is failing on my PR",
  "how should I merge this", or asks how to get a change landed. Includes the
  rule never to force-push or rewrite a shared branch without consent. Not for
  reviewing someone else's change (code-review) or general branching and
  history mechanics (git-workflow).
metadata:
  category: quality
  related: code-review, git-workflow, ci-cd-pipelines, release-management, technical-writing, verify-before-done, testing-strategy, plan-and-decompose
---

# Pull Request Workflow

A pull request (PR, merge request, changelist, patch series; the name varies by platform) is a proposal to change a shared codebase plus the conversation that decides whether to accept it. The author's job is to make that decision **easy, fast and safe**: easy for reviewers to understand, fast to get through, and safe to merge and, if needed, to revert.

Most slow, painful reviews are caused upstream, by the author: a change that is too big, mixes concerns, has no explanation, or arrives with red CI. This skill is about getting those upstream things right.

Scope: this skill is the author's workflow. For how to review a change, see `code-review`. For branching models, commits, rebasing mechanics and history repair, see `git-workflow`. For pipeline design, see `ci-cd-pipelines`. For shipping a release, see `release-management` and `release-readiness`.

## Core principles

**1. One PR, one purpose.** A PR should do one thing that can be described in one sentence and reverted as a unit. Mixing a refactor, a bug fix and a feature means a reviewer cannot tell which line serves which goal, and a revert of one undoes all three.

**2. Reviewer time is the scarce resource.** Every minute you spend making the change easier to review saves several reviewer-minutes and shortens the wait. Size, ordering, description and self-review are all ways of spending your time to save theirs.

**3. The description explains why; the diff shows what.** Reviewers can read the code. What they cannot see is the problem, the constraints, the alternatives you rejected, and how you know it works. That context is also what a future maintainer needs when they find this change via `blame`.

**4. You are the first reviewer.** Never ask someone to find problems you could have found yourself by reading your own diff. Self-review catches debug output, unrelated changes, and obvious bugs, and it signals respect for the reviewer's time.

**5. Green CI is a precondition, not a reviewer's problem.** A red build tells reviewers the change is not ready. A flaky build that everyone re-runs until green trains people to ignore failures, which is how real breakages get merged.

**6. Shared history is shared property.** Rewriting commits others have pulled or built on (force-push, rebase, amend on a shared branch) destroys their work or forces them to recover it. Never do it on a shared branch without the explicit agreement of the people affected.

**7. Follow the project's process.** Branch naming, commit message conventions, PR templates, required reviewers, labels, changelog entries, sign-off requirements and merge strategy are team decisions. Discover and follow them; do not import your own.

## Discovering the project's conventions

Before opening anything, look for:

- `CONTRIBUTING`, `README` "development" sections, PR/MR templates (often in a platform-specific config folder), `CODEOWNERS`.
- Commit message conventions: look at recent history on the main branch. Is there a prefix scheme, a ticket reference, a sign-off line, a line-length habit?
- Merge strategy: are main-branch commits squash merges (one commit per PR), merge commits, or rebased linear history? Repository settings sometimes enforce one.
- Required checks and approvals: branch protection rules, required CI jobs, number of approvals, owner approval for certain paths.
- Changelog or release-note practice: a `CHANGELOG` file, changeset files, labels that drive release notes.
- Size and draft norms: does the team use draft PRs for early feedback? Is there an informal size limit?
- Whether you can push to the main repository or must work from a fork.

When there is no written guidance, the recent merged PRs are the best evidence of the norm.

## The process

### 1. Scope the change before writing much code

Decide what this PR will and will not contain. Useful questions:

- Can I state its purpose in one sentence without "and"?
- Could it be reverted on its own without breaking anything else?
- Does it mix mechanical changes (renames, moves, formatting) with behavioural ones? If so, separate them: mechanical changes are fast to review on their own and noise in a behavioural diff.
- Is there a preparatory refactor that would make the real change small and obvious? Land it first.

Rough size guidance (teams differ; follow local norms): a few hundred changed lines of real logic is about the upper limit for a careful review. Generated files, lockfiles, fixtures and snapshots do not count the same, but call them out so the reviewer knows to skim them.

**Ways to split a large change** (pick the seam that keeps each step working):

| Strategy | How | Good for |
|---|---|---|
| Preparatory refactor first | Restructure without behaviour change, then add the feature | Features that need existing code reshaped |
| Layer by layer | Schema, then data access, then API, then UI | Full-stack features with clear boundaries |
| Behind a flag | Land incomplete work disabled, enable in a final small PR | Long-running features on trunk-based teams |
| Expand then contract | Add new path alongside old, migrate callers, remove old | API, schema and interface changes |
| Mechanical vs semantic | One PR for the rename or move, one for the logic | Any change that also touches many files cosmetically |
| By consumer | Migrate one caller or module per PR | Large migrations across a codebase |

Each intermediate PR must leave the main branch buildable, tested and deployable. "Part 2 will fix the broken build" is not a split, it is a broken main branch.

### 2. Make the commits tell a story (if the project keeps them)

If the project squash-merges, individual commits matter mainly to you and to reviewers reading commit by commit. If it preserves commits (merge commits or rebase merges), each commit becomes permanent history and should build, pass tests, and have a meaningful message. Either way:

- Write messages that explain why, not just what ("Retry on 503 from payment provider, which returns it during deploys" beats "fix retry").
- Keep fixups out of permanent history when the project cares about it: squash "fix typo" commits into the commit they fix before merge, using whatever the project's normal approach is. (See `git-workflow`.)

### 3. Self-review before requesting review

Read your own diff as a reviewer would, in the same view they will use. Check:

- **No accidental content**: debug prints, commented-out code, local config, credentials or tokens, large unintended files, editor artifacts, unrelated formatting churn.
- **Only intended changes**: every hunk serves the stated purpose. Move anything else to another PR.
- **Correctness walk**: run through the edge cases from `code-review` (empty, boundary, failure, concurrent) for the code you changed.
- **Tests**: new behaviour is tested; a bug fix has a regression test; the tests fail without your change (try reverting the implementation and running them, if practical).
- **Docs and config**: public behaviour changes are reflected in docs, changelog, config examples, migrations, API specs.
- **Run it**: build, run the test suite (at least the relevant subset), lint, type-check, and exercise the feature by hand where it has a user-visible effect.

If you are an agent preparing a PR, self-review includes re-reading the entire diff from the top after the last edit, not just the last hunk you changed. Agents commonly leave stray edits from earlier attempts. See `verify-before-done`.

### 4. Write the description

There is no single right format, and the project's template wins if it has one. A good description lets a reviewer who has never seen the ticket understand and evaluate the change. It usually contains:

- **The problem or goal**: what is wrong or missing, and for whom. Link the issue, but do not rely on the link alone; tickets get reorganised and many reviewers will not click.
- **The approach**: what you changed, at the level of ideas, and why this way. Mention alternatives you considered and rejected if a reviewer might reasonably propose them.
- **How it was verified**: what you ran, what you tested by hand, with what data. "Tests pass" is weak; "added tests for X and Y; manually verified the export with a 50k-row file" is strong.
- **Risk and rollout**: what could break, who is affected, migrations, flags, backward compatibility, and how to roll back.
- **Reviewer guidance**: where to start reading, which files are mechanical or generated, specific questions you want answered, what is intentionally out of scope.
- **Visual evidence** for UI changes: before and after screenshots or short recordings.

Illustrative example of a compact description (one possible shape, not a template):

> Fixes duplicate charges when the payment webhook is retried (#1423).
>
> The provider retries webhooks on timeout, and our handler is not idempotent: each delivery creates a new charge record. This change records the provider's event ID in a unique column and skips events already processed.
>
> Considered locking on the order row instead, but that does not protect against the two deliveries hitting different instances before either commits.
>
> Verified with a new integration test that delivers the same event twice concurrently, plus a manual replay against the sandbox.
>
> Migration adds a nullable column and a unique index created concurrently; safe on the current table size. Rollback: revert the code; the column can stay.
>
> Start with `webhooks/handler`; the migration is mechanical.

Write the title for someone scanning a list: specific and in the project's convention ("Make payment webhook idempotent" rather than "Fix bug").

### 5. Open it and request the right reviewers

- Use a **draft** (or the platform's equivalent) when you want early feedback on direction and the change is not ready to merge. Say explicitly what feedback you want.
- Request reviewers who own or know the area; for cross-cutting risk (security, database, accessibility), request a specialist and say why.
- Do not request ten reviewers. Diffuse responsibility means nobody reviews carefully.
- If the change is urgent, say so and why in the description, rather than pinging people privately.

### 6. Keep CI green and honest

- Wait for CI before requesting review, or at least before expecting it.
- When a check fails, **read the failure** before re-running. Determine whether it is your change, a pre-existing breakage on main, or a flaky test.
- Do not re-run a failing job repeatedly hoping for green. If it is flaky, say so in the PR, link or file an issue for the flake, and get agreement before merging over it.
- Never disable, skip, or weaken a check (or a test) to get your PR through without saying so explicitly in the description and getting reviewer agreement. This is one of the most damaging silent changes a PR can contain.
- If main is broken by someone else, do not "fix" it inside your unrelated PR; raise it, and rebase or merge once it is fixed.

See `ci-cd-pipelines` for making pipelines faster and less flaky.

### 7. Respond to review

Treat review as a collaboration on the shared goal of good code, not a negotiation.

- **Respond to every comment.** Fix it, explain why not, or agree on a follow-up. Unanswered comments leave reviewers guessing whether you saw them.
- **Fix blockers first**, then should-fix items, then decide on suggestions and nits.
- **Disagree with reasons, not resistance.** If you think a comment is wrong, explain your reasoning and evidence. If it is a matter of taste and the reviewer is not blocking, it is reasonable to keep your version. If you cannot converge in two exchanges, talk synchronously and record the outcome.
- **Ask when unclear.** "Do you mean X or Y?" is faster than guessing and re-reviewing.
- **Make re-review easy.** Push fixes as new commits during review (rather than rewriting history) so reviewers can see what changed since their last look, unless the project prefers otherwise. Squash at merge time if that is the norm. Reply to each thread saying what you did.
- **Do not resolve threads someone else opened** if the project expects the reviewer to resolve them; check the norm.
- **Push back on scope creep politely.** "Good idea; I've filed #1500 for it so this PR stays focused" is a complete answer.
- **Re-request review** explicitly once you have addressed everything, with a short summary of what changed.

If you are an agent responding to review: address every comment, report which you fixed and which you did not and why, and do not mark threads resolved or dismiss reviews on the user's behalf unless asked.

### 8. Update the branch with the base

When main moves on, you may need to incorporate it. Choose based on the branch's sharing status and the project's norms:

| Branch situation | Safe default |
|---|---|
| Only you work on it, nobody has based work on it | Rebase or merge per project norm; force-pushing *your own* branch is generally acceptable, but prefer the lease-protected form (e.g. `--force-with-lease`) so you do not overwrite pushes you have not seen |
| Others have pushed to it or branched from it | Merge the base in; do not rewrite. Coordinate before any rebase |
| Under active review and the platform loses comment context on force-push | Prefer merging the base in, or push fixes as new commits and only clean history just before merge |

**Never force-push to the main branch or any long-lived shared branch** (release branches, integration branches) without explicit consent from the team. If you are an agent: never force-push, rebase a pushed branch, or delete a remote branch without the user's explicit instruction for that specific action, and say what will be overwritten before doing it.

Resolve conflicts carefully: a conflict resolution is new code nobody reviewed. Re-run tests after resolving, and mention significant resolutions in the PR.

### 9. Merge

Before merging, confirm:

- All required approvals and checks are satisfied (not bypassed).
- All blocking threads are resolved; agreed follow-ups are filed.
- The branch is current enough that CI results reflect what will land.
- The merge strategy matches project norm.
- Release notes, changelog, or labels are in place if required.
- You are merging at a sensible time for anything risky (not right before a holiday or an unmonitored period, if the change deploys automatically).

**Merge strategies** (use what the project uses; this is for when you get a say):

| Strategy | Result | Pros | Cons |
|---|---|---|---|
| Squash merge | One commit on main per PR | Clean, revertible-by-PR history; messy branch commits disappear | Loses intermediate commits; harder to stack PRs; the squash message needs care |
| Merge commit | All branch commits plus a merge commit | Preserves full history and context; works well with stacks | Noisier history; requires disciplined commits |
| Rebase and merge | Branch commits replayed linearly on main | Linear history with individual commits | Rewrites commit IDs; each commit must build and pass on its own |

When squashing, edit the final message: the default concatenation of "wip", "fix", "address review" is useless history. A good squash message is close to a condensed PR description.

Merge only what you are authorised to merge. If you are an agent, do not merge without the user's explicit go-ahead for that PR.

### 10. After merge

- Watch the deploy or the next pipeline run if the change deploys automatically; check dashboards or logs for the behaviour you changed. See `observability`.
- Delete the branch if that is the norm (and it is yours).
- Close or update linked issues; file the follow-ups you promised.
- If something goes wrong, revert first and investigate second when the impact is significant. A clean, single-purpose PR makes this trivial, which is one more reason to keep them small.

## Stacked changes

When a feature needs several dependent PRs, you can stack them: PR B is based on PR A's branch, C on B, and so on. This keeps each review small without waiting for each merge.

Guidance:

- State the stack in each description ("2 of 4; depends on #101") with links, so reviewers read in order.
- Keep the bottom of the stack moving: the deeper the stack, the more rebasing each change at the bottom causes.
- Each PR must make sense and be safe on its own once merged, in order.
- Restacking after a lower PR changes involves rebasing upper branches. This is rewriting history on those branches; it is fine on branches only you use, and needs coordination otherwise.
- With squash merges, merging the bottom PR changes commit IDs, so upper PRs need rebasing onto main; tools that manage stacks automate this, but know what they do before relying on them.
- If the stack grows beyond three or four, consider landing behind a feature flag directly on main instead.

## Worked example: splitting a change

Suppose the task is "let users export their order history as CSV", and the first working version is a single 1,400-line branch. Reading it back, the author finds it contains:

- a move of the order-query code from the controller into a new repository module (600 lines, mostly moved),
- a new paginated query that streams rows instead of loading them all,
- a CSV serialiser with escaping rules,
- a new endpoint plus authorisation,
- a button and progress state in the UI,
- a reformat of two unrelated files the editor touched.

Reasoning about the split:

1. The reformat has nothing to do with the feature: drop it, or send it as its own trivial PR if the project wants it.
2. The move is mechanical and large. On its own, with "no behaviour change; moved with tooling" in the description, it reviews in minutes. Mixed in, it hides the real logic. It goes first.
3. The streaming query and serialiser are pure logic with no user-visible effect; they can land together with thorough unit tests, unused.
4. The endpoint and its authorisation are the security-relevant part and deserve a focused review; it goes next, perhaps behind a flag.
5. The UI is last and enables the feature.

The result is four PRs, each with one purpose, each safe to deploy, and each reviewed by the right people (the security-relevant one gets a careful reviewer; the move gets a quick skim). Total review time drops even though the PR count rises, because no reviewer has to hold 1,400 lines in their head.

## When review stalls

Waiting is the most common cost in PR workflows. Before nudging, check whether the delay is your fault: is the PR too large, undescribed, red, or assigned to the wrong person? Fix those first. Then:

- Ping once, in the PR or the team's normal channel, with what you need ("needs one approval; the migration part is the only tricky bit").
- If the designated reviewer is unavailable, ask who else can review rather than waiting indefinitely.
- Offer a short walkthrough for complex changes; ten minutes talking often replaces a day of async back-and-forth.
- Do not route around required review (self-approving, admin-merging) because it is slow. If the process is too slow in general, raise that as a process issue.

## Reverting

A revert is a normal tool, not an admission of failure. When a merged change causes a significant problem, reverting quickly usually beats fixing forward under pressure, provided:

- the change is self-contained (another reason for single-purpose PRs),
- no irreversible step has happened that the revert would not undo (a data migration, sent emails, an external API contract others now rely on). Check this before reverting; reverting code does not revert data.
- the revert itself goes through the project's normal (perhaps expedited) review and CI.

Write the revert's description like any other: what is being reverted, why, and what the plan is to re-land it.

## Special cases

- **Hotfixes**: smallest possible change, clear description of the incident, expedited but not skipped review, and a follow-up for the proper fix if the hotfix is a patch. Backport to release branches per the project's process.
- **Large mechanical changes** (formatter rollout, mass rename): do them in a PR with no behaviour change, describe how they were generated (the command or script), and let reviewers verify the process rather than every line. Coordinate timing, since they conflict with everyone's open work.
- **Dependency updates**: describe what changed upstream that matters (breaking changes, security fixes), and how you verified. See `dependency-management`.
- **Database migrations**: describe lock behaviour, run time on realistic data, backward compatibility with the running code, and rollback. Often the migration should be its own PR, deployed before the code that needs it. See `database-migrations`.
- **Contributing to projects you do not maintain**: read the contribution guide, discuss significant changes in an issue first, keep the PR minimal, and expect maintainers to have different priorities. Accept that they may decline.
- **Generated code (including AI-generated)**: you are accountable for every line. Review it as thoroughly as code from an unknown contributor (see `code-review`, "Reviewing AI-generated code"), and disclose generation if the project's policy asks for it.

## Pitfalls

- **The mega-PR**: thousands of lines, multiple concerns, reviewed superficially or never. Split it.
- **The empty description**: "see ticket" or nothing. The reviewer reconstructs your reasoning, badly.
- **Asking for review on red CI**: wastes reviewer attention and signals the change is not ready.
- **Silent check weakening**: skipped tests, loosened lint rules, raised thresholds, or deleted assertions hidden inside a feature PR.
- **Re-running flaky tests to green** without recording the flake.
- **Force-pushing a shared branch**: destroys collaborators' commits or review context. Always ask first.
- **Rewriting history mid-review** on platforms where it hides what changed since the last review.
- **Leaving comments unanswered**, or resolving others' threads without a reply.
- **Scope creep from either side**: accepting every "while you're here" request, or sneaking unrelated changes in.
- **Merging and walking away** from an auto-deploying change.
- **Default squash messages** full of "fix" and "wip".
- **Long-lived branches** that drift from main and become merge-conflict projects. Integrate early and often.

## Quality bar and verification

Before requesting review, you should be able to say yes to:

- The PR has one purpose, stated in its title and first sentence.
- The description explains why, how it was verified, and the risk and rollback.
- I have read the entire diff myself and it contains only intended changes.
- CI is green, or any failure is explained and agreed as unrelated.
- Tests cover the change and would fail without it.
- No checks, tests or safety rules were weakened without being called out.
- Docs, changelog, and migrations are included where needed.

Before merging:

- Required approvals and checks are met, not bypassed.
- Every review comment has a response; follow-ups are filed.
- The merge strategy and final commit message match the project's norm.
- Nothing will force-push or rewrite a shared branch without consent.
- Someone (you) will watch the change land.

## Related skills

- `code-review` — the reviewer's side, and the checklist to self-review against.
- `git-workflow` — commits, branching, rebasing and conflict mechanics.
- `ci-cd-pipelines` — fixing slow or flaky pipelines.
- `release-management`, `release-readiness` — getting merged changes to users.
- `technical-writing` — writing descriptions others can follow.
- `plan-and-decompose` — splitting a large change into a sequence of PRs.
