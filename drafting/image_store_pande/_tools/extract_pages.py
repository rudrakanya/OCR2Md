"""Extract each page's native camera photo (JPEG XObject), decode once, rotate upright by the page's
placement matrix (exact 90-degree pixel rotation), save as lossless PNG in _work/pages/pNNN.png."""
import io, sys
from pathlib import Path
import pymupdf
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
PDF = HERE.parents[1] / "PDF Originals" / "The Udayesvara Temple - Anupa Pande (scanned).pdf"


def main():
    d = pymupdf.open(PDF)
    out = HERE / "_work" / "pages"
    out.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(d):
        f = out / f"p{i + 1:03d}.png"
        if f.exists():
            continue
        (xref, *_), = p.get_images(full=True)
        a, b, c, dd, e, ff = p.get_image_info(xrefs=True)[0]["transform"]
        im = Image.open(io.BytesIO(d.extract_image(xref)["image"]))
        im.load()
        # image unit square -> page: x' = a*u + c*v + e, y' = b*u + d*v + f  (PDF y up; page shown y down)
        # (0,832,-624,0,...): u runs up the page, v runs left -> rotate the pixels 90 degrees clockwise
        if (a, dd) == (0, 0) and b > 0 and c < 0:
            im = im.transpose(Image.Transpose.ROTATE_270)
        elif (a, dd) == (0, 0) and b < 0 and c > 0:
            im = im.transpose(Image.Transpose.ROTATE_90)
        elif a < 0 and dd < 0:
            im = im.transpose(Image.Transpose.ROTATE_180)
        im.save(f, optimize=False, compress_level=3)
        print(i + 1, im.size, flush=True)


if __name__ == "__main__":
    main()
