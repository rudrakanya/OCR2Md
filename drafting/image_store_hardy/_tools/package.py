"""Package the Hardy image store for a shared Google Drive folder (free, local; no API).

  python -I -X utf8 drafting/image_store_hardy/_tools/package.py

Writes for_drive/<folder>/:
  Figures/Ch NN — <chapter>/Fig NN.MM — <caption start>.png   every image file (whole figures and parts) with the
      pixels untouched and the full caption embedded as PNG iTXt chunks and an XMP packet (Title, Description,
      Author, Source, Credit, Identifier). The chunks are inserted before IEND; IDAT is copied byte for byte.
  Maps and others/…                         the four maps, cover, frontispiece, part openers, tailpiece
  Captioned copies/…                     one JPEG per figure with the caption printed beneath it,
      so the caption shows in Drive's preview and travels with a download (whole figures; the parts where a
      figure is stored as parts only)
  Index — <title>.xlsx, index.md, README.txt
and records the Drive names in image_manifest.jsonl (drive_file, drive_captioned).
"""
from __future__ import annotations

import html
import json
import re
import shutil
import struct
import textwrap
import zipfile
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STORE = Path(__file__).resolve().parents[1]
TITLE = "Hardy, Temple Architecture of India (2007)"
DRIVE_NAME = "Udaypur — Hardy 2007 figures"
OUT = STORE / "for_drive" / DRIVE_NAME
SUB_FIG = "Figures"
SUB_OTHER = "Maps and others"
SUB_CAP = "Captioned copies"
SOURCE = "Adam Hardy, The Temple Architecture of India (Chichester: John Wiley & Sons, 2007)"
AUTHOR = "Adam Hardy"
FONT = "C:/Windows/Fonts/georgia.ttf"
FONT_B = "C:/Windows/Fonts/georgiab.ttf"
VIEW_MAX = 1800          # longest side of a captioned viewing copy, px


# ------------------------------------------------------------------ names
def safe(s):
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")


def short_caption(r, n=45):
    c = r.get("caption_without_credit") or r.get("caption") or ""
    c = re.sub(r"^\s*\d{1,2}\.\d{1,2}\s*", "", c)
    c = re.sub(r"^(Top left|Top right|Right)\s+Map \d\.\s*", "", c)
    c = re.sub(r"^Map \d\.\s*", "", c)
    c = re.split(r"(?<=[a-z0-9)])[.:;](\s|$)", c)[0]
    if len(c) > n:
        c = c[:n].rsplit(" ", 1)[0].rstrip(",;( ")
    return safe(c)


def label_stem(r):
    if r["scheme"] == "figure":
        stem = f"Fig {r['chapter']:02d}.{r['number']:02d}"
    else:
        stem = r["label"]
    if r["kind"] == "part":
        stem += r["sub_label"] if r.get("sub_label") else f" part {r['part_index']}"
    if len(r.get("all_pages") or []) > 1 and r["page"] != min(r["all_pages"]):
        stem += " (cont'd)"
    return stem


def chapter_dir(r):
    t = r["chapter_title"]
    if len(t) > 26:
        t = t[:26].rsplit(" ", 1)[0]
    return safe(f"Ch {r['chapter']:02d} — {t}")


# ------------------------------------------------------------------ PNG text chunks (no recompression)
def chunk(typ, data):
    c = typ + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def itxt(key, text):
    return chunk(b"iTXt", key.encode("latin-1") + b"\x00\x00\x00" + b"\x00" + b"\x00" + text.encode("utf-8"))


def xmp(title, desc, ident, credit):
    e = html.escape
    x = ('<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>'
         '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
         '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" '
         'xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">'
         f'<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{e(title)}</rdf:li></rdf:Alt></dc:title>'
         f'<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{e(desc)}</rdf:li></rdf:Alt></dc:description>'
         f'<dc:creator><rdf:Seq><rdf:li>{e(AUTHOR)}</rdf:li></rdf:Seq></dc:creator>'
         f'<dc:identifier>{e(ident)}</dc:identifier><dc:source>{e(SOURCE)}</dc:source>'
         + (f'<photoshop:Credit>{e(credit)}</photoshop:Credit>' if credit else "")
         + '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>')
    return itxt("XML:com.adobe.xmp", x)


def tag_png(src, dst, fields, title, desc, ident, credit):
    b = src.read_bytes()
    assert b[:8] == b"\x89PNG\r\n\x1a\n"
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
                if v:
                    out.append(itxt(k, v))
            out.append(xmp(title, desc, ident, credit))
        out.append(whole)
    dst.write_bytes(b"".join(out))


def idat(p):
    b, pos, parts = p.read_bytes(), 8, []
    while pos < len(b):
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        if b[pos + 4:pos + 8] in (b"IDAT", b"IHDR", b"PLTE"):
            parts.append(b[pos:pos + 12 + n])
        pos += 12 + n
    return b"".join(parts)


def read_itxt(p):
    b, pos, d = p.read_bytes(), 8, {}
    while pos < len(b):
        n = struct.unpack(">I", b[pos:pos + 4])[0]
        typ, data = b[pos + 4:pos + 8], b[pos + 8:pos + 8 + n]
        pos += 12 + n
        if typ == b"iTXt":
            k, rest = data.split(b"\x00", 1)
            rest = rest[2:]
            _, rest = rest.split(b"\x00", 1)
            _, text = rest.split(b"\x00", 1)
            d[k.decode("latin-1")] = text.decode("utf-8")
    return d


# ------------------------------------------------------------------ captioned viewing copy
def captioned(src, dst, head, body, foot):
    im = Image.open(src).convert("RGB")
    s = min(1.0, VIEW_MAX / max(im.size))
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    # tall narrow figures get a wider caption panel, so the caption stays legible beside the picture's height
    W = max(im.width, 1100, round(im.height * 0.75))
    fs = max(24, round(max(W, im.height) / 60))
    f, fb, fsm = ImageFont.truetype(FONT, fs), ImageFont.truetype(FONT_B, fs), ImageFont.truetype(FONT, round(fs * .8))
    pad = round(fs * 1.1)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    cpl = max(30, int((W - 2 * pad) / probe.textlength("abcdefghijklmnopqrstuvwxyz", font=f) * 26))
    first, *rest = textwrap.wrap(body, width=cpl - len(head) - 2) or [""]
    rest = textwrap.wrap(" ".join(rest), width=cpl) if rest else []
    lh = round(fs * 1.4)
    H = im.height + pad * 2 + lh * (1 + len(rest)) + (round(lh * 1.3) if foot else 0)
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(im, ((W - im.width) // 2, 0))
    d = ImageDraw.Draw(canvas)
    y = im.height + pad
    d.text((pad, y), head, font=fb, fill=(20, 20, 20))
    d.text((pad + d.textlength(head + "  ", font=fb), y), first, font=f, fill=(20, 20, 20))
    for line in rest:
        y += lh
        d.text((pad, y), line, font=f, fill=(20, 20, 20))
    if foot:
        d.text((pad, y + round(lh * 1.3)), foot, font=fsm, fill=(110, 110, 110))
    canvas.save(dst, "JPEG", quality=90, optimize=True)


# ------------------------------------------------------------------ minimal xlsx (no third-party library)
def col(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, header, rows, widths, sheet_name="Figures"):
    def cell(ci, ri, v, bold=False):
        ref = f"{col(ci)}{ri}"
        s = ' s="1"' if bold else ""
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return f'<c r="{ref}"{s}><v>{v}</v></c>'
        t = html.escape(str(v if v is not None else ""))
        return f'<c r="{ref}" t="inlineStr"{s}><is><t xml:space="preserve">{t}</t></is></c>'
    data = ['<row r="1">' + "".join(cell(i, 1, h, True) for i, h in enumerate(header)) + "</row>"]
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
              '<cellXfs count="3"><xf fontId="0"/><xf fontId="1" applyFont="1"/>'
              '<xf fontId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs></styleSheet>')
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          f'<sheets><sheet name="{sheet_name}" sheetId="1" r:id="rId1"/></sheets>'
          f'<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">{sheet_name}!$A$1:${col(len(header) - 1)}${len(rows) + 1}</definedName></definedNames></workbook>')
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


def comment(r):
    c = f"Chapter {r['chapter']}: {r['chapter_title']}. " if r.get("chapter") else ""
    c += f"PDF page {r['page']}"
    if r.get("caption_page") and r["caption_page"] != r["page"]:
        c += f"; caption printed on PDF page {r['caption_page']}"
    if r.get("caption_hand_checked"):
        return c + ". Caption checked against the page scan."
    return c + (". Caption from OCR, flagged for checking." if r.get("ocr_verify") else ". Caption from OCR, cross-checked.")


# ------------------------------------------------------------------ main
def main():
    recs = [json.loads(l) for l in (STORE / "image_manifest.jsonl").open(encoding="utf-8")]
    # empty the folder in place: a directory held open (Explorer, a sync client, a shell) cannot be removed, but its
    # files can, and an emptied directory is simply reused
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(OUT.rglob("*"), key=lambda p: -len(p.parts)):
        if f.is_file():
            f.unlink()
        else:
            try:
                f.rmdir()
            except OSError:
                pass
    parts_only = {r["label"] for r in recs} - {r["label"] for r in recs if r["kind"] == "whole"}
    used = set()
    rows = []
    for r in recs:
        sub = Path(SUB_FIG) / chapter_dir(r) if r["scheme"] == "figure" else Path(SUB_OTHER)
        name = safe(label_stem(r) + (" — " + short_caption(r) if r.get("caption") else ""))
        rel = sub / f"{name}.png"
        k = 2
        while str(rel).lower() in used:
            rel = sub / f"{name} ({k}).png"
            k += 1
        used.add(str(rel).lower())
        (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
        cap = r.get("caption") or ""
        title = r["label_ref"] + (f" ({r['sub_label'] or 'part ' + str(r['part_index'])})" if r["kind"] == "part" else "")
        fields = {"Title": title, "Description": cap, "Author": AUTHOR, "Source": SOURCE,
                  "Identifier": r["id"], "Credit": r.get("credit") or "",
                  "Comment": comment(r)}
        tag_png(STORE / r["file"], OUT / rel, fields, title, cap, r["id"], r.get("credit"))
        assert idat(STORE / r["file"]) == idat(OUT / rel)
        r["drive_file"] = str(rel).replace("\\", "/")
        r["drive_captioned"] = None
        if r["kind"] == "whole" or r["label"] in parts_only:
            csub = Path(SUB_CAP) / (chapter_dir(r) if r["scheme"] == "figure" else SUB_OTHER)
            (OUT / csub).mkdir(parents=True, exist_ok=True)
            crel = csub / f"{rel.stem}.jpg"
            body = re.sub(r"^\s*\d{1,2}\.\d{1,2}\s*", "", r.get("caption_without_credit") or cap or "")
            head = title if r["scheme"] == "figure" else (r["label"] if r["scheme"] != "map" else "")
            if r["scheme"] == "map":
                head, body = r["label"] + ".", re.sub(r"^(Top left|Top right|Right)\s+Map \d\.\s*|^Map \d\.\s*", "", body)
            foot = "  ·  ".join(x for x in (r.get("credit"), f"{SOURCE}, PDF p. {r['page']}") if x)
            captioned(STORE / r["file"], OUT / crel, head, body or "(no caption printed)", foot)
            r["drive_captioned"] = str(crel).replace("\\", "/")
        rows.append([r["id"], r["label_ref"], r.get("sub_label") or (f"part {r['part_index']}" if r["part_index"] else ""),
                     r.get("chapter") or "", r.get("chapter_title") or "", r["page"], r.get("printed_page") or "",
                     r["image_type"], cap, r.get("credit") or "", "yes" if r.get("caption_hand_checked") else "",
                     "CHECK: " + "; ".join(r["ocr_verify_reasons"]) if r.get("ocr_verify") else "",
                     r["drive_file"], r["drive_captioned"] or ""])
    header = ["ID", "Label", "Part", "Ch.", "Chapter", "PDF page", "Printed page", "Type", "Caption (verbatim)",
              "Credit", "Caption checked by eye", "Flag", "File", "Captioned copy"]
    write_xlsx(OUT / f"Index — {TITLE}.xlsx", header, rows, [24, 12, 8, 5, 30, 8, 8, 14, 90, 26, 10, 40, 60, 60])
    md = [f"# {TITLE}: figure index", "", "| Label | Ch. | PDF p. | Type | Caption | File |", "|---|---|---|---|---|---|"]
    for r in recs:
        if r["kind"] == "whole" or r["label"] in parts_only:
            part = f" {r['sub_label'] or 'part ' + str(r['part_index'])}" if r["kind"] == "part" else ""
            md.append(f"| {r['label_ref']}{part} | {r.get('chapter') or ''} | {r['page']} | {r['image_type']} | "
                      f"{(r.get('caption') or '').replace('|', '/')} | {r['drive_file']} |")
    (OUT / "index.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    nfig = sum(1 for r in recs if r["scheme"] == "figure" and r["kind"] == "whole")
    readme = f"""{DRIVE_NAME}

Source: {SOURCE}. Extracted from the Internet Archive scan (archive.org/details/templearchitectu0000hard).

Figures/  every figure, one folder per chapter: 'Fig CC.NN — <start of caption>.png'. Fig 20.01 is the book's
    Fig. 20.1 (numbers are zero-padded only so that files sort in order). Figures made of several drawings are also
    saved as their separate parts: 'Fig 10.18b', or 'Fig 07.07 part 1' where the book gives no letter.
    Files are the scan's own pixels (about 360 dpi), lossless PNG.
Maps and others/  Maps 1–4, the cover, the frontispiece, the six part-opener photographs, the tailpiece.
Captioned copies/  the same figures as JPEGs with the full caption printed beneath the picture, for
    browsing in Drive or pasting into a document. Use the PNGs in Figures/ for anything that needs the original.

Captions are attached three ways: printed on the captioned copies; embedded inside every PNG (title, full
caption, credit, source, ID, as PNG text fields and XMP — visible in Photoshop, Lightroom, Bridge, exiftool,
IrfanView and most image managers, though Drive's own preview does not show them); and listed in
'Index — {TITLE}.xlsx' (filterable by chapter, type, page; searchable by caption text).

Captions are the author's wording as printed (his transliteration has no diacritics: Shekhari, Bhumija, Udayeshvara).
They were read by OCR and cross-checked; {sum(1 for r in recs if r.get('caption_hand_checked') and r['kind'] == 'whole')} were checked by eye against the scan. A few are
flagged 'CHECK' in the index where a word or the figure number rests on OCR alone.

Photographs and drawings are copyright of the author, John Wiley & Sons and the photographers named in each
caption (most are © Gerard Foekema). This folder is for private research reference; keep the credits with any use.
{nfig} figures, {len(recs)} image files in all.
"""
    (OUT / "README.txt").write_text(readme, encoding="utf-8")
    longest = max(len(str(f.resolve())) for f in OUT.rglob("*") if f.is_file())
    print("longest full path:", longest, "characters")
    assert longest < 240, "paths too long for Windows (260-character limit); shorten names"
    with open(STORE / "image_manifest.jsonl", "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(OUT, len(recs), "files,", sum(1 for r in recs if r["drive_captioned"]), "captioned copies")


if __name__ == "__main__":
    main()
