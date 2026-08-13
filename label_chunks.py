#!/usr/bin/env python3
"""
label_chunks.py — run the labeling and validation pass over the knowledge base.

Two passes, deliberately separated by cost:

  1. STRUCTURAL + VALIDATION   free, deterministic, runs over the whole corpus
     in seconds. Assigns the Unlimited-OCR structural label, an OCR-damage
     score, a quality score and an issue list, and decides `retrievable`.

  2. CONTENT + EVIDENCE ROLE   one LLM call per batch of chunks. Only run on
     chunks pass 1 marked retrievable, because paying a model to categorise an
     index page is waste.

Near-duplicate detection runs between them, over shingles, and is the pass that
finds what neither of the others can: the same passage entering the KB twice
because a source appears in both a Hindi original and its English translation,
or because an appendix reprints a chapter. Duplicates are not deleted — one is
kept retrievable and the rest are demoted, so a diversity-capped evidence pack
cannot be filled with three copies of one paragraph.

Everything is idempotent and resumable: labels are keyed by chunk id, and
`--only-missing` (the default) skips what is already labelled.

Usage:
    python label_chunks.py --structural          # free pass, whole corpus
    python label_chunks.py --duplicates
    python label_chunks.py --content --limit 500 # LLM pass, start small
    python label_chunks.py --content             # ...then all of it
    python label_chunks.py --report
    python label_chunks.py --review --structural toc     # spot-check a label
"""
import argparse
import collections
import json
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from kb_store import KBStore
from labels import (CONTENT, EVIDENCE_ROLES, ALL_STRUCTURAL, classify_structural,
                    is_retrievable, jaccard, shingle_hash, summarise, validate_chunk)

CONTENT_SYSTEM = """You categorise passages from the source corpus of a scholarly history of the \
Udayeśvara (Nīlakaṇṭheśvara) temple at Udaypur, Vidisha district, and the Paramāra dynasty of \
Malwa.

For each passage assign:

`content` — one to three categories from this list, most important first:
%s

`evidence_role` — exactly one:
%s

Rules:
- Judge what the passage IS, not what it is about. A modern scholar discussing an inscription is \
`epigraphy_meta` + `interpretation`; the inscription's own text is `inscription` + \
`primary_witness`.
- `primary_witness` is reserved for the historical object itself — an inscription's text, a \
Sanskrit prescription, testimony recorded from a resident. It is NOT for a reliable modern account.
- `observation` is for something the author measured, surveyed or saw: dimensions, condition, \
what stands where.
- If the passage is a contents list, index, bibliography or running header, use `apparatus` for \
both fields.
- `period_from`/`period_to`: the CE years the passage's CONTENT concerns, as integers (negative \
for BCE), or null. Not the publication date.

Return JSON only:
{"results": [{"i": 0, "content": ["..."], "evidence_role": "...", \
"period_from": null, "period_to": null, "confidence": 0.9}]}"""


def _system_prompt():
    c = "\n".join(f"  {k:22s} {v}" for k, v in CONTENT.items())
    r = "\n".join(f"  {k:18s} {v}" for k, v in EVIDENCE_ROLES.items())
    return CONTENT_SYSTEM % (c, r)


def load_chunks(store):
    rows = store.db.execute(
        "SELECT rowid, source, trail, heading, text FROM chunks ORDER BY rowid").fetchall()
    return [dict(r) for r in rows]


def existing_labels(store):
    return {r["chunk_id"]: dict(r)
            for r in store.db.execute("SELECT * FROM chunk_labels")}


def write_labels(store, rows):
    """Upsert label rows. A reviewed row is never overwritten by a machine."""
    with store.db:
        reviewed = {r["chunk_id"] for r in
                    store.db.execute("SELECT chunk_id FROM chunk_labels WHERE reviewed=1")}
        n = 0
        for r in rows:
            if r["chunk_id"] in reviewed:
                continue
            cols = list(r)
            ph = ",".join("?" * len(cols))
            store.db.execute(
                f"INSERT INTO chunk_labels ({','.join(cols)}) VALUES ({ph}) "
                f"ON CONFLICT(chunk_id) DO UPDATE SET "
                + ",".join(f"{c}=excluded.{c}" for c in cols if c != "chunk_id"),
                [r[c] for c in cols])
            n += 1
    return n


# ---------------------------------------------------------------------------
# Pass 1 — structural + validation (free)
# ---------------------------------------------------------------------------

def pass_structural(store, chunks, min_quality):
    rows = []
    for c in chunks:
        s = classify_structural(c)
        q, issues = validate_chunk(c, s)
        rows.append({
            "chunk_id": c["rowid"],
            "structural": s,
            "quality": q,
            "issues": json.dumps(issues, ensure_ascii=False),
            "retrievable": int(is_retrievable(q, issues, min_quality)),
            "labeled_by": "heuristic",
            "confidence": 0.8,
        })
    return rows


# ---------------------------------------------------------------------------
# Near-duplicate detection
# ---------------------------------------------------------------------------

def pass_duplicates(store, chunks, threshold=0.75):
    """Find near-identical chunks; keep one, demote the rest.

    Blocked by a cheap signature so this is not O(n^2) over 9,467 chunks: two
    chunks can only be near-duplicates if they share at least one shingle, so
    candidates are gathered from an inverted index and only those pairs are
    compared properly.
    """
    sigs = {}
    inverted = collections.defaultdict(list)
    for c in chunks:
        s = shingle_hash(c["text"])
        if not s:
            continue
        sigs[c["rowid"]] = s
        for h in list(s)[:24]:               # a sample is enough to co-locate
            inverted[h].append(c["rowid"])

    seen, groups = set(), []
    for cid, sig in sigs.items():
        if cid in seen:
            continue
        cand = {o for h in list(sig)[:24] for o in inverted[h] if o != cid and o not in seen}
        dupes = [o for o in cand if jaccard(sig, sigs[o]) >= threshold]
        if dupes:
            group = sorted([cid] + dupes)
            for g in group:
                seen.add(g)
            groups.append(group)
    return groups


def demote_duplicates(store, groups, chunks_by_id):
    """Keep the longest member of each group retrievable; demote the others."""
    updates = 0
    with store.db:
        for g in groups:
            keep = max(g, key=lambda i: len(chunks_by_id[i]["text"]))
            for cid in g:
                if cid == keep:
                    continue
                row = store.db.execute(
                    "SELECT issues FROM chunk_labels WHERE chunk_id=?", (cid,)).fetchone()
                issues = json.loads(row["issues"]) if row and row["issues"] else []
                tag = f"duplicate-of:{keep}"
                if tag not in issues:
                    issues.append(tag)
                store.db.execute(
                    "UPDATE chunk_labels SET retrievable=0, issues=? WHERE chunk_id=?",
                    (json.dumps(issues, ensure_ascii=False), cid))
                updates += 1
    return updates


# ---------------------------------------------------------------------------
# Pass 2 — content + evidence role (LLM)
# ---------------------------------------------------------------------------

def pass_content(store, chunks, batch=12, workers=4, limit=None, model=None):
    from llm import complete_json, get_client, parallel
    client = get_client()
    model = model or CFG.comprehension.model
    system = _system_prompt()

    todo = chunks[:limit] if limit else chunks
    if not todo:
        return []
    groups = [todo[i:i + batch] for i in range(0, len(todo), batch)]
    print(f"labelling {len(todo):,} chunk(s) in {len(groups)} batch(es) with {model}",
          flush=True)

    def one(g):
        items = [{"i": k, "source": c["source"], "section": (c["trail"] or "")[:120],
                  "text": c["text"][:1500]} for k, c in enumerate(g)]
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": json.dumps(items, ensure_ascii=False)}]
        # Headroom for the larger batch: each result is ~40 tokens, so 24 per
        # call needs ~1k plus JSON overhead. The cost of this pass is per
        # REQUEST, not per token, so bigger batches roughly halve wall-clock.
        return g, complete_json(client, model, msgs, max_tokens=3500,
                                temperature=0.0, quiet=True)

    def failed(g, e):
        print(f"    batch of {len(g)} failed: {type(e).__name__}", file=sys.stderr)
        return g, {"results": []}

    rows = []
    done = 0
    for start in range(0, len(groups), 20):          # checkpoint every 20 batches
        window = groups[start:start + 20]
        for g, data in parallel(one, window, workers=workers, on_error=failed):
            got = {int(r["i"]): r for r in (data or {}).get("results", []) if "i" in r}
            for k, c in enumerate(g):
                r = got.get(k)
                if not r:
                    continue
                cats = [x for x in (r.get("content") or []) if x in CONTENT][:3]
                role = r.get("evidence_role")
                rows.append({
                    "chunk_id": c["rowid"],
                    "content": json.dumps(cats, ensure_ascii=False),
                    "evidence_role": role if role in EVIDENCE_ROLES else None,
                    "period_from": r.get("period_from"),
                    "period_to": r.get("period_to"),
                    "labeled_by": "llm",
                    "confidence": float(r.get("confidence") or 0.7),
                })
        done += sum(len(g) for g in window)
        if rows:
            write_labels(store, rows)
            rows = []
        print(f"  {done:,}/{len(todo):,} labelled", flush=True)
    return rows


# ---------------------------------------------------------------------------

def report(store):
    rows = [dict(r) for r in store.db.execute(
        "SELECT l.*, c.source FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id")]
    if not rows:
        print("No labels yet. Run: python label_chunks.py --structural"); return
    for r in rows:
        r["content"] = json.loads(r["content"]) if r.get("content") else []
        r["issues"] = json.loads(r["issues"]) if r.get("issues") else []
        # Unlabelled is a real state, not a missing value: the content pass is
        # optional and costs money, so the report must render before it runs.
        r["structural"] = r.get("structural") or "unlabelled"
        r["evidence_role"] = r.get("evidence_role") or "(not yet labelled)"
    s = summarise(rows)

    total = store.count()
    print(f"{s['n']:,} of {total:,} chunks labelled "
          f"({s['n'] / max(total, 1) * 100:.1f}%)   mean quality {s['mean_quality']}")
    print(f"{s['retrievable']:,} retrievable "
          f"({s['retrievable'] / max(s['n'], 1) * 100:.1f}%), "
          f"{s['n'] - s['retrievable']:,} excluded\n")

    print("STRUCTURAL")
    for k, v in s["structural"].most_common():
        print(f"  {k:16s} {v:6,}")
    if s["content"]:
        print("\nCONTENT")
        for k, v in s["content"].most_common():
            print(f"  {k:22s} {v:6,}")
    if s["evidence_role"]:
        print("\nEVIDENCE ROLE")
        for k, v in s["evidence_role"].most_common():
            print(f"  {k:18s} {v:6,}")
    print("\nISSUES")
    for k, v in s["issues"].most_common():
        print(f"  {k:22s} {v:6,}")

    # What each source contributes, which is the question the labels exist to answer.
    print("\nPRIMARY WITNESS material by source")
    q = store.db.execute(
        "SELECT c.source, COUNT(*) n FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id"
        " WHERE l.evidence_role='primary_witness' GROUP BY c.source ORDER BY n DESC LIMIT 12")
    got = q.fetchall()
    if got:
        for r in got:
            print(f"  {r['n']:5,}  {r['source']}")
    else:
        print("  (none yet — run the --content pass)")


def review(store, structural=None, role=None, n=8):
    sql = ("SELECT l.*, c.source, c.trail, c.text FROM chunk_labels l "
           "JOIN chunks c ON c.rowid=l.chunk_id WHERE 1=1")
    params = []
    if structural:
        sql += " AND l.structural=?"; params.append(structural)
    if role:
        sql += " AND l.evidence_role=?"; params.append(role)
    sql += " ORDER BY RANDOM() LIMIT ?"
    params.append(n)
    for r in store.db.execute(sql, params):
        issues = json.loads(r["issues"]) if r["issues"] else []
        content = json.loads(r["content"]) if r["content"] else []
        print(f"--- chunk {r['chunk_id']}  [{r['source'][:40]}] ---")
        print(f"    structural={r['structural']}  role={r['evidence_role']}  "
              f"content={content}")
        print(f"    quality={r['quality']}  retrievable={bool(r['retrievable'])}  "
              f"issues={issues}")
        print(f"    {(r['trail'] or '')[:90]}")
        print(f"    {r['text'][:220].replace(chr(10), ' ')}\n")


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Label and validate the knowledge base")
    ap.add_argument("--structural", action="store_true", help="free pass: layout + quality")
    ap.add_argument("--duplicates", action="store_true", help="near-duplicate demotion")
    ap.add_argument("--content", action="store_true", help="LLM pass: category + role")
    ap.add_argument("--all", action="store_true", help="structural, duplicates, then content")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--review", action="store_true", help="print a random sample")
    ap.add_argument("--structural-filter", dest="sfilter", help="--review: one structural label")
    ap.add_argument("--role", help="--review: one evidence role")
    ap.add_argument("--limit", type=int, help="--content: cap the number of chunks")
    ap.add_argument("--batch", type=int, default=24)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--min-quality", type=float, default=0.45)
    ap.add_argument("--dup-threshold", type=float, default=0.75)
    ap.add_argument("--redo", action="store_true", help="relabel chunks that already have labels")
    args = ap.parse_args()

    store = KBStore()
    if not store.count():
        print("The store is empty — run build_kb.py first."); sys.exit(1)

    if args.report:
        report(store); return
    if args.review:
        review(store, args.sfilter, args.role); return

    chunks = load_chunks(store)
    have = existing_labels(store)

    if args.structural or args.all:
        rows = pass_structural(store, chunks, args.min_quality)
        n = write_labels(store, rows)
        print(f"structural + validation: {n:,} chunk(s) labelled")

    if args.duplicates or args.all:
        groups = pass_duplicates(store, chunks, args.dup_threshold)
        by_id = {c["rowid"]: c for c in chunks}
        demoted = demote_duplicates(store, groups, by_id)
        dup_total = sum(len(g) for g in groups)
        print(f"near-duplicates: {len(groups):,} group(s) covering {dup_total:,} chunk(s); "
              f"{demoted:,} demoted, {len(groups):,} kept")

    if args.content or args.all:
        have = existing_labels(store)
        pool = [c for c in chunks
                if have.get(c["rowid"], {}).get("retrievable", 1)
                and (args.redo or not have.get(c["rowid"], {}).get("content"))]
        if not pool:
            print("content: nothing to do (every retrievable chunk is already labelled)")
        else:
            pass_content(store, pool, batch=args.batch, workers=args.workers,
                         limit=args.limit)

    print()
    report(store)


if __name__ == "__main__":
    main()
