# Universal LLM Skills -- documentation

A library of deep, style-neutral skills (`skills/<name>/SKILL.md`) for any LLM, with a catalog, a validator, and a sync loop that grows it from daily work.

This directory is a wiki maintained by an LLM: linked markdown pages, nothing outside the
repository. The rules are in [`CLAUDE.md`](CLAUDE.md).

## Start here

1. `../AGENTS.md` -- how an LLM uses the library (not a wiki page)
2. `SKILL_STANDARD.md` -- what a skill is and the bar it must clear (not a wiki page)
3. [[skill-lab-sync]] -- how the library grows from daily work

To propose a skill from a session: [[skill-lab-sync]].

---

## concepts

(none yet -- grow mode)

## architecture

(none yet -- grow mode)

## subsystems

- [[skill-lab-sync]] -- the skill + script that compare daily work against the catalog and open PRs for what is new

## decisions

(none yet -- grow mode)

## reference

(none yet -- grow mode)

## operations

(none yet -- grow mode)

## history

(none yet -- grow mode)

---

## Using this wiki

```
/docs-sync     right after a deploy or release -- reads only what changed since verified_at
/docs-lint     integrity check (orphans, broken links, broken sources, stale, unverified)
/docs-query    ask the docs. If it is not there, the answer says so
/docs-status   commits not yet reflected, stale pages, recent work
```

Every page carries `verified_at`, the commit it was checked against. Change code, run
`/docs-sync`.
