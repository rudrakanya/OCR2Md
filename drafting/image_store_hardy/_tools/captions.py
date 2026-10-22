"""Pull every numbered caption (and the four map captions) out of the PDF's text layer, with its box.

A caption opens with its chapter.figure number on a small-set line; its continuation lines share the same left
edge, are set at caption size and follow without a paragraph gap. OCR noise read off a neighbouring picture can
fall between them (oversized "words" such as 'SRE', 'ae Poet'); lines set larger than any caption are skipped and
recorded as dropped, so they can be checked.

  python -I -X utf8 drafting/image_store_hardy/_tools/captions.py   -> _work/captions.json
"""
import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from common import CAP_MAX_H, CAP_RE, MAP_RE, WORK, lines, open_pdf  # noqa: E402

CREDIT_RE = re.compile(r"^(Photo|Photograph|Drawing|Drawn|After|Courtesy|Source|Plan after|Image)\b.*", re.I)
X_TOL = 3.5
GAP = 5.5           # pt between a caption line's foot and the next line's head
NOISE_SZ = 9.6      # OCR noise from pictures tends to come out with large font sizes


def page_captions(page, pno):
    L = sorted(lines(page), key=lambda t: (round(t[1]), t[0]))
    caps = []
    used = set()
    for i, (x0, y0, x1, y1, s, sz) in enumerate(L):
        m = CAP_RE.match(s)
        mm = MAP_RE.search(s) if pno in (10, 11) else None
        if not (m or mm) or (y1 - y0) > CAP_MAX_H + 1.5 or i in used:
            continue
        if m and not (m.group(3)[:1].isupper() or m.group(3)[:1] in "‘'\"“("):
            continue
        if m:
            ch, n = int(m.group(1)), int(m.group(2))
            if not (1 <= ch <= 27):
                continue
            label, kind = f"{ch}.{n}", "figure"
        else:
            ch, n = None, int(mm.group(1))
            label, kind = f"Map {n}", "map"
        body, dropped, box = [s], [], [x0, y0, x1, y1]
        last = y1
        for j in range(i + 1, len(L)):
            a0, b0, a1, b1, t, tsz = L[j]
            if b0 - last > GAP:
                break
            if abs(a0 - x0) > X_TOL:
                continue
            if CAP_RE.match(t) and (b1 - b0) <= CAP_MAX_H + 1.5:
                break
            if kind == "map" and MAP_RE.search(t):
                break
            if tsz > NOISE_SZ or (b1 - b0) > 11:
                dropped.append(t)
                last = b1
                continue
            body.append(t)
            used.add(j)
            box = [min(box[0], a0), min(box[1], b0), max(box[2], a1), max(box[3], b1)]
            last = b1
        credit = [t for t in body[1:] if CREDIT_RE.match(t)]
        if credit:
            k = body.index(credit[0])
            text_lines, credit_lines = body[:k], body[k:]
        else:
            text_lines, credit_lines = body, []
        caps.append({"page": pno, "label": label, "kind": kind, "chapter": ch, "number": n,
                     "lines": text_lines, "credit_lines": credit_lines, "dropped_noise": dropped,
                     "bbox_pt": [round(v, 1) for v in box]})
    return caps


def join(ls):
    out = ""
    for l in ls:
        l = l.strip()
        if out.endswith("-") and l[:1].islower():
            out = out[:-1] + l
        else:
            out = (out + " " + l).strip()
    return out


def main():
    d = open_pdf()
    allc = []
    for i in range(d.page_count):
        for c in page_captions(d[i], i + 1):
            c["caption_textlayer"] = join(c["lines"])
            c["credit"] = join(c["credit_lines"]) or None
            allc.append(c)
    WORK.mkdir(exist_ok=True)
    (WORK / "captions.json").write_text(json.dumps(allc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(allc), "captions")


if __name__ == "__main__":
    main()
