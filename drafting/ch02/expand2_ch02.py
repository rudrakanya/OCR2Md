"""Chapter 2 — second, smaller expansion after the hand cuts of cross-section repetition (same budget/log).

Each section keeps every sentence and gains a few unused evidence items, towards the rebalanced targets
(2.1 900 · 2.2 1,150 · 2.3 1,100 · 2.4 1,000 · 2.5 850 = 5,000). Kept only if citation integrity holds, the section
is within 90–110% of target and the code score is no worse than the current section. Then verification + fixes.

  python -u -I "drafting/ch02/expand2_ch02.py"
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import pipeline_ch02 as pc  # noqa: E402
import pipeline_v3 as pv  # noqa: E402
import validate as va  # noqa: E402
import verify as vf  # noqa: E402
from expand_ch02 import SYS  # noqa: E402

D = HERE
pv.EFFORT.update({"expand": "medium"})
AIM = {"2.1": (905, 960), "2.2": (1120, 1200), "2.3": (1080, 1150), "2.4": (980, 1050), "2.5": (845, 900)}
ADD = {
    "2.1": """- In P1: the inscriptions' editor makes the identification for "v. 7" of one record and "l. 10" of another [C02-CII-001; C02-CII-002] — give these as verse 7 and line 10; and Patil's description of Besnagar as "the famous ancient city" may be paraphrased (no superlative of your own).
- Nothing else; do not add any restatement.""",
    "2.2": """- In P2: the whole upper catchment receives more than 90 per cent of its rainfall during the Indian summer monsoon [C02-BETWA-FLOW-003].
- In P4 (talav and tekro): the baoli at the middle level of the hill may have served as a major source of water for the village, and fragments of carved columns lie over it [C02-KB-GEOHER-003]; numerous tanks and baolis were commissioned by ruling clans and filled mainly in the rains [C02-KB-GEOHER-003] (if not already said).
- In P6 (Bhoja's dam): Bhojpur near Bhopal, founded in Bhoja's name, where a huge Śiva temple still stands, according to *Bhojadeva* [C02-BHOJDEV-HI-001]; Rajpurohit's report that the present-day lake of Bhopal is said to be its remnant [C02-RAJABHOJ-EN-001].
- In P2 or P3: in the upper catchment the area of water bodies grew by 1 per cent between 1990 and 2020, which the streamflow study attributes to a dam built in 2011–2013 [C02-BETWA-FLOW-014; C02-BETWA-FLOW-015].""",
    "2.3": """- In the last paragraph: the streamflow study's projections — mean monsoon streamflow falling by about 39–47 per cent in 2023–2060 and 31–41 per cent in 2061–2100, and mean monsoon rainfall by 30–35 and 23–30 per cent, against 1982–2020 [C02-BETWA-FLOW-013] — presented as model projections; the study's note that monsoon rainfall correlates highly (0.8) with kharif crop-production anomalies, a finding it credits to Mall et al. [C02-BETWA-FLOW-016].
- In the basin-study paragraph: at Tikamgarh, Begumganj and Khurai, fewer rainy days without a fall in rainfall indicate rising average rainfall intensity, with consequences for run-off and groundwater recharge [C02-BETWA-CLIM-017].""",
    "2.4": """- After the catchment sentences (P5 of the current text): between 1990 and 2020 the upper catchment's agricultural land grew by 3 per cent and built-up land by 2 per cent, while forest and open land shrank by 4 and 2 per cent [C02-BETWA-FLOW-014]; the streamflow study links the growth of farmland and towns to a 60 per cent rise in the catchment's population between 1991 and 2011 [C02-BETWA-FLOW-015].
- In P1: Geo-Heritage identified the area's geomorphological features from Landsat satellite imagery and mapped them on a GIS platform [C02-GEOHER-007] — one clause; do not name the butte (Chapter 3).""",
    "2.5": """- In P4 (stone at hand): a contrast within the Betwa country — at Kurwai the fort and most houses are built of the gneiss rock abundant in the neighbourhood and roofed with big slabs [C02-GAZ-055] — showing that local rock, whatever it was, set the building material.
- In P5: nothing else.""",
}
EXTRA = {"2.1": ["C02-CII-001", "C02-CII-002", "C02-KB-MADHYABHARAT-001"],
         "2.2": ["C02-BETWA-FLOW-003", "C02-KB-GEOHER-003", "C02-BHOJDEV-HI-001", "C02-RAJABHOJ-EN-001", "C02-BETWA-FLOW-014", "C02-BETWA-FLOW-015"],
         "2.3": ["C02-BETWA-FLOW-013", "C02-BETWA-FLOW-016", "C02-BETWA-CLIM-017"],
         "2.4": ["C02-BETWA-FLOW-014", "C02-BETWA-FLOW-015", "C02-GEOHER-007"],
         "2.5": ["C02-GAZ-055"]}


def ts():
    return time.strftime("%H:%M:%S")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.time()
    outline, secs, targets, titles = pc.load_outline()
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    text = pc.OUT.read_text(encoding="utf-8")
    (D / "ch02_draft_v1_preExpand2.md").write_text(text, encoding="utf-8")
    cur = va.split_sections(text)
    R = pv.Run(False)
    spent0 = R.spent

    def job(sec):
        def f():
            lo, hi = AIM[sec]
            n = va.words(cur[sec])
            ids = [i for i in dict.fromkeys(pc.section_ids(secs[sec], P) + va.ids_in(cur[sec]) + EXTRA[sec]) if i in P]
            u = (f"WRITER BRIEF (binding):\n{pc.WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\n"
                 f"CURRENT LENGTH: {n} words. REQUIRED: {lo}–{hi} words, so add about {lo - n + 25} words.\n\n"
                 f"MATERIAL TO ADD:\n{ADD[sec]}\n\nNAMES: Vijay Manohar Tiwari is named in full only once in the chapter (in 2.2); write 'Tiwari' elsewhere. Keep 'the district Gazetteer of 1979' where it stands.\n\n"
                 f"COVERED ELSEWHERE (do not develop):\n{pv.covered_elsewhere(sec, pv.section_parts(secs), titles)}\n\n"
                 "EVIDENCE (the only permitted facts):\n" + "\n\n".join(pc.fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids)
                 + f"\n\n=== SECTION TO EXPAND ===\n{cur[sec].strip()}")
            return R.call(f"expand2_{sec}", 10, "expand", SYS.replace("MINW", str(lo)).replace("MAXW", str(hi)), u, hi + 60)
        return f

    res = R.parallel([(s, job(s)) for s in pc.SECTIONS])
    state = {"sections": {}}
    new = dict(cur)
    for sec in pc.SECTIONS:
        out = res.get(sec)
        ref = pc.check(cur[sec], P, sec, targets)
        rec = {"before": pc.summ(ref)}
        if isinstance(out, str) and out.strip():
            cand = out.strip() + "\n"
            (D / "candidates" / f"{sec}_expanded2.md").write_text(cand, encoding="utf-8")
            after = pc.check(cand, P, sec, targets)
            n = after["words"].get(sec, 0)
            keep = (after["integrity_ok"] and targets[sec] * 0.9 <= n <= targets[sec] * 1.1
                    and pc.score_rep(after) <= pc.score_rep(ref) and cand.startswith("## " + sec)
                    and not re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", cand)))
            rec.update(after=pc.summ(after), kept=keep, problems=pc.problems_of(after))
            if keep:
                new[sec] = cand
        state["sections"][sec] = rec
        print(f"[{ts()}] {sec}: kept={rec.get('kept')} words={rec.get('after', {}).get('words')} problems={rec.get('problems')}", flush=True)
    chapter = "\n\n".join(new[s].strip() for s in pc.SECTIONS) + "\n"
    rules = vf.rule_checks(chapter, P, vf.cited_sentences(chapter))
    print("rules before verification:", [(r["rule"], r.get("sid")) for r in rules], flush=True)
    chapter, vstate = pc.verify(chapter, P, R, targets)
    rep = pc.check(chapter, P, None, targets)
    state.update(verdicts_before=vstate["verdicts_before"], verdicts_after=vstate["verdicts_after"], final_validation=pc.summ(rep),
                 final_validation_detail=rep, spent_this_step=round(R.spent - spent0, 4), spent_total_usd=round(R.spent, 4),
                 calls=R.calls, seconds=round(time.time() - t0))
    pc.OUT.write_text(chapter, encoding="utf-8")
    (D / "ch02_expansion2_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: state[k] for k in ("verdicts_after", "final_validation", "spent_this_step", "spent_total_usd")}, ensure_ascii=False), flush=True)
    print(f"[{ts()}] EXPANSION 2 FINISHED", flush=True)
