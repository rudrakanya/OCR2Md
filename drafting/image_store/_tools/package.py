"""Package the image store for a shared Google Drive folder (free, local; no API).

  python -I -X utf8 drafting/image_store/_tools/package.py

1. Captions: the List of Plates wording, as transcribed from the scanned List (list_of_plates_checked.json), replaces
   the on-plate OCR; real differences between the plate caption and the List are kept as a variant note.
2. Corrections: face labels read from the plate scans, the Arthunā LXXXV/LXXXVI numbers, the LXXXVII-B letter;
   the caption-line crop on Plate XVI is excluded.
3. Files are copied under readable names into for_drive/<folder>/..., with the caption embedded as PNG iTXt chunks
   (and an XMP packet). The chunks are inserted before IEND; the IDAT image data is copied byte for byte.
4. Writes the index (.xlsx and index.md), a README, and updates image_manifest.jsonl (old -> new names).
"""
from __future__ import annotations

import datetime
import html
import io
import json
import re
import struct
import unicodedata
import zipfile
import zlib
from pathlib import Path

STORE = Path(__file__).resolve().parents[1]
DRIVE_NAME = "Udaypur — Inscription Plates (CII VII.2)"
OUT = STORE / "for_drive" / DRIVE_NAME
SUB_PLATES = "Plates (full page)"
SUB_IMAGES = "Separated images"
SUB_OTHER = "Other (front matter)"
SOURCE = ("Corpus Inscriptionum Indicarum, Vol. VII, Part 2: Inscriptions of the Paramāras, ed. H. V. Trivedi "
          "(Archaeological Survey of India)")

# ------------------------------------------------------------------ corrections read from the scans (22 Oct 2026)
# face labels printed above each image, read from the page images by eye (keyed by stable ID)
FACES = {
    "CII7.2-P001-1": "i", "CII7.2-P001-2": "ii", "CII7.2-P002-1": "i", "CII7.2-P002-2": "ii",
    "CII7.2-P004-1": "i", "CII7.2-P004-2": "ii", "CII7.2-P005-1": "i", "CII7.2-P005-2": "ii",
    "CII7.2-P007-1": "i", "CII7.2-P007-2": "ii", "CII7.2-P012-1": "i", "CII7.2-P012-2": "ii",
    "CII7.2-P013-1": "i", "CII7.2-P013-2": "ii", "CII7.2-P014-1": "i", "CII7.2-P014-2": "ii",
    "CII7.2-P015-1": "i", "CII7.2-P015-2": "ii", "CII7.2-P016-B": "i (a)",
    "CII7.2-P017-b": "i (b)", "CII7.2-P017-2": "ii", "CII7.2-P018-1": "i", "CII7.2-P018-a": "ii (a)",
    "CII7.2-P019-A_b": "ii (b)", "CII7.2-P019-A": "iii", "CII7.2-P020-1": "i", "CII7.2-P020-2": "ii",
    "CII7.2-P036-2": "ii", "CII7.2-P041-B": "i", "CII7.2-P042-1": "i", "CII7.2-P042-2": "ii",
    "CII7.2-P045-1": "i", "CII7.2-P045-2": "ii", "CII7.2-P049-1": "i", "CII7.2-P049-a": "ii (a)",
    "CII7.2-P050-b": "ii (b)", "CII7.2-P050-2": "ii.", "CII7.2-P056-1": "i", "CII7.2-P056-a": "ii (a)",
    "CII7.2-P060-1": "i", "CII7.2-P060-2": "ii (a)", "CII7.2-P061-b": "ii (b)", "CII7.2-P061-a": "iii (a)",
    "CII7.2-P062-1": "iii (b)", "CII7.2-P062-2": "iv (a)",
    "CII7.2-P031-Leftside": "Left side", "CII7.2-P031-Rightside": "Right side",
    "CII7.2-P043-Leftside": "Left side", "CII7.2-P043-Rightside": "Right side",
    "CII7.2-P074-Leftside": "Left side", "CII7.2-P074-Rightside": "Right side",
}
FACE_NOTES = {
    "CII7.2-P036-1": "no face label is printed above this image (the second is labelled ii)",
    "CII7.2-P050-2": "printed 'ii.'; after ii (b) on the same plate this may be a damaged 'iii' — check the page image",
}
# sub-letters confirmed on the plate page by eye (the OCR missed or mis-read them)
SUBLETTER = {"CII7.2-P081-1": "A", "CII7.2-P073-1": "A", "CII7.2-P087-B": "B"}
EXCLUDE = {"CII7.2-P016-A_2": "a single caption line (A— British Museum ...), detected as an image before the "
                              "caption-line filter was added; not an image"}
# inscription numbers: the plate pages and the List put No. 84 (V.S. 1136) on LXXXIV-LXXXV and No. 85 (V.S. 1137) on
# LXXXVI; the Contents and the edition heading print "No. 85; PLATE LXXXV".
NOS_FIX = {"LXXXV": [84], "LXXXVI": [85]}
NOS_NOTE = {"LXXXV": "Contents and the edition heading print 'No. 85; PLATE LXXXV'; the plate caption (V.S. 1136) and "
                     "the List of Plates (LXXXIV–LXXXV, Year 1136) put this plate with No. 84.",
            "LXXXVI": "The plate caption (V.S. 1137) and the List of Plates put No. 85 here; the Contents and the "
                      "edition heading print 'PLATE LXXXV' for No. 85."}
# real differences between the plate's own caption and the List (read on the plate pages)
VARIANTS = {
    "XVI-A": "Plate caption: 'A— British Museum Saraswatī Image Inscription of the Time of Bhōjadēva: (Vikrama) Year 1091'.",
    "XIX-B": "Plate caption: 'B— Bhōjpur Image Inscription of the Time of Bhōjadēva: (Undated)'; the List has 'fragmentary Stone Inscription'.",
    "XX": "Plate caption: 'Māndhātā Copper-plate Grant of Jayasiṁha I: (Vikrama) Year 1112'.",
    "XXI-B": "Plate caption: 'B— Dhār Image Inscription of the Time of Udayāditya: (Vikrama) Year 1138'.",
    "XXII": "Plate caption gives (Vikrama) Year 1140 (and 'Kamēd Stone Inscription'); the List prints 1040.",
    "XXVII": "Plate caption: 'Mahākālēśvara Temple Sarpa-bandha Inscription (Ujjain): (Undated)'.",
    "XXVIII": "Plate caption: 'Dhār Sarpa-bandha Inscription: A (Duplicate and Undated)'.",
    "XXIX": "Plate caption: 'Dhār Sarpa-bandha Inscription: B (Undated)'.",
    "XXXIV-A": "Plate caption: 'A — Dēwās Copper-plate Inscription of Naravarman: (Fragmentary), (Vikrama) Year 1152'.",
    "XXXIV-B": "Plate caption: 'B — Bhōjpur Stone Inscription of the Time of Naravarman: (Vikrama) Year 1157'; the List has 'Image Inscription'.",
    "XL-B": "Plate caption: 'B — Ujjain Copper-plate Inscription of Jayavarman: (Undated)'; the List has '(fragmentary)'.",
    "XLV": "Plate caption adds the date: '(Vikrama) Year 1214'.",
    "LXXVIII": "Plate caption: 'Copper-plate Inscription of the Paramāras of Chandrāvatī: (Fragmentary and Undated)' (no place-name).",
    "LXXXVII-B": "Plate caption: 'B — Arthūṇā Stone Inscription of the Time of Chāmuṇḍarāja: (Vikrama) Year 1159'; the List has 'Image Inscription'.",
}


def roman(n):
    s = ""
    for a, r in [(90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= a:
            s += r
            n -= a
    return s


def ascii_fold(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("—", "-").replace("–", "-")


def face_for_name(face):
    """'ii (b)' -> 'ii, b'; 'ii.' -> 'ii' (file names avoid nested brackets; metadata keeps the printed form)."""
    return re.sub(r"\s*\((\w)\)", r", \1", face).rstrip(".")


def short_caption(title):
    t = title
    t = re.sub(r"\s*:\s*\(Vikrama\)?\s*Years?\s*", ", VS ", t)
    t = re.sub(r"\s*:\s*\(Vikrama\s+Year\s*", ", VS ", t)
    t = re.sub(r"\s*:\s*Śaka Year\s*", ", Saka ", t)
    t = t.replace(" : ", ", ").replace(" :", "").replace("(Undated)", "undated").replace("(fragmentary)", "fragmentary")
    t = t.replace("(Fragmentary)", "fragmentary").replace("(Date lost ?)", "date lost").replace("(sarpabandha)", "sarpabandha")
    t = ascii_fold(t)
    t = re.sub(r'[\\/:*?"<>|]', "", t)
    t = re.sub(r"\s+", " ", t).strip(" ,.")
    if len(t) > 95:
        t = t[:95].rsplit(" ", 1)[0]
    return t


# ------------------------------------------------------------------ PNG text chunks (no recompression)
def chunk(typ, data):
    c = typ + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def itxt(key, text):
    return chunk(b"iTXt", key.encode("latin-1") + b"\x00\x00\x00" + b"\x00" + b"\x00" + text.encode("utf-8"))


def xmp(title, desc, ident, source):
    e = html.escape
    x = ('<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
         '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
         '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">'
         f'<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{e(title)}</rdf:li></rdf:Alt></dc:title>'
         f'<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{e(desc)}</rdf:li></rdf:Alt></dc:description>'
         f'<dc:identifier>{e(ident)}</dc:identifier><dc:source>{e(source)}</dc:source>'
         '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>')
    return itxt("XML:com.adobe.xmp", x)


def tag_png(src, dst, fields, title, desc, ident):
    b = src.read_bytes()
    assert b[:8] == b"\x89PNG\r\n\x1a\n"
    # drop any earlier text chunks, keep everything else byte for byte
    out, pos = [b[:8]], 8
    while pos < len(b):
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        typ = b[pos + 4:pos + 8]
        whole = b[pos:pos + 12 + n]
        pos += 12 + n
        if typ in (b"tEXt", b"iTXt", b"zTXt"):
            continue
        if typ == b"IEND":
            for k, v in fields.items():
                out.append(itxt(k, v))
            out.append(xmp(title, desc, ident, SOURCE))
        out.append(whole)
    dst.write_bytes(b"".join(out))


def read_itxt(p):
    b, pos, d = p.read_bytes(), 8, {}
    while pos < len(b):
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        typ, data = b[pos + 4:pos + 8], b[pos + 8:pos + 8 + n]
        pos += 12 + n
        if typ == b"iTXt":
            k, rest = data.split(b"\x00", 1)
            # compression flag, method, language\0, translated keyword\0, text
            rest = rest[2:]
            _, rest = rest.split(b"\x00", 1)
            _, text = rest.split(b"\x00", 1)
            d[k.decode("latin-1")] = text.decode("utf-8")
    return d


def idat(p):
    b, pos, parts = p.read_bytes(), 8, []
    while pos < len(b):
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        if b[pos + 4:pos + 8] in (b"IDAT", b"IHDR", b"PLTE"):
            parts.append(b[pos:pos + 12 + n])
        pos += 12 + n
    return b"".join(parts)


# ------------------------------------------------------------------ minimal xlsx (no third-party library)
def col(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, header, rows, widths):
    def cell(ci, ri, v, bold=False):
        ref = f"{col(ci)}{ri}"
        s = ' s="1"' if bold else ""
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return f'<c r="{ref}"{s}><v>{v}</v></c>'
        t = html.escape(str(v if v is not None else ""))
        return f'<c r="{ref}" t="inlineStr"{s}><is><t xml:space="preserve">{t}</t></is></c>'
    data = [f'<row r="1">' + "".join(cell(i, 1, h, True) for i, h in enumerate(header)) + "</row>"]
    for r, row in enumerate(rows, start=2):
        data.append(f'<row r="{r}">' + "".join(cell(i, r, v) for i, v in enumerate(row)) + "</row>")
    last = f"{col(len(header) - 1)}{len(rows) + 1}"
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
             f'<cols>{cols}</cols><sheetData>{"".join(data)}</sheetData><autoFilter ref="A1:{last}"/></worksheet>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
              '<cellXfs count="2"><xf fontId="0"/><xf fontId="1" applyFont="1"/></cellXfs></styleSheet>')
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<sheets><sheet name="Plates" sheetId="1" r:id="rId1"/></sheets>'
          f'<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">Plates!$A$1:${col(len(header) - 1)}${len(rows) + 1}</definedName></definedNames></workbook>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   '</Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                   '</Relationships>')
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                   '</Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", sheet)
        z.writestr("xl/styles.xml", styles)


# ------------------------------------------------------------------ main
def main():
    R = [json.loads(l) for l in (STORE / "image_manifest.jsonl").open(encoding="utf-8")]
    L = json.loads((STORE / "list_of_plates_checked.json").read_text(encoding="utf-8"))["entries"]
    by_plate = {}
    for e in L:
        for p in e["plates"]:
            by_plate[p] = e
    for d in (OUT / SUB_PLATES, OUT / SUB_IMAGES, OUT / SUB_OTHER):
        d.mkdir(parents=True, exist_ok=True)
    used = set()
    rows = []
    corrected = 0
    for r in R:
        lab = r.get("plate_roman")
        rid = r["id"]
        if rid in EXCLUDE:
            r.update({"excluded": EXCLUDE[rid], "drive_file": None})
            continue
        sub = SUBLETTER.get(rid) or (r.get("sub_label") if r.get("sub_label") in ("A", "B") else None)
        face = FACES.get(rid) if r["kind"] == "image" else None
        notes = []
        # authoritative caption from the checked List
        if r["kind"] == "emblem":
            entry, cap = None, None
        elif sub and f"{lab}-{sub}" in by_plate:
            entry = by_plate[f"{lab}-{sub}"]
            cap = entry["title"]
        elif lab in by_plate:
            entry = by_plate[lab]
            cap = entry["title"]
        else:   # a plate in A/B parts: both entries
            parts = [by_plate[f"{lab}-{s}"] for s in "AB" if f"{lab}-{s}" in by_plate]
            entry = parts[0] if parts else None
            cap = "; ".join(f"{s} — {p['title']}" for s, p in zip("AB", parts)) if parts else None
        key = f"{lab}-{sub}" if sub else lab
        if r["kind"] == "plate" and not (lab in by_plate):
            variant = " ".join(VARIANTS[f"{lab}-{s}"] for s in "AB" if f"{lab}-{s}" in VARIANTS) or None
        else:
            variant = VARIANTS.get(key) or (VARIANTS.get(lab) if not sub else None)
        if entry and entry.get("note"):
            notes.append("List: " + entry["note"])
        if rid in FACE_NOTES:
            notes.append(FACE_NOTES[rid])
        nos = r.get("inscription_nos") or []
        if lab in NOS_FIX:
            nos = NOS_FIX[lab]
            notes.append(NOS_NOTE[lab])
        if rid in SUBLETTER:
            notes.append(f"sub-letter {SUBLETTER[rid]} read on the plate page (the OCR missed it)")
        old_cap = r.get("caption") or r.get("plate_caption") or ""
        if cap and old_cap and old_cap != cap:
            corrected += 1
        # label and file name
        label = f"Plate {lab}" + (f"-{sub}" if sub and r["kind"] == "image" else "") if lab else "Emblem"
        if r["kind"] == "plate" and r.get("file") is None:
            status = "absent from the scan (record only)"
        elif FACE_NOTES.get(rid) and "check" in FACE_NOTES[rid]:
            status = "List wording (checked against the scan); face label to check"
        elif r["kind"] == "emblem":
            status = "no printed caption"
        else:
            status = "List wording (checked against the scan)"
        if r.get("file") is None:
            r.update({"caption_final": cap, "caption_status": status, "hand_verified": False, "drive_file": None,
                      "inscription_nos": nos, "notes": notes})
            rows.append([None, "(no file)", label, "", cap, r.get("caption") or "", variant or "", ", ".join(map(str, nos)),
                         r.get("page"), entry["location"] if entry else "", "missing from scan", status, "; ".join(notes), rid, ""])
            continue
        if r["kind"] == "plate":
            folder, fname = SUB_PLATES, f"{label} [full page] — {short_caption(cap)}.png"
        elif r["kind"] == "emblem":
            folder, fname = SUB_OTHER, "Emblem of the Archaeological Survey of India (title page, p. 6).png"
        else:
            folder = SUB_IMAGES
            facepart = f" ({face_for_name(face)})" if face else ""
            fname = f"{label}{facepart} — {short_caption(cap)}.png"
        fname = re.sub(r'[\\/:*?"<>|]', "", fname)
        base, n = fname, 2
        while (folder, fname.lower()) in used:
            fname = base[:-4] + f" ({n}).png"
            n += 1
        used.add((folder, fname.lower()))
        src = STORE / r["file"]
        dst = OUT / folder / fname
        full_label = label + (f" ({face})" if face else "") + (" [full page]" if r["kind"] == "plate" else "")
        caption_meta = cap or r.get("note") or ""
        fields = {
            "Title": f"{full_label} — {cap}" if cap else full_label,
            "Description": caption_meta + (f" | Plate variant: {variant}" if variant else ""),
            "Label": full_label, "Caption": caption_meta,
            "InscriptionNo": ", ".join(map(str, nos)), "SourcePage": f"PDF page {r.get('page')}"
                                                                     + (f"; {entry['location']}" if entry else ""),
            "ImageType": r.get("image_type") or "", "StableID": rid, "Source": SOURCE,
            "CaptionStatus": status,
        }
        tag_png(src, dst, fields, fields["Title"], fields["Description"], rid)
        r.update({"caption_final": cap, "caption_status": status, "hand_verified": False, "variant_note": variant,
                  "notes": notes, "face_label": face, "sub_label_final": sub, "label_final": full_label,
                  "inscription_nos": nos, "old_file": r["file"], "drive_file": f"{folder}/{fname}"})
        rows.append([folder, fname, full_label, face or (sub or ""), cap or "", r.get("caption") or "",
                     variant or "", ", ".join(map(str, nos)), r.get("page"), entry["location"] if entry else "",
                     r.get("image_type"), status, "; ".join(notes), rid, Path(r["file"]).name])
    # manifest (old -> new names kept in old_file / drive_file)
    with (STORE / "image_manifest.jsonl").open("w", encoding="utf-8") as f:
        for r in R:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for x in rows:   # sortable plate number (Drive sorts Roman numerals alphabetically)
        m = re.match(r"Plate ([IVXLC]+)", x[2] or "")
        x.insert(3, {roman(i): i for i in range(1, 100)}.get(m.group(1), "") if m else "")
    header = ["Folder", "Filename", "Label", "Plate no. (sort)", "Sub-label / face", "Caption (List of Plates)",
              "On-plate caption (OCR)", "Plate variant", "Inscription No.", "PDF page", "Printed location",
              "Image type", "Caption status", "Notes", "Stable ID", "Old filename"]
    rows.sort(key=lambda x: (x[0] or "", x[3] if isinstance(x[3], int) else 999, x[14]))
    write_xlsx(OUT / "Index — Inscription Plates (CII VII.2).xlsx", header, rows,
               [20, 70, 26, 10, 14, 70, 60, 50, 12, 9, 22, 22, 30, 50, 22, 26])
    md = [f"# {DRIVE_NAME}", "",
          f"Plates and separated images from *{SOURCE}*. Captions are the authors' List of Plates wording, "
          "transcribed from the scanned List and kept with the authors' spelling and diacritics; where the plate's own "
          "caption differs, the difference is given as a variant. Each image file also carries its label and caption "
          "in its embedded metadata.", "",
          f"Built {datetime.date.today().isoformat()}. Plate LXVII is absent from the scanned volume (record only).", "",
          "| Folder | Filename | Label | Caption (List of Plates) | No. | PDF p. | Type | Status | Plate variant / notes |",
          "|---|---|---|---|---|---|---|---|---|"]
    esc = lambda s: str(s or "").replace("|", "\\|")
    for x in rows:
        md.append(f"| {esc(x[0])} | {esc(x[1])} | {esc(x[2])} | {esc(x[5])} | {esc(x[8])} | {esc(x[9])} | "
                  f"{esc(x[11])} | {esc(x[12])} | {esc('; '.join(v for v in (x[7], x[13]) if v))} |")
    (OUT / "index.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (OUT / "README.txt").write_text(
        f"{DRIVE_NAME}\n\n"
        f"Source: {SOURCE}.\n\n"
        f"{SUB_PLATES}/  each plate page as printed (91 files; Plate LXVII is absent from the scan).\n"
        f"{SUB_IMAGES}/  each estampage, photograph or facsimile cut from its plate, with its A/B part and face label.\n"
        f"{SUB_OTHER}/  the Survey's emblem from the title page.\n\n"
        "File names: 'Plate <number>[-A/B] (<face>) — <caption>'. The full caption with diacritics, the inscription\n"
        "number, the source page and a stable ID are in the spreadsheet index and inside each PNG (iTXt/XMP fields).\n"
        "Find a plate by label, inscription number or caption text in 'Index — Inscription Plates (CII VII.2).xlsx'.\n",
        encoding="utf-8")
    print("rows", len(rows), "captions replaced", corrected)


if __name__ == "__main__":
    main()
