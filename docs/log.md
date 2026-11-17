# Work log

Append-only. Newest entries at the bottom.

---

## [2026-11-06] setup | docs/ wiki scaffolded

- Categories: concepts - architecture - subsystems - decisions - reference - operations - history
- Baseline commit: `6e9490e`
- Created: `docs/{CLAUDE,index,log}.md`, `raw/`, 4 `.claude/commands/docs-*`,
  and `.claude/scripts/docs-lint.py`

- Started in grow mode: one page, `subsystems/skill-lab-sync`, written from
  `skills/skill-lab-sync/SKILL.md` and `scripts/skill_lab_sync.py` (the area just built).
  `docs/SKILL_STANDARD.md` and `docs/CONNECTING.md` predate the wiki and stay as plain
  documents. Nothing else surveyed.

## [2026-11-17] sync | skill-lab-sync line references

- Re-checked `subsystems/skill-lab-sync` against `scripts/skill_lab_sync.py` at `b225f38`.
  The `propose` line references had drifted after the `compare` error-handling change
  (`:212`, `:218`, `:240`, `:278`, `:295` are now `:215`, `:221`, `:244`, `:281`, `:299`).
- Bumped `verified_at` to `b225f38`.
