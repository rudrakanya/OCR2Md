"""Phase 2: draft Chapter 1 section by section with the OpenAI API, then one stitching call.

  python -I "drafting/ch01/draft.py" --dry-run      # build every prompt, count tokens, estimate cost; no API calls
  python -I "drafting/ch01/draft.py"                # draft (needs approval; budget-guarded)
  python -I "drafting/ch01/draft.py" --revise 1.3 --problems problems.json   # Phase 3 revision of one section

Key: OPENAI_API_KEY from the environment or the project .env (never printed or logged).
Model: OPENAI_MODEL env var overrides; otherwise model_choice.json (chosen in Phase 1 from client.models.list()
and OpenAI's model page). Every request/response (minus the key) is logged to api_log/ with token counts.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
D = ROOT / "drafting" / "ch02"
LOG = D / "api_log"
BUDGET_USD = 5.00
SECTIONS = ["2.1", "2.2", "2.3", "2.4", "2.5"]
# Assumed hidden reasoning tokens per call at "high" effort, used only for the pre-flight estimate.
REASONING_ALLOWANCE = {"section": 8000, "stitch": 10000, "revise": 8000}


# ---------------------------------------------------------------------------------------------
def load_key():
    if not os.getenv("OPENAI_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not found in the environment or .env")


def model_and_price():
    choice = json.loads((D / "model_choice.json").read_text(encoding="utf-8"))
    model = os.getenv("OPENAI_MODEL") or choice["model"]
    price = choice["prices_per_1M"].get(model)
    return model, price, choice


def ntok(text: str) -> int:
    try:
        import tiktoken
        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return len(text) // 4


# ---------------------------------------------------------------------------------------------
def outline_sections():
    text = (D / "ch01_outline_refined.md").read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## 1\.\d)", text)
    head = parts[0]
    secs = {}
    for p in parts[1:]:
        k = re.match(r"## (1\.\d)", p).group(1)
        secs[k] = p.split("\n## Word targets")[0].strip()
    targets = {k: int(re.search(r"·\s*([\d,]+)\s*w\)|\((\d+) w\)", secs[k]).group(1 if re.search(r"·\s*([\d,]+)\s*w\)", secs[k]) else 2).replace(",", ""))
               for k in secs}
    titles = {k: re.match(r"## (1\.\d [^*\n(]+)", secs[k]).group(1).strip() for k in secs}
    return text, head, secs, targets, titles


def pack():
    return {i["id"]: i for i in json.loads((D / "evidence_pack.json").read_text(encoding="utf-8"))}


def section_evidence(sec, secs, P, cov):
    assigned = [i for i in cov["per_section"][sec]]
    subs = {P[i]["sub"] for i in assigned}
    used_anywhere = set(cov["used"])
    extra = [i["id"] for i in P.values() if i["id"] not in used_anywhere and i["strength"] == "direct"
             and i["sub"] in subs][:10]
    return assigned, extra


def fmt_item(i):
    flags = [f for f in i["flags"] if not f.startswith("also")]
    lines = [f"[{i['id']}] {i['strength'].upper()} · {i['book_title']} · {i['page']}"
             + (f" · flags: {', '.join(flags)}" if flags else "")]
    lines.append("QUOTE (verbatim; only this text may be quoted): " + " ".join(i["quote"].split()))
    if i.get("gloss"):
        lines.append("ENGLISH RENDERING (translation, not a quotation; mark '(translation)' if used): " + i["gloss"])
    if i.get("note"):
        lines.append("Mapping note (orientation only; not citable, add nothing from it): " + i["note"])
    return "\n".join(lines)


WRITER_BRIEF = """You are drafting Chapter 1 of a book on Udaypur (Vidisha district, Madhya Pradesh, India) for informed general readers.

VOICE: narrative non-fiction. Authoritative, warm and concrete. No academic throat-clearing ("It is important to note", "This chapter will examine"), no tourist-brochure tone ("nestled", "timeless", "mists of time", "treasure trove", "steeped in history", "bears silent witness"). Open sections on an image, not a thesis. Let concrete nouns carry the weight. Vary sentence length; a short sentence after a long one lands a fact. Name people. State ironies once, flatly. No stacked rhetorical questions. No superlatives borrowed from sources unless quoted and attributed. Present tense belongs only to section 1.1 (the present-day arrival); medieval events are told in the past tense.

SPELLING AND NAMES: British/Indian English. The town is "Udaypur" throughout; use "Udayapura" only when speaking of the name in the records. Distinguish it explicitly from Udaipur in Rajasthan where the brief asks. Apply diacritics consistently: Udayāditya, Paramāra, Udayeśvara, Nīlakaṇṭheśvara, Udayasamudra, praśasti, Bhūmija, Lūṇapasāka, Devapāla, liṅga, darśan, pūjā. Italicise Sanskrit/Persian terms on first use and gloss them in half a clause. The testimony book is *Jagta Hua Kasba*.

FACTS: Use ONLY facts contained in the supplied evidence items. Do not add dates, names, numbers, places or claims from general knowledge — not even well-known ones. If the evidence does not support a point in the brief, leave it out or state it as an open question. Mapping notes are orientation only: never cite them and never take facts from them.

CITATIONS: Every sentence that states a fact ends with its evidence ID(s) in square brackets, e.g. [C01-GANGULY-006] or [C01-GAZ-007; C01-MADHYABHARAT-002]. Use only IDs supplied to you. Purely transitional or reflective sentences that state no fact need no ID.

QUOTATIONS: A direct quotation must be copied character-for-character from an item's QUOTE, inside double quotation marks, followed by its ID. Use about 2–4 short, purposeful quotations per section; prefer paraphrase. Never quote an item flagged ⚠ (paraphrase it cautiously and cite). Hindi or Sanskrit items are paraphrased in English or quoted in English with "(translation)" after the quotation marks, and still cited.

ROUTING (binding editorial canon): *Jagta Hua Kasba* (IDs containing JAGTA) is testimony: use it for present-day observation, folklore, oral tradition and the author's own views, always attributed in the same sentence ("the author of *Jagta Hua Kasba* writes…", "residents told the author…"); never use it as the source of a medieval fact or a measurement. Its page numbers are approximate; build no precise claim on them. The district Gazetteer (IDs containing GAZ) is for the modern setting, not for medieval facts. A praśasti is royal panegyric: present what it claims as its claim.

CONFLICTS: Where sources disagree, present the disagreement as a disagreement, naming who says what ("Ganguly places…, while the INTACH report gives…"). Never pick a winner.

HAND-OFFS: Topics that belong to later chapters are mentioned briefly and signposted ("Chapter 6 returns to the inscriptions"), not developed.

BANNED WORDS AND MOVES: never use "nestled", "tapestry", "testament to", "stands as", "rich history", "steeped in", "delve", "bustling", "timeless", "hidden gem", "in conclusion", and no rhetorical questions as filler. The narrator never uses superlatives (no "finest", "greatest", "most beautiful", "unrivalled" in your own voice).

SIGNIFICANCE: across the whole chapter at most 3 short, attributed scholarly assessments ("Krishna Deva called it…"), each cited; only in the section whose brief asks for them.

SPECIFIC OVER GENERAL: every paragraph contains at least one concrete, cited detail — a name, date, measurement, place or quoted phrase.

OPENINGS: the section opens on a concrete image or fact drawn from the evidence, never on a summary or thesis.

THE TESTIMONY AUTHOR: name the author of *Jagta Hua Kasba* once in the chapter as Vijay Manohar Tiwari (this is the editor's knowledge and needs no citation); afterwards write "the author" or "Tiwari". Never use a gendered pronoun for the author. If an earlier section (see the summary) has already named Tiwari, do not re-introduce the full name.

BORROWED ITEMS: items flagged "borrowed" come from other chapters' evidence; use them only for the brief overview the outline asks for, and cite them like any other item.

OUTPUT FORMAT: Return the section text in Markdown, beginning with its heading line exactly as given ("## <number> <title>"), then a line containing only "---SUMMARY---", then a 150–250 word plain summary of what the section said (for continuity; no IDs)."""


def section_prompt(sec, full_outline, secs, targets, titles, P, cov, running_summary):
    assigned, extra = section_evidence(sec, secs, P, cov)
    ev = "\n\n".join(fmt_item(P[i]) for i in assigned)
    ev_extra = "\n\n".join(fmt_item(P[i]) for i in extra)
    t = targets[sec]
    user = f"""THE WHOLE CHAPTER OUTLINE (for the arc; draft only the section named below):
{full_outline}

SUMMARY OF SECTIONS ALREADY DRAFTED:
{running_summary or '(none — this is the first section)'}

SECTION TO DRAFT NOW: {titles[sec]}
Section brief (from the outline):
{secs[sec]}

WORD TARGET: {t} words (acceptable range {int(t * 0.9)}–{int(t * 1.1)}), not counting bracketed IDs.

EVIDENCE ASSIGNED TO THIS SECTION ({len(assigned)} items):
{ev}

FURTHER RELEVANT ITEMS YOU MAY USE ({len(extra)} items):
{ev_extra or '(none)'}
"""
    return WRITER_BRIEF, user, assigned + extra


STITCH_BRIEF = """You are the final editor of Chapter 1 of a book on Udaypur. You receive the five drafted sections.
Smooth the transitions between sections and remove repetition across sections. Keep each section's heading, order and approximate length.
STRICT RULES: Do not add any fact, date, name, number or claim. Do not remove, alter, move to another claim, or invent any bracketed evidence ID — every factual sentence must keep its IDs exactly. Do not change any text inside quotation marks. You may delete a repeated sentence together with its IDs, shorten, reorder within a section, and rewrite connective wording. British/Indian English; keep all diacritics.
Return only the full chapter in Markdown."""


# ---------------------------------------------------------------------------------------------
class Client:
    def __init__(self, dry):
        self.dry = dry
        self.spent = 0.0
        self.calls = []
        if not dry:
            load_key()
            from openai import OpenAI
            self.c = OpenAI()
        self.model, self.price, self.choice = model_and_price()
        if self.price is None and not dry:
            sys.exit(f"No price on record for model {self.model}; add it to model_choice.json before running.")

    def est(self, system, user, kind, out_words):
        tin = ntok(system) + ntok(user)
        tout = int(out_words * 1.45) + REASONING_ALLOWANCE[kind]
        p = self.price or {"input": 0, "output": 0}
        return tin, tout, tin / 1e6 * p["input"] + tout / 1e6 * p["output"]

    def call(self, name, system, user, kind, out_words, max_out):
        tin, tout, cost = self.est(system, user, kind, out_words)
        rec = {"name": name, "kind": kind, "model": self.model, "est_input_tokens": tin,
               "est_output_tokens": tout, "est_cost_usd": round(cost, 4)}
        if self.dry:
            self.calls.append(rec)
            return None
        if self.spent + cost > BUDGET_USD:
            sys.exit(f"STOP: call {name} would take spend to ${self.spent + cost:.2f} (> ${BUDGET_USD}). Ask before continuing.")
        params = {"model": self.model, "input": [{"role": "system", "content": system},
                                                 {"role": "user", "content": user}],
                  "max_output_tokens": max_out}
        if self.choice.get("reasoning_effort"):
            params["reasoning"] = {"effort": self.choice["reasoning_effort"]}
        t0 = time.time()
        r = self.c.responses.create(**params)
        u = r.usage
        rtok = getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", None)
        cost = u.input_tokens / 1e6 * self.price["input"] + u.output_tokens / 1e6 * self.price["output"]
        self.spent += cost
        rec.update(input_tokens=u.input_tokens, output_tokens=u.output_tokens, reasoning_tokens=rtok,
                   cost_usd=round(cost, 4), seconds=round(time.time() - t0, 1), response_id=r.id,
                   status=getattr(r, "status", None))
        LOG.mkdir(exist_ok=True)
        n = len(list(LOG.glob("*.json"))) + 1
        (LOG / f"{n:02d}_{name}.json").write_text(json.dumps(
            {"meta": rec, "request": {k: v for k, v in params.items()}, "response_text": r.output_text},
            ensure_ascii=False, indent=1), encoding="utf-8")
        self.calls.append(rec)
        return r.output_text


def split_summary(text):
    if "---SUMMARY---" in text:
        body, summ = text.split("---SUMMARY---", 1)
        return body.strip(), summ.strip()
    return text.strip(), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    full_outline, head, secs, targets, titles = outline_sections()
    P = pack()
    cov = json.loads((D / "coverage.json").read_text(encoding="utf-8"))
    cl = Client(a.dry_run)
    drafts, summaries, used = {}, [], {}
    for sec in SECTIONS:
        system, user, ids = section_prompt(sec, full_outline, secs, targets, titles, P, cov, "\n".join(summaries))
        used[sec] = ids
        out = cl.call(f"section_{sec}", system, user, "section", targets[sec] + 250, 30000)
        if out is None:
            summaries.append("(about 200 words of summary of section %s)" % sec + " lorem" * 200)
            drafts[sec] = "x " * targets[sec] + " [C01-GANGULY-006]" * (targets[sec] // 18)
            continue
        body, summ = split_summary(out)
        drafts[sec] = body
        summaries.append(f"{titles[sec]}: {summ}")
        (D / f"draft_section_{sec}.md").write_text(body, encoding="utf-8")
    joined = "\n\n".join(drafts[s] for s in SECTIONS)
    stitch_user = f"CHAPTER OUTLINE (for reference):\n{full_outline}\n\nDRAFT TO EDIT:\n{joined}"
    out = cl.call("stitch", STITCH_BRIEF, stitch_user, "stitch", sum(targets.values()) + 300, 40000)
    if out is not None:
        (D / "ch01_draft_v1.md").write_text(out.strip() + "\n", encoding="utf-8")
        (D / "ch01_draft_presitch.md").write_text(joined + "\n", encoding="utf-8")
    (D / "section_evidence.json").write_text(json.dumps(used, indent=1), encoding="utf-8")
    tot_in = sum(c.get("input_tokens", c["est_input_tokens"]) for c in cl.calls)
    tot_out = sum(c.get("output_tokens", c["est_output_tokens"]) for c in cl.calls)
    tot = sum(c.get("cost_usd", c["est_cost_usd"]) for c in cl.calls)
    report = {"model": cl.model, "price_per_1M": cl.price, "calls": cl.calls,
              "total_input_tokens": tot_in, "total_output_tokens": tot_out, "total_cost_usd": round(tot, 4),
              "dry_run": a.dry_run}
    (D / ("cost_estimate.json" if a.dry_run else "cost_actual.json")).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
