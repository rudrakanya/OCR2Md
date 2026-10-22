"""Footnoted Markdown -> .docx with real Word footnotes (pandoc, private copy in drafting/_tools/vendor).

  python -I "drafting/ch01/make_docx.py" [ch01_draft_v2_footnoted.md] [ch01_draft_v2.docx]

Styling: body Georgia 11 pt, 1.15 line spacing; section headings Heading 2; footnotes 9 pt;
bibliography on its own page. HTML comments (the evidence IDs after each note) are dropped by pandoc.
"""
import re
import subprocess
import sys
from pathlib import Path

D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
sys.path.insert(0, str(D.parent / "_tools" / "vendor"))
import pypandoc  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402

PANDOC = pypandoc.get_pandoc_path()


def reference_docx(path: Path):
    data = subprocess.run([PANDOC, "--print-default-data-file", "reference.docx"], capture_output=True, check=True).stdout
    path.write_bytes(data)
    doc = Document(str(path))
    for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text"):
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        st.font.name = "Georgia"
        st.font.size = Pt(11)
        st.paragraph_format.line_spacing = 1.15
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts")
        if rf is not None:
            for a in ("ascii", "hAnsi", "cs", "eastAsia"):
                rf.set(f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{a}", "Georgia")
    for name in ("Footnote Text", "Footnote Block Text"):
        try:
            st = doc.styles[name]
            st.font.name = "Georgia"
            st.font.size = Pt(9)
            st.paragraph_format.line_spacing = 1.0
        except KeyError:
            pass
    for name in ("Heading 1", "Heading 2", "Title"):
        try:
            doc.styles[name].font.name = "Georgia"
        except KeyError:
            pass
    doc.save(str(path))


def prepare(md: str) -> str:
    # drop the visible "Notes" block heading (pandoc turns [^n]: definitions into real footnotes)
    md = re.sub(r"(?m)^---\s*\n+## Notes\s*\n", "\n", md)
    # bibliography on its own page
    pagebreak = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
    md = re.sub(r"(?m)^## Bibliography\s*$", pagebreak + "## Bibliography", md)
    return md


def main():
    src = D / (sys.argv[1] if len(sys.argv) > 1 else "ch01_draft_v2_footnoted.md")
    dst = D / (sys.argv[2] if len(sys.argv) > 2 else src.name.replace("_footnoted.md", ".docx"))
    ref = D / "_reference_georgia.docx"
    reference_docx(ref)
    md = prepare(src.read_text(encoding="utf-8"))
    tmp = D / "_docx_input.md"
    tmp.write_text(md, encoding="utf-8")
    subprocess.run([PANDOC, str(tmp), "-f", "markdown+footnotes+raw_attribute", "-t", "docx",
                    f"--reference-doc={ref}", "-o", str(dst)], check=True)
    tmp.unlink()
    import zipfile
    fx = zipfile.ZipFile(dst).read("word/footnotes.xml").decode("utf-8")
    n = len([i for i in re.findall(r'<w:footnote [^>]*w:id="(-?\d+)"', fx) if int(i) > 0])
    print(f"wrote {dst.name}: {n} Word footnotes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
