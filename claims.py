#!/usr/bin/env python3
"""
claims.py — typed claim extraction and conflict detection (§2.4).

v1 found 116 "conflicts" by numeric divergence across sources on the same
sub-unit. That is a good heuristic and it cannot tell *two sources disagreeing
about the temple's completion date* from *two sources measuring different
things*. Grouping by proximity in an outline is grouping by the wrong key.

Here a claim is structured — (subject_entity, predicate, object) with a type and
a provenance — so conflicts can be grouped by what they are actually about:

    group by (subject_entity, predicate)   not by sub-unit adjacency
    separate genuine from apparent         different referents, units, eras
    brief each side with its source's stance and reliability_notes (§2.1)

The output remains **candidates for judgement, not adjudications**. v1's
limitation #3 is correct and stays correct: a numeric divergence between an
11th-century praśasti and a 1952 survey is a research question, not a bug. What
changes is that the historian gets a briefed decision instead of two bare
numbers.

`scope` separates claims extracted from the corpus from claims extracted from
the drafted manuscript (§5.3). They are compared against each other, but a
manuscript claim is never evidence for anything.

Usage:
    python claims.py --extract --limit 400     # corpus claims (start small)
    python claims.py --conflicts               # grouped, briefed candidates
    python claims.py --extract-manuscript --dir chapter_drafts
    python claims.py --stats
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from doc_understanding import load_all as load_dossiers
from entities import EntityIndex
from kb_store import KBStore
from llm import complete_json, get_client, parallel

CLAIM_TYPES = ("date_event", "attribution", "measurement", "identification",
               "interpretation", "quotation")

EXTRACT_SYSTEM = """You extract structured factual claims from a passage of a scholarly source \
about the Udayeśvara (Nīlakaṇṭheśvara) temple at Udaypur and the Paramāra dynasty of Malwa.

A claim is (subject, predicate, object) — one assertion, checkable, standing alone.

  date_event      "Udayeśvara temple | completed | 1080 CE"
  attribution     "Udayeśvara temple | built by | Udayāditya"
  measurement     "Udayeśvara temple sikhara | height | 24 m"
  identification  "Nīlakaṇṭheśvara | is the same as | Udayeśvara"
  interpretation  the author's reading, offered as such
  quotation       the source quoting another text or an inscription

Rules:
- Extract only what THIS passage asserts. Do not add anything you know.
- `subject` must be a named thing wherever possible — a person, place, monument, dynasty, text \
or inscription. Skip claims whose subject is a pronoun you cannot resolve.
- Put dates, units and conditions in `qualifiers` ("according to Cunningham", "circa", "per the \
praśasti"), NOT inside `object`.
- If the passage asserts nothing checkable — a table of contents, a heading, bibliography, OCR \
noise — return {"claims": []}.

Return JSON only:
{"claims": [{"subject": "...", "predicate": "...", "object": "...",
             "type": "date_event", "qualifiers": {"circa": true}, "confidence": 0.9}]}"""

_NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


def claim_id(scope, source, chunk_id, subject, predicate, obj):
    raw = f"{scope}|{source}|{chunk_id}|{subject}|{predicate}|{obj}".lower()
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def extract_from_chunks(store, entities, rows, client=None, model=None, workers=6):
    """Extract claims from chunk rows. Returns the number inserted."""
    client = client or get_client()
    model = model or CFG.comprehension.model

    def one(r):
        msgs = [{"role": "system", "content": EXTRACT_SYSTEM},
                {"role": "user", "content":
                    f"SOURCE: {r['source']}\nSECTION: {r['trail']}\n\n{r['text'][:2400]}"}]
        return r, complete_json(client, model, msgs, max_tokens=2000,
                                temperature=0.0, quiet=True)

    def failed(r, e):
        return r, {"claims": []}

    n = 0
    with store.db:
        for r, data in parallel(one, rows, workers=workers, stagger=0.2, on_error=failed):
            for c in (data or {}).get("claims", []):
                subj, pred, obj = (c.get("subject") or "").strip(), \
                    (c.get("predicate") or "").strip(), (c.get("object") or "").strip()
                if not (subj and pred):
                    continue
                ctype = c.get("type") if c.get("type") in CLAIM_TYPES else "interpretation"
                # Resolve the subject to a registry entity where possible: that
                # is what lets conflicts group by the thing rather than by the
                # spelling. Unresolved subjects keep their surface form and
                # simply group less well.
                eid = entities.resolve(subj)
                store.db.execute(
                    "INSERT OR REPLACE INTO claims (claim_id, scope, subject_entity, predicate,"
                    " object, qualifiers, claim_type, source, page_start, page_end, chunk_id,"
                    " confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (claim_id("corpus", r["source"], r["rowid"], subj, pred, obj),
                     "corpus", eid or subj, pred, obj,
                     json.dumps(c.get("qualifiers") or {}, ensure_ascii=False), ctype,
                     r["source"], r["page_start"], r["page_end"], r["rowid"],
                     float(c.get("confidence") or 0.7)))
                n += 1
    return n


def extract_from_manuscript(store, entities, chapters, client=None, model=None, workers=4):
    """Extract claims from drafted chapters — the input to §5.3's coherence pass."""
    client = client or get_client()
    model = model or CFG.comprehension.model

    jobs = []
    for n, path in chapters:
        text = Path(path).read_text(encoding="utf-8").split("## Notes")[0]
        for i in range(0, len(text), 9000):
            jobs.append((n, path, text[i:i + 9000]))

    def one(job):
        n, path, seg = job
        msgs = [{"role": "system", "content": EXTRACT_SYSTEM},
                {"role": "user", "content": f"DRAFTED CHAPTER {n}\n\n{seg}"}]
        return n, complete_json(client, model, msgs, max_tokens=2500,
                                temperature=0.0, quiet=True)

    def failed(job, e):
        return job[0], {"claims": []}

    total = 0
    with store.db:
        store.db.execute("DELETE FROM claims WHERE scope='manuscript'")
        for n, data in parallel(one, jobs, workers=workers, stagger=0.3, on_error=failed):
            for c in (data or {}).get("claims", []):
                subj, pred, obj = (c.get("subject") or "").strip(), \
                    (c.get("predicate") or "").strip(), (c.get("object") or "").strip()
                if not (subj and pred):
                    continue
                eid = entities.resolve(subj)
                store.db.execute(
                    "INSERT OR REPLACE INTO claims (claim_id, scope, subject_entity, predicate,"
                    " object, qualifiers, claim_type, source, chapter, confidence)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (claim_id("manuscript", f"ch{n}", n, subj, pred, obj),
                     "manuscript", eid or subj, pred, obj,
                     json.dumps(c.get("qualifiers") or {}, ensure_ascii=False),
                     c.get("type") if c.get("type") in CLAIM_TYPES else "interpretation",
                     f"chapter-{n:02d}", n, float(c.get("confidence") or 0.7)))
                total += 1
    return total


def _numbers(s):
    return {x.replace(",", "") for x in _NUM_RE.findall(s or "")}


def _predicate_key(pred):
    """Loose predicate grouping: 'was built by' and 'built by' are one relation."""
    p = re.sub(r"\b(was|were|is|are|has|have|had|been|being)\b", " ", (pred or "").lower())
    return re.sub(r"[^a-z ]", " ", p).split()


def find_conflicts(store, scope="corpus", min_sources=2):
    """Group claims by (subject, predicate) and surface incompatible objects."""
    rows = store.db.execute(
        "SELECT * FROM claims WHERE scope=? AND claim_type IN "
        "('date_event','measurement','attribution','identification')", (scope,)).fetchall()

    groups = collections.defaultdict(list)
    for r in rows:
        key_words = _predicate_key(r["predicate"])
        key = (r["subject_entity"], " ".join(sorted(set(key_words))[:3]))
        groups[key].append(dict(r))

    conflicts = []
    for (subj, pred), items in groups.items():
        if len(items) < 2:
            continue
        srcs = {i["source"] for i in items}
        if scope == "corpus" and len(srcs) < min_sources:
            continue                       # one source disagreeing with itself is an OCR issue
        objs = {}
        for i in items:
            objs.setdefault((i["object"] or "").strip().lower(), []).append(i)
        if len(objs) < 2:
            continue

        # Numeric divergence is the strong signal; differing prose for the same
        # value is usually paraphrase, not disagreement.
        nums = [(_numbers(o), grp) for o, grp in objs.items()]
        numeric = [n for n, _ in nums if n]
        genuine = len(numeric) >= 2 and len({frozenset(n) for n in numeric}) > 1
        conflicts.append({
            "subject": subj, "predicate": pred,
            "kind": "numeric" if genuine else "verbal",
            "sides": [{"object": o,
                       "sources": sorted({i["source"] for i in grp}),
                       "pages": sorted({i["page_start"] for i in grp if i["page_start"]}),
                       "chapters": sorted({i["chapter"] for i in grp if i["chapter"]}),
                       "type": grp[0]["claim_type"]}
                      for o, grp in objs.items()],
        })
    conflicts.sort(key=lambda c: (c["kind"] != "numeric", -len(c["sides"])))
    return conflicts


def brief_conflicts(conflicts, dossiers, entities):
    """Attach each side's source stance and reliability notes (§2.4)."""
    for c in conflicts:
        eid = c["subject"]
        e = entities.by_id.get(eid)
        c["subject_label"] = e["canonical"] if e else eid
        for side in c["sides"]:
            side["authority"] = []
            for s in side["sources"]:
                d = dossiers.get(s) or {}
                side["authority"].append({
                    "source": s,
                    "kind": d.get("kind"),
                    "stance": (d.get("stance") or "")[:220],
                    "reliability": (d.get("reliability_notes") or [])[:2],
                })
    return conflicts


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Extract claims and detect conflicts")
    ap.add_argument("--extract", action="store_true", help="extract corpus claims")
    ap.add_argument("--extract-manuscript", action="store_true")
    ap.add_argument("--dir", default="chapter_drafts")
    ap.add_argument("--limit", type=int, default=400, help="chunks to extract from")
    ap.add_argument("--source", help="restrict extraction to one source")
    ap.add_argument("--conflicts", action="store_true")
    ap.add_argument("--scope", default="corpus", choices=["corpus", "manuscript"])
    ap.add_argument("--out", default="book/_conflicts.json")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    store, entities = KBStore(), EntityIndex.load()

    if args.extract:
        sql = "SELECT rowid,source,trail,text,page_start,page_end FROM chunks WHERE length(text)>500"
        params = []
        if args.source:
            sql += " AND source=?"; params.append(args.source)
        # Prefer chunks that name a registry entity: those are the ones whose
        # claims can group, and therefore the ones that can ever conflict.
        sql = (f"SELECT c.* FROM ({sql}) c JOIN entity_mentions m ON m.chunk_id=c.rowid"
               f" GROUP BY c.rowid ORDER BY COUNT(DISTINCT m.entity_id) DESC LIMIT ?")
        params.append(args.limit)
        rows = [dict(r) for r in store.db.execute(sql, params)]
        print(f"extracting claims from {len(rows)} entity-dense chunks ...", flush=True)
        n = extract_from_chunks(store, entities, rows)
        print(f"{n} corpus claim(s) stored")

    if args.extract_manuscript:
        chapters = []
        for p in sorted(Path(args.dir).glob("chapter-*.md")):
            m = re.search(r"chapter-(\d+)", p.name)
            if m:
                chapters.append((int(m.group(1)), p))
        if not chapters:
            print(f"no chapters in {args.dir}"); sys.exit(1)
        print(f"extracting claims from {len(chapters)} drafted chapter(s) ...", flush=True)
        n = extract_from_manuscript(store, entities, chapters)
        print(f"{n} manuscript claim(s) stored")

    if args.conflicts:
        dossiers = load_dossiers()
        conflicts = brief_conflicts(find_conflicts(store, args.scope), dossiers, entities)
        numeric = [c for c in conflicts if c["kind"] == "numeric"]
        print(f"\n{len(conflicts)} conflict candidate(s) in scope '{args.scope}' "
              f"— {len(numeric)} with numeric divergence\n")
        for c in conflicts[:25]:
            print(f"  [{c['kind']:7s}] {c['subject_label']} — {c['predicate']}")
            for s in c["sides"]:
                where = (f"ch {s['chapters']}" if s["chapters"]
                         else f"{', '.join(x[:34] for x in s['sources'])}")
                print(f"      {s['object'][:60]:62s} {where}")
                for a in s.get("authority", [])[:1]:
                    if a.get("stance"):
                        print(f"        └ {a['kind']}: {a['stance'][:90]}")
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(conflicts, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
        print(f"\n-> {args.out}")
        print("These are CANDIDATES for your judgement, not adjudications. A divergence "
              "between a praśasti and a modern survey is a research question.")

    if args.stats or not any([args.extract, args.extract_manuscript, args.conflicts]):
        for k, v in store.stats().items():
            print(f"  {k:20s} {v:>8,}")
        by_type = store.db.execute(
            "SELECT scope, claim_type, COUNT(*) n FROM claims GROUP BY scope, claim_type"
            " ORDER BY n DESC").fetchall()
        for r in by_type:
            print(f"  {r['scope']:11s} {r['claim_type']:16s} {r['n']:>6,}")


if __name__ == "__main__":
    main()
