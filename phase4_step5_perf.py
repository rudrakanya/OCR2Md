#!/usr/bin/env python
"""Step 5 — retrieval latency and scalability headroom, measured.

    python phase4_step5_perf.py

Times the two retrieval paths cold and warm, breaks the time down so the fix is
aimed at the actual cost rather than a guess, and projects memory and latency to
50k vectors (the Inscriptions Corpus alone is 496 pages).

Nothing here changes results. Memory is sampled per phase because this machine
has ~3 GB free and has already OOM'd twice on bulk vector work.
"""
from __future__ import annotations

import gc
import json
import os
import statistics
import sys
import time
from pathlib import Path

os.environ.setdefault("KB_STORE", "v2-openai")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
QUERIES = [
    ("Udayaditya accession date and reign", "C5"),
    ("sculpture on the jangha of the temple exterior", "C7"),
    ("stepwell baoli water structures at Udaypur", "C3"),
]


def rss_mb():
    try:
        import ctypes
        import ctypes.wintypes as wt

        class PMC(ctypes.Structure):
            _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        c = PMC()
        c.cb = ctypes.sizeof(c)
        ctypes.windll.psapi.GetProcessMemoryInfo(
            ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(c), c.cb)
        return c.WorkingSetSize / 1e6
    except Exception:
        return float("nan")


def timed(fn, n=3):
    ts = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return min(ts), statistics.median(ts)


def main():
    out = {}
    print(f"baseline RSS {rss_mb():.0f} MB\n")

    # ---- component costs ---------------------------------------------------
    print("=" * 74)
    print("COMPONENT COSTS")
    print("=" * 74)
    import chromadb
    import kb_target as T
    coll = T.collection("v2-openai")

    t0 = time.perf_counter()
    client = chromadb.PersistentClient(path=str(ROOT / "kb3" / "chroma"))
    col = client.get_collection(coll)
    t_client = time.perf_counter() - t0
    print(f"  PersistentClient + get_collection      {t_client*1000:7.0f} ms   "
          f"(paid on EVERY search call today)")

    import kb3_chroma_query as Q
    t0 = time.perf_counter()
    Q.embed_query("Udayaditya accession date and reign", "v2-openai")
    t_embed = time.perf_counter() - t0
    print(f"  one OpenAI query embedding             {t_embed*1000:7.0f} ms   (network)")

    from bilingual import second_form
    t0 = time.perf_counter()
    second_form("Udayaditya accession date and reign")
    t_tr = time.perf_counter() - t0
    print(f"  translation (cached)                   {t_tr*1000:7.0f} ms")

    t0 = time.perf_counter()
    got = col.get(where={"in_C5": True}, limit=20000,
                  include=["metadatas", "documents", "embeddings"])
    t_bucket = time.perf_counter() - t0
    n_b = len(got["metadatas"])
    print(f"  bucket fetch WITH embeddings (C5)      {t_bucket*1000:7.0f} ms   "
          f"{n_b} rows, RSS now {rss_mb():.0f} MB")
    del got
    gc.collect()

    t0 = time.perf_counter()
    got2 = col.query(query_embeddings=[Q.embed_query("test query", "v2-openai")],
                     n_results=200, where={"in_C5": True}, include=["metadatas"])
    t_ann = time.perf_counter() - t0
    print(f"  HNSW query, n_results=200, filtered    {t_ann*1000:7.0f} ms   "
          f"(includes one embedding call)")
    del got2
    out["components"] = {"client_ms": t_client*1000, "embed_ms": t_embed*1000,
                         "translate_cached_ms": t_tr*1000,
                         "bucket_fetch_ms": t_bucket*1000, "bucket_rows": n_b,
                         "hnsw_query_ms": t_ann*1000}

    # ---- end to end --------------------------------------------------------
    print("\n" + "=" * 74)
    print("END TO END (3 runs, best / median)")
    print("=" * 74)
    import kb3_query as L
    rows = []
    for q, chap in QUERIES:
        b1, m1 = timed(lambda: Q.search(query=q, chapter=chap, k=20))
        b2, m2 = timed(lambda: Q.search(query=q, k=20))
        b3, m3 = timed(lambda: L.search(query=q, chapter=chap, k=20))
        print(f"  {chap} {q[:34]:36s}")
        print(f"      chroma chapter-scoped   {b1*1000:7.0f} / {m1*1000:7.0f} ms")
        print(f"      chroma unscoped         {b2*1000:7.0f} / {m2*1000:7.0f} ms")
        print(f"      kb3_query (BM25)        {b3*1000:7.0f} / {m3*1000:7.0f} ms")
        rows.append({"query": q, "chapter": chap,
                     "chroma_chapter_ms": m1*1000, "chroma_unscoped_ms": m2*1000,
                     "bm25_ms": m3*1000})
    out["end_to_end"] = rows
    print(f"\n  RSS after all searches {rss_mb():.0f} MB")

    # ---- scalability -------------------------------------------------------
    print("\n" + "=" * 74)
    print("SCALABILITY HEADROOM")
    print("=" * 74)
    n_now = col.count()
    dim = 1536
    per_vec = dim * 4
    print(f"  vectors now                {n_now:,} x {dim}-d float32 = "
          f"{n_now*per_vec/1e6:.0f} MB of raw vectors")
    for target in (20_000, 50_000, 100_000):
        print(f"  at {target:,} vectors        raw vectors {target*per_vec/1e6:>6.0f} MB"
              f" | biggest bucket fetch ~{target*0.35*per_vec/1e6:>6.0f} MB"
              f" | HNSW query ~{t_ann*1000*1:.0f} ms (index scales log n)")
    cfg = col.metadata or {}
    print(f"\n  collection metadata: {cfg}")
    out["scalability"] = {"n": n_now, "dim": dim,
                          "raw_mb_now": n_now*per_vec/1e6,
                          "metadata": cfg}
    (ROOT / "kb_audit" / "perf.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote kb_audit/perf.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
