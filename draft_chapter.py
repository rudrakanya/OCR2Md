#!/usr/bin/env python3
r"""
draft_chapter.py — retrieval-augmented chapter drafting via Mistral chat.

For each chapter it:
  1. reads that chapter's evidence pack (book/_evidence/chNN.md) produced by
     make_evidence.py from the vector knowledge base, and
  2. reads a writing-style reference (the OCR'd writing sample), and
  3. asks a Mistral chat model to write the chapter in third-person narrative
     history voice, grounded ONLY in the evidence, with numbered endnotes,
  4. and saves it to book/chapterNN.md.

Requires: mistralai, python-dotenv ; MISTRAL_API_KEY in .env.
Prereqs : run build_kb.py then make_evidence.py first (so book/_evidence/ exists).

Usage (VSCode PowerShell):
    python draft_chapter.py 1
    python draft_chapter.py 1 2 3            # several chapters
    python draft_chapter.py all              # all seven
    python draft_chapter.py 4 --style-file "output\writing sample ocr\WhatsApp Image ....md"
"""
import argparse
import glob
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()
MODEL = os.environ.get("MISTRAL_CHAT_MODEL", "mistral-large-latest")
EVID = Path("book/_evidence")
OUT = Path("book")

# title + scope for each chapter
CHAPTERS = {
    1: ("The Rising Lord: An Introduction to the Nīlakaṇṭheśvara (Udayeśvara) Temple and Its World",
        "Introduce the temple and its world: the town of Udaypur in Vidisha and the Betwa (Vetravatī) country; "
        "the Malwa plateau / Avanti as a historical region; why this 11th-century Śiva temple matters; and a preview "
        "of the book's arc (dynasty, founder-king, architecture, sculpture/philosophy, inscriptions/afterlife)."),
    2: ("The Fire-Born: Origins and Rise of the Paramāra Rajputs",
        "The Agnikula ('fire-born') origin legend on Mount Abu and its political work; Avanti/Malwa with Ujjain and "
        "Dhārā; the earliest rulers (Upendra, Vairisiṃha, Sīyaka) and the rise from vassalage; Vākpati Mūñja the "
        "warrior-poet, his southern wars and patronage and fall. End on the threshold of Bhoja."),
    3: ("The Golden Noon: Bhoja and the Paramāra Zenith",
        "Bhoja the scholar-king as the apogee of Paramāra power and culture; his vast attributed works (incl. the "
        "Samarāṅgaṇasūtradhāra) and the authorship debate; his building and engineering (Dhārā, Bhojpur and its lake); "
        "court and legend; then the unravelling and decline after his death that sets up Udayāditya's recovery."),
    4: ("Udayāditya and the Founding of Udayapur",
        "Udayāditya's accession amid post-Bhoja crisis and his consolidation; the founding of the city Udayapur with "
        "the Udayasamudra tank; the building of the Nīlakaṇṭheśvara/Udayeśvara temple with its dated inscriptions "
        "(V.S. 1116/1059 and V.S. 1137/1080); the Udayapur Praśasti and its sun-imagery. Flag date disagreements."),
    5: ("The Bhūmija Vision: Plan and Architecture",
        "The Bhūmija style within Nāgara architecture and the Samarāṅgaṇasūtradhāra's temple taxonomy; the rotated-"
        "square plan (saptaratha/saptabhūmi); the parts (garbhagṛha, antarāla, gūḍhamaṇḍapa and porches, jagati, Vedī); "
        "the elevation — maṇḍovara mouldings rising into the śikhara with its stacked miniature spires. Explain terms."),
    6: ("Stone Made Speech: Sculpture, Iconography, and the Śaiva Vision",
        "The sculptural programme of the outer walls (Dikpālas; Śiva as Naṭeśa, Tripurāntaka, Mṛtyuñjaya; goddesses "
        "and surasundarīs; syncretic Harihara/Ardhanārīśvara) AND the theology it embodies — Śaiva Siddhānta and "
        "Bhoja's Tattvaprakāśa — reading the carved walls as theology made visible."),
    7: ("An Archive in Stone: Inscriptions, Conquest, and Afterlife",
        "The temple as an eight-century epigraphic archive; the 'serpentine scimitar of letters' (varṇanāgakṛpāṇikā) "
        "and its kin and political-Śaiva meaning; the Tughluq-era mosque of temple stone; later defacement traditions; "
        "the Maratha brass-faced liṅga (1775) and modern ASI conservation; a brief closing reflection. Flag disagreements."),
}

SYSTEM = (
    "You are a historian writing a chapter of a serious narrative history book. "
    "Write in the THIRD PERSON throughout — never use 'I', 'we', 'us', 'you', no direct address, no diary voice. "
    "Adopt the register and complexity of a serious history book: analytical, contextualizing, attentive to evidence "
    "and scholarly judgement. Carry a rich literary cadence — long, flowing, hypotactic sentences with em-dash asides "
    "and parenthetical qualifications, elevated and exact diction, vivid but restrained imagery, varied with the "
    "occasional short, weighted sentence (evocative, never purple). "
    "Ground EVERY substantive claim in the supplied EVIDENCE only; do not invent dates, names, or quotations; mark "
    "anything you cannot support as '[GAP — not in sources]'; where the evidence disagrees, say so. "
    "Preserve correct IAST diacritics (normalize OCR-style â/î/û to ā/ī/ū). "
    "Use numbered in-text endnote markers [1], [2], … and end with a '## Notes' section citing the real scholarly "
    "works named inside the evidence (authors/titles), never file names. Aim for ~3,500 words; use section subheadings. "
    "Output only the chapter (its title heading, the body with markers, and the ## Notes)."
)


def find_style_file():
    pats = ["output/**/*.md", "output/writing sample ocr/*.md"]
    for p in pats:
        hits = glob.glob(p, recursive=True)
        hits = [h for h in hits if "writing sample" in h.lower() or "whatsapp" in h.lower()]
        if hits:
            return hits[0]
    return None


def draft(client, n, style_text, model):
    title, scope = CHAPTERS[n]
    pack = (EVID / f"ch{n:02d}.md")
    if not pack.exists():
        print(f"  ! missing evidence pack {pack} — run make_evidence.py first"); return False
    evidence = pack.read_text(encoding="utf-8")
    user = (
        f"Write Chapter {n} of the book *The Rising Lord: The Nīlakaṇṭheśvara (Udayeśvara) Temple of Udaypur "
        f"and the World of the Paramāra Rajputs*.\n\n"
        f"CHAPTER TITLE: {title}\n\nCHAPTER SCOPE: {scope}\n\n"
        + (f"WRITING-STYLE REFERENCE (match the rhythm and texture of this prose, NOT its first-person voice "
           f"and NOT its subject):\n\"\"\"\n{style_text[:2500]}\n\"\"\"\n\n" if style_text else "")
        + "EVIDENCE (your only source of facts — each block is headed by its source):\n"
        + "\"\"\"\n" + evidence + "\n\"\"\"\n\n"
        "Now write the chapter."
    )
    resp = client.chat.complete(
        model=model,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        max_tokens=8000, temperature=0.4,
    )
    text = resp.choices[0].message.content
    OUT.mkdir(exist_ok=True)
    (OUT / f"chapter-{n:02d}.md").write_text(text, encoding="utf-8")
    print(f"  chapter-{n:02d}.md written ({len(text.split())} words)")
    return True


def main():
    ap = argparse.ArgumentParser(description="Draft a book chapter from the KB evidence pack (Mistral chat)")
    ap.add_argument("chapters", nargs="+", help="chapter numbers (1-7) or 'all'")
    ap.add_argument("--style-file", help="path to the OCR'd writing-sample .md (auto-detected if omitted)")
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env)"); sys.exit(1)
    nums = list(CHAPTERS) if args.chapters == ["all"] else [int(x) for x in args.chapters]

    sf = args.style_file or find_style_file()
    style_text = ""
    if sf and Path(sf).exists():
        style_text = Path(sf).read_text(encoding="utf-8")
        print(f"style reference: {sf}")
    else:
        print("style reference: none found (using built-in voice spec only). "
              "Tip: OCR the 'writing sample ocr' folder first with ocr_to_markdown.py, "
              "or pass --style-file.")

    model = args.model
    client = Mistral(api_key=key)
    for n in nums:
        if n not in CHAPTERS:
            print(f"  ! no chapter {n}"); continue
        print(f"Chapter {n}: {CHAPTERS[n][0]}")
        draft(client, n, style_text, model)
    print("Done. Review the chapters, then run: python assemble_book.py")


if __name__ == "__main__":
    main()
