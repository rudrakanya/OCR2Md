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
CREDIT_RE = re.compile(r"^(photo|photograph|drawing|plan|courtesy)\b.{0,60}$", re.I)
EMPTY_QUOTE_RE = re.compile(r"^>+\s*$")
# The OCR'd page-scan note emitted by ocr_to_markdown.py for blank/plate pages.
OCR_EMPTY_RE = re.compile(r"No machine-readable text detected", re.I)

MIN_RUNHEAD_HITS = 5
MAX_RUNHEAD_LEN = 70
RUNHEAD_UPPER_RATIO = 0.6


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
    )


def clean_lines(text):
    """Clean `text`, returning one record per surviving line.

    Each record: {text, page, heading_level}. `heading_level` is 0 for body
    lines and 1-6 for Markdown headings; `text` for a heading is its title only
    (the '#' marks are stripped). Blank separator lines are preserved as
    records with empty text so paragraph boundaries survive for the chunker.
    """
    # Multi-line HTML comments (e.g. the translators' conventions block at the
    # head of Jagta_Hua_Kasba_EN.md) must go before the text is split by line.
    text = COMMENT_RE.sub(" ", text)
    raw = text.split("\n")
    runheads = find_running_heads(raw)
    seen_heading = set()

    out, page = [], None
    for line in raw:
        pm = PAGE_RE.search(line)
        if pm:
            page = int(pm.group(1))
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
