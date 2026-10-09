#!/usr/bin/env python3
"""Stage 1: turn each source photograph into a page image fit for a book PDF.

Source files are opened read-only and never written back; every result is a new
file under the derivatives directory. Per page the steps are:

    EXIF rotation -> measured rotation (for photos with no EXIF flag)
    -> crop to the page -> deskew -> trim the facing-page strip
    -> cap the long edge -> JPEG

Each page's outcome is recorded so the manifest can show exactly what was done
and which pages need a human eye.
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from recon.rectify import rectify, deskew          # noqa: E402
from recon.gutter import find_gutter               # noqa: E402

MAX_EDGE = 2800        # plenty for reading 10pt type; keeps the PDF sane
JPEG_QUALITY = 88
Image.MAX_IMAGE_PIXELS = None


def process(job):
    src, dst, rotate = Path(job["src"]), Path(job["dst"]), job.get("rotate")
    rec = {"source": str(src), "derivative": str(dst)}
    try:
        im = Image.open(src)
        rec["source_size"] = list(im.size)
        rec["exif_orientation"] = im.getexif().get(0x0112, 1)
        im = ImageOps.exif_transpose(im)
        if rotate == "cw":
            im = im.transpose(Image.ROTATE_270)
        elif rotate == "ccw":
            im = im.transpose(Image.ROTATE_90)
        rec["applied_rotation"] = rotate or "exif-only"

        cropped, method, note = rectify(im)
        rec["crop_method"], rec["crop_note"] = method, note

        straight, angle = deskew(cropped)
        rec["deskew_deg"] = round(angle, 2)

        left, right, gnote = find_gutter(straight)
        page = straight.crop((left, 0, right, straight.height))
        rec["gutter"] = gnote

        if max(page.size) > MAX_EDGE:
            page.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        rec["page_size"] = list(page.size)
        rec["area_kept"] = round((page.width * page.height) /
                                 float(im.width * im.height), 3)
        dst.parent.mkdir(parents=True, exist_ok=True)
        page.convert("RGB").save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True,
                                 progressive=True)
        rec["bytes"] = dst.stat().st_size
        rec["status"] = "ok"
    except Exception as e:                           # noqa: BLE001 - one bad page must not stop the book
        rec["status"] = f"error:{type(e).__name__}"
        rec["error"] = str(e)[:300]
    return rec


def main():
    jobs = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(process, jobs, chunksize=4))
    out.write_text(json.dumps(results, indent=1))
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"derivatives: {ok}/{len(results)} ok -> {out}")
    for r in results:
        if r["status"] != "ok":
            print("  FAILED:", r["source"], r["status"], r.get("error", ""))


if __name__ == "__main__":
    main()
