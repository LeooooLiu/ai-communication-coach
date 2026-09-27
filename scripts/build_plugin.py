#!/usr/bin/env python3
"""Build and verify the portable skills-only Agent Plugin release tree."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "ai-communication-coach"
TRACKED_PLUGIN = ROOT / "plugin" / PLUGIN_NAME
DEFAULT_ARCHIVE = ROOT / "dist" / f"{PLUGIN_NAME}-plugin-v{(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}.zip"

ROOT_FILES = (
    "LICENSE",
    "PRIVACY.md",
    "SECURITY.md",
    "SUPPORT.md",
    "TERMS.md",
)
SKILL_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/diagnostic-framework.md",
    "references/examples.md",
    "references/learning-loop.md",
    "references/theory-foundations.md",
    "research/README.md",
    "research/corpus-manifest.json",
    "research/source-notes/iso-29148-2018.md",
    "scripts/build_corpus.py",
    "scripts/search_corpus.py",
)
ASSET_FILES = (
    "assets/plugin-icon.png",
    "assets/plugin-logo.png",
    "assets/plugin-screenshot.png",
)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def render_plugin(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    copy_file(ROOT / "packaging/plugin.json", target / "plugin.json")
    copy_file(ROOT / "packaging/codex-plugin.json", target / ".codex-plugin/plugin.json")

    for relative in ROOT_FILES:
        copy_file(ROOT / relative, target / relative)
    for relative in ASSET_FILES:
        copy_file(ROOT / relative, target / relative)

    skill_root = target / "skills" / PLUGIN_NAME
    for relative in SKILL_FILES:
        copy_file(ROOT / relative, skill_root / relative)


def file_map(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def compare_plugin(expected: Path, actual: Path) -> list[str]:
    expected_files = file_map(expected)
    actual_files = file_map(actual)
    messages: list[str] = []
    for path in sorted(expected_files.keys() - actual_files.keys()):
        messages.append(f"missing: {path}")
    for path in sorted(actual_files.keys() - expected_files.keys()):
        messages.append(f"unexpected: {path}")
    for path in sorted(expected_files.keys() & actual_files.keys()):
        if expected_files[path] != actual_files[path]:
            messages.append(f"stale: {path}")
    return messages


def write_archive(plugin_root: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(plugin_root.rglob("*")):
            if not path.is_file():
                continue
            relative = Path(PLUGIN_NAME) / path.relative_to(plugin_root)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes(), compresslevel=9)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare the tracked plugin tree with canonical sources")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE, help="Output ZIP path")
    parser.add_argument("--no-archive", action="store_true", help="Update the tracked tree without creating a ZIP")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="ai-communication-coach-plugin-") as directory:
            expected = Path(directory) / PLUGIN_NAME
            render_plugin(expected)
            differences = compare_plugin(expected, TRACKED_PLUGIN)
        if differences:
            print("Plugin tree is out of date:")
            for difference in differences:
                print(f"- {difference}")
            return 1
        print(f"Plugin tree is synchronized: {len(file_map(TRACKED_PLUGIN))} files.")
        return 0

    render_plugin(TRACKED_PLUGIN)
    print(f"Built tracked plugin: {TRACKED_PLUGIN}")
    if not args.no_archive:
        archive = args.archive.resolve()
        write_archive(TRACKED_PLUGIN, archive)
        print(f"Built release archive: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
