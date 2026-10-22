"""Full-chapter spot-check for ch02_draft_v1.md: 15 cited sentences at random (3 per section) beside their evidence,
then the sentences edited by hand after the last machine verification (with what changed and why).

  python -I "drafting/ch02/make_spotcheck.py"
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import pipeline_ch02 as pc  # noqa: E402
import verify as vf  # noqa: E402

D = HERE
HAND = [
    ("2.1", "The district Gazetteer of 1979 calls the Betwa…", "restored the canon's 1979 date-stamp, which the automatic fixer had removed"),
    ("2.2", "Vijay Manohar Tiwari, in *Jagta Hua Kasba*, records that Hoshang Shah Ghori…", "restored Tiwari's full name (first mention), removed by the fixer; substance re-verified SUPPORTED in the 2.2 run"),
    ("2.2", "…by order of a king he does not name.", "replaced the model's 'on a Muslim king's orders' (not the source's wording) with a faithful paraphrase of Smith's 'by order of a Muhammedan King'"),
    ("2.2", "…during the monsoon. / …the king built the lake…", "replaced 'Indian summer monsoon' (not in the cited item) and 'Bhoja' (the item says 'King Bhoj'); re-verified SUPPORTED"),
    ("2.4", "Tiwari attributes Udaypur's importance as a centre on the border of two dynasties…", "replaced the Devanagari title the fixer had introduced; the claim itself is the item's gloss, attributed as testimony"),
    ("2.4", "At Udaypur itself, black cotton soil and Vindhyan sandstone occur within the same village area.", "replaced a PARTIAL closing sentence that over-read C02-JAGTA-HI-002; now cites only C02-GEOHER-027, which states both"),
    ("2.5", "Tiwari describes shops made from Udaypur's own stone…", "restored 'Tiwari' and the spelling 'Udaypur' (the fixer had written 'The account' and 'Udaipur')"),
    ("2.5", "…at Kurwai the Gazetteer describes a fort of gneiss…", "merged two verified sentences; 'Kurwai' named from the item's mapping note (the quote says only 'the place'), so the town is not mistaken for Udaypur"),
    ("2.1–2.5", "seven cut sentences", "cross-section repetition removed by hand (alluvium, Patil's river systems, Dhasan, Bay of Bengal depressions, stepwells), plus three filler sentences; no text added"),
]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    text = pc.OUT.read_text(encoding="utf-8")
    smap = vf.cited_sentences(text)
    rnd = random.Random(2026)
    L = ["# Chapter 2 spot-check\n",
         "Fifteen cited sentences chosen at random (three per section), each beside the exact evidence it cites. Every cited sentence "
         "was SUPPORTED at the last machine verification (2.1, 2.3–2.5 in the full-chapter run; 2.2 in its own run); the hand edits made "
         "after it are listed at the end.\n"]
    n = 0
    for sec, rows in smap.items():
        for r in rnd.sample(rows, min(3, len(rows))):
            n += 1
            L.append(f"## {n}. Section {sec}\n\n> {r['sentence']}\n")
            for i in r["ids"]:
                if i in P:
                    it = P[i]
                    L.append(f"- **{i}** — {it['book_title']}, {it['page']}" + (" *(kb-new)*" if "kb-new" in it["flags"] else "")
                             + f"\n  > {' '.join(it['quote'].split())}" + (f"\n  *English rendering:* {it['gloss']}" if it.get("gloss") else ""))
            L.append("")
    L.append("## Hand edits after the last machine verification\n")
    L += [f"- **{s}** — {what}: {why}" for s, what, why in HAND]
    (D / "ch02_spotcheck.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote ch02_spotcheck.md")
