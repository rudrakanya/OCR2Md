#!/usr/bin/env python3
"""
verify.py — claim decomposition and the entailment gate (§5).

v1 stated the problem exactly: grounding is a report, not a gate, and nothing
prevents spontaneous fabrication. The Chapter 1 experiment settled the method
question — suppressing the specific fabricated terms produced *different*
fabrications and raised the ungrounded count from 9 to 17. You cannot enumerate
what a model might invent, so a denylist cannot work.

The fix inverts the burden. Instead of blocking a list of forbidden things,
every assertion must carry a warrant:

    1. decompose the drafted section into atomic claims
    2. check each claim for entailment against that section's own evidence pack
    3. classify supported / unsupported / contradicted / not-a-factual-claim
    4. require every proper noun and numeral to trace to a passage

Two cheap deterministic checks run BEFORE the expensive judge, because they are
free and catch the commonest failure: a proper noun or a date that appears
nowhere in the pack. Only what survives goes to the entailment call.

`contradicted` is kept distinct from `unsupported` on purpose. Unsupported means
the corpus is silent — a candidate for [GAP - not in sources]. Contradicted
means the corpus says otherwise, which is a factual error and more serious; it
should never be silently cut, because the sentence needs correcting, not
deleting.

    from verify import verify_section, repair_prompt
    report = verify_section(client, text, passages, entities=ix)
    report.unsupported     # [{claim, terms, sentence}]
    report.rate            # supported / (supported + unsupported + contradicted)

CLI:
    python verify.py chapter_drafts/chapter-06.md --chapter 6
    python verify.py --all --out book/_verify
"""
import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from config import CFG
from console import use_utf8
from llm import complete_json, get_client, parallel
from textnorm import WORD_RE, fold, numerals, proper_nouns

EVID = Path("book/_evidence")

DECOMPOSE_SYSTEM = """You break drafted historical prose into atomic factual claims.

An atomic claim asserts exactly one thing and can be checked on its own. Split compound \
sentences. Resolve pronouns and demonstratives so each claim stands alone ("the temple" -> \
"the Udayeśvara temple").

Classify each claim:
  factual        asserts something checkable about the world — a date, an attribution, a \
measurement, an identification, an event, an influence
  interpretive   the author's reading, framing or judgement, presented as such ("the effect is \
one of restraint", "this suggests a deliberate archaism")
  narrative      transitions, scene-setting, rhetorical questions, signposting

Only `factual` claims will be checked against sources. Do not invent claims the text does not \
make, and do not merge two assertions into one.

Return JSON only:
{"claims": [{"id": 1, "text": "...", "kind": "factual|interpretive|narrative", \
"quote": "the sentence it came from, verbatim"}]}"""

ENTAIL_SYSTEM = """You decide whether each claim is supported by the supplied source passages, \
and by nothing else.

You are NOT being asked whether the claim is true. You are being asked whether THESE PASSAGES \
establish it. A claim you know to be correct from your own knowledge of Indian history is \
`unsupported` if the passages do not say it. That distinction is the entire purpose of this step.

  supported     the passages state or directly entail the claim
  partial       the passages support part of it — some detail (a date, a number, an \
attribution) goes beyond what they say
  unsupported   the passages are silent on it
  contradicted  the passages assert something incompatible with it

For `partial` and `unsupported`, name in `missing` exactly which element is unattested. For \
`contradicted`, quote in `conflict` what the passages say instead.

Return JSON only:
{"results": [{"id": 1, "verdict": "supported|partial|unsupported|contradicted", \
"passage_ids": ["E12"], "missing": "...", "conflict": "..."}]}"""


@dataclass
class Report:
    claims: list = field(default_factory=list)
    supported: list = field(default_factory=list)
    partial: list = field(default_factory=list)
    unsupported: list = field(default_factory=list)
    contradicted: list = field(default_factory=list)
    unverified: list = field(default_factory=list)
    skipped: list = field(default_factory=list)
    ungrounded_terms: list = field(default_factory=list)

    @property
    def checked(self):
        """Claims the verifier actually reached a verdict on.

        `unverified` is excluded by construction — those claims go to their own
        list. A claim nobody judged belongs in neither the numerator nor the
        denominator of a faithfulness score; counting it as a failure reported
        chapter 1 at 45% faithful when the true figure was simply unknown,
        because the account's API quota had run out mid-run.
        """
        return len(self.supported) + len(self.partial) + len(self.unsupported) + \
            len(self.contradicted)

    @property
    def rate(self):
        """Fraction of JUDGED factual claims that are fully supported."""
        return len(self.supported) / self.checked if self.checked else 1.0

    @property
    def coverage(self):
        """Fraction of factual claims the verifier managed to judge at all.

        Always reported beside `rate`, because 100% faithful over three judged
        claims is not the same result as 100% over three hundred, and only this
        number distinguishes them.
        """
        total = self.checked + len(self.unverified)
        return self.checked / total if total else 1.0

    def problems(self):
        """What REPAIR must act on, worst first.

        `unverified` is deliberately absent: there is nothing to repair in a
        claim that was never judged, and handing it to the repair prompt would
        invite the model to rewrite sound prose to satisfy a check that never ran.
        """
        return self.contradicted + self.unsupported + self.partial

    def summary(self):
        tail = (f", {len(self.unverified)} UNVERIFIED"
                if self.unverified else "")
        return (f"{len(self.supported)} supported, {len(self.partial)} partial, "
                f"{len(self.unsupported)} unsupported, {len(self.contradicted)} contradicted"
                f"{tail} ({self.rate * 100:.0f}% faithful over "
                f"{self.coverage * 100:.0f}% judged)")


def _pack_vocabulary(passages, entities=None):
    """Folded tokens and numerals the evidence actually attests."""
    blob = "\n".join(p.get("text", "") for p in passages)
    toks = {fold(w) for w in WORD_RE.findall(blob)} - {""}
    nums = set(numerals(blob))
    return toks, nums, blob


def ungrounded_terms(text, passages, entities=None):
    """Proper nouns and numerals in the prose that no passage attests.

    The deterministic pre-filter. It is v1's UNGROUNDED check with the entity
    registry behind it: a sentence about 'Udayeśvara' is grounded by a passage
    that only ever says 'Nīlakaṇṭheśvara', which folding alone cannot know.
    """
    toks, nums, blob = _pack_vocabulary(passages, entities)
    folded_blob = " ".join(fold(w) for w in WORD_RE.findall(blob))
    bad = []
    for t in proper_nouns(text):
        if entities is not None:
            if not entities.attested(t, toks, folded_blob):
                bad.append(t)
        elif fold(t) not in toks:
            bad.append(t)
    for n in numerals(text):
        if n not in nums:
            bad.append(n)
    return sorted(set(bad), key=lambda x: (-len(x), x))


@dataclass
class PackReport:
    """Deterministic validation of an evidence pack, BEFORE any prose exists.

    Everything here is ordinary code, not a model call. That is the point:
    whether a passage has a source, whether that source resolves to a real
    citation, whether two passages are the same text — these are facts about
    the pack, and asking a language model to establish them would be slower,
    costlier and less reliable than reading the JSON.

    The stage it guards is the one the pipeline never had. Retrieval could
    return a pack with unresolvable sources or empty passages and drafting would
    proceed regardless, discovering the problem only as a strange sentence three
    stages later.
    """
    checks: list = field(default_factory=list)      # [{name, status, detail}]
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    source_references: dict = field(default_factory=dict)   # source -> n passages
    unresolved_sources: list = field(default_factory=list)
    duplicate_passages: list = field(default_factory=list)
    thin_subtopics: list = field(default_factory=list)
    gap_subtopics: list = field(default_factory=list)
    incomplete_metadata: list = field(default_factory=list)
    n_passages: int = 0
    n_subtopics: int = 0

    @property
    def status(self):
        if self.errors:
            return "fail"
        return "warn" if self.warnings else "ok"

    @property
    def usable_passages(self):
        return self.n_passages - len(self.duplicate_passages)

    def check(self, name, ok, detail=""):
        self.checks.append({"name": name, "status": "ok" if ok else "fail",
                            "detail": detail})
        return ok

    def summary(self):
        return (f"{self.usable_passages}/{self.n_passages} passages usable from "
                f"{len(self.source_references)} sources; "
                f"{len(self.gap_subtopics)} gap, {len(self.thin_subtopics)} thin")

    def to_dict(self):
        return {"status": self.status, "checks": self.checks,
                "warnings": self.warnings, "errors": self.errors,
                "source_references": self.source_references,
                "unresolved_sources": self.unresolved_sources,
                "duplicate_passages": self.duplicate_passages,
                "thin_subtopics": self.thin_subtopics,
                "gap_subtopics": self.gap_subtopics,
                "incomplete_metadata": self.incomplete_metadata,
                "n_passages": self.n_passages, "n_subtopics": self.n_subtopics}


def validate_pack(brief, min_passages=3, require_pages=False):
    """Check an evidence pack before it becomes chapter prose.

    Returns a PackReport. An error means the pack should not be drafted from;
    a warning means it can be, but the chapter will be weaker in a specific,
    named way.
    """
    import hashlib
    import sources as src_mod

    rep = PackReport()
    subs = brief.get("subtopics") or []
    rep.n_subtopics = len(subs)

    rep.check("pack has sub-topics", bool(subs),
              "" if subs else "the pack contains no sub-topics at all")
    if not subs:
        rep.errors.append("evidence pack is empty — nothing to draft from")
        return rep

    seen_text, seen_ids = {}, set()
    for s in subs:
        key = s.get("key", "?")
        passages = s.get("passages") or []
        rep.n_passages += len(passages)

        status = (s.get("status") or "").upper()
        if status == "GAP" or not passages:
            rep.gap_subtopics.append(key)
        elif status in ("THIN", "SINGLE-SOURCE") or len(passages) < min_passages:
            rep.thin_subtopics.append(key)

        for p in passages:
            pid = p.get("id")
            if not pid or pid in seen_ids:
                rep.errors.append(f"{key}: duplicate or missing passage id {pid!r}")
            seen_ids.add(pid)

            text = (p.get("text") or "").strip()
            if not text:
                rep.errors.append(f"{key}/{pid}: passage has no text")
                continue

            src = p.get("source")
            if not src:
                rep.errors.append(f"{key}/{pid}: passage has no source")
            else:
                rep.source_references[src] = rep.source_references.get(src, 0) + 1
                # Does the source resolve to a real citation? sources.py is the
                # authority; an unmapped file degrades to a filename in the
                # endnotes, which is exactly the untraceable citation the
                # lookup table exists to prevent.
                if src in src_mod.unmapped([src]):
                    if src not in rep.unresolved_sources:
                        rep.unresolved_sources.append(src)

            if require_pages and not p.get("page_start"):
                rep.incomplete_metadata.append(f"{pid} ({src}): no page number")

            # Exact-duplicate passages inside one pack waste the context window
            # and let one passage look like corroboration of itself.
            h = hashlib.blake2b(text.encode("utf-8"), digest_size=8).hexdigest()
            if h in seen_text:
                rep.duplicate_passages.append({"id": pid, "duplicate_of": seen_text[h],
                                               "source": src})
            else:
                seen_text[h] = pid

    rep.check("every passage has text and a source", not rep.errors)
    rep.check("all sources resolve to citations", not rep.unresolved_sources,
              ", ".join(rep.unresolved_sources[:3]))
    rep.check("no duplicate passages", not rep.duplicate_passages,
              f"{len(rep.duplicate_passages)} duplicate(s)")
    rep.check("every sub-topic has evidence", not rep.gap_subtopics,
              ", ".join(rep.gap_subtopics[:5]))

    if rep.unresolved_sources:
        rep.warnings.append(
            f"{len(rep.unresolved_sources)} source(s) not in sources.py; their "
            f"endnotes will fall back to filenames: "
            f"{', '.join(rep.unresolved_sources[:3])}")
    if rep.duplicate_passages:
        rep.warnings.append(f"{len(rep.duplicate_passages)} duplicate passage(s) "
                            f"in the pack")
    if rep.gap_subtopics:
        rep.warnings.append(f"{len(rep.gap_subtopics)} sub-topic(s) have no evidence "
                            f"and must be written as gaps: "
                            f"{', '.join(rep.gap_subtopics[:4])}")
    if rep.thin_subtopics:
        rep.warnings.append(f"{len(rep.thin_subtopics)} sub-topic(s) thinly covered: "
                            f"{', '.join(rep.thin_subtopics[:4])}")
    if rep.incomplete_metadata:
        rep.warnings.append(f"{len(rep.incomplete_metadata)} passage(s) lack page numbers")

    # A pack with no usable evidence at all is an error, not a warning: drafting
    # from it would produce prose with nothing behind it.
    if rep.usable_passages == 0:
        rep.errors.append("no usable passages in the entire pack")
    return rep


def _windows(text, words_per=550):
    """Split prose at paragraph boundaries into decomposition-sized windows.

    A 1,800-word section decomposes into 60-100 atomic claims, each carrying its
    source sentence verbatim — comfortably past a 6,000-token ceiling, which is
    how the first run of this stage died after successfully drafting the whole
    chapter. Windowing bounds the output per call instead of raising the ceiling
    and hoping, and it parallelises for free.
    """
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, buf, n = [], [], 0
    for p in paras:
        w = len(p.split())
        if buf and n + w > words_per:
            out.append("\n\n".join(buf))
            buf, n = [], 0
        buf.append(p)
        n += w
    if buf:
        out.append("\n\n".join(buf))
    return out or [text]


def decompose(client, model, text, max_tokens=8000, words_per=550):
    """Prose -> atomic claims, windowed so no single response can be truncated."""
    wins = _windows(text, words_per)

    def one(w):
        msgs = [{"role": "system", "content": DECOMPOSE_SYSTEM},
                {"role": "user", "content": w}]
        return complete_json(client, model, msgs, max_tokens=max_tokens,
                             temperature=0.0, quiet=True)

    def failed(w, e):
        print(f"    claim decomposition failed on a {len(w.split())}-word window "
              f"({type(e).__name__})", file=sys.stderr)
        return {"claims": []}

    out = []
    for data in parallel(one, wins, workers=3, stagger=0.4, on_error=failed):
        for c in (data or {}).get("claims", []):
            if c.get("text"):
                # Ids are reassigned across windows: each call numbers from 1,
                # so keeping the model's ids would collide and silently merge
                # one window's verdicts into another's claims.
                out.append({"id": len(out) + 1, "text": c["text"],
                            "kind": c.get("kind", "factual"), "quote": c.get("quote", "")})
    return out


def entail(client, model, claims, passages, batch=None):
    """Check factual claims against the pack. Returns {claim_id: result}."""
    batch = batch or CFG.verify.claims_per_call
    if not claims:
        return {}
    listing = "\n\n".join(
        f"[{p.get('id', 'E?')}] ({p.get('source', '?')}"
        + (f", p. {p['page_start']}" if p.get("page_start") else "") + ")\n"
        + p.get("text", "")[:1800]
        for p in passages)

    groups = [claims[i:i + batch] for i in range(0, len(claims), batch)]

    def one(g):
        msgs = [{"role": "system", "content": ENTAIL_SYSTEM},
                {"role": "user", "content":
                    f"SOURCE PASSAGES:\n{listing[:60000]}\n\n"
                    f"CLAIMS:\n" + json.dumps(
                        [{"id": c["id"], "text": c["text"]} for c in g], ensure_ascii=False)}]
        return complete_json(client, model, msgs, max_tokens=3000, temperature=0.0, quiet=True)

    def failed(g, e):
        # A failed batch must not be read as "supported" — that would let an API
        # error smuggle unverified claims into the manuscript. Treat as unknown.
        print(f"    entailment batch failed ({type(e).__name__}); "
              f"{len(g)} claim(s) left unverified", file=sys.stderr)
        return {"results": [{"id": c["id"], "verdict": "unverified"} for c in g]}

    out = {}
    for data in parallel(one, groups, workers=4, stagger=0.3, on_error=failed):
        for r in (data or {}).get("results", []):
            out[int(r.get("id", -1))] = r
    return out


def verify_section(client, text, passages, entities=None, model=None, cfg=None):
    """Full verification of one drafted section against its own evidence pack."""
    cfg = cfg or CFG
    model = model or cfg.verify.model
    rep = Report()

    rep.ungrounded_terms = ungrounded_terms(text, passages, entities)

    rep.claims = decompose(client, model, text)
    factual = [c for c in rep.claims if c["kind"] == "factual"]
    rep.skipped = [c for c in rep.claims if c["kind"] != "factual"]

    verdicts = entail(client, model, factual, passages)
    for c in factual:
        v = verdicts.get(c["id"], {})
        verdict = v.get("verdict", "unverified")
        rec = {**c, **{k: v.get(k) for k in ("passage_ids", "missing", "conflict")}}
        if verdict == "supported":
            rep.supported.append(rec)
        elif verdict == "partial":
            rep.partial.append(rec)
        elif verdict == "contradicted":
            rep.contradicted.append(rec)
        elif verdict == "unsupported":
            rep.unsupported.append(rec)
        else:
            # UNVERIFIED IS ITS OWN STATE. It is not "unsupported", and the
            # difference is not pedantic: filing it under unsupported made the
            # pipeline delete 127 claims from chapter 1 because the account's
            # API quota had run out. The verifier learned nothing about those
            # claims; treating silence as a guilty verdict destroys correct,
            # well-evidenced prose whenever the network or the billing does.
            #
            # So: never cut, never counted against faithfulness, always
            # reported. An unjudged claim is a gap in the CHECK, not in the
            # evidence.
            rep.unverified.append({**rec, "missing": v.get("missing")
                                   or "not verified (verifier unavailable)"})
    return rep


REPAIR_SYSTEM = """You are revising a drafted section of a scholarly book so that every factual \
assertion is backed by the supplied sources. This is a REVISION, not a rewrite and not an \
expansion.

You will be given the section, and a list of specific problems found in it.

For each problem, prefer these in ORDER. Only fall to the next when the one above cannot work:

  1. HEDGE — rewrite the sentence so it says only what the sources support. Drop the unattested \
date, number or name and keep the sentence. This should handle the large majority.
  2. CUT — delete the assertion entirely, if the section reads fine without it.
  3. MARK — replace it with {gap}, ONLY as a last resort.

For a CONTRADICTED claim, correct it to what the sources actually say. Never simply delete a \
contradiction — the reader needs the right fact, not silence.

THE MARKER HAS STRICT RULES. It is a signal to the author that a whole point is missing, not a \
redaction tool:
  - It may replace ONLY a complete sentence, or a complete clause that makes its own factual \
point. Never a noun phrase, never an adjective, never a fragment mid-sentence.
  - It must NEVER appear inside a heading.
  - Use it at most a handful of times in the whole section. A section peppered with markers is \
worse than one that simply says less — the reader cannot read around them.
  - Prose describing what a source plainly shows — a wall's condition, a building's material, \
where something stands — is supported. Do not mark ordinary descriptive writing as missing \
merely because the evidence phrases it differently.

Rules:
  - Change nothing else. Sentences not named in the problem list must survive verbatim.
  - Do NOT add new facts, new examples or new comparanda. An earlier version of this pipeline \
was given an unconstrained editing pass and responded by inflating the text 59% and inventing \
temple comparisons; that is the specific behaviour this instruction forbids.
  - Keep the [E12]-style citation markers exactly where they are on surviving text.
  - Preserve every heading exactly as written.
  - The result must be no longer than the input.

Return the full revised section as markdown. No preamble, no commentary."""


def repair_prompt(text, report, gap_marker=None):
    """The messages for one constrained repair pass."""
    gap = gap_marker or CFG.verify.gap_marker
    problems = []
    for c in report.contradicted:
        problems.append(f"- CONTRADICTED: \"{c['text']}\"\n  sources say instead: "
                        f"{c.get('conflict') or '(see pack)'}")
    for c in report.unsupported:
        problems.append(f"- UNSUPPORTED: \"{c['text']}\"\n  nothing in the pack establishes this"
                        + (f" ({c['missing']})" if c.get("missing") else ""))
    for c in report.partial:
        problems.append(f"- PARTLY UNSUPPORTED: \"{c['text']}\"\n  unattested element: "
                        f"{c.get('missing') or 'unclear'}")
    if report.ungrounded_terms:
        problems.append("- These names/numbers appear nowhere in the evidence and must be "
                        "removed or hedged: " + ", ".join(report.ungrounded_terms[:40]))
    return [
        {"role": "system", "content": REPAIR_SYSTEM.replace("{gap}", gap)},
        {"role": "user", "content": f"PROBLEMS FOUND:\n" + "\n".join(problems)
                                    + f"\n\n---\n\nSECTION TO REVISE:\n\n{text}"},
    ]


def repair(client, text, report, passages, entities=None, model=None, cfg=None, rounds=None):
    """VERIFY -> REPAIR loop. Returns (text, final_report, history)."""
    from llm import complete
    cfg = cfg or CFG
    model = model or cfg.verify.model
    rounds = cfg.verify.max_repairs if rounds is None else rounds
    history = [report.summary()]

    for _ in range(rounds):
        if not report.problems() and not report.ungrounded_terms:
            break
        words_in = len(text.split())
        # Budget tied to the input, per v1's stitch-pass finding: an editing
        # call with a free budget expands instead of revising.
        budget = int(words_in * cfg.verify.repair_token_ratio) + 400
        try:
            new_text, _ = complete(client, model, repair_prompt(text, report),
                                   max_tokens=budget, temperature=0.2)
        except Exception as e:                        # noqa: BLE001
            history.append(f"repair failed: {type(e).__name__}")
            break
        if len(new_text.split()) > words_in * 1.15:
            history.append(f"repair rejected: grew {words_in} -> {len(new_text.split())} words")
            break

        # A repair that shreds the prose is worse than the ungrounded prose it
        # replaced. The first run of this loop returned a chapter carrying 133
        # gap markers — one every 56 words, including one inside a section
        # heading — which is unreadable and unfixable by hand. Reject it on the
        # same principle the length check already applies: a revision that
        # damages the text more than it repairs it is not a revision.
        gap = cfg.verify.gap_marker
        added = new_text.count(gap) - text.count(gap)
        cap = cfg.verify.get("max_gaps_per_section", 6)
        in_heading = re.search(rf"(?m)^#{{1,6}}.*{re.escape(gap)}", new_text)
        if added > cap or in_heading:
            why = ("put a gap marker inside a heading" if in_heading
                   else f"added {added} gap markers (cap {cap})")
            history.append(f"repair rejected: {why}")
            break
        text = new_text
        report = verify_section(client, text, passages, entities, model, cfg)
        history.append(report.summary())

    return text, report, history


def cut_unsupported(text, report, gap_marker=None):
    """Last resort: replace still-unsupported sentences with the gap marker.

    This is the gate. After the repair budget is spent, anything still
    unsupported does not ship as prose — §5.1. Contradicted claims are NOT cut,
    because a contradiction needs a correction and cutting it hides an error.
    """
    gap = gap_marker or CFG.verify.gap_marker
    out, cut = text, 0
    cap = CFG.verify.get("max_gaps_per_section", 6)
    for c in report.unsupported:
        if cut >= cap:
            break
        quote = (c.get("quote") or "").strip()
        # Whole sentences only. A short quote is a fragment, and swapping a
        # fragment for the marker leaves a sentence that reads as damage rather
        # than as a flagged gap.
        if not quote or len(quote.split()) < 6 or quote not in out:
            continue
        if re.search(r"(?m)^#{1,6}[^\n]*" + re.escape(quote[:40]), out):
            continue                     # never perforate a heading
        out = out.replace(quote, gap, 1)
        cut += 1
    return re.sub(rf"(?:{re.escape(gap)}\s*){{2,}}", gap + " ", out), cut


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Verify drafted prose against its evidence pack")
    ap.add_argument("draft", nargs="?", help="path to a drafted chapter")
    ap.add_argument("--chapter", type=int, help="which evidence pack to check against")
    ap.add_argument("--all", action="store_true", help="every chapter in --dir")
    ap.add_argument("--dir", default="chapter_drafts")
    ap.add_argument("--out", default="book/_verify")
    ap.add_argument("--repair", action="store_true", help="run the repair loop and rewrite")
    args = ap.parse_args()

    from entities import EntityIndex
    ix = EntityIndex.load()
    client = get_client()
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    jobs = []
    if args.all:
        for p in sorted(Path(args.dir).glob("chapter-*.md")):
            m = re.search(r"chapter-(\d+)", p.name)
            if m:
                jobs.append((int(m.group(1)), p))
    elif args.draft:
        n = args.chapter
        if n is None:
            m = re.search(r"(\d+)", Path(args.draft).stem)
            n = int(m.group(1)) if m else None
        jobs.append((n, Path(args.draft)))
    else:
        ap.error("give a draft path or --all")

    print(f"{'ch':>3s} {'claims':>7s} {'fact':>5s} {'supp':>5s} {'part':>5s} "
          f"{'unsup':>6s} {'contra':>7s} {'faith':>6s}  ungrounded")
    print("-" * 78)
    for n, path in jobs:
        pack_path = EVID / f"ch{n:02d}.json"
        if not pack_path.exists():
            print(f"{n:3d}  no evidence pack at {pack_path}"); continue
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        passages = [p for s in pack["subtopics"] for p in s["passages"]]
        text = path.read_text(encoding="utf-8")

        rep = verify_section(client, text, passages, entities=ix)
        if args.repair:
            text, rep, hist = repair(client, text, rep, passages, entities=ix)
            path.write_text(text, encoding="utf-8")
            print(f"    repair: {' -> '.join(hist)}")

        print(f"{n:3d} {len(rep.claims):7d} {rep.checked:5d} {len(rep.supported):5d} "
              f"{len(rep.partial):5d} {len(rep.unsupported):6d} {len(rep.contradicted):7d} "
              f"{rep.rate * 100:5.0f}%  {len(rep.ungrounded_terms)}")
        (outdir / f"ch{n:02d}.json").write_text(json.dumps({
            "chapter": n, "rate": rep.rate, "summary": rep.summary(),
            "ungrounded_terms": rep.ungrounded_terms,
            "unsupported": rep.unsupported, "contradicted": rep.contradicted,
            "partial": rep.partial}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
