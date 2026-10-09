#!/usr/bin/env python
"""Verify that every book on disk is in the vector KB, with real vectors.

    python kb_inventory.py              # table in the terminal
    python kb_inventory.py --html       # also write kb_inventory.html and open-ready
    python kb_inventory.py --deep       # fetch every embedding, not a sample

Reconciles four things that can silently disagree:

    Udaypur Reference Markdown Files/   the books themselves
    kb_audit/source_registry.yaml       what the project claims to hold
    kb3/kb_active.sqlite                the chunk store Chroma is built from
    kb3/chroma  (udaypur_kb)            the vectors retrieval actually reads

A row is only "ok" when the file exists, the registry names it, the store has
chunks for it, and Chroma holds a usable vector for each distinct passage.

Exit code is 1 if any book is missing, unregistered, or has no vectors — so this
can gate a rebuild.
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import sqlite3
import sys
import unicodedata
from pathlib import Path

import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
CHROMA = ROOT / "kb3" / "chroma"
# The store under inspection is selectable, so a candidate rebuild can be checked
# with exactly these checks rather than this tool only ever being able to confirm
# the store it is about to replace. --store overrides SQLITE / ACTIVE / ARCHIVE.
STORES = {
    "v1": ("kb_active.sqlite", "udaypur_kb", "udaypur_kb_archive"),
    "v2": ("kb_active_v2.sqlite", "udaypur_kb_v2", "udaypur_kb_v2_archive"),
    "v2-openai": ("kb_active_v2.sqlite", "udaypur_kb_v2_openai",
                  "udaypur_kb_v2_openai_archive"),
}
ACTIVE, ARCHIVE = "udaypur_kb", "udaypur_kb_archive"
SAMPLE = 3          # embeddings fetched per source unless --deep


def human(n):
    return f"{n:,}"


def gather(deep=False):
    import chromadb

    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    sources = {s["source_id"]: s for s in reg["sources"]}
    by_file = {s.get("file"): sid for sid, s in sources.items()}

    on_disk = {}
    if BOOKS.is_dir():
        for p in sorted(BOOKS.glob("*.md")):
            on_disk[p.name] = p.stat().st_size

    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    rows = dict(db.execute("select parent_source_id, count(*) from chunks group by 1"))
    uniq = dict(db.execute(
        "select parent_source_id, count(distinct content_hash) from chunks group by 1"))

    client = chromadb.PersistentClient(path=str(CHROMA))
    names = [c.name for c in client.list_collections()]
    act = client.get_collection(ACTIVE)
    got = act.get(limit=500000, include=["metadatas"])
    chroma_n = collections.Counter(m["parent_source_id"] for m in got["metadatas"])
    archived_n = collections.Counter(m["parent_source_id"] for m in got["metadatas"]
                                     if m.get("is_archived"))
    quotable_n = collections.Counter(m["parent_source_id"] for m in got["metadatas"]
                                     if m.get("is_quotable"))
    pages_n = collections.Counter(m["parent_source_id"] for m in got["metadatas"]
                                  if m.get("page") not in (None, "", -1, "-1"))
    buckets = collections.defaultdict(set)
    for m in got["metadatas"]:
        for k, v in m.items():
            if k.startswith("in_") and v:
                buckets[m["parent_source_id"]].add(k[3:])

    # do the vectors actually exist, and are they usable?
    vec = {}
    for sid in sources:
        ids = [i for i, m in zip(got["ids"], got["metadatas"]) if m["parent_source_id"] == sid]
        if not ids:
            vec[sid] = {"checked": 0, "dim": None, "degenerate": 0}
            continue
        pick = ids if deep else ids[:: max(1, len(ids) // SAMPLE)][:SAMPLE]
        emb = act.get(ids=pick, include=["embeddings"])["embeddings"]
        arr = [np.asarray(e, dtype=np.float32) for e in emb if e is not None]
        dims = {a.shape[0] for a in arr}
        bad = sum(1 for a in arr if not np.isfinite(a).all() or float(np.abs(a).sum()) == 0.0)
        vec[sid] = {"checked": len(arr),
                    "dim": (dims.pop() if len(dims) == 1 else sorted(dims)) if arr else None,
                    "degenerate": bad}

    report = []
    for sid, s in sources.items():
        fname = s.get("file")
        size = on_disk.get(fname)
        r = {
            "code": s.get("code", "?"), "source_id": sid, "file": fname,
            "title": s.get("title", "?"), "language": s.get("language", "?"),
            "source_type": s.get("source_type", "?"),
            "kb_rows": rows.get(sid, 0), "distinct": uniq.get(sid, 0),
            "vectors": chroma_n.get(sid, 0), "archived": archived_n.get(sid, 0),
            "quotable": quotable_n.get(sid, 0), "with_page": pages_n.get(sid, 0),
            "chapters": sorted(buckets.get(sid, ()), key=lambda c: (len(c), c)),
            "file_kb": round(size / 1024) if size else 0,
            "vec": vec[sid],
        }
        problems = []
        # A registration merged into another work (Phase 4 Step 3 folded the three
        # Patil registrations into one) is SUPPOSED to hold no chunks of its own.
        # Without this it reports as "no chunks / NO VECTORS", which reads as a
        # broken store when it is the intended outcome of the merge.
        merged = s.get("merged_into")
        if merged:
            r["note"] = f"merged into {merged} — its chunks live there by design"
            r["problems"] = []
            r["ok"] = True
            r["merged_into"] = merged
            report.append(r)
            continue
        if fname not in on_disk:
            problems.append("file missing from the books folder")
        if not r["kb_rows"]:
            problems.append("no chunks in kb_active.sqlite")
        if not r["vectors"]:
            problems.append("NO VECTORS in Chroma")
        elif r["vectors"] != r["distinct"]:
            problems.append(f"{r['distinct'] - r['vectors']} distinct passages without a vector")
        if r["vec"]["degenerate"]:
            problems.append(f"{r['vec']['degenerate']} zero/NaN vector(s) sampled")
        if r["vectors"] and r["kb_rows"] > r["distinct"]:
            r["note"] = (f"{r['kb_rows'] - r['distinct']} duplicate passage(s) collapsed to one "
                         "vector each — by design")
        r["problems"] = problems
        r["ok"] = not problems
        report.append(r)

    report.sort(key=lambda r: r["code"])
    extras = {k: v for k, v in chroma_n.items() if k not in sources}
    unregistered = sorted(set(on_disk) - set(by_file))
    return {
        "report": report,
        "collections": names,
        "active_total": act.count(),
        "archive_total": client.get_collection(ARCHIVE).count() if ARCHIVE in names else 0,
        "files_on_disk": len(on_disk),
        "unregistered_files": unregistered,
        "chroma_extras": extras,
        "deep": deep,
    }


def print_table(d):
    print(f"books folder : {BOOKS.name} — {d['files_on_disk']} .md files")
    print(f"collections  : {', '.join(d['collections'])}")
    print(f"vectors      : {human(d['active_total'])} active, {human(d['archive_total'])} archived")
    print()
    w = f"{'code':9s} {'book':44s} {'rows':>6s} {'uniq':>6s} {'vectors':>8s} {'dim':>5s} {'chapters':>9s}  status"
    print(w)
    print("-" * len(w))
    for r in d["report"]:
        dim = r["vec"]["dim"]
        dim = str(dim) if isinstance(dim, int) else ("—" if dim is None else "MIXED")
        status = "ok" if r["ok"] else "; ".join(r["problems"])
        print(f"{r['code']:9s} {r['title'][:44]:44s} {r['kb_rows']:6d} {r['distinct']:6d} "
              f"{r['vectors']:8d} {dim:>5s} {len(r['chapters']):9d}  {status}")
    bad = [r for r in d["report"] if not r["ok"]]
    deduped = [r for r in d["report"] if r.get("note")]
    print()
    if deduped:
        print("De-duplicated (not an error):")
        for r in deduped:
            print(f"  {r['code']:9s} {r['note']}")
        print()
    if d["unregistered_files"]:
        print("Files in the folder with no registry entry:")
        for f in d["unregistered_files"]:
            print("  " + f)
        print()
    if d["chroma_extras"]:
        print("In Chroma but not in the registry:")
        for k, v in d["chroma_extras"].items():
            print(f"  {k}: {v} chunk(s)")
        print()
    print(f"{len(d['report']) - len(bad)} of {len(d['report'])} books fully verified"
          + (f" — {len(bad)} with problems" if bad else ""))
    return 1 if bad or d["unregistered_files"] else 0


CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1b;--mut:#6b6b68;--line:#e3e3df;--ok:#15803d;--bad:#b91c1c;
--warn:#a16207;--card:#fff;--accent:#1f3864}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17171a;--fg:#e9e9e6;
--mut:#a0a09c;--line:#2e2e33;--card:#1f1f23;--ok:#4ade80;--bad:#f87171;--warn:#fbbf24;
--accent:#9db4e0}}
:root[data-theme=dark]{--bg:#17171a;--fg:#e9e9e6;--mut:#a0a09c;--line:#2e2e33;--card:#1f1f23;
--ok:#4ade80;--bad:#f87171;--warn:#fbbf24;--accent:#9db4e0}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,Roboto,
Helvetica,Arial,sans-serif;padding:24px 16px 64px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--mut);font-size:13px;margin-bottom:20px}
.cards{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;
min-width:120px}
.card b{display:block;font-size:20px}
.card span{color:var(--mut);font-size:12px}
input[type=search]{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:8px;
background:var(--card);color:var(--fg);font-size:14px;margin-bottom:12px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);
border-radius:10px;overflow:hidden;font-size:13px}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:rgba(127,127,127,.08);font-weight:600;cursor:pointer;white-space:nowrap}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}
code{font:12px/1.4 ui-monospace,Consolas,monospace;color:var(--accent)}
.ok{color:var(--ok);font-weight:600}
.bad{color:var(--bad);font-weight:600}
.note{color:var(--warn);font-size:12px}
.chips{color:var(--mut);font-size:11px}
footer{margin-top:22px;color:var(--mut);font-size:12px}
@media(max-width:720px){th:nth-child(4),td:nth-child(4),th:nth-child(7),td:nth-child(7){display:none}}
"""

JS = """
const q=document.getElementById('q'),rows=[...document.querySelectorAll('tbody tr')];
q.addEventListener('input',()=>{const t=q.value.toLowerCase();
rows.forEach(r=>r.style.display=r.innerText.toLowerCase().includes(t)?'':'none')});
document.querySelectorAll('th').forEach((th,i)=>th.addEventListener('click',()=>{
const tb=th.closest('table').querySelector('tbody');
const num=th.classList.contains('n');const dir=th.dataset.d==='1'?-1:1;th.dataset.d=dir===1?'1':'';
[...tb.rows].sort((a,b)=>{const x=a.cells[i].innerText.trim(),y=b.cells[i].innerText.trim();
return dir*(num?(parseFloat(x.replace(/,/g,''))||0)-(parseFloat(y.replace(/,/g,''))||0)
:x.localeCompare(y))}).forEach(r=>tb.appendChild(r))}));
"""


def write_html(d, path):
    rep = d["report"]
    ok = sum(1 for r in rep if r["ok"])
    rows_html = []
    for r in rep:
        dim = r["vec"]["dim"]
        dim = str(dim) if isinstance(dim, int) else ("—" if dim is None else "mixed")
        status = ('<span class="ok">verified</span>' if r["ok"]
                  else '<span class="bad">' + html.escape("; ".join(r["problems"])) + "</span>")
        note = f'<div class="note">{html.escape(r["note"])}</div>' if r.get("note") else ""
        chips = (f'<div class="chips">{len(r["chapters"])} chapters: '
                 f'{html.escape(", ".join(r["chapters"]))}</div>' if r["chapters"] else "")
        rows_html.append(
            "<tr>"
            f'<td><code>{html.escape(r["code"])}</code></td>'
            f'<td>{html.escape(r["title"])}<div class="chips">{html.escape(r["file"] or "—")}'
            f' · {html.escape(r["language"])} · {html.escape(r["source_type"])}</div>{chips}</td>'
            f'<td class="n">{r["kb_rows"]:,}</td>'
            f'<td class="n">{r["distinct"]:,}</td>'
            f'<td class="n">{r["vectors"]:,}</td>'
            f'<td class="n">{dim}</td>'
            f'<td class="n">{r["quotable"]:,}</td>'
            f"<td>{status}{note}</td></tr>")

    extra = ""
    if d["chroma_extras"]:
        items = "".join(f"<li><code>{html.escape(k)}</code> — {v} chunk(s)</li>"
                        for k, v in d["chroma_extras"].items())
        extra += f"<p>In Chroma but not in the registry:<ul>{items}</ul></p>"
    if d["unregistered_files"]:
        items = "".join(f"<li>{html.escape(f)}</li>" for f in d["unregistered_files"])
        extra += f"<p>Files with no registry entry:<ul>{items}</ul></p>"

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KB inventory</title><style>{CSS}</style></head><body><div class="wrap">
<h1>Vector knowledge base — book inventory</h1>
<div class="sub">{html.escape(str(BOOKS.name))} reconciled against the registry,
kb_active.sqlite and the Chroma collection.
{'Every embedding checked.' if d['deep'] else f'Embeddings sampled ({SAMPLE} per book).'}
Click a column to sort; type to filter.</div>
<div class="cards">
<div class="card"><b>{ok}/{len(rep)}</b><span>books verified</span></div>
<div class="card"><b>{d['files_on_disk']}</b><span>.md files on disk</span></div>
<div class="card"><b>{d['active_total']:,}</b><span>active vectors</span></div>
<div class="card"><b>{d['archive_total']:,}</b><span>archived vectors</span></div>
<div class="card"><b>{sum(r['vectors'] for r in rep):,}</b><span>vectors from these books</span></div>
</div>
<input id="q" type="search" placeholder="filter by code, title, file, chapter or status…">
<table><thead><tr>
<th>code</th><th>book</th><th class="n">rows</th><th class="n">distinct</th>
<th class="n">vectors</th><th class="n">dim</th><th class="n">quotable</th><th>status</th>
</tr></thead><tbody>{''.join(rows_html)}</tbody></table>
{extra}
<footer>rows = chunks in kb_active.sqlite · distinct = unique passages (one vector each) ·
vectors = rows in the Chroma collection · dim = embedding dimension.
A book is verified when the file exists, the registry names it, the store has chunks and Chroma
holds a vector for every distinct passage. Regenerate with
<code>python kb_inventory.py --html</code>.</footer>
</div><script>{JS}</script></body></html>"""
    path.write_text(unicodedata.normalize("NFC", doc), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--html", action="store_true", help="also write kb_inventory.html")
    ap.add_argument("--json", action="store_true", help="also write kb_inventory.json")
    ap.add_argument("--deep", action="store_true", help="fetch every embedding, not a sample")
    from kb_target import active as _kb_active
    ap.add_argument("--store", choices=sorted(STORES), default=_kb_active(),
                    help="which store to verify (default: the live one, per kb_target)")
    n = ap.parse_args()

    global SQLITE, ACTIVE, ARCHIVE
    _sq, ACTIVE, ARCHIVE = STORES[n.store]
    SQLITE = ROOT / "kb3" / _sq
    print(f"store: {n.store}   sqlite={SQLITE.name}   collection={ACTIVE}\n")

    d = gather(deep=n.deep)
    code = print_table(d)
    if n.html:
        p = ROOT / "kb_inventory.html"
        write_html(d, p)
        print(f"\nwrote {p}  — open it in a browser")
    if n.json:
        p = ROOT / "kb_inventory.json"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {p}")
    return code


if __name__ == "__main__":
    sys.exit(main())
