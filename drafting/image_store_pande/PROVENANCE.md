# Provenance

- **Source PDF:** `PDF Originals/The Udayesvara Temple - Anupa Pande (scanned).pdf` (199 pages, 519 MB). Each page is
  one phone photograph of the open book (JPEG, 4624 × 3468 px, placed rotated 90°) with an invisible OCR text layer
  (Tesseract `eng`, added when the PDF was assembled locally from the photographs).
- **Book:** Anupa Pande, *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta*. The
  photographed copy is from the Archaeological Survey of India, Bhopal Circle Library (books_manifest.yaml); no
  year is stated in the copy.
- **Coverage:** front matter from the List of Illustrations onwards and book pp. 1–197. Four openings were not
  photographed: book pp. 8-9, 34-35, 58-59, 82-83, so Pl. 7, 43, 83, 116 and 117 are listed but have no image.
- **Stable ID:** `PANDE-UDT-FIG01`, `PANDE-UDT-PL001` … `PANDE-UDT-PL130`.
- **Extracted:** 2026-10-22, locally, no paid API: PyMuPDF (page photos pulled as stored, decoded once, turned upright
  by an exact 90° pixel rotation), OpenCV/NumPy (picture detection, edge snapping), Pillow (lossless PNG),
  Tesseract 5 (`Latin` and `eng`, tessdata_best) for caption anchors and cross-readings.
- **Resolution:** the photos have no scan dpi. The printed text block (about 6 in wide) spans roughly 2,600–2,900 px,
  so the effective resolution is about 430–480 px per inch, varying page to page with camera distance and tilt.
- **Files:** `plates/` holds the bounding-box crop of each picture from the decoded photo (not resampled; because
  the page was photographed at an angle, the crop is not rectangular to the print and carries slivers of paper at
  the corners). `rectified/` holds the same picture perspective-corrected to a rectangle (Lanczos resampling at the
  picture's own pixel size), the better copy for viewing and publication.
- **Captions:** `caption` is the List of Illustrations, transcribed by eye; on-page captions are checked against it
  (OCR, and by eye wherever OCR disagreed). See review_flags.md.
