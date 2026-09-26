#!/usr/bin/env python3
"""Search the local theory corpus with SQLite FTS5."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sqlite3


SKILL_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = SKILL_ROOT / "research" / ".local-corpus" / "corpus.sqlite3"


def fts_expression(query: str) -> str:
    terms = re.findall(r"[\w-]+", query, flags=re.UNICODE)
    return " OR ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    if not INDEX_PATH.exists():
        raise SystemExit(
            "Corpus index not found. Run: uv run --with pypdf python scripts/build_corpus.py"
        )

    connection = sqlite3.connect(INDEX_PATH)
    connection.row_factory = sqlite3.Row
    expression = fts_expression(args.query)
    if not expression:
        raise SystemExit("Query contains no searchable terms")
    rows = connection.execute(
        """
        SELECT c.source_id, s.title, c.chunk_id, c.location,
               snippet(chunks_fts, 3, '[', ']', ' … ', 28) AS excerpt,
               bm25(chunks_fts) AS score
        FROM chunks_fts AS c
        JOIN sources AS s ON s.source_id = c.source_id
        WHERE chunks_fts MATCH ?
        ORDER BY score
        LIMIT ?
        """,
        (expression, args.limit),
    ).fetchall()
    connection.close()

    for index, row in enumerate(rows, start=1):
        print(f"{index}. {row['title']} — {row['location']} — chunk {row['chunk_id']}")
        print(f"   {row['excerpt']}")
    if not rows:
        print("No matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
