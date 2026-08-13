#!/usr/bin/env python3
"""
textnorm.py — script-aware text normalisation shared across the pipeline.

v1 kept `_fold`, `_present` and `proper_nouns` inside make_evidence.py. The
sparse index (kb_store), the entity registry (entities) and the grounding check
all need the same operations, and having each import from make_evidence would
put a retrieval module downstream of an evidence-building one. They live here
instead; nothing in this file imports anything else in the project.

Three levels of normalisation, in increasing aggression:

    nfkd_strip("Vidiśā")   -> "vidisa"     diacritics dropped, script kept
    fold("Vidiśā")         -> "vidisa"     ...plus digraph collapse
    fold("Vidisha")        -> "vidisa"     — the point: both forms meet

The digraph collapse (sh->s, ch->c, kh->k ...) exists because Indic romanisation
varies by more than diacritics. Sources write 'Udaypur' where the outline writes
'Udayapura' and an inscription reads 'Udayapura'; a diacritic-only fold leaves
those three apart. It over-collapses in principle — 'ship' and 'sip' fold alike —
which is why fold() is used for *matching candidate proper nouns*, never for
indexing prose meaning.
"""
import re
import unicodedata
from functools import lru_cache

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate as _translit
    _HAVE_INDIC = True
except ImportError:                    # optional dependency; degrade, don't crash
    _HAVE_INDIC = False

DEVANAGARI_RE = re.compile(r"[ऀ-ॿ]")

# Word-shaped tokens. Capitalisation is tested in code, not in the pattern, so
# IAST capitals (Ś, Ā, Ṇ) need no explicit character class.
WORD_RE = re.compile(r"[^\W\d_][\w'’-]{1,}", re.UNICODE)

STOP_TERMS = {
    "the", "a", "an", "and", "or", "of", "in", "at", "on", "to", "for", "by",
    "its", "their", "his", "her", "this", "that", "these", "those", "with",
    "from", "but", "not", "was", "were", "are", "is", "be", "been", "as",
    "sanskrit", "hindu", "indian", "india", "chapter", "section", "figure",
    "how", "what", "why", "when", "where", "did", "does", "do", "which", "who",
}

_DIGRAPHS = (("sh", "s"), ("ch", "c"), ("kh", "k"), ("th", "t"), ("ph", "p"),
             ("bh", "b"), ("dh", "d"), ("gh", "g"), ("jh", "j"), ("ee", "i"),
             ("oo", "u"), ("aa", "a"), ("ii", "i"), ("uu", "u"),
             # व is romanised both ways: 'Udayeshwar' / 'Udayesvara',
             # 'Vishwakarma' / 'Visvakarma'. One letter, two conventions.
             ("w", "v"))


def has_devanagari(s):
    return bool(DEVANAGARI_RE.search(s))


def strip_devanagari(s):
    """Latin-script lines only — used for the bilingual embed split."""
    return "\n".join(ln for ln in s.split("\n") if ln.strip() and not has_devanagari(ln))


def devanagari_only(s):
    """Devanagari lines only — the sparse index's script-3 stream."""
    return "\n".join(ln for ln in s.split("\n") if has_devanagari(ln))


def nfkd_strip(s):
    """Drop combining marks, lowercase. 'Nīlakaṇṭheśvara' -> 'nilakanthesvara'."""
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def depossess(s):
    """'Udayāditya's' -> 'Udayāditya'. Both straight and curly apostrophes."""
    return re.sub(r"['’]s\b|['’]\B|['’]$", "", s)


@lru_cache(maxsize=200_000)
def deva_to_latin(s):
    """Devanagari -> IAST, so the two scripts can meet under fold().

    Without this, fold() destroys Devanagari outright: NFKD strips the matras
    (which are combining marks) and the final [^a-z0-9] filter removes what is
    left, so every Devanagari alias folds to the empty string and the entity
    stream is dead for the Hindi and Sanskrit sources. Transliterating first
    means भोज and Bhoja both fold to 'boja'.
    """
    if not _HAVE_INDIC or not DEVANAGARI_RE.search(s):
        return s
    try:
        return _translit(s, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:                  # noqa: BLE001 - never let a fold crash a build
        return s


def fold(s):
    """Transliteration-insensitive key for proper-noun matching.

    Script-neutral: Devanagari is transliterated to IAST first, so
    fold('भोज') == fold('Bhoja') == 'boja'.
    """
    s = nfkd_strip(deva_to_latin(depossess(s)))
    s = s.replace("'", "")             # IAST avagraha / glottal from transliteration
    for a, b in _DIGRAPHS:
        s = s.replace(a, b)
    # Collapse doubled consonants left by the digraph pass ('mallla' -> 'mala').
    s = re.sub(r"(.)\1+", r"\1", s)
    return re.sub(r"[^a-z0-9]", "", s)


def fold_text(s):
    """Fold every word in a passage, space-joined — the sparse index's stream 2."""
    return " ".join(f for f in (fold(w) for w in WORD_RE.findall(s)) if f)


def tokens(s):
    """The folded token set of a passage."""
    return {f for f in (fold(w) for w in WORD_RE.findall(s)) if f}


def proper_nouns(text, stop=None):
    """Capitalised words that are genuinely proper nouns.

    A capital at the start of a sentence proves nothing, so a word counts only
    where it is capitalised somewhere that is not sentence-initial.

    That test alone does not tame Title Case: in "How Did the Corpus Debate",
    only "How" is sentence-initial, so "Corpus" and "Debate" survive. Callers
    must therefore keep Title Case headings and sub-unit titles *out* of the
    text they pass here — filtering them afterwards is unreliable. Resolving
    what does come back through the entity registry is the real defence.
    """
    stop = STOP_TERMS if stop is None else stop
    out, seen = [], set()
    for m in WORD_RE.finditer(text):
        w = m.group(0)
        if len(w) < 3 or not w[:1].isupper() or w.lower() in stop:
            continue
        before = text[:m.start()].rstrip()
        if not before or before.endswith((".", "!", "?", ":", ";", "\n", "|", "-", "—")):
            continue
        if w.lower() not in seen:
            seen.add(w.lower())
            out.append(w)
    return out


NUMERAL_RE = re.compile(r"\b\d{1,4}(?:[–\-/]\d{1,4})?\b")


def numerals(text):
    """Bare numbers and ranges — dates, measurements, counts.

    Used by the verification gate: a numeral asserted in prose must trace to a
    passage, exactly as a proper noun must.
    """
    return [m.group(0) for m in NUMERAL_RE.finditer(text)]
