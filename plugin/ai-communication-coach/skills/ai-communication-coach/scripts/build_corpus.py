#!/usr/bin/env python3
"""Build the private local source cache and SQLite FTS5 index.

Run with:
  uv run --with pypdf python scripts/build_corpus.py
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import logging
from pathlib import Path
import re
import sqlite3
import ssl
import subprocess
import sys
import tempfile
import urllib.request

import certifi
from pypdf import PdfReader


logging.getLogger("pypdf").setLevel(logging.ERROR)


SKILL_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = SKILL_ROOT / "research"
MANIFEST_PATH = RESEARCH_ROOT / "corpus-manifest.json"
CORPUS_ROOT = RESEARCH_ROOT / ".local-corpus"
RAW_ROOT = CORPUS_ROOT / "raw"
TEXT_ROOT = CORPUS_ROOT / "text"
CHUNK_ROOT = CORPUS_ROOT / "chunks"
INDEX_PATH = CORPUS_ROOT / "corpus.sqlite3"
REPORT_PATH = CORPUS_ROOT / "build-report.json"


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {
        "article", "blockquote", "br", "div", "h1", "h2", "h3", "h4",
        "h5", "h6", "header", "li", "main", "p", "section", "table",
        "td", "th", "tr"
    }
    SKIP_TAGS = {"script", "style", "svg", "noscript"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if tag in self.BLOCK_TAGS and not self.skip_depth:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag in self.BLOCK_TAGS and not self.skip_depth:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts))
        value = re.sub(r"[\t\r\f\v ]+", " ", value)
        value = re.sub(r" *\n *", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 AICommunicationCoachCorpus/1.0",
            "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
        },
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=45, context=context) as response:
        return response.read(), response.headers.get("Content-Type", "")


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.name)]


def ocr_pdf(path: Path) -> tuple[str, list[dict[str, str]]]:
    with tempfile.TemporaryDirectory(prefix="ai-communication-ocr-") as temporary:
        prefix = Path(temporary) / "page"
        subprocess.run(
            ["pdftoppm", "-r", "220", "-png", str(path), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        pages: list[dict[str, str]] = []
        blocks: list[str] = []
        for index, image_path in enumerate(sorted(Path(temporary).glob("page-*.png"), key=natural_key), start=1):
            result = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", "6"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            page_text = result.stdout.strip()
            pages.append({"location": f"page {index} (OCR)", "text": page_text})
            blocks.append(f"\n\n--- page {index} (OCR) ---\n\n{page_text}")
        return "".join(blocks).strip(), pages


def extract_pdf(path: Path, minimum_chars: int) -> tuple[str, list[dict[str, str]]]:
    reader = PdfReader(str(path))
    pages: list[dict[str, str]] = []
    blocks: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        pages.append({"location": f"page {index}", "text": page_text})
        blocks.append(f"\n\n--- page {index} ---\n\n{page_text}")
    extracted = "".join(blocks).strip()
    if len(re.sub(r"\s+", "", extracted)) < minimum_chars:
        print(f"OCR  {path.name}: embedded text is insufficient")
        return ocr_pdf(path)
    return extracted, pages


def extract_html(raw: bytes) -> tuple[str, list[dict[str, str]]]:
    decoded = raw.decode("utf-8", errors="replace")
    parser = TextExtractor()
    parser.feed(decoded)
    text = parser.text()
    return text, [{"location": "official page", "text": text}]


def extract_local_markdown(raw: bytes) -> tuple[str, list[dict[str, str]]]:
    text = raw.decode("utf-8", errors="replace").strip()
    return text, [{"location": "curated source note", "text": text}]


def split_chunks(blocks: list[dict[str, str]], target_chars: int = 1800, overlap_chars: int = 220) -> list[dict[str, str | int]]:
    chunks: list[dict[str, str | int]] = []
    chunk_number = 0
    for block in blocks:
        text = re.sub(r"\s+", " ", block["text"]).strip()
        if not text:
            continue
        start = 0
        while start < len(text):
            end = min(len(text), start + target_chars)
            if end < len(text):
                boundary = text.rfind(" ", start + target_chars // 2, end)
                if boundary > start:
                    end = boundary
            chunk_number += 1
            chunks.append(
                {
                    "chunk_id": chunk_number,
                    "location": block["location"],
                    "text": text[start:end].strip(),
                }
            )
            if end >= len(text):
                break
            start = max(start + 1, end - overlap_chars)
    return chunks


def init_database() -> sqlite3.Connection:
    if INDEX_PATH.exists():
        INDEX_PATH.unlink()
    connection = sqlite3.connect(INDEX_PATH)
    connection.execute(
        """
        CREATE TABLE sources (
            source_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            year INTEGER NOT NULL,
            kind TEXT NOT NULL,
            access_level TEXT NOT NULL,
            source_url TEXT NOT NULL,
            local_raw_path TEXT,
            local_text_path TEXT,
            sha256 TEXT,
            content_chars INTEGER NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            source_id UNINDEXED,
            chunk_id UNINDEXED,
            location UNINDEXED,
            text,
            tokenize = 'unicode61 remove_diacritics 2'
        )
        """
    )
    return connection


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Download files again")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for directory in (RAW_ROOT, TEXT_ROOT, CHUNK_ROOT):
        directory.mkdir(parents=True, exist_ok=True)

    connection = init_database()
    report: dict[str, object] = {"sources": [], "required_failures": []}

    for source in manifest["sources"]:
        source_id = source["id"]
        raw_path = RAW_ROOT / source["filename"]
        text_path = TEXT_ROOT / f"{source_id}.txt"
        chunks_path = CHUNK_ROOT / f"{source_id}.jsonl"
        entry: dict[str, object] = {"id": source_id}
        try:
            reuse_derived = (
                not args.refresh
                and source["format"] != "local_markdown"
                and raw_path.exists()
                and text_path.exists()
                and chunks_path.exists()
            )
            if reuse_derived:
                payload = raw_path.read_bytes()
                content_type = "cached"
                extracted_text = text_path.read_text(encoding="utf-8")
                chunks = [
                    json.loads(line)
                    for line in chunks_path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
            else:
                if source["format"] == "local_markdown":
                    local_source = SKILL_ROOT / source["local_source"]
                    payload = local_source.read_bytes()
                    content_type = "text/markdown; local curated note"
                    raw_path.write_bytes(payload)
                elif args.refresh or not raw_path.exists():
                    payload, content_type = download(source["url"])
                    if source["format"] == "pdf" and not payload.startswith(b"%PDF"):
                        raise ValueError(f"expected PDF, got {content_type or 'unknown content type'}")
                    raw_path.write_bytes(payload)
                else:
                    payload = raw_path.read_bytes()
                    content_type = "cached"

                if source["format"] == "pdf":
                    extracted_text, blocks = extract_pdf(raw_path, source.get("min_text_chars", 1000))
                elif source["format"] == "local_markdown":
                    extracted_text, blocks = extract_local_markdown(payload)
                else:
                    extracted_text, blocks = extract_html(payload)

                text_path.write_text(extracted_text, encoding="utf-8")
                chunks = split_chunks(blocks)
                with chunks_path.open("w", encoding="utf-8") as output:
                    for chunk in chunks:
                        output.write(json.dumps(chunk, ensure_ascii=False) + "\n")

            if len(re.sub(r"\s+", "", extracted_text)) < source.get("min_text_chars", 1000):
                raise ValueError(
                    f"extracted text below minimum: {len(extracted_text)} < {source.get('min_text_chars', 1000)}"
                )

            digest = hashlib.sha256(payload).hexdigest()
            source_status = "curated_local" if source["format"] == "local_markdown" else "downloaded"
            connection.execute(
                "INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    source_id,
                    source["title"],
                    source["authors"],
                    source["year"],
                    source["kind"],
                    source["access_level"],
                    source["url"],
                    str(raw_path),
                    str(text_path),
                    digest,
                    len(extracted_text),
                    source_status,
                ),
            )
            connection.executemany(
                "INSERT INTO chunks_fts(source_id, chunk_id, location, text) VALUES (?, ?, ?, ?)",
                [
                    (source_id, chunk["chunk_id"], chunk["location"], chunk["text"])
                    for chunk in chunks
                ],
            )
            entry.update(
                {
                    "status": source_status,
                    "content_type": content_type,
                    "bytes": len(payload),
                    "text_chars": len(extracted_text),
                    "chunks": len(chunks),
                    "sha256": digest,
                }
            )
            print(f"OK   {source_id}: {len(extracted_text):,} chars, {len(chunks)} chunks")
        except Exception as error:  # keep other sources buildable and report exact failures
            entry.update({"status": "failed", "error": str(error)})
            connection.execute(
                "INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, 0, ?)",
                (
                    source_id,
                    source["title"],
                    source["authors"],
                    source["year"],
                    source["kind"],
                    source["access_level"],
                    source["url"],
                    "failed",
                ),
            )
            if source.get("required"):
                report["required_failures"].append(source_id)
            print(f"FAIL {source_id}: {error}", file=sys.stderr)
        report["sources"].append(entry)

    connection.commit()
    connection.close()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    failures = report["required_failures"]
    print(f"\nIndex: {INDEX_PATH}")
    print(f"Report: {REPORT_PATH}")
    if failures:
        print(f"Required downloads failed: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
