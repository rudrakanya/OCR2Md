"""Chapter 2 — expansion pass on the editor-revised sections (candidates/<sec>_edit2.md), same budget/log.

revise_ch02.py's line edits read well but came back 9–19% short of target (all rejected on length). Here each
edited section keeps every sentence and gains named, unused evidence, with an explicit minimum length. Kept only
if citation integrity holds, the section lands within 90–110% of target and the code score is no worse than the
pipeline version of the section. Then citation-support verification + fixes on the whole chapter, footnotes, docx.

  python -u -I "drafting/ch02/expand_ch02.py" [--dry-run]
"""
from __future__ import annotations

import json
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
pv.EFFORT.update({"expand": "medium"})

ADD = {
    "2.1": """- In P3 (through Vidisha district): the district's extent (latitude 23° 21'–24° 22' N, longitude 77° 15' 30"–78° 18' E), its place "in the central part of the State and eastern part of the fertile Malwa region", and its roughly elliptical shape with the longer axis from north-west to south-east [C02-GAZ-006].
- In P2: the basin's position (77°10'E–80°20'E, 22°54'–26°05'N) beside its area of about 43,500 km² [C02-BETWA-CLIM-001].
- In P4 (tributaries): the fuller roll of tributaries the Gazetteer gives — on the left bank the Kaliasot, Ajoar, Besh, Bah, Sagar, Kethan and Orr; on the right the Richhan, Dabar, Nion, Parasri, Bina, Jamni, Dhasan and Birma — and which of them flow in Vidisha district (the Besh, Sahodra, Bah, Sagar, Kethan, Nion, Parasri and Bina) [C02-GAZ-003]; the Bina's own tributaries, the Babnai and the Bagaru, draining the east of the district [C02-KB-GAZ-001].
- Alluvium along the Betwa, a yellow or grey-brown sandy clay with kankar, often forms steep cliffs in the north of the district [C02-GAZ-009] (one sentence, in P3 or P4).""",
    "2.2": """- Cut the sentence on Vidisha's Betwa water-supply scheme and wells elsewhere (C02-GAZ-053): section 2.1 owns it.
- Replace "Betwa-fed" wherever it appears.
- Wherever Kincaid is named, cite C02-GANGULY-001 together with any other ID in that sentence (Kincaid is named in that item's mapping note); Ganguly quotes "Mr. W. Kincaid, who personally visited the lake".
- In P2 or P3: the basin study's judgement that the Betwa basin, "though historically important", remains highly underdeveloped for lack of irrigation, with agriculture the mainstay, and is prone to famines and droughts, particularly in its upper and middle regions [C02-BETWA-CLIM-018].
- In P2: water bodies make up 2 per cent of land in the upper Betwa catchment, against 76 per cent agricultural land [C02-BETWA-FLOW-014].
- In P6 (Bhoja's dam): Kincaid's dimensions, as quoted by Ganguly — the lesser opening closed by a band 87 feet high and 300 ft thick at the base, the greater by one in places 40 ft high and about 100 ft broad on top [C02-GANGULY-001]; V. A. Smith's description, quoted in *Bhoja Paramara and His Times*, of a lake "formed by massive embankments" and of its dam cut in the fifteenth century "by order of a Muhammedan King" [C02-BHOJA-TIMES-003] (quote only these exact words; do not use his "noblest"); Rajpurohit's tradition that Bhoja built the lake for the benefit of his health and went boating on it [C02-RAJABHOJ-EN-002]. At most 2 quotations in the whole section.""",
    "2.3": """- Write the famine years exactly as the item does: "1899-00" (as 1899–00), not 1899–1900.
- In P1: humidity above 70 per cent in the monsoon and below 20 per cent on summer afternoons, the driest part of the year; skies heavily clouded in the monsoon and mostly clear otherwise [C02-GAZ-020].
- In P2: the basin study divides its water year (1 June to 31 May) into three four-month seasons — monsoon (June–September), winter (October–January), summer (February–May) — beside the Gazetteer's four [C02-BETWA-CLIM-005].
- In P6: the streamflow study's count of dry events rising by 15 per cent in 2001–2020 against 1980–2000, while wet and normal events fell by 4 and 11 per cent [C02-BETWA-FLOW-011]; the basin study's exception to its no-trend finding — summer rainfall decreasing at five stations, with possible effects on crop productivity [C02-BETWA-CLIM-016]; and its warning that a delayed monsoon onset delays kharif sowing, which in turn affects the rabi crop [C02-BETWA-CLIM-019].""",
    "2.4": """- In P1: most of Udaypur village is covered by sandstone and quaternary deposits, and most of its landforms are landforms of these rocks; the south side of the village shows undulating topography with moderately dissected hills [C02-GEOHER-007] (do not name the butte — Chapter 3).
- In P2: Vidisha district's extent and place in the eastern part of the fertile Malwa region [C02-GAZ-006] — ONE clause only, since 2.1 gives the coordinates; do not repeat the coordinates.
- In P4: the large hill, Shiva Pindi, is sedimentary terrain, and most of Udaypur has sedimentary structures [C02-GEOHER-013].
- The district's seismic setting: earthquakes felt only with slight intensity, no epicentre of consequence in the district, fringe effects from great earthquakes in the Himalayan Boundary Fault Zone and the Rann of Kutch [C02-GAZ-011] — if not already present.
- Upper Betwa catchment land use: agricultural land 76 per cent and forest 14 per cent [C02-BETWA-FLOW-014] (one sentence, labelled as the upper catchment).""",
    "2.5": """- In P2: sandstone was the material of the fort wall, varying in shape and size, and the steep terrain lets storm water run off without damaging the wall [C02-GEOHER-030] — a clause or one sentence; no other fort detail (Chapter 11).
- In P4: the Gazetteer's statement that building construction was important in Vidisha, citing the testimony of buildings in Bhilsa, Gyaraspur and many other places to the extensive use of limestone and sandstone from an early period [C02-GAZ-048] — merge with C02-GAZ-050, do not repeat; Kramrisch's note that temples are built of stones quarried in the various parts of India and that sandstone prevails in central Indian temples [C02-KRAM-1-001] (attributed).
- In P4 or P5: on the hilltop, fragments of āmalakas, decorative slabs and pillars of red sandstone, with white sandstone used less often [C02-GEOHER-026].
- In P5: Tiwari's own words, glossed from the Hindi, that the quarries supplied basic building material in abundance [C02-JAGTA-HI-003] only if it does not repeat C02-JAGTA-EN-002 — otherwise skip.""",
}
EXTRA = {"2.1": ["C02-GAZ-006", "C02-BETWA-CLIM-001", "C02-GAZ-003", "C02-KB-GAZ-001", "C02-GAZ-009"],
         "2.2": ["C02-BETWA-CLIM-018", "C02-BETWA-FLOW-014", "C02-GANGULY-001", "C02-BHOJA-TIMES-003", "C02-RAJABHOJ-EN-002"],
         "2.3": ["C02-GAZ-020", "C02-BETWA-CLIM-005", "C02-BETWA-FLOW-011", "C02-BETWA-CLIM-016", "C02-BETWA-CLIM-019"],
         "2.4": ["C02-GEOHER-007", "C02-GAZ-006", "C02-GEOHER-013", "C02-GAZ-011", "C02-BETWA-FLOW-014"],
         "2.5": ["C02-GEOHER-030", "C02-GAZ-048", "C02-KRAM-1-001", "C02-GEOHER-026", "C02-JAGTA-HI-003"]}

SYS = """You expand one section of a university-press history chapter about Udaypur (Vidisha district, Madhya Pradesh).
KEEP every existing sentence and its bracketed IDs (you may adjust connective wording to integrate new material, and apply the explicit cuts/replacements in the instructions). ADD the listed material as new sentences in the paragraphs named, each with its bracketed evidence ID(s).
STRICT: only facts in the supplied items' QUOTE or ENGLISH RENDERING; quotations character-for-character from a QUOTE, at most 2 in the section; no sentence may restate a fact already given; no meta-commentary about the book, chapter, sources or method; no superlatives in the narrator's voice; British/Indian English with diacritics; keep the heading line exactly; paragraphs 120–200 words with topic sentences (split a paragraph that grows past 200 words).
LENGTH IS A HARD REQUIREMENT: the output must contain at least MINW words (IDs excluded) and at most MAXW. Outputs below MINW are rejected.
Return the full section in Markdown and nothing else."""


def ts():
    return time.strftime("%H:%M:%S")


def main(dry):
    t0 = time.time()
    outline, secs, targets, titles = pc.load_outline()
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    pipe = va.split_sections((D / "ch02_draft_v1_pipeline.md").read_text(encoding="utf-8"))
    base = {s: (D / "candidates" / f"{s}_edit2.md").read_text(encoding="utf-8") for s in pc.SECTIONS}
    R = pv.Run(dry)
    state = {"spent_before": round(R.spent, 4), "sections": {}}

    def job(sec):
        def f():
            lo, hi = int(targets[sec] * 0.97), int(targets[sec] * 1.07)
            n = va.words(base[sec])
            ids = list(dict.fromkeys(pc.section_ids(secs[sec], P) + va.ids_in(base[sec]) + EXTRA[sec]))
            ids = [i for i in ids if i in P]
            u = (f"WRITER BRIEF (binding):\n{pc.WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\n"
                 f"CURRENT LENGTH: {n} words. REQUIRED: {lo}–{hi} words, so add about {lo - n + 40} words.\n\n"
                 f"MATERIAL TO ADD / CHANGES:\n{ADD[sec]}\n\n"
                 f"COVERED ELSEWHERE (do not develop):\n{pv.covered_elsewhere(sec, pv.section_parts(secs), titles)}\n\n"
                 "EVIDENCE (the only permitted facts):\n" + "\n\n".join(pc.fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids)
                 + f"\n\n=== SECTION TO EXPAND ===\n{base[sec].strip()}")
            return R.call(f"expand_{sec}", 9, "expand", SYS.replace("MINW", str(lo)).replace("MAXW", str(hi)), u, hi + 80)
        return f

    res = R.parallel([(s, job(s)) for s in pc.SECTIONS])
    final = {}
    for sec in pc.SECTIONS:
        out = res.get(sec)
        ref = pc.check(pipe[sec], P, sec, targets)
        rec = {"pipeline": pc.summ(ref), "base_words": va.words(base[sec])}
        final[sec] = pipe[sec]
        if isinstance(out, str) and out.strip():
            cand = out.strip() + "\n"
            after = pc.check(cand, P, sec, targets)
            n = after["words"].get(sec, 0)
            keep = (after["integrity_ok"] and targets[sec] * 0.9 <= n <= targets[sec] * 1.1
                    and pc.score_rep(after) <= pc.score_rep(ref) and cand.startswith("## " + sec))
            rec.update(after=pc.summ(after), kept=keep, problems=pc.problems_of(after))
            if not dry:
                (D / "candidates" / f"{sec}_expanded.md").write_text(cand, encoding="utf-8")
            if keep:
                final[sec] = cand
        else:
            rec.update(kept=False, reason=repr(out)[:200])
        state["sections"][sec] = rec
        print(f"[{ts()}] {sec}: kept={rec.get('kept')} words={rec.get('after', {}).get('words')} problems={rec.get('problems')}", flush=True)
    chapter = "\n\n".join(final[s].strip() for s in pc.SECTIONS) + "\n"
    if dry:
        print(json.dumps({"projected_usd": round(R.spent, 3)}, indent=1))
        return
    (D / "ch02_expanded_preverify.md").write_text(chapter, encoding="utf-8")
    chapter, vstate = pc.verify(chapter, P, R, targets)
    state["verification"] = {k: vstate[k] for k in ("verdicts_before", "verdicts_after")}
    rep = pc.check(chapter, P, None, targets)
    state.update(final_validation=pc.summ(rep), final_validation_detail=rep, spent_usd=round(R.spent, 4),
                 calls=R.calls, seconds=round(time.time() - t0))
    pc.OUT.write_text(chapter, encoding="utf-8")
    (D / "ch02_expansion_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", pc.OUT.name], ["make_docx.py", pc.OUT.stem + "_footnoted.md", pc.OUT.stem + ".docx"]):
        subprocess.run([sys.executable, "-I", str(D / cmd[0])] + cmd[1:])
    print(json.dumps({"final": state["final_validation"], "spent_usd": state["spent_usd"]}, ensure_ascii=False), flush=True)
    print(f"[{ts()}] EXPANSION FINISHED", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--dry-run" in sys.argv)
