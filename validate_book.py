#!/usr/bin/env python3
"""
validate_book.py — integrity and grounding checks for the drafted chapters.

Reports, per chapter:

  words       body length against the target derived for that chapter, so a
              structurally short chapter is judged by its own evidence rather
              than a uniform quota
  notes       in-text markers vs the Notes list, and any unresolved [E..] ids
              the citation resolver failed to convert
  trunc       whether the file ends mid-word — the old pipeline shipped six of
              nine chapters truncated inside their endnotes
  gaps        [GAP — not in sources] markers awaiting human review
  1st         first-person leakage (a few false positives from quotations)
  rep         phrases of ten words recurring across different sections
  UNGROUNDED  proper nouns and numerals asserted in the prose that appear
              nowhere in the chapter's own evidence brief

The last is the important one. A chapter can cite correctly, read well and
still be wrong: Chapter 1's first draft attributed the region to the Meghadūta,
the Mahābhārata and three Purāṇas, none of which appear anywhere in its
retrieved evidence. Similarity scores cannot detect that, and neither can a
citation check — the fabricated claims carried valid markers.

Usage:
    python validate_book.py                 # table for every chapter
    python validate_book.py --chapter 1     # detail, incl. every ungrounded term
    python validate_book.py --allow-ungrounded   # report only; do not fail
"""
import argparse
import json
import re
import sys
from pathlib import Path

from book_outline import CHAPTERS, BY_NUMBER
from console import use_utf8
from entities import EntityIndex
from textnorm import fold as _fold

# Grounding resolution moved to the entity registry in v2: a sentence about
# 'Udayeśvara' is grounded by a passage that only ever says 'Nīlakaṇṭheśvara',
# which no amount of string folding can know. The registry is loaded once and
# `_present` keeps its old signature so the checks below are unchanged.
_ENTITIES = EntityIndex.load()


def _present(key, tokens):
    """Is this folded key attested among the evidence's folded tokens?"""
    return _ENTITIES.attested(key, tokens)

EVID = Path("book/_evidence")

# Sentence-initial and generic capitalised words that are not claims about the
# world; flagging them would bury the real findings.
_IGNORE = set("""
a an and or of in at on to by for from with without within into onto upon as is are was were be been
the this that these those there their its his her our your my it he she they we you i
but yet so if then than when where while whether though although because since after before during
all any both each few more most other some such no nor not only own same too very can will just
administered alternatively archive beyond devotion endures kingship landscape living memory relic
scripture silence subsumed survival whether across against among around behind below beneath beside
between beyond despite down near off out over past through toward under until up
chapter section notes bibliography figure plate map table appendix
bce ce bc ad century centuries era
buddhist islamic hindu jain jaina muslim brahmanical brahminical vedic puranic sanskrit persian
""".split())


def load_brief(n):
    p = EVID / f"ch{n:02d}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def target_words(brief):
    """Mirror of draft_chapter.target_words, so the check matches the brief."""
    subs = brief["subtopics"]
    ev = sum(len(p["text"].split()) for s in subs for p in s["passages"])
    return int(max(4000, min(9000, 800 * len(subs) + 0.25 * ev)))


def evidence_tokens(brief):
    toks = set()
    for s in brief["subtopics"]:
        for p in s["passages"]:
            for w in re.findall(r"[\w'’-]+", p["text"]):
                toks.add(_fold(w))
    toks.discard("")
    return toks


def ungrounded(body, brief):
    """Proper nouns and numerals in the prose with no support in the brief."""
    toks = evidence_tokens(brief)
    # Also allow anything the outline itself names — chapter and section titles
    # are the author's words, not claims drawn from a source.
    ch = BY_NUMBER.get(brief["n"], {})
    allowed = {_fold(w) for w in re.findall(r"[\w'’-]+",
               " ".join([ch.get("title", ""), ch.get("scope", ""), ch.get("theme") or ""]))}

    prose = re.sub(r"\[\d+\]", " ", body)                 # drop citation markers
    prose = re.sub(r"\[GAP[^\]]*\]", " ", prose)
    prose = re.sub(r"(?m)^#{1,6}.*$", " ", prose)          # headings are the author's words

    # A capital at the start of a sentence proves nothing. Only treat a word as
    # a proper noun if it appears capitalised somewhere that is *not* sentence-
    # initial; otherwise "Perched", "Sacred" and "Did" read as claims.
    midsentence = set()
    for m in re.finditer(r"[^\W\d_][\w'’-]{2,}", prose, re.UNICODE):
        w = m.group(0)
        if not w[:1].isupper():
            continue
        before = prose[:m.start()].rstrip()
        if before and not before.endswith((".", "!", "?", ":", ";", '"', "”", "*")):
            midsentence.add(w)

    names, nums = [], []
    for w in sorted(midsentence):
        if w.lower() in _IGNORE:
            continue
        k = _fold(w)
        if k and k not in allowed and not _present(k, toks):
            names.append(w)
    numtoks = {t for t in toks if t.isdigit()}
    for d in re.findall(r"\b\d{2,4}\b", prose):
        if d not in numtoks and not any(d in t for t in toks):
            nums.append(d)
    return sorted(set(names)), sorted(set(nums))


def repetition(body, n=10):
    secs = re.split(r"(?m)^##\s+", body)[2:]
    grams = []
    for s in secs:
        w = re.findall(r"[^\W\d_]+", s.lower(), re.UNICODE)
        grams.append({" ".join(w[i:i + n]) for i in range(len(w) - n)})
    dup = set()
    for i in range(len(grams)):
        for j in range(i + 1, len(grams)):
            dup |= grams[i] & grams[j]
    return dup


def check(n, d):
    fp = d / f"chapter-{n:02d}.md"
    if not fp.exists():
        return None
    t = fp.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+Notes\s*$", t)
    body, notes = parts[0], (parts[1] if len(parts) > 1 else "")
    brief = load_brief(n)

    marks = re.findall(r"\[(\d+)\]", body)
    listed = re.findall(r"(?m)^\[(\d+)\]", notes)
    tail = t.rstrip()
    r = {
        "n": n,
        "words": len(body.split()),
        "target": target_words(brief) if brief else None,
        "markers": len(set(marks)),
        "notes": len(listed),
        "aligned": sorted(set(marks), key=int) == sorted(set(listed), key=int),
        "eids": len(re.findall(r"\[E\d+\]", t)),
        "trunc": not tail.endswith((".", "!", "?", "”", '"', ")", "]")),
        "gaps": body.count("[GAP"),
        "first": len(re.findall(r"\b(?:I|we|us|our|you|your)\b", body)),
        "rep": len(repetition(body)),
        "brief": brief is not None,
    }
    if brief:
        names, nums = ungrounded(body, brief)
        r["ung_names"], r["ung_nums"] = names, nums
    else:
        r["ung_names"], r["ung_nums"] = [], []
    return r


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Validate drafted chapters")
    ap.add_argument("--dir", default="book")
    ap.add_argument("--chapter", type=int, help="detail for one chapter")
    # §5.2: strict is the DEFAULT in v2. v1's default — assemble regardless — is
    # what let a chapter that "cites correctly, reads well and is still wrong"
    # reach the manuscript. --allow-ungrounded is the explicit escape hatch for
    # work in progress, so shipping ungrounded prose becomes a decision someone
    # made rather than something that happened.
    ap.add_argument("--allow-ungrounded", action="store_true",
                    help="do not fail on ungrounded terms (work in progress)")
    ap.add_argument("--strict", action="store_true",
                    help=argparse.SUPPRESS)      # retained for compatibility; now the default
    args = ap.parse_args()
    d = Path(args.dir)

    nums = [args.chapter] if args.chapter else [c["n"] for c in CHAPTERS]
    rows = [(n, check(n, d)) for n in nums]

    hdr = (f"{'ch':<4}{'words':>7}{'target':>8}{'notes':>7}{'algn':>6}"
           f"{'Eid':>5}{'trunc':>7}{'gaps':>6}{'1st':>5}{'rep':>5}{'UNGROUNDED':>12}")
    print(hdr); print("-" * len(hdr))
    bad = 0
    for n, r in rows:
        if r is None:
            print(f"{n:<4}  (not drafted)"); continue
        u = len(r["ung_names"]) + len(r["ung_nums"])
        bad += u
        print(f"{n:<4}{r['words']:>7}{(r['target'] or 0):>8}{r['notes']:>7}"
              f"{str(r['aligned']):>6}{r['eids']:>5}{str(r['trunc']):>7}"
              f"{r['gaps']:>6}{r['first']:>5}{r['rep']:>5}{u:>12}")

    if args.chapter and rows[0][1]:
        r = rows[0][1]
        print(f"\nChapter {args.chapter} — ungrounded proper nouns ({len(r['ung_names'])}):")
        print("   " + (", ".join(r["ung_names"]) if r["ung_names"] else "(none)"))
        print(f"\nChapter {args.chapter} — numerals absent from evidence ({len(r['ung_nums'])}):")
        print("   " + (", ".join(r["ung_nums"]) if r["ung_nums"] else "(none)"))

    print("\nnote: 'algn' = every in-text marker has a matching note; 'Eid' = unresolved [E..] "
          "ids (should be 0); 'rep' = 10-word phrases shared across sections; 'UNGROUNDED' = "
          "names/numbers asserted in prose but absent from that chapter's evidence brief "
          "(review each — some are legitimate variant spellings).")
    strict = not args.allow_ungrounded
    if bad and strict:
        print(f"\nFAILED: {bad} ungrounded term(s) across {len(rows)} chapter(s). "
              f"Repair them (python verify.py --all --repair) or, to proceed anyway, "
              f"re-run with --allow-ungrounded.")
        sys.exit(1)


if __name__ == "__main__":
    main()
