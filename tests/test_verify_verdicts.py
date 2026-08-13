"""
Stage 6: verdict handling — and specifically the distinction between a claim
that FAILED verification and one that was never verified.

These tests exist because their absence cost a chapter. Chapter 1 ran while the
account's API quota was exhausted; every entailment call errored, `verify_section`
filed the results under `unsupported`, and `cut_unsupported` deleted 127 claims
that had perfectly good evidence behind them. The faithfulness figure printed
45% when the honest answer was "unknown".

Nothing here calls a model: `entail` is stubbed, which is the whole point —
the verdict-routing logic is ordinary code and must be tested as such.
"""
import pytest

import verify
from verify import Report, verify_section


@pytest.fixture
def claims_and_passages():
    passages = [{"id": "E1", "source": "bhojdev.md", "text": "Bhoja ruled from Dhara."}]
    return passages


def _stub(monkeypatch, verdicts):
    """Stub decompose+entail so only the routing logic is under test."""
    n = len(verdicts)
    monkeypatch.setattr(verify, "decompose", lambda *a, **k: [
        {"id": i + 1, "text": f"claim {i + 1}", "kind": "factual",
         "quote": f"Sentence number {i + 1} of the drafted section here."}
        for i in range(n)])
    monkeypatch.setattr(verify, "entail", lambda *a, **k: {
        i + 1: {"verdict": v} for i, v in enumerate(verdicts)})
    monkeypatch.setattr(verify, "ungrounded_terms", lambda *a, **k: [])


# ── the bug this file exists for ───────────────────────────────────────────

def test_unverified_is_not_filed_as_unsupported(monkeypatch, claims_and_passages):
    _stub(monkeypatch, ["supported", "unverified", "unverified"])
    rep = verify_section(None, "text", claims_and_passages)
    assert len(rep.unsupported) == 0            # NOT 2
    assert len(rep.unverified) == 2
    assert len(rep.supported) == 1


def test_unverified_is_excluded_from_the_faithfulness_denominator(monkeypatch,
                                                                  claims_and_passages):
    _stub(monkeypatch, ["supported", "unverified", "unverified", "unverified"])
    rep = verify_section(None, "text", claims_and_passages)
    assert rep.checked == 1
    assert rep.rate == 1.0                      # 1/1 judged, not 1/4
    assert rep.coverage == 0.25                 # ...but only a quarter was judged


def test_unverified_is_never_offered_to_repair(monkeypatch, claims_and_passages):
    """Repairing an unjudged claim would rewrite sound prose for no reason."""
    _stub(monkeypatch, ["unsupported", "unverified", "contradicted"])
    rep = verify_section(None, "text", claims_and_passages)
    texts = {c["text"] for c in rep.problems()}
    assert "claim 2" not in texts               # the unverified one
    assert len(rep.problems()) == 2


def test_unverified_claims_are_not_cut_from_the_prose(monkeypatch, claims_and_passages):
    """cut_unsupported reads report.unsupported — unverified must not be there."""
    _stub(monkeypatch, ["unverified", "unverified"])
    rep = verify_section(None, "text", claims_and_passages)
    body = ("Sentence number 1 of the drafted section here. "
            "Sentence number 2 of the drafted section here.")
    out, n_cut = verify.cut_unsupported(body, rep)
    assert n_cut == 0
    assert out == body                          # prose untouched


def test_total_verifier_failure_reports_unknown_not_zero(monkeypatch,
                                                         claims_and_passages):
    _stub(monkeypatch, ["unverified"] * 5)
    rep = verify_section(None, "text", claims_and_passages)
    assert rep.checked == 0
    assert rep.coverage == 0.0                  # nothing judged
    assert rep.rate == 1.0                      # vacuous, and paired with coverage
    assert "UNVERIFIED" in rep.summary()


# ── ordinary verdict routing ───────────────────────────────────────────────

def test_each_verdict_lands_in_its_own_bucket(monkeypatch, claims_and_passages):
    _stub(monkeypatch, ["supported", "partial", "unsupported", "contradicted"])
    rep = verify_section(None, "text", claims_and_passages)
    assert (len(rep.supported), len(rep.partial),
            len(rep.unsupported), len(rep.contradicted)) == (1, 1, 1, 1)
    assert rep.checked == 4
    assert rep.coverage == 1.0


def test_contradicted_is_kept_distinct_from_unsupported(monkeypatch,
                                                        claims_and_passages):
    """A contradiction needs correcting; cutting it would hide a factual error."""
    _stub(monkeypatch, ["contradicted"])
    rep = verify_section(None, "text", claims_and_passages)
    body = "Sentence number 1 of the drafted section here."
    _out, n_cut = verify.cut_unsupported(body, rep)
    assert n_cut == 0
    assert len(rep.contradicted) == 1
    assert rep.problems()                       # ...but repair still sees it


def test_non_factual_claims_are_skipped_not_judged(monkeypatch, claims_and_passages):
    monkeypatch.setattr(verify, "decompose", lambda *a, **k: [
        {"id": 1, "text": "a date", "kind": "factual", "quote": "q"},
        {"id": 2, "text": "a reading", "kind": "interpretive", "quote": "q"},
        {"id": 3, "text": "a transition", "kind": "narrative", "quote": "q"}])
    monkeypatch.setattr(verify, "entail", lambda *a, **k: {1: {"verdict": "supported"}})
    monkeypatch.setattr(verify, "ungrounded_terms", lambda *a, **k: [])
    rep = verify_section(None, "text", claims_and_passages)
    assert rep.checked == 1
    assert len(rep.skipped) == 2


def test_summary_shows_both_faithfulness_and_coverage():
    rep = Report()
    rep.supported = [1, 2, 3]
    rep.unsupported = [4]
    rep.unverified = [5, 6]
    s = rep.summary()
    assert "50% faithful" not in s              # 3/4 judged, not 3/6
    assert "75% faithful" in s
    assert "67% judged" in s
