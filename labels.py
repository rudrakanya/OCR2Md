#!/usr/bin/env python3
"""
labels.py — the labeling taxonomy and the deterministic validators behind it.

Everything the knowledge base holds arrives as undifferentiated prose. A page of
Cunningham's measured survey, a table of contents, a Sanskrit verse with its
translation, a plate caption and a bibliography entry are all just "text" once
they have been chunked, and retrieval treats them alike. That is wrong in a way
that costs the manuscript: a sub-topic asking for inscriptional evidence should
be able to ask for inscriptions, and no sub-topic should ever be answered from
an index page.

Three orthogonal label sets, because they answer different questions:

    structural     WHAT KIND OF PAGE ELEMENT is this?
                   Taxonomy adopted verbatim from Baidu's Unlimited-OCR
                   (github.com/baidu/Unlimited-OCR), whose document-parsing
                   model emits <|det|>type [bbox]<|/det|> spans over exactly
                   these categories. Using its vocabulary rather than inventing
                   one means a future GPU ingest can populate these labels
                   directly, with no schema migration.

    content        WHAT KIND OF EVIDENCE does it carry, for THIS corpus?
                   Corpus-specific and the reason the layer earns its keep:
                   inscription, measurement, chronology, iconography, oral
                   testimony, hydrology, and so on.

    evidence_role  HOW MAY IT BE USED? A measured dimension, a translated verse
                   and a modern scholar's inference are all "true" and must be
                   written differently. This is the axis the drafting prompt
                   most needs and never had.

On Unlimited-OCR specifically
----------------------------
Its model is a vision-language model requiring torch 2.10 and a GPU. This
machine reports `torch 2.13.0+cpu, CUDA: False`, and a 568M cross-encoder
already measured 3.2 s/pair here, so running a multi-billion-parameter VLM
locally is not viable. The taxonomy is therefore adopted as the *interface*:
`parse_det_markers()` reads its output when it exists, and `classify_structural()`
derives the same labels from markdown shape when it does not. Both write the
same values, so a later re-ingest upgrades label quality without changing
anything downstream.

    from labels import classify_structural, validate_chunk, STRUCTURAL
    structural = classify_structural(chunk)
    quality, issues = validate_chunk(chunk)
"""
import hashlib
import re
from collections import Counter

from textnorm import DEVANAGARI_RE, WORD_RE, has_devanagari

# ---------------------------------------------------------------------------
# Structural taxonomy — Unlimited-OCR's <|det|> types, unchanged.
# ---------------------------------------------------------------------------
STRUCTURAL = (
    "title",      # a heading of any level
    "text",       # ordinary running prose — the default
    "list",       # enumerated or bulleted
    "table",      # tabular data
    "figure",     # a figure/plate region
    "caption",    # the label attached to a figure, plate or table
    "formula",    # displayed mathematics or a measured formula
    "header",     # running head
    "footer",     # running foot, folio
    "image",      # an image with no recoverable text
    # Observed in Unlimited-OCR's actual output on this corpus but absent from
    # its documented type list — it emits `page_number` as a category distinct
    # from `footer`. Recorded here so a real label is never silently coerced to
    # "text" by the membership test in elements_from_raw().
    "page_number",
)

# Not in Unlimited-OCR's vocabulary, but unavoidable in scanned scholarly books
# and exactly the material that must never answer a research question.
EXTRA_STRUCTURAL = (
    "toc",           # table of contents / list of plates
    "index",         # back-of-book index
    "bibliography",  # reference list
    "footnote",      # apparatus at the foot of the page
)

ALL_STRUCTURAL = STRUCTURAL + EXTRA_STRUCTURAL

# ---------------------------------------------------------------------------
# Content taxonomy — what kind of evidence, for THIS corpus.
# ---------------------------------------------------------------------------
CONTENT = {
    "inscription": "the text of an inscription, its edition, reading or translation",
    "sanskrit_text": "a Sanskrit or Prakrit passage, verse, or śāstric prescription",
    "translation": "a rendering of a source text into English or Hindi",
    "measurement": "dimensions, counts, distances, heights, areas, survey figures",
    "chronology": "dates, regnal years, saṃvat/CE equivalences, dynastic sequence",
    "architecture": "plan, elevation, śikhara type, mouldings, structural description",
    "iconography": "deities, attributes, sculptural programme, identification of figures",
    "epigraphy_meta": "discussion of an inscription's script, palaeography or discovery",
    "political_history": "reigns, wars, succession, administration, land grants",
    "religion_ritual": "cult, worship, festivals, patronage, sectarian affiliation",
    "economy": "trade, crafts, guilds, revenue, endowments, agriculture",
    "society": "caste, community, demography, custom, daily life",
    "geography_hydrology": "rivers, terrain, climate, streamflow, settlement pattern",
    "oral_testimony": "local memory, tradition, present-day informants",
    "conservation": "condition, damage, restoration, protection, present state",
    "historiography": "what previous scholars argued; debate, attribution, revision",
    "apparatus": "bibliography, index, contents, abbreviations, plate lists",
}

# ---------------------------------------------------------------------------
# Evidence role — how the drafter may use it.
# ---------------------------------------------------------------------------
EVIDENCE_ROLES = {
    "primary_witness": "the historical object itself: an inscription's text, a "
                       "śāstric prescription, a testimony recorded from a resident",
    "observation": "something the author measured, surveyed or saw directly",
    "interpretation": "a modern scholar's reading, inference or argument",
    "restatement": "a summary of what another source says",
    "apparatus": "bibliography, index, contents — never evidence for anything",
}

# ---------------------------------------------------------------------------
# Structural classification without a GPU.
# ---------------------------------------------------------------------------
_DET_RE = re.compile(r"<\|det\|>\s*([a-z_]+)\s*(\[[^\]]*\])?\s*<\|/det\|>", re.I)
# Left behind by ocr_layout.elements_to_markdown so the label survives
# markdown rendering and chunking.
_ELEMENT_RE = re.compile(r"<!--\s*element:([a-z_]+)\s*-->", re.I)

_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_LIST_RE = re.compile(r"^\s*(?:[-*+•]|\(?[0-9ivxIVX]{1,4}[.)])\s+\S")
_CAPTION_RE = re.compile(
    r"^\s*(?:fig(?:ure)?|plate|pl|table|tab|map|diagram|photo|illus)\.?\s*"
    r"(?:[0-9IVXLC]+|[A-Z])\b", re.I)
_FOOTNOTE_RE = re.compile(r"^\s*(?:\[?\d{1,3}\]?[.)]\s+|\*+\s+)(?=[A-Z\"'])")
_BIB_RE = re.compile(
    r"(?:\b\d{4}\b.*\bpp?\.\s*\d|\bed\.\b|\btrans\.\b|\bvol\.\s*[IVXL0-9]|"
    r"\bJournal\b|\bPress\b|\bcf\.\s|\bibid\b|\bop\.\s*cit)", re.I)
_TOC_RE = re.compile(r"\.{4,}\s*\d{1,4}\s*$|…{2,}\s*\d{1,4}\s*$", re.M)
_INDEX_RE = re.compile(r"^\s*[A-ZĀĪŪŚṢṆṬḌÑṚ][\w’'-]+(?:,\s*[\w’'-]+)*,\s*\d{1,4}"
                       r"(?:\s*[,-]\s*\d{1,4})*\s*$")
_FORMULA_RE = re.compile(r"\$[^$]{2,}\$|\\frac|\\sum|\\times|=\s*\d+(?:\.\d+)?\s*[×x]\s*\d")


_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _running_prose(text, min_long=2, long_words=18):
    """Does this read as continuous prose rather than a list of entries?

    A bibliography entry is a noun phrase with punctuation; a sentence of
    argument runs on. Two sentences of 18+ words is enough to say this is
    somebody writing, not somebody listing.
    """
    longs = 0
    for s in _SENT_SPLIT_RE.split(text):
        if len(s.split()) >= long_words and not s.lstrip().startswith(("|", "-", "*")):
            longs += 1
            if longs >= min_long:
                return True
    return False


def parse_det_markers(text):
    """Extract Unlimited-OCR <|det|> spans, if the text carries any.

    Returns [(type, bbox_or_None, span_text)]. Empty when the source was not
    parsed by a layout model — which is the normal case for this corpus, whose
    markdown came from Mistral OCR.
    """
    out = []
    matches = list(_DET_RE.finditer(text or ""))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((m.group(1).lower(), m.group(2), text[m.end():end].strip()))
    return out


def classify_structural(chunk):
    """Best structural label for a chunk, from markdown shape.

    Deliberately conservative: 'text' is the default and everything else has to
    be earned, because mislabelling prose as apparatus would hide real evidence
    from retrieval — a far worse error than letting an index page through, which
    the quality score catches separately.
    """
    text = (chunk.get("text") if isinstance(chunk, dict) else str(chunk)) or ""
    trail = (chunk.get("trail", "") if isinstance(chunk, dict) else "") or ""
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return "image"

    det = parse_det_markers(text)
    if det:
        # A layout model has already decided; trust it, taking the type that
        # covers the most characters.
        weigh = Counter()
        for t, _bbox, body in det:
            weigh[t] += len(body)
        return weigh.most_common(1)[0][0]

    # ocr_layout.py renders <|det|> spans to markdown and leaves the element
    # type behind as an HTML comment, so a chunk built from a re-ingested
    # source still carries the model's judgement even though the markers are
    # gone. An observed label always beats the heuristics below.
    obs = _ELEMENT_RE.findall(text)
    if obs:
        return Counter(t.lower() for t in obs).most_common(1)[0][0]

    # Apparatus first — these are the categories that must not answer questions,
    # so their tests have to be the strictest in the file. An apparatus label
    # excludes the chunk from retrieval outright, and there is no downstream
    # stage that can recover a passage the corpus has stopped containing.
    #
    # The keyword tests are POSITIONAL for exactly that reason. Matching
    # "contents" anywhere in the body labelled a Sanskrit technical glossary
    # from the Samarāṅgaṇasūtradhāra as a table of contents — on the phrase
    # "volume contents (kṣetraphala)" — and deleted it from the knowledge base.
    # A heading may announce apparatus; a sentence merely using the word may not.
    head = f"{trail}\n{lines[0]}".lower()
    body_low = text.lower()

    if _TOC_RE.search(text) or re.search(
            r"^\s*(?:table of\s+)?contents\s*$|\blist of (?:plates|figures|illustrations)\b",
            head, re.M):
        return "toc"
    # Scholarly prose is dense with citations — Kramrisch cites the Śilparatna
    # and the Īśānaśivagurudevapaddhati mid-argument — so a citation-per-line
    # count alone reads her chapters as a reference list and deletes them. A
    # reference list is made of ENTRIES, which are short and do not run on;
    # prose is made of sentences. Long sentences therefore veto the apparatus
    # labels outright.
    prose = _running_prose(text)

    idx_hits = sum(1 for l in lines if _INDEX_RE.match(l))
    if not prose and idx_hits >= max(3, len(lines) * 0.5):
        return "index"
    # 0.8 rather than 0.6, and at least five entries. Measured: at 0.6 the rule
    # was still the sole cause of every remaining false exclusion in the audit —
    # footnote-heavy pages of Kramrisch and the Paramāra temple survey read as
    # reference lists. A real bibliography is almost entirely entries.
    bib_hits = sum(1 for l in lines if _BIB_RE.search(l))
    if not prose and (bib_hits >= max(5, len(lines) * 0.8) or re.search(
            r"^\s*(?:select\s+)?(?:bibliography|references|works cited|abbreviations)\s*$",
            head, re.M)):
        return "bibliography"

    table_rows = sum(1 for l in lines if _TABLE_ROW_RE.match(l))
    if table_rows >= max(2, len(lines) * 0.5):
        return "table"
    list_rows = sum(1 for l in lines if _LIST_RE.match(l))
    if list_rows >= max(3, len(lines) * 0.6):
        return "list"
    # A caption is a LABEL, not a passage that happens to open with one. An
    # INTACH chunk beginning "Figure 25: Inscription installed in..." and then
    # describing that inscription at length is evidence about an inscription;
    # calling it a caption would be a lie about what the chunk contains.
    if _CAPTION_RE.match(lines[0]) and len(lines) <= 2 and len(text) < 300:
        return "caption"
    if len(lines) >= 3 and \
            sum(1 for l in lines if _FOOTNOTE_RE.match(l)) >= max(3, len(lines) * 0.6):
        return "footnote"
    if _FORMULA_RE.search(text) and len(text) < 600:
        return "formula"
    if len(lines) == 1 and len(text) < 120 and chunk.get("heading_level"):
        return "title"
    return "text"


# ---------------------------------------------------------------------------
# Validation — deterministic quality gates, no API calls.
# ---------------------------------------------------------------------------
# Explicit ranges rather than literal glyphs: IAST lives in Latin Extended-A
# (ā ī ū) and Latin Extended Additional (ṇ ṭ ḍ ṃ ḥ ś ṛ), which are far apart,
# and writing them as a literal span silently produced a reversed range.
_LATIN = r"A-Za-zÀ-ɏḀ-ỿ"
_DEVA = r"ऀ-ॿ"
_WORDISH_RE = re.compile(rf"[{_LATIN}{_DEVA}]")
_GARBLE_RE = re.compile(
    rf"[^\w\s.,;:!?'\"()\[\]/\-–—°%&$£₹×·•"
    rf"{_LATIN}{_DEVA}]")

# Structural categories that carry no answerable content, whatever their prose
# quality. They stay in the store — a bibliography is useful for citation
# checking — but must never be retrieved as evidence.
NON_EVIDENTIAL = {"toc", "index", "bibliography", "header", "footer",
                  "image", "page_number"}


def ocr_damage(text):
    """0 (clean) .. 1 (badly damaged). Cheap proxies, no model.

    Scanned scholarly books with diacritics OCR badly in characteristic ways:
    stray punctuation clusters, single-letter tokens where a word was broken,
    and runs of non-word characters. None of these is conclusive alone.
    """
    if not text:
        return 1.0
    toks = WORD_RE.findall(text)
    if not toks:
        return 1.0
    singles = sum(1 for t in toks if len(t) == 1)
    garble = len(_GARBLE_RE.findall(text))
    letters = len(_WORDISH_RE.findall(text))
    if letters < 20:
        return 0.9
    score = 0.0
    score += min(1.0, singles / max(len(toks), 1) / 0.25) * 0.45
    score += min(1.0, garble / max(letters, 1) / 0.08) * 0.35
    # Very long unbroken runs mean spaces were lost.
    longest = max((len(t) for t in toks), default=0)
    score += 0.20 if longest > 32 else 0.0
    return round(min(1.0, score), 3)


def shingle_hash(text, k=8):
    """A set of hashed word-shingles, for near-duplicate detection."""
    w = [t.lower() for t in WORD_RE.findall(text)]
    if len(w) < k:
        return set()
    return {hashlib.blake2b(" ".join(w[i:i + k]).encode("utf-8"),
                            digest_size=8).hexdigest()
            for i in range(0, len(w) - k + 1, 2)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def validate_chunk(chunk, structural=None):
    """(quality 0..1, issues[]) for one chunk.

    Quality is about whether the chunk can *support a claim*, not whether it is
    interesting. A pristine index page scores low; a slightly garbled paragraph
    of Cunningham's measurements scores high, because it still carries evidence.
    """
    text = (chunk.get("text") if isinstance(chunk, dict) else str(chunk)) or ""
    structural = structural or classify_structural(chunk)
    issues = []
    quality = 1.0

    # A table of wage figures is not damaged OCR merely because it contains no
    # sentences. Scoring it 1.0 excluded a perfectly good gazetteer table.
    damage = 0.0 if structural in ("table", "formula") else ocr_damage(text)
    if damage > 0.6:
        issues.append(f"ocr-damage:{damage}")
        quality -= 0.5
    elif damage > 0.35:
        issues.append(f"ocr-noise:{damage}")
        quality -= 0.2

    if structural in NON_EVIDENTIAL:
        issues.append(f"non-evidential:{structural}")
        quality -= 0.6

    words = len(WORD_RE.findall(text))
    if words < 40 and structural not in ("table", "formula"):
        issues.append(f"short:{words}w")
        quality -= 0.25

    # A chunk that is mostly digits and punctuation is a table fragment or an
    # index remnant; it retrieves on numerals and supports nothing.
    digits = sum(c.isdigit() for c in text)
    if len(text) and digits / len(text) > 0.25 and structural not in ("table", "formula"):
        issues.append("numeric-fragment")
        quality -= 0.3

    # Devanagari with no Latin at all is unreachable by an English query except
    # through the sparse Devanagari stream — worth knowing, not a defect.
    if has_devanagari(text) and not re.search(r"[A-Za-z]{3,}", text):
        issues.append("devanagari-only")

    # Starts mid-sentence AND ends mid-sentence: a chunk boundary landed badly.
    t = text.strip()
    if t and t[0].islower() and not t.endswith((".", "!", "?", '"', "”", ")", "]")):
        issues.append("fragment")
        quality -= 0.1

    return round(max(0.0, min(1.0, quality)), 3), issues


def is_retrievable(quality, issues, min_quality=0.45):
    """Should this chunk be allowed to answer a research question?"""
    if any(i.startswith("non-evidential") for i in issues):
        return False
    return quality >= min_quality


def summarise(labels):
    """Counts for a labeling report. `labels` is an iterable of label dicts."""
    out = {"structural": Counter(), "content": Counter(), "evidence_role": Counter(),
           "issues": Counter(), "n": 0, "retrievable": 0, "quality_sum": 0.0}
    for l in labels:
        out["n"] += 1
        out["structural"][l.get("structural", "?")] += 1
        out["evidence_role"][l.get("evidence_role", "?")] += 1
        for c in l.get("content") or []:
            out["content"][c] += 1
        for i in l.get("issues") or []:
            out["issues"][i.split(":")[0]] += 1
        out["quality_sum"] += float(l.get("quality") or 0)
        if l.get("retrievable"):
            out["retrievable"] += 1
    out["mean_quality"] = round(out["quality_sum"] / out["n"], 3) if out["n"] else 0.0
    return out
