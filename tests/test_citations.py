"""Stages 5 and 7: the editorial citation guard, and citation/provenance resolution."""
import sources
from draft_chapter import citation_delta, resolve_citations


# ── stage 7: citation resolution ───────────────────────────────────────────

def test_ids_become_numbered_endnotes_in_order(byid):
    body = "First claim [E4]. Second claim [E1]. Third [E4] again."
    out, notes, order, bogus = resolve_citations(body, byid)
    assert order == ["E4", "E1"]              # numbered by first appearance
    assert "[1]" in out and "[2]" in out
    assert "[E4]" not in out                  # raw ids never survive
    assert bogus == []
    assert notes.startswith("## Notes")


def test_endnote_carries_source_and_page(byid):
    _out, notes, order, _ = resolve_citations("A claim [E4].", byid)
    line = [l for l in notes.splitlines() if l.startswith("[1]")][0]
    assert sources.short("samarangana-sutradhara.md").split(",")[0] in line
    assert "p. 12" in line                    # provenance reaches the reader


def test_invented_citation_is_stripped_and_reported(byid):
    body = "Real [E1]. Invented [E999]."
    out, _notes, order, bogus = resolve_citations(body, byid)
    assert bogus == ["E999"]
    assert "E999" not in out
    assert order == ["E1"]


def test_every_endnote_resolves_to_a_real_source(byid):
    body = " ".join(f"claim [{k}]." for k in byid)
    _out, _notes, order, bogus = resolve_citations(body, byid)
    assert bogus == []
    assert len(order) == len(byid)
    for eid in order:
        assert byid[eid]["source"]
        assert byid[eid].get("chunk_id") is not None   # back to the KB row


def test_claim_to_source_chain_is_walkable(byid):
    """claim → E-id → passage → source document → page."""
    _out, _notes, order, _ = resolve_citations("A [E5].", byid)
    p = byid[order[0]]
    assert p["source"] == "bhojdev.md"
    assert p["trail"] and p["page_start"]
    assert sources.full(p["source"])          # resolves to a bibliography entry


# ── stage 5: the editorial guard ───────────────────────────────────────────

def test_clean_edit_reports_no_change():
    d = citation_delta("The temple [E1] stands. It is old [E2].",
                       "The temple stands [E1] — and it is old [E2].")
    assert d["dropped"] == {} and d["added"] == {}
    assert d["gaps_lost"] == 0


def test_dropped_citation_is_caught():
    d = citation_delta("A [E1] and B [E2].", "A and B [E1].")
    assert d["dropped"] == {"E2": 1}


def test_invented_citation_is_caught():
    d = citation_delta("A [E1].", "A [E1] and more [E7].")
    assert d["added"] == {"E7": 1}


def test_lost_gap_marker_is_caught():
    d = citation_delta("Known [E1]. [GAP — not in sources]",
                       "Known [E1].")
    assert d["gaps_lost"] == 1


def test_merging_sentences_must_keep_both_citations():
    """The prompt tells the model this; the check enforces it."""
    before = "The temple was built in 1080 [E1]. It stands on the Betwa [E2]."
    merged_ok = "The temple, built in 1080 [E1], stands on the Betwa [E2]."
    merged_bad = "The temple, built in 1080, stands on the Betwa [E2]."
    assert citation_delta(before, merged_ok)["dropped"] == {}
    assert citation_delta(before, merged_bad)["dropped"] == {"E1": 1}


def test_repeated_citation_count_is_tracked():
    """Multiset, not set: losing one of two [E1]s is still a loss."""
    d = citation_delta("A [E1]. B [E1].", "A [E1]. B.")
    assert d["dropped"] == {"E1": 1}
