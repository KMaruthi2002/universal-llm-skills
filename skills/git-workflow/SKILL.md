---
name: git-workflow
description: >-
  Use Git well and safely: crafting focused commits and messages, choosing a
  branching model (trunk-based, feature branches, release branches), rebasing
  vs. merging, interactive history cleanup, resolving merge and rebase
  conflicts, recovering lost work with reflog, undoing mistakes, tags, and
  rules for rewriting or force-pushing shared history. Use when committing,
  branching, rebasing, merging, untangling a messy history, fixing a botched
  merge or reset, recovering a deleted branch or commit, cleaning up before a
  PR, or deciding on a team branching strategy.
metadata:
  category: development
  related: pull-request-workflow, code-review, release-management, ci-cd-pipelines, scripting-and-shell, secure-coding
---

# Git Workflow

Git history is a shared, long-lived record of why the code is the way it is. Good Git practice makes that record useful (for review, debugging, bisecting, reverting, and auditing) and keeps teammates' work safe. Bad practice destroys work, obscures intent, and turns every merge into a negotiation.

## Scope

Covers local and shared Git operations: commits, branches, integration (merge/rebase), history editing, conflicts, recovery, tags, and team branching models.

Not covered:

- Opening, describing, and shepherding pull requests — see `pull-request-workflow`.
- Reviewing the code in them — see `code-review`.
- Versioning and release processes beyond tagging — see `release-management`.
- CI configuration triggered by Git events — see `ci-cd-pipelines`.

## Core principles

### 1. Shared history is immutable by default

Once commits are on a branch others use (the main branch, a release branch, a teammate's branch, anything others have pulled), do not rewrite them: no rebase, amend, reset, or force-push. Why: rewriting changes commit IDs; everyone who based work on the old IDs now has diverged history, and a force-push can silently delete their commits from the remote. Private, unpushed (or pushed-only-for-backup, clearly personal) branches can be rewritten freely.

### 2. Almost nothing in Git is truly lost — until garbage collection

Commits you "lost" through reset, rebase, amend, or branch deletion are still in the object database and reachable via the reflog for a period (by default around 30–90 days depending on reachability). Why it matters: when something goes wrong, stop and recover via reflog rather than making more changes. The exceptions — things Git cannot recover — are uncommitted work discarded by `reset --hard`, `checkout -- <file>`/`restore`, `clean -fd`, and `stash drop`/`clear` once the stash commit is unreachable and collected. Treat those as destructive.

### 3. A commit is a unit of intent

Each commit should do one logical thing, leave the project building and passing tests, and explain why. Why: atomic commits make review possible, make `git bisect` find the real culprit, and make `git revert` remove exactly one change without collateral damage.

### 4. Follow the repository's conventions

Commit message format, branch naming, merge strategy (merge commits, squash, rebase), signed commits, and protected-branch rules are team decisions. Discover and follow them. Why: consistency matters more than any particular choice, and tooling (changelog generators, release automation, CI rules) often depends on the convention.

### 5. Look before you leap

Before any history-altering or destructive command, check where you are and what will change: `git status`, `git branch -vv`, `git log --oneline --graph --decorate -n 20`, and `git diff`/`git diff --staged`. Why: most Git disasters are a correct command run on the wrong branch or with uncommitted changes present.

## Discovering context

Before committing or changing history in a repository:

- Read CONTRIBUTING, the PR template, and recent history (`git log --oneline -n 30`) to learn the message style — e.g. Conventional Commits (`feat:`, `fix:`), ticket prefixes, imperative mood, sign-off lines.
- Check for commit hooks (`.git/hooks`, a hooks manager config such as husky, lefthook, or pre-commit) and respect them; do not bypass with `--no-verify` unless the user asks and understands why.
- Learn the integration strategy: does the main branch show merge commits, squashed single commits per PR, or a linear rebased history?
- Identify protected branches and whether direct pushes are allowed.
- Check for signing requirements (GPG/SSH commit signing), DCO sign-off, or co-author conventions.
- Check `.gitattributes` (line endings, LFS, merge drivers) and `.gitignore` before adding files.
- Find whether the repository uses submodules, subtrees, or LFS; each changes how some operations behave.

If you are an automated agent: never change Git configuration (user identity, global settings, hooks) without being asked, and follow any instructions the user gives about authorship and attribution lines.

## Commits

### What goes in one commit

- One logical change: a bug fix with its test, a refactoring, a feature slice, a dependency bump.
- Separate mechanical changes (formatting, renames, moving files) from behaviour changes. A rename plus edit in one commit makes the diff unreadable and can defeat rename detection.
- Each commit should build and pass tests where practical, so bisect works.
- Do not mix unrelated fixes because they happened to be in your working tree. Use partial staging (`git add -p`, or a GUI's line staging) to split them.

### What never goes in a commit

- Secrets: API keys, passwords, tokens, private keys, `.env` files with real values, credentials in config. If you see one staged, stop. If one was committed, see "Secrets in history" below.
- Generated artifacts and build outputs (unless the project deliberately commits them).
- Large binaries without LFS or an equivalent, when the project uses it.
- Local editor or OS files — these belong in a global or project `.gitignore`.
- Personal data or production data dumps.

Review `git diff --staged` before every commit. It is the last cheap checkpoint.

### Messages

A good message tells a future reader what changed and why, in that order of brevity:

- **Subject line**: a short summary (commonly ≤50–72 characters), in the project's convention. Many projects use imperative mood ("Fix race in cache eviction"), which reads as "this commit will…".
- **Blank line**, then a **body** when the why is not obvious: the problem, the reason for this approach, alternatives rejected, side effects, links to issues. Wrap lines (commonly ~72 characters) if the project does.
- Reference issues and breaking changes in the way the project's tooling expects.

Weak: "fix", "updates", "WIP", "address review comments". The diff shows what lines changed; the message must carry the intent the diff cannot.

Illustrative example (not a required format):

```
Retry token refresh once on 401 from the billing API

The billing API occasionally returns 401 for tokens that are still
valid for a few seconds after rotation. One retry with a fresh token
removes the spurious failures seen in the nightly invoice job.
A retry loop was rejected because a real auth failure would then
hammer the API.

Refs: BILL-412
```

## Branching models

| Model | How it works | Fits | Costs |
|---|---|---|---|
| **Trunk-based** | Short-lived branches (hours to a couple of days) merged to main frequently; incomplete features hidden behind flags | Teams with good CI and continuous delivery | Requires feature flags, strong tests, small changes |
| **Feature branches + PRs** (GitHub flow) | A branch per change, merged to main via reviewed PR; main always deployable | Most teams; the common default | Long-lived branches drift and conflict |
| **Release branches** | Cut a branch per release for stabilization and hotfixes; main continues | Products with versioned releases, multiple supported versions | Fixes must be applied to several branches (cherry-picks) |
| **Git flow** (develop + main + release + hotfix branches) | Separate integration and production lines | Scheduled, infrequent releases with formal QA | Heavy; slow integration; many merges; often overkill for web services |
| **Fork-based** | Contributors work in forks, PR to upstream | Open source, untrusted contributors | Syncing forks; CI permissions for forks |

Guidance:

- Branch lifetime matters more than the named model. Conflicts and integration pain grow roughly with how long a branch lives and how much main changes meanwhile. Aim for branches measured in days.
- Keep up with main on long-ish branches by integrating regularly (rebase if private, merge if shared) rather than once at the end.
- Name branches per project convention (often `type/short-description` or including a ticket ID).
- Delete merged branches, locally and remotely, to keep the branch list meaningful.

## Integrating changes: merge vs. rebase vs. squash

| Operation | Result | Use when | Avoid when |
|---|---|---|---|
| **Merge** (`git merge`) | Creates a merge commit joining two histories; no rewriting | Integrating shared branches; preserving exact history; integrating main into a shared feature branch | You want linear history and the branch is private |
| **Fast-forward merge** | Moves the branch pointer; no merge commit | Branch is strictly ahead of target | — |
| **Rebase** (`git rebase`) | Replays your commits on a new base; new commit IDs; linear history | Updating a *private* branch with upstream changes; cleaning history before review | The branch is shared or already reviewed and others pulled it |
| **Squash merge** | Combines all branch commits into one on the target | Teams that want one commit per PR; messy branch history | Branch contains several logically separate commits worth keeping |
| **Cherry-pick** | Copies specific commits to another branch | Backporting a fix to a release branch | As a substitute for merging whole branches (creates duplicate commits and later conflicts) |

The "rebase vs. merge" debate is about values: rebasing optimizes for a readable linear history; merging optimizes for an honest record of what happened and never rewrites. Both are legitimate. Follow the project. The non-negotiable part is principle 1: do not rebase shared commits.

`git pull` performs fetch plus merge (or rebase, if configured). Prefer knowing which: `git pull --rebase` on private branches, or `git fetch` then decide. Configure `pull.ff only` or `pull.rebase` if you want to avoid surprise merge commits, but do not change a user's global config without asking.

## Cleaning up history before review

On a private branch, before opening or updating a PR (if the project values curated commits):

- `git commit --amend` to fix the last commit (message or content).
- `git rebase -i <base>` to reorder, squash, fixup, reword, or drop commits. In non-interactive environments, use `git commit --fixup=<sha>` followed by `git rebase -i --autosquash <base>` with an editor override such as `GIT_SEQUENCE_EDITOR=:` to accept the generated plan, or construct the history with soft resets and new commits.
- `git reset --soft <base>` then recommit in logical chunks when the history is beyond repair (this keeps all changes staged; nothing is lost).
- After review has started, prefer adding new commits (often "fixup" commits) so reviewers can see what changed since their last look; squash at merge time if the project does so. Rewriting a branch mid-review destroys reviewers' context and may orphan their comments.

Push a rewritten private branch with `git push --force-with-lease` (ideally also `--force-if-includes` on recent Git), never plain `--force`. `--force-with-lease` refuses if the remote has commits you have not seen, which protects a collaborator's or CI bot's pushes from being overwritten.

## Resolving conflicts

Conflicts mean two changes touched the same region and Git cannot know the intended combination. Resolution is a semantic decision, not a text-editing one.

Process:

1. **Understand both sides before editing.** Look at what each side intended: `git log --merge -p <file>`, or view the base, ours, and theirs versions (`git show :1:<file>`, `:2:`, `:3:`). Enabling `merge.conflictStyle zdiff3` (or `diff3`) shows the common ancestor in conflict markers, which makes intent much clearer.
2. **Combine the intents**, not just the lines. Often the correct result contains parts of both, or neither verbatim.
3. **Check beyond the markers.** A clean textual merge can still be semantically broken: a function renamed on one side and a new call to the old name added on the other. Build and run tests after resolving.
4. **Remove all markers** (`<<<<<<<`, `=======`, `>>>>>>>`); search for them before committing.
5. **Lockfiles and generated files**: do not hand-merge. Take one side and regenerate with the tool.
6. **Mark resolved** with `git add`, then `git merge --continue` / `git rebase --continue` / `git cherry-pick --continue`.
7. **If it goes badly**, abort cleanly: `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort`. This restores the pre-operation state.

Notes on "ours" and "theirs": during a merge, "ours" is the branch you are on and "theirs" is the one being merged in. During a rebase, they are reversed from intuition: "ours" is the branch being rebased onto (upstream), "theirs" is your commit being replayed. Double-check before using `--ours`/`--theirs` or strategy options like `-X theirs`, which resolve every conflict blindly.

If the same conflicts recur (long-running branches, repeated rebases), `git rerere` can record and reuse resolutions. Review its automatic resolutions; they can be wrong when context changed.

Reduce conflicts in the first place: small branches, frequent integration, separating formatting changes into their own commits that land quickly, and agreeing on auto-formatters so whitespace never conflicts.

## Undoing things

Choose the tool by whether the commit is shared and what you want to keep.

| Situation | Command | Safe on shared history? |
|---|---|---|
| Unstage a file, keep changes | `git restore --staged <file>` (older: `git reset <file>`) | Yes (local only) |
| Discard uncommitted changes to a file | `git restore <file>` | Destroys those changes — irreversible |
| Fix the last unpushed commit | `git commit --amend` | No if pushed |
| Undo last commit, keep changes staged | `git reset --soft HEAD~1` | No if pushed |
| Undo last commit, keep changes unstaged | `git reset HEAD~1` (mixed) | No if pushed |
| Throw away last commit and its changes | `git reset --hard HEAD~1` | No; also discards uncommitted work |
| Undo a pushed commit | `git revert <sha>` (creates an inverse commit) | Yes — the right tool for shared history |
| Undo a merge commit that was pushed | `git revert -m 1 <merge-sha>` | Yes, but re-merging the branch later needs the revert reverted first |
| Remove untracked files | `git clean -n` (dry run) then `git clean -f` | Irreversible for those files |
| Set work aside temporarily | `git stash push -m "msg"` (add `-u` for untracked) | Local |

Before any `reset --hard`, `clean -f`, `restore`, or `checkout -- .`, check `git status`. If there are uncommitted changes you might want, commit them to a temporary branch or stash them first. A throwaway commit is cheap; lost work is not.

## Recovering from mistakes with the reflog

The reflog records where `HEAD` (and each branch) pointed after every change: commits, resets, rebases, checkouts, merges, amends.

```
git reflog                       # HEAD history: HEAD@{0}, HEAD@{1}, ...
git reflog show <branch>         # history of one branch
git log -g --oneline             # reflog as a log
```

Common recoveries:

- **Bad reset or rebase**: find the entry just before it (e.g. `HEAD@{5}: rebase (start)` — you want the line before that), inspect with `git log <sha>`, then `git branch rescue <sha>` (safe) or `git reset --hard <sha>` (after confirming there is no uncommitted work to lose).
- **Deleted branch**: the deletion message prints the tip SHA; otherwise find it in `git reflog` and run `git branch <name> <sha>`.
- **Amended away a commit**: the pre-amend commit is in the reflog.
- **Abandoned rebase in progress**: `git rebase --abort`; if already finished, use `ORIG_HEAD` (set by reset, rebase, and merge) or the reflog.
- **Dropped stash**: `git fsck --no-reflogs --unreachable | grep commit` lists dangling commits; inspect them to find the stash.

Recovery discipline: create a new branch at the found commit first (`git branch rescue <sha>`), verify its content, and only then move existing branches. Creating a branch is non-destructive; resetting is not.

The reflog is local to each clone. Commits only ever on another machine, or deleted from the remote by someone else's force-push, may be recoverable from that person's clone, from CI checkouts, or from the hosting provider's UI/API (some keep events of force-pushes), not from your reflog.

## Force-pushing and shared history

Rules:

- Never force-push to main, release branches, or any branch others commit to, unless the team has explicitly agreed to it for this specific case (e.g. removing a leaked secret) and everyone affected knows to re-sync.
- On your own branches, use `--force-with-lease`.
- Announce force-pushes to anyone who might have pulled the branch.
- If you are an automated agent, do not force-push, delete remote branches, or rewrite published history without the user's explicit, specific approval.

How collaborators recover after an agreed rewrite of a shared branch: `git fetch`, then for a branch without local work `git reset --hard origin/<branch>`; with local work, `git rebase --onto origin/<branch> <old-upstream-sha> <local-branch>` to move only their own commits.

## Secrets in history

If a secret was committed:

1. **Rotate or revoke the secret immediately.** This is the real fix. Assume it is compromised the moment it was pushed anywhere, including a private repository or a fork, and remember CI logs, caches, and clones may hold it.
2. Remove it from the current tree and add the file to `.gitignore`; move the value to a secret store or environment.
3. If it was **never pushed**, amend or rebase it out locally.
4. If it **was pushed**, rewriting history (with a tool designed for it, e.g. `git filter-repo` or BFG) only limits further exposure; it does not un-leak the secret. Coordinate with the team and the hosting provider (cached views, pull request refs, and forks may retain it), and expect everyone to re-clone.
5. Add a secret-scanning pre-commit hook or CI check to catch the next one.

Never paste the secret value into commit messages, issues, or chat while handling the incident.

## Tags

- **Annotated tags** (`git tag -a v1.4.0 -m "..."`) store tagger, date, and message, and can be signed; use them for releases. **Lightweight tags** are just pointers; fine for private bookmarks.
- Tags are not pushed by default: `git push origin v1.4.0` (or `--follow-tags` to push annotated tags reachable from pushed commits).
- Treat release tags as immutable. Moving or re-creating a published tag breaks anyone who already fetched it, and caches and package registries may have recorded the old commit. If a release is broken, cut a new version.
- Follow the project's tag format (`v1.2.3` vs `1.2.3`, prefixed per package in monorepos); release tooling usually depends on it.

## Useful investigative tools

- `git log -S'<string>'` (pickaxe) finds commits that added or removed a string; `-G'<regex>'` for changes matching a pattern.
- `git log -L <start>,<end>:<file>` or `-L :<function>:<file>` shows the history of a range or function.
- `git blame -w -C -C` ignores whitespace and follows moved/copied lines; configure `blame.ignoreRevsFile` with a list of mass-formatting commits so blame skips them.
- `git bisect start <bad> <good>` then `git bisect run <test-command>` finds the commit that introduced a regression automatically. Atomic, building commits make this work.
- `git range-diff <old-base>..<old-tip> <new-base>..<new-tip>` compares two versions of a rewritten branch; useful for reviewing a force-pushed PR.
- `git worktree add <path> <branch>` checks out another branch in a separate directory, avoiding stash juggling when you need to switch context. Useful for running parallel tasks on separate branches.

## Common scenarios

Short recipes for situations that come up constantly. Check `git status` first in every case.

- **Committed to main instead of a feature branch (not pushed)**: `git branch feature/x` (keeps the commits), then `git reset --hard origin/main` on main (only if there is no uncommitted work), then `git switch feature/x`.
- **Committed to the wrong feature branch**: on the right branch, `git cherry-pick <sha>`; then remove it from the wrong branch with `git reset` (if private) or `git revert` (if shared).
- **Need to switch branches with uncommitted work**: `git stash push -u -m "context"`, switch, later `git stash pop`; or commit a WIP commit and amend it later; or use `git worktree add` to avoid switching at all.
- **Branch is far behind main and private**: `git fetch` then `git rebase origin/main`, resolving conflicts commit by commit. If conflicts are overwhelming, abort and instead squash your branch to one commit first (`git reset --soft $(git merge-base HEAD origin/main)` then commit), then rebase — one conflict pass instead of many.
- **Branch is far behind main and shared**: `git merge origin/main` into it; do not rebase.
- **Split one big commit into several**: `git reset HEAD~1` (mixed), then stage and commit in pieces with `git add -p`.
- **Move the last N commits to a new branch**: `git branch new-branch`, then `git reset --hard HEAD~N` on the current branch (after checking for uncommitted work).
- **Accidentally committed a large file (not pushed)**: `git rm --cached <file>`, add it to `.gitignore`, `git commit --amend`. If pushed, it is in history; decide with the team whether a rewrite is warranted.
- **Find which commit broke something**: `git bisect`, ideally with `git bisect run` and an automated check.
- **Merge went wrong but is not pushed**: `git reset --hard ORIG_HEAD` (or `git merge --abort` if still in progress).
- **Detached HEAD with commits you want to keep**: `git branch keep-this` before switching away; otherwise find them in the reflog later.

## Large repositories and special content

- **LFS** for large binaries when the project uses it; check `.gitattributes`. Committing a large binary without it bloats every clone permanently (until history is rewritten).
- **Submodules** pin another repository at a commit. After pulling, run `git submodule update --init --recursive`. Committing a submodule pointer change is a real change; review it.
- **Partial and shallow clones** (`--filter=blob:none`, `--depth`) speed up large repositories but some history operations then need extra fetching.
- **Line endings**: set via `.gitattributes` (`* text=auto` and explicit rules) rather than per-user `core.autocrlf`, to avoid whole-file diffs.

## Pitfalls

- Running a destructive command on the wrong branch or with uncommitted changes. Always check `git status` and the current branch first.
- `git add .` or `git commit -a` sweeping in secrets, debug code, build artifacts, or unrelated changes. Stage deliberately and review the staged diff.
- Rebasing a branch someone else has pulled, then force-pushing over their work.
- Plain `--force` instead of `--force-with-lease`.
- "Resolving" conflicts by taking one side wholesale (`-X ours/theirs`) without understanding what the other side did.
- Leaving conflict markers in files, or committing a resolution without building and testing.
- Reverting a merge and later being surprised that re-merging the branch does not bring its changes back.
- Giant "WIP" commits that make bisect and revert useless.
- Squash-merging a long branch that contained several independent changes, so they can no longer be reverted separately.
- Bypassing hooks with `--no-verify` to get past a failing check rather than fixing the cause.
- Moving or deleting published tags.
- Believing a history rewrite removes a leaked secret. Rotate it.

## Quality bar and verification

Before pushing or declaring Git work done:

- `git status` is clean or contains only intended changes; you know which branch you are on and what it tracks.
- `git log --oneline --graph` for your branch shows focused commits with meaningful messages in the project's format.
- `git diff <base>...HEAD` contains only what you intend to propose — no secrets, debug output, unrelated files, or conflict markers.
- The branch builds and tests pass after any rebase or conflict resolution (CI is the final check, but run it locally where possible).
- Any rewrite affected only private commits, and any force-push used `--force-with-lease`.
- For recoveries: the recovered content was verified on a rescue branch before branches were moved.

When reporting, state what changed in history (e.g. "rebased onto main, squashed 6 commits into 2, force-pushed with lease to my feature branch"), and flag anything that affects collaborators.
