#!/usr/bin/env python3
"""Retrieve per-chapter evidence packs from the vector KB for book drafting."""
import os
from pathlib import Path
from dotenv import load_dotenv
from mistralai.client import Mistral
from kb_search import search

load_dotenv()
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

QUERIES = {
    1: [
        "Udayapur town Vidisha district geography setting and the Betwa river",
        "significance and importance of the Udayesvara Nilkantheshwara temple",
        "Malwa plateau as a historical region Avanti overview",
    ],
    2: [
        "origin of the Paramara Rajput dynasty Agnikula fire myth Mount Abu Vasistha",
        "early Paramara rulers Upendra Vairisimha Siyaka Vakpati rise to power",
        "Avanti Malwa Dhara Ujjain Paramara capital and titles",
        "Munja Vakpati warrior poet patron campaigns against the Calukyas",
    ],
    3: [
        "Bhoja Paramara the scholar king reign and achievements",
        "literary and scientific works of Bhoja Samaranganasutradhara Sarasvatikanthabharana",
        "Bhojpur lake Dhara cultural patronage learning",
        "decline of the Paramaras after Bhoja invasions Calukyas of Gujarat",
    ],
    4: [
        "Udayaditya Paramara accession and consolidation of the kingdom",
        "founding of the city of Udayapur and the Udayasamudra tank",
        "Udayapur Prasasti inscription temple foundation and dates 1059 1080",
        "Udayaditya builds the Siva temple Nilakanthesvara at Udayapur",
    ],
    5: [
        "Bhumija style of architecture sikhara superstructure",
        "Udayesvara temple ground plan garbhagrha mandapa jagati saptaratha saptabhumi",
        "mandovara mouldings spire kutastambha latas of the tower",
        "Samaranganasutradhara prasada temple types classification",
    ],
    6: [
        "iconography of the outer walls Dikpalas guardians of directions",
        "forms of Siva Natesa Tripurantaka Mrtyunjaya sculpture at the temple",
        "syncretic and rare images Harihara Ardhanarisvara goddesses surasundaris",
        "Saiva Siddhanta philosophy Tattvaprakasa of Bhoja pati pasu pasa tattvas",
    ],
    7: [
        "serpentine scimitar of letters inscription varnanagakrpanika Udaypur",
        "inscriptions of the Udayesvara temple across centuries Sanskrit Persian Hindi",
        "Tughluq mosque conversion temple destruction at Udayapur",
        "brass lingam mukhalinga Scindia Maratha restoration and ASI conservation",
    ],
}

outdir = Path("book/_evidence")
outdir.mkdir(parents=True, exist_ok=True)
for ch, queries in QUERIES.items():
    seen, packed = set(), []
    for q in queries:
        for r in search(q, k=8, client=client):
            kid = (r["source"], r["heading"], r["chunk"])
            if kid in seen:
                continue
            seen.add(kid)
            packed.append(r)
    with open(outdir / f"ch{ch:02d}.md", "w", encoding="utf-8") as f:
        f.write(f"# Evidence pack — Chapter {ch}\n\n")
        for r in packed:
            f.write(f"## [{r['source']}] {r['heading']}  (score {r['score']:.2f})\n\n{r['text']}\n\n---\n\n")
    words = sum(len(r["text"].split()) for r in packed)
    print(f"ch{ch}: {len(packed)} chunks, ~{words} words -> {outdir}/ch{ch:02d}.md")
