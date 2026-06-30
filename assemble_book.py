import os
from pathlib import Path

d = Path("book")
titles = [
    "The Rising Lord: An Introduction to the Nīlakaṇṭheśvara (Udayeśvara) Temple and Its World",
    "The Fire-Born: Origins and Rise of the Paramāra Rajputs",
    "The Golden Noon: Bhoja and the Paramāra Zenith",
    "Udayāditya and the Founding of Udayapur",
    "The Bhūmija Vision: Plan and Architecture",
    "Stone Made Speech: Sculpture, Iconography, and the Śaiva Vision",
    "An Archive in Stone: Inscriptions, Conquest, and Afterlife",
]
parts = [
    "# The Rising Lord\n"
    "## The Nīlakaṇṭheśvara (Udayeśvara) Temple of Udaypur and the World of the Paramāra Rajputs\n\n"
    "*A working draft, written in third-person narrative history and grounded, via a vector "
    "knowledge base, in the Udaypur reference corpus.*\n",
    "\n## Contents\n\n" + "".join(f"{i+1}. {t}\n" for i, t in enumerate(titles)) + "8. Bibliography\n",
]
body_words = 0
for i in range(1, 8):
    txt = (d / f"chapter-{i:02d}.md").read_text(encoding="utf-8").strip()
    body_words += len(txt.split())
    parts.append("\n\n---\n\n" + txt)
parts.append("\n\n---\n\n" + (d / "Bibliography.md").read_text(encoding="utf-8").strip())

out = d / "The_Rising_Lord_manuscript.md"
out.write_text("\n".join(parts), encoding="utf-8")
print(f"Assembled {out}  (~{body_words} words incl. notes across 7 chapters + bibliography)")
for i in range(1, 8):
    fp = d / f"chapter-{i:02d}.md"
    print(f"  chapter-{i:02d}.md : {len(fp.read_text(encoding='utf-8').split())} words")
