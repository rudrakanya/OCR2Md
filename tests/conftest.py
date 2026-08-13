"""
Shared fixtures. These are the repository's first tests, so a note on scope.

Nothing here touches a live model, the Mistral API, the embedding matrix or the
SQLite store. Every stage that needs one of those takes it as an argument, which
is what makes the pipeline testable at all — the seams already existed, they
were just never exercised.

What IS tested is the deterministic spine: evidence validation, citation
resolution, provenance, the editorial citation guard, and the run record. That
is deliberate. Those are the parts that must not silently break, and they are
precisely the parts that need no model to check.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _passage(pid, source, text, page=12, trail="A > B", score=0.7):
    return {"id": pid, "source": source, "trail": trail, "heading": "B",
            "page_start": page, "page_end": page, "score": score, "text": text,
            "chunk_id": 100 + int(pid[1:])}


@pytest.fixture
def good_pack():
    """A well-formed evidence brief: two sub-topics, distinct real sources."""
    return {
        "n": 6, "title": "The Paramāras and Bhoja", "theme": "t", "scope": "s",
        "kb": {"hash": "abc123", "count": 9467, "config": "cfg1"},
        "subtopics": [
            {"key": "origins", "question": "Where did the Paramāras come from?",
             "status": "OK", "note": "ok", "cut": 0.3, "unevidenced": [],
             "n_candidates": 48, "queries": ["q1", "q2"],
             "retrieval": {"reranker": "hosted", "floor_mode": "rerank-provisional"},
             "passages": [
                 _passage("E1", "bhoja-paramara-and-his-times.md",
                          "The Agnikula legend places the dynasty's origin at Mount Abu."),
                 _passage("E2", "paramara-dynasty-comprehensive-history.md",
                          "Upendra is named as the first historical ruler of the line."),
                 _passage("E3", "The Hindu Temple Vol 1 Stella Kramrisch.md",
                          "The prasada is conceived as the body of the deity."),
             ]},
            {"key": "bhoja-learning", "question": "What did Bhoja write?",
             "status": "OK", "note": "ok", "cut": 0.3, "unevidenced": [],
             "n_candidates": 48, "queries": ["q3"],
             "retrieval": {"reranker": "hosted", "floor_mode": "rerank-provisional"},
             "passages": [
                 _passage("E4", "samarangana-sutradhara.md",
                          "The Samarangana Sutradhara is attributed to Bhojadeva."),
                 _passage("E5", "bhojdev.md",
                          "Bhoja's court at Dhara drew scholars from across Malwa."),
                 _passage("E6", "bhoja-paramara-and-his-times.md",
                          "His reign is conventionally dated to the eleventh century."),
             ]},
        ],
    }


@pytest.fixture
def byid(good_pack):
    return {p["id"]: p for s in good_pack["subtopics"] for p in s["passages"]}
