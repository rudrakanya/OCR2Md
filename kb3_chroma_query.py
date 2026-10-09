#!/usr/bin/env python
"""Chapter-scoped retrieval over the ChromaDB store. The drafting entry point.

    python kb3_chroma_query.py "Bhoja's own writings and learning" --chapter C5
    python kb3_chroma_query.py "yoga doctrine samadhi" --chapter C7      # should stay empty-ish
    python kb3_chroma_query.py "village life today" --chapter C16 --profile prose
    python kb3_chroma_query.py "..." --quotable-only --json

ARCHIVE IS UNREACHABLE: this module names exactly one collection, "udaypur_kb".
The archive lives in "udaypur_kb_archive" and is never opened here, so
quarantined chunks cannot reach a draft (spec E).

SCOPING is a metadata filter, not a re-rank: `where={"in_C5": True}` means only
chunks bucketed into C5 are candidates. Combine with `--quotable-only`
(excludes AI-reworded and OCR needs_recheck text), `--source-type`,
`--status`.

RANKING combines the separately-stored scores only here (spec B):
    evidence: 0.45 topical + 0.25 credibility + 0.15 primacy + 0.15 reliability
    prose:    0.45 topical + 0.20 credibility + 0.10 primacy + 0.10 reliability
              + 0.15 for observation / folklore / opinion (quotable colour)
    topical = chapter relevance and/or semantic similarity to the query
    ties (2 dp) break by recency ONLY inside secondary/tertiary tiers; primary
    and field sources sort ahead of any tie, so recency never demotes primacy.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "kb3" / "chroma"

# Which store this path reads, and therefore which embedder a query needs. A
# collection holds exactly one vector space, so the embedder is a property of the
# collection and not a free choice: v1 is local e5-small at 384-d, v2 is OpenAI
# text-embedding-3-large at 1536-d. KB_STORE picks one; the default stays v1
# until cutover, so nothing changes under existing callers.
STORES = {
    "v1": {"collection": "udaypur_kb", "embedder": "local", "dim": 384},
    "v2": {"collection": "udaypur_kb_v2", "embedder": "local", "dim": 384},
    "v2-openai": {"collection": "udaypur_kb_v2_openai", "embedder": "openai", "dim": 1536},
}
from kb_target import active as _kb_active  # noqa: E402
STORE = _kb_active()               # KB_STORE env var still overrides, per kb_target
COLLECTION = STORES[STORE]["collection"]   # the archive collection is never named here
PRIMARY_TIERS = {"primary_authorial_paramara", "primary_epigraphic", "primary_scriptural",
                 "field_observation_survey", "field_observation_reportage"}
_model = None


def embed_query(text: str, store=None):
    """Embed a query in the vector space of the store being read."""
    global _model
    cfg = STORES[store or STORE]
    ck = f"{cfg['embed_model'] if 'embed_model' in cfg else cfg['embedder']}|{cfg['dim']}|{text}"
    cached = _qcache().get(ck)
    if cached is not None:
        return list(cached)
    if cfg["embedder"] == "openai":
        from openai import OpenAI
        from phase4_embed_v2 import load_key
        global _oai
        try:
            _oai
        except NameError:
            _oai = OpenAI(api_key=load_key())
        r = _oai.embeddings.create(model="text-embedding-3-large", input=[text],
                                   dimensions=cfg["dim"])
        v = list(r.data[0].embedding)
        _qcache()[ck] = v
        _qcache_save()
        return v
    if _model is None:
        from embed_e5 import load_model, encode
        _model = (*load_model("intfloat/multilingual-e5-small"), encode)
    tok, model, encode = _model
    v = encode([text], tok, model, "query: ")[0].astype("float32").tolist()
    _qcache()[ck] = v
    _qcache_save()
    return v


# ---------------------------------------------------------------------------
# Caches. Measured costs per search BEFORE these existed:
#   PersistentClient + get_collection      392 ms, paid on every call
#   one OpenAI query embedding          ~1-9 s of network, x2 with bilingual
#   bucket fetch with embeddings        6,040 ms for C5's 3,527 rows, and the
#                                       embeddings arrive as nested Python lists,
#                                       which is also the memory spike that has
#                                       OOM'd this machine twice
# None of these change what is returned, so all three are cached. The bucket is
# held as one float32 array instead of lists, and only a couple of buckets are
# kept, so memory stays bounded on a 3 GB machine.
# ---------------------------------------------------------------------------
_CLIENT = None
_COLS = {}
_BUCKET = collections.OrderedDict()      # (collection, chapter, count) -> payload
_BUCKET_MAX = 2
_QCACHE_PATH = ROOT / "kb3" / "query_vectors.npz"
_QCACHE = None


def _client():
    global _CLIENT
    if _CLIENT is None:
        import chromadb
        _CLIENT = chromadb.PersistentClient(path=str(CHROMA))
    return _CLIENT


def _collection(name):
    if name not in _COLS:
        _COLS[name] = _client().get_collection(name)
    return _COLS[name]


def _qcache():
    """Query vectors cached on disk: a drafting session repeats queries, and an
    embedding call is network latency every time."""
    global _QCACHE
    if _QCACHE is None:
        _QCACHE = {}
        if _QCACHE_PATH.exists():
            try:
                import numpy as np
                z = np.load(_QCACHE_PATH, allow_pickle=True)
                _QCACHE = {k: z["V"][i] for i, k in enumerate(z["keys"])}
            except Exception:
                _QCACHE = {}
    return _QCACHE


def _qcache_save():
    try:
        import numpy as np
        c = _qcache()
        if not c:
            return
        keys = list(c)
        V = np.stack([np.asarray(c[k], dtype="float32") for k in keys])
        tmp = _QCACHE_PATH.with_suffix(".tmp.npz")
        np.savez(tmp, keys=np.array(keys, dtype=object), V=V)
        tmp.replace(_QCACHE_PATH)
    except Exception:
        pass


def _bucket(col, name, chapter, where):
    """The chapter's rows, with embeddings as one float32 matrix, memoized.

    Keyed on the collection's row count so a rebuilt store invalidates the cache
    automatically rather than silently serving stale vectors.
    """
    import numpy as np
    key = (name, chapter, col.count())
    hit = _BUCKET.get(key)
    if hit is not None:
        _BUCKET.move_to_end(key)
        return hit
    # Paged, and converted to float32 as each page arrives. Two reasons:
    #
    #  * Chroma hands embeddings back as nested Python lists. One page of 2,000
    #    x 1536 floats is ~98 MB of objects; a whole 17,500-row bucket (what a
    #    35%-membership chapter looks like at 50k vectors) would be ~860 MB
    #    transient, on a machine with ~3 GB free. Paging bounds that.
    #  * `limit=20000` was a SILENT TRUNCATION ceiling: a bucket larger than the
    #    limit would quietly return part of itself and the chapter would be
    #    scored on an arbitrary subset. Paging until exhaustion removes the
    #    ceiling, and the warning fires if a page ever comes back short.
    PAGE = 2000
    metas, docs, mats = [], [], []
    off = 0
    while True:
        res = col.get(where=where, limit=PAGE, offset=off,
                      include=["metadatas", "documents", "embeddings"])
        got = len(res["metadatas"])
        if not got:
            break
        metas += res["metadatas"]
        docs += res["documents"]
        mats.append(np.asarray(res["embeddings"], dtype=np.float32))
        del res
        off += got
        if got < PAGE:
            break
        if off > 500_000:
            print(f"  [kb3_chroma_query] bucket {chapter} exceeded 500k rows; "
                  f"stopping the page loop", file=sys.stderr)
            break
    payload = (metas, docs,
               np.concatenate(mats) if mats else np.zeros((0, 1), dtype=np.float32))
    del mats
    _BUCKET[key] = payload
    while len(_BUCKET) > _BUCKET_MAX:
        _BUCKET.popitem(last=False)
    return payload


_CODE = None


def _code_of(source_id):
    """Registry code for a source id, for the per-source caps and reporting."""
    global _CODE
    if _CODE is None:
        import yaml
        reg = yaml.safe_load((ROOT / "kb_audit" / "source_registry.yaml").read_text(encoding="utf-8"))
        _CODE = {s["source_id"]: (s.get("code") or s["source_id"]) for s in reg["sources"]}
    return _CODE.get(source_id, source_id)


def _second_query(query):
    """The same question in the other script, or None. Never raises: if the
    translation is unavailable, retrieval proceeds monolingually."""
    try:
        from bilingual import second_form, enabled
        return second_form(query) if enabled() else None
    except Exception:
        return None


def _apply_source_cap(rows, chapter, k):
    """Demote chunks past a source's share of the candidate list.

    Nothing is removed: excess chunks move to the tail, so on-topic evidence
    beyond the cap stays retrievable and citable. It simply stops one book
    crowding a chapter out. SAM tops all sixteen buckets at 26-38%, which is what
    this exists for; the per-chapter and per-source ceilings live in
    kb3/retrieval.yaml so C7 can lean on its subject while C2/C3 cannot.
    """
    if not chapter or not rows:
        return rows
    from bilingual import config
    sc = (config().get("source_cap") or {})
    limit = float((sc.get("per_chapter") or {}).get(chapter, sc.get("default", 0.30)))
    per_src = ((sc.get("per_source") or {}).get(chapter) or {})
    n = k or len(rows)
    kept, tail, used = [], [], {}
    for r in rows:
        code = r.get("_code") or r.get("parent_source_id") or "?"
        cap = float(per_src.get(code, limit))
        allowed = max(1, int(round(cap * n)))
        if used.get(code, 0) >= allowed:
            tail.append(r)
            continue
        used[code] = used.get(code, 0) + 1
        kept.append(r)
    return kept + tail


def search(query=None, chapter=None, k=10, profile="evidence", quotable_only=False,
           source_type=None, status=None, candidates=200, source=None,
           bilingual=True, store=None, cap_sources=True, _trace=None):
    """Retrieve for a chapter and/or a query.

    `bilingual` also issues the query in the other script and merges the two
    candidate sets (see bilingual.py): without it the Devanagari sources are
    unreachable from English, which the vector map measured directly.
    `cap_sources` stops one book supplying more than its configured share of a
    chapter's candidates. Both are on by default and both only ever REORDER --
    no chunk is excluded from the store or made uncitable by either.
    """
    import yaml
    store = store or STORE
    _name = STORES[store]["collection"]
    col = _collection(_name)
    prof = {}
    if chapter:
        cfg = yaml.safe_load(open(ROOT / "kb3" / "chapters.yaml", encoding="utf-8"))
        prof = next((c for c in cfg["chapters"] if c["id"] == chapter), {}) or {}

    where = {}
    if chapter:
        where[f"in_{chapter}"] = True
    if quotable_only:
        where["is_quotable"] = True
    if source_type:
        where["source_type"] = source_type
    if source:
        where["parent_source_id"] = source
    if status:
        where["epistemic_status"] = status
    where = {"$and": [{k_: v} for k_, v in where.items()]} if len(where) > 1 else (where or None)

    if chapter:
        # Score the WHOLE bucket, not just the query's nearest neighbours.
        # Chroma returns the top-N by vector distance, and with a small
        # multilingual model a Hindi or Sanskrit passage never enters the top-N
        # of an English query — the Rājamārtaṇḍa's introduction was invisible
        # for "Bhoja's works" while ranking first for the same query in Hindi.
        # The bucket is a few thousand rows, so cosine is computed here.
        metas, docs, _V = _bucket(col, _name, chapter, where)
        if query:
            import numpy as np
            V = _V
            qv = np.asarray(embed_query(query, store), dtype=np.float32)
            sim = (V @ qv) if len(V) else np.zeros(0)
            q2 = _second_query(query) if bilingual else None
            if q2 and len(V):
                from bilingual import config
                w = float(config()["second_weight"])
                s2 = V @ np.asarray(embed_query(q2, store), dtype=np.float32)

                # Normalise each query's similarities within that query before
                # comparing them. Raw cosines from two different queries sit on
                # different scales -- the Hindi form's best match scored lower
                # than the English form's best even when it was the better
                # answer -- so a raw max silently demoted every Devanagari chunk.
                def _n(a):
                    lo, hi = float(a.min()), float(a.max())
                    return (a - lo) / (hi - lo) if hi - lo > 1e-9 else np.ones_like(a)

                n1, n2 = _n(sim), _n(s2)
                if _trace is not None:
                    _trace["second_query"] = q2
                    _trace["second_better"] = int(((w * n2) > n1).sum())
                sim = np.maximum(n1, w * n2)
            dists = (1 - sim).tolist() if len(V) else []
        else:
            dists = [None] * len(metas)
    elif query:
        # Two retrievals, merged by chunk id. The second form is what makes the
        # Devanagari sources reachable at all; the cap in bilingual.merge_candidates
        # keeps it from flooding a list the primary form already answers.
        got = {}
        q2 = _second_query(query) if bilingual else None
        for form, qtext in (("primary", query), ("second", q2)):
            if not qtext:
                continue
            r = col.query(query_embeddings=[embed_query(qtext, store)],
                          n_results=min(candidates, 500), where=where,
                          include=["metadatas", "documents", "distances"])
            for m, d, dist in zip(r["metadatas"][0], r["documents"][0], r["distances"][0]):
                cid = m.get("chunk_id")
                slot = got.setdefault(cid, {"meta": m, "doc": d, "primary": None, "second": None})
                slot[form] = 1 - dist
        if _trace is not None:
            _trace["second_query"] = q2
            _trace["second_only"] = sum(
                1 for v in got.values() if v["primary"] is None and v["second"] is not None)
        from bilingual import merge_candidates
        order = merge_candidates({c: v["primary"] for c, v in got.items() if v["primary"] is not None},
                                 {c: v["second"] for c, v in got.items() if v["second"] is not None},
                                 k=max(k, 1))
        metas = [got[c]["meta"] for c, _, _ in order]
        docs = [got[c]["doc"] for c, _, _ in order]
        dists = [1 - s for _, s, _ in order]
        _origin = {c: o for c, _, o in order}
    else:
        res = col.get(where=where, limit=candidates, include=["metadatas", "documents"])
        metas, docs = res["metadatas"], res["documents"]
        dists = [None] * len(metas)

    sims = [1 - d if d is not None else None for d in dists]
    lo, hi = (min(s for s in sims if s is not None), max(s for s in sims if s is not None)) if query else (0, 1)
    out = []
    for m, doc, s in zip(metas, docs, sims):
        qn = 0.0 if s is None else ((s - lo) / (hi - lo) if hi > lo else 1.0)
        rel = m.get(f"rel_{chapter}", 0.0) if chapter else 0.0
        # Chapter-scoped: lean on the bucket score rather than raw query
        # similarity. multilingual-e5-small matches an English query to Hindi
        # or Sanskrit text weakly (the Rājamārtaṇḍa's Hindi introduction ranks
        # top-3 for a Hindi query and nowhere for the English equivalent),
        # while chapter relevance already carries Devanagari seed terms.
        T = 0.35 * qn + 0.65 * rel if (query and chapter) else (qn if query else rel)
        cred, prim = m["score_claim_credibility"], m["score_primacy"]
        relia = m["score_source_reliability"]
        if profile == "prose":
            vivid = 0.15 if (m["epistemic_status"] == "observation"
                             or m.get("tag_folklore") or m.get("tag_opinion")) else 0.0
            score = 0.45 * T + 0.20 * cred + 0.10 * prim + 0.10 * relia + vivid
        else:
            score = 0.45 * T + 0.25 * cred + 0.15 * prim + 0.15 * relia
        if chapter and m.get(f"admitted_{chapter}"):
            score *= 0.85
        # spec F: the chapter's preferred source types get an evidentiary-rank
        # boost inside the chapter. C5/C10 prefer primary_authorial_paramara,
        # which is what a work written by Bhoja himself is.
        if m["source_type"] in prof.get("preferred_source_types", []):
            score *= 1.10
        if m.get("tag_udaypur_specific"):
            score *= 1.10
        tie = 2.0 if m["source_type"] in PRIMARY_TIERS else max(0.0, m["score_recency"])
        out.append((round(score, 2), tie, score, m, doc, T))
    out.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    rows = [{"score": round(s, 3), "topical": round(T, 3), **m, "text": doc,
             "_code": _code_of(m.get("parent_source_id"))}
            for _, _, s, m, doc, T in out]
    # The cap runs on the FULL ranked list and before truncation, so a demoted
    # chunk falls to the tail of the candidates rather than off the end of a
    # top-k that was already cut.
    if cap_sources:
        rows = _apply_source_cap(rows, chapter, k)
    if _trace is not None:
        import collections as _c
        _trace["returned_sources"] = dict(_c.Counter(r["_code"] for r in rows[:k]))
    return rows[:k]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?")
    ap.add_argument("--chapter")
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--profile", choices=["evidence", "prose"], default="evidence")
    ap.add_argument("--quotable-only", action="store_true")
    ap.add_argument("--source-type")
    ap.add_argument("--source", help="restrict to one parent_source_id")
    ap.add_argument("--status")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args(argv)
    if not a.query and not a.chapter:
        raise SystemExit("give a query and/or --chapter")
    res = search(a.query, a.chapter, a.k, a.profile, a.quotable_only, a.source_type, a.status, source=a.source)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for i, r in enumerate(res, 1):
        flags = [t.replace("tag_", "") for t in r if t.startswith("tag_") and r[t]]
        if not r["is_quotable"]:
            flags.insert(0, "NOT-QUOTABLE")
        print(f"\n[{i}] {r['chunk_id']}  score {r['score']} (topical {r['topical']} | cred "
              f"{r['score_claim_credibility']} | primacy {r['score_primacy']} | reliab {r['score_source_reliability']})")
        print(f"    {r['source_type']} / {r['epistemic_status']} · {r['title'][:70]} · page {r['page'] or '—'} "
              f"· event {r['event_date'] or '—'} ({r['date_confidence']}) · corroborated by {r['corroboration_count']}")
        print(f"    buckets [{r['chapter_buckets']}]" + (f" · {' · '.join(flags)}" if flags else ""))
        t = re.sub(r"\s+", " ", r["text"])
        print("    " + (t if a.full else t[:340] + ("…" if len(t) > 340 else "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
