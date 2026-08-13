#!/usr/bin/env python3
"""
audit_labels.py — measure whether the labeling layer is actually right.

label_chunks.py reports what it decided. That is not the same as being correct,
and the distinction matters here more than usual: these labels now gate
retrieval, so a wrong `toc` or a wrong `duplicate-of` removes real evidence from
the corpus permanently and silently. "It ran and produced plausible counts" is
not evidence of anything.

Four audits, ordered by how much damage the thing being audited can do:

  1. EXCLUSIONS   every chunk the retrievable gate removed, judged blind.
                  A false exclusion is the worst failure the layer can produce,
                  because nothing downstream can recover from it — the passage
                  simply ceases to exist as far as the manuscript is concerned.
  2. DUPLICATES   sampled pairs, checked for genuine near-identity. A false
                  duplicate silently deletes a distinct passage.
  3. STRUCTURAL   stratified sample per label, judged blind, per-label precision.
  4. QUALITY      is the score calibrated? Do low scores mean bad chunks?

"Judged blind" means the judge is shown the passage and asked to classify it
WITHOUT being told what the heuristic decided, then the two are compared. Asking
a model to confirm a label it has already been shown measures agreeableness.

Usage:
    python audit_labels.py --exclusions        # start here
    python audit_labels.py --structural -n 12
    python audit_labels.py --duplicates -n 30
    python audit_labels.py --all
    python audit_labels.py --all --no-judge    # deterministic checks only, free
"""
import argparse
import collections
import json
import random
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from kb_store import KBStore
from labels import ALL_STRUCTURAL, CONTENT, EVIDENCE_ROLES, jaccard, shingle_hash

OUT = Path("eval/results")

JUDGE_STRUCTURAL = """You classify a passage extracted from a scanned scholarly book.

Choose exactly ONE label for what the passage IS as a page element:

  title         a heading
  text          ordinary running prose — the default for anything substantive
  list          an enumerated or bulleted list
  table         tabular data
  caption       a SHORT label attached to a figure, plate or table (not a passage
                that merely begins by naming one)
  formula       displayed mathematics
  footnote      apparatus at the foot of a page
  toc           a table of contents, or a list of plates/figures
  index         a back-of-book index: names followed by page numbers
  bibliography  a reference list of published works
  header        a running head
  footer        a running foot or bare folio number

Then answer: could this passage support a factual claim in a history book?
`usable` = true for anything with substantive content, false ONLY for pure
apparatus (contents, index, bibliography, running heads) or unreadable OCR.

Return JSON only: {"label": "...", "usable": true, "why": "<8 words"}"""

JUDGE_DUPLICATE = """You are shown two passages from a corpus. Decide whether they are
NEAR-DUPLICATES: the same text, differing only in OCR noise, whitespace or a few words.

Two passages about the same subject in different words are NOT duplicates.
Two overlapping chunks that share a long verbatim run ARE duplicates.

Return JSON only: {"duplicate": true, "why": "<10 words"}"""


def _judge(client, model, system, user, max_tokens=300):
    from llm import complete_json
    return complete_json(client, model,
                         [{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                         max_tokens=max_tokens, temperature=0.0, quiet=True)


# ---------------------------------------------------------------------------
# 1. Exclusions — the highest-risk decision
# ---------------------------------------------------------------------------

def audit_exclusions(store, client, model, n=40, seed=3, judge=True):
    rows = store.db.execute(
        "SELECT l.chunk_id, l.structural, l.quality, l.issues, c.source, c.trail, c.text "
        "FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id "
        "WHERE l.retrievable=0").fetchall()
    rows = [dict(r) for r in rows]
    total = len(rows)
    if not total:
        print("Nothing is excluded — the gate is not removing anything."); return {}

    by_reason = collections.Counter()
    for r in rows:
        iss = json.loads(r["issues"]) if r["issues"] else []
        reason = next((i.split(":")[0] for i in iss
                       if i.split(":")[0] in ("duplicate-of", "non-evidential")), None)
        by_reason[reason or "low-quality"] += 1

    print(f"{total:,} chunk(s) excluded from retrieval")
    for k, v in by_reason.most_common():
        print(f"    {k:18s} {v:6,}")

    if not judge:
        return {"total": total, "by_reason": dict(by_reason)}

    # Duplicate demotions are audited by audit_duplicates, not here, and the
    # distinction is not pedantic: demoting a duplicate loses NOTHING, because
    # its twin stays retrievable. Asking "is this passage usable?" of a demoted
    # duplicate always answers yes and reports a catastrophe that has not
    # happened — the first run of this audit scored 50% that way, of which more
    # than half was this artefact. Only exclusions that remove content from the
    # corpus outright belong in a false-exclusion rate.
    content_loss = [r for r in rows
                    if not any(i.startswith("duplicate-of")
                               for i in (json.loads(r["issues"]) if r["issues"] else []))]
    print(f"\n  {len(rows) - len(content_loss):,} of these are duplicate demotions "
          f"(their twin is retained — no content lost; audited by --duplicates)")
    print(f"  {len(content_loss):,} remove content from the corpus outright — "
          f"auditing those")
    if not content_loss:
        return {"total": total, "by_reason": dict(by_reason), "content_loss": 0}

    rng = random.Random(seed)
    sample = rng.sample(content_loss, min(n, len(content_loss)))
    print(f"\njudging {len(sample)} of them blind ...", flush=True)

    wrong = []
    for r in sample:
        try:
            v = _judge(client, model, JUDGE_STRUCTURAL,
                       f"SECTION: {r['trail'] or '(none)'}\n\nPASSAGE:\n{r['text'][:2000]}")
        except Exception as e:                        # noqa: BLE001
            print(f"    judge failed on {r['chunk_id']}: {type(e).__name__}", file=sys.stderr)
            continue
        # The judge saying `usable` means the gate threw away something that
        # could have supported a claim.
        if v.get("usable"):
            iss = json.loads(r["issues"]) if r["issues"] else []
            wrong.append({"chunk_id": r["chunk_id"], "source": r["source"],
                          "heuristic": r["structural"], "judge": v.get("label"),
                          "why": v.get("why"), "issues": iss,
                          "text": r["text"][:260]})

    rate = len(wrong) / max(len(sample), 1)
    print(f"\nFALSE EXCLUSION RATE: {len(wrong)}/{len(sample)} = {rate * 100:.0f}%")
    print(f"  -> roughly {int(rate * len(content_loss)):,} of {len(content_loss):,} "
          f"content-removing exclusions may be wrong")
    for w in wrong[:10]:
        print(f"\n  chunk {w['chunk_id']} [{w['source'][:34]}]")
        print(f"    heuristic={w['heuristic']}  judge={w['judge']}  ({w['why']})")
        print(f"    issues={w['issues']}")
        print(f"    {w['text'][:200]}")
    return {"total": total, "by_reason": dict(by_reason),
            "content_removing": len(content_loss), "sampled": len(sample),
            "false_exclusions": len(wrong), "rate": round(rate, 3),
            "examples": wrong[:20]}


# ---------------------------------------------------------------------------
# 2. Duplicates
# ---------------------------------------------------------------------------

def audit_duplicates(store, client, model, n=30, seed=5, judge=True):
    rows = [dict(r) for r in store.db.execute(
        "SELECT l.chunk_id, l.issues, c.source, c.text FROM chunk_labels l "
        "JOIN chunks c ON c.rowid=l.chunk_id WHERE l.issues LIKE '%duplicate-of%'")]
    if not rows:
        print("No duplicates recorded."); return {}
    import re
    pairs = []
    for r in rows:
        m = re.search(r"duplicate-of:(\d+)", r["issues"])
        if m:
            keep = store.chunk(int(m.group(1)))
            if keep:
                pairs.append((r, keep))

    # Deterministic check first: what the shingle overlap actually is.
    sims = [jaccard(shingle_hash(a["text"]), shingle_hash(b["text"])) for a, b in pairs]
    lo = sum(1 for s in sims if s < 0.75)
    print(f"{len(pairs):,} duplicate pair(s); measured shingle similarity "
          f"min={min(sims):.2f} mean={sum(sims)/len(sims):.2f}")
    if lo:
        print(f"  ⚠ {lo} pair(s) below the 0.75 threshold they were demoted at")

    cross = sum(1 for a, b in pairs if a["source"] != b["source"])
    print(f"  {len(pairs) - cross:,} same-source, {cross:,} cross-source")

    if not judge:
        return {"pairs": len(pairs), "mean_similarity": round(sum(sims) / len(sims), 3),
                "cross_source": cross}

    rng = random.Random(seed)
    sample = rng.sample(pairs, min(n, len(pairs)))
    print(f"\njudging {len(sample)} pair(s) blind ...", flush=True)
    wrong = []
    for a, b in sample:
        try:
            v = _judge(client, model, JUDGE_DUPLICATE,
                       f"PASSAGE A:\n{a['text'][:1200]}\n\nPASSAGE B:\n{b['text'][:1200]}")
        except Exception:                             # noqa: BLE001
            continue
        if not v.get("duplicate"):
            wrong.append({"a": a["chunk_id"], "b": b["chunk_id"],
                          "why": v.get("why"), "a_text": a["text"][:200]})
    rate = len(wrong) / max(len(sample), 1)
    print(f"\nFALSE DUPLICATE RATE: {len(wrong)}/{len(sample)} = {rate * 100:.0f}%")
    for w in wrong[:6]:
        print(f"  {w['a']} vs {w['b']}: {w['why']}\n    {w['a_text'][:150]}")
    return {"pairs": len(pairs), "sampled": len(sample), "false_duplicates": len(wrong),
            "rate": round(rate, 3), "cross_source": cross,
            "mean_similarity": round(sum(sims) / len(sims), 3)}


# ---------------------------------------------------------------------------
# 3. Structural precision
# ---------------------------------------------------------------------------

def audit_structural(store, client, model, per_label=10, seed=7, judge=True):
    counts = {r["structural"]: r["n"] for r in store.db.execute(
        "SELECT structural, COUNT(*) n FROM chunk_labels GROUP BY structural")}
    print("labelled distribution:")
    for k, v in sorted(counts.items(), key=lambda t: -t[1]):
        print(f"    {k:14s} {v:6,}")
    if not judge:
        return {"counts": counts}

    rng = random.Random(seed)
    results, confusion = {}, collections.Counter()
    for label in sorted(counts):
        rows = [dict(r) for r in store.db.execute(
            "SELECT l.chunk_id, c.source, c.trail, c.text FROM chunk_labels l "
            "JOIN chunks c ON c.rowid=l.chunk_id WHERE l.structural=? "
            "ORDER BY RANDOM() LIMIT ?", (label, per_label))]
        if not rows:
            continue
        agree = 0
        for r in rows:
            try:
                v = _judge(client, model, JUDGE_STRUCTURAL,
                           f"SECTION: {r['trail'] or '(none)'}\n\n"
                           f"PASSAGE:\n{r['text'][:2000]}")
            except Exception:                         # noqa: BLE001
                continue
            got = (v.get("label") or "").lower()
            confusion[(label, got)] += 1
            if got == label:
                agree += 1
        results[label] = {"n": len(rows), "agree": agree,
                          "precision": round(agree / max(len(rows), 1), 2)}
        print(f"  {label:14s} precision {results[label]['precision']:.2f} "
              f"({agree}/{len(rows)})", flush=True)

    print("\nmost common disagreements (heuristic -> judge):")
    for (h, j), n in confusion.most_common(12):
        if h != j:
            print(f"    {h:14s} -> {j:14s} {n}")
    return {"counts": counts, "per_label": results,
            "confusion": {f"{h}->{j}": n for (h, j), n in confusion.items() if h != j}}


# ---------------------------------------------------------------------------
# 4. Quality calibration
# ---------------------------------------------------------------------------

def audit_quality(store):
    """Is the quality score doing anything? Deterministic, no judge."""
    buckets = collections.OrderedDict()
    for lo in (0.0, 0.2, 0.4, 0.6, 0.8):
        hi = lo + 0.2
        rows = store.db.execute(
            "SELECT COUNT(*) n, AVG(LENGTH(c.text)) len FROM chunk_labels l "
            "JOIN chunks c ON c.rowid=l.chunk_id WHERE l.quality >= ? AND l.quality < ?",
            (lo, hi)).fetchone()
        buckets[f"{lo:.1f}-{hi:.1f}"] = {"n": rows["n"],
                                         "mean_chars": int(rows["len"] or 0)}
    print("quality distribution:")
    for k, v in buckets.items():
        print(f"    {k}  {v['n']:6,} chunks   mean {v['mean_chars']:5,} chars")

    # A score that never varies is not a score. Report the spread honestly.
    distinct = store.db.execute(
        "SELECT COUNT(DISTINCT quality) n FROM chunk_labels").fetchone()["n"]
    top = store.db.execute(
        "SELECT COUNT(*) n FROM chunk_labels WHERE quality >= 0.95").fetchone()["n"]
    total = store.db.execute("SELECT COUNT(*) n FROM chunk_labels").fetchone()["n"]
    print(f"  {distinct} distinct values; {top:,}/{total:,} "
          f"({top / max(total,1) * 100:.0f}%) score >= 0.95")
    if top / max(total, 1) > 0.9:
        print("  ⚠ the score is nearly constant — it is not discriminating between "
              "chunks, so `min_quality` filtering buys almost nothing.")
    return {"buckets": buckets, "distinct_values": distinct, "near_perfect": top,
            "total": total}


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Audit the labeling and validation layer")
    ap.add_argument("--exclusions", action="store_true")
    ap.add_argument("--duplicates", action="store_true")
    ap.add_argument("--structural", action="store_true")
    ap.add_argument("--quality", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-judge", action="store_true", help="deterministic checks only")
    ap.add_argument("-n", type=int, default=40, help="sample size")
    ap.add_argument("--per-label", type=int, default=10)
    ap.add_argument("--out", default=str(OUT / "label_audit.json"))
    args = ap.parse_args()

    store = KBStore()
    if not store.db.execute("SELECT COUNT(*) n FROM chunk_labels").fetchone()["n"]:
        print("Nothing is labelled yet — run: python label_chunks.py --structural")
        sys.exit(1)

    judge = not args.no_judge
    client = model = None
    if judge:
        from llm import get_client
        client = get_client()
        model = CFG.eval.judge_model

    do_all = args.all or not any([args.exclusions, args.duplicates,
                                  args.structural, args.quality])
    report = {"judge_model": model if judge else None}

    if do_all or args.quality:
        print("\n=== 4. QUALITY CALIBRATION ===")
        report["quality"] = audit_quality(store)
    if do_all or args.exclusions:
        print("\n=== 1. EXCLUSIONS (highest risk) ===")
        report["exclusions"] = audit_exclusions(store, client, model, args.n, judge=judge)
    if do_all or args.duplicates:
        print("\n=== 2. DUPLICATES ===")
        report["duplicates"] = audit_duplicates(store, client, model, min(args.n, 30),
                                                judge=judge)
    if do_all or args.structural:
        print("\n=== 3. STRUCTURAL PRECISION ===")
        report["structural"] = audit_structural(store, client, model, args.per_label,
                                                judge=judge)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
