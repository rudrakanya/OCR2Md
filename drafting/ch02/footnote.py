"""Chicago notes-bibliography (17th ed.) for any Chapter 2 draft version.

  python -I "drafting/ch02/footnote.py"                       # ch02_draft_v1.md -> ch02_draft_v1_footnoted.md
  python -I "drafting/ch02/footnote.py" <draft>.md [out.md]   # any version (v1, v2, intermediate)

* Each bracket of evidence IDs becomes one footnote marker [^n].
* Notes: the first citation of a book is a full note; later citations of the same book use the short form
  (surname, short title, page). No "Ibid.". Page notes are kept: approximate pages ("≈ 23, Hindi-original
  page"), unpaged items ("no page; <section>"), ⚠ items ("verify against source"). The evidence IDs follow each
  note inside an HTML comment (kept, not displayed).
* Bibliography: every book once, Chicago style, alphabetical. Year/publisher/place come only from
  books_manifest.yaml (and, where the manifest marks two filenames as the same book, from its twin row) or the
  knowledge-base metadata; nothing is invented. Missing details are simply omitted and listed by
  `incomplete_entries()` for the report.
* Works for every earlier version: input is any draft with bracketed IDs; evidence_pack_v2.json is used if
  present (it contains the v1 pack plus kb-new items), else evidence_pack.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch02"))
BR = re.compile(r"\[((?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR)(?:\s*[;,]\s*(?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR))*)\]")

# Bibliographic metadata by book code. Source for every field is books_manifest.yaml unless stated.
#   names: list of (given, surname); corp: corporate author; eds: True if the names are editors
#   kind: book | article | edited ; src: provenance note ; confirm: fields needing the editor's confirmation
BIB = {
    "BETWA-CLIM": {"names": [("Shakti", "Suryavanshi"), ("Ashish", "Pandey"), ("Umesh Chandra", "Chaube"), ("Nitin", "Joshi")],
                   "title": "Long-term Historic Changes in Climatic Variables of Betwa Basin, India", "short": "Climatic Variables of Betwa Basin",
                   "journal": "Theoretical and Applied Climatology", "year": 2013, "kind": "article",
                   "src": "manifest (title, byline, journal, year) and KB metadata",
                   "confirm": "volume, issue and page range not recorded"},
    "BETWA-FLOW": {"names": [("Amit", "Kumar"), ("Raghvender Pratap", "Singh"), ("Swatantra Kumar", "Dubey"), ("Kumar", "Gaurav")],
                   "title": "Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change", "short": "Streamflow of the Betwa River",
                   "year": 2022, "kind": "article",
                   "src": "KB metadata and the manifest's retired row for this file (byline, 2022); the active row Betwa_Streamflow.md gives 'Amit Kumar et al.', 2023",
                   "confirm": "year 2022 (KB metadata) vs 2023 (manifest active row); journal not recorded"},
    "ARTPAR": {"short": "Art of the Paramāras", "names": [("R. K.", "Sharma")], "title": "Art of the Paramāras of Malwa", "kind": "book", "src": "manifest (needs_review)"},
    "BHOJA-TIMES": {"short": "Bhoja Paramara", "names": [("Mahesh", "Singh")], "title": "Bhoja Paramara and His Times", "place": "Delhi",
                    "publisher": "Bharatiya Vidya Prakashan", "year": 1984, "kind": "book", "src": "manifest"},
    "CII": {"names": [("Harihar Vithal", "Trivedi")], "eds": True,
            "title": "Corpus Inscriptionum Indicarum, Vol. VII, Part 2: Inscriptions of the Paramāras", "short": "Corpus Inscriptionum Indicarum",
            "kind": "book", "src": "manifest (needs_review)"},
    "GANGULY": {"short": "Paramāra Dynasty", "names": [("D. C.", "Ganguly")], "title": "History of the Paramāra Dynasty", "year": 1933, "kind": "book", "src": "manifest"},
    "GAZ": {"names": [("P. N.", "Shrivastav"), ("Rajendra", "Verma")], "eds": True, "title": "Madhya Pradesh District Gazetteers: Vidisha",
            "short": "District Gazetteers: Vidisha", "year": 1979, "kind": "book",
            "src": "manifest twin row vidisha-district-gazetteer.md (the active row 'Vidisha Gazeteer.md' says 'likely the same gazetteer')",
            "confirm": "editors and year are taken from the manifest's twin row; confirm they belong to this copy"},
    "GEOHER": {"names": [], "title": "Geo-Heritage of Udaypur, Vidisha District, Madhya Pradesh: The Third Eye", "short": "Geo-Heritage of Udaypur",
               "kind": "report", "src": "manifest (needs_review)"},
    "HARDY": {"short": "Temple Architecture of India", "names": [("Adam", "Hardy")], "title": "The Temple Architecture of India", "year": 2007, "kind": "book", "src": "manifest (needs_review)"},
    "INTACH": {"short": "Architectural Splendor of Udaypur", "corp": "INTACH Bhopal", "names": [], "title": "The Architectural Splendor of Udaypur", "year": 2022, "kind": "report", "src": "manifest"},
    "JAGTA": {"names": [("Vijay Manohar", "Tiwari")], "title": "Jagta Hua Kasba", "kind": "book",
              "edition": "Hindi original (कथा उदयपुर); English translation cited, its page numbers approximated to the Hindi original",
              "src": "author per the editor; the manifest records no author, year or publisher"},
    "KRAM": {"short": "Hindu Temple", "names": [("Stella", "Kramrisch")], "title": "The Hindu Temple", "year": 1946, "volumes": "2 vols.", "kind": "book", "src": "manifest"},
    "MADHYABHARAT": {"short": "Cultural Heritage of Madhya Bharat", "names": [("D. R.", "Patil")], "title": "The Cultural Heritage of Madhya Bharat", "year": 1952, "kind": "book", "src": "manifest"},
    "PANDE": {"names": [("Anupa", "Pande")], "title": "The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta",
              "short": "The Udayeśvara Temple", "kind": "book", "src": "manifest (needs_review)"},
    "PARMAR-RAJPUT": {"short": "Parmar Rajput Dynasty", "names": [("Pratapsinh Ranaji", "Venziya")], "title": "History of the Parmar Rajput Dynasty", "year": 2025, "kind": "article",
                      "journal": "The Academic: International Journal of Multidisciplinary Research",
                      "src": "manifest (journal from twin row parmar-rajput-dynasty-origins.md)"},
    "PARTEMPLES": {"names": [("Swati Mondal", "Adhikari")], "title": "Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un",
                   "short": "Some Paramāra Temples", "year": 2013, "kind": "book", "src": "manifest"},
    "RAJABHOJ-EN": {"names": [("Bhagwatilal", "Rajpurohit")], "title": "Raja Bhoj aur Parmarkaleen Nagar Sthapatya",
                    "trans_title": "King Bhoj and Paramara-period Town Architecture", "short": "Raja Bhoj aur Parmarkaleen Nagar Sthapatya",
                    "edition": "English translation cited", "kind": "book", "src": "manifest (needs_review)"},
    "SERPENT": {"names": [("Saarthak", "Singh")], "title": "A Serpentine Scimitar of Letters from Udaypur, District Vidisha",
                "short": "A Serpentine Scimitar of Letters", "year": 2019, "kind": "article",
                "src": "manifest: author from row serpentine-scimitar-inscription-udaypur.md, year from row A_serpentine_scimitar_of_letters_from_Ud.md",
                "confirm": "author's full name and year come from two manifest rows for the same article; journal not recorded"},
    "TEMPLES-IND": {"short": "Temples of North India", "names": [("Krishna", "Deva")], "title": "Temples of North India", "year": 1969, "kind": "book",
                    "src": "manifest twin row Temples_of_India.md (title, 1969); author from the book's title page as recorded in the evidence log",
                    "confirm": "the active file is titled 'Temples of India' in the manifest; title, author and year come from its twin row and title page"},
    "SAMAR-1": {"names": [("", "Bhojadeva")], "title": "Samarāṅgaṇasūtradhāra", "volumes": "vol. 1", "kind": "book", "src": "manifest (attrib.)"},
    "SAMAR-2": {"names": [("", "Bhojadeva")], "title": "Samarāṅgaṇasūtradhāra", "volumes": "vol. 2", "kind": "book", "src": "manifest (attrib.)"},
    "TEMPLE-ECON": {"names": [("Sandeep", "Singh")], "title": "Temple Economics (Arthavyavasthā of Mandirs), Volume I", "short": "Temple Economics",
                    "kind": "book", "src": "manifest (needs_review)"},
    "GUPTE": {"names": [("R. S.", "Gupte")], "title": "Iconography of the Hindus, Buddhists and Jains", "year": 1972, "kind": "book", "src": "manifest"},
    "BHOJDEV-HI": {"names": [], "title": "Bhojadeva (भोजदेव)", "kind": "book", "src": "manifest (needs_review)"},
}
BOOK_OF = {"JAGTA-EN": "JAGTA", "JAGTA-HI": "JAGTA", "KRAM-1": "KRAM", "KRAM-2": "KRAM"}
VOL_OF = {"KRAM-1": "1", "KRAM-2": "2"}


def book_key(code):
    return BOOK_OF.get(code, code)


def names_str(b, inverted=False):
    if b.get("corp"):
        return b["corp"]
    ns = b.get("names") or []
    if not ns:
        return ""
    def one(g, s, inv):
        return (f"{s}, {g}" if g else s) if inv else (f"{g} {s}".strip())
    if inverted:
        out = one(*ns[0], True) + "".join((", and " if k == len(ns) - 1 else ", ") + one(*n, False) for k, n in enumerate(ns[1:], 1))
    elif len(ns) >= 4:                     # Chicago 17th: four or more authors -> first author et al. in notes
        out = one(*ns[0], False) + " et al."
    else:
        out = " and ".join(one(*n, False) for n in ns) if len(ns) <= 2 else ", ".join(one(*n, False) for n in ns[:-1]) + ", and " + one(*ns[-1], False)
    if b.get("eds"):
        out += ", ed." if len(ns) == 1 else ", eds."
    return out


def surname(b):
    if b.get("corp"):
        return b["corp"]
    ns = b.get("names") or []
    if len(ns) == 2:
        return f"{ns[0][1]} and {ns[1][1]}"
    if len(ns) >= 4:
        return f"{ns[0][1]} et al."
    return ns[0][1] if ns else ""


def short_title(b):
    if b.get("short"):
        return b["short"]
    t = b["title"].split(":")[0]
    w = t.split()
    return " ".join(w[:5]) if len(w) > 5 else t


def facts(b):
    pub = ": ".join(x for x in (b.get("place"), b.get("publisher")) if x)
    parts = ", ".join(str(x) for x in (pub or None, b.get("year")) if x)
    return parts


def page_str(it):
    p = it["page"].strip()
    m = re.match(r"≈\s*p\.\s*([\d–-]+)", p)
    if m:
        return f"≈ {m.group(1)} (Hindi-original page)"
    if p.startswith("no page"):
        rest = p.split(";", 1)[1].strip() if ";" in p else ""
        return "no page" + (f"; {rest}" if rest else "")
    return re.sub(r"^p\.\s*", "", p)


def title_fmt(b, short=False):
    t = short_title(b) if short else b["title"]
    if b["kind"] == "article":
        return f"“{t}”"
    return f"*{t}*"


def full_note(it, b):
    code = it["book_code"]
    who = names_str(b)
    t = title_fmt(b)
    extra = []
    if b.get("trans_title"):
        t += f" [{b['trans_title']}]"
    if code == "JAGTA-EN":
        extra.append("English translation")
    elif code == "JAGTA-HI":
        extra.append("Hindi original")
    elif b.get("edition") and code != "JAGTA-EN":
        extra.append(b["edition"])
    if b["kind"] == "article":
        jr = f" *{b['journal']}*" if b.get("journal") else ""
        yr = f" ({b['year']})" if b.get("year") else ""
        loc = f"{jr}{yr}"
        s = (f"{who}, " if who else "") + t[:-1] + ",”" + (loc if b.get("journal") else f" {b['year']}" if b.get("year") else "")
    else:
        f = facts(b)
        vol = ""
        if code in VOL_OF:
            vol = f", vol. {VOL_OF[code]}"
        s = (f"{who}, " if who else "") + t + vol + (f", {', '.join(extra)}" if extra else "") + (f" ({f})" if f else "")
    return s


def short_note(it, b):
    code = it["book_code"]
    t = title_fmt(b, short=True)
    s = (f"{surname(b)}, " if surname(b) else "") + t
    if code in VOL_OF:
        s += f", vol. {VOL_OF[code]}"
    if code == "JAGTA-HI":
        s += " (Hindi original)"
    return s


def note_for(it, seen):
    code = it["book_code"]
    k = book_key(code)
    b = BIB.get(k) or {"names": [], "title": it["book_title"], "kind": "book"}
    first = k not in seen or (code == "JAGTA-HI" and "JAGTA-HI" not in seen)
    s = full_note(it, b) if first else short_note(it, b)
    seen.add(k)
    seen.add(code)
    if b["kind"] == "article" and first and b.get("journal"):
        s += f": {page_str(it)}"                  # Chicago: journal article locator after a colon
    elif b["kind"] == "article":
        s = s[:-1] + f",” {page_str(it)}" if s.endswith("”") else s + f", {page_str(it)}"
    else:
        s += f", {page_str(it)}"
    if "⚠" in it["flags"]:
        s += " (verify against source)"
    return s


def bib_entry(k):
    b = BIB.get(k, {"names": [], "title": k, "kind": "book"})
    who = names_str(b, inverted=True)
    if b["kind"] == "article":
        s = (f"{who.rstrip('.')}. " if who else "") + f"“{b['title']}.”"
        if b.get("journal"):
            s += f" *{b['journal']}*"
        if b.get("year"):
            s += f" ({b['year']})" if b.get("journal") else f" {b['year']}"
        return s.rstrip() + "."
    s = (f"{who.rstrip('.')}. " if who else "") + f"*{b['title']}*"
    if b.get("trans_title"):
        s += f" [{b['trans_title']}]"
    s += "."
    if b.get("volumes") and k == "KRAM":
        s += f" {b['volumes'].capitalize()}"[:-1] + "."
    if b.get("edition"):
        s += f" {b['edition'][0].upper() + b['edition'][1:]}."
    f = facts(b)
    if f:
        s += f" {f}."
    return s


def incomplete_entries(keys):
    out = []
    for k in keys:
        b = BIB.get(k, {})
        missing = [f for f in (("year",) if b.get("kind") == "article" else ("place", "publisher", "year")) if not b.get(f)]
        if b.get("kind") == "article" and not b.get("journal"):
            missing.append("journal")
        if not (b.get("names") or b.get("corp")):
            missing.append("author/editor")
        if missing or b.get("confirm"):
            out.append({"book": b.get("title", k), "code": k, "missing": missing, "confirm": b.get("confirm", ""), "source": b.get("src", "")})
    return out


def load_pack():
    p = D / "evidence_pack_v2.json"
    if not p.exists():
        p = D / "evidence_pack.json"
    return {i["id"]: i for i in json.loads(p.read_text(encoding="utf-8"))}


def convert(src: Path, dst: Path, P):
    text = src.read_text(encoding="utf-8")
    text = re.split(r"(?m)^---\s*$\n+(?:## )?(?:Notes|Bibliography):?\s*$", text)[0].rstrip() + "\n"
    notes, used, seen = [], [], set()

    def rep(m):
        ids = [x.strip() for x in re.split(r"[;,]", m.group(1))]
        parts, kept = [], []
        for x in ids:
            if x == "AUTHOR":
                parts.append("Author's site notes")
            elif x in P:
                parts.append(note_for(P[x], seen))
                kept.append(x)
                k = book_key(P[x]["book_code"])
                if k not in used:
                    used.append(k)
        notes.append("; ".join(parts) + "." + (f" <!-- {'; '.join(kept)} -->" if kept else ""))
        return f"[^{len(notes)}]"

    body = BR.sub(rep, text)
    body = re.sub(r"[ \t]+(\[\^\d+\])", r"\1", body).rstrip()
    keys = sorted(used, key=lambda k: re.sub(r"[^\w ]", "", (names_str(BIB.get(k, {}), True) or BIB.get(k, {}).get("title", k))).lower())
    out = (body + "\n\n---\n\n## Notes\n\n" + "\n".join(f"[^{i}]: {n}" for i, n in enumerate(notes, 1))
           + "\n\n## Bibliography\n\n" + "\n\n".join(bib_entry(k) for k in keys) + "\n")
    dst.write_text(out, encoding="utf-8")
    return len(notes), keys


def main():
    P = load_pack()
    src = D / (sys.argv[1] if len(sys.argv) > 1 else "ch02_draft_v1.md")
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_footnoted.md")
    if not dst.is_absolute():
        dst = D / dst
    n, keys = convert(src, dst, P)
    inc = incomplete_entries(keys)
    (dst.with_suffix(".bibliography_todo.json")).write_text(json.dumps(inc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{dst.name}: {n} footnotes, {len(keys)} bibliography entries; {len(inc)} incomplete entries")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
