"""One command for the rendering (user brief, 2026-10-15).

  python -I build_outputs.py [--chapters 4]   (--chapters N: that chapter only, no combined document)
  python -I build_outputs.py            per chapter: footnote.py (consolidated Chicago notes, hidden IDs) + make_docx.py;
                                        then the combined "Udaypur - Chapters 1-3 - Draft.docx" (each chapter on a new page,
                                        footnotes restarting in each chapter, one bibliography with each book once) and a
                                        metrics/summary skeleton at drafting/run/summary_data.json
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
DR = HERE.parent
CFGS = {1: DR / "ch01" / "cfg_ch01v6.py", 2: DR / "ch02" / "cfg_ch02v4.py", 3: DR / "ch03" / "cfg_ch03v4.py"}
MORE_CFGS = {4: DR / "ch04" / "cfg_ch04v3.py", 5: DR / "ch05" / "cfg_ch05v1.py", 6: DR / "ch06" / "cfg_ch06v3.py", 7: DR / "ch07" / "cfg_ch07v1.py", 8: DR / "ch08" / "cfg_ch08v1.py", 9: DR / "ch09" / "cfg_ch09v1.py", 10: DR / "ch10" / "cfg_ch10v1.py", 11: DR / "ch11" / "cfg_ch11v1.py", 12: DR / "ch12" / "cfg_ch12v1.py", 13: DR / "ch13" / "cfg_ch13v1.py"}   # built only with --chapters N (no combined document)
PY = sys.executable
COMBINED = DR / "Udaypur - Chapters 1-3 - Draft.docx"
GDOCS_LIMIT = 1_020_000          # Google Docs: about 1.02 million characters per document


def load_cfg(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"cfg_{path.stem}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def per_chapter(only=None):
    out = {}
    allc = {**CFGS, **MORE_CFGS}
    for ch, cfg in allc.items():
        if (only and ch not in only) or (not only and ch not in CFGS):
            continue
        env = dict(os.environ, UDAY_CFG=str(cfg), PYTHONIOENCODING="utf-8")
        C = load_cfg(cfg)
        fn = C.OUT.with_name(C.OUT.stem + "_footnoted.md")
        r1 = subprocess.run([PY, "-I", str(HERE / "footnote.py"), str(C.OUT), str(fn)], env=env, capture_output=True, text=True, encoding="utf-8")
        r2 = subprocess.run([PY, "-I", str(HERE / "make_docx.py"), str(fn), str(C.D / C.DOCX_NAME)], env=env, capture_output=True, text=True, encoding="utf-8")
        out[ch] = {"footnote": (r1.stdout + r1.stderr).strip()[-300:], "docx": (r2.stdout + r2.stderr).strip()[-300:], "footnoted": str(fn), "docx_path": str(C.D / C.DOCX_NAME)}
        print(f"ch{ch}: {out[ch]['footnote']} | {out[ch]['docx']}")
    return out


def combined():
    os.environ["UDAY_CFG"] = str(CFGS[1])
    sys.path.insert(0, str(HERE))
    import make_docx as mk
    parts, bib = [], []
    sect = ('\n```{=openxml}\n<w:p><w:pPr><w:sectPr><w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr>'
            '<w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
            '</w:sectPr></w:pPr></w:p>\n```\n\n')
    for ch, cfg in CFGS.items():
        C = load_cfg(cfg)
        md = C.OUT.with_name(C.OUT.stem + "_footnoted.md").read_text(encoding="utf-8")
        md = re.sub(r"\[\^(\d+)\]", lambda m: f"[^c{ch}n{m.group(1)}]", md)          # unique labels; Word restarts numbering per section
        md = re.sub(r"(?m)^---\s*\n+## Notes\s*\n", "\n", md)
        md = re.sub(r"\s*<!--\s*(C\d\d-[^>]*?)\s*-->", lambda m: " [" + m.group(1).strip() + ']{custom-style="Evidence ID"}', md)
        md = re.sub(r"(?m)^## (\d+\.\d+ .*)$", r"# \1", md)
        head, _, b = md.partition("\n## Bibliography\n")
        bib += [e.strip() for e in b.strip().split("\n\n") if e.strip()]
        title = (f'::: {{custom-style="Chapter Label"}}\nCHAPTER {ch}\n:::\n\n::: {{custom-style="Title"}}\n{C.TITLE}\n:::\n\n'
                 f'::: {{custom-style="Subtitle"}}\n{getattr(C, "SUBTITLE", "Draft · October 2026")}\n:::\n\n')
        parts.append(title + head.rstrip() + "\n")
    seen, uniq = set(), []
    for e in bib:
        k = re.sub(r"\W+", "", e.lower())
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    uniq.sort(key=lambda e: re.sub(r"[^\w ]", "", e).lower())
    md = sect.join(parts) + sect + "# Bibliography\n\n" + "\n\n".join(f'::: {{custom-style="Bibliography Entry"}}\n{e}\n:::' for e in uniq) + "\n"
    tmp = DR / "run" / "_combined_input.md"
    tmp.write_text(md, encoding="utf-8")
    subprocess.run([mk.PANDOC, str(tmp), "-f", "markdown+footnotes+raw_attribute+fenced_divs+bracketed_spans", "-t", "docx", "-o", str(COMBINED)], check=True)
    mk.finish(COMBINED)
    # the final section too restarts its footnotes
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    doc = Document(str(COMBINED))
    for sp in doc.element.body.iter(qn("w:sectPr")):
        if sp.find(qn("w:footnotePr")) is None:
            fp = OxmlElement("w:footnotePr")
            nr = OxmlElement("w:numRestart")
            nr.set(qn("w:val"), "eachSect")
            fp.append(nr)
            sp.insert(0, fp)
    doc.save(str(COMBINED))
    z = zipfile.ZipFile(COMBINED)
    body = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    notes = re.sub(r"<[^>]+>", "", z.read("word/footnotes.xml").decode("utf-8"))
    nfn = len([i for i in re.findall(r'<w:footnote [^>]*w:id="(-?\d+)"', z.read("word/footnotes.xml").decode("utf-8")) if int(i) > 0])
    chars = len(body) + len(notes)
    info = {"path": str(COMBINED), "footnotes": nfn, "bibliography_entries": len(uniq), "characters": chars,
            "google_docs_limit": GDOCS_LIMIT, "share_of_limit": round(chars / GDOCS_LIMIT, 3)}
    print(json.dumps(info, indent=1))
    return info


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    only = [int(x) for x in sys.argv[sys.argv.index("--chapters") + 1].split(",")] if "--chapters" in sys.argv else None
    res = {"chapters": per_chapter(only) if "--combined-only" not in sys.argv else {}}
    if not only:
        res["combined"] = combined()
    (DR / "run" / "outputs.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
