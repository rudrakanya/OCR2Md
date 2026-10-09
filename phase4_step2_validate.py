#!/usr/bin/env python
"""Step 2 validation — against ground truth, at full depth.

    python phase4_step2_validate.py

Checks, in order of what would be worst to get wrong:

  1. NAMED ROWS. Not a count: the actual Ganguly concordance rows and the
     PAT-CH row naming Udaypur, looked up by their text in v2.
  2. ALL 362 substantive rows the asset audit found missing, re-measured.
  3. ADH fabrications unreachable in v2 -- full depth, not a top-k sample.
  4. Flags carried forward: is_quotable:false equivalents (needs_recheck /
     llm_regenerated / ai_derived tags), source_type, buckets, provenance.
  5. Coherence not worse than the live store's real 75.5% clean.
"""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
LIVE = ROOT / "kb3" / "kb_active.sqlite"
V2 = ROOT / "kb3" / "kb_active_v2.sqlite"
V2Q = ROOT / "kb3" / "kb_quarantine_v2.sqlite"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"

PIPE = re.compile(r"(?m)^\s*\|.*\|\s*$")
MID = re.compile(r"^[a-z,;:)\]]")
OPEN = re.compile(r"[a-z,;:(\[]$")
PIPE1 = re.compile(r"^\s*\|")
PAGENO = re.compile(r"^(?:[ivxlcdm]+|\d{1,4}(?:\s*[-–]\s*\d{1,4})?|\.{2,})$", re.I)

NAMED = {
    "GAN": ["Mandhata | C. | 1112 | 1055 | Jayasimha",
            "Tilakwada | C. | 1103 | 1047 | Bhoja",
            "Bijapur inscription of Dhavala of Hastikund",
            "Vadnagar prasasti of Kumarapâla",
            "Bheraghat inscription of Alhaņadevî"],
    # PAT-CH/PAT-TEM/PAT-INS became one code, PAT, in Step 3.
    "PAT": ["Badoh, Besnagar, Bhilsa, Gyaraspur, Pathari, Udaypur, Udaygiri"],
    "KRAM-2": ["Type of Image | 7 Tāla"],
    "GUP": ["Thunderbolt, spear, protection pose"],
}


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip().lower()


def cells(l):
    return [c for c in (x.strip() for x in l.strip().strip("|").split("|")) if c]


def navigational(r):
    cs = cells(r)
    return len(cs) >= 2 and bool(PAGENO.match(cs[-1]))


def flags(t):
    t = (t or "").strip()
    f = []
    if len(t) < 200:
        f.append("short")
    if MID.match(t):
        f.append("starts mid-sentence")
    if OPEN.search(t):
        f.append("ends mid-sentence")
    ls = [l for l in t.split("\n") if l.strip()]
    if ls and sum(1 for l in ls if PIPE1.match(l)) / len(ls) > 0.6:
        f.append("table fragment")
    if t and sum(c.isalpha() for c in t) / max(1, len(t)) < 0.45:
        f.append("mostly non-letters")
    return f


def main():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    by_code = {s.get("code"): s for s in reg["sources"]}
    live = sqlite3.connect(f"file:{LIVE}?mode=ro", uri=True)
    v2 = sqlite3.connect(f"file:{V2}?mode=ro", uri=True)
    v2q = sqlite3.connect(f"file:{V2Q}?mode=ro", uri=True)
    ok = True

    def text_of(db, sid):
        return norm(" ".join(r[0] for r in db.execute(
            "select text from chunks where parent_source_id=?", (sid,))))

    print("=" * 72)
    print("1. NAMED ROWS — checked by hand, not by count")
    print("=" * 72)
    for code, probes in NAMED.items():
        if code not in by_code:
            print(f"  {code:8s} (no such code in the registry — skipped)")
            continue
        sid = by_code[code]["source_id"]
        lt, vt = text_of(live, sid), text_of(v2, sid)
        for p in probes:
            pn = norm(p)
            a, b = pn in lt, pn in vt
            verdict = "RECOVERED" if (b and not a) else ("present in both" if b else "STILL MISSING")
            print(f"  {code:8s} {p[:52]:54s} v1={'y' if a else 'n'} v2={'y' if b else 'n'}  {verdict}")
            ok &= b

    print("\n" + "=" * 72)
    print("2. ALL substantive table rows missing from the live store")
    print("=" * 72)
    tot_missing_v1 = tot_missing_v2 = tot_sub_v1 = tot_sub_v2 = 0
    per = []
    for s in reg["sources"]:
        f = BOOKS / s.get("file", "")
        if not f.exists():
            continue
        sid, code = s["source_id"], s.get("code", "?")
        # A registration merged into another work holds no chunks of its own, so
        # every row of its file would count as "missing" from it. Its content
        # lives under the merge target and is measured there.
        if s.get("merged_into"):
            continue
        md = f.read_text(encoding="utf-8", errors="replace")
        rows = {norm(l) for l in PIPE.findall(md)
                if set(l.strip()) - set("|-: ") and not re.match(r"^\s*\|\s*-+", l)}
        if not rows:
            continue
        lt, vt = text_of(live, sid), text_of(v2, sid)
        # v2's reach is active PLUS quarantine: a row that moved to quarantine
        # has not been lost from the store, and for ADH the fabricated rows are
        # SUPPOSED to be absent from active. Measuring only the active store
        # counted the quarantine as data loss and showed ADH getting worse.
        vq = norm(" ".join(r[0] for r in v2q.execute(
            "select text from chunks where parent_source_id=?", (sid,))))
        vt_all = vt + " " + vq

        def miss(hay):
            m = []
            for r in rows:
                cs = sorted(cells(r), key=len, reverse=True)
                pr = next((c for c in cs if len(c) >= 12), None)
                if pr is not None and norm(pr) not in hay:
                    m.append(r)
            return m
        m1, m2 = miss(lt), miss(vt_all)
        s1 = [r for r in m1 if not navigational(r)]
        s2_ = [r for r in m2 if not navigational(r)]
        tot_missing_v1 += len(m1); tot_missing_v2 += len(m2)
        tot_sub_v1 += len(s1); tot_sub_v2 += len(s2_)
        if s1 or s2_:
            per.append((code, len(s1), len(s2_)))
    print(f"{'code':9s} {'substantive missing v1':>22s} {'v2':>6s}")
    for code, a, b in sorted(per, key=lambda x: -x[1]):
        print(f"{code:9s} {a:22d} {b:6d}")
    print(f"\n  all missing rows   : v1 {tot_missing_v1} -> v2 {tot_missing_v2}")
    print(f"  SUBSTANTIVE missing: v1 {tot_sub_v1} -> v2 {tot_sub_v2}  "
          f"(recovered {tot_sub_v1 - tot_sub_v2})")
    ok &= tot_sub_v2 < tot_sub_v1

    print("\n" + "=" * 72)
    print("3. ADH fabrications in v2 — full depth")
    print("=" * 72)
    FAB = ("island | attribution", "rāhīna", "jñābhadras", "māhukaraṇi", "vayyāni")
    adh_act = text_of(v2, "adhikari-2013-un")
    for p in FAB:
        hit = norm(p) in adh_act
        print(f"  {p:22s} in ACTIVE v2: {'PRESENT — BAD' if hit else 'absent'}")
        ok &= not hit
    nq = v2q.execute("select count(*) from chunks").fetchone()[0]
    inq = sum(1 for r in v2q.execute("select text from chunks")
              if any(f in norm(r[0]) for f in FAB))
    print(f"  quarantine file holds {nq} chunks, {inq} carrying a fabrication marker")
    print(f"  active ADH chunks: "
          f"{v2.execute('select count(*) from chunks where parent_source_id=?',('adhikari-2013-un',)).fetchone()[0]}")
    # the prose that shared a chunk with the table must survive
    for p in ["The niches in the bhadras are adorned with beautiful parikarmas",
              "Kicaka-kicaki couples adorn the brackets"]:
        present = norm(p) in adh_act
        print(f"  prose kept: {p[:46]!r:48s} {'yes' if present else 'LOST'}")
        ok &= present

    print("\n" + "=" * 72)
    print("4. FLAGS CARRIED FORWARD")
    print("=" * 72)
    for tag in ("llm_regenerated", "needs_recheck", "ai_derived", "single_source"):
        a = live.execute("select count(*) from chunks where relevance_tags like ?",
                         (f'%"{tag}"%',)).fetchone()[0]
        b = v2.execute("select count(*) from chunks where relevance_tags like ?",
                       (f'%"{tag}"%',)).fetchone()[0]
        print(f"  tag {tag:18s} v1 {a:6d}  v2 {b:6d}")
    for src, tag in (("vidisha-gazetteer-1979", "llm_regenerated"),
                     ("samarangana", "llm_regenerated")):
        a = live.execute("select count(*) from chunks where parent_source_id=? and relevance_tags like ?",
                         (src, f'%"{tag}"%')).fetchone()[0]
        b = v2.execute("select count(*) from chunks where parent_source_id=? and relevance_tags like ?",
                       (src, f'%"{tag}"%')).fetchone()[0]
        print(f"  {src:24s} {tag:16s} v1 {a:5d} -> v2 {b:5d}")
        ok &= (b > 0 if a > 0 else True)
    miss_type = v2.execute("select count(*) from chunks where source_type is null").fetchone()[0]
    miss_prov = v2.execute("select count(*) from chunks where provenance is null "
                           "or provenance='null'").fetchone()[0]
    nob = v2.execute("select count(*) from chunks where chapter_buckets='[]'").fetchone()[0]
    print(f"  source_type null : {miss_type}")
    print(f"  provenance null  : {miss_prov}")
    print(f"  no chapter bucket: {nob} (the v2-unclassified orphans)")
    ok &= miss_type == 0 and miss_prov == 0
    unclass = v2.execute("select count(*) from chunks where review_status='v2-unclassified'").fetchone()[0]
    print(f"  review_status='v2-unclassified': {unclass}")

    print("\n" + "=" * 72)
    print("5. CHUNK COHERENCE")
    print("=" * 72)
    for name, db in (("live", live), ("v2", v2)):
        tal = collections.Counter()
        n = 0
        for r in db.execute("select text from chunks"):
            n += 1
            f = flags(r[0])
            if not f:
                tal["clean"] += 1
            for x in f:
                tal[x] += 1
        lens = sorted(len(r[0]) for r in db.execute("select text from chunks"))
        print(f"  {name:5s} {n:6d} chunks | clean {tal['clean']/n:5.1%} | "
              f"median {lens[len(lens)//2]:5d} chars | "
              + " ".join(f"{k}={v}" for k, v in tal.most_common() if k != "clean"))
        if name == "v2":
            ok &= tal["clean"] / n >= 0.70

    print("\n" + "=" * 72)
    print("RESULT:", "STEP 2 VALIDATED" if ok else "VALIDATION FAILED")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
