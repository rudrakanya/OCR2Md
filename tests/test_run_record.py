"""Observability: the run record, stage attribution, and CLI rendering."""
import json

import pytest

from run import GenerationRun, render, summary_line


def test_stages_are_recorded_in_order():
    run = GenerationRun.start(chapter=6, title="T")
    for name in ("Accessing knowledge base", "Retrieving evidence", "Validating evidence"):
        with run.stage(name, total=3, echo=False) as st:
            st.metric("things", 1)
    assert [s.name for s in run.stages] == [
        "Accessing knowledge base", "Retrieving evidence", "Validating evidence"]
    assert [s.index for s in run.stages] == [1, 2, 3]
    assert all(s.total == 3 for s in run.stages)


def test_failure_is_attributed_to_its_stage_and_reraised():
    run = GenerationRun.start(chapter=6)
    with run.stage("Accessing knowledge base", echo=False):
        pass
    with pytest.raises(ValueError):
        with run.stage("Validating evidence", echo=False):
            raise ValueError("pack malformed")
    assert run.failed
    stage, msg = run.errors[0]
    assert stage == "Validating evidence"        # the point of the whole record
    assert "pack malformed" in msg
    assert run.stages[0].status == "ok"


def test_warnings_do_not_mark_the_run_failed():
    run = GenerationRun.start(chapter=1)
    with run.stage("Validating evidence", echo=False) as st:
        st.warn("2 sub-topics thin")
    assert not run.failed
    assert run.warnings == [("Validating evidence", "2 sub-topics thin")]
    assert run.to_dict()["status"] == "warn"


def test_sources_merge_across_stages_and_counts_add():
    run = GenerationRun.start(chapter=1)
    with run.stage("Retrieving evidence", echo=False) as st:
        st.source("kramrisch.md", passages=12)
        st.source("bhojdev.md", passages=3)
    with run.stage("Resolving citations", echo=False) as st:
        st.source("kramrisch.md", cited=4)
    ordered = run.all_sources()
    merged = {s["source"]: s for s in ordered}
    assert merged["kramrisch.md"]["passages"] == 12
    assert merged["kramrisch.md"]["cited"] == 4
    # Sorted by passage count, so the heaviest-used book leads the list.
    # Compare order, not identity: all_sources() rebuilds its dicts per call.
    assert [s["source"] for s in ordered] == ["kramrisch.md", "bhojdev.md"]


def test_run_record_is_json_serialisable_and_complete():
    run = GenerationRun.start(chapter=6, title="T", kb={"hash": "abc"})
    with run.stage("Retrieving evidence", total=7, echo=False) as st:
        st.metric("passages", 60)
        st.source("bhojdev.md", passages=3)
    run.finish(words=7000, endnotes=20, sources=5, path="x.md")
    blob = json.dumps(run.to_dict())            # must not raise
    d = json.loads(blob)
    for key in ("run_id", "chapter", "pipeline_version", "stages", "sources",
                "warnings", "errors", "output", "kb", "status"):
        assert key in d
    assert d["output"]["words"] == 7000
    assert d["stages"][0]["metrics"]["passages"] == 60


def test_record_holds_no_prompts_or_credentials():
    """The record is decisions and evidence — never the text behind them."""
    run = GenerationRun.start(chapter=1)
    with run.stage("Formulating chapter", echo=False) as st:
        st.data("plan", [{"title": "S1", "subtopics": ["a"]}])
        st.note("target 6,500 words")
    blob = json.dumps(run.to_dict()).lower()
    for forbidden in ("api_key", "authorization", "bearer", "system prompt",
                      "you are revising", "mistral_api_key"):
        assert forbidden not in blob


def test_render_shows_stages_metrics_and_warnings():
    run = GenerationRun.start(chapter=6, title="Bhoja")
    with run.stage("Retrieving evidence", total=7, echo=False) as st:
        st.metric("passages retrieved", 60)
        st.warn("2 sub-topics thin")
    run.finish(words=7000, endnotes=20, sources=5, path="x.md")
    out = render(run)
    assert "[1/7] Retrieving evidence" in out
    assert "60 passages retrieved" in out
    assert "2 sub-topics thin" in out
    assert "Chapter draft generated" in out


def test_render_names_the_failing_stage():
    run = GenerationRun.start(chapter=6)
    try:
        with run.stage("Validating evidence", total=7, echo=False):
            raise RuntimeError("no usable passages")
    except RuntimeError:
        pass
    out = render(run)
    assert "FAILED" in out
    assert "Validating evidence: RuntimeError: no usable passages" in out


def test_show_sources_lists_reference_books():
    run = GenerationRun.start(chapter=1)
    with run.stage("Retrieving evidence", echo=False) as st:
        st.source("The Hindu Temple Vol 1 Stella Kramrisch.md", passages=12)
    run.finish(words=1, endnotes=0, sources=1)
    assert "Kramrisch" in render(run, show_sources=True)
    assert "Kramrisch" not in render(run, show_sources=False)


def test_verbose_adds_structured_detail_only_when_asked():
    run = GenerationRun.start(chapter=1)
    with run.stage("Retrieving evidence", echo=False) as st:
        st.data("queries", {"origins": ["q1"]})
    assert "queries" not in render(run)
    assert "queries" in render(run, verbose=True)


def test_summary_line_is_one_line_per_chapter():
    run = GenerationRun.start(chapter=3)
    with run.stage("x", echo=False):
        pass
    run.finish(words=6200, endnotes=18)
    line = summary_line(run)
    assert "ch03" in line and "6,200w" in line
    assert "\n" not in line


def test_save_writes_a_readable_record(tmp_path):
    run = GenerationRun.start(chapter=9)
    with run.stage("x", echo=False) as st:
        st.metric("n", 1)
    run.finish(words=10)
    p = run.save(tmp_path)
    assert p.exists()
    assert json.loads(p.read_text(encoding="utf-8"))["chapter"] == 9
