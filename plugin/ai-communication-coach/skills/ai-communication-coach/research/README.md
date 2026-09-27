# Local Theory Corpus

This directory defines a private, rebuildable source corpus for deeper theory checks.

## Storage model

- `corpus-manifest.json` is safe to publish. It records titles, source URLs, access level, and redistribution status.
- `.local-corpus/raw/` contains downloaded PDFs or official web pages.
- `.local-corpus/text/` contains extracted plain text.
- `.local-corpus/chunks/` contains page-aware or page-level JSONL chunks.
- `.local-corpus/corpus.sqlite3` contains a SQLite FTS5 full-text index.
- `.local-corpus/build-report.json` records retrieval results, hashes, text size, and failures.

The entire `.local-corpus/` directory is ignored by Git. Its contents are for local research and should not be pushed to a public repository unless each source's redistribution rights are checked separately.

## Build

From the Skill root:

```bash
uv run --with pypdf --with fonttools --with certifi python scripts/build_corpus.py
```

This command requires `uv` and installs the Python dependencies in an isolated environment for the run. Use `--refresh` to retrieve sources again.

Text-based PDFs need no additional tools. When a PDF contains scanned pages and text extraction is too sparse, the builder uses `pdftoppm` and `tesseract` for OCR; install those system commands only when that fallback is needed.

## Search

```bash
python3 scripts/search_corpus.py 'grounding collaborative effort'
python3 scripts/search_corpus.py 'claim warrant qualifier'
```

The current corpus uses keyword ranking through SQLite FTS5. This is enough for eleven known sources because `theory-foundations.md` already routes each diagnostic problem to the right source family.

The current local access mix is explicit:

- 5 public, open-access, or author-hosted full-text PDFs;
- 1 university-hosted book excerpt;
- 1 public standard preview PDF;
- 3 official publisher or journal pages containing abstracts, previews, or detailed overviews;
- 1 curated local source note based on an official public standard preview.

All eleven theory entries are searchable offline. A searchable entry does not imply that the complete copyrighted work is present.

## When embeddings become useful

Add a vector index only after one of these conditions appears:

- the corpus grows to dozens of long documents or roughly one million tokens;
- users repeatedly phrase the same concept in vocabulary absent from the sources;
- keyword retrieval misses relevant passages in an evaluated query set;
- cross-source semantic comparison becomes a frequent workflow.

At that point, keep the source registry in SQLite and add embeddings per chunk with source, page, section, hash, and access metadata. Use hybrid retrieval: metadata filtering plus keyword ranking plus vector similarity. Do not replace the curated theory cards or the original-source links with embeddings.
