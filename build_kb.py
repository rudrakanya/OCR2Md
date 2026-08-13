#!/usr/bin/env python3
"""
build_kb.py — build a local vector knowledge base from Markdown sources.

Chunks every .md file in a source directory, embeds the chunks with Mistral
embeddings (mistral-embed), and persists a simple, dependency-light vector store
under ./kb/ :

    kb/embeddings.npy   float32 [N, dim], L2-normalized (cosine == dot product)
    kb/chunks.jsonl     one record per chunk:
                        {source, trail, heading, chunk, page_start, page_end, text}
    kb/config.json      {model, dim, count, source_dir, built_at, fingerprint}

Source text is run through md_clean.py first, so page markers, image
placeholders, running heads and folio numbers never reach the embedder — while
the page each chunk came from is kept as metadata.

Chunking is heading-aware: every chunk carries the full heading *trail*
(document > chapter > section), is bounded by MAX_CHARS even when the source
puts a whole page on one line, overlaps its predecessor by OVERLAP_CHARS within
a section, and is never shorter than MIN_CHARS (short tails are merged back).

`text` holds the body only. The source/trail header is added at embed time and
by make_evidence.py when it writes a pack — it is stored once, not twice.

It is idempotent: if the sources, model, and chunk settings are unchanged since
the last build, it skips (no re-embedding). Use --force to rebuild anyway.

Query it with kb_search.py.

Requires: mistralai, python-dotenv, numpy ; MISTRAL_API_KEY in .env.
Usage:    python build_kb.py ["Udaypur Reference Markdown Files"] [--force]
"""
import argparse
import glob
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from mistralai.client import Mistral

from md_clean import clean_lines
from config import CFG

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

MODEL = os.environ.get("MISTRAL_EMBED_MODEL", "mistral-embed")
KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
MAX_CHARS = 1800                       # hard ceiling on chunk size (~350-450 words)
MIN_FLUSH = int(MAX_CHARS * 0.6)       # prefer to break at a paragraph past this
OVERLAP_CHARS = int(MAX_CHARS * 0.15)  # 270 — carried between chunks of a section
MIN_CHARS = 200                        # below this a chunk is merged back or dropped
BATCH_TOKENS = 12000      # approx token budget per embed request (chars/4)
BATCH_ITEMS = 64

# Sentence boundaries, including the Devanagari danda. The negative lookbehinds
# keep bibliography abbreviations ("J. A. P. 1910, p. 146") from being carved
# into fragments — each is fixed-width, as Python's re requires.
_SENT_RE = re.compile(
    r"(?<=[.!?;:])"
    r"(?<![A-Z]\.)(?<!\bp\.)(?<!\bpp\.)(?<!\bvol\.)(?<!\bno\.)"
    r"(?<!\bfig\.)(?<!\bcf\.)(?<!\bed\.)(?<!\bch\.)(?<!\bPl\.)"
    r"\s+"
    r"|(?<=।)\s*"
)


def _split_units(text, limit):
    """Break one over-long line into <= limit pieces, at sentence bounds if possible."""
    if len(text) <= limit:
        return [text]
    out, buf = [], ""
    for piece in _SENT_RE.split(text):
        if not piece:
            continue
        if len(piece) > limit:                       # a sentence longer than the limit
            if buf:
                out.append(buf); buf = ""
            words, cur = piece.split(" "), ""
            for w in words:
                if cur and len(cur) + len(w) + 1 > limit:
                    out.append(cur); cur = w
                else:
                    cur = f"{cur} {w}".strip()
            if cur:
                buf = cur
            continue
        if buf and len(buf) + len(piece) + 1 > limit:
            out.append(buf); buf = piece
        else:
            buf = f"{buf} {piece}".strip()
    if buf:
        out.append(buf)
    return out


def _overlap_tail(body, limit):
    """The last whole sentences of `body`, up to `limit` chars — the bridge into
    the next chunk so a thought split across a boundary stays retrievable."""
    if limit <= 0 or not body:
        return ""
    parts = [p for p in _SENT_RE.split(body) if p]
    tail, total = [], 0
    for p in reversed(parts):
        if total + len(p) + 1 > limit and tail:
            break
        tail.insert(0, p)
        total += len(p) + 1
    return " ".join(tail).strip()


def chunk_markdown(path):
    """Split a cleaned markdown file into chunk dicts with heading trail + pages."""
    recs = clean_lines(Path(path).read_text(encoding="utf-8"))
    chunks, stack = [], []
    buf, buflen, pages = [], 0, []

    def trail():
        return " > ".join(t for _, t in stack)

    def flush(carry_overlap):
        """Emit the buffer as a chunk; return the overlap text to seed the next."""
        nonlocal buf, buflen, pages
        body = "\n".join(buf).strip()
        buf, buflen = [], 0
        pg = [p for p in pages if p is not None]
        pages = []
        if not body:
            return ""
        chunks.append({
            "trail": trail(),
            "heading": stack[-1][1] if stack else "",
            "page_start": min(pg) if pg else None,
            "page_end": max(pg) if pg else None,
            "text": body,
        })
        return _overlap_tail(body, OVERLAP_CHARS) if carry_overlap else ""

    def seed(overlap, page, budget=0):
        """Start the next buffer with the overlap bridge — unless carrying it
        would leave no room for the text that triggered the flush."""
        nonlocal buf, buflen, pages
        if overlap and len(overlap) + budget + 2 <= MAX_CHARS:
            buf, buflen, pages = [overlap], len(overlap) + 1, [page]

    def add(unit, page):
        nonlocal buf, buflen, pages
        if buflen and buflen + len(unit) + 1 > MAX_CHARS:
            seed(flush(carry_overlap=True), page, budget=len(unit))
        buf.append(unit)
        buflen += len(unit) + 1
        pages.append(page)
        if buflen > MAX_CHARS:               # a single unit wider than the ceiling
            flush(carry_overlap=False)

    for r in recs:
        if r["heading_level"]:
            flush(carry_overlap=False)      # never bleed across a section boundary
            lvl = r["heading_level"]
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, r["text"]))
            continue

        if not r["text"]:                    # paragraph break
            if buflen > MIN_FLUSH:
                seed(flush(carry_overlap=True), r["page"])
            continue

        for unit in _split_units(r["text"], MAX_CHARS):
            add(unit, r["page"])
    flush(carry_overlap=False)

    return _absorb_short(chunks)


def _fits(a, b):
    return len(a["text"]) + len(b["text"]) + 1 <= MAX_CHARS


def _merge(into, other):
    into["text"] = into["text"] + "\n" + other["text"]
    for a, b in (("page_start", min), ("page_end", max)):
        vals = [v for v in (into[a], other[a]) if v is not None]
        into[a] = b(vals) if vals else None


def _absorb_short(chunks):
    """Fold sub-MIN_CHARS chunks into a neighbour in the same section, never
    breaching MAX_CHARS. A fragment with no room either side is dropped rather
    than embedded — a 40-character stub only adds noise to the vector space."""
    out, dropped = [], 0
    for i, c in enumerate(chunks):
        if len(c["text"]) >= MIN_CHARS:
            out.append(c)
            continue
        if out and out[-1]["trail"] == c["trail"] and _fits(out[-1], c):
            _merge(out[-1], c)
        elif i + 1 < len(chunks) and chunks[i + 1]["trail"] == c["trail"] and _fits(chunks[i + 1], c):
            nxt = chunks[i + 1]                     # prepend: the stub precedes it
            nxt["text"] = c["text"] + "\n" + nxt["text"]
            for a, b in (("page_start", min), ("page_end", max)):
                vals = [v for v in (nxt[a], c[a]) if v is not None]
                nxt[a] = b(vals) if vals else None
        else:
            dropped += 1
    for j, c in enumerate(out):
        c["chunk"] = j
    if dropped:
        _absorb_short.dropped = getattr(_absorb_short, "dropped", 0) + dropped
    return out


_DEVA_RE = re.compile(r"[ऀ-ॿ]")
MIN_LATIN_FOR_SPLIT = 200      # chars of Latin text needed before we drop the Devanagari


def embed_input(source, chunk, context=""):
    """What actually gets embedded: source + heading trail + preamble, then body.

    The situating preamble (contextualize.py, §2.2) is prepended HERE and only
    here. It never reaches chunks.jsonl's `text`, so the drafting model quotes
    the source rather than a generated gloss of it, and the preamble cannot be
    mistaken for evidence.

    Two sources — samarangana-sutradhara.md and bhojdev.md — are bilingual
    editions carrying the Sanskrit or Hindi and its English rendering line by
    line. Embedding both halves together pulls the vector between two languages
    and leaves the passage unreachable from an English query even though its
    translation is sitting right there. For such chunks only the English is
    embedded; `text` on disk keeps both, so the drafting model can still quote
    the original.
    """
    head = f"[{source}] {chunk['trail']}".strip()
    if context:
        head = f"{head}\n{context}".strip()
    body = chunk["text"]
    latin = [ln for ln in body.split("\n") if ln.strip() and not _DEVA_RE.search(ln)]
    latin_chars = sum(len(ln) for ln in latin)
    if latin_chars >= MIN_LATIN_FOR_SPLIT and latin_chars < len(body) * 0.9:
        # Drop code fences too — with the Sanskrit removed they wrap nothing.
        body = "\n".join(ln for ln in latin if not ln.lstrip().startswith("```"))
    return f"{head}\n{body}".strip()


def fingerprint(files, contexts=None):
    """A signature of the inputs + settings; identical => KB is still current.

    v2 folds in the config's index-relevant sections and the number of
    situating preambles in play. Without that, turning contextualisation on or
    changing a chunk setting would leave the fingerprint unmoved and the KB
    silently stale — the same class of bug that made v1's kb_stamp blind to a
    rebuild that recomputed every vector.
    """
    stat = [[os.path.basename(f), os.path.getsize(f), int(os.path.getmtime(f))] for f in sorted(files)]
    return {"model": MODEL, "max_chars": MAX_CHARS, "min_chars": MIN_CHARS,
            "overlap": OVERLAP_CHARS, "cleaner": "md_clean/1",
            "config": CFG.section_hash("chunking", "embedding", "comprehension"),
            "contexts": len(contexts or {}),
            "files": stat}


def embed_all(client, texts):
    out, i = [], 0
    while i < len(texts):
        batch, toks = [], 0
        while i < len(texts):
            tt = len(texts[i]) // 4 + 1
            if batch and (toks + tt > BATCH_TOKENS or len(batch) >= BATCH_ITEMS):
                break
            batch.append(texts[i]); toks += tt; i += 1
        delay = 5
        for attempt in range(5):
            try:
                r = client.embeddings.create(model=MODEL, inputs=batch)
                out.extend(d.embedding for d in r.data)
                break
            except Exception as e:                       # noqa: BLE001 retry transient
                if attempt == 4:
                    raise
                print(f"    embed retry {attempt+1}: {type(e).__name__}", flush=True)
                time.sleep(delay); delay = min(delay * 2, 60)
        print(f"  embedded {len(out)}/{len(texts)} chunks", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser(description="Build the vector knowledge base from a Markdown folder")
    ap.add_argument("src_dir", nargs="?", default="Udaypur Reference Markdown Files")
    ap.add_argument("--force", action="store_true", help="rebuild even if sources are unchanged")
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env or the environment)"); sys.exit(1)

    files = sorted(glob.glob(os.path.join(args.src_dir, "*.md")))
    if not files:
        print(f"ERROR: no .md files in '{args.src_dir}'"); sys.exit(1)

    contexts = {}
    if CFG.embedding.get("contextualize"):
        from contextualize import load_contexts
        raw = load_contexts()
        contexts = {int(k): v.get("context", "") for k, v in raw.items() if v.get("context")}
        print(f"contextualisation ON — {len(contexts):,} preambles loaded")
    fp = fingerprint(files, contexts)
    cfg_path = KB_DIR / "config.json"
    if cfg_path.exists() and not args.force:
        try:
            old = json.loads(cfg_path.read_text(encoding="utf-8"))
            if old.get("fingerprint") == fp:
                print(f"KB is up to date ({old.get('count')} chunks); nothing to rebuild. Use --force to override.")
                return
        except Exception:
            pass  # unreadable/old config -> rebuild

    records, texts = [], []
    for f in files:
        name = os.path.basename(f)
        got = chunk_markdown(f)
        for c in got:
            i = len(records)
            records.append({"source": name, **c})
            texts.append(embed_input(name, c, contexts.get(i, "")))
        print(f"  {name[:58]:60s} {len(got):5d} chunks", flush=True)
    if not texts:
        print("ERROR: sources produced no text chunks"); sys.exit(1)
    print(f"{len(files)} files -> {len(texts)} chunks; embedding with {MODEL} ...", flush=True)

    client = Mistral(api_key=key)
    arr = np.asarray(embed_all(client, texts), dtype="float32")
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms

    KB_DIR.mkdir(parents=True, exist_ok=True)
    np.save(KB_DIR / "embeddings.npy", arr)
    with open(KB_DIR / "chunks.jsonl", "w", encoding="utf-8") as fh:
        for rec in records:                     # `text` is the body only — the
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")   # header lives in `trail`
    json.dump({"model": MODEL, "dim": int(arr.shape[1]), "count": int(arr.shape[0]),
               "source_dir": args.src_dir,
               "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "contextualized": bool(contexts),
               "config": CFG.hash(),
               "fingerprint": fp},
              open(KB_DIR / "config.json", "w", encoding="utf-8"), indent=2)
    print(f"KB built: {arr.shape[0]} chunks, dim {arr.shape[1]} -> {KB_DIR}/", flush=True)

    # The dense matrix and the SQLite store must be built from the SAME chunk
    # list in the SAME order: rowid is the join key between them, and a mismatch
    # would silently pair one passage's vector with another's text. Building
    # both here is what keeps that invariant true by construction.
    try:
        from entities import EntityIndex
        from kb_store import KBStore
        store = KBStore()
        alias_map = EntityIndex.load(store=store).alias_map()
        n = store.build(records, contexts=contexts, alias_map=alias_map,
                        stamp={"built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "count": int(arr.shape[0]), "config": CFG.hash()})
        st = store.stats()
        print(f"Sparse index: {n} chunks, {st['mentions']:,} entity mentions, "
              f"{st['entities']} entities -> {store.path}", flush=True)
    except Exception as e:
        print(f"WARNING: sparse index not built ({type(e).__name__}: {e}). "
              f"Dense retrieval works; hybrid does not. "
              f"Fix, then run: python entities.py --reindex", file=sys.stderr)

    # The dense matrix and the SQLite store must be built from the SAME chunk
    # list in the SAME order: rowid is the join key between them, and a
    # mismatch would silently pair one passage's vector with another's text.
    # Building both here is what keeps that invariant true by construction.
    try:
        from entities import EntityIndex
        from kb_store import KBStore
        store = KBStore()
        alias_map = EntityIndex.load(store=store).alias_map()
        n = store.build(records, contexts=contexts, alias_map=alias_map,
                        stamp={"built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "count": int(arr.shape[0]), "config": CFG.hash()})
        st = store.stats()
        print(f"Sparse index: {n} chunks, {st['mentions']:,} entity mentions, "
              f"{st['entities']} entities -> {store.path}", flush=True)
    except Exception as e:                            # noqa: BLE001 - dense KB is still valid
        print(f"WARNING: sparse index not built ({type(e).__name__}: {e}). "
              f"Dense retrieval works; hybrid does not. "
              f"Fix, then run: python entities.py --reindex", file=sys.stderr)


if __name__ == "__main__":
    main()
