#!/usr/bin/env python
"""Step 2 — near-duplicate text that escaped exact-hash dedup in v2.

    python phase4_step2_neardup.py --report        # measure only
    python phase4_step2_neardup.py --apply         # collapse true duplicates
    python phase4_step2_neardup.py --undo kb_audit/phase4_neardup_undo.json

WHY THIS EXISTS. Step 3's dedup matched on exact `content_hash`, which is
sha1(text). Re-chunking gave the same passage different neighbours, so two
chunks can carry the same sentences with a few words of different context either
side -- different hash, both kept. That is the Patil "one source counted twice"
problem one layer down, and it was left unquantified.

METHOD: the project's own detector, reused verbatim from stage2_build so these
numbers are comparable with how v1 was deduped -- 5-word shingles, crc32, 64
MinHash permutations in 16 bands for candidate generation, then exact Jaccard on
the shingle sets. stage2_build treated Jaccard >= 0.5 as a duplicate link; that
is a deliberately loose bar for LINKING, and far too loose for COLLAPSING, so
three bands are reported separately:

    >= 0.95   effectively the same passage -> collapse
    0.80-0.95 heavy overlap, judged per case
    0.50-0.80 shared wording, usually genuinely distinct -> leave alone

WHAT ACTUALLY MATTERS is not the count but whether a duplicate inflates
corroboration -- one passage read as two independent witnesses. That is checked
directly against the corroboration metadata, as the Patil check was.

Memory-lean: shingle sets and signatures only, no vectors fetched. 10.6k chunks
is ~5 MB of signatures.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sqlite3
import sys
import types
from pathlib import Path

for _n in ("mistralai", "mistralai.client"):
    sys.modules.setdefault(_n, types.ModuleType(_n))
sys.modules["mistralai.client"].Mistral = object
sys.modules["mistralai"].Mistral = object

import stage2_build as s2   # shingles / minhash / UF, reused as-is

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
UNDO = ROOT / "kb_audit" / "phase4_neardup_undo.json"
REPORT = ROOT / "kb_audit" / "neardup.json"
COLLAPSE_AT = 0.95
NOW = dt.datetime.now().isoformat(timespec="seconds")


def jload(v, d):
    try:
        return json.loads(v) if v else d
    except (TypeError, ValueError):
        return d


def find_pairs(rows):
    """LSH candidates then exact Jaccard. Returns [(a, b, jaccard)] sorted desc."""
    shs, sigs = {}, {}
    for r in rows:
        sh = s2.shingles(r["text"])
        if len(sh) >= 8:
            shs[r["chunk_id"]] = sh
            sigs[r["chunk_id"]] = s2.minhash(sh)
    print(f"  signatures built for {len(sigs)} of {len(rows)} chunks "
          f"(skipped {len(rows)-len(sigs)} too short to fingerprint)")
    rows_per_band = s2.NPERM // s2.BANDS
    buckets = collections.defaultdict(list)
    for cid, sg in sigs.items():
        for b in range(s2.BANDS):
            buckets[(b, sg[b * rows_per_band:(b + 1) * rows_per_band].tobytes())].append(cid)
    cand = set()
    for ids in buckets.values():
        if 1 < len(ids) < 200:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    cand.add((ids[i], ids[j]) if ids[i] < ids[j] else (ids[j], ids[i]))
    print(f"  LSH candidate pairs: {len(cand)}")
    out = []
    for a, b in cand:
        j = len(shs[a] & shs[b]) / len(shs[a] | shs[b])
        if j >= 0.50:
            out.append((a, b, round(j, 3)))
    out.sort(key=lambda x: -x[2])
    return out


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--report", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--undo")
    a = ap.parse_args()

    import kb_target as T
    SQ = T.sqlite_path("v2-openai")
    QP = T.quarantine_path("v2-openai")

    if a.undo:
        prev = json.loads(Path(a.undo).read_text(encoding="utf-8"))
        db = sqlite3.connect(str(SQ))
        with db:
            for r in prev["rows"]:
                db.execute("""update chunks set duplicate_of=?, corroboration_ids=?,
                                     corroboration_count=?, provenance=?, relevance_tags=?
                              where chunk_id=?""",
                           (r["duplicate_of"], r["corroboration_ids"], r["corroboration_count"],
                            r["provenance"], r["relevance_tags"], r["chunk_id"]))
        db.close()
        print(f"restored {len(prev['rows'])} rows")
        return 0

    db = sqlite3.connect(f"file:{SQ}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    rows = list(db.execute("select * from chunks"))
    by_id = {r["chunk_id"]: r for r in rows}
    code = {}
    import yaml
    reg = yaml.safe_load((ROOT / "kb_audit" / "source_registry.yaml").read_text(encoding="utf-8"))
    for s in reg["sources"]:
        code[s["source_id"]] = s.get("code") or s["source_id"]

    print(f"v2 active chunks: {len(rows)}")
    print(f"exact content_hash duplicates still present: "
          f"{len(rows) - len({r['content_hash'] for r in rows})}")
    print("\nfinding near-duplicates (5-word shingles, 64-perm MinHash, 16 bands)")
    pairs = find_pairs(rows)

    bands = {">=0.95": [], "0.80-0.95": [], "0.50-0.80": []}
    for p in pairs:
        bands[">=0.95" if p[2] >= 0.95 else ("0.80-0.95" if p[2] >= 0.80 else "0.50-0.80")].append(p)
    print(f"\n{'band':12s} {'pairs':>6s}  {'within-source':>13s} {'cross-source':>13s}")
    for b, ps in bands.items():
        within = sum(1 for x, y, _ in ps
                     if by_id[x]["parent_source_id"] == by_id[y]["parent_source_id"])
        print(f"{b:12s} {len(ps):6d}  {within:13d} {len(ps)-within:13d}")

    # ---- what matters: does any of this inflate corroboration? -------------
    print("\n--- does a near-duplicate inflate corroboration? ---")
    uf = s2.UF()
    for x, y, j in bands[">=0.95"] + bands["0.80-0.95"]:
        uf.union(x, y)
    clusters = collections.defaultdict(set)
    for cid in list(by_id):
        if cid in uf.p:
            clusters[uf.find(cid)].add(cid)
    clusters = {k: v for k, v in clusters.items() if len(v) > 1}
    inflated = []
    for root, members in clusters.items():
        works = {by_id[m]["work_id"] or by_id[m]["parent_source_id"] for m in members}
        for m in members:
            cids = set(jload(by_id[m]["corroboration_ids"], []))
            twins = cids & (members - {m})
            if twins:
                inflated.append((m, sorted(twins)))
    print(f"  near-dup clusters (Jaccard >= 0.80): {len(clusters)}")
    print(f"  chunks citing a near-duplicate of themselves as corroboration: {len(inflated)}")
    for m, tw in inflated[:5]:
        print(f"     {m} <- {tw}")
    multi_work = [c for c in clusters.values()
                  if len({by_id[m]["work_id"] or by_id[m]["parent_source_id"] for m in c}) > 1]
    print(f"  clusters spanning more than one work: {len(multi_work)} "
          f"(these are the ones that could read as independent witnesses)")
    for c in multi_work[:5]:
        print(f"     {sorted(code.get(by_id[m]['parent_source_id'], '?') for m in c)}")

    print("\n--- the >=0.95 band, by source (collapse candidates) ---")
    per = collections.Counter()
    for x, y, _ in bands[">=0.95"]:
        per[code.get(by_id[x]["parent_source_id"], "?")] += 1
    for s, n in per.most_common():
        print(f"     {s:9s} {n}")
    print("\n  samples:")
    for x, y, j in bands[">=0.95"][:4]:
        print(f"\n   j={j} {code.get(by_id[x]['parent_source_id'])} {x} <-> {y}")
        print(f"     A: {by_id[x]['text'][:150]!r}")
        print(f"     B: {by_id[y]['text'][:150]!r}")
    print("\n  samples from 0.50-0.80 (expected to be genuinely distinct):")
    for x, y, j in bands["0.50-0.80"][:2]:
        print(f"\n   j={j} {code.get(by_id[x]['parent_source_id'])}")
        print(f"     A: {by_id[x]['text'][:130]!r}")
        print(f"     B: {by_id[y]['text'][:130]!r}")

    data = {"at": NOW, "active": len(rows),
            "bands": {b: len(p) for b, p in bands.items()},
            "clusters_ge_080": len(clusters),
            "self_corroborating": len(inflated),
            "multi_work_clusters": len(multi_work),
            "collapse_candidates": [[x, y, j] for x, y, j in bands[">=0.95"]]}
    REPORT.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {REPORT}")

    if a.report:
        return 0

    # ---- collapse only the >=0.95 band ------------------------------------
    uf2 = s2.UF()
    for x, y, _ in bands[">=0.95"]:
        uf2.union(x, y)
    groups = collections.defaultdict(set)
    for cid in list(by_id):
        if cid in uf2.p:
            groups[uf2.find(cid)].add(cid)
    groups = {k: v for k, v in groups.items() if len(v) > 1}
    if not groups:
        print("\nnothing at or above 0.95 to collapse.")
        return 0

    def canon_key(cid):
        r = by_id[cid]
        return (0 if (r["parent_source_id"] == "patil-1952") else 1,
                -(r["n_chars"] or 0), cid)

    db.close()
    UNDO.write_text(json.dumps({
        "at": NOW, "restore_with": f"python phase4_step2_neardup.py --undo {UNDO.as_posix()}",
        "rows": [{"chunk_id": r["chunk_id"], "duplicate_of": r["duplicate_of"],
                  "corroboration_ids": r["corroboration_ids"],
                  "corroboration_count": r["corroboration_count"],
                  "provenance": r["provenance"], "relevance_tags": r["relevance_tags"]}
                 for r in rows],
    }, ensure_ascii=False), encoding="utf-8")
    print(f"\nundo file: {UNDO}")

    w = sqlite3.connect(str(SQ))
    w.row_factory = sqlite3.Row
    q = sqlite3.connect(str(QP))
    qcols = [d[1] for d in w.execute("PRAGMA table_info(chunks)")]
    moved = 0
    with w, q:
        for root, members in groups.items():
            keep = sorted(members, key=canon_key)[0]
            others = [m for m in members if m != keep]
            kr = w.execute("select * from chunks where chunk_id=?", (keep,)).fetchone()
            prov = jload(kr["provenance"], {})
            prov["near_duplicates_collapsed"] = sorted(others)
            prov["near_dup_basis"] = f"minhash_jaccard>={COLLAPSE_AT} (phase 4 step 2)"
            w.execute("update chunks set provenance=? where chunk_id=?",
                      (json.dumps(prov, ensure_ascii=False), keep))
            for m in others:
                r = w.execute("select * from chunks where chunk_id=?", (m,)).fetchone()
                if r is None:
                    continue
                reason = (f"near-duplicate of {keep}: shingle Jaccard >= {COLLAPSE_AT}. "
                          f"One passage must count as one witness. Phase 4 Step 2.")
                q.execute(
                    f"insert into chunks (quarantined_at, {','.join(chr(34)+c+chr(34) for c in qcols)}) "
                    f"values (?, {','.join('?'*len(qcols))})",
                    [NOW] + [reason if c == "quarantine_reason" else
                             (1 if c == "is_quarantined" else
                              (keep if c == "duplicate_of" else r[c])) for c in qcols])
                w.execute("delete from chunks_fts where rowid=?", (r["rowid"],))
                w.execute("delete from chunks where chunk_id=?", (m,))
                w.execute("insert into links values (?,?,?,?)",
                          (m, keep, "duplicate", f"minhash_jaccard>={COLLAPSE_AT}"))
                moved += 1
    left = w.execute("select count(*) from chunks").fetchone()[0]
    w.close(); q.close()
    print(f"collapsed {len(groups)} clusters; moved {moved} copies to the quarantine file")
    print(f"v2 active now {left} chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
