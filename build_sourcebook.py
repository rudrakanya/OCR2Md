#!/usr/bin/env python
"""Build the unified book sourcebook: every chapter, with cited KB evidence.

    python build_sourcebook.py

Writes two files:
    source_codes.md       the code registry — one code per source, defined once
    BOOK_SOURCEBOOK.md    17 sections of grouped, cited excerpts + a coverage matrix

This gathers and cites; it writes no chapter prose. Selection, grouping and
ranking are deterministic, so the sourcebook can be rebuilt and diffed.
"""
from __future__ import annotations

import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

import chromadb
import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "kb3" / "chroma"
from kb_target import collection as _kb_collection  # noqa: E402
COLLECTION = _kb_collection()      # resolved through kb_target; see kb3/active_store.txt
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
CHAPTERS = ROOT / "kb3" / "chapters.yaml"
import datetime as _dt
NOW_STR = _dt.datetime.now().isoformat(timespec="seconds")
PAGES_UNRELIABLE = set(json.loads((ROOT / "kb3" / "pages_unreliable.json").read_text()))

# Not books. `ai-derived` holds six model-written synthesis chunks (AI-0001..0006)
# that sit in the KB marked is_quotable:true and reach ten chapter buckets. They
# are excluded here: a sourcebook cites what a source says, and nothing in it may
# be model-written text presented as evidence.
SYNTHETIC = {"ai-derived"}

SUBTHEMES = 6          # clusters per chapter
PER_SUBTHEME = 4       # excerpts kept per cluster (6 x 4 = ~24 per chapter)
PER_SOURCE_CAP = 4     # max excerpts one source may supply to one chapter
KEY_FACTS = 18         # key-fact lines per chapter
EXCERPT_CHARS = 480
CORROB_JACCARD = 0.45  # token overlap at which two sources are treated as one claim

# One code per source, defined here and nowhere else. Mnemonic, collision-free;
# a translation and its original are distinct codes because they cannot stand in
# for one another in a quotation.
CODES = {
    "adhikari-2013-un": "ADH",           "bhojdev-hi": "BHJ-H",
    "kumar-2023-betwa": "BET-K",         "suryavanshi-2013-betwa": "BET-S",
    "deva-1969-temples": "DEV",          "ganguly-paramara": "GAN",
    "vidisha-gazetteer-1979": "GAZ-VID", "gupte-1972": "GUP",
    "hardy-2007": "HAR",                 "intach-2022-udaypur": "INT-ARC",
    "intach-geoheritage": "INT-GEO",     "kramrisch-1946-v1": "KRAM-1",
    "kramrisch-1946-v2": "KRAM-2",       "pande-udayesvara": "PAN",
    "parmar-2025-origins": "PAR",        "patil-1952": "PAT-CH",
    "patil-composite-inscriptions": "PAT-INS", "patil-composite-temples": "PAT-TEM",
    "rajpurohit-bhoj-en": "RAJ-E",       "rajamartanda-bhoja": "RAJM",
    "samarangana": "SAM",                "singh-1984-bhoja": "SIN-B",
    "singh-serpentine": "SIN-S",         "singh-temple-economics": "SIN-T",
    "skanda-xiii": "SKP-13",             "tiwari-jhk-en": "TIW-E",
    "tiwari-jhk-hi": "TIW-H",
}

STOP = set("""the a an of in on at to for and or is was were be by with from as that this which what who how
about into its it their his her not but are had has have been would could should may might must one two
three also such other more most than then there here when while them he she we you i s t n d m re ve ll
pp vol fig pl no page chapter part section see also had been which were""".split())


def norm(t):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t or "")).strip()


def write_codes_to_registry():
    """Write `code:` into source_registry.yaml beside each source_id.

    Line-wise on purpose: the registry carries a long explanatory header and
    inline comments that a yaml round-trip would silently delete."""
    lines = REGISTRY.read_text(encoding="utf-8").splitlines()
    out, added, present = [], 0, 0
    for i, line in enumerate(lines):
        out.append(line)
        m = re.match(r"(\s*)- source_id:\s*(\S+)", line)
        if not m:
            continue
        indent, sid = m.group(1) + "  ", m.group(2)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if re.match(r"\s*code:", nxt):
            present += 1
            continue
        code = CODES.get(sid)
        if code:
            out.append(f"{indent}code: {code}")
            added += 1
    REGISTRY.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"source_registry.yaml: {added} codes written, {present} already present")


def load_sources():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    out = {}
    for s in reg["sources"]:
        sid = s["source_id"]
        out[sid] = {
            "code": CODES.get(sid, "??-" + sid[:4].upper()),
            "title": s.get("title", "?"), "author": s.get("author", "?"),
            "language": s.get("language", "?"), "source_type": s.get("source_type", "?"),
            "publication_date": s.get("publication_date", ""),
            "notes": s.get("provenance_notes", "") or "",
        }
    return out, reg.get("excluded", [])


def citation(m, srcs):
    """Code · book · page (only where the KB has one) · chunk id."""
    sid = m.get("parent_source_id", "?")
    s = srcs.get(sid, {"code": "??", "title": m.get("title", "?")})
    page = m.get("page")
    if sid in PAGES_UNRELIABLE:
        trail = (m.get("provenance") or "").split("|")[-1].strip()
        where = f"sec. {trail}" if trail else "sec. —"
    elif page in (None, "", -1, "-1"):
        where = "p. —"
    else:
        where = f"p. {page}"
    return f"**{s['code']}** · *{s['title']}* · {where} · `{m.get('chunk_id','?')}`"


def cluster(rows, k, seed=7):
    V = np.stack([r["_vec"] for r in rows])
    V = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    rng = np.random.default_rng(seed)
    C = V[rng.choice(len(V), size=min(k, len(V)), replace=False)]
    lab = np.zeros(len(V), dtype=int)
    for _ in range(25):
        lab = (V @ C.T).argmax(axis=1)
        for j in range(len(C)):
            sel = V[lab == j]
            if len(sel):
                c = sel.mean(axis=0)
                C[j] = c / max(1e-9, np.linalg.norm(c))
    groups = collections.defaultdict(list)
    for r, l in zip(rows, lab):
        groups[int(l)].append(r)
    return groups


def terms(text):
    return {w for w in re.findall(r"[a-zāīūṛṅñṭḍṇśṣḥṃ]{4,}", text.lower()) if w not in STOP}


def label(rows, df, n_all):
    tf = collections.Counter()
    for r in rows:
        for w in terms(r["text"]):
            tf[w] += 1
    scored = sorted(((t * np.log(n_all / (1 + df.get(w, 0))), w) for w, t in tf.items() if t >= 2),
                    reverse=True)
    return ", ".join(w for _, w in scored[:5]) or "general"


def quality(m, cid):
    """Relevance dominates: primacy orders what already belongs in the chapter.

    Weighted the other way round, a primary source outranks everything on
    primacy alone — the Samarāṅgaṇa's siege-engine chapter surfaced at the top
    of the temple-sculpture sub-theme, which is not evidence for it."""
    return (0.55 * float(m.get(f"rel_{cid}") or 0)
            + 0.20 * float(m.get("score_primacy") or 0)
            + 0.15 * float(m.get("score_claim_credibility") or 0)
            + 0.10 * float(m.get("score_source_reliability") or 0))


# ---------------------------------------------------------------------------
# Key facts: extracted from the chunks, never composed. A fact line is a
# condensed sentence from a cited passage; status is derived mechanically from
# how many distinct sources carry it and whether their numbers agree.
# ---------------------------------------------------------------------------
YEAR = re.compile(r"\b(?:1[0-9]{3}|[89][0-9]{2})\b")
VS_YEAR = re.compile(r"\b(?:V\.?\s?S\.?|sa[mṃ]vat)\s*(\d{3,4})\b", re.I)
SENT = re.compile(r"(?<=[.!?])\s+")
# dots that do not end a sentence; protected before splitting, restored after
ABBREV = re.compile(
    r"\b(?:A\.\s?D|B\.\s?C|A\.\s?H|V\.\s?S|C\.\s?E|Dr|Mr|Mrs|Prof|St|No|Vol|Pl|Fig|\n    pp|ed|eds|cf|viz|e\.g|i\.e|c)\.", re.I)
CITATION_YEAR = re.compile(r"\([^)]{0,48}(?:1[6-9]\d{2}|20\d{2})\s*\)")  # (… 1942)
CAPTION = re.compile(r"^(?:Figure|Fig\.|Plate|Pl\.|Table|Map|Photo|Source:|Annexure)\b"
                     r"|(?:Figure|Plate|Table)\s+\d+\s*[:.]", re.I)
ASIDE = re.compile(r"^(?:only|but|thus|hence|however|therefore|moreover|these|those|it |this )",
                   re.I)


def sentences_of(text):
    """Split on sentence ends, keeping abbreviation dots intact."""
    held = ABBREV.sub(lambda m: m.group(0).replace(".", "\u0001"), text)
    return [s.replace("\u0001", ".").strip() for s in SENT.split(held)]
# publisher imprints, journal runs, report titles: apparatus, not evidence
BIBLIOGRAPHIC = re.compile(
    r"University Press|Oxford|Routledge|Motilal|Banarsidass|Delhi:|London:|New York|"
    r"\bed\.|\beds\.|\btrans\.|\bvols?\.|\bpp\.|Progress Report|Annual Report|"
    r"Journal|Quarterly|Bulletin|ISBN|reprint", re.I)


def fact_candidates(rows, cid):
    """Sentences carrying concrete data: a year, a measurement, or named parties."""
    out = []
    for r in rows:
        for s in sentences_of(norm(r["text"])):
            s = s.strip()
            if not (45 <= len(s) <= 240):
                continue
            years = set(YEAR.findall(s)) | set(VS_YEAR.findall(s))
            caps = len(re.findall(r"\b[A-ZĀĪŪŚṢṆṬḌṄÑ][\w'’-]{2,}", s))
            nums = len(re.findall(r"\b\d[\d,.]*\b", s))
            if not years and caps < 2 and nums < 2:
                continue
            if sum(c.isalpha() for c in s) < len(s) * 0.55:      # tables, OCR noise
                continue
            if BIBLIOGRAPHIC.search(s) or CITATION_YEAR.search(s) or CAPTION.search(s):
                continue                 # reference entry or caption, not a fact
            if ASIDE.match(s) or not s[:1].isupper():
                continue                 # a continuation, not a standalone statement
            if s.rstrip().endswith((" A.", " D.", " C.", " H.", " S.", " p.", " No.")):
                continue                 # truncated on an abbreviation
            if s.count("|") >= 2 or s.count("$") >= 2:
                continue                 # a table row or a formula, not a statement
            spec = min(1.0, 0.25 * len(years) + 0.06 * caps + 0.04 * nums)
            out.append({"text": s, "row": r, "years": years,
                        "score": quality(r, cid) + 0.35 * spec})
    return sorted(out, key=lambda f: -f["score"])


def group_facts(cands, srcs, limit):
    """Cluster near-identical statements so corroboration and conflict show."""
    groups = []
    for f in cands:
        t = terms(f["text"])
        if len(t) < 4:
            continue
        # Two books rarely phrase one fact the same way, so wording overlap alone
        # under-reports corroboration badly. A shared date plus shared rare terms
        # is the signal that they are talking about the same thing.
        hit = None
        for g in groups:
            jac = len(t & g["terms"]) / max(1, len(t | g["terms"]))
            shared_years = bool(f["years"] & g["years"])
            if jac >= 0.5 or (shared_years and len(t & g["terms"]) >= 3):
                hit = g
                break
        if hit is None:
            if len(groups) >= limit * 3:
                continue
            groups.append({"terms": t, "years": set(f["years"]), "members": [f]})
        else:
            hit["members"].append(f)
            hit["terms"] |= t
            hit["years"] |= f["years"]
    out = []
    for g in groups:
        best = g["members"][0]
        codes, yearsets = {}, {}
        for m in g["members"]:
            sid = m["row"].get("parent_source_id")
            code = srcs.get(sid, {}).get("code", "??")
            codes.setdefault(code, m)
            if m["years"]:
                yearsets.setdefault(code, set()).update(m["years"])
        distinct = [v for v in yearsets.values() if v]
        # Disjoint year sets alone are not disagreement: one book may simply
        # mention more dates than another. Only call it contested when each side
        # commits to a small set and those sets exclude one another.
        contested = (len(distinct) > 1 and not set.intersection(*distinct)
                     and all(len(v) <= 2 for v in distinct))
        status = "single-source"
        if (best["row"].get("epistemic_status") or "") == "speculation":
            status = "unverified"
        elif contested:
            status = "contested"
        elif len(codes) > 1:
            status = "established"
        out.append({"text": best["text"], "codes": sorted(codes), "status": status,
                    "score": best["score"], "chunk": best["row"].get("chunk_id", "?"),
                    "years": {c: sorted(v) for c, v in yearsets.items()} if contested else {}})
    return sorted(out, key=lambda g: -g["score"])[:limit]


CURATED = ROOT / "curated_facts.yaml"


def load_curated(dossier_ids):
    """Hand-verified facts the extractor cannot see. Every chunk id must exist,
    or the build stops: a curated fact with a dead citation is worse than none."""
    if not CURATED.exists():
        return {}
    data = yaml.safe_load(CURATED.read_text(encoding="utf-8")) or {}
    by_chapter = collections.defaultdict(list)
    for f in data.get("facts", []):
        ids = list(f.get("supporting_chunks") or []) + list(f.get("chunks") or [])
        for pos in f.get("positions", []):
            ids += list(pos.get("chunks") or [])
        missing = [i for i in ids if i not in dossier_ids]
        if missing:
            raise SystemExit(f"curated fact {f.get('id')!r} cites chunks not in the KB: {missing}")
        for cid in f.get("chapters", []):
            by_chapter[cid].append(f)
    return by_chapter


def main():
    write_codes_to_registry()
    srcs, excluded = load_sources()
    chapters = yaml.safe_load(CHAPTERS.read_text(encoding="utf-8"))["chapters"]
    col = chromadb.PersistentClient(path=str(CHROMA)).get_collection(COLLECTION)
    all_ids = set(col.get(limit=200000, include=[])["ids"])
    known = {i.split("-", 1)[-1] for i in all_ids}
    every_chunk = set()
    for _m in col.get(limit=200000, include=["metadatas"])["metadatas"]:
        every_chunk.add(_m.get("chunk_id"))
    curated = load_curated(every_chunk)
    print(f"curated facts: {sum(len(v) for v in curated.values())} placements")

    # ---------------------------------------------------------------- codes
    cm = ["# Source codes — the code of record", "",
          "Every citation in `BOOK_SOURCEBOOK.md` uses a code from this table, and codes are "
          "defined here and nowhere else. One code per source; no code covers two sources. A "
          "translation and its original carry different codes, because they cannot substitute for "
          "one another in a quotation.", "",
          "| code | book | author | lang | source type | source_id (KB) | notes |",
          "|---|---|---|---|---|---|---|"]
    for sid, s in sorted(srcs.items(), key=lambda kv: kv[1]["code"]):
        note = norm(s["notes"])[:110].replace("|", "/")
        if sid in PAGES_UNRELIABLE:
            note = "**cite by section, never page — page numbers in this source are unreliable.** " + note
        cm.append(f"| `{s['code']}` | {s['title']} | {s['author']} | {s['language']} | "
                  f"{s['source_type']} | `{sid}` | {note} |")
    cm += ["", f"{len(srcs)} sources carry codes.", ""]
    if excluded:
        cm += ["## Known to exist, not in the corpus", ""]
        for e in excluded:
            cm.append(f"- **{e.get('file','?')}** — {norm(e.get('reason',''))}")
        cm.append("")
    (ROOT / "source_codes.md").write_text("\n".join(cm), encoding="utf-8")
    print("wrote source_codes.md —", len(srcs), "codes")

    # ------------------------------------------------------------ sourcebook
    doc = ["# The Udaypur book — sourcebook", "",
           "Chapter by chapter, the evidence the knowledge base holds, grouped by sub-theme and "
           "cited in full. It gathers and cites; it contains no chapter prose.", "",
           "**How to use this.** Every excerpt carries its source code, book, page and KB chunk id, "
           "so any line can be checked without searching the corpus. Codes resolve in the table "
           "below and in `source_codes.md`. Quotations are gated: a chunk the KB marks "
           "`is_quotable: false` — AI-reworded or OCR-damaged text — never appears as a quotation, "
           "only as a marked paraphrase. Page numbers appear only where the KB actually holds one; "
           "otherwise `p. —`, and for the Samarāṅgaṇa-sūtradhāra a section trail, because its page "
           "numbers are known to be corrupt. Nothing here is invented, and thin coverage is "
           "flagged rather than filled.", "",
           "**Excluded by design.** The knowledge base contains six model-written synthesis chunks "
           "under the source id `ai-derived` (`AI-0001`–`AI-0006`), bucketed into ten chapters. They "
           "are not a source and do not appear anywhere below. They shipped marked quotable; they "
           "were re-flagged `is_quotable: false` and archived on 2026-09-29, their chapter buckets "
           "cleared, and `build_chroma.py` now archives and un-buckets anything tagged `ai_derived` "
           "so a rebuild cannot restore them.", "",
           f"**Selection.** Each chapter's bucket is clustered into {SUBTHEMES} sub-themes on the "
           f"KB's own embeddings; the top {PER_SUBTHEME} excerpts per sub-theme are kept, ranked by "
           "primacy, then claim credibility, then source reliability, then relevance to that "
           "chapter. Excerpts are trimmed to about "
           f"{EXCERPT_CHARS} characters, marked `…` where trimmed. No source may supply more than "
           f"{PER_SOURCE_CAP} excerpts to one chapter, so a large book cannot crowd out the rest "
           "of the shelf.", "",
           "## Source codes", "",
           "| code | book | author | source type |", "|---|---|---|---|"]
    for sid, s in sorted(srcs.items(), key=lambda kv: kv[1]["code"]):
        doc.append(f"| `{s['code']}` | {s['title']} | {s['author']} | {s['source_type']} |")
    doc.append("")

    matrix = {}          # code -> {cid: n}
    at_glance = []       # (cid, title, chunks, sources, facts, excerpts, flag)
    sidecar = {}         # cid -> machine-readable facts, gaps, coverage
    stat_counts = collections.Counter()
    fact_total = [0]
    totals = collections.Counter()
    gate_blocked = 0
    excerpt_count = 0
    thin = []

    for ch in chapters:
        cid, title = ch["id"], ch.get("title", "")
        got = col.get(where={f"in_{cid}": True}, limit=50000,
                      include=["metadatas", "documents", "embeddings"])
        rows = []
        for m, d, e in zip(got["metadatas"], got["documents"], got["embeddings"]):
            m = dict(m)
            if m.get("is_archived") or m.get("parent_source_id") in SYNTHETIC:
                continue
            m["text"] = d
            m["_vec"] = np.asarray(e, dtype=np.float32)
            rows.append(m)
        if not rows:
            doc += [f"## {cid} — {title}", "", "_No chunks are bucketed to this chapter._", ""]
            continue

        by_src = collections.Counter(r["parent_source_id"] for r in rows)
        by_type = collections.Counter(r.get("source_type", "?") for r in rows)
        n_src = len(by_src)
        top_src, top_n = by_src.most_common(1)[0]
        share = top_n / len(rows)

        df = collections.Counter()
        for r in rows:
            for w in terms(r["text"]):
                df[w] += 1
        groups = cluster(rows, SUBTHEMES)

        facts_before, exc_before = fact_total[0], excerpt_count
        doc += [f"## {cid} — {title}", "",
                "[↑ contents](#contents)", ""]
        codes_here = sorted({srcs.get(s, {}).get("code", "??") for s in by_src})
        summary = (f"**Coverage.** {len(rows):,} chunks from {n_src} sources "
                   f"({', '.join('`' + c + '`' for c in codes_here)}). Source-type mix: "
                   + ", ".join(f"{k} {v}" for k, v in by_type.most_common()) + ". "
                   f"The largest single contributor is `{srcs.get(top_src,{}).get('code','??')}` "
                   f"with {top_n:,} chunks ({share:.0%} of the bucket).")
        if share > 0.45:
            summary += (" **Single-source risk:** more than 45% of this chapter's evidence comes "
                        "from one book; corroborate before asserting.")
            thin.append((cid, srcs.get(top_src, {}).get("code", "??"), f"{share:.0%}"))
        doc += [summary, ""]

        # --- key facts ---------------------------------------------------
        facts = group_facts(fact_candidates(rows, cid), srcs, KEY_FACTS)
        doc += ["**Key facts the KB establishes.** Each line is condensed from the cited passage, "
                "not composed; the status is derived from how many distinct sources carry it and "
                "whether their figures agree. `[single-source]` means no second source was matched "
                "by that test, which is deliberately conservative — it under-reports "
                "corroboration rather than claiming it. Read it as \"attribute, do not assert\", "
                "not as proof that no other book says this.", ""]
        for cf in curated.get(cid, []):
            if cf["status"] == "contested":
                vals = "; ".join(f"**{pos['value']}** (`{pos['code']}`)" for pos in cf["positions"])
                doc.append(f"- {norm(cf['text'])} — competing values: {vals} "
                           f"`[contested]` `[curated]`")
                if cf.get("note"):
                    doc.append(f"  - {norm(cf['note'])}")
            else:
                codes = " · ".join(f"`{c}`" for c in sorted(
                    {srcs.get(x, {}).get('code', '??') for x in cf.get('chunks', [])}))
                doc.append(f"- {norm(cf['text'])} — {codes} `[{cf['status']}]` `[curated]`")
            ids = list(cf.get("supporting_chunks") or [])
            for pos in cf.get("positions", []):
                ids += list(pos.get("chunks") or [])
            if ids:
                doc.append("  - traceable to: " + ", ".join(f"`{i}`" for i in ids))
            sidecar.setdefault(cid, {"facts": []})["facts"].append({
                "text": norm(cf["text"]), "status": cf["status"], "curated": True,
                "codes": sorted({pos["code"] for pos in cf.get("positions", [])}) or
                         sorted({srcs.get(x, {}).get("code", "??") for x in cf.get("chunks", [])}),
                "positions": [{"value": q["value"], "code": q["code"]} for q in cf.get("positions", [])],
                "note": norm(cf.get("note") or ""),
                "chunks": list(cf.get("supporting_chunks") or [])
                          + [c for q in cf.get("positions", []) for c in q.get("chunks", [])],
            })
            stat_counts[cf["status"]] += 1
            stat_counts["curated"] += 1
            fact_total[0] += 1

        for fct in facts:
            codes = " · ".join(f"`{c}`" for c in fct["codes"])
            tag = f"`[{fct['status']}]`"
            extra = ""
            if fct["years"]:
                extra = " — figures differ: " + "; ".join(
                    f"`{c}` {', '.join(v)}" for c, v in sorted(fct["years"].items()))
            doc.append(f"- {fct['text']} — {codes} {tag}{extra}")
            sidecar.setdefault(cid, {"facts": []})["facts"].append({
                "text": fct["text"], "status": fct["status"], "curated": False,
                "codes": fct["codes"], "positions": [], "note": "",
                "chunks": [fct["chunk"]],
            })
            stat_counts[fct["status"]] += 1
            fact_total[0] += 1
        thin_codes = sorted(srcs.get(s, {}).get("code", "??") for s, n in by_src.items() if n <= 3)
        if thin_codes:
            doc.append(f"- Barely represented in this bucket, so anything resting on them is a "
                       f"thin reed: {', '.join('`' + c + '`' for c in thin_codes[:10])} — `[gap]`")
            stat_counts["gap"] += 1
            fact_total[0] += 1
        doc.append("")

        seen_texts = []          # (set(terms), index in doc-entry list) for corroboration merge
        entries = []
        used = collections.Counter()   # per-source cap, chapter-wide
        for gi in sorted(groups, key=lambda g: -len(groups[g])):
            grp = []
            for r in sorted(groups[gi], key=lambda r: -quality(r, cid)):
                sid = r.get("parent_source_id")
                if used[sid] >= PER_SOURCE_CAP:    # one big book must not crowd out the rest
                    continue
                grp.append(r)
                used[sid] += 1
                if len(grp) >= PER_SUBTHEME:
                    break
            if not grp:
                continue
            doc += [f"### {cid}.{gi + 1} — {label(groups[gi], df, len(rows))}", ""]
            for r in grp:
                body = norm(r["text"])
                trimmed = len(body) > EXCERPT_CHARS
                body = body[:EXCERPT_CHARS] + ("…" if trimmed else "")
                tset = terms(body)
                merged = None
                for prev_t, prev_i in seen_texts:
                    if prev_t and tset and len(tset & prev_t) / max(1, len(tset | prev_t)) >= CORROB_JACCARD:
                        merged = prev_i
                        break
                cite = citation(r, srcs)
                code = srcs.get(r["parent_source_id"], {}).get("code", "??")
                matrix.setdefault(code, collections.Counter())[cid] += 1
                totals[code] += 1
                if merged is not None and entries[merged][1] != code:
                    doc[entries[merged][0]] += f" · also **{code}** · `{r.get('chunk_id','?')}`"
                    continue
                if r.get("is_quotable"):
                    doc.append(f"> {body}")
                else:
                    gate_blocked += 1
                    doc.append(f"> [paraphrase — not a verbatim quote; source text unreliable] {body}")
                doc.append(f"> — {cite}")
                doc.append("")
                entries.append((len(doc) - 2, code))
                seen_texts.append((tset, len(entries) - 1))
                excerpt_count += 1

        gaps = []
        if n_src < 20:
            gaps.append(f"only {n_src} of {len(srcs)} sources reach this chapter")
        singles = [srcs.get(s, {}).get("code", "??") for s, n in by_src.items() if n <= 3]
        if singles:
            gaps.append("barely represented here: " + ", ".join("`" + c + "`" for c in sorted(singles)[:12]))
        if share > 0.45:
            gaps.append("the chapter leans on one book for nearly half its evidence")
        at_glance.append((cid, title, len(rows), n_src,
                          fact_total[0] - facts_before, excerpt_count - exc_before,
                          "leans on one book" if share > 0.45 else
                          ("few sources" if n_src < 24 else "")))
        rec = sidecar.setdefault(cid, {"facts": []})
        rec["title"] = title
        rec["chunks"] = len(rows)
        rec["sources"] = sorted(srcs.get(s, {}).get("code", "??") for s in by_src)
        rec["dominant"] = {"code": srcs.get(top_src, {}).get("code", "??"),
                           "share": round(share, 3)}
        rec["gaps"] = gaps
        rec["thin_codes"] = thin_codes
        doc += ["**Gaps.** " + ("; ".join(gaps) if gaps else
                                "no structural gap detected: the bucket is broad and no single "
                                "source dominates.") + ".", ""]
        print(f"{cid}: {len(rows):5d} chunks, {n_src:2d} sources -> excerpts so far {excerpt_count}")

    # -------------------------------------------------------- coverage matrix
    doc += ["## Coverage matrix — sources × chapters", "",
            "Excerpts selected per chapter, by source code. A blank cell means the source "
            "contributed no selected excerpt to that chapter; it does not always mean the source "
            "is absent from the bucket.", ""]
    cids = [c["id"] for c in chapters]
    doc.append("| code | " + " | ".join(cids) + " | total |")
    doc.append("|---" * (len(cids) + 2) + "|")
    for code in sorted(matrix, key=lambda c: -totals[c]):
        cells = [str(matrix[code].get(c, "") or "") for c in cids]
        doc.append(f"| `{code}` | " + " | ".join(cells) + f" | {totals[code]} |")
    doc += ["", f"{excerpt_count} excerpts and {fact_total[0]} key-fact lines in total; "
                f"{gate_blocked} entries were blocked from quotation by the quotability gate and "
                "appear as marked paraphrase.", "",
                "Key-fact status tally: "
                + ", ".join(f"`[{k}]` {v}" for k, v in stat_counts.most_common()) + ".", ""]
    if thin:
        doc += ["**Chapters resting heavily on one source:** "
                + "; ".join(f"{c} (`{code}`, {pct})" for c, code, pct in thin) + ".", ""]

    nav = ["## Contents", "",
           "| § | chapter | chunks | sources | key facts | excerpts | watch |",
           "|---|---|--:|--:|--:|--:|---|"]
    for cid, title, nchunks, nsrc, nf, nx, flag in at_glance:
        heading = f"{cid} — {title}".lower()
        slug = "".join(ch for ch in heading if ch.isalnum() or ch in " -").replace(" ", "-")
        nav.append(f"| [{cid}](#{slug}) | {title} | {nchunks:,} | {nsrc} | {nf} | {nx} | {flag} |")
    nav += ["", "[Source codes](#source-codes) · [Coverage matrix](#coverage-matrix--sources--chapters)", ""]

    marker = "## Source codes"
    i = doc.index(marker)
    doc[i:i] = nav
    doc.insert(i, '<a id="contents"></a>')
    (ROOT / "kb3" / "sourcebook_facts.json").write_text(
        json.dumps({"generated": NOW_STR, "codes": {sid: v["code"] for sid, v in srcs.items()},
                    "chapters": sidecar}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote kb3/sourcebook_facts.json —",
          sum(len(v.get("facts", [])) for v in sidecar.values()), "facts")
    (ROOT / "BOOK_SOURCEBOOK.md").write_text("\n".join(doc), encoding="utf-8")
    print(f"\nwrote BOOK_SOURCEBOOK.md — {excerpt_count} excerpts, {gate_blocked} gated")


if __name__ == "__main__":
    main()
