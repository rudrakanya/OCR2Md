#!/usr/bin/env python
"""Append-only, lexical ingest for the Udaypur KB.

WHY THIS EXISTS
    Three reference books were never indexed: Geo-Heritage (INTACH), Anupa
    Pande's full monograph, and the Skanda-Purāṇa. The normal path,
    build_kb.py, cannot run: it imports `dotenv` and `mistralai` at module
    level (both uninstalled) and its embed_all() needs a Mistral key whose
    quota is spent.

    But dense retrieval is already dead — every query in this project is
    lexical BM25 over chunks_fts. So the books can be made fully searchable
    without touching the embedding side at all.

WHAT IT DOES NOT DO
    It does not call KBStore.build(). build() begins with `DELETE FROM chunks`
    and `DROP TABLE chunks_fts` — a full rebuild — which would destroy the
    9,467 existing rows. This appends instead.

THE ONE INVARIANT
    chunks.rowid order is the join key to embeddings.npy row order. New rows
    are appended strictly ABOVE the current maximum rowid (9466), so every
    pre-existing row keeps its index. The new rows have no embedding, which is
    harmless: nothing can query them densely, and the dense path is dead.

    Contentless FTS5 (content='') rejects DELETE but accepts INSERT, which is
    exactly why append works where rebuild would not.

    New chunks get no chunk_labels row. That is deliberate and correct: the
    retrievable gate reads `(lb.retrievable IS NULL OR lb.retrievable = 1)`,
    so unlabelled chunks are admitted rather than silently filtered out.

    python kb_append_lexical.py --dry-run
    python kb_append_lexical.py
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import kb_store

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

REF = Path(r"C:\Users\CBIC\Desktop\markdown extractor\Udaypur Reference Markdown Files")
TARGETS = [
    "Geo-Heritage of Udaypur - The Third Eye.md",
    "The Udayesvara Temple - Anupa Pande.md",
    "467921465-Skanda-Purana-13-AITM.md",
]

# Match the stored corpus: build_kb used max_chars 1800 / overlap 270.
MAX_CHARS, OVERLAP, MIN_CHARS = 1800, 270, 200

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def chunk_markdown(path: Path):
    """Split one markdown file into records shaped like chunks.jsonl rows."""
    text = unicodedata.normalize("NFC", path.read_text(encoding="utf-8", errors="replace"))
    stack: list[str] = []
    page: int | None = None
    blocks: list[dict] = []
    buf: list[str] = []
    cur_trail, cur_page = "", None

    def flush():
        nonlocal buf, cur_trail, cur_page
        body = "\n".join(buf).strip()
        buf = []
        if len(body) < MIN_CHARS:
            return
        for piece in split_long(body):
            blocks.append({"trail": cur_trail, "heading": stack[-1] if stack else "",
                           "page_start": cur_page, "text": piece})

    def split_long(body: str):
        if len(body) <= MAX_CHARS:
            return [body]
        out, start = [], 0
        while start < len(body):
            end = min(start + MAX_CHARS, len(body))
            if end < len(body):                       # break on a sentence/space
                cut = body.rfind(". ", start + MIN_CHARS, end)
                if cut == -1:
                    cut = body.rfind(" ", start + MIN_CHARS, end)
                if cut != -1:
                    end = cut + 1
            out.append(body[start:end].strip())
            if end >= len(body):
                break
            start = max(end - OVERLAP, start + 1)
        return [o for o in out if len(o) >= MIN_CHARS // 2]

    for line in text.splitlines():
        m_page = PAGE_RE.search(line)
        if m_page:
            page = int(m_page.group(1))
        m = HEADING_RE.match(line)
        if m:
            flush()
            level, title = len(m.group(1)), COMMENT_RE.sub("", m.group(2)).strip()
            if title:
                stack = stack[: level - 1]
                while len(stack) < level - 1:
                    stack.append("")
                stack.append(title)
                cur_trail = " > ".join(h for h in stack if h)
                cur_page = page
            continue
        if not buf:
            cur_page = page
            cur_trail = " > ".join(h for h in stack if h)
        buf.append(line)
        if sum(len(x) for x in buf) > MAX_CHARS * 2:
            flush()
    flush()
    return blocks


def load_alias_map(db) -> dict:
    """{folded_alias: [entity_id, ...]} straight from entity_aliases."""
    am: dict[str, list[str]] = {}
    for eid, _alias, folded in db.execute(
            "SELECT entity_id, alias, folded FROM entity_aliases"):
        if folded:
            am.setdefault(folded, []).append(eid)
    return am


def main(argv=None):
    ap = argparse.ArgumentParser(description="Append missing books to the KB (lexical only)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--files", nargs="*", default=TARGETS)
    args = ap.parse_args(argv)

    st = kb_store.KBStore()
    db = st.db
    alias_map = load_alias_map(db)
    print(f"alias map: {len(alias_map)} folded aliases")

    already = {r[0] for r in db.execute("SELECT DISTINCT source FROM chunks")}
    start_rowid = db.execute("SELECT MAX(rowid) FROM chunks").fetchone()[0] + 1
    print(f"existing chunks: {start_rowid}  (appending from rowid {start_rowid})\n")

    total = 0
    rowid = start_rowid
    for name in args.files:
        path = REF / name
        if not path.exists():
            print(f"  !! MISSING FILE: {name}")
            continue
        if name in already:
            print(f"  -- already indexed, skipping: {name}")
            continue
        recs = chunk_markdown(path)
        print(f"  {name[:56]:58s} -> {len(recs):>4} chunks")
        total += len(recs)
        if args.dry_run:
            continue
        with db:
            for i, c in enumerate(recs):
                db.execute(
                    "INSERT INTO chunks (rowid, source, chunk, trail, heading,"
                    " page_start, page_end, text, context) VALUES (?,?,?,?,?,?,?,?,?)",
                    (rowid, name, i, c["trail"], c["heading"],
                     c["page_start"], None, c["text"], ""))
                searchable = f"{c['trail']}\n{c['text']}"
                ents, ids = st._entity_stream(searchable, alias_map)
                db.execute(
                    "INSERT INTO chunks_fts (rowid, raw, folded, deva, ents)"
                    " VALUES (?,?,?,?,?)",
                    (rowid, searchable.lower(), kb_store.fold_text(searchable),
                     kb_store.devanagari_only(c["text"]), ents))
                for eid, n in ids.items():
                    db.execute("INSERT OR REPLACE INTO entity_mentions"
                               " (entity_id, chunk_id, n) VALUES (?,?,?)", (eid, rowid, n))
                rowid += 1

    print(f"\n{'DRY RUN — nothing written. ' if args.dry_run else ''}"
          f"{total} chunks {'would be' if args.dry_run else ''} appended")
    if not args.dry_run:
        print("post-append chunks:",
              db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0],
              "| sources:",
              db.execute("SELECT COUNT(DISTINCT source) FROM chunks").fetchone()[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
