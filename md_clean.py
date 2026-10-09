#!/usr/bin/env python3
"""
md_clean.py — strip OCR page furniture from Markdown before it is embedded.

The OCR'd reference books carry a layer of print-artefacts that mean nothing to a
retriever but occupy 20%+ of the corpus: page markers, image placeholders,
running heads repeated once per page, bare folio numbers, figure labels, photo
credits. Embedding them dilutes every vector they land in and, worse, feeds them
straight into the drafting model as if they were prose.

This module removes that layer while *preserving page provenance*: each surviving
line is returned tagged with the source page it came from, so a chunk can still
say "pages 193-195" even though the `<!-- page 193 -->` marker itself never
reaches the embedder.

Running heads are detected per file rather than hard-coded: a short, mostly
upper-case line that recurs five or more times is print furniture, not content.
Where such a line is also a Markdown heading, the first occurrence is kept (it is
usually the genuine section opening) and the repeats are dropped, so the heading
hierarchy survives intact.

    from md_clean import clean_lines
    for rec in clean_lines(text):
        rec["text"], rec["page"], rec["heading_level"]

Used by build_kb.py. Import-only; no side effects.
"""
import re
from collections import Counter

PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)[^>]*-->", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
# OCR renders footnote superscripts and ordinals as inline TeX; 1,800+ across
# the corpus, in forms like $^{17}$, $^{1)}$, $^{18-9}$, 3$^{rd}$. Only these
# reference-marker shapes are stripped, so real mathematics is left alone.
SUPERSCRIPT_RE = re.compile(r"\$\^\{?[\d)\-]{1,7}\}?\$|\$\^\{?(?:st|nd|rd|th)\}?\$")
HEADING_RE = re.compile(r"^(#{1,6})\s*(.*?)\s*#*$")
RULE_RE = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")

# Lines that are pure print furniture regardless of how often they recur.
FOLIO_RE = re.compile(r"^\d{1,4}$")
ROMAN_FOLIO_RE = re.compile(r"^[ivxlcdm]{1,7}$", re.I)
FIG_LABEL_RE = re.compile(r"^[A-Za-z]$|^[A-Za-z][.)]$|^\(?[a-z]\)$")
NONTEXT_RE = re.compile(r"^\[?non-?text\]?$", re.I)
# A credit line ("Photo © Gerard Foekema", "DRAWING SIZE:", a bare "plan") carries
# nothing retrievable. A CAPTION that happens to start with the same word does:
# the negative lookahead for " of " keeps "PLAN OF NĪLAKAṆṬHEŚVARA TEMPLE
# (1059—1080 A.D.)" — a dated caption for this book's own temple, which the
# earlier pattern dropped — along with "Plan of Vidisha, CGWB" and two Singh
# sentences that merely begin with the word "Drawing". The cost is that four
# "Courtesy ... Institute of Indian Studies" lines now survive; keeping a credit
# is cheaper than silently deleting a dated plan caption.
CREDIT_RE = re.compile(r"^(photo|photograph|drawing|plan|courtesy)\b(?![^\n]*\bof\b).{0,60}$", re.I)
EMPTY_QUOTE_RE = re.compile(r"^>+\s*$")
# The OCR'd page-scan note emitted by ocr_to_markdown.py for blank/plate pages.
OCR_EMPTY_RE = re.compile(r"No machine-readable text detected", re.I)

# The extraction model narrating its own OCR, written into the markdown as if it
# were the book. GUP and KRAM-1 carry 120 copies of lines like "The OCR has
# hallucinated text (underscores) where none should exist, violating the rule to
# ignore such lines. Hence, the OCR result is inconsistent with the Ground
# Truth." This is the same class of defect as ADH's leaked `box_2d` JSON: not a
# misreading of the page, but text the page never contained. It is dropped here
# rather than downstream so no rebuild can reintroduce it.
EXTRACTION_META_RE = re.compile(
    r"the OCR (?:has|is|result|output)\b"
    r"|OCR has hallucinated"
    r"|inconsistent with the Ground Truth"
    r"|the Ground Truth image (?:displays|shows)"
    r"|According to Rule \d"
    r"|UNDERSCORE & LINE RULES"
    r"|violating the rule to ignore"
    r"|\bbox_2d\b"
    r"|as an AI language model"
    r"|per the transcription instructions",
    re.I)

# CJK in a corpus of English, Hindi and Sanskrit books on Paramāra architecture
# is never the source. Measured across the 27 markdown files: 329 lines carry CJK
# and every one is model training-data leakage -- Chinese corporate boilerplate
# about a Shanghai bank and stock prices, in 8 books including Hardy, Kramrisch
# and Gupte. A fraction threshold let short rows through ("| 64 | 2014年1月64日 |
# 150 |" is only 11% CJK), so presence is the test. If this corpus ever gains a
# genuine CJK source, this rule has to become source-scoped.
CJK_RE = re.compile(r"[　-〿぀-ヿ一-鿿＀-￯]")


def _has_cjk(s):
    return bool(s) and bool(CJK_RE.search(s))


MIN_RUNHEAD_HITS = 5
MAX_RUNHEAD_LEN = 70
RUNHEAD_UPPER_RATIO = 0.6

# Photographing a bound book catches a vertical strip of the facing page at the
# edge of the frame. OCR dutifully transcribes that strip, which lands as a
# column of clipped word-ends below the real text:
#
#     es / n / is / it / ty / of / ts / va / te / nd
#
# One such line is indistinguishable from a real short word ("The", "has"), so
# they are only dropped in a RUN: four or more in a row, blank lines ignored,
# any other content breaking the run. Measured over the reference corpus that
# removes 26% of the lines of a photographed book and 0.1% elsewhere, and every
# sampled removal outside the photographed book was also OCR debris (figure-label
# columns, scan-edge noise). Runs of 1-3 are left alone: too close to prose.
SLIVER_FRAG_RE = re.compile(r"[A-Za-z']{1,4}")
MIN_SLIVER_RUN = 4

# A second book photographed the same way showed the strip can be wider, giving
# fragments the rule above cannot see — whole short words and clipped stems with
# spaces in them ("of the S", "A temp", "beyond", "archite").
#
# This tier is OPT-IN and off by default, because a short line is also what a
# table cell looks like. Measured across the reference corpus it would have
# deleted a rates table from bhoja-paramara-and-his-times ("Breadth", "in
# cubits", "Height") and a header row from the iconography volume ("Hands",
# "Symbols", "Mudra", "Vehicle", "Colour"). Losing a table silently is worse
# than keeping some debris, so callers ask for it explicitly, and only for
# photographed books where the strip dominates.
#
# Two guards still apply when it is on: the block must carry MIN_PROSE_CHARS of
# real prose (an index or list-of-illustrations page is ALL short lines, so
# stripping runs there would eat the content), and a line containing a digit
# never matches — illustration and index numbers live on lines of their own.
WIDE_SLIVER_FRAG_RE = re.compile(r"[A-Za-z][A-Za-z',.\- ]{0,9}")
MIN_PROSE_CHARS = 200
PROSE_LINE_LEN = 40


def has_prose(lines):
    """True if this block carries real running text, not just short entries."""
    return sum(len(l.strip()) for l in lines
               if len(l.strip()) > PROSE_LINE_LEN) >= MIN_PROSE_CHARS


def find_sliver_runs(lines, min_run=None, wide=False):
    """Indices of `lines` that belong to an edge-sliver run.

    A run is a maximal sequence of fragment lines. Blank lines are transparent —
    the OCR interleaves them — but any other content ends the run.

    Two patterns are used. SLIVER_FRAG_RE (<=4 chars, letters only) is safe
    anywhere and is the default. WIDE_SLIVER_FRAG_RE also catches wider strips
    but can mistake a table for debris, so `wide=True` is opt-in; even then it
    is suppressed on a block without prose, which is how index and
    list-of-illustrations pages keep their content.

    `min_run` defaults to MIN_SLIVER_RUN, read at call time rather than bound as
    a default argument, so raising the constant actually takes effect.
    """
    if min_run is None:
        min_run = MIN_SLIVER_RUN
    pattern = WIDE_SLIVER_FRAG_RE if (wide and has_prose(lines)) else SLIVER_FRAG_RE

    hits, run = set(), []
    for i, line in enumerate(lines):
        s = line.strip()
        if pattern.fullmatch(s) or SLIVER_FRAG_RE.fullmatch(s):
            run.append(i)
        elif s == "":
            continue
        else:
            if len(run) >= min_run:
                hits.update(run)
            run = []
    if len(run) >= min_run:
        hits.update(run)
    return hits


def find_sliver_runs_by_page(lines, pages_by_line, min_run=None, wide=False):
    """find_sliver_runs, but deciding the wide tier one page at a time.

    The prose gate has to be judged per page: a whole book obviously contains
    prose, so gating on the document would switch the wide tier on across its
    index and list-of-illustrations pages, which is exactly what the gate exists
    to prevent. `pages_by_line` (line index -> page number) marks the
    boundaries; with no markers the whole text is one block, as before.
    """
    if not pages_by_line:
        return find_sliver_runs(lines, min_run, wide)

    bounds = sorted(pages_by_line) + [len(lines)]
    hits = set()
    if bounds[0] > 0:                       # front matter before the first marker
        hits.update(find_sliver_runs(lines[:bounds[0]], min_run, wide))
    for start, end in zip(bounds, bounds[1:]):
        block = lines[start:end]
        hits.update(start + i for i in find_sliver_runs(block, min_run, wide))
    return hits


def strip_sliver_runs(text, min_run=MIN_SLIVER_RUN, wide=False):
    """`text` with edge-sliver runs removed. Returns (text, lines_removed).

    `wide` opts into the wider fragment pattern; see find_sliver_runs.
    """
    lines = text.split("\n")
    drop = find_sliver_runs(lines, min_run, wide)
    if not drop:
        return text, 0
    kept = [l for i, l in enumerate(lines) if i not in drop]
    return "\n".join(kept), len(drop)


def _bare(line):
    """A line reduced to its comparable text: no heading marks, no emphasis."""
    m = HEADING_RE.match(line.strip())
    s = m.group(2) if m else line.strip()
    return s.strip("*_ ").strip()


def _upper_ratio(s):
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def find_running_heads(lines):
    """Short, mostly-capitalised lines that recur across pages are print furniture."""
    counts = Counter()
    for ln in lines:
        s = _bare(ln)
        if 3 <= len(s) <= MAX_RUNHEAD_LEN:
            counts[s] += 1
    return {
        s
        for s, n in counts.items()
        if n >= MIN_RUNHEAD_HITS and _upper_ratio(s) >= RUNHEAD_UPPER_RATIO
    }


def _is_noise(s):
    """True for a stripped line that carries no retrievable content."""
    if not s:
        return True
    return bool(
        FOLIO_RE.match(s)
        or ROMAN_FOLIO_RE.match(s)
        or FIG_LABEL_RE.match(s)
        or NONTEXT_RE.match(s)
        or CREDIT_RE.match(s)
        or EMPTY_QUOTE_RE.match(s)
        or OCR_EMPTY_RE.search(s)
        or EXTRACTION_META_RE.search(s)
        or _has_cjk(s)
    )


def clean_lines(text):
    """Clean `text`, returning one record per surviving line.

    Each record: {text, page, heading_level}. `heading_level` is 0 for body
    lines and 1-6 for Markdown headings; `text` for a heading is its title only
    (the '#' marks are stripped). Blank separator lines are preserved as
    records with empty text so paragraph boundaries survive for the chunker.
    """
    # The `<!-- page N -->` markers carry the provenance every chunk cites, but
    # the comment strip below removes them, so record which page each line
    # belongs to first.
    pages_by_line = {}
    for idx, line in enumerate(text.split("\n")):
        pm = PAGE_RE.search(line)
        if pm:
            pages_by_line[idx] = int(pm.group(1))

    # Multi-line HTML comments (e.g. the translators' conventions block at the
    # head of Jagta_Hua_Kasba_EN.md) must go before the text is split by line.
    # Collapsing one to a single space would pull every following line up and
    # invalidate the index map above, so each comment leaves its newlines behind
    # and the line numbering is preserved exactly.
    text = COMMENT_RE.sub(lambda m: " " + "\n" * m.group(0).count("\n"), text)
    raw = text.split("\n")
    runheads = find_running_heads(raw)
    slivers = find_sliver_runs_by_page(raw, pages_by_line)
    seen_heading = set()

    out, page = [], None
    for idx, line in enumerate(raw):
        if idx in pages_by_line:
            page = pages_by_line[idx]
        if idx in slivers:
            # Facing-page strip caught by the camera; never real text.
            continue
        # Page markers and any other HTML comments never reach the embedder.
        line = COMMENT_RE.sub("", line)
        line = IMG_RE.sub("", line)
        line = SUPERSCRIPT_RE.sub("", line)

        stripped = line.strip()
        if RULE_RE.match(stripped):
            stripped = ""

        if not stripped:
            if out and out[-1]["text"]:
                out.append({"text": "", "page": page, "heading_level": 0})
            continue

        m = HEADING_RE.match(stripped)
        level = len(m.group(1)) if m else 0
        body = m.group(2).strip() if m else stripped
        bare = _bare(stripped)

        if _is_noise(bare):
            continue

        if bare in runheads:
            # Keep the first appearance of a running head that is also a real
            # heading — that is the section opening. Drop every repeat, and drop
            # all bare-text appearances (those are page furniture).
            if level and bare not in seen_heading:
                seen_heading.add(bare)
            else:
                continue

        if level and not body:
            continue

        out.append({"text": body if level else stripped,
                    "page": page, "heading_level": level})

    while out and not out[-1]["text"]:
        out.pop()
    return out


def clean_markdown(text):
    """Convenience: cleaned text as a plain string (page numbers dropped)."""
    parts = []
    for r in clean_lines(text):
        parts.append(("#" * r["heading_level"] + " " + r["text"]).strip()
                     if r["heading_level"] else r["text"])
    return "\n".join(parts)


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(0)
    src = Path(sys.argv[1]).read_text(encoding="utf-8")
    recs = clean_lines(src)
    kept = sum(1 for r in recs if r["text"])
    print(f"{len(src.split(chr(10)))} lines in -> {kept} content lines out")
    print(f"running heads detected: {sorted(find_running_heads(src.split(chr(10))))[:10]}")
