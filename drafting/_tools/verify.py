"""Mechanical verification of extracted items.

For every item in drafting/_runs/<ch>_items.jsonl:
  1. each quote segment (split on ' … ') must occur verbatim in the stored chunk text;
  2. ... and verbatim in the source Markdown file, located at/after the chunk's own position;
  3. the page is the last `<!-- page N -->` marker in force at the quote's offset in the source
     file, cross-checked against the marker in force inside the chunk (chunk page_start if none).
Whitespace runs are matched loosely (a line break in the source may be a space in the quote).
Writes drafting/_runs/<ch>_verified.jsonl and prints failures.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
CORPUS = ROOT / "Udaipur Books Markdown files"
RUNS = ROOT / "drafting" / "_runs"
PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)  # identical to src/chunker.py
ELLIPSIS = " … "


def loose(seg: str) -> re.Pattern:
    parts = [re.escape(p) for p in seg.split()]
    return re.compile(r"\s+".join(parts))


def page_at(text: str, pos: int):
    last = None
    for m in PAGE_RE.finditer(text, 0, pos):
        last = int(m.group(1))
    return last


def locate_chunk(src: str, chunk: str) -> int:
    for line in chunk.splitlines():
        s = line.strip()
        if len(s) > 30 and not PAGE_RE.search(s):
            i = src.find(s)
            if i >= 0:
                return i
    return 0


def verify_item(it, chunk_text, meta, src):
    segs = [s for s in it["q"].split(ELLIPSIS) if s.strip()]
    cpos = 0
    for s in segs:
        m = loose(s).search(chunk_text, cpos)
        if not m:
            return {"ok": False, "why": f"segment not in chunk: {s[:60]!r}"}
        cpos = m.end()
    first_in_chunk = loose(segs[0]).search(chunk_text)
    # page from the chunk alone: marker before the quote inside the chunk, else page_start
    p_chunk = page_at(chunk_text, first_in_chunk.start())
    if p_chunk is None:
        p_chunk = meta.get("page_start")
    if src is None:
        return {"ok": False, "why": "source file missing"}
    anchor = locate_chunk(src, chunk_text)
    pos = anchor
    spans = []
    for s in segs:
        m = loose(s).search(src, pos)
        if not m:
            return {"ok": False, "why": f"segment not in source file after chunk anchor: {s[:60]!r}"}
        spans.append((m.start(), m.end()))
        pos = m.end()
    p_src = page_at(src, spans[0][0])
    p_end = page_at(src, spans[-1][1])
    # The source file is authoritative: chunk text can omit marker lines that the
    # source file has (e.g. blank scan pages), so a differing chunk-derived page is
    # recorded as information, not a failure.
    return {"ok": True, "page": p_src, "page_end": p_end, "page_chunk": p_chunk,
            "src_offset": spans[0][0],
            "why": "" if p_src == p_chunk else f"note: metadata/chunk page {p_chunk}, source-file marker {p_src}"}


def main(ch):
    db = sqlite3.connect(f"file:{ROOT / 'chroma_db' / 'sidecar.sqlite3'}?mode=ro", uri=True)
    sys.path.insert(0, str(ROOT))
    import chromadb
    col = chromadb.PersistentClient(path=str(ROOT / "chroma_db")).get_collection("udaypur_corpus_openai_large")
    items = [json.loads(l) for l in (RUNS / f"{ch}_items.jsonl").open(encoding="utf-8") if l.strip()]
    ids = sorted({i["chunk_id"] for i in items})
    got = col.get(ids=ids, include=["metadatas"])
    metas = dict(zip(got["ids"], got["metadatas"]))
    srcs = {}
    out, fails = [], 0
    for it in items:
        cid = it["chunk_id"]
        text = db.execute("select text from chunks where chunk_id=?", (cid,)).fetchone()[0]
        meta = metas[cid]
        sp = meta["source_path"]
        if sp not in srcs:
            p = CORPUS / sp
            srcs[sp] = p.read_text(encoding="utf-8") if p.exists() else None
        r = verify_item(it, text, meta, srcs[sp])
        rec = dict(it, **{"v_" + k: v for k, v in r.items()}, source_path=sp,
                   book_title=meta.get("book_title"), author=meta.get("author"),
                   book_year=meta.get("book_year"), heading_path=meta.get("heading_path"),
                   language=meta.get("language"), is_duplicate=meta.get("is_duplicate"),
                   duplicate_of=meta.get("duplicate_of"), page_start=meta.get("page_start"))
        out.append(rec)
        if not r["ok"]:
            fails += 1
            print(f"FAIL {cid[:10]} {sp[:40]}: {r['why']}")
    with (RUNS / f"{ch}_verified.jsonl").open("w", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(out)} items, {len(out) - fails} pass, {fails} fail")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1])
