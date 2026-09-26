#!/usr/bin/env python3
"""Validate the publishable AI Communication Coach package."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "evals/behavioral-cases.json",
    "references/diagnostic-framework.md",
    "references/examples.md",
    "references/learning-loop.md",
    "references/theory-foundations.md",
    "research/corpus-manifest.json",
    "scripts/build_corpus.py",
    "scripts/search_corpus.py",
}
LINK_RE = re.compile(r"(?<!!)\[[^]\n]+\]\(([^)\n]+)\)")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_required_files() -> None:
    missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
    require(not missing, f"Missing required files: {', '.join(missing)}")


def validate_skill_metadata() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    _, frontmatter, _ = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)
    require(metadata.get("name") == "ai-communication-coach", "Unexpected Skill name")
    require(bool(metadata.get("description")), "Skill description is required")

    agent = yaml.safe_load((ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
    require(agent["interface"]["default_prompt"].startswith("Use $ai-communication-coach"), "Default prompt must invoke the Skill")
    require(agent["policy"]["allow_implicit_invocation"] is True, "Implicit invocation must stay explicit")


def validate_python() -> None:
    scripts = sorted((ROOT / "scripts").glob("*.py"))
    for path in scripts:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def validate_behavior_cases() -> None:
    data = json.loads((ROOT / "evals/behavioral-cases.json").read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    require(cases, "Behavioral cases are required")
    ids = [case.get("id") for case in cases]
    require(len(ids) == len(set(ids)), "Behavioral case IDs must be unique")
    required = {"id", "state", "prompt", "expected", "critical_failure"}
    for case in cases:
        missing = required - case.keys()
        require(not missing, f"Case {case.get('id', '<unknown>')} is missing: {sorted(missing)}")
        require(bool(case["expected"]), f"Case {case['id']} has no expected behavior")


def validate_manifest() -> None:
    data = json.loads((ROOT / "research/corpus-manifest.json").read_text(encoding="utf-8"))
    sources = data.get("sources", [])
    require(sources, "Corpus manifest must contain sources")
    ids = [source.get("id") for source in sources]
    require(len(ids) == len(set(ids)), "Corpus source IDs must be unique")
    for source in sources:
        require(source.get("title") and source.get("url"), f"Incomplete source: {source.get('id')}")
        require(source.get("redistribution"), f"Missing redistribution status: {source.get('id')}")


def validate_links() -> None:
    missing: list[str] = []
    for markdown in ROOT.rglob("*.md"):
        if ".local-corpus" in markdown.parts:
            continue
        for target in LINK_RE.findall(markdown.read_text(encoding="utf-8")):
            clean = target.split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            if not (markdown.parent / clean).resolve().exists():
                missing.append(f"{markdown.relative_to(ROOT)} -> {clean}")
    require(not missing, "Broken local Markdown links: " + "; ".join(missing))


def validate_distribution_boundary() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    require("research/.local-corpus/" in ignore, "Private corpus cache must remain Git-ignored")
    require(not (ROOT / "research/.local-corpus").is_symlink(), "Local corpus cache cannot be a symlink")


def main() -> int:
    checks = [
        validate_required_files,
        validate_skill_metadata,
        validate_python,
        validate_behavior_cases,
        validate_manifest,
        validate_links,
        validate_distribution_boundary,
    ]
    try:
        for check in checks:
            check()
    except (ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    case_count = len(json.loads((ROOT / "evals/behavioral-cases.json").read_text(encoding="utf-8"))["cases"])
    source_count = len(json.loads((ROOT / "research/corpus-manifest.json").read_text(encoding="utf-8"))["sources"])
    print(f"Skill package is valid: {case_count} behavioral cases, {source_count} theory sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
