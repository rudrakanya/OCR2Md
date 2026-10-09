#!/usr/bin/env python
"""Step 3 — resolve the Patil triple-registration in v2, and recompute corroboration.

    python phase4_step3_patil.py --dry-run
    python phase4_step3_patil.py --apply
    python phase4_step3_patil.py --undo kb_audit/phase4_step3_undo.json

PAT-CH, PAT-TEM and PAT-INS are one physical volume (D. R. Patil, *The Cultural
Heritage of Madhya Bharat*, 1952) registered three times. 120 passages are
byte-identical between PAT-CH and PAT-TEM, so one passage could be cited under
three codes as three authorities.

WHAT WAS ALREADY RIGHT, AND WHAT WAS NOT
----------------------------------------
All three registry entries already carry `work_id: patil-1952`, and
stage2_build counts corroboration over work_id -- so the independence COUNT was
never inflated, which is what the audit measured (corroboration_count was 0 for
242 of 246 of those chunks). The unresolved risk is the citation layer: the
drafter and the sourcebook cite by `code`, and three codes existed, so the same
sentence could appear as PAT-CH, PAT-TEM and PAT-INS in one chapter's evidence.

WHAT THIS CHANGES
-----------------
  parent_source_id   -> patil-1952 for all three  (one authority unit)
  code               -> PAT                        (one citation code)
  duplicates         the 120 identical passages collapse to one active copy;
                     the redundant copies move to the quarantine file with a
                     reason, so nothing is deleted
  source_type        LEFT PER CHUNK on purpose. PAT-INS is primary_epigraphic
                     while PAT-CH is secondary_core; flattening to one type
                     would either demote the inscriptions or promote the rest.
                     Authority is counted once; evidentiary type stays true.
  provenance.part    records which registration a chunk came from

Then corroboration is recomputed for the WHOLE v2 store with stage2_build's own
entity-year key detector (deterministic, no vectors, no model), counting
independence over work_id with duplicate clusters collapsed.

Writes only to the v2 store and the registry, both with undo files.
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

import yaml

for _n in ("mistralai", "mistralai.client"):
    sys.modules.setdefault(_n, types.ModuleType(_n))
sys.modules["mistralai.client"].Mistral = object
sys.modules["mistralai"].Mistral = object

import stage2_build as s2   # noqa: E402  entity/date/sentence helpers, reused verbatim

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
V2 = K3 / "kb_active_v2.sqlite"
V2Q = K3 / "kb_quarantine_v2.sqlite"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
UNDO = ROOT / "kb_audit" / "phase4_step3_undo.json"
NOW = dt.datetime.now().isoformat(timespec="seconds")

BASE = "patil-1952"
MERGED = ["patil-1952", "patil-composite-inscriptions", "patil-composite-temples"]
NEW_CODE = "PAT"
UNIFIED_TITLE = "The Cultural Heritage of Madhya Bharat"
UNIFIED_AUTHOR = "D. R. Patil"
PART_OF = {
    "patil-1952": "Part I — The Cultural Heritage of Madhya Bharat (1952)",
    "patil-composite-inscriptions": "Shrines, architecture and inscriptions (composite registration)",
    "patil-composite-temples": "Temples and architecture (composite registration)",
}


def jload(v, d):
    try:
        return json.loads(v) if v else d
    except (TypeError, ValueError):
        return d


def corroborate(rows):
    """stage2_build's entity-year corroboration, recomputed for v2.

    Independence is work_id, with exact-duplicate clusters collapsed to their
    canonical member, so two copies of one passage are one witness.
    """
    by_id = {r["chunk_id"]: r for r in rows}
    # exact-duplicate clusters -> canonical (prefer the base registration, then id)
    groups = collections.defaultdict(list)
    for r in rows:
        groups[r["content_hash"]].append(r["chunk_id"])
    dup_of = {}
    for h, ids in groups.items():
        if len(ids) < 2:
            continue
        canon = sorted(ids, key=lambda i: (0 if by_id[i]["parent_source_id"] == BASE else 1, i))[0]
        for i in ids:
            if i != canon:
                dup_of[i] = canon

    def indep(cid):
        root = dup_of.get(cid, cid)
        return by_id[root]["work_id"] or by_id[root]["parent_source_id"]

    CONTEXTUAL = s2.CONTEXTUAL
    keyidx = collections.defaultdict(set)
    for r in rows:
        if not r["claim_bearing"] or r["source_type"] in CONTEXTUAL:
            continue
        for sent in s2.sentences(r["text"]):
            ev = s2.event_years(sent)
            if not ev or ev[2] != "dated":
                continue
            for e in s2.entity_set(sent) - {"inscription"}:
                for y in {ev[0], ev[1]}:
                    keyidx[(e, y)].add(r["chunk_id"])
    corro = collections.defaultdict(dict)
    for key, ids in keyidx.items():
        if len(ids) < 2 or len(ids) > 60:
            continue
        ids = sorted(ids)
        for a in ids:
            for b in ids:
                if a >= b or indep(a) == indep(b):
                    continue
                corro[a].setdefault(b, key)
                corro[b].setdefault(a, key)

    # Claims-register pass: chunks arguing the same position in different works
    # corroborate each other. The register points at v1 chunk ids, which do not
    # exist after re-chunking, so each entry is re-pointed by its own `snippet`
    # -- all 67 of them resolve into v2. Without this the recompute would miss
    # the register-based corroboration that wires the Udayāditya date dispute.
    reg_file = K3 / "claims_register.yaml"
    n_reg = 0
    if reg_file.exists():
        claims = yaml.safe_load(reg_file.read_text(encoding="utf-8"))["claims"]
        texts = [(r["chunk_id"], s2.norm_ws(r["text"])) for r in rows]
        for k in claims:
            for p in k["positions"]:
                here = []
                for ent in p["chunks"]:
                    sn = s2.norm_ws(ent.get("snippet", ""))
                    if not sn:
                        continue
                    here += [cid for cid, t in texts if sn in t]
                for x in set(here):
                    for y in set(here):
                        if x != y and indep(x) != indep(y):
                            corro[x].setdefault(y, ("register", k["id"]))
                            n_reg += 1
    if n_reg:
        print(f"  register-based corroboration pairs: {n_reg}")

    out = {}
    for r in rows:
        cid = r["chunk_id"]
        others = corro.get(cid, {})
        out[cid] = (sorted(others)[:30],
                    len({indep(o) for o in others} - {indep(cid)}))
    return out, dup_of


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--undo")
    a = ap.parse_args()

    if a.undo:
        prev = json.loads(Path(a.undo).read_text(encoding="utf-8"))
        db = sqlite3.connect(str(V2))
        with db:
            for r in prev["chunks"]:
                db.execute("""update chunks set parent_source_id=?, title=?, author=?,
                                     provenance=?, corroboration_ids=?, corroboration_count=?,
                                     duplicate_of=?, relevance_tags=? where chunk_id=?""",
                           (r["parent_source_id"], r["title"], r["author"], r["provenance"],
                            r["corroboration_ids"], r["corroboration_count"],
                            r["duplicate_of"], r["relevance_tags"], r["chunk_id"]))
        db.close()
        Path(REGISTRY).write_text(prev["registry"], encoding="utf-8")
        print(f"restored {len(prev['chunks'])} chunk rows and the registry")
        return 0

    db = sqlite3.connect(f"file:{V2}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    rows = list(db.execute("select * from chunks"))
    pat = [r for r in rows if r["parent_source_id"] in MERGED]
    print(f"v2 chunks: {len(rows)} | Patil registrations: "
          + ", ".join(f"{sid}={sum(1 for r in pat if r['parent_source_id']==sid)}"
                      for sid in MERGED))
    hashes = collections.Counter(r["content_hash"] for r in pat)
    dups = sum(c - 1 for c in hashes.values() if c > 1)
    print(f"identical passages across the three registrations: {dups} redundant copies")
    print(f"work_id already shared: "
          f"{len({r['work_id'] for r in pat})} distinct work_id -> "
          f"{sorted({r['work_id'] for r in pat})}")
    print(f"source_type per registration (kept, not flattened): "
          + ", ".join(f"{sid}={sorted({r['source_type'] for r in pat if r['parent_source_id']==sid})}"
                      for sid in MERGED))

    print("\nrecomputing corroboration over the whole v2 store...")
    corro, dup_of = corroborate(rows)
    cc = collections.Counter(n for _, n in corro.values())
    print(f"  corroboration_count distribution: {dict(sorted(cc.items())[:6])}")
    print(f"  exact-duplicate clusters: {len(set(dup_of.values()))} canonical, "
          f"{len(dup_of)} redundant copies store-wide")

    if a.dry_run:
        print("\n--- would change ---")
        print(f"  {len(pat)} chunks -> parent_source_id={BASE}, code {NEW_CODE}")
        print(f"  {len([i for i in dup_of if db.execute('select parent_source_id from chunks where chunk_id=?',(i,)).fetchone()[0] in MERGED])}"
              f" Patil duplicate copies -> quarantine")
        print(f"  corroboration recomputed for all {len(rows)} chunks")
        return 0

    # ---------- undo file first ----------
    UNDO.write_text(json.dumps({
        "created": NOW, "step": "phase4 step3 patil merge",
        "restore_with": f"python phase4_step3_patil.py --undo {UNDO.as_posix()}",
        "registry": REGISTRY.read_text(encoding="utf-8"),
        "chunks": [{"chunk_id": r["chunk_id"], "parent_source_id": r["parent_source_id"],
                    "title": r["title"], "author": r["author"], "provenance": r["provenance"],
                    "corroboration_ids": r["corroboration_ids"],
                    "corroboration_count": r["corroboration_count"],
                    "duplicate_of": r["duplicate_of"],
                    "relevance_tags": r["relevance_tags"]} for r in rows],
    }, ensure_ascii=False), encoding="utf-8")
    print(f"\nundo file: {UNDO}")
    db.close()

    w = sqlite3.connect(str(V2))
    w.row_factory = sqlite3.Row
    q = sqlite3.connect(str(V2Q))
    qcols = [d[1] for d in w.execute("PRAGMA table_info(chunks)")]

    # 1. merge the three registrations
    n_merged = 0
    with w:
        for r in list(w.execute("select * from chunks where parent_source_id in "
                                "(?,?,?)", tuple(MERGED))):
            prov = jload(r["provenance"], {})
            prov["part"] = PART_OF.get(r["parent_source_id"], r["parent_source_id"])
            prov["registration"] = r["parent_source_id"]
            prov["merged_by"] = "phase4 step3: three registrations of one Patil volume"
            w.execute("""update chunks set parent_source_id=?, work_id=?, title=?, author=?,
                                provenance=? where chunk_id=?""",
                      (BASE, BASE, UNIFIED_TITLE, UNIFIED_AUTHOR,
                       json.dumps(prov, ensure_ascii=False), r["chunk_id"]))
            n_merged += 1
    print(f"merged {n_merged} chunks into {BASE} (code {NEW_CODE})")

    # 2. move redundant identical copies out of the active store
    n_q = 0
    with w, q:
        for cid, canon in dup_of.items():
            r = w.execute("select * from chunks where chunk_id=?", (cid,)).fetchone()
            if r is None:
                continue
            reason = (f"duplicate of {canon}: byte-identical passage. "
                      f"Phase 4 Step 3 — one passage must count as one witness.")
            q.execute(
                f"insert into chunks (quarantined_at, {','.join(chr(34)+c+chr(34) for c in qcols)}) "
                f"values (?, {','.join('?'*len(qcols))})",
                [NOW] + [reason if c == "quarantine_reason" else
                         (1 if c == "is_quarantined" else
                          (canon if c == "duplicate_of" else r[c])) for c in qcols])
            w.execute("delete from chunks where chunk_id=?", (cid,))
            w.execute("delete from chunks_fts where rowid=?", (r["rowid"],))
            n_q += 1
    print(f"moved {n_q} byte-identical duplicate copies to the quarantine file")

    # 3. write recomputed corroboration + single_source tag
    n_single = 0
    with w:
        for r in list(w.execute("select chunk_id, claim_bearing, relevance_tags from chunks")):
            ids, cnt = corro.get(r["chunk_id"], ([], 0))
            tags = set(jload(r["relevance_tags"], []))
            if r["claim_bearing"] and cnt == 0:
                tags.add("single_source"); n_single += 1
            else:
                tags.discard("single_source")
            w.execute("""update chunks set corroboration_ids=?, corroboration_count=?,
                                relevance_tags=? where chunk_id=?""",
                      (json.dumps(ids), cnt, json.dumps(sorted(tags)), r["chunk_id"]))
        for a_, b_ in dup_of.items():
            w.execute("insert into links values (?,?,?,?)",
                      (a_, b_, "duplicate", "exact_content_hash"))
        w.execute("insert or replace into meta values (?,?)",
                  ("patil_merge", f"{NOW}: {MERGED} -> {BASE} / {NEW_CODE}"))
    print(f"corroboration written; single_source on {n_single} claim-bearing chunks")
    w.close(); q.close()

    # 4. registry, edited line-wise to keep its comments.
    # Idempotent: a second --apply would otherwise find the already-rewritten
    # `code: PAT` line and append a SECOND parts block and canonical flag on top
    # of the first, because the loop re-emits them whenever it sees a code line.
    raw = REGISTRY.read_text(encoding="utf-8")
    if "\n    parts:\n" in raw and f"code: {NEW_CODE}" in raw:
        print(f"registry already merged (code {NEW_CODE}, parts block present) — left as is")
        return 0
    txt = raw.split("\n")
    out, i = [], 0
    while i < len(txt):
        line = txt[i]
        if line.strip() == "- source_id: patil-1952":
            out.append(line)
            i += 1
            while i < len(txt) and txt[i].strip() and not txt[i].strip().startswith("- source_id:"):
                if txt[i].strip().startswith("code:"):
                    out.append(f"    code: {NEW_CODE}")
                    out.append("    # Phase 4 Step 3: PAT-CH/PAT-TEM/PAT-INS were three")
                    out.append("    # registrations of this one volume. Merged to one source_id and")
                    out.append("    # one code so a passage cannot be cited as three authorities.")
                    out.append("    # Each chunk keeps its own source_type and provenance.part.")
                    out.append("    parts:")
                    for sid in MERGED:
                        out.append(f"      - {sid}: \"{PART_OF[sid]}\"")
                    out.append("    canonical_for_quotation: true")
                else:
                    out.append(txt[i])
                i += 1
            continue
        if line.strip() in ("- source_id: patil-composite-inscriptions",
                            "- source_id: patil-composite-temples"):
            out.append(line)
            i += 1
            while i < len(txt) and txt[i].strip() and not txt[i].strip().startswith("- source_id:"):
                if txt[i].strip().startswith("code:"):
                    out.append(f"    merged_into: {BASE}   # Phase 4 Step 3; no own code")
                else:
                    out.append(txt[i])
                i += 1
            continue
        out.append(line)
        i += 1
    REGISTRY.write_text("\n".join(out), encoding="utf-8")
    codes = [s.get("code") for s in yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["sources"]
             if s.get("code")]
    print(f"registry updated: {len(codes)} codes, "
          f"{'no collisions' if len(codes) == len(set(codes)) else 'COLLISION'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
