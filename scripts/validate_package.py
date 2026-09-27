#!/usr/bin/env python3
"""Validate the publishable AI Communication Coach package."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "README.en.md",
    "VERSION",
    "LICENSE",
    "PRIVACY.md",
    "SECURITY.md",
    "SUPPORT.md",
    "TERMS.md",
    ".agents/plugins/marketplace.json",
    "agents/openai.yaml",
    "docs/plugin-submission.md",
    "docs/release-readiness-v0.2.md",
    "docs/release-verification-v0.2.md",
    "evals/behavioral-cases.json",
    "evals/real-conversation-cases.json",
    "evals/runs/2026-09-27-gpt-6-luna.md",
    "evals/runs/2026-09-27-cross-model-context.md",
    "evals/runs/2026-09-27-multiturn-workspaces.md",
    "evals/runs/2026-09-27-release-artifact.md",
    "packaging/plugin.json",
    "packaging/codex-plugin.json",
    "packaging/plugin.schema.json",
    "plugin/ai-communication-coach/plugin.json",
    "plugin/ai-communication-coach/.codex-plugin/plugin.json",
    "references/diagnostic-framework.md",
    "references/examples.md",
    "references/learning-loop.md",
    "references/theory-foundations.md",
    "research/corpus-manifest.json",
    "scripts/build_corpus.py",
    "scripts/build_plugin.py",
    "scripts/run_model_eval.py",
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


def validate_case_file(relative_path: str) -> int:
    data = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    require(cases, f"Cases are required in {relative_path}")
    ids = [case.get("id") for case in cases]
    require(len(ids) == len(set(ids)), f"Case IDs must be unique in {relative_path}")
    required = {"id", "state", "prompt", "expected", "critical_failure"}
    for case in cases:
        missing = required - case.keys()
        require(not missing, f"Case {case.get('id', '<unknown>')} is missing: {sorted(missing)}")
        require(bool(case["expected"]), f"Case {case['id']} has no expected behavior")
    return len(cases)


def validate_behavior_cases() -> None:
    validate_case_file("evals/behavioral-cases.json")
    validate_case_file("evals/real-conversation-cases.json")


def validate_manifest() -> None:
    data = json.loads((ROOT / "research/corpus-manifest.json").read_text(encoding="utf-8"))
    sources = data.get("sources", [])
    require(sources, "Corpus manifest must contain sources")
    ids = [source.get("id") for source in sources]
    require(len(ids) == len(set(ids)), "Corpus source IDs must be unique")
    for source in sources:
        require(source.get("title") and source.get("url"), f"Incomplete source: {source.get('id')}")
        require(source.get("redistribution"), f"Missing redistribution status: {source.get('id')}")


def validate_plugin_package() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    require(re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "VERSION must use strict semantic versioning")

    schema = json.loads((ROOT / "packaging/plugin.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    canonical = json.loads((ROOT / "packaging/plugin.json").read_text(encoding="utf-8"))
    errors = sorted(validator.iter_errors(canonical), key=lambda error: list(error.path))
    require(not errors, "Portable plugin manifest is invalid: " + "; ".join(error.message for error in errors))
    require(canonical.get("version") == version, "Portable plugin version must match VERSION")

    plugin_root = ROOT / "plugin/ai-communication-coach"
    bundled = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
    require(bundled == canonical, "Bundled portable manifest is not synchronized")

    extension = canonical["extensions"]["com.openai"]
    interface = extension["interface"]
    required_interface = {
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "websiteURL",
        "privacyPolicyURL",
        "termsOfServiceURL",
        "defaultPrompt",
        "brandColor",
        "composerIcon",
        "logo",
        "screenshots",
    }
    require(not (required_interface - interface.keys()), "OpenAI plugin interface metadata is incomplete")
    prompts = interface["defaultPrompt"]
    require(1 <= len(prompts) <= 3, "Plugin must provide one to three starter prompts")
    require(all(len(prompt) <= 128 for prompt in prompts), "Plugin starter prompts must not exceed 128 characters")
    for url_key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(urlparse(interface[url_key]).scheme == "https", f"{url_key} must use HTTPS")
    asset_paths = [interface["composerIcon"], interface["logo"], *interface["screenshots"]]
    for relative in asset_paths:
        require(relative.startswith("./assets/"), f"Plugin asset must be under ./assets/: {relative}")
        require((plugin_root / relative.removeprefix("./")).is_file(), f"Missing plugin asset: {relative}")

    overlay = json.loads((ROOT / "packaging/codex-plugin.json").read_text(encoding="utf-8"))
    bundled_overlay = json.loads((plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    require(overlay == bundled_overlay, "Bundled Codex compatibility manifest is not synchronized")
    require(overlay.get("version") == version, "Codex compatibility version must match VERSION")
    require(overlay.get("skills") == "./skills/", "Codex compatibility manifest must discover skills")

    skill_root = plugin_root / "skills/ai-communication-coach"
    require((skill_root / "SKILL.md").is_file(), "Portable plugin is missing its Skill")
    require((skill_root / "SKILL.md").read_bytes() == (ROOT / "SKILL.md").read_bytes(), "Bundled SKILL.md is stale")

    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entries = marketplace.get("plugins", [])
    matches = [entry for entry in entries if entry.get("name") == "ai-communication-coach"]
    require(len(matches) == 1, "Marketplace must contain one ai-communication-coach entry")
    require(matches[0]["source"] == {"source": "local", "path": "./plugin/ai-communication-coach"}, "Unexpected marketplace source")


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
        validate_plugin_package,
        validate_links,
        validate_distribution_boundary,
    ]
    try:
        for check in checks:
            check()
    except (ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    case_count = validate_case_file("evals/behavioral-cases.json")
    real_case_count = validate_case_file("evals/real-conversation-cases.json")
    source_count = len(json.loads((ROOT / "research/corpus-manifest.json").read_text(encoding="utf-8"))["sources"])
    print(
        f"Skill package is valid: {case_count} general cases, "
        f"{real_case_count} real-conversation cases, {source_count} theory sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
