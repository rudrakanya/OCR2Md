#!/usr/bin/env python
"""Stage 1B — chunk every reference source into claim-coherent units and
classify each chunk.

    python stage1_classify.py                  # all sources in the registry
    python stage1_classify.py --only ganguly-paramara

Deterministic and offline: no model is called. Every label records the rule
that fired and the exact cue phrases that drove it, so any decision can be
checked by a human reading the log.

WHAT IT DECIDES
  source_type       inherited from kb_audit/source_registry.yaml (book level)
  epistemic_status  read from the chunk's OWN language, sentence by sentence:
      factual      assertive declarative, no hedge
      observation  firsthand, author-attributed reporting (fieldwork verbs,
                   first person, present-condition description in a field
                   source)
      inference    a conclusion drawn from evidence: reasoning connectors, or
                   a hedge that is anchored by evidence / citation apparatus
      speculation  a hedge with NO traceable anchor

DESIGN DECISIONS (each one answers a defect the audit found)
  * No overlap between chunks. The old store repeated ~270 chars in 62.5% of
    adjacent pairs, so every boundary claim was stored twice and any naive
    corroboration count double-counted it.
  * Chunks end on sentence boundaries only. The old store ended 27.5% of
    chunks mid-sentence.
  * A paragraph is split where it crosses from certain {factual, observation}
    to uncertain {inference, speculation} language, so a speculative aside is
    not filed under its neighbour's factual label (spec 1B.3).
  * Deontic "may be" (a sastra prescribing "the width may be six digits") is
    NOT an epistemic hedge. Treating it as one produced 135 false speculation
    flags in the Samarangana-sutradhara alone.
  * Folklore and opinion are TAGS, never speculation (spec C6).
  * OCR-model commentary leaked into the text ("The OCR has hallucinated...")
    is not source content: it is stripped before chunking and every removal
    is logged.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
REF = ROOT / "Udaypur Reference Markdown Files"
OUT = ROOT / "kb_audit"
REGISTRY = OUT / "source_registry.yaml"

TARGET, MAX_CHARS, MIN_CHARS, MIN_SPLIT = 900, 1600, 250, 150
VERSION = "stage1-classify/1.0"

# --------------------------------------------------------------------------
# Pre-processing: things that are not source content
# --------------------------------------------------------------------------
PAGE_RX = [
    (re.compile(r"<!--\s*page\s+(\d+)[^>]*-->", re.I), "pdf_page"),
    (re.compile(r"^-{2,}\s*PAGE\s+(\d+)\s*-{2,}\s*$", re.I | re.M), "printed_page"),
    (re.compile(r"^\*\*Page\s+(\d+)\*\*\s*$", re.I | re.M), "printed_page"),
]
COMMENT_RX = re.compile(r"<!--.*?-->", re.S)
IMAGE_RX = re.compile(r"!\[[^\]]*\]\([^)]*\)")
CHATTER_RX = re.compile(
    r"[^.\n]*\bThe OCR (?:has|result)[^.\n]*\.?"
    r"|[^.\n]*\bis a hallucination and does not correspond[^.\n]*\.?"
    r"|Therefore, the correct OCR output is an empty string\.?"
    r"|The image is too blurry to recognize any text content\.?"
    r"|The image contains no text\.?"
    r"|\[Non-Text\]"
    r"|\*\[No machine-readable text detected[^\]]*\]\*"
    r"|[^.\n]*\bThe Ground Truth image\b[^\n]*"
    r"|[^.\n]*\bThe provided OCR (?:content|output|text)\b[^\n]*"
    r"|[^.\n]*\bAccording to Rule \d+\b[^\n]*"
    r"|^[^\n]*[一-鿿]{4,}[^\n]*$",          # CJK lines: bilingual-model hallucination
    re.I | re.M)

# --------------------------------------------------------------------------
# Cue lexicons — the auditable heart of the classifier
# --------------------------------------------------------------------------
def rx(*parts):
    return re.compile("|".join(parts), re.I)

# Epistemic uncertainty. Deliberately excludes bare "may be" (deontic in a
# sastra) and "may have + noun" ("a temple may have several shrines").
HEDGE = rx(
    r"\b(?:may|might|could) have (?:been|had|\w+ed|\w+en)\b",
    r"\bmight (?:be|have)\b(?! (?:said|called|termed))",
    r"\bcould be\b(?! (?:seen|found|noticed|observed|reached))",
    # "possible" alone is not a hedge ("identification is not possible").
    r"\bprobabl[ey]\b", r"\bpossibly\b", r"\bit is (?:quite |very |also )?possible\b",
    r"\bpossible that\b", r"\bpossibility\b", r"\bperhaps\b", r"\bpresumabl[ey]\b",
    r"\b(?:seems?|seemed|appears?|appeared) to\b", r"\bit (?:seems|appears)\b",
    r"\bit (?:is|was) (?:thought|believed|supposed|surmised|conjectured)\b",
    r"\bin all (?:likelihood|probability)\b", r"\b(?:is|are|was|were) (?:likely|unlikely)\b",
    r"\bit is likely\b", r"\bmay be identified\b", r"\bconjectur\w*", r"\bspeculat\w*",
    r"\bnot (?:unlikely|impossible)\b", r"\bapparently\b", r"\bsupposedly\b",
    r"\bpurportedly\b", r"\bdoubtful\b", r"\buncertain\b",
    r"शायद", r"संभवतः?", r"लगता है", r"प्रतीत होता")

# A conclusion drawn from evidence.
INFER = rx(
    # bare "thus" is usually "in this way" ("thus is the one named...",
    # "when I was told thus"); only sentence-initial "Thus," concludes.
    r"\b(?:therefore|hence|consequently|accordingly)\b", r"(?:^|[.;]\s*)Thus,",
    r"\bit (?:follows|is evident|is clear|is obvious)\b",
    r"\bit (?:can|may) (?:fairly )?be (?:inferred|concluded|gathered|presumed|seen)\b",
    # "it shows" alone is too loose ("Much of it shows in the ruins").
    r"\b(?:this|these|which) (?:shows?|proves?|indicates?|suggests?|implies|demonstrates?|establishes?)\b",
    r"\bit (?:shows|proves|indicates|suggests|implies|demonstrates|establishes) that\b",
    r"\b(?:indicates?|suggests?|implies) that\b", r"\bmust have \w+\b",
    r"\bwe (?:may|can|must) (?:infer|conclude|assume|presume)\b", r"\bevidently\b",
    r"\bon the (?:basis|strength|evidence) of\b", r"\bin (?:the )?light of\b",
    r"\bleads? (?:us )?to (?:believe|conclude|infer)\b", r"\bpoints? to\b",
    r"\bfrom (?:this|these|the above|the evidence)\b", r"\bbecause\b",
    r"\bइससे (?:स्पष्ट|पता)", r"\bअतः\b")

# Nouns that anchor a hedge in evidence.
EVIDENCE = rx(
    r"\binscriptions?\b", r"\bepigraph\w*", r"\bgrants?\b", r"\bcopper.?plates?\b",
    r"\brecords?\b", r"\bevidence\b", r"\bdata\b", r"\bsurvey\w*\b", r"\bexcavat\w*",
    r"\bcoins?\b", r"\bpra[sś]asti\b", r"\bchronicles?\b", r"\bcolophon\b",
    r"\bremains\b", r"\bplates?\b", r"\bmanuscripts?\b")

# Citation apparatus anywhere in the chunk = traceable support.
CITATION = rx(
    r"\bE\.\s?I\.", r"\bI\.\s?A\.", r"\bJ\.\s?A\.\s?S\.\s?B", r"\bA\.\s?S\.\s?I\.",
    r"\bVol\.\s?[IVXLC\d]", r"\bpp?\.\s?\d", r"\bIbid\b", r"\bop\.\s?cit\b", r"\bcf\.?\s",
    r"[a-zĀ-ſ][.,;:)]?\*(?:\s|$)", r"\^\d",   # footnote markers: "Yadava king.*", "dcad.^"
    r"[¹²³⁴⁵⁶⁷⁸⁹⁰]", r"\$\^\{?\d", r"\[\d{1,3}\]", r"\(\w[\w\s.&]+,? (?:19|20)\d{2}\)")

# Firsthand fieldwork — valid in ANY source.
FIELDWORK = rx(
    r"\b(?:I|we) (?:saw|noticed|observed|visited|reached|walked|climbed|photographed|measured|surveyed|documented|met|went|entered|stood|stopped|interacted|found (?:that|a|an|the|several|many))\b",
    r"\b(?:our|my) (?:team|visit|survey|fieldwork|field work|walk|heritage walk|journey|trip)\b",
    r"\bduring (?:our|my|the author's|the) (?:visit|survey|field ?work|documentation|walk)\b",
    r"\bauthor's field survey\b", r"\bdrone\b", r"\btotal station\b",
    r"\bहमने\b", r"\bमैंने\b", r"\bहम (?:गए|पहुंचे|पहुँचे)")

# Present-condition / on-site description — observation ONLY in a field source.
ONSITE = rx(
    r"\b(?:is|are) (?:now|still|presently|currently)\b", r"\bat present\b",
    r"\bpresent (?:condition|state)\b", r"\bin (?:a )?(?:dilapidated|ruinous|ruined|poor|fair|good|bad) (?:condition|state)\b",
    r"\bGPS\b", r"\b\d{1,2}\.\d{2}\.?\d*\s?[NE]\b", r"\btoday\b",
    r"\b(?:is|are) (?:situated|located|lying|visible|seen|found)\b",
    r"\b(?:is|are) (?:made|built|constructed|decorated|carved|surrounded) (?:of|with|by)\b",
    r"\b(?:I|we|me|my|our|us)\b", r"\bआज\b", r"\bअब\b",
    r"मैं", r"हमें", r"मुझे", r"हमारे?", r"वर्तमान में", r"आज भी",
    # present-tense description of a physical feature, in a field source
    r"\b(?:is|are|has|have|can be seen|lies|stands?)\b[^.]{0,80}\b(?:walls?|pillars?|images?|"
    r"sculptures?|idols?|carvings?|structures?|doors?|doorways?|roofs?|shrines?|steps?|tanks?|"
    r"stepwell|baoli|gates?|stones?|platforms?|domes?|arches|niches?|plinth|mandapa|"
    r"garbhagriha|sikhara|temple|mosque|fort|hill|village|houses?|lanes?)\b")

FOLKLORE = rx(
    r"\blegends?\b", r"\bfolklore\b", r"\bfolk ?(?:tale|story|lore|songs?)\b",
    r"\btradition has it\b", r"\baccording to (?:the )?(?:local|popular) (?:belief|tradition|legend|people|villagers)\b",
    r"\b(?:locals|villagers|local people|the elders) (?:believe|say|recall|told)\b",
    r"\bas per (?:the )?local\b", r"\bmyths?\b", r"\bstory goes\b",
    r"\boral (?:history|tradition)\b", r"\bit is said that\b",
    r"\b(?:they|people|the old(?:er)? (?:people|residents)) (?:relate|narrate|recount|tell)\b",
    r"किंवदंती", r"लोककथा", r"जनश्रुति", r"कहा जाता है", r"मान्यता")

OPINION = rx(
    # Normative recommendations about the present. Bare "should be" is left to
    # DEONTIC: in a sastra or its translation ("the deity should be shown with
    # four faces") it prescribes form, it does not express the author's view.
    r"\b(?:should|must|ought to|needs? to) (?:not )?(?:be )?(?:protect|declar|develop|preserv|conserv|"
    r"restor|sav|remov|promot|encourag|stop|ensur|begin|revive|repair|clean|notif|includ|recogni[sz])\w*\b",
    r"\bshould not be at all\b", r"\b(?:the )?(?:government|administration|authorities|society) (?:should|must)\b",
    r"\bwe (?:recommend|suggest|propose|urge|demand|request)\b",
    r"\bit is (?:necessary|essential|imperative|high time|a shame|unfortunate|sad|regrettable)\b",
    r"\b(?:shameful|disgrace\w*|tragic|pathetic)\b", r"चाहिए")

DEONTIC = rx(
    r"\b(?:may|should|must|shall|is to|are to|ought to) be (?:made|built|constructed|placed|created|elevated|equipped|fixed|provided|of|divided|set|laid|given|raised|erected|carved|kept|done|adorned|endowed)\b",
    r"\bdeserves? to be\b", r"\b(?:is|are) to be\b")

FACTUAL_CUE = rx(
    r"\b(?:records?|recorded|states?|stated|mentions?|mentioned|dated|founded|built|constructed|erected|consecrated|issued|granted|ruled|reigned|died|defeated|captured|annexed)\b",
    r"\b(?:V\.?\s?S\.?|Sam(?:vat)?\.?|[SŚ]aka|A\.?\s?D\.?|C\.?E\.?|B\.?C\.?|A\.?H\.?)\s*\d{3,4}\b",
    r"\b\d{3,4}\s*(?:A\.?\s?D\.?|C\.?E\.?|B\.?C\.?E?)\b")

MEDIEVAL = rx(r"\b(?:Paramāra|Paramara|Parmar|Bhoja|Bhoj|Udayāditya|Udayaditya|Munja|Muñja|Sīyaka|Siyaka|Naravarman|Jayasi[mṃ]ha)\b",
              r"\b(?:[5-9]\d{2}|1[0-7]\d{2})\s*(?:A\.?\s?D\.?|C\.?E\.?)", r"परमार", r"भोज", r"उदयादित्य",
              r"\b(?:in|of|by|year) (?:[5-9]\d{2}|1[0-8]\d{2})\b", r"\b(?:Mughal|Babur|Akbar|Aurangzeb|Iltutmish|"
              r"Tughlu[qk]|Sultan|Mandu|Malwa Sultanate|Scindia|Sindhia|Gwalior State|Maratha)\w*")

APPARATUS_TRAIL = re.compile(
    r"^\W*(?:\d+(?:\.\d+)*\s+)?(?:PRIMARY |SECONDARY )?"
    r"(?:INDEX|CONTENTS|TABLE OF CONTENTS|BIBLIOGRAPHY|REFERENCES|WORKS CITED|ABBREVIATIONS|"
    r"LIST OF (?:ILLUSTRATIONS|PLATES|FIGURES|MAPS)|NOTES AND REFERENCES|SOURCES|"
    r"PUBLISHED BOOKS?|RESEARCH PAPERS?)\W*$", re.I)


def apparatus_heading(trail: str) -> bool:
    """Only the innermost heading counts: an earlier version matched any
    ancestor, so every section after 'PRIMARY SOURCES' in Pande was filed as
    apparatus. Index letter sections ('INDEX > J') are the one exception."""
    parts = [t for t in (trail or "").split(" > ") if t]
    if not parts:
        return False
    if APPARATUS_TRAIL.search(parts[-1]):
        return True
    return len(parts[-1]) <= 3 and len(parts) > 1 and bool(APPARATUS_TRAIL.search(parts[-2]))
INDEX_LINE = re.compile(r"\b\d{1,3}(?:[-–]\d{1,3})?(?:, \d{1,3}(?:[-–]\d{1,3})?){1,}")
REF_LINE = re.compile(r"\b(?:19|20)\d{2}[a-z]?\.\s|\bpp?\.\s?\d|\bVol\.\s?\w|\bed(?:s)?\.\s")
GARBAGE = set("~^{}¾¼½@$%|\\")
DEVA = re.compile(r"[ऀ-ॿ]")
LLM_CITE = re.compile(r"\[cite:\s*\d")

ABBR = {"e.g.", "i.e.", "etc.", "viz.", "cf.", "dr.", "mr.", "mrs.", "prof.", "st.", "vol.",
        "vols.", "no.", "nos.", "pp.", "p.", "fig.", "figs.", "pl.", "pls.", "ch.", "ed.",
        "eds.", "a.d.", "b.c.", "v.s.", "c.e.", "sam.", "skt.", "ibid.", "op.", "cit.",
        "sh.", "smt.", "shri.", "ltd.", "co.", "jr.", "sr.", "vs.", "approx.", "ca."}


def split_sentences(text: str) -> list[str]:
    # Sentence ends, plus a line break before a list item ("\n2. ", "\n- ").
    parts = re.split(r"(?<=[.!?।॥])\s+|\n(?=\s*(?:\d{1,3}[.)]|[-*•])\s)", text.strip())
    out: list[str] = []
    for p in parts:
        if not p:
            continue
        if out:
            prev = out[-1]
            last = prev.split()[-1].lower() if prev.split() else ""
            if (last in ABBR or re.search(r"(?:^|\s)[A-Z]\.$", prev)
                    or re.search(r"\b\d{1,3}\.$", prev) or p[:1].islower()):
                out[-1] = prev + " " + p
                continue
        out.append(p)
    return out


def label_sentence(s: str, field: bool) -> tuple[str, list[str], set[str]]:
    """-> (status, cues, tags). Status here is provisional; the chunk may
    upgrade an unanchored hedge to inference if it carries citations."""
    cues: list[str] = []
    tags: set[str] = set()

    def hits(pat, name):
        found = [m.group(0) for m in pat.finditer(s)][:3]
        for f in found:
            cues.append(f"{name}:{f.strip()[:40]}")
        return bool(found)

    folk = hits(FOLKLORE, "folklore")
    opin = hits(OPINION, "opinion")
    deon = hits(DEONTIC, "deontic")
    hedge = hits(HEDGE, "hedge")
    infer = hits(INFER, "infer")
    evid = hits(EVIDENCE, "evidence") if (hedge or infer) else False
    fwork = hits(FIELDWORK, "fieldwork")
    onsite = hits(ONSITE, "onsite") if field else False
    hits(FACTUAL_CUE, "factual")

    if folk:
        tags.add("folklore")
    if opin:
        tags.add("opinion")
    if deon:
        tags.add("prescriptive")

    if folk:
        cues.append("rule:folklore-report (never speculation)")
        return ("observation" if field else "factual"), cues, tags
    if hedge and (infer or evid):
        cues.append("rule:hedge anchored in evidence -> inference")
        return "inference", cues, tags
    if hedge:
        cues.append("rule:unanchored hedge -> speculation (provisional)")
        return "speculation", cues, tags
    # A recommendation ("...and hence needs to be conserved") is a view about
    # what to do, not a conclusion about what was: the opinion tag carries it,
    # and a reasoning connector inside it does not make it an inference.
    if opin:
        if field:
            cues.append("rule:firsthand opinion in field source -> observation")
            return "observation", cues, tags
        cues.append("rule:normative judgement -> inference")
        return "inference", cues, tags
    if infer:
        cues.append("rule:reasoning connector -> inference")
        return "inference", cues, tags
    if fwork or (field and onsite):
        cues.append("rule:firsthand/on-site reporting -> observation")
        return "observation", cues, tags
    cues.append("rule:assertive declarative, no hedge -> factual")
    return "factual", cues, tags


CERTAIN = {"factual", "observation"}


def group_of(status):
    return "certain" if status in CERTAIN else "uncertain"


# --------------------------------------------------------------------------
# Parsing a source into blocks with provenance
# --------------------------------------------------------------------------
def parse_blocks(text: str, prelog: list, source_id: str):
    """Yield dicts: kind, text, trail, page, page_kind, start, end."""
    trail: list[str] = []
    page, page_kind = None, None
    buf: list[str] = []
    buf_start = None
    kind = "para"
    in_fence = False
    pos = 0

    def flush(end):
        nonlocal buf, buf_start, kind
        body = "\n".join(buf).strip()
        if body:
            yield_blocks.append({"kind": kind, "text": body, "trail": " > ".join(trail),
                                 "page": page, "page_kind": page_kind,
                                 "start": buf_start, "end": end})
        buf, buf_start, kind = [], None, "para"

    yield_blocks: list[dict] = []
    # Running headers/footers: short non-heading lines repeated many times in
    # one source ("THE HINDU TEMPLE", "Author's personal copy").
    freq = collections.Counter(l.strip().strip("*# ") for l in text.splitlines()
                               if 0 < len(l.strip()) <= 60 and not l.lstrip().startswith(("#", "|")))
    running = {k for k, v in freq.items() if v >= 6 and len(k) >= 3 and not k.startswith("```")}
    for line in text.splitlines(keepends=True):
        lstart, pos = pos, pos + len(line)
        raw = line.rstrip("\n")

        for prx, pk in PAGE_RX:
            m = prx.search(raw)
            if m:
                page, page_kind = int(m.group(1)), pk
                raw = prx.sub("", raw)
        if COMMENT_RX.search(raw):
            for m in COMMENT_RX.finditer(raw):
                prelog.append({"source_id": source_id, "char": lstart, "removed": "html_comment",
                               "text": m.group(0)[:160]})
            raw = COMMENT_RX.sub("", raw)
        if IMAGE_RX.search(raw):
            prelog.append({"source_id": source_id, "char": lstart, "removed": "image_ref",
                           "count": len(IMAGE_RX.findall(raw))})
            raw = IMAGE_RX.sub("", raw)
        if CHATTER_RX.search(raw):
            for m in CHATTER_RX.finditer(raw):
                prelog.append({"source_id": source_id, "char": lstart, "removed": "ocr_commentary",
                               "text": m.group(0).strip()[:200]})
            raw = CHATTER_RX.sub("", raw)

        stripped = raw.strip()
        rule_line = bool(re.fullmatch(r"[-*_=]{3,}", stripped))
        if rule_line or re.fullmatch(r"\d{1,4}", stripped) or (stripped and stripped.strip("*# ") in running):
            if not rule_line:
                prelog.append({"source_id": source_id, "char": lstart,
                               "removed": "page_furniture", "text": stripped[:80]})
            raw, stripped = "", ""
        if stripped.startswith("```"):
            if in_fence:
                buf.append(raw); in_fence = False; flush(pos)
            else:
                flush(lstart); in_fence = True; kind = "verse"
                buf_start = lstart; buf.append(raw)
            continue
        if in_fence:
            buf.append(raw); continue

        h = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if h:
            flush(lstart)
            level, title = len(h.group(1)), h.group(2).strip(" #*")
            if title:
                trail[:] = trail[: level - 1]
                trail.append(title[:120])
            continue
        if not stripped:
            flush(lstart); continue
        is_table = stripped.startswith("|")
        if buf and ((kind == "table") != is_table):
            flush(lstart)
        if not buf:
            buf_start = lstart
            kind = "table" if is_table else "para"
        buf.append(raw)
    flush(pos)
    return yield_blocks


def block_flags(b: dict) -> dict:
    t = b["text"]
    n = max(1, len(t))
    garbage = sum(1 for ch in t if ch in GARBAGE) / n
    letters = sum(1 for ch in t if ch.isalpha())
    idx = len(INDEX_LINE.findall(t)); refs = len(REF_LINE.findall(t))
    apparatus = None
    # Line-level test for long lists: an index ("Mat Industry 253") or a
    # numbered reference list ("2. J. H. 1910, p. 89"). The density test
    # above missed a 9,777-char footnote list in Adhikari.
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    app_lines = sum(1 for l in lines if len(l) < 110 and (
        re.search(r"[A-Za-z].*\s\d{1,3}(?:\s?[-–,]\s?\d{1,3})*\.?$", l) or REF_LINE.search(l)))
    if apparatus_heading(b["trail"]) or (idx >= 4 and idx * 60 > n) or (refs >= 5 and refs * 90 > n) \
            or (len(lines) >= 5 and app_lines / len(lines) >= 0.6):
        apparatus = "apparatus"
    return {"garbage": garbage, "letters": letters, "apparatus": apparatus,
            "deva_ratio": len(DEVA.findall(t)) / n}


# --------------------------------------------------------------------------
# Chunk assembly
# --------------------------------------------------------------------------
def make_chunks(blocks, reg, field):
    chunks = []
    cur = None

    def new_chunk(b):
        return {"sents": [], "text": [], "trail": b["trail"], "page_start": b["page"],
                "page_end": b["page"], "page_kind": b["page_kind"], "start": b["start"],
                "end": b["end"], "kinds": set(), "splits": 0}

    def close():
        nonlocal cur
        if cur and "".join(cur["text"]).strip():
            chunks.append(cur)
        cur = None

    for b in blocks:
        fl = block_flags(b)
        # Atomic blocks: tables, verse, apparatus, OCR garbage. Never mixed
        # with prose; split only at line boundaries when over MAX_CHARS
        # (Samarangana verse fences reach 75,000 chars).
        garbage = fl["garbage"] > 0.12 and fl["letters"] >= 25
        if b["kind"] in ("table", "verse") or fl["apparatus"] or garbage:
            close()
            kind = "apparatus" if fl["apparatus"] else "ocr_garbage" if garbage else b["kind"]
            lines = b["text"].split("\n")
            header = lines[:2] if b["kind"] == "table" and len(lines) > 2 and "---" in lines[1] else []
            pieces, piece = [], []
            for ln in lines[len(header):]:
                if piece and sum(len(x) + 1 for x in header + piece) + len(ln) > MAX_CHARS:
                    pieces.append(piece); piece = []
                piece.append(ln)
            if piece:
                pieces.append(piece)
            for k, pc in enumerate(pieces):
                c = new_chunk(b)
                body = "\n".join(header + pc)
                c["text"].append(body); c["kinds"].add(b["kind"])
                c["atomic"] = kind
                c["part"] = f"{k + 1}/{len(pieces)}" if len(pieces) > 1 else None
                c["sents"] = [(body, ("factual", [f"rule:atomic {kind} block"], set()))]
                chunks.append(c)
            continue

        if cur and (cur["trail"] != b["trail"]):
            close()
        if cur and sum(len(x) for x in cur["text"]) >= MIN_CHARS:
            close()
        if cur is None:
            cur = new_chunk(b)
        else:
            cur["end"] = b["end"]; cur["page_end"] = b["page"] or cur["page_end"]

        for s in split_sentences(b["text"]):
            lab = label_sentence(s, field)
            size = sum(len(x) for x in cur["text"])
            crossing = (cur["sents"] and group_of(lab[0]) != group_of(cur["sents"][-1][1][0])
                        and len(s) >= MIN_SPLIT and size >= MIN_SPLIT)
            if (size + len(s) > MAX_CHARS and size >= MIN_CHARS) or crossing or size >= TARGET and s[:1].isupper() and size + len(s) > TARGET + 400:
                if crossing:
                    cur["splits"] += 1
                close()
                cur = new_chunk(b)
            cur["sents"].append((s, lab))
            cur["text"].append(s)
            cur["kinds"].add(b["kind"])
    close()
    return merge_slivers(chunks)


def merge_slivers(chunks):
    """Fold prose slivers (< MIN_SPLIT chars: captions, one-line paragraphs
    between headings, figure labels) into the preceding prose chunk, or the
    following one when there is none. Status-change splits are never slivers:
    they require >= MIN_SPLIT on both sides."""
    out = []
    pending = None                                    # sliver awaiting a host
    for c in chunks:
        prose = c.get("atomic") is None
        size = sum(len(x) for x in c["text"])
        if prose and size < MIN_SPLIT:
            host = out[-1] if out and out[-1].get("atomic") is None else None
            if host and sum(len(x) for x in host["text"]) + size <= MAX_CHARS:
                host["text"] += c["text"]; host["sents"] += c["sents"]
                host["end"] = c["end"]; host["page_end"] = c["page_end"] or host["page_end"]
                host.setdefault("absorbed_trails", []).append(c["trail"])
            elif pending:
                pending["text"] += c["text"]; pending["sents"] += c["sents"]; pending["end"] = c["end"]
            else:
                pending = c
            continue
        if pending:
            if prose:
                c["text"] = pending["text"] + c["text"]; c["sents"] = pending["sents"] + c["sents"]
                c["start"] = pending["start"]; c["page_start"] = pending["page_start"] or c["page_start"]
                c.setdefault("absorbed_trails", []).append(pending["trail"])
            else:
                out.append(pending)
            pending = None
        out.append(c)
    if pending:
        out.append(pending)
    return out


def finalise(c, reg, field, idx):
    text = " ".join(c["text"]).strip() if c.get("atomic") is None else c["text"][0].strip()
    has_cite = bool(CITATION.search(text))
    weights = collections.Counter()
    sent_log = []
    tags: set[str] = set()
    adjustments = []
    for i, (s, (status, cues, stags)) in enumerate(c["sents"]):
        if status == "speculation" and has_cite:
            status = "inference"
            cues = cues + ["chunk:hedge anchored by citation apparatus in chunk -> inference"]
            adjustments.append(f"s{i}: speculation->inference (citations present)")
        weights[status] += len(s)
        tags |= stags
        sent_log.append({"i": i, "status": status, "cues": cues[:8]})

    atomic = c.get("atomic")
    claim_bearing = atomic not in ("apparatus", "ocr_garbage", "fragment")
    # Uncertain language wins once it is a material share of the chunk (>= 1/3
    # of characters): a short "it can be inferred that..." that carries the
    # passage's actual claim must not be outvoted by the lines that set it up.
    # Shorter asides are recorded as mixed_status with their share.
    total_w = sum(weights.values()) or 1
    if weights.get("speculation", 0) / total_w >= 1 / 3:
        status = "speculation"
    elif (weights.get("speculation", 0) + weights.get("inference", 0)) / total_w >= 1 / 3:
        status = "inference"
    elif weights:
        status = "observation" if weights.get("observation", 0) >= weights.get("factual", 0) else "factual"
    else:
        status = "factual"
    # Firsthand frame. In a field source, a passage that is all certain
    # language, contains at least one firsthand/on-site sentence and no
    # pre-modern history is the author reporting what they saw and heard on
    # the visit: the third-person sentences around "we went" are part of the
    # same report, so the whole chunk is observation.
    if (field and status == "factual" and weights.get("observation")
            and set(weights) <= CERTAIN and not MEDIEVAL.search(text)):
        status = "observation"
        adjustments.append("chunk: firsthand frame in field source, no pre-modern history -> observation")
    total = sum(weights.values()) or 1
    spec_share = weights.get("speculation", 0) / total
    inf_share = weights.get("inference", 0) / total
    mixed = len([k for k, v in weights.items() if v > 0]) > 1

    if LLM_CITE.search(text):
        tags.add("llm_regenerated")
    coarse = reg.get("source_type_coarse", reg["source_type"])
    if DEVA.search(text) and (atomic == "verse" or len(DEVA.findall(text)) / max(1, len(text)) > 0.4):
        tags.add("embeds_primary_text" if coarse != "primary" else "original_script")
    if "│" in text or sum(1 for ch in text if ch in GARBAGE) / max(1, len(text)) > 0.03:
        tags.add("ocr_damaged")
    if coarse == "contextual_background":
        tags.add("contextual")
    if reg.get("register") == "scriptural":
        tags.add("scriptural_register")
    if field and status == "factual" and MEDIEVAL.search(text):
        tags.add("secondhand_history")
    if atomic:
        tags.add(f"content_kind:{atomic}")

    rule = ("atomic block (non-claim)" if not claim_bearing else
            "char-weighted sentence statuses: speculation if >=1/3; inference if speculation+inference >=1/3; else observation vs factual majority")
    cid = f"{reg['source_id']}-{idx:05d}"
    rec = {
        "chunk_id": cid,
        "parent_source_id": reg["source_id"],
        "work_id": reg.get("work_id"),
        "source_type": reg["source_type"],
        "epistemic_status": status,
        "claim_bearing": claim_bearing,
        "mixed_status": mixed,
        "speculation_share": round(spec_share, 3),
        "inference_share": round(inf_share, 3),
        "tags": sorted(tags),
        "provenance": {
            "file": reg["file"], "title": reg.get("title"), "author": reg.get("author"),
            "publication_date": reg.get("publication_date"),
            "date_confidence": reg.get("date_confidence"),
            "heading_trail": c["trail"], "page_start": c["page_start"], "page_end": c["page_end"],
            "page_kind": c["page_kind"], "char_start": c["start"], "char_end": c["end"],
            "block_part": c.get("part"), "absorbed_heading_trails": c.get("absorbed_trails") or [],
        },
        "cues": sorted({cue for e in sent_log for cue in e["cues"] if not cue.startswith("rule:")})[:15],
        "text": text,
        "content_hash": hashlib.sha1(text.encode("utf-8")).hexdigest()[:16],
        "n_sentences": len(c["sents"]),
        "n_chars": len(text),
    }
    log = {"chunk_id": cid, "epistemic_status": status, "decision_rule": rule,
           "status_weights": dict(weights), "sentence_labels": sent_log,
           "chunk_adjustments": adjustments, "status_splits_in_paragraph": c["splits"],
           "tags": sorted(tags)}
    return rec, log


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--suffix", default="", help="write to classified_inventory<suffix>.jsonl etc (keeps the main inventory intact)")
    args = ap.parse_args(argv)

    reg_all = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["sources"]
    if args.only:
        reg_all = [r for r in reg_all if r["source_id"] == args.only]
    OUT.mkdir(exist_ok=True)
    inv = open(OUT / f"classified_inventory{args.suffix}.jsonl", "w", encoding="utf-8")
    clog = open(OUT / f"classification_log{args.suffix}.jsonl", "w", encoding="utf-8")
    plog = open(OUT / f"preprocessing_log{args.suffix}.jsonl", "w", encoding="utf-8")
    tally = collections.Counter(); per_src = collections.Counter(); splits = 0
    t0 = dt.datetime.now()
    for reg in reg_all:
        path = REF / reg["file"]
        if not path.exists():
            print(f"  !! missing on disk: {reg['file']}")
            continue
        text = unicodedata.normalize("NFC", path.read_text(encoding="utf-8", errors="replace"))
        coarse = reg.get("source_type_coarse", reg["source_type"])
        field = coarse == "field_observation"
        prelog: list = []
        blocks = parse_blocks(text, prelog, reg["source_id"])
        chunks = make_chunks(blocks, reg, field)
        for p in prelog:
            plog.write(json.dumps(p, ensure_ascii=False) + "\n")
        n = 0
        for i, c in enumerate(chunks):
            rec, log = finalise(c, reg, field, i)
            if not rec["text"]:
                continue
            inv.write(json.dumps(rec, ensure_ascii=False) + "\n")
            clog.write(json.dumps(log, ensure_ascii=False) + "\n")
            tally[(rec["source_type"], rec["epistemic_status"])] += 1
            splits += log["status_splits_in_paragraph"]
            n += 1
        per_src[reg["source_id"]] = n
        chatter = sum(1 for p in prelog if p["removed"] == "ocr_commentary")
        print(f"  {reg['source_id']:32s} {n:>6} chunks   ocr-commentary stripped: {chatter}")
    inv.close(); clog.close(); plog.close()
    secs = (dt.datetime.now() - t0).total_seconds()
    run = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "stage": "1B-classify",
           "version": VERSION, "params": {"target": TARGET, "max": MAX_CHARS, "min": MIN_CHARS,
           "min_split": MIN_SPLIT}, "registry_sha1": hashlib.sha1(REGISTRY.read_bytes()).hexdigest()[:12],
           "sources": dict(per_src), "chunks": sum(per_src.values()),
           "status_splits": splits, "seconds": round(secs, 1)}
    with open(OUT / "audit_log.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(run, ensure_ascii=False) + "\n")
    print(f"\n{sum(per_src.values()):,} chunks from {len(per_src)} sources in {secs:.0f}s "
          f"| paragraph splits at status change: {splits}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
