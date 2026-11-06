#!/usr/bin/env python3
"""Compare the skills you worked on today against this library, and propose new ones by pull request.

This is the mechanical half of `skills/skill-lab-sync/SKILL.md`. Standard library only.

Usage:
  python3 scripts/skill_lab_sync.py compare "candidate name: one-line description" [...]
  python3 scripts/skill_lab_sync.py compare --file today.md          # one candidate per line
  python3 scripts/skill_lab_sync.py compare --catalog URL_OR_PATH ... # default: this clone's catalog.json
  python3 scripts/skill_lab_sync.py propose path/to/SKILL.md [--dry-run] [--no-pr] [--extend]

`compare` prints, for each candidate, a verdict:
  existing  the library already covers this task; use the named skill
  extend    the library has a close neighbour; propose a section in it rather than a new skill
  new       nothing covers it; write it to docs/SKILL_STANDARD.md and `propose` it

`propose` copies a finished SKILL.md into `skills/<name>/`, runs validate.py and
build_catalog.py, commits on a `skill-lab/<name>` branch in a temporary worktree,
pushes, and opens a pull request with `gh` (forking first if you lack write access).
It never commits to main.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import CATEGORIES, NAME_RE, ROOT, load_skill  # noqa: E402

UPSTREAM = "KMaruthi2002/universal-llm-skills"
RAW_CATALOG = f"https://raw.githubusercontent.com/{UPSTREAM}/main/catalog.json"

# Thresholds on the overlap coefficient between candidate tokens and a skill's name+description tokens.
EXISTING_AT = 0.45
EXTEND_AT = 0.25

STOPWORDS = {
    "a", "an", "and", "any", "are", "as", "at", "be", "before", "by", "do", "for", "from", "how",
    "in", "into", "is", "it", "its", "not", "of", "on", "or", "see", "so", "than", "that", "the",
    "their", "them", "then", "there", "these", "this", "to", "use", "used", "using", "when", "with",
    "you", "your", "what", "which", "who", "will", "would", "can", "should", "also", "e", "g", "i",
    "if", "we", "our", "all", "one", "more", "most", "very", "only", "just", "about", "after",
    "work", "working", "works", "task", "tasks", "make", "makes", "making", "thing", "things",
    "need", "needs", "needed", "want", "wants", "get", "gets", "new", "existing", "good", "well",
}


# --------------------------------------------------------------------------- compare


def tokens(text: str) -> set[str]:
    """Lowercase word tokens with light stemming, minus stopwords.

    Light stemming (plurals, -ing, -ed) is enough to make "migrations" meet "migration" without
    pulling in a stemming library; it deliberately stays crude so results are easy to predict.
    """
    out = set()
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if len(w) < 3 or w in STOPWORDS:
            continue
        for suffix in ("ing", "ed", "es", "s"):
            if w.endswith(suffix) and len(w) - len(suffix) >= 4:
                w = w[: -len(suffix)]
                break
        out.add(w)
    return out


def load_catalog(source: str | None) -> list[dict]:
    if source is None:
        local = ROOT / "catalog.json"
        if local.exists():
            return json.loads(local.read_text(encoding="utf-8"))["skills"]
        source = RAW_CATALOG
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=20) as resp:  # noqa: S310 - fixed public URL by default
            return json.loads(resp.read().decode("utf-8"))["skills"]
    return json.loads(Path(source).read_text(encoding="utf-8"))["skills"]


def split_candidate(raw: str) -> tuple[str, str]:
    """'name: description' -> (name, description); plain text -> ('', text)."""
    raw = raw.strip().lstrip("-*• ").strip()
    m = re.match(r"^([a-z0-9][a-z0-9 _-]{0,63})\s*[:—–-]\s+(.+)$", raw, re.IGNORECASE)
    if m:
        name = re.sub(r"[\s_]+", "-", m.group(1).strip().lower())
        return name, m.group(2).strip()
    return "", raw


def idf_table(skills: list[dict]) -> dict[str, float]:
    """Inverse document frequency over the catalog, so rare words ("cron", "readme") count
    for more than words every skill uses ("design", "writing")."""
    import math

    docs = [tokens(s["name"].replace("-", " ") + " " + s["description"]) for s in skills]
    n = len(docs) or 1
    df: dict[str, int] = {}
    for d in docs:
        for t in d:
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}


def score(candidate_name: str, candidate_desc: str, skill: dict, idf: dict[str, float]) -> float:
    cand = tokens(candidate_name.replace("-", " ") + " " + candidate_desc)
    if not cand:
        return 0.0
    if candidate_name and candidate_name == skill["name"]:
        return 1.0
    target = tokens(skill["name"].replace("-", " ") + " " + skill["description"])
    name_tokens = tokens(skill["name"].replace("-", " "))
    unseen = max(idf.values(), default=1.0)  # a word the catalog never uses is maximally specific
    w = lambda t: idf.get(t, unseen)  # noqa: E731
    # Coverage: how much of what the candidate says (weighted by specificity) this skill already says.
    coverage = sum(w(t) for t in cand & target) / sum(w(t) for t in cand)
    # Name hits are the strongest signal, but only when most of the skill's name is actually named.
    name_hit = len(cand & name_tokens) / len(name_tokens) if name_tokens else 0.0
    if name_hit < 1.0 and len(name_tokens) > 1:
        name_hit *= 0.5
    return round(min(1.0, 0.65 * coverage + 0.35 * name_hit), 3)


def verdict(best: float) -> str:
    if best >= EXISTING_AT:
        return "existing"
    if best >= EXTEND_AT:
        return "extend"
    return "new"


def compare(candidates: list[str], catalog_source: str | None, as_json: bool) -> int:
    skills = load_catalog(catalog_source)
    idf = idf_table(skills)
    results = []
    for raw in candidates:
        name, desc = split_candidate(raw)
        ranked = sorted(((score(name, desc, s, idf), s) for s in skills), key=lambda t: t[0], reverse=True)[:3]
        best = ranked[0][0] if ranked else 0.0
        results.append(
            {
                "candidate": raw.strip(),
                "name": name or None,
                "verdict": verdict(best),
                "matches": [{"skill": s["name"], "score": sc, "path": s["path"]} for sc, s in ranked],
            }
        )

    if as_json:
        print(json.dumps(results, indent=2))
        return 0

    for r in results:
        print(f"{r['verdict'].upper():9} {r['candidate']}")
        for m in r["matches"]:
            print(f"          {m['score']:.2f}  {m['skill']}  ({m['path']})")
        if r["verdict"] == "existing":
            print(f"          -> use skills/{r['matches'][0]['skill']}/SKILL.md; nothing to add")
        elif r["verdict"] == "extend":
            print(f"          -> read skills/{r['matches'][0]['skill']}/SKILL.md; if it misses this case, propose a section there (propose --extend)")
        else:
            print("          -> write a new skill per docs/SKILL_STANDARD.md, then: propose <path/to/SKILL.md>")
        print()
    print("Verdicts are a floor, not a ruling: read the top match before writing anything new.")
    return 0


# --------------------------------------------------------------------------- propose


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=capture)


def gh_json(args: list[str]) -> dict | list | str | None:
    try:
        out = subprocess.run(["gh", *args], check=True, text=True, capture_output=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out.strip()


def propose(path: Path, dry_run: bool, no_pr: bool, extend: bool, repo: str, base: str) -> int:
    if not path.is_file():
        print(f"error: {path} is not a file", file=sys.stderr)
        return 2
    draft = load_skill(path)
    if draft.errors or not draft.name:
        for e in draft.errors or ["missing `name`"]:
            print(f"error: {e}", file=sys.stderr)
        return 2
    if not NAME_RE.match(draft.name) or len(draft.name) > 64:
        print(f"error: invalid skill name {draft.name!r} (lowercase, digits, hyphens)", file=sys.stderr)
        return 2
    if draft.category not in CATEGORIES:
        print(f"error: unknown category {draft.category!r}; one of {', '.join(CATEGORIES)}", file=sys.stderr)
        return 2
    if len(draft.body.strip()) < 2000:
        print("error: body is too short to be a skill; see docs/SKILL_STANDARD.md §4 (depth)", file=sys.stderr)
        return 2

    target_rel = Path("skills") / draft.name / "SKILL.md"
    exists = (ROOT / target_rel).exists()
    if exists and not extend:
        print(f"error: skills/{draft.name} already exists. Use it, or pass --extend to propose changes to it.", file=sys.stderr)
        return 2
    if extend and not exists:
        print(f"error: --extend given but skills/{draft.name} does not exist; drop --extend to propose a new skill.", file=sys.stderr)
        return 2

    if shutil.which("git") is None:
        print("error: git is not available; paste the file at the GitHub 'new file' URL instead (see the skill).", file=sys.stderr)
        return 2

    branch = f"skill-lab/{draft.name}"
    verb = "Extend" if extend else "Add"
    run(["git", "fetch", "origin", base], cwd=ROOT)
    # Detect whether `origin` is the upstream or a fork so the PR targets the right repo.
    origin_url = run(["git", "remote", "get-url", "origin"], cwd=ROOT, capture=True).stdout.strip()
    origin_is_upstream = origin_url.rstrip("/").removesuffix(".git").lower().endswith(repo.lower())
    if not origin_is_upstream:
        run(["git", "fetch", origin_url, base], cwd=ROOT, check=False)

    tmp = Path(tempfile.mkdtemp(prefix="skill-lab-"))
    worktree = tmp / "wt"
    try:
        run(["git", "worktree", "add", "-b", branch, str(worktree), f"origin/{base}"], cwd=ROOT)
        dest = worktree / target_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        # Optional sidecars next to the draft travel with it.
        for sub in ("references", "scripts", "examples"):
            src = path.parent / sub
            if src.is_dir():
                shutil.copytree(src, dest.parent / sub, dirs_exist_ok=True)

        py = sys.executable
        v = run([py, str(worktree / "scripts" / "validate.py")], cwd=worktree, check=False)
        if v.returncode != 0:
            print("error: validate.py failed; fix the errors above and rerun.", file=sys.stderr)
            return 1
        run([py, str(worktree / "scripts" / "build_catalog.py")], cwd=worktree)
        run(["git", "add", "-A"], cwd=worktree)
        if not run(["git", "diff", "--cached", "--quiet"], cwd=worktree, check=False).returncode:
            print("error: nothing changed; the draft is identical to what is on the branch.", file=sys.stderr)
            return 1
        run(["git", "commit", "-q", "-m", f"{verb} {draft.name} skill\n\nProposed via skill-lab-sync."], cwd=worktree)

        if dry_run:
            print(f"\nDRY RUN: validated and committed {target_rel} on local branch {branch}; nothing pushed.")
            print("Rerun without --dry-run to push and open the pull request.")
            return 0

        if shutil.which("gh") is None or run(["gh", "auth", "status"], check=False, capture=True).returncode != 0:
            print("error: `gh` is missing or not logged in. Run `gh auth login`, or push the branch and open the PR by hand.", file=sys.stderr)
            return 1

        perms = gh_json(["api", f"repos/{repo}", "--jq", ".permissions.push"])
        can_push = str(perms).lower() == "true"
        if can_push and origin_is_upstream:
            run(["git", "push", "-u", "origin", branch], cwd=worktree)
            head = branch
        else:
            # No write access: fork (idempotent), push there, and open the PR across the fork.
            run(["gh", "repo", "fork", repo, "--remote=true", "--remote-name=skill-lab-fork"], cwd=worktree, check=False)
            run(["git", "push", "-u", "skill-lab-fork", branch], cwd=worktree)
            login = gh_json(["api", "user", "--jq", ".login"])
            head = f"{login}:{branch}"

        if no_pr:
            print(f"\nPushed {head}. Open the PR against {repo}:{base} when ready.")
            return 0

        title = f"{verb} {draft.name} skill"
        body = (
            f"{verb}s `skills/{draft.name}/SKILL.md`, proposed from daily work via `skill-lab-sync`.\n\n"
            f"**Category:** {draft.category}\n\n**Description:** {draft.description}\n\n"
            "Checklist (from docs/SKILL_STANDARD.md):\n"
            "- [ ] no near-duplicate in CATALOG.md\n- [ ] style- and model-neutral, no project or client specifics\n"
            "- [ ] every principle has a reason; pitfalls and verification included\n- [ ] validate.py and build_catalog.py run clean\n"
        )
        run(["gh", "pr", "create", "--repo", repo, "--base", base, "--head", head, "--title", title, "--body", body], cwd=worktree)
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, check=False)
        shutil.rmtree(tmp, ignore_errors=True)
        # The local branch has done its job: a dry run discards it, a real run has pushed it.
        run(["git", "branch", "-D", branch], cwd=ROOT, check=False, capture=True)


# --------------------------------------------------------------------------- cli


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compare", help="classify candidates as existing / extend / new")
    c.add_argument("candidates", nargs="*", help='"name: description" or free text, one per argument')
    c.add_argument("--file", help="read candidates from a file, one per non-empty line")
    c.add_argument("--catalog", help="catalog.json path or URL (default: this clone, else the public raw URL)")
    c.add_argument("--json", action="store_true", help="machine-readable output")

    q = sub.add_parser("propose", help="validate a finished SKILL.md and open a pull request for it")
    q.add_argument("skill_md", help="path to the drafted SKILL.md (its folder may hold references/, scripts/, examples/)")
    q.add_argument("--dry-run", action="store_true", help="validate and commit locally; do not push or open a PR")
    q.add_argument("--no-pr", action="store_true", help="push the branch but do not open the PR")
    q.add_argument("--extend", action="store_true", help="the skill exists; propose this file as its replacement")
    q.add_argument("--repo", default=UPSTREAM, help=f"upstream owner/name (default {UPSTREAM})")
    q.add_argument("--base", default="main", help="base branch (default main)")

    a = p.parse_args(argv)
    if a.cmd == "compare":
        cands = list(a.candidates)
        if a.file:
            cands += [l for l in Path(a.file).read_text(encoding="utf-8").splitlines() if l.strip() and not l.lstrip().startswith("#")]
        if not cands:
            p.error("give at least one candidate or --file")
        return compare(cands, a.catalog, a.json)
    return propose(Path(a.skill_md).resolve(), a.dry_run, a.no_pr, a.extend, a.repo, a.base)


if __name__ == "__main__":
    sys.exit(main())
