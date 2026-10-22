"""Tesseract 5 (`Latin` and `eng`, tessdata_best) TSV with word boxes for each illustrated page photo
-> _work/tsv/pNNN.{Latin,eng}.tsv. Free, local; runs pages in parallel."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = ROOT.parents[1] / "drafting" / "image_store" / "_tools" / "tessdata"


def run(n, lang):
    out = ROOT / "_work" / "tsv" / f"p{n:03d}.{lang}"
    if (out.with_suffix(f".{lang}.tsv")).exists() or Path(str(out) + ".tsv").exists():
        return
    subprocess.run([TESS, str(ROOT / "_work" / "pages" / f"p{n:03d}.png"), str(out), "--tessdata-dir", str(TESSDATA),
                    "-l", lang, "--psm", "3", "tsv"], capture_output=True)


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda t: run(*t), [(n, l) for n in range(a, b + 1) for l in ("Latin", "eng")]))
