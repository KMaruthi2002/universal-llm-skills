"""Shared helpers for reading skills. Standard library only, so the scripts run anywhere."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

CATEGORIES = {
    "meta": "Meta: how to work",
    "development": "Development",
    "devops": "DevOps and operations",
    "ai-ml": "AI, LLMs and machine learning",
    "app-generation": "Application generation",
    "analysis": "Analysis and research",
    "quality": "Quality, testing and reviews",
    "design": "Design, UI and UX",
    "automation": "Automation",
    "product-and-communication": "Product, writing and communication",
}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class Skill:
    path: Path
    name: str = ""
    description: str = ""
    category: str = ""
    related: list[str] = field(default_factory=list)
    body: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def folder(self) -> str:
        return self.path.parent.name

    @property
    def rel_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    @property
    def references(self) -> list[str]:
        ref_dir = self.path.parent / "references"
        if not ref_dir.is_dir():
            return []
        return sorted(p.relative_to(ROOT).as_posix() for p in ref_dir.rglob("*.md"))


def _parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    """Parse the small YAML subset used by SKILL.md frontmatter.

    Supports top-level scalars, folded/literal block scalars (>, >-, |, |-),
    and one level of nested mapping (for `metadata:`). Avoids a PyYAML dependency.
    """
    errors: list[str] = []
    if not text.startswith("---"):
        return {}, text, ["missing frontmatter (file must start with ---)"]
    parts = text.split("\n")
    try:
        end = next(i for i in range(1, len(parts)) if parts[i].strip() == "---")
    except StopIteration:
        return {}, text, ["unterminated frontmatter"]
    lines = parts[1:end]
    body = "\n".join(parts[end + 1 :])

    data: dict = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith(" "):
            errors.append(f"unexpected indentation in frontmatter: {line!r}")
            i += 1
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value in (">", ">-", "|", "|-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            sep = " " if value.startswith(">") else "\n"
            data[key] = sep.join(b for b in block if b).strip()
            continue
        if value == "":
            nested = {}
            i += 1
            while i < len(lines) and lines[i].startswith(" "):
                nk, _, nv = lines[i].strip().partition(":")
                nested[nk.strip()] = nv.strip().strip("'\"")
                i += 1
            data[key] = nested
            continue
        data[key] = value.strip("'\"")
        i += 1
    return data, body, errors


def load_skill(path: Path) -> Skill:
    skill = Skill(path=path)
    text = path.read_text(encoding="utf-8")
    data, body, errors = _parse_frontmatter(text)
    skill.errors.extend(errors)
    skill.body = body
    skill.name = str(data.get("name", ""))
    skill.description = str(data.get("description", ""))
    meta = data.get("metadata", {}) if isinstance(data.get("metadata"), dict) else {}
    skill.category = meta.get("category", "")
    related = meta.get("related", "")
    skill.related = [r.strip() for r in related.split(",") if r.strip()] if related else []
    return skill


def load_all() -> list[Skill]:
    return sorted(
        (load_skill(p) for p in SKILLS_DIR.glob("*/SKILL.md")),
        key=lambda s: (list(CATEGORIES).index(s.category) if s.category in CATEGORIES else 99, s.name),
    )
