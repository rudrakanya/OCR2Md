#!/usr/bin/env python
"""Query the rebuilt KB (Stage 2). The ONLY retrieval path for drafting.

    python kb3_query.py "Udayaditya relation to Bhoja"
    python kb3_query.py --chapter C8                      # best of a chapter bucket
    python kb3_query.py "mosque behind the temple" --chapter C9 --profile evidence
    python kb3_query.py "village life lanes" --chapter C16 --profile prose --dense
    python kb3_query.py "..." --json                      # machine-readable, for drafting tools

QUARANTINE IS UNREACHABLE TWO WAYS (spec E): this module opens exactly one
file, kb3/kb_active.sqlite, read-only, and the archive
(kb3/kb_quarantine.sqlite) is a separate file no code here names. Separation by
file is not sufficient on its own, though: a row quarantined IN PLACE in
kb_active still satisfied every candidate query, so `search()` also filters
`is_quarantined=0` where it hydrates candidate rows.

RANKING (spec F: topical fit and evidentiary rank kept apart; spec B: the
five scores are stored separately and combined ONLY here)
    topical   T = chapter relevance r(c,k) and/or query match (BM25, + bge-m3
                cosine with --dense), each min-max normalised over candidates
    profile   evidence: 0.45 T + 0.25 credibility + 0.15 primacy + 0.15 reliability
              prose:    0.45 T + 0.20 credibility + 0.10 primacy + 0.10 reliability
                        + 0.15 if observation / folklore / opinion (vivid, quotable)
    × admitted_penalty if the chunk is only 'admitted' to the chapter
    × preferred_type_boost if its source_type is preferred by the chapter
    × udaypur_specific_boost if it names the town, temple or king
    ties (to 2 decimals) are broken by recency ONLY within secondary/tertiary;
    primary and field chunks sort ahead of any tie (spec B5: recency never
    demotes a primary chunk beneath newer commentary).
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

K3 = Path(__file__).resolve().parent / "kb3"
from kb_target import sqlite_path as _kb_sqlite  # noqa: E402
ACTIVE = _kb_sqlite()              # resolved through kb_target; see kb3/active_store.txt
UDAY = {"udaipur", "udaypur", "udayapur", "udayapura", "udaipura"}
STOP = set("the a an of in on at to for and or is was were be by with from as that this which what who how "
           "about into its it their his her".split())


def connect():
    assert "quarantine" not in ACTIVE.name
    return sqlite3.connect(f"file:{ACTIVE}?mode=ro", uri=True)


def fts_query(q: str) -> str:
    words = [w for w in re.findall(r"\w+", q.lower()) if w not in STOP and len(w) > 1]
    parts = ['"' + w.replace('"', "") + '"' for w in words]
    if UDAY & set(words):
        parts.append("aliases:udaypur")
    return " OR ".join(parts)


def search(query=None, chapter=None, k=10, profile="evidence", dense=False, source=None,
           bilingual=True):
    """Lexical (BM25) + optional dense retrieval over the active store.

    `bilingual` also runs the query in the other script. On the lexical path this
    is a direct win and costs nothing but the translation: the FTS tokenizer
    indexes Devanagari, so a Hindi query form matches Hindi and Sanskrit text
    that an English query cannot tokenise onto at all. Each form's BM25 scores
    are normalised WITHIN that form before they are compared -- BM25 is not on a
    shared scale across different queries any more than cosine is, which is the
    error that made the first bilingual attempt on the vector path a no-op.
    """
    chap = yaml.safe_load(open(K3 / "chapters.yaml", encoding="utf-8"))
    prof = {c["id"]: c for c in chap["chapters"]}.get(chapter) if chapter else None
    db = connect()
    db.row_factory = sqlite3.Row
    cand = {}
    second = None
    if query:
        for r in db.execute("select rowid, bm25(chunks_fts) s from chunks_fts where chunks_fts match ? "
                            "order by s limit 400", (fts_query(query),)):
            cand[r["rowid"]] = {"bm25": -r["s"]}
        if bilingual:
            try:
                from bilingual import second_form, enabled
                second = second_form(query) if enabled() else None
            except Exception:
                second = None
        if second:
            fq2 = fts_query(second)
            if fq2:
                for r in db.execute("select rowid, bm25(chunks_fts) s from chunks_fts "
                                    "where chunks_fts match ? order by s limit 400", (fq2,)):
                    cand.setdefault(r["rowid"], {})["bm25_2"] = -r["s"]
        # The bge-m3 vectors on disk were built for v1's chunk ids. Using them
        # against another store would silently score the wrong rows, so --dense
        # is available only for the store they belong to.
        dense_ok = dense and _kb_sqlite().name == "kb_active.sqlite"
        if dense and not dense_ok:
            print("  [kb3_query] --dense ignored: active_vectors.npy belongs to v1",
                  file=sys.stderr)
        if dense_ok and (K3 / "active_vectors.npy").exists():
            sys.path.insert(0, str(K3.parent))
            from kb3_embed import load_model, encode
            tok, model = load_model()
            qv = encode([query], tok, model)[0].astype(np.float32)
            V = np.load(K3 / "active_vectors.npy").astype(np.float32)
            ids = json.loads((K3 / "active_vector_ids.json").read_text())
            sims = V @ qv
            top = np.argsort(-sims)[:400]
            rid = {cid: r for cid, r in db.execute("select chunk_id, rowid from chunks")}
            for t in top:
                cand.setdefault(rid[ids[t]], {})["cos"] = float(sims[t])
    elif chapter:
        for r in db.execute("select rowid from chunks where chapter_buckets like ?", (f'%"{chapter}%',)):
            cand[r["rowid"]] = {}
    else:
        raise SystemExit("give a query and/or --chapter")
    if not cand:
        return []

    # Quarantine is enforced HERE, at the single point every candidate path
    # (BM25, dense, chapter bucket) must pass through. The module header's
    # "unreachable by construction" held only for quarantine kept in a separate
    # FILE; ADH's 50 fabricated table rows were quarantined in place, in
    # kb_active.sqlite, and 49 of them were still reachable from a C7/C10
    # bucket read at depth. A flag nothing honours is not a quarantine.
    rows = {r["rowid"]: r for r in db.execute(
        f"select rowid, * from chunks where rowid in ({','.join(map(str, cand))}) "
        f"and is_quarantined=0")}
    cand = {rid: v for rid, v in cand.items() if rid in rows}
    if not cand:
        return []

    def mm(key):
        vals = [v[key] for v in cand.values() if key in v]
        lo, hi = (min(vals), max(vals)) if vals else (0, 1)
        return lambda x: 0.0 if x is None else (x - lo) / (hi - lo) if hi > lo else 1.0
    nb, nb2, nc = mm("bm25"), mm("bm25_2"), mm("cos")
    try:
        from bilingual import config as _bcfg
        _w2 = float(_bcfg()["second_weight"])
    except Exception:
        _w2 = 0.95
    out = []
    for rid, sig in cand.items():
        r = rows[rid]
        if source and r["parent_source_id"] != source:
            continue
        cs = json.loads(r["chapter_scores"])
        buckets = json.loads(r["chapter_buckets"])
        tags = set(json.loads(r["relevance_tags"]))
        qs = [x for x in (nb(sig.get("bm25")) if "bm25" in sig else None,
                          _w2 * nb2(sig.get("bm25_2")) if "bm25_2" in sig else None,
                          nc(sig.get("cos")) if "cos" in sig else None) if x is not None]
        qscore = max(qs) if qs else 0.0
        # .get, not [chapter]: v2 carries unclassified front-matter chunks whose
        # chapter_scores are {}, and a BM25 candidate can be one of them even when
        # a chapter is named. Indexing directly raised KeyError('C5') on the first
        # chapter+query search against v2 — it would have broken drafting the
        # moment the store was cut over.
        if chapter and query:
            T = 0.5 * qscore + 0.5 * cs.get(chapter, 0.0)
        elif chapter:
            T = cs.get(chapter, 0.0)
        else:
            T = qscore
        cred = r["score_claim_credibility"]; prim = r["score_primacy"]
        rel = r["score_source_reliability"] if r["score_source_reliability"] is not None else 0.5
        if profile == "prose":
            vivid = 0.15 if (r["epistemic_status"] == "observation" or tags & {"folklore", "opinion"}) else 0.0
            s = 0.45 * T + 0.20 * cred + 0.10 * prim + 0.10 * rel + vivid
        else:
            s = 0.45 * T + 0.25 * cred + 0.15 * prim + 0.15 * rel
        if chapter:
            if f"{chapter}:admitted" in buckets:
                s *= chap["admitted_penalty"]
            if prof and r["source_type"] in prof.get("preferred_source_types", []):
                s *= chap["preferred_type_boost"]
        if "udaypur_specific" in tags:
            s *= chap.get("udaypur_specific_boost", 1.0)
        tie = 2.0 if r["source_type"] in ("primary", "field_observation") else (r["score_recency"] or 0.0)
        out.append((round(s, 2), tie, s, r, T))
    out.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    res = []
    for s2, tie, s, r, T in out[:k]:
        prov = json.loads(r["provenance"])
        res.append({
            "chunk_id": r["chunk_id"], "source": r["parent_source_id"], "title": r["title"],
            "source_type": r["source_type"], "epistemic_status": r["epistemic_status"],
            "score": round(s, 3), "topical": round(T, 3),
            "credibility": r["score_claim_credibility"], "primacy": r["score_primacy"],
            "reliability": r["score_source_reliability"], "recency": r["score_recency"],
            "event_date": r["event_date"], "date_confidence": r["date_confidence"],
            "publication_date": r["publication_date"],
            "locator": {"heading": prov.get("heading_trail"), "page_start": prov.get("page_start"),
                        "page_end": prov.get("page_end"), "file": prov.get("file")},
            "tags": json.loads(r["relevance_tags"]),
            "corroboration_count": r["corroboration_count"],
            "contradiction_ids": json.loads(r["contradiction_ids"]),
            "contested_claims": json.loads(r["contested_claims"]),
            "superseded_by": r["superseded_by"], "duplicate_of": r["duplicate_of"],
            "supports": json.loads(r["supports"]) if r["supports"] else None,
            "text": r["text"],
        })
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?")
    ap.add_argument("--chapter")
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--profile", choices=["evidence", "prose"], default="evidence")
    ap.add_argument("--dense", action="store_true", help="add bge-m3 semantic search (~40 s model load)")
    ap.add_argument("--source")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args(argv)
    res = search(a.query, a.chapter, a.k, a.profile, a.dense, a.source)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for i, r in enumerate(res, 1):
        flags = []
        if r["contested_claims"]:
            flags.append("CONTESTED:" + ",".join(sorted({c["claim"] + "/" + c["disposition"] for c in r["contested_claims"]})))
        if r["superseded_by"]:
            flags.append(f"SUPERSEDED→{r['superseded_by']}")
        if r["duplicate_of"]:
            flags.append(f"dup-of {r['duplicate_of']}")
        flags += [t for t in r["tags"] if t in ("folklore", "opinion", "llm_regenerated", "single_source",
                                                 "ai_derived", "footnote", "verify_before_use")]
        loc = r["locator"]
        where = f"p.{loc['page_start']}" if loc["page_start"] else (loc["heading"] or "")[:60]
        print(f"\n[{i}] {r['chunk_id']}  score {r['score']}  (topical {r['topical']} | cred {r['credibility']} "
              f"| primacy {r['primacy']} | reliab {r['reliability']})")
        print(f"    {r['source_type']} / {r['epistemic_status']} · {r['title']} · {where} · event {r['event_date']} "
              f"({r['date_confidence']}) · corroborated by {r['corroboration_count']} work(s)")
        if flags:
            print("    " + " · ".join(flags))
        t = re.sub(r"\s+", " ", r["text"])
        print("    " + (t if a.full else t[:400] + ("…" if len(t) > 400 else "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
