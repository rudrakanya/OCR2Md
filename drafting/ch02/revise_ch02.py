"""Chapter 2 — editorial revision pass after the pipeline (same budget, same api_log_ch02/).

The pipeline draft passed every code check but read thinly: 4,656 words (target 5,000); filler sentences
restating the previous fact; Tiwari never named; the Gazetteer never date-stamped; Chapter 3/11 material
(sandstone petrology, fort bastions) and crops repeated across 2.3/2.4. One revision call per section
(effort medium, the user's level for edits/revisions), in parallel, with line-level editor's notes, a ±5% word range and
the section's evidence plus a few unused items for substance. Kept only if citation integrity holds and the
code score is no worse (word-range problems count). Then the citation-support verification + fixes run again
on the whole chapter (pipeline_ch02.verify), and footnotes/docx are rebuilt.

  python -u -I "drafting/ch02/revise_ch02.py" [--dry-run]
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import pipeline_ch02 as pc  # noqa: E402
import pipeline_v3 as pv  # noqa: E402
import validate as va  # noqa: E402

D = HERE
pv.EFFORT.update({"edit2": "medium"})
BAND = 0.05

NOTES = {
    "2.1": """- Date-stamp the Gazetteer at its first mention in this section: "the district Gazetteer of 1979".
- P1: cut the two closing sentences ("The river's association with the city rests both…", "At Besnagar, the Betwa forms one side of the fork…"): they restate the first sentence.
- P2: cut "Its course therefore extends beyond…", "The longer part of the channel thus lies in Uttar Pradesh…" and "Raisen and Hamirpur mark the two ends…" (restatements). Keep the Gazetteer's ranking attributed, without the padding clause after it. Move the basin area (about 43,500 km²) here from P6.
- P3: cut "Its passage through Vidisha is consequently…" and "The water divides, rather than the district boundary…". Add the Bes: it joins the Betwa 3 km north of Vidisha after a course of about 65 km [C02-KB-GAZ-002]; the Gazetteer notes Besnagar as a place of great archaeological importance along the river [C02-GAZ-003].
- P4: cut "Ancient Besnagar occupies the fork of the Bes and the Betwa" (already in P1).
- P5: cut the first sentence ("Near Udaypur, the Betwa's drainage network comes close…") and the last sentence (it repeats the Kewtan's course). Give the Kewtan distances exactly as Geo-Heritage does: 1.8 km from the site of Shiva Pindi and 1 km from the village settlement — no "hill", no "below".
- P6: cut the basin-area sentence (moved to P2) and the final sentence about the Kewtan (the distance is already given in P5). Close instead on the contrast the Gazetteer records — a river that supplies Vidisha's waterworks while the rest of the district draws on wells — leading into 2.2.
- Use the words freed by these cuts for the new Bes material and for fuller, concrete topic sentences; no new restatements.""",
    "2.2": """- Vijay Manohar Tiwari: name him in full here, at the first mention of *Jagta Hua Kasba* (P7): "Vijay Manohar Tiwari, in *Jagta Hua Kasba*, …". Nowhere else in full.
- P1: the first three sentences say the same thing three times (rivers absent / Kewtan 1 km). Make it one topic sentence quoting Geo-Heritage's "rivers in this landscape are absent" and one sentence noting that the same survey places the Kewtan 1 km from the village. Keep the talav/tekro logic for P4; here only the semi-arid importance of water.
- P2: replace the abstract last sentence ("A place within this river basin consequently shares neither…") with the concrete catchment figure: the upper Betwa's catchment of 9,322 km² [C02-BETWA-FLOW-002].
- P5: replace "Their recollection encompasses several kinds of water source…" with the residents' formula itself, quoted exactly: "chappan baoli, bavan kuae and saadhe baarah talab" with Geo-Heritage's gloss (56 stepwells, 52 wells and 12 and half lakes) [C02-KB-GEOHER-001].
- P6: the auxiliary storage tank appears twice (first and fourth sentences) — keep it once. Open with a topic sentence on Bhoja's dam as the river's best-known medieval intervention. Add Kincaid's description, quoted by Ganguly, of the valley's wall of hills broken by only two gaps, both closed by dams of an earthen core faced with stone blocks laid without mortar [C02-GANGULY-001] (paraphrase; attribute to Kincaid as quoted by Ganguly). Add that the island in the lake's middle is still a settlement called Deep, according to *Bhojadeva* [C02-BHOJDEV-HI-003] (do not repeat its "largest" claim). Cut the summarising last sentence.
- P7: attribute the Shah Hussain account precisely: Mahesh Singh (*Bhoja Paramara and His Times*) and Kincaid as quoted by Ganguly. End on the exchange of stored water for cultivable silt, then one sentence leading to the monsoon (tanks and baolis fill in the rains) — keep that lead short.""",
    "2.3": """- P1: the opening sentence and the fourth sentence both give the 92 per cent; give it once (keep the fourth). Open instead with a topic sentence on a dry country with one wet season. Keep the evaporation-versus-rainfall point, stated as the basin study's figures (about 1,830 mm evaporation against an average 1,138 mm rainfall).
- P2: last sentence: "the streamflow study gives the upper Betwa summer maxima of 40–45 °C and winter minima reaching 2 °C" [C02-BETWA-FLOW-010].
- P3: add rainy days (from 47 at Basoda to 56 at Mohammadgarh) and the heaviest fall in 24 hours, 360.2 mm at Basoda on 31 July 1951 [C02-GAZ-019].
- P4: cut the last sentence ("The famine account concerns Malwa, whereas…") — it comments on the sources rather than the weather.
- P6: say "no significant trend" (these exact words) for the basin study's rainfall finding, and keep "a transition from wetter to drier hydro-climatic conditions" for the upper catchment. Add the streamflow study's annual average flow falling from 312 to 281 m³/s between 1982–2000 and 2001–2020 [C02-BETWA-FLOW-005], and the basin study's finding that winter maximum and minimum temperatures rose at all stations, with possible effects on winter wheat [C02-BETWA-CLIM-015]. End with one sentence (no new fact) leading to the tableland on which the rain falls.
- Crops at Udaypur (soybean, pigeon pea, maize; wheat, gram, lentil; 90/34 per cent rain-fed) belong here and only here.""",
    "2.4": """- P1: cut the sandstone petrology (medium- to coarse-grained, cross-bedded, glauconites, marls, claystones, 4 cm horizons, weathering) — Chapter 3 owns it. Keep only that the tableland owes its existence to flat-lying sedimentary rocks. Cut "placing the village within a spread of rising and falling ground rather than on a single level". Give the area as 1,966 hectares.
- P2: the spurs and the northward slope are said twice; say each once. Cut the summarising last sentence. Add Patil's picture of the region's three river systems (Chambal, Betwa, Narmada) and its Vindhya and Satpura mountain systems [C02-MADHYABHARAT-001] (attributed).
- P3: cut "The village's foothill position joins this contrast…".
- P4: cut the crops and rain-fed shares (2.3 owns them); keep the soils. Add the Gazetteer's three formations — alluvium, laterite and Deccan (Malwa) Trap — and that alluvium along the Betwa often forms steep cliffs in the north of the district [C02-GAZ-009]. Keep the catchment elevations in one sentence, labelled as the upper Betwa catchment (376–669 m, higher in the west at 451–669 m than in the east at 376–550 m) [C02-BETWA-FLOW-007], distinct from Udaypur's committed 340–480 m.
- P5: cut the summarising last sentence.
- P6: remove the Devanagari title "कथा उदयपुर". Write "Tiwari" (named in full in 2.2): Tiwari attributes Udaypur's importance as a centre on the border of two dynasties to its sandstone quarries [C02-JAGTA-HI-002] — attributed as his view. Cut "The two station approaches lead to a settlement among the western foothills…". Close on black soil and exposed sandstone meeting at the site, leading into 2.5.
- Optional, if words are needed: the district lies in a zone where earthquakes have been felt only with slight intensity, with fringe effects from distant great earthquakes [C02-GAZ-011].""",
    "2.5": """- P1: fine; tighten the last two sentences into one.
- P2: cut the fort-wall detail ("The thick fortification wall encircles a hillock…", bastions and gateways) — Chapter 11 owns the fort; keep at most the clause that a wall encircles the hillock. Cut the stepwells-as-resting-places/aquifer sentences (2.2 already gives them). Keep the hilltop kunds, the three-sided stepwell on the western slope of Pindi Hill (twenty steps), its suggested use as a reservoir, and the talav and Udaysagar as central to the settlement pattern (Udaysagar in a clause).
- P3: cut "1.94 acres … the highest district figure in the State" (a superlative). Add the Gazetteer's account that the doab between the Bah and the Betwa holds the richest cultivated land of Vidisha tahsil and that the central tract is rich from silt deposits [C02-GAZ-047] — attributed to the Gazetteer.
- P4: cut "Its uses include both substantial structures and delicate carving, connecting…" (repeats the next sentence). Add the Gazetteer's phrase "inexhaustible reserves of building materials" [C02-GAZ-041]; its list of minor minerals quarried across the district — clay, sandstone, murram, chhuimitti [C02-GAZ-049]; and the ferruginous laterite cappings once tapped as iron ore for indigenous furnaces [C02-GAZ-044]. Quote Patil's phrase "the ready availability of the sandstone from its hills" [C02-MADHYABHARAT-003] (attributed). Max 2 quotations in the section.
- P5: replace the repetitive last sentence with a closing that hands on to Chapter 3: Cunningham, quoted by Pande, on the temple's stone "quarried in the hill close by" [C02-PANDE-001] — the turn from water to rock. Do not repeat that quotation elsewhere in the section.""",
}
EXTRA = {"2.1": ["C02-KB-GAZ-002", "C02-GAZ-003"], "2.2": ["C02-GANGULY-001", "C02-BHOJDEV-HI-003", "C02-BETWA-FLOW-002"],
         "2.3": ["C02-GAZ-019", "C02-BETWA-FLOW-005", "C02-BETWA-CLIM-015", "C02-BETWA-FLOW-010"],
         "2.4": ["C02-GAZ-009", "C02-GAZ-011", "C02-MADHYABHARAT-001", "C02-BETWA-FLOW-007"],
         "2.5": ["C02-GAZ-041", "C02-GAZ-044", "C02-GAZ-049", "C02-GAZ-047", "C02-MADHYABHARAT-003"]}

SYS = """You are the line editor of one section of a university-press history chapter about Udaypur (Vidisha district, Madhya Pradesh). Apply the EDITOR'S NOTES exactly; then, to reach the word range, add substance only from the supplied evidence (fuller concrete detail, never restatement).
STRICT: every factual sentence keeps or gains bracketed evidence IDs from the supplied evidence only; no facts, dates, names or numbers that are not in an item's QUOTE or ENGLISH RENDERING; quotations character-for-character from a QUOTE, at most 2 in the section; no sentence may restate a fact already given in the section; no meta-commentary about the book, chapter, sources' reliability or method; no superlatives in the narrator's voice; British/Indian English with diacritics; keep the heading line exactly; paragraphs 120–200 words with topic sentences.
Return the full revised section in Markdown and nothing else."""


def ts():
    return time.strftime("%H:%M:%S")


def main(dry):
    t0 = time.time()
    outline, secs, targets, titles = pc.load_outline()
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    src = pc.OUT
    text = src.read_text(encoding="utf-8")
    if not dry and not (D / "ch02_draft_v1_pipeline.md").exists():
        shutil.copy(src, D / "ch02_draft_v1_pipeline.md")
        shutil.copy(D / "ch02_verification.json", D / "ch02_verification_pipeline.json")
    parts = va.split_sections(text)
    R = pv.Run(dry)
    state = {"spent_before": round(R.spent, 4), "sections": {}}
    rng = {s: (int(targets[s] * (1 - BAND)), int(targets[s] * (1 + BAND))) for s in pc.SECTIONS}

    def job(sec):
        def f():
            lo, hi = rng[sec]
            ids = list(dict.fromkeys(pc.section_ids(secs[sec], P) + pc.va.ids_in(parts[sec]) + EXTRA[sec]))
            ids = [i for i in ids if i in P]
            u = (f"WRITER BRIEF (binding):\n{pc.WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\n"
                 f"WORD RANGE: {lo}–{hi} words (IDs excluded); aim for {targets[sec]}.\n\nEDITOR'S NOTES:\n{NOTES[sec]}\n\n"
                 f"COVERED ELSEWHERE (do not develop):\n{pv.covered_elsewhere(sec, pv.section_parts(secs), titles)}\n\n"
                 "EVIDENCE (the only permitted facts):\n" + "\n\n".join(pc.fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids)
                 + f"\n\n=== SECTION TO REVISE ===\n{parts[sec].strip()}")
            return R.call(f"edit2_{sec}", 8, "edit2", SYS, u, targets[sec] + 100)
        return f

    res = R.parallel([(s, job(s)) for s in pc.SECTIONS])
    new_parts = dict(parts)
    for sec in pc.SECTIONS:
        out = res.get(sec)
        before = pc.check(parts[sec], P, sec, targets)
        rec = {"before": pc.summ(before)}
        if isinstance(out, str) and out.strip():
            cand = out.strip() + "\n"
            after = pc.check(cand, P, sec, targets)
            n = after["words"].get(sec, 0)
            lo, hi = int(targets[sec] * 0.9), int(targets[sec] * 1.1)
            keep = after["integrity_ok"] and lo <= n <= hi and pc.score_rep(after) <= pc.score_rep(before) and cand.startswith("## " + sec)
            rec.update(after=pc.summ(after), kept=keep)
            if not dry:
                (D / "candidates" / f"{sec}_edit2.md").write_text(cand, encoding="utf-8")
            if keep:
                new_parts[sec] = cand
        else:
            rec.update(kept=False, reason=repr(out)[:200])
        state["sections"][sec] = rec
        print(f"[{ts()}] {sec}: {rec.get('kept')} words {rec.get('after', {}).get('words')}", flush=True)
    chapter = "\n\n".join(new_parts[s].strip() for s in pc.SECTIONS) + "\n"
    if dry:
        print(json.dumps({"projected_usd": round(R.spent, 3), "calls": len(R.calls)}, indent=1))
        return
    (D / "ch02_revised_preverify.md").write_text(chapter, encoding="utf-8")
    chapter, vstate = pc.verify(chapter, P, R, targets)
    state["verification"] = {k: vstate[k] for k in ("verdicts_before", "verdicts_after")}
    rep = pc.check(chapter, P, None, targets)
    state["final_validation"] = pc.summ(rep)
    state["final_validation_detail"] = rep
    state["spent_usd"] = round(R.spent, 4)
    state["calls"] = R.calls
    state["seconds"] = round(time.time() - t0)
    src.write_text(chapter, encoding="utf-8")
    (D / "ch02_revision_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", src.name], ["make_docx.py", src.stem + "_footnoted.md", src.stem + ".docx"]):
        subprocess.run([sys.executable, "-I", str(D / cmd[0])] + cmd[1:])
    print(json.dumps({"final": state["final_validation"], "spent_usd": state["spent_usd"]}, ensure_ascii=False), flush=True)
    print(f"[{ts()}] REVISION FINISHED", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--dry-run" in sys.argv)
