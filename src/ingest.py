"""Load -> chunk -> embed -> tag -> upsert.

    python -m src.ingest --rebuild            # clean build (§3)
    python -m src.ingest                      # idempotent incremental upsert
    python -m src.ingest --embed-preset e5_small_fast
    python -m src.ingest --dry-run            # chunk and report, embed nothing
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

from . import settings as st
from . import tag as tagmod
from .chunker import ChunkingError, chunk_document
from .dedupe import find_duplicates
from .embedder import get_embedder
from .store import Store, wipe
from .textutil import nfc


class IngestError(RuntimeError):
    pass


def load_corpus(cfg) -> list[tuple[Path, str]]:
    """§3: fail loudly on an empty file or non-UTF-8 bytes."""
    corpus_dir = Path(cfg.get_path("project.corpus_dir"))
    if not corpus_dir.is_dir():
        raise IngestError(f"corpus_dir does not exist: {corpus_dir}")
    pattern = cfg.get_path("project.glob", "*.md")
    files = sorted(corpus_dir.glob(pattern))
    if not files:
        raise IngestError(f"no files matching {pattern!r} in {corpus_dir}")

    out: list[tuple[Path, str]] = []
    for f in files:
        raw = f.read_bytes()
        if not raw.strip():
            raise IngestError(f"{f.name}: file is empty")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise IngestError(
                f"{f.name}: not valid UTF-8 at byte {exc.start} ({exc.reason}). "
                "Re-export this file as UTF-8; decoding with errors='replace' "
                "would silently corrupt Devanagari."
            ) from exc
        out.append((f, nfc(text)))
    return out


def build_chunks(cfg, corpus, manifest, embedder, *, verbose: bool = True):
    chunks = []
    per_book = []
    for path, text in corpus:
        meta = manifest.get(path.name)
        if meta is None:
            raise IngestError(
                f"{path.name} is in the corpus directory but not in "
                f"books_manifest.yaml. Add a row for it (or remove the file) — "
                "silently ingesting an unlisted book would leave you unable to "
                "cite it."
            )
        title = meta.get("title") or path.stem
        try:
            got = chunk_document(text, book_title=title, source_path=path.name,
                                 cfg=cfg, token_len=embedder.token_len)
        except ChunkingError as exc:
            raise IngestError(str(exc)) from exc
        chunks.extend(got)
        toks = [c.token_count for c in got]
        per_book.append({
            "file": path.name, "title": title, "chunks": len(got),
            "tokens": sum(toks),
            "min_tok": min(toks), "median_tok": sorted(toks)[len(toks) // 2],
            "max_tok": max(toks),
        })
        if verbose:
            print(f"  {path.name[:56]:56s} {len(got):5d} chunks  "
                  f"{sum(toks):9,d} tok  median {sorted(toks)[len(toks)//2]:5d}")
    return chunks, per_book


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ingest the Udaypur corpus into ChromaDB")
    ap.add_argument("--rebuild", action="store_true",
                    help="delete the collection, caches and sidecar first (§3)")
    ap.add_argument("--no-rebuild", dest="rebuild", action="store_false")
    ap.add_argument("--clear-results", action="store_true",
                    help="also delete eval/results (kept by default, so a model "
                         "change leaves you a before/after)")
    ap.add_argument("--embed-preset", default=None,
                    help="use an alternative model from config.embedding.alternatives")
    ap.add_argument("--chunk-tokens", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="chunk and report only; do not download or embed anything")
    ap.add_argument("--no-tag", action="store_true",
                    help="skip chapter tagging (run `python -m src.tag` later)")
    ap.add_argument("--limit", type=int, default=None,
                    help="ingest only the first N files (smoke test)")
    ap.set_defaults(rebuild=False)
    args = ap.parse_args(argv)

    cfg = st.apply_overrides(st.load(), embed_preset=args.embed_preset,
                             chunk_tokens=args.chunk_tokens)
    prov = st.provenance(cfg)
    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")

    print("=" * 78)
    print(f"INGEST  run {run_id}   config {prov['config_hash']}")
    print(f"  model        {prov['embedding_model']}  ({prov['embedding_preset']})")
    print(f"  chunking     target {prov['chunk_target_tokens']} / "
          f"overlap {prov['chunk_overlap_tokens']} tokens")
    print("=" * 78)

    if args.rebuild:
        wipe(cfg, clear_results=args.clear_results)
        print()

    corpus = load_corpus(cfg)
    manifest = st.load_manifest(cfg)
    if args.limit:
        corpus = corpus[: args.limit]
    print(f"corpus: {len(corpus)} files, "
          f"{sum(len(t) for _, t in corpus):,} chars (all valid UTF-8)\n")

    t0 = time.time()
    if args.dry_run:
        # Count tokens with the cached XLM-R tokenizer without instantiating
        # (and therefore downloading) the encoder itself.
        from transformers import AutoTokenizer
        tok_name = cfg.get_path("embedding.model")
        try:
            _tok = AutoTokenizer.from_pretrained(tok_name)
        except Exception:
            _tok = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
            print(f"  (tokenizer for {tok_name} unavailable offline; "
                  "using the XLM-R vocab already cached — same tokenisation)\n")

        class _Dry:
            def token_len(self, text: str) -> int:
                return len(_tok(text, add_special_tokens=False)["input_ids"]) if text else 0
        embedder = _Dry()
    else:
        print(f"loading encoder {cfg.get_path('embedding.model')} ...")
        embedder = get_embedder(cfg)
        print(f"  device={getattr(embedder, 'device', 'n/a')}  dim={embedder.dim}\n")

    print("chunking:")
    chunks, per_book = build_chunks(cfg, corpus, manifest, embedder)
    toks = sorted(c.token_count for c in chunks)
    print(f"\n  TOTAL {len(chunks):,} chunks   "
          f"tokens min/median/p95/max = {toks[0]}/{toks[len(toks)//2]}/"
          f"{toks[int(len(toks)*0.95)]}/{toks[-1]}")

    print("\nnear-duplicate scan ...")
    dupes = find_duplicates(chunks)
    if dupes:
        by_src: dict[str, int] = {}
        for cid, (keep, _s) in dupes.items():
            src = next(c.source_path for c in chunks if c.chunk_id == cid)
            by_src[src] = by_src.get(src, 0) + 1
        print(f"  {len(dupes)} duplicate chunks flagged (kept, but demoted at query time):")
        for src, n in sorted(by_src.items(), key=lambda kv: -kv[1]):
            print(f"    {n:4d}  {src}")
    else:
        print("  none found")

    if args.dry_run:
        print(f"\nDRY RUN — nothing embedded or written. {time.time()-t0:.1f}s")
        return 0

    print(f"\nembedding {len(chunks):,} chunks ...")
    vecs = embedder.embed_passages([c.embed_text for c in chunks], progress=True)
    if embedder.cache is not None:
        print(f"  cache: {embedder.cache.hits} hits, {embedder.cache.misses} computed")

    store = Store(cfg)
    metas = []
    for c in chunks:
        book = manifest.get(c.source_path, {})
        m = {
            "source_path": c.source_path,
            "book_title": c.book_title,
            "heading_path": c.heading_path,
            "chunk_index": c.chunk_index,
            "token_count": c.token_count,
            "language": c.language,
            "is_duplicate": c.chunk_id in dupes,
        }
        if book.get("author"):
            m["author"] = str(book["author"])
        if book.get("year") is not None:
            m["book_year"] = int(book["year"])
        if book.get("kind"):
            m["kind"] = str(book["kind"])
        if c.page_start is not None:
            m["page_start"] = int(c.page_start)
        if c.chunk_id in dupes:
            m["duplicate_of"] = dupes[c.chunk_id][0]
            m["dup_score"] = float(dupes[c.chunk_id][1])
        metas.append(m)

    print(f"\nupserting into '{cfg.get_path('storage.collection')}' ...")
    store.upsert([c.chunk_id for c in chunks], [c.text for c in chunks], vecs, metas)
    store.put_sidecar([
        (c.chunk_id, c.source_path, c.book_title, c.heading_path, c.chunk_index,
         c.token_count, c.language, c.page_start, c.text, c.text_folded,
         dupes.get(c.chunk_id, (None, None))[0], dupes.get(c.chunk_id, (None, None))[1])
        for c in chunks])
    print(f"  collection now holds {store.count():,} chunks")

    payload = {"run_id": run_id, "provenance": prov, "files": len(corpus),
               "chunks": len(chunks), "duplicates": len(dupes),
               "per_book": per_book, "elapsed_s": round(time.time() - t0, 1)}
    store.record_run(run_id, "ingest", payload)
    results = st.resolve(cfg, "evaluation.results_dir")
    results.mkdir(parents=True, exist_ok=True)
    (results / f"ingest_{run_id}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if not args.no_tag:
        print()
        tagmod.run_tagging(cfg, store=store, embedder=embedder, run_id=run_id)

    print(f"\nDONE in {time.time()-t0:.1f}s   "
          f"(run record: {results / f'ingest_{run_id}.json'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
