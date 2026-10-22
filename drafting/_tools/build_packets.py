"""Build compact reading packets (~25 chunks each, grouped by book, in book order).

drafting/_runs/packets/P0001.md ...   what the judge reads
drafting/_runs/packets/_sentences.jsonl  chunk_id -> sentence char spans (the slicer uses these)
drafting/_runs/packets/_index.json       packet -> chunk ids
Sentences are numbered per chunk; `<!-- page N -->` markers are shown as
unnumbered separators "— scan p. N —" and never belong to a sentence.
"""
from pathlib import Path
import collections
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "drafting" / "_tools"))
from engine import RUNS, Corpus  # noqa: E402

PACKET = 25
PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)
# split after sentence punctuation (Latin, danda, double danda) followed by whitespace
SENT_END = re.compile(r"(?<=[.?!।॥])\s+")

SHORT = {
 "467921465-Skanda-Purana-13-AITM.md": "SKANDA",
 "806955603-The-Temple-Architecture-of-India-Adam-Hardy.md": "HARDY",
 "A_serpentine_scimitar_of_letters_from_Ud.md": "SERPENT",
 "Art of Paramaras.md": "ARTPAR",
 "Geo-Heritage of Udaypur The Third Eye.md": "GEOHER",
 "History of Paramara Dynasty DC Ganguly.md": "GANGULY",
 "History of the Parmar Rajput Dynasty.md": "PARMAR-RAJPUT",
 "Inscriptions Corpus.md": "CII",
 "Intach Udaypur (1).md": "INTACH",
 "Jagta_Hua_Kasba_EN.md": "JAGTA-EN",
 "Jagta_Hua_Kasba_OCR_text.md": "JAGTA-HI",
 "Long-termhistoricchangesinclimaticvariablesofBetwa.md": "BETWA-CLIM",
 "Raja_Bhoj_Aur_Parmarkaleen_EN.md": "RAJABHOJ-EN",
 "Samarangan Vol 2 (a)_combined.md": "SAMAR-2",
 "Samrangana Sutradhar Vol 1.md": "SAMAR-1",
 "Some Paramara Templess.md": "PARTEMPLES",
 "Streamflow of the Betwa Rive.md": "BETWA-FLOW",
 "Temple Economics.md": "TEMPLE-ECON",
 "Temples of India.md": "TEMPLES-IND",
 "The Hindu Temple Vol 1 Stella Kramrisch.md": "KRAM-1",
 "The Hindu Temple Vol 2.md": "KRAM-2",
 "The Udayesvara Temple - Anupa Pande.md": "PANDE",
 "The cultural heritage of madhya bharat.md": "MADHYABHARAT",
 "Vidisha Gazeteer.md": "GAZ",
 "bhoja-paramara-and-his-times.md": "BHOJA-TIMES",
 "bhojdev.md": "BHOJDEV-HI",
 "iconography of hindus, buddhists and jains Gupte.md": "GUPTE",
 "patanjala-yogasutra-rajamartanda-bhoja.md": "YOGASUTRA",
 "The Udayesvara Temple Art, Architecture and Philosophy of the Saiva Siddhanta.md": "PANDE-COPY2",
}
FLAGS = {
 "SAMAR-1": "⚠ old OCR, pending re-OCR", "SAMAR-2": "⚠ old OCR, pending re-OCR",
 "YOGASUTRA": "⚠ OCR quality warning",
 "TEMPLE-ECON": "CONTEXTUAL ONLY; its 'Udaipur' is Udaipur, Rajasthan — never evidence about Udaypur",
 "JAGTA-EN": "English translation of JAGTA-HI; pages approximate",
}


def sentences(text: str):
    """Yield ('s', start, end) for sentences and ('p', page, None) for page markers."""
    out = []
    pos = 0
    for m in list(PAGE_RE.finditer(text)) + [None]:
        seg_end = m.start() if m else len(text)
        seg = text[pos:seg_end]
        base = pos
        for line in re.finditer(r"[^\n]+", seg):
            ls, lt = base + line.start(), line.group()
            cur = 0
            for b in SENT_END.finditer(lt):
                s, e = cur, b.start()
                if lt[s:e].strip():
                    out.append(("s", ls + s, ls + e))
                cur = b.end()
            if lt[cur:].strip():
                out.append(("s", ls + cur, ls + len(lt.rstrip())))
        if m:
            out.append(("p", int(m.group(1)), None))
            pos = m.end()
    # trim leading whitespace inside spans
    fixed = []
    for k, a, b in out:
        if k == "s":
            while a < b and text[a].isspace():
                a += 1
        fixed.append((k, a, b))
    return fixed


def main():
    C = Corpus()
    cands = [json.loads(l) for l in (RUNS / "candidates.jsonl").open(encoding="utf-8")]
    pilot = {json.loads(l)["chunk_id"] for l in (RUNS / "C01_judgments.jsonl").open(encoding="utf-8")}
    out_dir = RUNS / "packets"
    out_dir.mkdir(exist_ok=True)
    # packets already handed to judges are frozen (_keep.json); only the rest is (re)packed
    keep_f = out_dir / "_keep.json"
    frozen = json.loads(keep_f.read_text(encoding="utf-8")) if keep_f.exists() else {}
    frozen_ids = {c for L in frozen.values() for c in L}
    by_book = collections.defaultdict(list)
    for c in cands:
        if c["chunk_id"] not in frozen_ids:
            by_book[c["source_path"]].append(c)
    for old in out_dir.glob("P*.md"):
        if old.stem not in frozen:
            old.unlink()
    idx, n = dict(frozen), len(frozen)
    cmap = {c["chunk_id"]: c for c in cands}
    sent_fh = (out_dir / "_sentences.jsonl").open("w", encoding="utf-8")
    for cid in sorted(frozen_ids):
        sent_fh.write(json.dumps({"chunk_id": cid, "spans": [[a, b] for k, a, b in sentences(C.text[C.idx[cid]]) if k == "s"]}) + "\n")
    for book in sorted(by_book, key=lambda b: SHORT[b]):
        L = sorted(by_book[book], key=lambda c: C.meta[C.idx[c["chunk_id"]]].get("chunk_index", 0))
        for i in range(0, len(L), PACKET):
            n += 1
            pid = f"P{n:04d}"
            lines = []
            for c in L[i:i + PACKET]:
                cid = c["chunk_id"]
                j = C.idx[cid]
                m, text = C.meta[j], C.text[j]
                code = SHORT[book]
                sp = sentences(text)
                spans = [[a, b] for k, a, b in sp if k == "s"]
                sent_fh.write(json.dumps({"chunk_id": cid, "spans": spans}) + "\n")
                ret = " ".join(f"{u}[{','.join(v['subs'])}]" for u, v in sorted(c["units"].items()))
                head = f"### {cid[:10]} | {code} | scan p.{m.get('page_start')} | {m.get('heading_path') or ''}"
                lines.append(head)
                note = f"retrieved for: {ret}"
                if cid in pilot:
                    note += "  ·  C01 ALREADY HAND-JUDGED (pilot): give NO C01 items"
                if code in FLAGS:
                    note += f"  ·  {FLAGS[code]}"
                lines.append(note)
                k = 0
                for kind, a, b in sp:
                    if kind == "p":
                        lines.append(f"— scan p. {a} —")
                    else:
                        k += 1
                        lines.append(f"[{k}] {' '.join(text[a:b].split())}")
                lines.append("")
            (out_dir / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8")
            idx[pid] = [c["chunk_id"] for c in L[i:i + PACKET]]
    sent_fh.close()
    (out_dir / "_index.json").write_text(json.dumps(idx, indent=0), encoding="utf-8")
    (RUNS / "book_codes.json").write_text(json.dumps({"codes": SHORT, "flags": FLAGS}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(n, "packets,", sum(len(v) for v in idx.values()), "chunks;", len(frozen), "frozen")


if __name__ == "__main__":
    main()
