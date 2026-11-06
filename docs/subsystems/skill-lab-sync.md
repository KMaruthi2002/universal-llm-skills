---
title: Skill lab sync
type: subsystem
created: 2026-11-06
updated: 2026-11-06
sources:
  - code: skills/skill-lab-sync/SKILL.md
  - code: scripts/skill_lab_sync.py
  - code: scripts/validate.py
  - code: .github/workflows/validate.yml
verified_at: 6e9490e
---

# Skill lab sync

The loop that grows the library from daily work. It has two halves: a skill that any
assistant can load, and a script that does the mechanical part when a shell is available.

## The skill (`skills/skill-lab-sync/SKILL.md`)

An ordinary library skill, category `meta`, so it ships through the same catalog and
validator as everything else. Its job is to make one uploaded file enough: it carries the
repository URL, the raw `catalog.json` URL, the compare rules, the bar for a new skill
(delegated to `docs/SKILL_STANDARD.md` and `write-new-skill`), and both landing paths —
by script when the assistant has `git` and `gh`, or by a prefilled GitHub "new file" link
(`/new/main?filename=skills/<name>/SKILL.md`) when it has nothing but a chat window.

Verdicts are **existing** (use the named skill), **extend** (propose a section in the
nearest skill), **new** (write and propose). The skill tells the assistant to default to
*existing* when in doubt, because near-duplicates degrade routing for every skill around
them.

## The script (`scripts/skill_lab_sync.py`)

Standard library only, like the other scripts, so it runs wherever Python does.

**`compare`** (`scripts/skill_lab_sync.py:141`) scores each candidate against every
catalog entry. Tokens are lowercased, lightly stemmed and stopword-filtered
(`scripts/skill_lab_sync.py:60`); each token is weighted by inverse document frequency
over the catalog (`scripts/skill_lab_sync.py:100`) so a rare word like "cron" counts for
more than "design". The score (`scripts/skill_lab_sync.py:114`) is 0.65 × weighted
coverage of the candidate's words plus 0.35 × how much of the skill's *name* the
candidate says; an exact name match is 1.0. Thresholds live at
`scripts/skill_lab_sync.py:43`: ≥ 0.45 existing, ≥ 0.25 extend, else new. The catalog
comes from the clone's `catalog.json`, or `--catalog` with a path or URL.

**`propose`** (`scripts/skill_lab_sync.py:196`) takes a finished `SKILL.md`, rejects it
early if the body is under 2000 characters (`:212`) or its name already exists without
`--extend` (`:218`), then works in a temporary git worktree on `skill-lab/<name>` cut
from `origin/main` (`:240`): copy the skill and any `references/`, `scripts/`,
`examples/` beside it, run `scripts/validate.py` and `scripts/build_catalog.py`, commit, push, open the
PR with `gh` (`:295`). Without push permission it forks first (`:278`). The worktree and
the local branch are removed in `finally` (`:301`), so the contributor's checkout is
never touched. `--dry-run` stops before the push.

The PR is then gated by CI (`.github/workflows/validate.yml:11`), which runs the
validator and fails if the generated catalog files are not up to date (`:15`).

> ⚠️ `propose` validates against `origin/main`, not the local checkout. A draft whose
> `related:` names a skill that exists only locally (uncommitted or unpushed) fails
> validation with "related skill does not exist". Push the dependency first, or drop the
> link.

> ⚠️ The thresholds (`scripts/skill_lab_sync.py:43`) were calibrated by hand on nine
> candidates on 2026-11-05. A short candidate ("Writing a README for a repo") still lands
> on a neighbour rather than `code-documentation`; the skill compensates by telling the
> assistant to read the top match before deciding. Do not lower `EXISTING_AT` to make
> such cases "new" — the whole design leans toward reuse.

> ⚠️ The validator's thin-body check (`scripts/validate.py:19`) counts non-empty lines
> of the *body*, excluding frontmatter. A file that is 125 lines long can still be 112
> body lines and warn. The warning is not fatal in CI (no `--strict`), but reviewers see
> it.

> ⚠️ A browser-submitted PR (the no-tools path) cannot regenerate `CATALOG.md`,
> `catalog.json` and `llms.txt`, so its CI catalog check is red by design. The maintainer
> runs `scripts/build_catalog.py` on merge. The skill tells the person this in advance so the red
> check does not read as their mistake.

## Related pages

None yet; this wiki is in grow mode. The skill standard itself is at
`docs/SKILL_STANDARD.md` (a plain document, not a wiki page).
