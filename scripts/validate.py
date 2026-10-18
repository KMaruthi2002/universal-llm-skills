#!/usr/bin/env python3
"""Validate every skill against docs/SKILL_STANDARD.md.

Usage:  python3 scripts/validate.py [--strict]

Errors (always fatal): missing/invalid frontmatter, name/folder mismatch,
unknown category, over-long description, broken `related` links, duplicate names.
Warnings (fatal with --strict): thin bodies, missing "use when" guidance,
broken links to files under the skill folder.
"""

from __future__ import annotations

import re
import sys

from skilllib import CATEGORIES, NAME_RE, ROOT, load_all

MIN_LINES = 120


def main() -> int:
    strict = "--strict" in sys.argv
    skills = load_all()
    names = {s.name for s in skills}
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for s in skills:
        where = s.rel_path
        errors += [f"{where}: {e}" for e in s.errors]
        if not s.name:
            errors.append(f"{where}: missing `name`")
        elif not NAME_RE.match(s.name) or len(s.name) > 64:
            errors.append(f"{where}: invalid name {s.name!r}")
        if s.name and s.name != s.folder:
            errors.append(f"{where}: name {s.name!r} does not match folder {s.folder!r}")
        if s.name in seen:
            errors.append(f"{where}: duplicate name {s.name!r}")
        seen.add(s.name)

        if not s.description:
            errors.append(f"{where}: missing `description`")
        elif len(s.description) > 1024:
            errors.append(f"{where}: description is {len(s.description)} chars (max 1024)")
        elif "use when" not in s.description.lower() and "use for" not in s.description.lower():
            warnings.append(f"{where}: description has no 'Use when…' trigger guidance")

        if s.category not in CATEGORIES:
            errors.append(f"{where}: unknown category {s.category!r}")

        for r in s.related:
            if r not in names:
                errors.append(f"{where}: related skill {r!r} does not exist")
            if r == s.name:
                warnings.append(f"{where}: lists itself as related")

        body_lines = [l for l in s.body.splitlines() if l.strip()]
        if len(body_lines) < MIN_LINES:
            warnings.append(f"{where}: body is thin ({len(body_lines)} non-empty lines, expected ≥{MIN_LINES})")

        # Relative links inside the skill folder (e.g. references/foo.md) must resolve.
        for target in re.findall(r"\]\(((?:references|scripts|examples)/[^)#\s]+)", s.body):
            if not (s.path.parent / target).exists():
                warnings.append(f"{where}: broken link to {target}")

    for line in errors:
        print(f"ERROR   {line}")
    for line in warnings:
        print(f"WARNING {line}")
    total_lines = sum(len(s.body.splitlines()) for s in skills)
    print(f"\n{len(skills)} skills, {total_lines} body lines, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "scripts"))
    sys.exit(main())
