#!/usr/bin/env python
"""Chapter-writing pipeline: KB → dossier → outline → sections → QA → handoff.

    python chapter_pipeline.py status
    python chapter_pipeline.py retrieve C7          # stage 1  → research.md
    python chapter_pipeline.py outline  C7          # stage 2  → outline.md   (GATE)
    python chapter_pipeline.py approve  C7 outline  # human says the outline is sound
    python chapter_pipeline.py brief    C7 2        # stage 3  → drafting brief for section 2
    python chapter_pipeline.py assemble C7          # stage 3b → draft-vN.md from sections/
    python chapter_pipeline.py verify   C7          # stage 4  → qa_review.md
    python chapter_pipeline.py approve  C7 draft    # human says the draft is sound  (GATE)
    python chapter_pipeline.py handoff  C7          # stage 5  → handoff/

One chapter is one folder under chapters/<id>/, every stage leaves a file, and
state.json records where the chapter stands, so a run can stop and resume.

WHAT IS DETERMINISTIC AND WHAT IS NOT
  Retrieval, dossier assembly, gap analysis, verification and packaging are
  local and deterministic: no model is involved and the result is reproducible.
  The prose of a section is written by whatever model the team uses, from the
  brief this pipeline emits (`brief`), and handed back as sections/NN.md. The
  guarantees therefore hold whoever writes: `verify` re-checks every marker,
  quotation and epistemic label against the KB itself.

THE RULES VERIFY ENFORCES (see STYLE_GUIDE.md)
  * every factual-looking sentence carries [src: chunk_id], or [ed] if it is the
    author's own framing and asserts no fact from the KB
  * every id resolves to a chunk in THIS chapter's dossier
  * a quoted span of >= 6 words must appear verbatim in a cited chunk that is
    is_quotable — AI-reworded and OCR needs_recheck text may lead, never be quoted
  * a sentence citing an `inference` or `speculation` chunk must attribute or hedge
  * word count within the style guide's range; text NFC; no mojibake
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "chapters"
CHROMA = ROOT / "kb3" / "chroma"
# Resolved through kb_target so a cutover is one pointer, not an edit in every
# module. The archive collection is never opened here.
from kb_target import collection as _kb_collection, sqlite_path as _kb_sqlite  # noqa: E402
COLLECTION = _kb_collection()
WORDS_MIN, WORDS_MAX = 4000, 5200      # chapter budget raised to ~5,000 words (C1, 2026-09-28)
NOW = lambda: dt.datetime.now().isoformat(timespec="seconds")

HEDGE = re.compile(
    r"\b(suggests?|appears?|seems?|points? to|may|might|probably|likely|perhaps|arguably|"
    r"infers?|inferred|reads? (?:the|this)|argues?|proposes?|conjectur\w+|would have|"
    r"is thought|ha(?:s|ve) been read|interprets?|takes? it|supposes?|surmises?|surmise|posits?|"
    r"would be|is offered as)\b", re.I)
ATTRIB = re.compile(
    r"\b(according to|[Ii]n [A-Z]\w+'s (?:view|reading|account|analysis)|[A-Z][\w.-]+ (?:argues|suggests|reads|proposes|"
    r"infers|holds|reports|records|notes|dates|calls|treats|describes|identifies|thinks)|"
    r"scholars?|historians?)\b")
FACTUAL_HINT = re.compile(
    r"\b\d{3,4}\b|\bsaṃvat\b|\bsamvat\b|\bCE\b|\bBCE\b|century|inscription|records?|measured|"
    r"survey|built|founded|carved|temple|king|dynasty|records", re.I)
SRC = re.compile(r"\[src:\s*([^\]]+)\]")
ABBREV = re.compile(r"\b(?:V\.\s?S|A\.\s?H|A\.\s?D|C\.\s?E|B\.\s?C|Dr|Mr|Mrs|Prof|St|etc|e\.g|i\.e|cf|Fig|No|pp|Vol)\.", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{25,})[\"”]")


def fold(t):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip().lower()


def chapters_cfg():
    return yaml.safe_load(open(ROOT / "kb3" / "chapters.yaml", encoding="utf-8"))


def chapter_profile(cid):
    for c in chapters_cfg()["chapters"]:
        if c["id"] == cid:
            return c
    raise SystemExit(f"unknown chapter {cid}")


def folder(cid):
    p = BOOK / cid
    (p / "sections").mkdir(parents=True, exist_ok=True)
    (p / "handoff").mkdir(parents=True, exist_ok=True)
    return p


# --------------------------------------------------------------------------
# House standard for transliteration, script and era (STYLE_GUIDE.md §10).
# A term that takes diacritics takes them everywhere; anglicised geography
# takes them nowhere; no bare Devanagari in running prose; one era form.
# --------------------------------------------------------------------------
IAST_TERMS = {                        # correct form -> spellings that must not appear
    "bhūmija": r"\bbhumija\b", "śikhara": r"\bs[hi]?ikhara\b", "garbhagṛha": r"\bgarbhagriha\b",
    "sabhāmaṇḍapa": r"\bsabhamandapa\b", "praśasti": r"\bpra[sš]asti\b", "liṅga": r"\blinga\b",
    "Udayeśvara": r"\bUdaye[sš]h?vara\b", "Nīlakaṇṭheśvara": r"\bN[ei]+lkanthe[sš]h?[vw]ara?\b",
    "Udayāditya": r"\bUdayaditya\b", "Vetravatī": r"\bVetravati\b", "Daśārṇa": r"\bDasarna\b",
    "Paramāra": r"\bParamara\b|\bParmar\b", "Jayasiṃha": r"\bJayasimha\b",
}
PLAIN_GEO = ["Mālava", "Dhārā", "Vidishā", "Bhopāl", "Betwā", "Udaypūr"]
DEVANAGARI = re.compile(r"[ऀ-ॿ]+")
ERA_BAD = re.compile(r"\bsa[ṃm]vat\b|\bSam\.?\s+\d{3,4}\b", re.I)
ERA_VS = re.compile(r"\bV\.\s?S\.\s?(\d{3,4})")


def translit_findings(body):
    """The three defects a reviewer should never have to catch by hand."""
    out = []
    prose = re.sub(r"`[^`]*`", "", re.sub(r"^>.*$", "", body, flags=re.M))   # code spans, block quotes
    for m in DEVANAGARI.finditer(prose):
        out.append(("script", f"Devanagari in running prose: “{m.group()}” — transliterate, or move "
                              "it into a set-off quotation or the glossary"))
    for m in ERA_BAD.finditer(prose):
        out.append(("era-form", f"“{m.group()}” — the house form is V.S. 1116 (1059 CE)"))
    for para in prose.split("\n\n"):                    # CE pairing on first V.S. of a passage
        m = ERA_VS.search(para)
        if m and "CE" not in para[m.end():m.end() + 30]:
            out.append(("era-form", f"V.S. {m.group(1)} is the first Vikrama year in its paragraph "
                                    "and is not paired with its CE equivalent"))
    for right, wrong in IAST_TERMS.items():
        if right in prose and re.search(wrong, prose):
            out.append(("transliteration", f"“{right}” and a bare spelling of it both appear — "
                                           "a term takes diacritics everywhere or nowhere"))
    for g in PLAIN_GEO:
        if g in prose:
            out.append(("transliteration", f"“{g}” — anglicised geographic names go bare "
                                           "(Malwa, Dhar, Vidisha, Bhopal, Betwa, Udaypur)"))
    return out


SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
GROUP = re.compile(r"[ \t]*\[src:[^\]]*\](?:[ \t]*,[ \t]*\[src:[^\]]*\])*")
UNVER = re.compile(r"[ \t]*`?\[UNVERIFIED[^\]]*\]`?")


def reading_and_notes(text, dossier):
    """Split the marked draft into reader-facing prose plus numbered endnotes.

    A note number tracks a DISTINCT SOURCE, not a sentence: consecutive markers
    resting on the same work collapse into one note placed at the end of the run,
    so four sentences out of one book carry one number rather than four. A single
    note may carry several works, which is the first place corroboration becomes
    visible to a reader — the inline markers never showed it."""
    body = re.sub(r"[ \t]*\[ed\]", "", text)

    def work_of(i):
        r = dossier.get(i, {})
        return r.get("parent_source_id") or f"{r.get('author', '?')}|{r.get('title', '?')}"

    spans = []                                    # (start, end, kind, ids)
    for m in GROUP.finditer(body):
        ids = []
        for one in re.findall(r"\[src:\s*([^\]]+)\]", m.group(0)):
            ids += [i.strip() for i in re.split(r"[,;]", one) if i.strip()]
        spans.append([m.start(), m.end(), "src", ids])
    flag_text = {}
    for m in UNVER.finditer(body):
        spans.append([m.start(), m.end(), "unverified", []])
        # the note must identify the FLAGGED claim, not the sourced sentence before it
        flag_text[m.start()] = re.sub(r"\s+", " ", m.group(0)).strip(" `").lstrip("[").rstrip("]")
    spans.sort(key=lambda s: s[0])

    # One note per work per paragraph: a paragraph resting on one book carries one
    # number, wherever in it the markers fall, and the number sits at the last of
    # them. Numbering happens afterwards, by anchor position, so the sequence a
    # reader meets still ascends.
    runs, seen = [], {}
    for s in spans:
        para = body.count("\n\n", 0, s[0])
        works = frozenset(work_of(i) for i in s[3])
        key = (para, works) if s[2] == "src" else ("unverified", s[0])
        if key in seen:
            r = seen[key]
            r["ids"] += [i for i in s[3] if i not in r["ids"]]
            r["spans"].append(s)
            r["anchor"] = s
            continue
        seen[key] = {"kind": s[2], "para": para, "works": works, "ids": list(s[3]),
                     "spans": [s], "anchor": s, "at": s[0]}
        runs.append(seen[key])
    runs.sort(key=lambda r: r["anchor"][0])

    def phrase(pos):                               # a short identifying phrase for the note
        head = body.rfind(". ", 0, pos)
        head = max(head + 2, body.rfind("\n", 0, pos) + 1)
        t = re.sub(r"\s+", " ", GROUP.sub("", UNVER.sub("", body[head:pos]))).strip(" ,;:—-")
        return (t[:88].rstrip() + "…") if len(t) > 90 else (t or "—")

    anchored = {}                                  # span start -> note number
    for n, r in enumerate(runs, 1):
        r["n"] = n
        r["phrase"] = (flag_text[r["spans"][0][0]] if r["kind"] == "unverified"
                       else phrase(r["spans"][0][0]))
        anchored[r["anchor"][0]] = n
    notes = runs

    out, cut = [], 0                               # walk every span in position order
    for s in sorted(spans, key=lambda s: s[0]):
        out.append(body[cut:s[0]])
        cut = s[1]
        if s[0] in anchored:
            nxt = body[cut:cut + 1]                # the number follows the punctuation
            if nxt in ".,;:!?":
                out.append(nxt)
                cut += 1
            out.append(str(anchored[s[0]]).translate(SUP))
    out.append(body[cut:])
    clean = "".join(out)
    clean = re.sub(r"[ \t]{2,}", " ", clean)
    clean = re.sub(r"[ \t]+([.,;:])", r"\1", clean)
    return clean, notes


def drafts_of(f):
    """Drafts newest last. Sorted by version NUMBER, not by name: plain sorting
    puts draft-v9 after draft-v10 and silently ships the wrong draft."""
    return sorted(f.glob("draft-v*.md"),
                  key=lambda p: int(re.search(r"draft-v(\d+)", p.name).group(1)))


def state(cid, **update):
    f = folder(cid) / "state.json"
    s = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"chapter": cid, "stages": {}, "log": []}
    if update:
        for k, v in update.items():
            if k == "stage":
                s["stages"][v] = NOW()
            else:
                s[k] = v
        s["log"].append({"at": NOW(), **update})
        f.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    return s


SOURCEBOOK = ROOT / "kb3" / "sourcebook_facts.json"

# How a sourcebook status must read on the page. The drafting brief prints this
# and `verify` enforces the two that can be got wrong without anyone noticing.
STATUS_RULE = {
    "established": "assert it plainly; it is carried by more than one source",
    "single-source": "attribute it, do not assert it as settled — name the evidence, not the book",
    "contested": "show the disagreement: give the competing values, never just the one you prefer",
    "unverified": "keep the `[UNVERIFIED — …]` flag; it may never harden into an asserted fact",
    "gap": "do not fill it — write `[GAP: what is missing]` or leave the claim out",
}


def load_sourcebook(cid=None):
    """Facts, gaps and source codes from the sourcebook build, or {} if absent."""
    if not SOURCEBOOK.exists():
        return {}
    d = json.loads(SOURCEBOOK.read_text(encoding="utf-8"))
    if cid is None:
        return d
    ch = dict(d.get("chapters", {}).get(cid, {}))
    ch["codes"] = d.get("codes", {})
    ch["generated"] = d.get("generated", "")
    return ch


def load_bucket(cid):
    """Every active chunk bucketed into this chapter, with its vector."""
    import chromadb
    col = chromadb.PersistentClient(path=str(CHROMA)).get_collection(COLLECTION)
    got = col.get(where={"$and": [{f"in_{cid}": True}, {"is_archived": False}]}, limit=50000,
                  include=["metadatas", "documents", "embeddings"])
    rows = []
    for m, d, e in zip(got["metadatas"], got["documents"], got["embeddings"]):
        m = dict(m)
        if m.get("is_archived"):        # belt and braces: the flag is authoritative
            continue
        m["text"] = d
        m["_vec"] = np.asarray(e, dtype=np.float32)
        rows.append(m)
    return rows


# --------------------------------------------------------------------------
# Stage 1 — retrieve
# --------------------------------------------------------------------------
STOP = set("""the a an of in on at to for and or is was were be by with from as that this which what who how
about into its it their his her not but are were had has have been would could should may might must
one two three also such other more most than then there here when where while who whom whose they them
he she we you i s t n d m re ve ll of- -- p pp vol fig pl no""".split())


def cluster(rows, k=8, seed=7):
    """k-means over the KB's own vectors: sub-themes come from the evidence,
    not from a guess about what the chapter should contain."""
    V = np.stack([r["_vec"] for r in rows])
    V = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    rng = np.random.default_rng(seed)
    C = V[rng.choice(len(V), size=min(k, len(V)), replace=False)]
    for _ in range(25):
        lab = (V @ C.T).argmax(axis=1)
        for j in range(len(C)):
            sel = V[lab == j]
            if len(sel):
                C[j] = sel.mean(axis=0) / max(1e-9, np.linalg.norm(sel.mean(axis=0)))
    groups = collections.defaultdict(list)
    for r, l in zip(rows, lab):
        groups[int(l)].append(r)
    return groups


def label_group(rows, all_df, n_all):
    """Name a sub-theme by the terms that distinguish it from the chapter."""
    tf = collections.Counter()
    for r in rows:
        for w in set(re.findall(r"[\wऀ-ॿ]{4,}", fold(r["text"]))):
            if w not in STOP and not w.isdigit():
                tf[w] += 1
    scored = [(t * np.log(n_all / (1 + all_df.get(w, 0))), w) for w, t in tf.items() if t >= 2]
    scored.sort(reverse=True)
    return ", ".join(w for _, w in scored[:6]) or "misc"


# Sources whose page numbers cannot be trusted: a single stray "Page N" line in
# the markdown propagated to every later chunk (samarangana: 1,499 chunks, 7
# distinct pages). Citing those pages would send an editor to nothing.
PAGES_UNRELIABLE = set(json.loads((ROOT / "kb3" / "pages_unreliable.json").read_text())
                       if (ROOT / "kb3" / "pages_unreliable.json").exists() else [])


def page_of(r):
    if r["parent_source_id"] in PAGES_UNRELIABLE:
        return "—(no reliable page)"
    return r["page"] or "—"


def quality(r):
    """Relevance to THIS chapter leads; the other scores order what already belongs.

    Weighted the other way round — credibility 0.35, primacy 0.25, relevance 0.2 —
    retrieval for C2 (the Betwa valley: land, rivers, seasons) put 14 chunks of the
    Samarāṅgaṇa-sūtradhāra in the dossier at mean rel_C2 0.39, and only 4 each of
    the two Betwa hydrology and climate papers at rel_C2 0.82 and 0.72. A primary
    architectural treatise outranked the river science in a chapter about the river,
    because primacy is a property of the book and relevance is the only score that
    knows what the chapter is about."""
    q = (0.45 * r.get(f"rel_{r['_cid']}", 0) + 0.25 * r["score_claim_credibility"]
         + 0.20 * r["score_source_reliability"] + 0.10 * r["score_primacy"])
    # a chapter about this temple wants evidence about this temple first
    return q * (1.25 if r.get("tag_udaypur_specific") else 1.0)


def cmd_retrieve(cid, k=8, per_group=14, rel_floor=0.0):
    prof = chapter_profile(cid)
    rows = load_bucket(cid)
    if not rows:
        raise SystemExit(f"no chunks bucketed into {cid}")
    for r in rows:
        r["_cid"] = cid

    # A relevance floor drops weakly-related chunks BEFORE clustering, because the
    # sub-themes form from whatever the bucket holds: a bucket that is 43% a
    # treatise on architecture gives a chapter on rivers eight architectural
    # sub-themes. C2 unfiltered is mean rel 0.43, themes
    # "having / lord / deserves / cite"; at 0.55 it is 0.75 and
    # "streamflow / trend / rainfall".
    #
    # It is OFF by default and should stay off by default. Relevance and
    # citation-worthiness are only loosely correlated: 38 of the 47 chunks the
    # finished C1 actually cites — the porch inscriptions, Tiwari's lane, the
    # census returns — score below 0.5 on rel_C1, so a silent floor would have
    # denied that chapter most of its evidence. Diagnose first; pass --rel-floor
    # only when the bucket is genuinely polluted.
    before = len(rows)
    kept = [r for r in rows if float(r.get(f"rel_{cid}") or 0) >= rel_floor]
    if len(kept) < max(2 * per_group, 60):
        print(f"  rel-floor {rel_floor} would leave only {len(kept)} chunks — ignoring it")
    else:
        rows = kept
    dropped = before - len(rows)

    _rels = sorted(float(r.get(f"rel_{cid}") or 0) for r in rows)
    median_rel = _rels[len(_rels) // 2]
    _by_work = collections.Counter(r["parent_source_id"] for r in rows)
    top_work, top_n = _by_work.most_common(1)[0]
    _top = [float(r.get(f"rel_{cid}") or 0) for r in rows if r["parent_source_id"] == top_work]
    top_mean = sum(_top) / len(_top)
    advice = ""
    if not rel_floor and top_n / len(rows) > 0.25 and top_mean < median_rel + 0.05:
        advice = (f"  NOTE {top_work} supplies {top_n / len(rows):.0%} of this bucket at mean "
                  f"relevance {top_mean:.2f}, against a bucket median of {median_rel:.2f}; the "
                  f"sub-themes will form around it.\n"
                  f"       consider: retrieve {cid} --rel-floor {median_rel + 0.15:.2f}")

    df = collections.Counter()
    for r in rows:
        for w in set(re.findall(r"[\wऀ-ॿ]{4,}", fold(r["text"]))):
            df[w] += 1
    groups = cluster(rows, k=k)

    dossier, L = {}, []
    L += [f"# Evidence dossier — {cid} {prof['title']}", "",
          (f"Relevance floor {rel_floor}: {dropped:,} of {before:,} bucketed chunks were "
           f"set aside as too weakly related to this chapter before sub-themes were formed."
           if dropped else "No relevance floor applied."), "",
          f"Generated {NOW()} by `chapter_pipeline.py retrieve {cid}` from the Chroma collection "
          f"`{COLLECTION}` (`where in_{cid} = true`, archive excluded).", "",
          f"**{len(rows):,} chunks** are bucketed into this chapter. Below they are grouped into "
          f"sub-themes by clustering the KB's own vectors, and within each sub-theme ranked by "
          f"claim credibility, primacy, source reliability and chapter relevance.", "",
          "Read the coverage note at the end before outlining: it says what this chapter can and "
          "cannot be written from.", ""]

    spine = sorted([r for r in rows if r.get("tag_udaypur_specific")], key=quality, reverse=True)
    if spine:
        L += ["## Spine: evidence that names this town, temple or king", "",
              f"{len(spine)} of the {len(rows):,} bucketed chunks are Udaypur-specific. The chapter's "
              "argument should rest on these; the rest supply canon, comparison and context.", "",
              "| chunk_id | source | type | status | page | corrob. | quotable | text |",
              "|---|---|---|---|---|--:|---|---|"]
        seen_src = collections.Counter()
        for r in spine:
            if seen_src[r["parent_source_id"]] >= 6 or seen_src.total() >= 30:
                continue
            seen_src[r["parent_source_id"]] += 1
            dossier[r["chunk_id"]] = r
            txt = re.sub(r"\s+", " ", r["text"])[:260].replace("|", "/")
            L.append(f"| `{r['chunk_id']}` | {r['parent_source_id']} | {r['source_type']} | "
                     f"{r['epistemic_status']} | {page_of(r)} | {r['corroboration_count']} | "
                     f"{'yes' if r['is_quotable'] else '**no**'} | {txt} |")
        L.append("")

    order = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    for gi, (_, grp) in enumerate(order, 1):
        grp.sort(key=quality, reverse=True)
        name = label_group(grp, df, len(rows))
        L += [f"## Sub-theme {gi}: {name}", "",
              f"{len(grp)} chunks · sources: " +
              ", ".join(f"{s} ({n})" for s, n in collections.Counter(r["parent_source_id"] for r in grp).most_common(5)), "",
              "| chunk_id | source | type | status | page | corrob. | quotable | text |",
              "|---|---|---|---|---|--:|---|---|"]
        seen_src = collections.Counter()
        picked = []
        for r in grp:                       # cap any one book at 4 rows per sub-theme
            if seen_src[r["parent_source_id"]] >= 4:
                continue
            seen_src[r["parent_source_id"]] += 1
            picked.append(r)
            if len(picked) >= per_group:
                break
        for r in picked:
            dossier[r["chunk_id"]] = r
            txt = re.sub(r"\s+", " ", r["text"])[:260].replace("|", "/")
            L.append(f"| `{r['chunk_id']}` | {r['parent_source_id']} | {r['source_type']} | "
                     f"{r['epistemic_status']} | {page_of(r)} | {r['corroboration_count']} | "
                     f"{'yes' if r['is_quotable'] else '**no**'} | {txt} |")
        L.append("")

    # ---- coverage note
    st = collections.Counter(r["epistemic_status"] for r in rows)
    ty = collections.Counter(r["source_type"] for r in rows)
    works = collections.Counter(r["work_id"] for r in rows)
    nq = sum(1 for r in rows if not r["is_quotable"])
    single = sum(1 for r in rows if r["corroboration_count"] == 0)
    contested = [r for r in rows if r.get("tag_contested")]
    thin = [(gi, len(g)) for gi, (_, g) in enumerate(order, 1) if len(g) < 8]
    L += ["## Coverage note", "",
          f"- **Evidence volume:** {len(rows):,} chunks from {len(works)} independent works.",
          "- **Source mix:** " + ", ".join(f"{k} {v}" for k, v in ty.most_common()),
          "- **Epistemic mix:** " + ", ".join(f"{k} {v}" for k, v in st.most_common()),
          f"- **Not quotable:** {nq} chunks ({nq / len(rows):.0%}) are AI-reworded or OCR needs_recheck. "
          "They may lead to a fact; the fact must be verified elsewhere and paraphrased.",
          f"- **Single-source claims:** {single} chunks ({single / len(rows):.0%}) have no detected independent "
          "corroboration. Attribute them rather than presenting them as settled.",
          f"- **Contested claims present:** {len(contested)} chunks touch a claim in the register "
          f"({', '.join(sorted({c for r in contested for c in [r.get('chapter_buckets','')] if c})[:0]) or 'see kb3/claims_register.yaml'}).",
          f"- **Dominant work:** {works.most_common(1)[0][0]} supplies {works.most_common(1)[0][1]} chunks "
          f"({works.most_common(1)[0][1] / len(rows):.0%}). Watch for a chapter written out of one book.",
          ("- **Page numbers unreliable** for: " + ", ".join(sorted(
              {r["parent_source_id"] for r in rows if r["parent_source_id"] in PAGES_UNRELIABLE}))
           + ". Cite these by section, never by page." if any(
              r["parent_source_id"] in PAGES_UNRELIABLE for r in rows) else
           "- Page numbers: no unreliable-page sources in this chapter."),
          "- **Sources with no page numbers at all** (cite by heading trail): " + ", ".join(sorted(
              {r["parent_source_id"] for r in rows if not r["page"]})) or "none",
          "- **Thin sub-themes:** " + (", ".join(f"#{g} ({n} chunks)" for g, n in thin) if thin else "none"), ""]
    # date sanity: a foundation/completion year far outside the period is almost
    # always OCR damage. adhikari-2013-un-00602 says the temple "was completed in
    # A.D. 1880" — 1080 with a broken digit, labelled factual and quotable.
    suspect = []
    for r in rows:
        # [^.] would stop at the full stop inside "A.D." — allow any characters
        for m in re.finditer(r"(?:built|completed|founded|erected|constructed)\W{0,3}(?:\w+\W{1,3}){0,5}?(1[5-9]\d{2}|20\d{2})" , r["text"], re.I):
            if r.get("tag_udaypur_specific"):
                suspect.append((r["chunk_id"], m.group(0)[:70]))
    if suspect:
        L += ["### Date-sanity flags (check before citing)", "",
              "A construction date far outside the temple's period, on a Udaypur-specific chunk. "
              "Usually OCR damage; the KB cannot tell, so the writer must.", "",
              "| chunk_id | phrase |", "|---|---|"]
        L += [f"| `{i}` | {t} |" for i, t in suspect[:20]]
        L.append("")

    if nq:
        L += ["### Chunks that must not be quoted", "",
              ", ".join(f"`{r['chunk_id']}`" for r in rows if not r["is_quotable"])[:4000], ""]

    f = folder(cid)
    (f / "research.md").write_text("\n".join(L), encoding="utf-8")
    slim = {cid_: {k: v for k, v in r.items() if k != "_vec"} for cid_, r in dossier.items()}
    (f / "dossier.json").write_text(json.dumps(slim, ensure_ascii=False, indent=1), encoding="utf-8")
    state(cid, stage="retrieve", bucket_size=len(rows), dossier=len(slim))
    print(f"{cid}: {len(rows):,} chunks → {len(slim)} in dossier across {len(order)} sub-themes → {f/'research.md'}")
    if advice:
        print(advice.lstrip("\n"))


def cmd_topup(cid, query, n=6):
    """Targeted retrieval for a gap the dossier does not cover (stage 1b).

    The outline stage names gaps; this fills them from the same chapter bucket,
    so a section is never written on air and never on evidence from outside the
    chapter's own scope. Every top-up is logged in state.json.
    """
    from kb3_chroma_query import search
    f = folder(cid)
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    # ask for more than we need: the top of the bucket is already in the dossier,
    # and a top-up is for what the dossier does NOT yet have
    hits = search(query, cid, n * 10)
    added = []
    for r in hits:
        if r["chunk_id"] in dossier or len(added) >= n:
            continue
        r.pop("_vec", None)
        dossier[r["chunk_id"]] = r
        added.append(r)
    (f / "dossier.json").write_text(json.dumps(dossier, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(f / "research.md", "a", encoding="utf-8") as fh:
        fh.write(f"\n## Top-up: “{query}”\n\n"
                 f"_Targeted retrieval {NOW()} to fill a gap named in the outline._\n\n"
                 "| chunk_id | source | type | status | page | quotable | text |\n"
                 "|---|---|---|---|---|---|---|\n")
        for r in added:
            fh.write(f"| `{r['chunk_id']}` | {r['parent_source_id']} | {r['source_type']} | {r['epistemic_status']} | "
                     f"{page_of(r)} | {'yes' if r['is_quotable'] else '**no**'} | "
                     f"{re.sub(r'[|]', '/', re.sub(r'\s+', ' ', r['text']))[:260]} |\n")
    state(cid, stage="topup", last_topup=query, dossier=len(dossier))
    print(f"{cid}: +{len(added)} chunks for “{query}” (dossier now {len(dossier)})")
    for r in added:
        print(f"   {r['chunk_id']} [{r['parent_source_id']}] " + re.sub(r"\s+", " ", r["text"])[:110])


def cmd_cite(cid, chunk_ids, why=""):
    """Add specific chunks to a chapter's dossier by id, whatever bucket they sit in.

    A chapter legitimately needs evidence bucketed elsewhere — C1's survey of
    regimes rests on the mosque and Maratha chunks that belong to C9 and C14.
    The chunk still carries its own provenance and flags; only the dossier
    membership changes, and every addition is logged with a reason.
    """
    import chromadb
    col = chromadb.PersistentClient(path=str(CHROMA)).get_collection(COLLECTION)
    f = folder(cid)
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    got = col.get(where={"chunk_id": {"$in": list(chunk_ids)}},
                  include=["metadatas", "documents"])
    added = []
    for m, d in zip(got["metadatas"], got["documents"]):
        m = dict(m); m["text"] = d
        if m["chunk_id"] in dossier:
            continue
        m["cited_from_other_bucket"] = why or "explicitly requested"
        dossier[m["chunk_id"]] = m
        added.append(m)
    missing = set(chunk_ids) - {m["chunk_id"] for m in got["metadatas"]}
    (f / "dossier.json").write_text(json.dumps(dossier, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(f / "research.md", "a", encoding="utf-8") as fh:
        fh.write(f"\n## Cited from another chapter's bucket\n\n_{why} · added {NOW()}_\n\n"
                 "| chunk_id | source | buckets | status | page | quotable | text |\n"
                 "|---|---|---|---|---|---|---|\n")
        for m in added:
            fh.write(f"| `{m['chunk_id']}` | {m['parent_source_id']} | {m['chapter_buckets']} | "
                     f"{m['epistemic_status']} | {page_of(m)} | {'yes' if m['is_quotable'] else '**no**'} | "
                     + re.sub(r"[|]", "/", re.sub(r"\s+", " ", m["text"]))[:240] + " |\n")
    state(cid, stage="cite", dossier=len(dossier))
    print(f"{cid}: +{len(added)} cited chunks" + (f"; NOT FOUND: {sorted(missing)}" if missing else ""))


# --------------------------------------------------------------------------
# Stage 2 — outline scaffold (human completes and approves)
# --------------------------------------------------------------------------
def cmd_outline(cid):
    f = folder(cid)
    prof = chapter_profile(cid)
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    research = (f / "research.md").read_text(encoding="utf-8")
    subs = re.findall(r"^## Sub-theme (\d+): (.+)$", research, re.M)
    L = [f"# Outline — {cid} {prof['title']}", "",
         f"*Scaffold generated {NOW()}. The writer fills the through-line and the section arguments; "
         "the editor approves before any prose is written (`approve " + cid + " outline`).*", "",
         "## Through-line", "", "_One paragraph: the argument or narrative this chapter carries._", "",
         "## Opening (250–400 words)", "", "_A scene, an object or a document. Evidence: _", "",
         "## Sections", ""]
    for n, name in subs:
        ids = re.findall(r"\| `([^`]+)` \|", research.split(f"## Sub-theme {n}: ")[1].split("## ")[0])
        L += [f"### Section {n} — _title_  ·  sub-theme: {name}", "",
              "_Argument of this section._", "",
              "Evidence: " + ", ".join(f"`{i}`" for i in ids[:10]), "",
              "Gaps: _what this section needs that the dossier does not have_", ""]
    L += ["## Bridge out (150–250 words)", "", "_Close the argument; turn to the next chapter._", "",
          "## Research gaps to settle before drafting", "",
          "_List anything a section rests on that the KB cannot support. Each gap is either filled by "
          "more retrieval, narrowed, or cut — never written on air._", ""]
    (f / "outline.md").write_text("\n".join(L), encoding="utf-8")
    state(cid, stage="outline")
    print(f"{cid}: outline scaffold → {f/'outline.md'}  (edit it, then: approve {cid} outline)")


def cmd_approve(cid, what, force=False):
    f = folder(cid)
    s = state(cid)
    if what == "draft":
        if not (f / "qa_review.md").exists():
            raise SystemExit("run `verify` before approving the draft")
        drafts = drafts_of(f)
        if not drafts:
            raise SystemExit(f"no draft found in {f}")
        latest = drafts[-1]
        blocks = []
        if s.get("draft") != latest.name:
            blocks.append(f"the last `verify` ran on {s.get('draft')!r}, but the newest draft is "
                          f"{latest.name!r} — re-run `verify {cid}`")
        if s.get("findings"):
            blocks.append(f"the last `verify` left {s['findings']} finding(s) unfixed — see "
                          f"{(f / 'qa_review.md').name}")
        gaps = latest.read_text(encoding="utf-8").count("[GAP:")
        if gaps:
            blocks.append(f"{latest.name} still carries {gaps} `[GAP: …]` placeholder(s); a chapter "
                          "with unwritten sections is not ready to approve")
        if blocks and not force:
            raise SystemExit("cannot approve the draft:\n  - " + "\n  - ".join(blocks)
                             + "\nfix these, or re-run with --force to approve anyway.")
        if blocks:
            print("WARNING — approving over " + str(len(blocks)) + " objection(s):")
            for b in blocks:
                print("  - " + b)
    extra = {f"approved_{what}": NOW()}
    if what == "draft" and force:
        extra["approved_draft_forced"] = True
    state(cid, stage=f"approved:{what}", **extra)
    print(f"{cid}: {what} approved at {NOW()}" + (" (forced)" if force and what == "draft" else ""))


# --------------------------------------------------------------------------
# Stage 3 — per-section drafting brief
# --------------------------------------------------------------------------
# Headings that are apparatus, not a section anyone drafts.
NOT_A_SECTION = re.compile(
    r"^(drafting order|budget|sources?\b|evidence\b|coverage|gaps?\b|contents|"
    r"what to write|rules|appendix|notes?\b)", re.I)


def outline_sections(outline):
    """Every draftable section, in order, whatever format the outline uses.

    `outline` writes '### Section 2 Title'; C1's was hand-written as
    '## 1.2 The inventory (~900 w) — …'. Both parse here."""
    heads = list(re.finditer(r"^#{2,4}[ \t]+(.+?)[ \t]*$", outline, flags=re.M))
    out = []
    for n, m in enumerate(heads):
        title = m.group(1).strip()
        end = heads[n + 1].start() if n + 1 < len(heads) else len(outline)
        body = outline[m.end():end]
        num = re.match(r"(?:Section[ \t]+)?(\d+(?:\.\d+)*)[ \t]*(.*)", title)
        key = num.group(1) if num else ""
        label = (num.group(2) if num else title).strip(" —-–:")
        if NOT_A_SECTION.match(label or title):
            continue
        out.append({"key": key, "label": label or title, "title": title, "body": body})
    return out


def resolve_section(sections, want):
    """Accept the section's own number, its position in the outline, or its name."""
    w = str(want).strip().lower()
    for s in sections:
        if s["key"].lower() == w:
            return s
    if w.isdigit() and 1 <= int(w) <= len(sections):
        return sections[int(w) - 1]
    hits = [s for s in sections if w and w in s["label"].lower()]
    return hits[0] if len(hits) == 1 else None


def section_stem(sec):
    """A filename stem that survives '1.1' as well as '2'."""
    if sec["key"].isdigit():
        return f"{int(sec['key']):02d}"
    if sec["key"]:
        return sec["key"].replace(".", "_")
    return re.sub(r"\W+", "_", sec["label"].lower()).strip("_")[:24] or "section"


def cmd_brief(cid, section):
    f = folder(cid)
    s = state(cid)
    if not s.get("approved_outline"):
        raise SystemExit(f"outline not approved — run: approve {cid} outline")
    outline = (f / "outline.md").read_text(encoding="utf-8")
    sections = outline_sections(outline)
    sec = resolve_section(sections, section)
    if not sec:
        avail = "; ".join(f"{s['key'] or '—'} {s['label'][:38]}" for s in sections)
        raise SystemExit(f"section {section!r} not found in {f/'outline.md'}.\n"
                         f"available: {avail}\n"
                         "address a section by its number (1.1), its position (1) or its name.")
    match = sec["body"]
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    ids, seen = [], set()
    for i in re.findall(r"`([^`]+)`", match):      # backticks also hold filenames
        if i in dossier and i not in seen:
            seen.add(i)
            ids.append(i)
    style = (ROOT / "STYLE_GUIDE.md").read_text(encoding="utf-8")
    L = [f"# Drafting brief — {cid} section {sec['key'] or sec['label']}"
         + (f": {sec['label']}" if sec["key"] else ""), "",
         "## What to write", "", match.split("Evidence:")[0].strip(), "",
         "## Rules (from STYLE_GUIDE.md — the QA pass checks these mechanically)", "",
         "- 500–900 words. Open on something specific, not a signpost.",
         "- Every factual sentence ends with `[src: chunk_id]` before the full stop.",
         "- Only the chunk ids below may be cited. If a point needs evidence that is not here, "
         "write `[GAP: what is missing]` instead of asserting it.",
         "- Quote only chunks marked quotable=yes, and quote them exactly.",
         "- A sentence resting on an `inference` or `speculation` chunk must attribute or hedge.",
         "- IAST diacritics exact; 'Udaypur' in the book's voice.", "",
         "## Evidence for this section", ""]

    sb = load_sourcebook(cid)
    if sb.get("facts"):
        order = ["contested", "unverified", "established", "single-source"]
        # consume the evidence heading AND its blank line; both are re-added below,
        # so the sourcebook block sits between the rules and the evidence
        L[-2:] = ["## What the sourcebook already establishes for this chapter", "",
                  f"From `BOOK_SOURCEBOOK.md` (built {sb.get('generated','?')}). Treat these as the "
                  "chapter's standing findings: the status decides how each may appear on the page.",
                  ""]
        for st in order:
            group = [f for f in sb["facts"] if f["status"] == st]
            if not group:
                continue
            L += [f"**`[{st}]` — {STATUS_RULE[st]}**", ""]
            for fct in group[:14]:
                codes = " · ".join(f"`{c}`" for c in fct["codes"]) or "`—`"
                line = f"- {fct['text']} — {codes}"
                if fct.get("curated"):
                    line += " *(curated)*"
                if fct.get("positions"):
                    line += " — competing values: " + "; ".join(
                        f"**{q['value']}** (`{q['code']}`)" for q in fct["positions"])
                L.append(line)
                if fct.get("note"):
                    L.append(f"  - {fct['note']}")
            L.append("")
        if sb.get("gaps"):
            L += ["**`[gap]` — " + STATUS_RULE["gap"] + "**", ""]
            L += [f"- {g}" for g in sb["gaps"]] + [""]
        if sb.get("dominant", {}).get("share", 0) > 0.45:
            L += [f"**Single-source risk:** `{sb['dominant']['code']}` supplies "
                  f"{sb['dominant']['share']:.0%} of this chapter's evidence. Corroborate before "
                  "asserting anything that rests on it alone.", ""]
        L += ["## Evidence for this section", ""]
    for i in ids:
        r = dossier.get(i)
        if not r:
            continue
        L += [f"### `{i}`  ·  {r['parent_source_id']}  ·  {r['source_type']} / {r['epistemic_status']}"
              f"  ·  page {page_of(r)}  ·  corroborated by {r['corroboration_count']}"
              f"  ·  quotable: {'yes' if r['is_quotable'] else 'NO — paraphrase only'}",
              "", "> " + re.sub(r"\s+", " ", r["text"])[:1800], ""]
    stem = section_stem(sec)
    p = f / "sections" / f"{stem}_brief.md"
    p.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {p}  ({len(ids)} evidence chunks) — write the prose to "
          f"{f/'sections'/f'{stem}.md'}")


# --------------------------------------------------------------------------
# Stage 3b — assemble section drafts into the next whole-chapter draft
# --------------------------------------------------------------------------
BUDGET_TAIL = re.compile(r"\s*\(~?\s*\d[\d,]*\s*w\.?\)\s*", re.I)


def clean_heading(sec):
    """The outline's label carries a word budget and a source hint; a chapter
    heading carries neither."""
    label = BUDGET_TAIL.sub(" ", sec["label"])
    label = re.split(r"\s+[—–]\s+", label)[0].strip(" :—–-")
    return f"## {sec['key']} {label}".replace("##  ", "## ").rstrip()


def cmd_assemble(cid, partial=False):
    f = folder(cid)
    s = state(cid)
    if not s.get("approved_outline"):
        raise SystemExit(f"outline not approved — run: approve {cid} outline")
    sections = outline_sections((f / "outline.md").read_text(encoding="utf-8"))

    parts, missing = [], []
    for sec in sections:
        src = f / "sections" / f"{section_stem(sec)}.md"
        if not src.exists():
            missing.append(f"{sec['key'] or sec['label'][:24]} -> {src.name}")
            continue
        body = src.read_text(encoding="utf-8").strip()
        if not body:
            missing.append(f"{sec['key'] or sec['label'][:24]} -> {src.name} (empty)")
            continue
        # the writer's own heading wins; otherwise take one from the outline
        if not re.match(r"^#{2,4}\s", body):
            body = clean_heading(sec) + "\n\n" + body
        parts.append((sec, body))

    if missing and not partial:
        raise SystemExit("not all sections are written:\n  "
                         + "\n  ".join(missing)
                         + "\nwrite them, or re-run with --partial to assemble what exists.")

    if not parts:
        raise SystemExit("no section drafts found under " + str(f / "sections"))

    drafts = drafts_of(f)
    title = None
    if drafts:
        first = drafts[-1].read_text(encoding="utf-8").lstrip().splitlines()[0]
        if first.startswith("# "):
            title = first
    title = title or f"# {cid} · {chapter_profile(cid).get('title', cid)}"

    out = [title, ""]
    for sec, body in parts:
        out += [body.strip(), ""]
        if partial and missing:
            pass
    if partial:
        for m in missing:
            out += [f"`[GAP: section not yet written — {m}]`", ""]

    nxt = (max(int(re.search(r"draft-v(\d+)", d.name).group(1)) for d in drafts) + 1) if drafts else 1
    path = f / f"draft-v{nxt}.md"
    text = unicodedata.normalize("NFC", "\n".join(out).rstrip() + "\n")
    path.write_text(text, encoding="utf-8")

    words = len(re.findall(r"\b[\w'ऀ-ॿ-]+\b", SRC.sub("", re.sub(r"^#.*$", "", text, flags=re.M))))
    state(cid, stage="assemble", assembled_draft=path.name, assembled_from=[s["key"] or s["label"] for s, _ in parts])
    print(f"{cid}: assembled {len(parts)} section(s) -> {path.name}  ({words:,} words)")
    if missing:
        print("  still missing: " + "; ".join(missing))
    print(f"  next: python chapter_pipeline.py verify {cid}")


# --------------------------------------------------------------------------
# Stage 4 — verification + QA review
# --------------------------------------------------------------------------
def sentences(t):
    """Split into sentences, keeping each sentence's trailing markers with it.

    A marker follows the full stop it belongs to ("… was not empty [src: x]."
    but also "… not empty. [ed]"), so a naive split either glues sentences
    together or orphans the marker from the sentence it qualifies. Both cost
    the checker its accuracy: the first hides unsourced sentences, the second
    invents them.
    """
    t = re.sub(r"\[src:[^\]]+\]", lambda m: m.group(0).replace(".", ""), t)
    # "V.S. 1116" and "A.H. 737-39" are not sentence ends
    t = ABBREV.sub(lambda m: m.group(0).replace(".", ""), t)
    out: list[str] = []
    for frag in re.split(r"(?<=[.!?])\s+", t):
        f = frag
        while out:                                   # leading markers belong to the previous sentence
            m = re.match(r"\s*(\[ed\]|\[src:[^\]]*\]|\[UNVERIFIED[^\]]*\])\s*", f)
            if not m:
                break
            out[-1] += " " + m.group(1)
            f = f[m.end():]
        if not f.strip():
            continue
        if out and f[:1].islower():                  # continuation of the previous sentence
            out[-1] += " " + f
        else:
            out.append(f)
    return [p.replace("", ".") for p in out]


def cmd_verify(cid, draft=None):
    f = folder(cid)
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    drafts = drafts_of(f)
    path = Path(draft) if draft else (drafts[-1] if drafts else None)
    if not path or not path.exists():
        raise SystemExit(f"no draft found in {f} (expected draft-v1.md)")
    text = path.read_text(encoding="utf-8")
    body = re.sub(r"^#.*$", "", text, flags=re.M)
    words = len(re.findall(r"\b[\w'ऀ-ॿ-]+\b", re.sub(r"\[src:[^\]]+\]", "", body)))

    findings = []
    cited = collections.Counter()
    for m in SRC.finditer(text):
        for i in re.split(r"[,;]\s*", m.group(1).strip()):
            cited[i.strip()] += 1
    unknown = [i for i in cited if i not in dossier]
    for i in unknown:
        findings.append(("fabricated-citation", f"`{i}` is not in this chapter's dossier"))

    # unsourced factual sentences
    unsourced = []
    for s in sentences(body):
        s_clean = s.strip()
        if len(s_clean) < 40 or s_clean.startswith((">", "#", "*[")):
            continue
        if SRC.search(s_clean) or "[GAP" in s_clean or "[ed]" in s_clean:
            continue                      # [ed] = the author's own framing, asserting no KB fact
        if FACTUAL_HINT.search(s_clean):
            unsourced.append(s_clean[:160])
    for s in unsourced:
        findings.append(("unsourced-sentence", s))

    # quotations
    for m in QUOTE.finditer(body):
        q = m.group(1)
        if len(q.split()) < 6:
            continue
        tail = body[m.end():m.end() + 220]
        ids = [i.strip() for mm in SRC.finditer(tail) for i in re.split(r"[,;]", mm.group(1))]
        ok = False
        for i in ids:
            r = dossier.get(i)
            if r and r["is_quotable"] and fold(q)[:80] in fold(r["text"]):
                ok = True
        if not ok:
            nonquote = [i for i in ids if dossier.get(i) and not dossier[i]["is_quotable"]]
            findings.append(("unverified-quotation",
                             f"“{q[:90]}…” — " + ("cited chunk is NOT quotable: " + ", ".join(nonquote)
                                                  if nonquote else "not found verbatim in any cited chunk")))

    # epistemic discipline
    for s in sentences(body):
        ids = [i.strip() for m in SRC.finditer(s) for i in re.split(r"[,;]", m.group(1))]
        for i in ids:
            r = dossier.get(i)
            if not r:
                continue
            if r["epistemic_status"] in ("inference", "speculation"):
                if not (HEDGE.search(s) or ATTRIB.search(s)):
                    findings.append((f"{r['epistemic_status']}-asserted",
                                     f"`{i}` is {r['epistemic_status']} but the sentence asserts it: {s.strip()[:140]}"))
    # the sourcebook's standing findings, where a draft can break them silently
    sb = load_sourcebook(cid)
    paras = body.split("\n\n")
    for fct in sb.get("facts", []):
        if fct["status"] == "contested" and fct.get("positions"):
            # match on the year span: a value may be dressed as
            # "1070–1093 (from the coinage)", which no sentence will contain
            vals, spans = [], {}
            for q in fct["positions"]:
                m = re.search(r"\d{3,4}\s*[–-]\s*\d{2,4}", q["value"])
                if not m:
                    continue
                vals.append(q["value"])
                spans[q["value"]] = m.group()
            hits = [v for v in vals if spans[v] in body]
            if len(hits) == 1:
                near = next((p for p in paras if spans[hits[0]] in p), "")
                if not (HEDGE.search(near) or "contested" in near.lower()
                        or "disput" in near.lower()):
                    findings.append(("contested-flattened",
                                     f"the draft gives only {spans[hits[0]]!r} of the competing values "
                                     + ", ".join(repr(v) for v in vals)
                                     + " — show the disagreement or hedge it"))
        if fct["status"] == "unverified" and "[UNVERIFIED" not in text:
            if any(ch in cited for ch in fct.get("chunks", [])):
                findings.append(("unverified-unflagged",
                                 "a chunk behind an unverified sourcebook fact is cited but no "
                                 "`[UNVERIFIED — …]` flag appears in the draft"))

    # diacritics / encoding
    if "�" in text or re.search(r"[ÃÂ]\w", text):
        findings.append(("encoding", "mojibake found — the text is not clean NFC"))
    if unicodedata.normalize("NFC", text) != text:
        findings.append(("encoding", "text is not NFC-normalised"))
    findings += translit_findings(body)
    if not (WORDS_MIN <= words <= WORDS_MAX):
        findings.append(("length", f"{words:,} words, outside {WORDS_MIN:,}–{WORDS_MAX:,}"))

    # evidence spread
    srcs = collections.Counter(dossier[i]["parent_source_id"] for i in cited if i in dossier)
    if srcs:
        top, n = srcs.most_common(1)[0]
        if n / max(1, sum(srcs.values())) > 0.5:
            findings.append(("evidence-spread", f"{n}/{sum(srcs.values())} citations come from {top}"))

    by_kind = collections.Counter(k for k, _ in findings)
    L = [f"# QA review — {cid} ({path.name})", "",
         f"Run {NOW()} by `chapter_pipeline.py verify {cid}`. Mechanical checks first; the editorial "
         "review below is written by the reviewer against the same draft.", "",
         "## Mechanical checks", "", "| check | result |", "|---|---|",
         f"| length | {words:,} words ({'ok' if WORDS_MIN <= words <= WORDS_MAX else 'OUT OF RANGE'}) |",
         f"| provenance markers | {sum(cited.values())} markers, {len(cited)} distinct chunks |",
         f"| citations resolving to the dossier | {len(cited) - len(unknown)}/{len(cited)} "
         f"({'**' + str(len(unknown)) + ' fabricated**' if unknown else 'none fabricated'}) |",
         f"| unsourced factual sentences | {by_kind.get('unsourced-sentence', 0)} |",
         f"| quotations verified against quotable chunks | "
         f"{'all' if not by_kind.get('unverified-quotation') else str(by_kind['unverified-quotation']) + ' FAILED'} |",
         f"| inference/speculation asserted without hedge | "
         f"{by_kind.get('inference-asserted', 0) + by_kind.get('speculation-asserted', 0)} |",
         f"| evidence spread | {', '.join(f'{s} {n}' for s, n in srcs.most_common(6))} |",
         f"| encoding | {'clean NFC' if not by_kind.get('encoding') else 'PROBLEM'} |",
         f"| gaps left in the draft | {text.count('[GAP')} |",
         f"| editorial framing sentences ([ed]) | {text.count('[ed]')} |", ""]
    if findings:
        L += ["## Findings to fix", "", "| kind | detail |", "|---|---|"]
        for k, d in findings[:120]:
            L.append(f"| {k} | {d.replace('|', '/')} |")
        L.append("")
    else:
        L += ["**No mechanical findings.**", ""]
    L += ["## Editorial review", "",
          "_Fill in against the draft: What Works · Clarity · Flow · Evidence · Style · line-edits._", "",
          "### What works", "", "### Clarity", "", "### Flow", "", "### Evidence", "", "### Style", "",
          "### Line edits", ""]
    (f / "qa_review.md").write_text("\n".join(L), encoding="utf-8")
    state(cid, stage="verify", words=words, findings=len(findings),
          fabricated=len(unknown), draft=path.name)
    print(f"{cid}: {words:,} words · {len(findings)} findings "
          f"({len(unknown)} fabricated citations) → {f/'qa_review.md'}")
    return findings


# --------------------------------------------------------------------------
# Stage 5 — handoff package
# --------------------------------------------------------------------------
def cmd_handoff(cid):
    f = folder(cid)
    s = state(cid)
    if not s.get("approved_draft"):
        raise SystemExit(f"draft not approved — run: verify {cid}, then approve {cid} draft")
    dossier = json.loads((f / "dossier.json").read_text(encoding="utf-8"))
    path = drafts_of(f)[-1]
    text = path.read_text(encoding="utf-8")
    prof = chapter_profile(cid)

    # One numbered entry per distinct work: every chunk drawn from the same book
    # shares that book's note number, and the provenance appendix below resolves
    # each note back to the individual chunk, page and epistemic status.
    def work_of(i):
        r = dossier.get(i, {})
        return r.get("parent_source_id") or f"{r.get('author', '?')}|{r.get('title', '?')}"

    order, notes, works = [], {}, {}
    def repl(m):
        ids = [i.strip() for i in re.split(r"[,;]\s*", m.group(1).strip())]
        nums = []
        for i in ids:
            if i not in notes:
                order.append(i)
                notes[i] = works.setdefault(work_of(i), len(works) + 1)
            if str(notes[i]) not in nums:
                nums.append(str(notes[i]))
        return "[" + ",".join(nums) + "]"
    final = SRC.sub(repl, text)
    # adjacent markers on the same book now carry the same number — collapse them
    final = re.sub(r"\[(\d+)\](?:,\s*\[\1\])+", r"[\1]", final)

    def page_key(p):
        m = re.match(r"\d+", str(p))
        return (0, int(m.group())) if m else (1, str(p))

    cites = ["## Sources cited", ""]
    for w, n in sorted(works.items(), key=lambda kv: kv[1]):
        chunks = [i for i in order if work_of(i) == w]
        r = dossier.get(chunks[0], {})
        pages = sorted({str(dossier[i]["page"]) for i in chunks
                        if dossier.get(i, {}).get("page")}, key=page_key)
        cites.append(f"{n}. {r.get('author','?')} — *{r.get('title','?')}*"
                     + (f", {'pp.' if len(pages) > 1 else 'p.'} {', '.join(pages)}" if pages else "")
                     + f". [{r.get('source_type','?')}]"
                     + f" — {len(chunks)} passage{'s' if len(chunks) > 1 else ''} cited;"
                     + " see the provenance appendix.")
    (f / "handoff" / f"{cid}_chapter.md").write_text(final + "\n\n" + "\n".join(cites) + "\n", encoding="utf-8")

    # Reading copy: continuous prose, as a reader would meet it. Citation markers
    # and [ed] come out; an [UNVERIFIED] flag deliberately stays, so nothing
    # unconfirmed can be mistaken for fact. The marked copy above remains the
    # authoritative one — both are generated from the same approved draft.
    _codes = load_sourcebook().get("codes", {})   # one citation scheme across the project
    clean, endnotes = reading_and_notes(text, dossier)
    (f / f"{cid}_chapter_reading.md").write_text(clean.rstrip() + "\n", encoding="utf-8")

    # Short forms, so a work's full citation is printed exactly once. A surname
    # alone where it is unambiguous; surname plus short title where two works
    # share an author; the title alone where the author is unnamed.
    def surname_of(author):
        a = re.sub(r"\(.*?\)", "", author or "").strip()
        if "INTACH" in a.upper():
            return "INTACH"
        people = [x.strip() for x in a.split("+")[0].split(",") if x.strip()]
        if len(people) > 1:                                   # a compiled work: name both
            return " & ".join(x.split()[-1] for x in people[:2])
        return people[0].split()[-1] if people and people[0].split() else "?"

    STOPW = {"the", "a", "an", "of", "and", "&", "from", "in", "to", "for", "on", "part"}

    def title_words(title):
        head = re.split(r"[:,]", title or "")[0]
        ws = [w for w in head.split() if w]
        while ws and ws[0].lower() in STOPW:
            ws.pop(0)
        return ws

    works_meta = {}
    for w in works:
        chunks = [i for i in order if work_of(i) == w]
        r = dossier.get(chunks[0], {})
        works_meta[w] = {"author": r.get("author", "?"), "title": r.get("title", "?"),
                         "surname": surname_of(r.get("author", "")),
                         "words": title_words(r.get("title", "")), "chunks": chunks}

    def short_title(v, others):
        """Fewest leading title words that are unique and do not end on a stop-word."""
        for n in range(1, 6):
            cand = v["words"][:n]
            if not cand or cand[-1].lower().strip(".,") in STOPW:
                continue
            s = " ".join(cand)
            if all(" ".join(o["words"][:n]) != s for o in others):
                return s[0].upper() + s[1:]
        return " ".join(v["words"][:3]) or v["title"]

    counts = collections.Counter(v["surname"] for v in works_meta.values())
    for w, v in works_meta.items():
        others = [o for k, o in works_meta.items() if k != w]
        if v["author"].lower().startswith("not named"):
            v["short"] = f"*{short_title(v, others)}*"
        elif counts[v["surname"]] > 1:
            v["short"] = f"{v['surname']}, *{short_title(v, others)}*"
        else:
            v["short"] = v["surname"]

    def cite(ids):
        """Short form plus the pages these chunks sit on; the full entry lives in Works cited."""
        by_work = {}
        for i in ids:
            by_work.setdefault(work_of(i), []).append(i)
        parts = []
        for w, chunks in by_work.items():
            pages = sorted({str(dossier[i]["page"]) for i in chunks
                            if dossier.get(i, {}).get("page")}, key=page_key)
            parts.append(works_meta[w]["short"]
                         + (f", {'pp.' if len(pages) > 1 else 'p.'} {', '.join(pages)}" if pages else ""))
        return "; ".join(parts)

    en = [f"# Works cited and endnotes — {cid} {prof['title']}", "",
          "Every work appears once, in full, in the first list. The notes then refer to it by the "
          "short form given there, so no title is printed twice. A note number identifies a source "
          "rather than a sentence: where several sentences in a row rest on the same work they "
          "carry one note, and where a claim is corroborated the note names every work that "
          "carries it. The trailing `[kb: …]` tag is the knowledge base's own chunk id, for "
          "checking against the provenance appendix.", "",
          "## Works cited", ""]
    for w, v in sorted(works_meta.items(), key=lambda kv: kv[1]["short"].lower()):
        pages = sorted({str(dossier[i]["page"]) for i in v["chunks"]
                        if dossier.get(i, {}).get("page")}, key=page_key)
        # the label is already emphasis in the notes; bold-inside-italic renders badly,
        # so the works-cited entry takes the plain form
        code = _codes.get(w, "")
        label = (f"{code} · " if code else "") + v["short"].replace("*", "")
        en.append(f"**{label}** — {v['author']}, *{v['title']}*"
                  + (f", {'pp.' if len(pages) > 1 else 'p.'} {', '.join(pages)}" if pages else "") + ".")
        en.append("")
    en += ["## Notes", ""]
    for r in endnotes:
        if r["kind"] == "unverified":
            en.append(f"{r['n']}. {r['phrase']} — **not supported by any ingested source.** "
                      "Flagged pending verification; no citation exists for this claim and none "
                      "should be supplied until a source is produced. See the handoff's "
                      "must-resolve items.")
        else:
            en.append(f"{r['n']}. {r['phrase']} — {cite(r['ids'])}. "
                      "[kb: " + ", ".join(f"`{i}`" for i in r["ids"]) + "]")
        en.append("")
    (f / f"{cid}_endnotes.md").write_text("\n".join(en) + "\n", encoding="utf-8")

    prov = [f"# Provenance appendix — {cid} {prof['title']}", "",
            "Every claim marker in the chapter, resolved to its KB chunk. An editor can check any line "
            "here without re-searching the corpus: the chunk id is the KB's own identifier, the page is "
            "the source's page, and `verify` re-checks these mechanically. A note number identifies a "
            "work, not a single passage — each book appears once in *Sources cited*, and the rows below "
            "give every passage cited from it, in the order the chapter first uses them.", "",
            "| note | chunk_id | source | type | status | page | corrob. | quotable | passage |",
            "|--:|---|---|---|---|---|--:|---|---|"]
    for i in order:
        r = dossier.get(i, {})
        prov.append(f"| {notes[i]} | `{i}` | {r.get('parent_source_id','?')} | {r.get('source_type','?')} | "
                    f"{r.get('epistemic_status','?')} | {r.get('page') or '—'} | {r.get('corroboration_count','?')} | "
                    f"{'yes' if r.get('is_quotable') else 'no'} | "
                    f"{re.sub(r'\s+', ' ', r.get('text', ''))[:300].replace('|', '/')} |")
    (f / "handoff" / "provenance_appendix.md").write_text("\n".join(prov) + "\n", encoding="utf-8")

    used = {i: dossier[i] for i in order if i in dossier}
    st = collections.Counter(r["epistemic_status"] for r in used.values())
    single = [i for i, r in used.items() if r["corroboration_count"] == 0]
    nonq = [i for i, r in used.items() if not r["is_quotable"]]
    research = (f / "research.md").read_text(encoding="utf-8")
    cov = research.split("## Coverage note")[-1]
    qa = (f / "qa_review.md").read_text(encoding="utf-8")
    note = [f"# Coverage and caveats — {cid} {prof['title']}", "",
            "## What this chapter rests on", "",
            f"- {len(used)} KB chunks cited, from {len(set(r['parent_source_id'] for r in used.values()))} sources.",
            "- Epistemic mix of what was cited: " + ", ".join(f"{k} {v}" for k, v in st.most_common()), "",
            "## What an editor should check", "",
            f"- **Single-source claims ({len(single)}):** " + (", ".join(f"`{i}`" for i in single[:25]) or "none")
            + ". These are attributed in the prose rather than asserted; confirm the attribution reads fairly.",
            f"- **Cited but not quotable ({len(nonq)}):** " + (", ".join(f"`{i}`" for i in nonq[:25]) or "none")
            + ". Used as leads and paraphrased. If you want a direct quotation from any of these, the "
            "underlying page image must be read first.", "",
            "## Coverage of the chapter bucket (from the dossier)", cov, "",
            "## QA state at handoff", "",
            qa.split("## Editorial review")[0].split("## Mechanical checks")[-1], ""]
    (f / "handoff" / "coverage_and_caveats.md").write_text("\n".join(note), encoding="utf-8")
    state(cid, stage="handoff", notes=len(order))
    print(f"{cid}: handoff → {f/'handoff'} ({len(order)} notes)")


def cmd_status():
    cfg = chapters_cfg()["chapters"]
    print(f"{'chapter':5s} {'title':52s} {'stage':22s} {'words':>6s} {'findings':>8s}")
    for c in cfg:
        f = BOOK / c["id"] / "state.json"
        if not f.exists():
            print(f"{c['id']:5s} {c['title'][:50]:52s} {'-':22s}")
            continue
        s = json.loads(f.read_text(encoding="utf-8"))
        last = max(s["stages"], key=lambda k: s["stages"][k]) if s.get("stages") else "-"
        print(f"{c['id']:5s} {c['title'][:50]:52s} {last:22s} {s.get('words','-'):>6} {s.get('findings','-'):>8}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    r = sub.add_parser("retrieve"); r.add_argument("chapter"); r.add_argument("-k", type=int, default=8)
    r.add_argument("--rel-floor", type=float, default=0.0, dest="rel_floor",
                   help="drop chunks below this chapter-relevance score before clustering")
    r.add_argument("--per-group", type=int, default=14)
    t = sub.add_parser("topup"); t.add_argument("chapter"); t.add_argument("query"); t.add_argument("-n", type=int, default=6)
    c = sub.add_parser("cite"); c.add_argument("chapter"); c.add_argument("ids", nargs="+"); c.add_argument("--why", default="")
    o = sub.add_parser("outline"); o.add_argument("chapter")
    a = sub.add_parser("approve"); a.add_argument("chapter"); a.add_argument("what", choices=["outline", "draft"])
    a.add_argument("--force", action="store_true",
                    help="approve a draft despite findings, gaps or a stale verify")
    b = sub.add_parser("brief"); b.add_argument("chapter"); b.add_argument("section")
    a = sub.add_parser("assemble"); a.add_argument("chapter")
    a.add_argument("--partial", action="store_true",
                   help="assemble the sections that exist, flagging the rest as gaps")
    v = sub.add_parser("verify"); v.add_argument("chapter"); v.add_argument("--draft")
    h = sub.add_parser("handoff"); h.add_argument("chapter")
    n = ap.parse_args(argv)
    if n.cmd == "status":
        return cmd_status()
    if n.cmd == "retrieve":
        return cmd_retrieve(n.chapter, n.k, n.per_group, n.rel_floor)
    if n.cmd == "cite":
        return cmd_cite(n.chapter, n.ids, n.why)
    if n.cmd == "topup":
        return cmd_topup(n.chapter, n.query, n.n)
    if n.cmd == "outline":
        return cmd_outline(n.chapter)
    if n.cmd == "approve":
        return cmd_approve(n.chapter, n.what, n.force)
    if n.cmd == "brief":
        return cmd_brief(n.chapter, n.section)
    if n.cmd == "assemble":
        return cmd_assemble(n.chapter, n.partial)
    if n.cmd == "verify":
        cmd_verify(n.chapter, n.draft)
        return 0
    if n.cmd == "handoff":
        return cmd_handoff(n.chapter)


if __name__ == "__main__":
    sys.exit(main() or 0)
