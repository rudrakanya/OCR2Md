"""Build the Hardy image store: image files, image_manifest.jsonl, image_index.md, review_flags.md, PROVENANCE.md.

  python -I -X utf8 drafting/image_store_hardy/_tools/build.py

Inputs: _work/caption_regions.json, _work/detect.json, overrides.json (run captions.py, caption_regions.py and
run_detect.py first; see README in PROVENANCE.md).

Caption text: the PDF's own (hidden, Internet Archive) OCR text layer inside the caption region is the primary
reading; Tesseract 5 on the same region at native resolution is the cross-reading. Where the two disagree beyond
small noise, or the caption exists only as image (not in the text layer), the record is flagged ocr_verify.
"""
import datetime
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BOOK, PDF, ROOT, WORK, fold, is_texty, lines, native_zoom, open_pdf, render  # noqa: E402
from plan import plan  # noqa: E402

IMG = ROOT / "images"
PAGES = WORK / "pages"
PAD = 6               # native px of margin kept around a picture (never reaching into a caption region)
FOLIO_OFFSET = 4      # printed page = PDF page - 4 (PDF p. 14 is printed p. 10)
SIM_OK = 0.93

# OCR glyph confusions made by both engines on this scan (rn->m, ri->n, small-caps era marks). Each restores the
# book's own printed spelling, checked against the page images; the raw readings stay in caption_tesseract and
# caption_textlayer.
GLYPH_FIXES = [
    (r"\bKamataka\b", "Karnataka"), (r"\bKamata\b", "Karnata"), (r"\bwestem\b", "western"),
    (r"\bsouthem\b", "southern"), (r"\beastem\b", "eastern"), (r"\bnorthem\b", "northern"),
    (r"\bcomer\b", "corner"), (r"\bcomers\b", "corners"), (r"\bpattem\b", "pattern"), (r"\bpattems\b", "patterns"),
    (r"\badom\b", "adorn"), (r"\badoms\b", "adorns"), (r"\bhomed\b", "horned"), (r"\bmodem\b", "modern"),
    (r"\bshnne\b", "shrine"), (r"\bshnnes\b", "shrines"), (r"\bcentunes\b", "centuries"),
    (r"\bcentuny\b", "century"), (r"\bmtroduction\b", "introduction"), (r"\bteflecting\b", "reflecting"),
    (r"\btelief\b", "relief"), (r"\bcomice\b", "cornice"), (r"\bfmeze\b", "frieze"),
    (r"¢\s?(?=\d|early|late|mid|AD|first|second)", "c "),
    (r"\b(?:ap|ab|aD|Ap|ad)\b(?=\s?\d)", "AD"), (r"(?<=\d )(?:ap|ab|aD|Ap)\b", "AD"),
    (r"(?<=century )(?:ap|ab|aD|Ap)\b", "AD"), (r"(?<=\d )Bc\b", "BC"), (r"(?<=centuries )Bc\b", "BC"),
    (r"(?<=century )Bc\b", "BC"), (r"\{", "("), (r"\}", ")"),
    (r"\bCAD\b", "c AD"), (r"\bc(?=(?:mid|late|early)\b)", "c "), (r"\b1s\b", "is"),
]

CHAPTERS = {
    1: "Introduction", 2: "Centres of Power", 3: "Temple, Body and Movement", 4: "The Emanating Universe",
    5: "Placing the Gods", 6: "The Architect and Unfolding Traditions", 7: "Early Indian Architecture",
    8: "Later Rock-Cut Architecture", 9: "Plans and Spaces", 10: "Nagara Shrines", 11: "Dravida Shrines",
    12: "Geometry", 13: "Mouldings", 14: "Pillars", 15: "Ceilings", 16: "Gavakshas", 17: "Early Nagara Temples",
    18: "Latina and Related Valabhi Temples", 19: "Shekhari Temples", 20: "Bhumija Temples",
    21: "Temples of Eastern India", 22: "Early Dravida Temples", 23: "The Great 8th-Century Dravida Temples",
    24: "Temples of the Cholas and Their Contemporaries", 25: "The Karnata Dravida Tradition Continued",
    26: "What Happened Afterwards", 27: "What Next?",
}
UNNUMBERED_ID = {"Cover": "cover", "Frontispiece": "frontispiece", "Tailpiece": "tailpiece"}


def hits(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def union(bs):
    return [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]


def textlayer_in(page, region_px, z):
    r = [v / z for v in region_px]
    out = []
    for x0, y0, x1, y1, s, sz in lines(page):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if r[0] <= cx <= r[2] and r[1] <= cy <= r[3]:
            if sz > 9.6 and not is_texty(s):
                continue          # OCR noise read off a picture
            out.append((round(y0), x0, s))
    out.sort()
    # lines on the same baseline (a split line) are joined left to right
    merged = []
    for y, x, s in out:
        if merged and abs(merged[-1][0] - y) <= 2:
            merged[-1][2].append((x, s))
        else:
            merged.append([y, x, [(x, s)]])
    return [" ".join(s for _, s in sorted(parts)) for _, _, parts in merged]


def join(ls):
    out = ""
    for l in ls:
        l = l.strip()
        if out.endswith("-") and l[:1].islower():
            out = out[:-1] + l
        else:
            out = (out + " " + l).strip()
    return out


OVR = json.loads((ROOT / "_tools" / "overrides.json").read_text(encoding="utf-8"))
OVR_FIXES = OVR.get("caption_fixes", {})
OVR_VERIFIED = set(OVR.get("caption_verified", []))


def join_lex(ls, d):
    """join OCR lines; a line-end hyphen is kept when both halves are words and the fused form is not
    (a printed compound such as 'barrel-roofed'), otherwise dropped (a soft hyphenation break)."""
    out = ""
    for l in ls:
        l = l.strip()
        if out.endswith("-") and l[:1].islower():
            left = re.findall(r"[A-Za-z]+$", out[:-1])
            right = re.findall(r"^[A-Za-z]+", l)
            if left and right:
                fused = left[0] + right[0]
                lex = lexicon(d)
                if lex[fold(fused)] < 2 and lex[fold(left[0])] >= 3 and lex[fold(right[0])] >= 3:
                    out = out + l
                    continue
            out = out[:-1] + l
        else:
            out = (out + " " + l).strip()
    return out


def norm(s):
    return re.sub(r"[^a-z0-9]", "", fold(s or ""))


def similarity(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


CREDIT_RE = re.compile(r"\b(Photo(?:graph)?\s*(?:©|\(c\)|:)?.*|After [A-Z][^.;]*|Courtesy [^.;]*)$")


def split_credit(c):
    m = re.search(r"(Photo(?:graph)?\s*:?\s*©.*)$", c)
    return (c[:m.start()].rstrip(), m.group(1)) if m else (c, None)


def clean_caption(text, label):
    t = text
    fixes = []
    for pat, rep in GLYPH_FIXES:
        t2 = re.sub(pat, rep, t)
        if t2 != t:
            fixes.append(rep)
            t = t2
    # the leading figure number as printed (OCR may give "14,1" or "5,1") is the label itself
    if re.fullmatch(r"\d+\.\d+", label or ""):
        t = re.sub(r"^\s*\d{1,2}\s?[.,·]\s?\d{1,2}\b", label, t)
    # a compound split at a line end keeps a stray space ("Maru- Gurjara"); close it up where the second element is
    # capitalised (a proper-name compound), leaving suspended hyphens such as "barrel- or wagon-roofed" alone
    t = re.sub(r"(\w)- (?=[A-Z])", r"\1-", t)
    t = re.sub(r"\bproto- ", "proto-", t)
    return re.sub(r"\s+", " ", t).strip(), fixes


LEX = None


def lexicon(d):
    """word -> count over the book's own text layer plus the project's other Markdown sources (17 MB of English
    prose on Indian architecture, excluding this book's own OCR), to find caption words seen nowhere else."""
    global LEX
    if LEX is None:
        LEX = Counter()
        for p in d:
            for w in re.findall(r"[A-Za-zÀ-ɏ]+", p.get_text()):
                LEX[fold(w)] += 1
        for f in (ROOT.parents[1] / "Udaipur Books Markdown files").glob("*.md"):
            if "Hardy" in f.name:
                continue
            for w in re.findall(r"[A-Za-zÀ-ɏ]+", f.read_text(encoding="utf-8", errors="ignore")):
                LEX[fold(w)] += 1
    return LEX


def known(w, d):
    return lexicon(d)[fold(w)] >= 3


WORD_RE = r"[A-Za-zÀ-ɏ]+"


def repair(text, other, d):
    """Word-level merge of the two readings: where a Tesseract word is unrecognised and the text layer has a
    recognised word in the same aligned slot (equal-length differing run), the text-layer word is taken."""
    if not other:
        return text, []
    a = re.findall(r"\S+", text)
    b = re.findall(r"\S+", other)
    key = lambda w: fold(re.sub(r"[^\w]", "", w))
    sm = difflib.SequenceMatcher(None, [key(w) for w in a], [key(w) for w in b], autojunk=False)
    out, swaps = list(a), []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "replace" or (i2 - i1) != (j2 - j1):
            continue
        for i, j in zip(range(i1, i2), range(j1, j2)):
            wa = re.findall(WORD_RE, a[i])
            wb = re.findall(WORD_RE, b[j])
            if len(wa) == 1 and len(wb) == 1 and not known(wa[0], d) and known(wb[0], d)                     and len(wb[0]) >= 3 and abs(len(wa[0]) - len(wb[0])) <= 1                     and difflib.SequenceMatcher(None, fold(wa[0]), fold(wb[0])).ratio() >= 0.6:
                out[i] = a[i].replace(wa[0], wb[0])
                swaps.append(f"{wa[0]} -> {wb[0]}")
    return " ".join(out), swaps


def odd_words(text, d, other):
    lex = lexicon(d)
    oth = {fold(w) for w in re.findall(r"[A-Za-zÀ-ɏ]+", other or "")}
    out = []
    for w in re.findall(r"[A-Za-zÀ-ɏ]+", text):
        f = fold(w)
        if len(f) >= 3 and lex[f] < 3 and f not in oth:
            out.append(w)
        elif len(f) <= 2 and f not in ("a", "an", "as", "at", "be", "by", "cf", "eg", "ie", "in", "is", "it", "of",
                                        "on", "or", "to", "up", "c", "ad", "bc", "uk", "mp", "up", "ap", "st", "nd",
                                        "rd", "th", "we", "me", "so", "no", "if", "do", "he", "i", "m", "w", "s",
                                        "k", "p", "x", "e", "f", "g", "h", "j", "b", "d", "l", "n", "q", "r", "t",
                                        "u", "v", "y", "z", "o") and lex[f] < 5:
            out.append(w)
    return out


def classify(rgb, paper):
    """photograph vs line drawing, from the pixel distribution inside the crop."""
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    near_paper = (np.abs(g.astype(int) - paper) < 30) & (hsv[..., 1] < 60)
    return "drawing" if near_paper.mean() > 0.55 else "photograph"


def refine_type(base, caption):
    if base != "drawing":
        return base
    c = fold(caption or "")
    if re.search(r"\bground plan|\bplans?\b|roof plan", c) and not re.search(r"elevation|section", c):
        return "plan"
    if "elevation" in c and "plan" not in c:
        return "elevation"
    if re.search(r"\bsections?\b", c) and "plan" not in c:
        return "section"
    if re.search(r"axonometric|reconstruction", c):
        return "drawing (axonometric/reconstruction)"
    return "drawing"


def fig_key(label):
    m = re.fullmatch(r"(\d+)\.(\d+)", label or "")
    if m:
        ch, n = int(m.group(1)), int(m.group(2))
        return "figure", ch, n, f"F{ch:02d}.{n:02d}", f"fig_{ch:02d}_{n:02d}"
    m = re.fullmatch(r"Map (\d+)", label or "")
    if m:
        n = int(m.group(1))
        return "map", None, n, f"MAP{n}", f"map_{n}"
    m = re.fullmatch(r"Part (\d) opener", label or "")
    if m:
        return "unnumbered", None, None, f"U-part{m.group(1)}-opener", f"part{m.group(1)}_opener"
    slug = UNNUMBERED_ID[label]
    return "unnumbered", None, None, f"U-{slug}", slug


def main():
    d = open_pdf()
    ovr, det, caps, figs = plan(d)
    IMG.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    for f in IMG.glob("*.png"):
        f.unlink()
    capd = defaultdict(list)
    for c in caps:
        if c.get("label"):
            capd[c["label"]].append(c)

    problems = [f for f in figs if f["how"] in ("UNMATCHED", "CAPTION WITHOUT PICTURE")]
    figs = [f for f in figs if f["how"] not in ("UNMATCHED", "CAPTION WITHOUT PICTURE")]
    label_pages = defaultdict(list)
    for f in figs:
        label_pages[f["label"]].append(f["page"])

    records, caption_cache, page_cache = [], {}, {}

    def page_img(p):
        if p not in page_cache:
            page_cache.clear()
            page_cache[p] = render(d[p - 1], native_zoom(d[p - 1]))
            small = cv2.resize(page_cache[p], None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(PAGES / f"p{p:03d}.jpg"), cv2.cvtColor(small, cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_JPEG_QUALITY, 85])
        return page_cache[p]

    def caption_for(label):
        if label in caption_cache:
            return caption_cache[label]
        cs = [c for c in capd.get(label, []) if c["kind"] not in ("continuation", "append")]
        apps = [c for c in capd.get(label, []) if c["kind"] == "append"]
        if not cs:
            caption_cache[label] = None
            return None
        c = cs[0]
        p = c["page"]
        z = c["zoom"]
        tl = textlayer_in(d[p - 1], c["bbox_px"], z)
        ts_lines = list(c["ocr_lines"])
        for a in apps:
            tl += textlayer_in(d[a["page"] - 1], a["bbox_px"], a["zoom"])
            ts_lines += a["ocr_lines"]
        tl_text = join_lex(tl, d)
        ts_text = join_lex(ts_lines, d)
        sim = similarity(tl_text, ts_text)
        reasons = []
        if len(cs) > 1:
            reasons.append(f"label {label} found on more than one caption ({[x['page'] for x in cs]})")
        if ts_text:
            text, src = ts_text, "Tesseract 5 (eng, LSTM) on the caption region at the scan's native resolution"
        else:
            text, src = tl_text, "PDF text layer (Internet Archive OCR) inside the caption region"
        if not tl_text:
            reasons.append("caption is not in the PDF text layer; Tesseract reading only (no cross-check)")
        text, fixes = clean_caption(text, label)
        text, swaps = repair(text, tl_text, d)
        text, fixes2 = clean_caption(text, label)
        fixes = list(dict.fromkeys(fixes + fixes2))
        odd = odd_words(text, d, tl_text)
        if odd:
            reasons.append("unrecognised words (not in the book's text layer or the project's reference corpus, "
                           "and not confirmed by the text layer): " + ", ".join(dict.fromkeys(odd)))
        elif tl_text and sim < 0.6:
            reasons.append(f"text layer and Tesseract readings differ widely (similarity {sim:.2f}); "
                           "the Tesseract reading was kept")
        if c["ocr_conf"] < 75:
            reasons.append(f"low Tesseract confidence ({c['ocr_conf']})")
        if c.get("label_source"):
            reasons.append("figure number read by OCR (the text layer missed the caption's first line)")
        if c.get("label_printed_as"):
            reasons.append(f"text layer printed the number as {c['label_printed_as']}; corrected to {label} "
                           "from the page image and the figure sequence")
        hand = []
        if label in OVR.get("caption_text", {}):
            text = OVR["caption_text"][label]
            src = "hand transcription, read against the page image (OCR readings kept alongside)"
            reasons = []
            hand.append("full caption transcribed by hand")
        for old, new in ([] if label in OVR.get("caption_text", {}) else OVR_FIXES.get(label, [])):
            if old in text:
                text = text.replace(old, new)
                hand.append(f"{old} -> {new}")
            else:
                reasons.append(f"hand fix not applied (text not found): {old!r}")
        if hand:
            reasons = [r for r in reasons if not r.startswith("unrecognised words")]
            odd = odd_words(text, d, tl_text)
            if odd:
                reasons.append("unrecognised words remaining after hand check (kept as printed or unresolved): "
                               + ", ".join(dict.fromkeys(odd)))
        if label in OVR_VERIFIED:
            reasons = [r for r in reasons if r.startswith("hand fix not applied")]
        cont = [x for x in capd.get(label, []) if x["kind"] == "continuation"]
        caption_cache[label] = {
            "caption": text, "caption_source": src, "caption_textlayer": tl_text or None,
            "caption_tesseract": ts_text or None, "caption_similarity": round(sim, 3),
            "tesseract_conf": c["ocr_conf"], "caption_page": p, "caption_bbox_px": c["bbox_px"],
            "caption_crop": f"_work/{c['crop']}", "reasons": reasons, "glyph_fixes": fixes or None,
            "word_merges": swaps or None, "hand_fixes": hand or None,
            "hand_verified": label in OVR_VERIFIED or bool(hand),
            "appended_regions": [{"page": a["page"], "crop": f"_work/{a['crop']}"} for a in apps] or None,
            "continuation_lines": {x["page"]: join(x["ocr_lines"]) for x in cont},
        }
        return caption_cache[label]

    for f in sorted(figs, key=lambda f: (f["page"], f["boxes"][0][1] if f["boxes"] else 0)):
        p, label = f["page"], f["label"]
        page = d[p - 1]
        z = native_zoom(page)
        rgb = page_img(p)
        H, W = rgb.shape[:2]
        scheme, ch, num, idpart, stem = fig_key(label)
        multi_page = len(set(label_pages[label])) > 1
        first_page = min(label_pages[label])
        if multi_page and p != first_page:
            idpart += f"-p{p:03d}"
            stem += f"_p{p:03d}"
        pcap = [c["bbox_px"] for c in caps if c["page"] == p]
        cap = caption_for(label)
        boxes = [list(b) for b in f["boxes"]]

        def pad(b):
            q = [max(0, b[0] - PAD), max(0, b[1] - PAD), min(W, b[2] + PAD), min(H, b[3] + PAD)]
            return q if not any(hits(q, c) for c in pcap) else b

        boxes = [pad(b) for b in boxes]
        whole, whole_note = None, None
        if len(boxes) > 1:
            u = union(boxes)
            texty = []
            for x0, y0, x1, y1, s, sz in lines(page):
                lb = [x0 * z, y0 * z, x1 * z, y1 * z]
                if is_texty(s) and (y1 - y0) < 12 and not any(hits(lb, b) for b in boxes):
                    texty.append(lb)
            if any(hits(u, c) for c in pcap) or any(hits(u, t) for t in texty):
                whole_note = ("parts only: a single rectangle around all parts would take in caption or body text, "
                              "so the parts are saved separately")
            else:
                whole = u
        paper = det[str(p)]["paper"]
        subs = f.get("sub") or []
        files = []
        if len(boxes) == 1:
            files.append(("whole", None, boxes[0]))
        else:
            if whole:
                files.append(("whole", None, whole))
            for k, b in enumerate(boxes):
                sl = subs[k] if k < len(subs) else None
                files.append(("part", sl or f"part{k + 1}", b))
        parent = f"{BOOK}-{idpart}"
        for kind, sl, b in files:
            iid = parent if kind == "whole" else f"{parent}-{sl}"
            fn = f"{stem}.png" if kind == "whole" else f"{stem}_{sl}.png"
            crop = rgb[b[1]:b[3], b[0]:b[2]].copy()
            masked = []
            for ml in OVR.get("mask_captions", {}).get(str(p), []):
                for mc in capd.get(ml, []):
                    if mc["page"] == p and hits(mc["bbox_px"], b):
                        m = mc["bbox_px"]
                        ring = rgb[max(0, m[1] - 12):m[3] + 12, max(0, m[0] - 12):m[2] + 12].reshape(-1, 3)
                        crop[max(0, m[1] - b[1]):max(0, m[3] - b[1]), max(0, m[0] - b[0]):max(0, m[2] - b[0])] =                             np.percentile(ring, 75, axis=0).astype(np.uint8)
                        masked.append(ml)
            cv2.imwrite(str(IMG / fn), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
            base = classify(crop, paper)
            caption = cap["caption"] if cap else None
            if scheme == "map":
                itype = "map"
            elif label == "Cover":
                itype = "photograph (book cover)"
            else:
                itype = refine_type(base, caption)
            reasons = list(cap["reasons"]) if cap else ["no caption printed for this image"]
            if label == "Tailpiece":
                reasons = []
            cap_text, credit = split_credit(caption) if caption else (None, None)
            refs = re.findall(r"\b(\d{1,2}\.\d{1,2}[a-z]?)\b", caption or "")
            if scheme == "figure" and refs and refs[0] == label:
                refs = refs[1:]
            notes = []
            if f.get("note"):
                notes.append(f["note"])
            if cap and p in cap["continuation_lines"]:
                notes.append(f"continuation line printed on this page: '{cap['continuation_lines'][p]}'")
            if cap and cap["caption_page"] != p:
                notes.append(f"caption is printed on PDF page {cap['caption_page']} (facing or preceding page)")
            if kind == "whole" and whole_note is None and len(boxes) > 1:
                notes.append(f"whole figure: one rectangle around its {len(boxes)} parts")
            if masked:
                notes.append(f"the caption of {', '.join(masked)} is printed inside this figure's rectangle; that "
                             "area is filled with the page's paper tone in this file (the drawing itself is untouched)")
            if kind == "part" and whole_note:
                notes.append(whole_note)
            rec = {
                "id": iid, "book": BOOK, "file": f"images/{fn}", "kind": kind if len(boxes) > 1 else "whole",
                "parent_id": parent if kind == "part" else None,
                "scheme": scheme, "label": label,
                "label_ref": f"Fig. {label}" if scheme == "figure" else label,
                "chapter": ch, "chapter_title": CHAPTERS.get(ch), "number": num,
                "sub_label": sl if kind == "part" and not str(sl).startswith("part") else None,
                "part_index": int(sl[4:]) if kind == "part" and str(sl).startswith("part") else None,
                "caption": caption, "caption_without_credit": cap_text, "credit": credit,
                "cross_refs": refs or None,
                "caption_source": cap["caption_source"] if cap else None,
                "caption_textlayer": cap["caption_textlayer"] if cap else None,
                "caption_tesseract": cap["caption_tesseract"] if cap else None,
                "caption_similarity": cap["caption_similarity"] if cap else None,
                "glyph_fixes": cap["glyph_fixes"] if cap else None,
                "word_merges_from_textlayer": cap["word_merges"] if cap else None,
                "hand_fixes": cap["hand_fixes"] if cap else None,
                "caption_hand_checked": cap["hand_verified"] if cap else False,
                "caption_continued_from": cap["appended_regions"] if cap else None,
                "page": p, "printed_page": p - FOLIO_OFFSET if p > FOLIO_OFFSET + 9 else None,
                "caption_page": cap["caption_page"] if cap else None,
                "all_pages": sorted(set(label_pages[label])),
                "image_type": itype,
                "extraction": ("page rendered at the scan's native resolution (PyMuPDF; the PDF embeds each page as "
                               "one JPEG-2000 scan, no per-figure images), region cropped, saved as lossless PNG"),
                "region_method": f["how"],
                "pixels": [int(b[2] - b[0]), int(b[3] - b[1])],
                "approx_dpi": round(z * 72),
                "bbox_px": [int(v) for v in b], "rotation": "none",
                "ocr_verify": bool(reasons), "ocr_verify_reasons": reasons or None,
                "page_image": f"_work/pages/p{p:03d}.jpg",
                "caption_crop": cap["caption_crop"] if cap else None,
                "notes": notes or None,
            }
            records.append(rec)

    # caption numbering completeness
    nums = defaultdict(set)
    for c in caps:
        m = re.fullmatch(r"(\d+)\.(\d+)", c.get("label") or "")
        if m and c["kind"] in ("figure",):
            nums[int(m.group(1))].add(int(m.group(2)))
    gaps = {ch: [n for n in range(1, max(v) + 1) if n not in v] for ch, v in nums.items()}
    gaps = {k: v for k, v in gaps.items() if v}
    stored = {r["label"] for r in records}
    no_pic = sorted({c["label"] for c in caps if c.get("label") and c["kind"] == "figure"} - stored,
                    key=lambda s: [int(x) for x in s.split(".")])

    with open(ROOT / "image_manifest.jsonl", "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_index(records)
    write_flags(records, gaps, no_pic, problems)
    write_provenance(d, records)
    t = Counter(r["image_type"] for r in records if r["kind"] == "whole")
    print(len(records), "image files;", len({r["label"] for r in records}), "labels;",
          sum(r["ocr_verify"] for r in records if r["kind"] == "whole"), "whole images flagged")
    print("types (whole images):", dict(t))
    print("numbering gaps:", gaps)
    print("captions with no picture:", no_pic)
    print("unresolved:", [(x["how"], x.get("page") or x.get("caption_page"), x["label"]) for x in problems])


def md(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def write_index(records):
    L = ["# Image index: Adam Hardy, *The Temple Architecture of India* (2007)", "",
         f"{len(records)} image files. Whole figures are listed with their parts indented beneath. Labels are the "
         "author's own (chapter.figure, as printed beside each caption; maps as \"Map N\"). Page = PDF page "
         "(printed page in brackets). ⚑ = caption flagged for checking (see review_flags.md).", ""]
    groups = [("Front matter, maps and part openers", lambda r: r["scheme"] != "figure")]
    L += ["| ID | Label | Ch. | Page | Type | Caption | File |", "|---|---|---|---|---|---|---|"]
    order = sorted(records, key=lambda r: (r["scheme"] == "figure", r["chapter"] or 0, r["number"] or 0, r["page"],
                                           r["kind"] != "whole", r["part_index"] or 0, r["sub_label"] or ""))
    for r in order:
        flag = " ⚑" if r["ocr_verify"] else ""
        pg = f"{r['page']}" + (f" ({r['printed_page']})" if r["printed_page"] else "")
        if r["kind"] == "part":
            L.append(f"| ↳ {r['id']} | {r['label']} {r['sub_label'] or 'part ' + str(r['part_index'])} | "
                     f"{r['chapter'] or ''} | {pg} | {r['image_type']} | | `{r['file']}` |")
        else:
            L.append(f"| {r['id']} | **{r['label']}**{flag} | {r['chapter'] or ''} | {pg} | {r['image_type']} | "
                     f"{md(r['caption'])} | `{r['file']}` |")
    (ROOT / "image_index.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_flags(records, gaps, no_pic, problems):
    L = ["# Review flags", "",
         "Captions marked `ocr_verify`, with both readings, so each can be checked against the page image "
         "(`_work/pages/pNNN.jpg`) or the caption crop (`_work/cap/…png`).", ""]
    seen = set()
    for r in records:
        if not r["ocr_verify"] or r["label"] in seen:
            continue
        seen.add(r["label"])
        L += [f"## {r['label']} (PDF p. {r['caption_page'] or r['page']})", "",
              *[f"- {x}" for x in r["ocr_verify_reasons"]],
              f"- caption stored: {r['caption']}",
              f"- text layer: {r['caption_textlayer']}",
              f"- Tesseract: {r['caption_tesseract']}",
              f"- page image: `{r['page_image']}`; caption crop: `{r['caption_crop']}`", ""]
    L += ["## Numbering gaps (caption numbers never found)", "", json.dumps(gaps) if gaps else "None.", "",
          "## Captions found with no picture paired", "", ", ".join(no_pic) or "None.", "",
          "## Picture regions left unpaired", "",
          "\n".join(f"- {x['how']}: page {x.get('page') or x.get('caption_page')} {x['label'] or ''}"
                    for x in problems) or "None.", ""]
    (ROOT / "review_flags.md").write_text("\n".join(L), encoding="utf-8")


def write_provenance(d, records):
    m = d.metadata
    t = (ROOT / "_tools" / "PROVENANCE_TEMPLATE.md").read_text(encoding="utf-8")
    t = t.format(date=datetime.date.today().isoformat(), pages=d.page_count, n=len(records),
                 pdf=PDF.name, size=round(PDF.stat().st_size / 1e6, 1), creator=m.get("creator"))
    (ROOT / "PROVENANCE.md").write_text(t, encoding="utf-8")


if __name__ == "__main__":
    main()
