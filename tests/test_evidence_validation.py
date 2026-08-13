"""Stage 3: evidence validation, before any prose exists."""
import copy

from verify import validate_pack


def test_good_pack_passes(good_pack):
    r = validate_pack(good_pack)
    assert r.status == "ok"
    assert r.errors == []
    assert r.n_passages == 6
    assert r.usable_passages == 6
    assert len(r.source_references) == 5      # E1 and E6 share a source


def test_source_metadata_survives_into_the_report(good_pack):
    r = validate_pack(good_pack)
    assert r.source_references["bhoja-paramara-and-his-times.md"] == 2
    assert "samarangana-sutradhara.md" in r.source_references


def test_empty_passage_is_an_error(good_pack):
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][0]["passages"][0]["text"] = "   "
    r = validate_pack(pack)
    assert r.status == "fail"
    assert any("no text" in e for e in r.errors)


def test_missing_source_is_an_error(good_pack):
    pack = copy.deepcopy(good_pack)
    del pack["subtopics"][0]["passages"][1]["source"]
    r = validate_pack(pack)
    assert r.status == "fail"
    assert any("no source" in e for e in r.errors)


def test_unresolvable_source_warns_but_does_not_block(good_pack):
    """A source missing from sources.py still drafts — its endnote degrades."""
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][0]["passages"][0]["source"] = "not-in-sources-py.md"
    r = validate_pack(pack)
    assert r.status == "warn"
    assert r.errors == []
    assert "not-in-sources-py.md" in r.unresolved_sources
    assert any("sources.py" in w for w in r.warnings)


def test_duplicate_passages_are_detected(good_pack):
    pack = copy.deepcopy(good_pack)
    dup = pack["subtopics"][0]["passages"][0]["text"]
    pack["subtopics"][1]["passages"][0]["text"] = dup
    r = validate_pack(pack)
    assert len(r.duplicate_passages) == 1
    assert r.duplicate_passages[0]["duplicate_of"] == "E1"
    assert r.usable_passages == r.n_passages - 1


def test_duplicate_passage_id_is_an_error(good_pack):
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][1]["passages"][0]["id"] = "E1"
    r = validate_pack(pack)
    assert r.status == "fail"
    assert any("duplicate or missing passage id" in e for e in r.errors)


def test_gap_subtopic_is_reported_not_silently_dropped(good_pack):
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][1]["passages"] = []
    pack["subtopics"][1]["status"] = "GAP"
    r = validate_pack(pack)
    assert "bhoja-learning" in r.gap_subtopics
    assert any("written as gaps" in w for w in r.warnings)


def test_thin_subtopic_warns(good_pack):
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][0]["passages"] = pack["subtopics"][0]["passages"][:1]
    pack["subtopics"][0]["status"] = "THIN"
    r = validate_pack(pack)
    assert "origins" in r.thin_subtopics
    assert r.status == "warn"


def test_completely_empty_pack_is_an_error():
    r = validate_pack({"n": 1, "subtopics": []})
    assert r.status == "fail"
    assert any("empty" in e for e in r.errors)


def test_pack_with_no_usable_passages_is_an_error(good_pack):
    pack = copy.deepcopy(good_pack)
    for s in pack["subtopics"]:
        s["passages"] = []
        s["status"] = "GAP"
    r = validate_pack(pack)
    assert r.status == "fail"
    assert any("no usable passages" in e for e in r.errors)


def test_missing_page_numbers_only_warn_when_required(good_pack):
    pack = copy.deepcopy(good_pack)
    pack["subtopics"][0]["passages"][0]["page_start"] = None
    assert validate_pack(pack, require_pages=False).incomplete_metadata == []
    r = validate_pack(pack, require_pages=True)
    assert len(r.incomplete_metadata) == 1
    assert r.status == "warn"


def test_report_is_structured_not_just_strings(good_pack):
    d = validate_pack(good_pack).to_dict()
    for key in ("status", "checks", "warnings", "errors", "source_references",
                "duplicate_passages", "gap_subtopics", "n_passages"):
        assert key in d
    assert all({"name", "status", "detail"} <= set(c) for c in d["checks"])
