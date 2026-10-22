"""Book ledger (user brief, 2026-10-15): what the reader has been told, where, across Chapters 1–3.

  set UDAY_CFG=<cfg>; python -I ledger.py build            one structured-extraction call over this chapter's plan (medium)
                                                           + a parser pass → drafting/run/ledger/ledger_chN.json
  python -I ledger.py merge                                → drafting/editorial/book_ledger.json + book_ledger.md
  python -I ledger.py digest <section>                     what the reader already knows, what must not be contradicted,
                                                           which questions this section may advance
  python -I ledger.py check <section> <text.md>            second glosses, re-introduced full names, conflicting figures
  set UDAY_CFG=<cfg>; python -I ledger.py update <draft>   one extraction over the chapter's final text (actual first mentions)

Section order is numeric (1.1 < 1.5 < 2.1 < 3.5). Nothing here is evidence: the ledger records what the PLANS assign, so
the digest can tell a writer what earlier sections will already have said when the chapters run in parallel.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
DR = HERE.parent
LD = DR / "run" / "ledger"
BOOK_JSON = DR / "editorial" / "book_ledger.json"
BOOK_MD = DR / "editorial" / "book_ledger.md"

EXTRACT_SYS = """You build a continuity ledger for a history book from ONE chapter's plan (or final text). Extract ONLY what the text states; never add knowledge.
Return ONLY JSON:
{"people": [{"name": "short form used after first mention", "full_name": "full form for the first mention", "first_section": "N.N", "role": "≤ 12 words"}],
 "terms": [{"term": "Indic or technical term as spelled", "gloss": "≤ 8 words", "first_section": "N.N"}],
 "places": [{"name": "...", "first_section": "N.N", "note": "≤ 12 words"}],
 "figures": [{"what": "the measured or dated thing", "value": "the committed value or range as written", "keyword": "one word that identifies it in prose", "sections": ["N.N"]}],
 "open_questions": [{"question": "...", "sections": ["N.N"], "status": "left open / weighed / answered"}],
 "forward_refs": [{"from": "N.N", "to": "chapter or section", "what": "..."}],
 "motifs": [{"motif": "...", "sections": ["N.N"]}]}
first_section = the first section of THIS text in which it appears. Include every named person, every italicised or Indic term, every place that matters to the argument, every committed figure (distances, heights, dates, counts), every question the text leaves open."""


def key(sec):
    a, b = sec.split(".")
    return (int(a), int(b))


def build(dry=False):
    sys.path.insert(0, str(HERE))
    from cfg import C
    import run as rn
    plan = Path(C.OUTLINE).read_text(encoding="utf-8")
    R = rn.Run(dry)
    out = R.call(f"ledger_build_ch{C.CH}", 0, "edit", EXTRACT_SYS, f"CHAPTER {C.CH} PLAN:\n\n{plan}", 2500, effort="medium")
    j = rn.parse_json(out) if out else None
    if dry:
        return
    j = j or {}
    j["chapter"] = C.CH
    j["sections"] = {m.group(1): m.group(2).strip() for m in re.finditer(r"(?m)^## (\d+\.\d+) (.+?)(?: \*\(.*)?$", plan)}
    j["through_line"] = (re.search(r"\*\*Through-line\.\*\*\s*(.+)", plan) or [None, ""])[1].strip()
    LD.mkdir(parents=True, exist_ok=True)
    (LD / f"ledger_ch{C.CH}.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ledger ch{C.CH}: " + ", ".join(f"{k} {len(v)}" for k, v in j.items() if isinstance(v, list)))


def merge():
    book = {"people": [], "terms": [], "places": [], "figures": [], "open_questions": [], "forward_refs": [], "motifs": [], "sections": {}, "through_lines": {}}
    for f in sorted(LD.glob("ledger_ch*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        book["sections"].update(j.get("sections", {}))
        book["through_lines"][str(j.get("chapter"))] = j.get("through_line", "")
        for k in ("people", "terms", "places"):
            for x in j.get(k, []):
                name = (x.get("name") or x.get("term") or "").strip()
                prev = next((y for y in book[k] if (y.get("name") or y.get("term") or "").lower() == name.lower()), None)
                if prev is None:
                    book[k].append(x)
                elif re.match(r"\d+\.\d+$", str(x.get("first_section", ""))) and key(x["first_section"]) < key(prev.get("first_section", "99.9")):
                    prev.update(x)
        for k in ("figures", "open_questions", "forward_refs", "motifs"):
            book[k] += j.get(k, [])
    BOOK_JSON.write_text(json.dumps(book, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# Book ledger", "", "*Rebuilt 17 October 2026 from the book contents and the final texts of Chapter 1 (v6), Chapter 2 (v4), Chapter 3 (v4), Chapter 4 (v3), Chapter 5 (v1), Chapter 6 (v1), Chapter 7 (v1), Chapter 8 (v1), Chapter 9 (v1), Chapter 10 (v1), Chapter 11 (v1), Chapter 12 (v1) and the Afterword (v1); later chapters are added as they are drafted. Not evidence: a record of what the reader is told, and where.*", ""]
    for ch, tl in sorted(book["through_lines"].items()):
        md.append(f"- **Chapter {ch} through-line:** {tl}")
    for k, title, f in (("people", "People", lambda x: f"**{x.get('name')}** ({x.get('full_name', '')}), first {x.get('first_section')}: {x.get('role', '')}"),
                        ("terms", "Terms (gloss once, at first appearance in the book)", lambda x: f"*{x.get('term')}*: {x.get('gloss', '')} (first {x.get('first_section')})"),
                        ("places", "Places", lambda x: f"**{x.get('name')}**, first {x.get('first_section')}: {x.get('note', '')}"),
                        ("figures", "Committed figures", lambda x: f"{x.get('what')}: **{x.get('value')}** ({', '.join(x.get('sections', []))})"),
                        ("open_questions", "Open questions", lambda x: f"{x.get('question')} ({', '.join(x.get('sections', []))}; {x.get('status', '')})"),
                        ("forward_refs", "Forward references", lambda x: f"{x.get('from')} → {x.get('to')}: {x.get('what')}"),
                        ("motifs", "Motifs", lambda x: f"{x.get('motif')} ({', '.join(x.get('sections', []))})")):
        md += ["", f"## {title}", ""] + [f"- {f(x)}" for x in sorted(book[k], key=lambda x: key(x["first_section"]) if re.match(r"\d+\.\d+$", str(x.get("first_section", ""))) else (99, 0))]
    BOOK_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"book ledger: {BOOK_JSON}  " + ", ".join(f"{k} {len(v)}" for k, v in book.items() if isinstance(v, list)))


def _book():
    return json.loads(BOOK_JSON.read_text(encoding="utf-8")) if BOOK_JSON.exists() else {}


def digest(sec, context=""):
    """only what THIS section needs: people/terms/places named in its plan or evidence (context), figures assigned to it or
    whose keyword occurs in its context (at most 12), and the open questions it may advance (run 2: the full digest listed
    all 137 figures in every call)"""
    b = _book()
    if not b:
        return ""
    ctx = (context or "").lower()
    before = lambda x: re.match(r"\d+\.\d+$", str(x.get("first_section", ""))) and key(x["first_section"]) < key(sec)
    named = lambda s: bool(s) and (not ctx or s.lower() in ctx)
    ppl = [f"{x['name']} (full name given in {x['first_section']}: use '{x['name']}')" for x in b.get("people", [])
           if before(x) and x.get("full_name") and named(x.get("name", ""))]
    trm = [f"{x['term']} (glossed in {x['first_section']})" for x in b.get("terms", []) if before(x) and named(x.get("term", ""))]
    plc = [f"{x['name']} ({x['first_section']})" for x in b.get("places", []) if before(x) and named(x.get("name", ""))]
    fig = [f"{x['what']}: {x['value']}" for x in b.get("figures", [])
           if sec in x.get("sections", []) or (x.get("keyword") and x["keyword"].lower() in ctx)][:12]
    qs = [f"{x['question']}" for x in b.get("open_questions", []) if sec in x.get("sections", [])][:6]
    out = ["BOOK LEDGER DIGEST (continuity; not evidence)"]
    if ppl:
        out.append("Already introduced (no full name, no re-introduction): " + "; ".join(ppl))
    if trm:
        out.append("Already glossed (do not gloss again): " + "; ".join(trm))
    if plc:
        out.append("Places already introduced: " + "; ".join(plc))
    if fig:
        out.append("Committed figures (never contradict; never narrow a range): " + "; ".join(fig))
    if qs:
        out.append("Open questions this section may advance (never close what the plan leaves open): " + "; ".join(qs))
    return "\n".join(out)


def check(sec, text):
    b = _book()
    out = []
    before = lambda x: re.match(r"\d+\.\d+$", str(x.get("first_section", ""))) and key(x["first_section"]) < key(sec)
    plain = re.sub(r"\[[^\]]*\]|\{\{note:.*?\}\}", "", text, flags=re.S)
    for x in b.get("people", []):
        fn = (x.get("full_name") or "").strip()
        if before(x) and fn and len(fn.split()) > 1 and fn != x.get("name") and fn in plain:
            out.append(f"full name re-introduced: {fn} (introduced in {x['first_section']})")
    for x in b.get("terms", []):
        t = re.escape(x.get("term", ""))
        if before(x) and t and re.search(rf"\*{t}\*\s*(?:,\s*(?:a|an|the)\s|\()", plain, re.I):
            out.append(f"term glossed again: {x['term']} (glossed in {x['first_section']})")
    for x in b.get("figures", []):
        kw, val = x.get("keyword", ""), x.get("value", "")
        nums = set(re.findall(r"\d+(?:\.\d+)?", val))
        if not kw or not nums:
            continue
        for s in re.split(r"(?<=[.!?])\s+", plain):
            if re.search(rf"\b{re.escape(kw)}\b", s, re.I):
                got = set(re.findall(r"\d+(?:\.\d+)?", s))
                if got and not (got & nums) and len(got) <= 3 and all(len(g) <= 4 for g in got):
                    out.append(f"figure may conflict with ledger ({x['what']}: {val}): {s.strip()[:140]}")
    return out


def update(draft):
    sys.path.insert(0, str(HERE))
    from cfg import C
    import run as rn
    R = rn.Run(False)
    txt = re.sub(r"\[[^\]]*\]", "", Path(draft).read_text(encoding="utf-8"))
    out = R.call(f"ledger_update_ch{C.CH}", 9, "edit", EXTRACT_SYS, f"CHAPTER {C.CH} FINAL TEXT:\n\n{txt}", 2500, effort="medium")
    j = rn.parse_json(out) or {}
    j["chapter"] = C.CH
    old = LD / f"ledger_ch{C.CH}.json"
    if old.exists():
        o = json.loads(old.read_text(encoding="utf-8"))
        j["sections"], j["through_line"] = o.get("sections", {}), o.get("through_line", "")
    old.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ledger ch{C.CH} updated from final text")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1]
    if cmd == "build":
        build("--dry-run" in sys.argv)
    elif cmd == "merge":
        merge()
    elif cmd == "digest":
        print(digest(sys.argv[2]))
    elif cmd == "check":
        print("\n".join(check(sys.argv[2], Path(sys.argv[3]).read_text(encoding="utf-8"))) or "ok")
    elif cmd == "update":
        update(sys.argv[2])
