"""Ch 6 v3 deepening: add a verbatim corpus slice to ONE worker's pack (free; no API). Like _tools/kb_new.py, but writes
only to ch06/_work/pack_<G>.json and _work/kbn_<G>.jsonl, so parallel workers never touch a shared file.

  python -I -X utf8 drafting/ch06/_work/kbn_local.py G BOOKCODE LINE ["start substring" ["end substring"]]
  G = A..E (worker); BOOKCODE = a pack book code (CII, GANGULY, JAGTA-EN, JAGTA-HI, BHOJA-TIMES, ...).
New ID: C06-KBN-<BOOKCODE>-<G>-<NNN>. Prints the ID, page, tier and the slice.
"""
import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
DR = W.parent.parent
CORPUS = DR.parent / "Udaipur Books Markdown files"
FILES = {"CII": "Inscriptions Corpus.md", "GANGULY": "History of Paramara Dynasty DC Ganguly.md",
         "GAZ": "Vidisha Gazeteer.md", "GEOHER": "Geo-Heritage of Udaypur The Third Eye.md",
         "JAGTA-EN": "Jagta_Hua_Kasba_EN.md", "JAGTA-HI": "Jagta_Hua_Kasba_OCR_text.md",
         "MADHYABHARAT": "The cultural heritage of madhya bharat.md", "PANDE": "The Udayesvara Temple - Anupa Pande.md",
         "RAJABHOJ-EN": "Raja_Bhoj_Aur_Parmarkaleen_EN.md", "SERPENT": "A_serpentine_scimitar_of_letters_from_Ud.md",
         "BHOJA-TIMES": "bhoja-paramara-and-his-times.md", "BHOJDEV-HI": "bhojdev.md",
         "PARTEMPLES": "Some Paramara Templess.md", "YOGASUTRA": "patanjala-yogasutra-rajamartanda-bhoja.md",
         "PARMAR-RAJPUT": "History of the Parmar Rajput Dynasty.md", "INTACH": "Intach Udaypur (1).md",
         "ARTPAR": "Art of Paramaras.md", "HARDY": "806955603-The-Temple-Architecture-of-India-Adam-Hardy.md",
         "KRAM-1": "The Hindu Temple Vol 1 Stella Kramrisch.md"}
sys.path.insert(0, str(DR / "_pipe"))
import tiers  # noqa: E402


def main():
    g, code, line = sys.argv[1], sys.argv[2], int(sys.argv[3])
    start = sys.argv[4] if len(sys.argv) > 4 else None
    end = sys.argv[5] if len(sys.argv) > 5 else None
    fname = FILES[code]
    lines = (CORPUS / fname).read_text(encoding="utf-8").split("\n")
    text = lines[line - 1]
    if start:
        i = text.index(start)
        j = text.index(end, i) + len(end) if end else len(text)
        text = text[i:j]
    page = None
    for k in range(line - 1, -1, -1):
        m = re.search(r"<!--\s*page\s+(\d+)\s*-->", lines[k])
        if m:
            page = int(m.group(1))
            break
    pack_p = W / f"pack_{g}.json"
    pack = json.loads(pack_p.read_text(encoding="utf-8"))
    n = 1 + sum(1 for e in pack if e["id"].startswith(f"C06-KBN-{code}-{g}"))
    iid = f"C06-KBN-{code}-{g}-{n:03d}"   # validator ID_RE needs a 3-digit tail
    title = next((x.get("book_title") for x in pack if x.get("book_code") == code and x.get("book_title")), "")
    item = {"id": iid, "unit": "C06", "kind": "kb-new", "book_code": code, "page": f"p. {page}" if page else "no page",
            "source_file": fname, "line": line, "quote": text.strip(), "tier": tiers.tier_of({"book_code": code})[0],
            "flags": ["kb-new", f"v3-{g}"], "book_title": title}
    pack.append(item)
    pack_p.write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
    with (W / f"kbn_{g}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(iid, item["page"], f"T{item['tier']}", text.strip()[:200])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
