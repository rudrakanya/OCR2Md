"""Unicode handling for a corpus that is simultaneously English, Devanagari,
Sanskrit and IAST (§5).

The single rule that governs this module: the text we STORE and DISPLAY keeps
every diacritic and every Devanagari codepoint, and a separate folded copy
exists only so a lexical search for "Udayaditya" can match "Udayāditya".
Folding is never applied to what gets embedded or shown.
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate as _translit
    _HAVE_INDIC = True
except ImportError:  # pragma: no cover
    _HAVE_INDIC = False

DEVANAGARI_RE = re.compile(r"[ऀ-ॿ꣠-ꣿ]")
LATIN_RE = re.compile(r"[A-Za-z]")
# IAST diacritics that survive in this corpus after OCR.
IAST_RE = re.compile(r"[āīūṛṝḷḹṅñṭḍṇśṣḥṃĀĪŪṚṜḶḸṄÑṬḌṆŚṢḤṂ]")

# Digraph substitutions applied before diacritic stripping, so that the folded
# form of a Devanagari word and of its romanisation converge on the same
# ASCII string. Order matters: longer keys first.
_DIGRAPHS = (
    ("ṣ", "s"), ("ś", "s"), ("ṛ", "r"), ("ṝ", "r"), ("ḷ", "l"), ("ḹ", "l"),
    ("ṅ", "n"), ("ñ", "n"), ("ṇ", "n"), ("ṭ", "t"), ("ḍ", "d"), ("ṃ", "m"),
    ("ḥ", "h"), ("ā", "a"), ("ī", "i"), ("ū", "u"),
    ("kh", "k"), ("gh", "g"), ("ch", "c"), ("jh", "j"), ("th", "t"),
    ("dh", "d"), ("ph", "p"), ("bh", "b"), ("sh", "s"), ("v", "w"),
)


def nfc(text: str) -> str:
    """§5: everything is normalised to NFC on load, once, at the boundary."""
    return unicodedata.normalize("NFC", text)


@lru_cache(maxsize=200_000)
def deva_to_latin(s: str) -> str:
    """Devanagari -> IAST, so the two scripts can meet under fold().

    Without this step, NFKD-then-strip destroys Devanagari outright: the
    decomposition separates the matras and the ASCII filter then deletes
    everything, leaving an empty folded string for every Hindi passage.
    """
    if not _HAVE_INDIC or not DEVANAGARI_RE.search(s):
        return s
    try:
        return _translit(s, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:
        return s


def fold(text: str) -> str:
    """Diacritic-folded, lowercased ASCII copy — for the lexical layer only.

    "Udayāditya", "उदयादित्य" and "Udayaditya" all fold to "udayaditya".
    """
    if not text:
        return ""
    text = deva_to_latin(nfc(text)).lower()
    for src, dst in _DIGRAPHS:
        text = text.replace(src, dst)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize_folded(text: str) -> list[str]:
    """Token stream for BM25. Operates on already-folded text."""
    return [t for t in fold(text).split() if len(t) > 1]


def detect_language(text: str) -> str:
    """Best-effort script/language label: en | hi | sa | mixed.

    Deliberately script-based rather than a statistical language ID: the
    distinction that actually matters downstream is which writing system a
    passage uses, and a model trained on running prose does badly on OCR'd
    verse with interleaved translation.
    """
    if not text.strip():
        return "en"
    deva = len(DEVANAGARI_RE.findall(text))
    latin = len(LATIN_RE.findall(text))
    total = deva + latin
    if total == 0:
        return "en"
    deva_ratio = deva / total
    if deva_ratio > 0.85:
        return "hi"
    if deva_ratio > 0.15:
        return "mixed"
    # Mostly Latin. Heavy IAST implies transliterated Sanskrit rather than
    # ordinary English prose.
    iast = len(IAST_RE.findall(text))
    if latin and iast / latin > 0.04:
        return "sa"
    return "en"


_WORD_RE = re.compile(r"\w+", re.UNICODE)


def shingles(text: str, n: int = 8) -> set[int]:
    """Hashed word n-grams of the folded text, for near-duplicate detection.

    Folded input means an OCR of the same page in two files still collides
    despite differing diacritic recovery.
    """
    words = fold(text).split()
    if len(words) < n:
        return {hash(" ".join(words))} if words else set()
    return {hash(" ".join(words[i:i + n])) for i in range(len(words) - n + 1)}


def jaccard(a: set[int], b: set[int]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def snippet(text: str, limit: int = 320) -> str:
    """A display snippet that does not split a Devanagari cluster."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    # Back off to a space so we never end mid-word or mid-conjunct.
    if " " in cut[limit // 2:]:
        cut = cut[:cut.rfind(" ")]
    return cut + "…"
