#!/usr/bin/env python3
"""Settle the rotation of the photographs that carry no EXIF flag.

Scoring a candidate rotation purely on "how much confident text came out" is
weak: a page read upside down still yields text, and on these photographs the
two candidates sometimes came within 1% of each other.

There is a better witness. Every page already has a transcript from the Mistral
OCR pass, which handled rotation itself, so it says what words are ON the page
regardless of which way up it was photographed. The rotation whose local OCR
reproduces those words is the right way up; the wrong one yields words that
match nothing. Pages with no text at all (full-page plates) cannot be settled
this way and are reported as undecided for a human to confirm.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from rapidocr_onnxruntime import RapidOCR

THUMB = 1300
WORD = re.compile(r"[a-z]{4,}")


def words(text):
    return set(WORD.findall(text.lower()))


def read(ocr, img):
    res, _ = ocr(np.array(img))
    if not res:
        return set(), 0.0
    text = " ".join(t for _, t, _ in res)
    conf = sum(float(c) * len(t) for _, t, c in res)
    return words(text), conf


def main():
    targets = json.loads(Path(sys.argv[1]).read_text())
    truth_dir = Path(sys.argv[2])
    ocr = RapidOCR()
    out = {}
    for i, path in enumerate(targets, 1):
        stem = Path(path).stem
        truth = words(re.sub(r"^<!--.*?-->", "", (truth_dir / f"{stem}.md").read_text(encoding="utf-8"), flags=re.S))
        im = ImageOps.exif_transpose(Image.open(path))
        im.thumbnail((THUMB, THUMB))
        rec = {}
        for tag, rotated in (("cw", im.transpose(Image.ROTATE_270)),
                             ("ccw", im.transpose(Image.ROTATE_90))):
            w, conf = read(ocr, rotated)
            rec[f"match_{tag}"] = len(w & truth)
            rec[f"conf_{tag}"] = round(conf, 1)
        m_cw, m_ccw = rec["match_cw"], rec["match_ccw"]
        if max(m_cw, m_ccw) >= 4 and m_cw != m_ccw:
            rec["rotate"] = "cw" if m_cw > m_ccw else "ccw"
            rec["basis"] = "transcript match"
            rec["confidence"] = round(abs(m_cw - m_ccw) / max(m_cw, m_ccw), 2)
        elif max(rec["conf_cw"], rec["conf_ccw"]) > 0:
            rec["rotate"] = "cw" if rec["conf_cw"] >= rec["conf_ccw"] else "ccw"
            rec["basis"] = "confidence only"
            rec["confidence"] = 0.0
        else:
            rec["rotate"] = None
            rec["basis"] = "undecided (no text found)"
            rec["confidence"] = 0.0
        out[stem] = rec
        print(f"[{i}/{len(targets)}] {stem}: {rec['rotate']} via {rec['basis']} "
              f"(match cw={m_cw} ccw={m_ccw})", flush=True)
    Path(sys.argv[3]).write_text(json.dumps(out, indent=1))
    print("written:", sys.argv[3])


if __name__ == "__main__":
    main()
