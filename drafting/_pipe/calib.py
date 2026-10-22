"""Phase 1 calibration (round 3; points written into the outline): rewrite paragraphs of the current draft in the authored voice — style brief (no
exemplars), thesis, the section's interpretive claims, the [INT:function] rules — check them in code, allow one repair
pass when the checks flag a problem (as the pipeline's revision step would), and write them beside the original and
the round-1 calibration, listing each interpretive sentence with the test it claims to pass.

  set UDAY_CFG=...; python -u -I drafting/_pipe/calib.py "<old section>:<paragraph no.>=<new section>:P<n>" …
Output: chNN_calibration.md in the chapter folder (earlier rounds kept as chNN_calibration_round1.md / _round2.md).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as p1  # noqa: E402
import pipeline2 as p2  # noqa: E402

SYS = """You rewrite one paragraph of a history chapter about Udaypur as an accomplished historian of India would, following the STYLE BRIEF and WRITER BRIEF exactly.
- The paragraph advances one idea: state the governing claim early and close on its consequence.
- Combine the facts that serve that idea into few sentences, IDs at the end of the clause or sentence they support; never one fact per sentence.
- Long sentences carry evidence and qualification; a short sentence lands the point.
- The paragraph exists to make its written POINT (given below with its function). Arrange the cited facts so they lead to it, and express the point as the paragraph's interpretive sentence(s), ending with the given [INT:function] label. You may sharpen its wording; you may not change, weaken or strengthen the claim. No new facts in interpretive sentences.
- Place the interpretive sentence where the argument turns (early as the governing claim, between two pieces of evidence, or last); a paragraph that turns on a tension may carry two.
- Vijay Manohar Tiwari is a witness and author of testimony, never "a visitor".
- Settled ranges stay ranges with both items cited (Udaypur lies about 13–16 km from Ganj Basoda and 55–70 km from Vidisha).
- Every name and number must appear in an item cited in the same sentence. A source disagreement goes into {{note: … [IDs]}}.
Length 130–200 words. Return only the paragraph."""

REPAIR = """Revise this paragraph to fix ONLY the listed code-check problems, keeping its argument, voice and length (130–200 words). Add no facts. Cite each name and number with an item that contains it.
Return only the paragraph."""


def earlier(spec_idx, rnd=2):
    p = C.D / f"ch{C.CH:02d}_calibration_round{rnd}.md"
    if not p.exists():
        return ""
    pat = r"### Rewritten\n\n(.*?)\n\n\*Interpretive" if rnd == 1 else r"### Round 2\n\n(.*?)\n\n\*Words"
    rew = re.findall(pat, p.read_text(encoding="utf-8"), re.S)
    return rew[spec_idx] if spec_idx < len(rew) else ""


def problems(rep):
    out = [f"not supported by the cited items: {x}" for x in rep["fabrication"]] + [f"uncited: {x}" for x in rep["uncited_claims"]]
    out += [f"quote not verbatim: {q['quote']}" for q in rep["nonverbatim_quotes"]] + rep["interpretive_issues"] + rep["fact_per_sentence"] + rep["settled_issues"]
    out += [f"generic significance: {x}" for x in rep["generic"]] + [f"source-led: {r['sentence']}" for rows in rep["subject_detail"].values() for r in rows]
    return out


def main(specs):
    P = va.load_pack()
    _, secs, targets, titles = va.load_outline()
    base = va.split_sections(C.BASELINE.read_text(encoding="utf-8"))
    R = rn.Run(False)
    s0 = R.spent
    md = [f"# Chapter {C.CH} — calibration paragraphs (round 3)\n",
          "The same paragraphs as rounds 1 and 2, rewritten with a written **Point** for each paragraph taken from the outline; the writer builds "
          "the paragraph to deliver that point as its interpretive sentence(s).\n\n"
          "Each paragraph is shown three ways: original (`" + C.BASELINE.name + "`), round 2, round 3.\n"
          "Interpretive sentences are labelled **⟨INT:function⟩**; discursive notes are shown as *[note: …]*.\n"]
    for n, spec in enumerate(specs):
        old, new = spec.split("=")
        old_sec, k = old.split(":")
        new_sec, pk = new.split(":")
        para = va.paragraphs(base[old_sec])[int(k) - 1].strip()
        pt = next(x for x in p2.points_of(secs[new_sec]) if x[0] == pk)
        blk = re.search(rf"\*\*{pk} — .*?\n\s*\(([^)]*)\)", secs[new_sec], re.S)
        plan_ids = re.findall(r"C\d\d-[A-Z0-9-]+-\d{3}", blk.group(1)) if blk else []
        ids = [i for i in dict.fromkeys(va.ids_in(para) + plan_ids + p1.section_ids(p2.SEC_BRIEF.get(new_sec, ""), P)) if i in P]
        u = (p2.STYLE_BLOCK + f"WRITER BRIEF:\n{p2.WRITER_BRIEF}\n\nCHAPTER THESIS:\n{p2.THESIS}\n\nSECTION ({titles.get(new_sec, new_sec)}) CLAIMS:\n{p2.SEC_BRIEF.get(new_sec, '')}\n\n"
             f"THIS PARAGRAPH'S POINT [INT:{pt[2]}]: {pt[3]}\n\n"
             "EVIDENCE:\n" + "\n\n".join(p1.fmt_item(P[i]) for i in ids) + f"\n\n=== PARAGRAPH TO REWRITE ===\n{para}")
        new = (R.call(f"calib3_{old_sec}_{k}", 0, "candidate", SYS, u, 220) or "").strip()
        chk = lambda t: p1.check(f"## {new_sec} x\n\n{t}\n", P, new_sec, {new_sec: 10 ** 6})  # noqa: E731
        rep = chk(new)
        first_probs = problems(rep)
        repaired = False
        if first_probs:
            ev = "\n\n".join(p1.fmt_item(P[i], False) for i in ids)
            fixed = (R.call(f"calib3_repair_{old_sec}_{k}", 0, "edit", REPAIR, "PROBLEMS:\n" + "\n".join(f"- {x}" for x in first_probs)
                            + f"\n\nEVIDENCE:\n{ev}\n\n=== PARAGRAPH ===\n{new}", 220) or "").strip()
            r2 = chk(fixed)
            if fixed and len(problems(r2)) < len(first_probs):
                new, rep, repaired = fixed, r2, True
        sents = va.sentences(va.strip_notes(new))
        ints = [(va.int_func(s) or "(unlabelled)", va.clean(s)) for s in sents if va.is_int(s)]
        show = re.sub(r"\{\{note:\s*(.*?)\}\}", r" *[note: \1]*", new, flags=re.S)
        show = va.INT_RE.sub(lambda m: f"**⟨INT:{m.group(1) or '?'}⟩**", show)
        left = problems(rep)
        md += [f"## {titles.get(new_sec, new_sec)} {pk} — paragraph {k} of the current draft's {old_sec}\n",
               f"**Point** *({pt[2]})*: {pt[3]}\n",
               "### Original\n", para + "\n", "### Round 2\n", (earlier(n) or "*(not available)*") + "\n",
               "### Round 3\n", show + "\n",
               f"*Words: {va.words(new)}; sentences: {len(sents)}; interpretive: {len(ints)}.* "
               + ("*One repair pass was applied for: " + "; ".join(first_probs) + "*\n" if repaired else "\n"),
               "**Interpretive sentences and the test each passes:**\n"]
        md += [f"- **{f}** — {s}" for f, s in ints] or ["- *(none)*"]
        md += ["", "**Code checks after the rewrite:** " + ("all clear" if not left else "; ".join(left)), ""]
    (C.D / f"ch{C.CH:02d}_calibration.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote ch{C.CH:02d}_calibration.md; spent this step ${R.spent - s0:.3f}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
