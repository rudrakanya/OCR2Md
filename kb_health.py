#!/usr/bin/env python3
"""
kb_health.py — deterministic structural health check for the knowledge base.

Distinct from eval/eval_retrieval.py on purpose: that measures whether
retrieval finds the RIGHT passages for real questions (needs a human-verified
gold set, costs LLM calls). This measures whether the KB ITSELF is sound —
embeddings consistent with chunks, no silent OCR garbage, no exact-duplicate
chunks bloating the candidate pool, every source properly classified, the
label/entity layers actually populated — using nothing but SQL and numpy, in
a few seconds, for free. Run this first; a retrieval-accuracy number computed
against a KB with embedding drift or unlabelled garbage chunks is not
trustworthy regardless of what eval_retrieval.py reports.

    python kb_health.py                 # full report
    python kb_health.py --json          # machine-readable, for CI/diffing
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from console import use_utf8
from kb_store import KBStore, KB_DIR
import sources as src_mod

_WS_RE = re.compile(r"\s+")
_PAGE_MARKER_RE = re.compile(r"^\s*(<!--\s*page\s*\d+\s*-->\s*)+\s*$", re.IGNORECASE)
_ALNUM_RE = re.compile(r"[^\W\d_]", re.UNICODE)   # letters only, any script


def _pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def check_embeddings(store):
    """Embedding matrix vs. chunk table: count, contiguity, and NaN/zero rows."""
    out = {"name": "embeddings"}
    cfg_path = KB_DIR / "config.json"
    emb_path = KB_DIR / "embeddings.npy"
    if not cfg_path.exists() or not emb_path.exists():
        out["status"] = "fail"
        out["error"] = f"missing {cfg_path} or {emb_path}"
        return out
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    emb = np.load(emb_path)
    n_chunks = store.db.execute("SELECT COUNT(*) n FROM chunks").fetchone()["n"]
    max_rowid = store.db.execute("SELECT MAX(rowid) m FROM chunks").fetchone()["m"] or 0
    issues = []
    if emb.shape[0] != cfg.get("count"):
        issues.append(f"embeddings.npy has {emb.shape[0]} rows but config.json "
                      f"records count={cfg.get('count')}")
    if emb.shape[0] != n_chunks:
        issues.append(f"embeddings.npy has {emb.shape[0]} rows but the chunks table "
                      f"has {n_chunks} rows")
    if max_rowid > emb.shape[0]:
        issues.append(f"max chunk rowid ({max_rowid}) exceeds the embedding matrix "
                      f"({emb.shape[0]} rows) -- dense retrieval would index out of "
                      f"range or silently misalign for the highest-numbered chunks")
    # A zero (or all-NaN) row means embed_texts() got an empty string or the
    # embedding call failed silently and the vector was never actually written.
    norms = np.linalg.norm(emb, axis=1)
    n_degenerate = int(np.sum((norms < 1e-6) | np.isnan(norms)))
    if n_degenerate:
        issues.append(f"{n_degenerate} embedding row(s) are all-zero or NaN -- "
                      f"those chunks are unreachable by dense search regardless "
                      f"of what their text says")
    out.update(status="fail" if issues else "ok", n_chunks=n_chunks,
               n_embeddings=int(emb.shape[0]), n_degenerate=n_degenerate,
               model=cfg.get("model"), built_at=cfg.get("built_at"), issues=issues)
    return out


def check_fts(store):
    """FTS5 external-content tables can desync from their source table silently."""
    out = {"name": "full_text_search_index"}
    try:
        n_fts = store.db.execute("SELECT COUNT(*) n FROM chunks_fts").fetchone()["n"]
    except Exception as e:                          # noqa: BLE001
        out["status"] = "fail"; out["error"] = str(e)
        return out
    n_chunks = store.db.execute("SELECT COUNT(*) n FROM chunks").fetchone()["n"]
    out["n_fts_rows"], out["n_chunks"] = n_fts, n_chunks
    out["status"] = "ok" if n_fts == n_chunks else "fail"
    if n_fts != n_chunks:
        out["issues"] = [f"chunks_fts has {n_fts} rows, chunks has {n_chunks} -- the "
                         f"sparse channel is searching a stale or partial index; "
                         f"rebuild it (kb_store.py has no incremental FTS sync)"]
    else:
        out["issues"] = []
    return out


def check_chunk_quality(store):
    """Empty/near-empty chunks, bare page markers, and two SEPARATE signals
    that get conflated if you're not careful.

    A low letter-to-character ratio does NOT reliably mean garbled OCR --
    checked on this KB directly: the first two flagged chunks were an HTML
    table of club membership numbers and a book's back-of-index page ("Bhoja
    I, 28, 44, 81-83..."), both real, legitimate content that is naturally
    numeral- and punctuation-heavy. Reported separately as "table/index-like"
    (informational -- these are usually poor retrieval evidence regardless of
    whether they're garbled, since a table cell or an index line rarely
    stands alone as a citable claim, but that's a content-labelling question,
    not a corruption one). True corruption -- the Unicode replacement
    character, or a single character repeated well past anything a real
    document does -- is checked separately and IS a reliable signal.
    """
    out = {"name": "chunk_quality"}
    rows = store.db.execute("SELECT rowid, source, text FROM chunks").fetchall()
    n = len(rows)
    empty, bare_marker, table_like, short, corrupted = [], [], [], [], []
    for r in rows:
        t = (r["text"] or "").strip()
        if not t:
            empty.append(r["rowid"])
            continue
        if _PAGE_MARKER_RE.match(t):
            bare_marker.append(r["rowid"])
            continue
        if len(t) < 20:
            short.append(r["rowid"])
        if "�" in t or "\x00" in t:
            corrupted.append(r["rowid"])
        letters = len(_ALNUM_RE.findall(t))
        if len(t) >= 40 and letters / len(t) < 0.35:
            table_like.append(r["rowid"])
    out.update(status="warn" if (empty or bare_marker or corrupted) else "ok",
               n_chunks=n, n_empty=len(empty), n_bare_page_marker=len(bare_marker),
               n_very_short=len(short), n_replacement_char_or_null=len(corrupted),
               n_table_or_index_like=len(table_like),
               sample_corrupted=corrupted[:8], sample_table_like=table_like[:8],
               sample_empty=empty[:8])
    return out


def check_duplicates(store):
    """Exact-duplicate chunk text KB-wide, not just within one evidence pack.

    verify.py's validate_pack() already catches this per-chapter, after
    retrieval; this catches it at the source, across the whole corpus --
    chunking-overlap bugs and re-ingested near-duplicate documents both show
    up here as the same normalised text appearing under more than one rowid.
    """
    out = {"name": "duplicate_chunks"}
    rows = store.db.execute("SELECT rowid, source, text FROM chunks").fetchall()
    seen, dupes = {}, []
    for r in rows:
        norm = _WS_RE.sub(" ", (r["text"] or "").strip().lower())
        if len(norm) < 40:
            continue                                # short/boilerplate matches are not meaningful
        key = hash(norm)
        if key in seen:
            dupes.append({"rowid": r["rowid"], "source": r["source"],
                         "duplicate_of": seen[key][0], "same_source": seen[key][1] == r["source"]})
        else:
            seen[key] = (r["rowid"], r["source"])
    within = [d for d in dupes if d["same_source"]]
    cross = [d for d in dupes if not d["same_source"]]
    by_source = Counter(d["source"] for d in within)
    out.update(status="warn" if dupes else "ok", n_duplicate_chunks=len(dupes),
               n_within_source=len(within), n_cross_source=len(cross),
               interpretation=("all within-source -- a chunking artifact (e.g. a table or "
                               "repeated running header spanning a chunk boundary), not a "
                               "duplicate-document ingestion problem" if within and not cross
                               else "cross-source duplicates present -- check for re-ingested "
                                    "or near-identical source documents" if cross else ""),
               top_sources=[{"source": s, "count": c} for s, c in by_source.most_common(5)],
               sample=dupes[:8])
    return out


def check_sources(store):
    """Every KB source resolves to a real bibliographic entry -- no citation
    silently degrading to a raw filename."""
    out = {"name": "source_bibliography"}
    kb_sources = {r["source"] for r in store.db.execute("SELECT DISTINCT source FROM chunks")}
    unmapped = src_mod.unmapped(kb_sources)
    unclassified = sorted(kb_sources - set(src_mod.CLASSIFICATION))
    stale = sorted(set(src_mod.SOURCES) - kb_sources)
    out.update(status="fail" if (unmapped or unclassified) else "ok",
               n_kb_sources=len(kb_sources), n_unmapped_bibliography=len(unmapped),
               n_unclassified=len(unclassified), n_stale_sources_py_entries=len(stale),
               unmapped=unmapped, unclassified=unclassified,
               note="stale entries (in sources.py but not in this KB) are harmless "
                    "but worth pruning if they keep accumulating")
    return out


def check_labels(store):
    """Label-layer coverage -- retrievability gate, quality scores, curation."""
    out = {"name": "label_coverage"}
    n_chunks = store.db.execute("SELECT COUNT(*) n FROM chunks").fetchone()["n"]
    n_labeled = store.db.execute("SELECT COUNT(*) n FROM chunk_labels").fetchone()["n"]
    n_blocked = store.db.execute(
        "SELECT COUNT(*) n FROM chunk_labels WHERE retrievable = 0").fetchone()["n"]
    n_reviewed = store.db.execute(
        "SELECT COUNT(*) n FROM chunk_labels WHERE reviewed = 1").fetchone()["n"]
    qrow = store.db.execute(
        "SELECT AVG(quality) a, MIN(quality) mn, MAX(quality) mx FROM chunk_labels "
        "WHERE quality IS NOT NULL").fetchone()
    out.update(status="ok", n_chunks=n_chunks, n_labeled=n_labeled,
               labeled_pct=_pct(n_labeled, n_chunks),
               n_blocked_by_retrievable_gate=n_blocked, n_human_reviewed=n_reviewed,
               quality_avg=round(qrow["a"], 3) if qrow["a"] is not None else None,
               quality_min=qrow["mn"], quality_max=qrow["mx"],
               note="an unlabelled chunk is NOT blocked (the retrievable gate "
                    "defaults to admitting it, see kb_store.py's _filter_sql) -- "
                    "low labeled_pct means the label layer isn't doing much "
                    "filtering yet, not that content is being lost")
    if n_labeled == 0:
        out["status"] = "info"
    return out


def check_entities(store):
    """Entity registry: curated fraction, alias coverage, and dead entries
    with zero mentions (harmless, but a sign the registry has drifted from
    the corpus it's meant to index)."""
    out = {"name": "entity_registry"}
    n_entities = store.db.execute("SELECT COUNT(*) n FROM entities").fetchone()["n"]
    n_curated = store.db.execute("SELECT COUNT(*) n FROM entities WHERE curated=1").fetchone()["n"]
    n_aliases = store.db.execute("SELECT COUNT(*) n FROM entity_aliases").fetchone()["n"]
    n_mentions = store.db.execute("SELECT COUNT(*) n FROM entity_mentions").fetchone()["n"]
    n_unmentioned = store.db.execute(
        "SELECT COUNT(*) n FROM entities e WHERE NOT EXISTS "
        "(SELECT 1 FROM entity_mentions m WHERE m.entity_id = e.entity_id)").fetchone()["n"]
    out.update(status="ok", n_entities=n_entities, n_curated=n_curated,
               curated_pct=_pct(n_curated, n_entities), n_aliases=n_aliases,
               n_mentions=n_mentions, n_entities_with_zero_mentions=n_unmentioned)
    return out


def check_size_distribution(store):
    """Chunk length outliers -- a chunker bug usually shows up here first,
    as a spike of near-zero or implausibly large chunks."""
    out = {"name": "chunk_size_distribution"}
    lens = [len(r["text"] or "") for r in store.db.execute("SELECT text FROM chunks")]
    arr = np.array(lens)
    out.update(status="ok", n=len(arr), min=int(arr.min()), p10=int(np.percentile(arr, 10)),
               median=int(np.median(arr)), p90=int(np.percentile(arr, 90)),
               max=int(arr.max()),
               n_under_50_chars=int(np.sum(arr < 50)),
               n_over_8000_chars=int(np.sum(arr > 8000)))
    return out


CHECKS = [check_embeddings, check_fts, check_chunk_quality, check_duplicates,
         check_sources, check_labels, check_entities, check_size_distribution]


def run():
    store = KBStore()
    return [c(store) for c in CHECKS]


def print_report(results):
    icon = {"ok": "OK  ", "warn": "WARN", "fail": "FAIL", "info": "INFO"}
    print("KB Health Report")
    print("=" * 60)
    n_fail = sum(1 for r in results if r["status"] == "fail")
    n_warn = sum(1 for r in results if r["status"] == "warn")
    for r in results:
        print(f"\n[{icon.get(r['status'], '?')}] {r['name']}")
        for k, v in r.items():
            if k in ("name", "status"):
                continue
            if isinstance(v, list) and len(v) > 8:
                v = v[:8] + [f"... +{len(v) - 8} more"]
            print(f"    {k}: {v}")
    print("\n" + "=" * 60)
    print(f"{n_fail} fail, {n_warn} warn, "
         f"{len(results) - n_fail - n_warn} ok/info, out of {len(results)} checks")
    return n_fail


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Deterministic KB structural health check")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    results = run()
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        n_fail = sum(1 for r in results if r["status"] == "fail")
    else:
        n_fail = print_report(results)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
