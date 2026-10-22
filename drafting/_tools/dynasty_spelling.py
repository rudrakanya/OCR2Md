"""D1 (user, 16 Oct): dynasty names in the style sheet's IAST forms, outside verbatim quotations (free).

  python -I -X utf8 drafting/_tools/dynasty_spelling.py scan  FILE...   list every variant, inside/outside quotes
  python -I -X utf8 drafting/_tools/dynasty_spelling.py fix   FILE...   replace variants outside quotations (in place)
  python -I -X utf8 drafting/_tools/dynasty_spelling.py check FILE...   exit 1 if any non-IAST variant stands outside quotes
                                                                         (also used by prose_checks for later chapters)
Quotations = text inside “…”, ‘…’ (when it spans more than one word) or "…". Evidence IDs [C..] are untouched.
"""
import re
import sys
from pathlib import Path

# variant -> IAST form (singular stems; plural and possessive suffixes are kept)
MAP = [
    (r"Kalachuri", "Kalacuri"), (r"Kalchuri", "Kalacuri"),
    (r"Chandella", "Candella"), (r"Chandela", "Candella"),
    (r"Chaulukya", "Caulukya"),
    (r"Chālukya", "Cālukya"), (r"Chalukya", "Cālukya"),
    (r"Rashtrakuta", "Rāṣṭrakūṭa"), (r"Rāshṭrakūṭa", "Rāṣṭrakūṭa"),
    (r"Paramara(?!ā)", "Paramāra"),
]
# familiar forms given once, at the first mention in the book
FAMILIAR = {"Kalacuri": "Kalachuri", "Candella": "Chandela", "Caulukya": "Chaulukya", "Cālukya": "Chalukya"}
VARIANT = re.compile(r"\b(" + "|".join(v for v, _ in MAP) + r")(s|'s|s')?\b")
# skipped spans: quotations; italic spans (book titles keep their own spelling); [bracketed] translated titles and IDs;
# <!-- --> comments; the footnote builder's upper-case section paths
QUOTE = re.compile(r"“[^”]*”|\"[^\"\n]*\"|‘[^’]*\s[^’]*’|\*[^*\n]+\*|\[[^\]\n]*\]|<!--.*?-->|\b[A-Z][A-Z ]{6,}(?: > [A-Z ,]+)+")


def spans(text):
    return [(m.start(), m.end()) for m in QUOTE.finditer(text)]


def inside(pos, sp, text=None, end=None):
    """True inside a quotation, or for the once-only familiar form in brackets: "Candellas (Chandelas)". The bracketed
    form is accepted only at the FIRST mention of that IAST name in the text checked (user, 19 Oct 2026); run the check
    on the stitched chapter to enforce first mention across sections."""
    if text is not None and text[end:end + 1] == ")":
        g = re.search(r"\b(" + "|".join(FAMILIAR) + r")\w*'?s? \($", text[max(0, pos - 30):pos])
        if g:
            first = re.search(r"\b" + g.group(1), text)
            return bool(first) and first.start() == max(0, pos - 30) + g.start(1)
    return any(a <= pos < b for a, b in sp)


def target(v):
    for pat, t in MAP:
        if re.fullmatch(pat, v):
            return t
    return v


def scan(text):
    sp = spans(text)
    return [(m.group(0), m.start(), inside(m.start(), sp, text, m.end())) for m in VARIANT.finditer(text)]


def fix(text):
    sp = spans(text)
    out, last, n = [], 0, 0
    for m in VARIANT.finditer(text):
        if inside(m.start(), sp, text, m.end()):
            continue
        out.append(text[last:m.start()])
        out.append(target(m.group(1)) + (m.group(2) or ""))
        last, n = m.end(), n + 1
    out.append(text[last:])
    return "".join(out), n


if __name__ == "__main__":
    cmd, files = sys.argv[1], [Path(f) for f in sys.argv[2:]]
    bad = 0
    for f in files:
        t = f.read_text(encoding="utf-8")
        if cmd == "scan":
            for w, pos, q in scan(t):
                print(f"{f.name}\t{'QUOTE' if q else 'text '}\t{w}\t…{t[max(0, pos - 50):pos + 40].replace(chr(10), ' ')}…")
        elif cmd == "fix":
            t2, n = fix(t)
            if n:
                f.write_text(t2, encoding="utf-8")
            print(f"{f.name}: {n} replaced")
        elif cmd == "check":
            hits = [(w, pos) for w, pos, q in scan(t) if not q]
            bad += len(hits)
            for w, pos in hits:
                print(f"{f.name}: non-IAST dynasty name outside quotation: {w} …{t[max(0, pos - 40):pos + 30]}…")
    sys.exit(1 if bad else 0)
