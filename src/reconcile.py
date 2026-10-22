"""Stale-chunk detection for a collection already built by `src.ingest`.

`chunk_id = sha1(f"{source_path}:{chunk_index}")` (src/chunker.py:make_id) is
POSITIONAL, not content-addressed. Editing a file so it produces fewer
chunks, renaming a file, or deleting a file all leave chunks behind in the
collection that `src.ingest`'s upsert never revisits and never deletes --
upsert only ever touches ids for files/positions that exist in TODAY's
corpus scan. This module finds those orphans by diffing "ids the current
corpus + chunking config would produce" against "ids actually in the
collection". It never embeds anything and never writes to the collection
unless --delete is passed.

    python -m src.reconcile                 # report only
    python -m src.reconcile --delete         # report, then remove stale ids
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict

from . import settings as st
from .chunker import chunk_document
from .ingest import load_corpus
from .store import Store


def expected_ids(cfg, token_len) -> dict[str, str]:
    """{chunk_id: source_path} the CURRENT corpus + chunking config would
    produce today. Pure chunking -- no embedding call, no network."""
    corpus = load_corpus(cfg)
    manifest = st.load_manifest(cfg)
    out: dict[str, str] = {}
    for path, text in corpus:
        meta = manifest.get(path.name)
        if meta is None:
            continue  # same file ingest.py would refuse; not this tool's job to fix
        title = meta.get("title") or path.stem
        for c in chunk_document(text, book_title=title, source_path=path.name,
                                cfg=cfg, token_len=token_len):
            out[c.chunk_id] = path.name
    return out


def find_stale(cfg, store: Store, token_len) -> dict:
    """Diff today's expected ids against what the collection actually holds.

    Returns a dict with:
      stale        {chunk_id: source_path}  -- in the collection, not expected
      missing      {chunk_id: source_path}  -- expected, not yet in the collection
      stale_by_source / missing_by_source    -- same, grouped for reporting
      corpus_files   set of filenames the scan actually read
      collection_sources   set of distinct source_path values stored
    """
    expected = expected_ids(cfg, token_len)
    existing_rows = store.all_chunks()
    existing = {r["chunk_id"]: r["metadata"].get("source_path", "?") for r in existing_rows}

    stale = {cid: src for cid, src in existing.items() if cid not in expected}
    missing = {cid: src for cid, src in expected.items() if cid not in existing}

    def group(d: dict[str, str]) -> dict[str, list[str]]:
        g: dict[str, list[str]] = defaultdict(list)
        for cid, src in d.items():
            g[src].append(cid)
        return dict(g)

    corpus_files = {p.name for p, _ in load_corpus(cfg)}
    collection_sources = set(existing.values())

    return {
        "stale": stale,
        "missing": missing,
        "stale_by_source": group(stale),
        "missing_by_source": group(missing),
        "corpus_files": corpus_files,
        "collection_sources": collection_sources,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Find (and optionally remove) stale chunks")
    ap.add_argument("--embed-preset", default=None)
    ap.add_argument("--delete", action="store_true",
                    help="actually remove stale ids from the collection (default: report only)")
    args = ap.parse_args(argv)

    cfg = st.apply_overrides(st.load(), embed_preset=args.embed_preset)

    # token_len only -- never call .embed_passages()/.embed_queries(), so this
    # never embeds anything or spends API credit, even for a hosted backend.
    from .embedder import get_embedder
    embedder = get_embedder(cfg)

    store = Store(cfg, create=False)
    result = find_stale(cfg, store, embedder.token_len)

    print(f"corpus files scanned: {len(result['corpus_files'])}")
    print(f"distinct source_path values in collection: {len(result['collection_sources'])}")
    renamed_or_deleted = result["collection_sources"] - result["corpus_files"]
    if renamed_or_deleted:
        print(f"\nsource_path values in the collection but NOT in the current corpus "
              f"(renamed or deleted source file):")
        for src in sorted(renamed_or_deleted):
            n = len(result["stale_by_source"].get(src, []))
            print(f"  {src}  ({n} stale chunks)")

    print(f"\nstale chunks (in collection, not reproduced by today's corpus+config): "
          f"{len(result['stale'])}")
    for src, ids in sorted(result["stale_by_source"].items(), key=lambda kv: -len(kv[1])):
        if src not in renamed_or_deleted:
            print(f"  {src}  ({len(ids)} stale chunks -- file edited/reconfigured, not removed)")

    print(f"\nmissing chunks (today's corpus+config would add these on next ingest): "
          f"{len(result['missing'])}")
    for src, ids in sorted(result["missing_by_source"].items(), key=lambda kv: -len(kv[1])):
        print(f"  {src}  ({len(ids)} new chunks)")

    if args.delete and result["stale"]:
        store.collection.delete(ids=list(result["stale"]))
        print(f"\nDELETED {len(result['stale'])} stale chunks from "
              f"{cfg.get_path('storage.collection')!r}")
    elif result["stale"]:
        print(f"\n{len(result['stale'])} stale chunks found -- rerun with --delete to remove them")

    return 0


if __name__ == "__main__":
    sys.exit(main())
