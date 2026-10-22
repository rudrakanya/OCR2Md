"""Turn judgments into the verified evidence log.

  python -I drafting/_tools/assemble.py

For every kept item in drafting/_runs/judgments/*.jsonl:
  1. slice the quote from the stored chunk text by sentence span (verbatim by construction);
     if the span crosses a `<!-- page N -->` marker it becomes several verbatim segments;
  2. locate every segment verbatim (whitespace-loose) in the chunk AND in the source Markdown,
     at/after the chunk's own position; page = last `<!-- page N -->` marker in force at the
     segment start in the source file (no marker -> [page not recorded] + heading);
  3. assign a unique item id.
Chapter 1 pilot items (C01_verified.jsonl, hand-extracted, already verified) are carried
over and re-verified the same way. Failures are logged and excluded.

Writes drafting/_evidence_log.jsonl, drafting/_runs/assembly_failures.jsonl,
drafting/_runs/judgment_summary.json.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "drafting" / "_tools"))
from engine import ROOT, RUNS, Corpus  # noqa: E402

CORPUS = ROOT / "Udaipur Books Markdown files"
# The two old Samarāṅgaṇa volumes are still what the collection indexes, but they were
# retired from the corpus folder on 2026-10-12 18:10; their last on-disk copies:
RETIRED = ROOT / "backups" / "2026-10-13_samarangana_reocr" / "Udaipur Books Markdown files"
PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)
SAMAR = {"Samrangana Sutradhar Vol 1.md": "Vol. 1", "Samarangan Vol 2 (a)_combined.md": "Vol. 2"}
SEG_JOIN = " … "


def loose(seg: str) -> re.Pattern:
    return re.compile(r"\s+".join(re.escape(p) for p in seg.split()))


def tolerant(seg: str) -> re.Pattern:
    """Like loose(), but also lets heading lines ('## …'), rule lines ('—'), HTML comments (page/element markers) and bare printed page-number lines sit between
    words: the chunker drops these from chunk text, the source file keeps them."""
    sep = r"\s+(?:(?:#{1,6} [^\n]*|[—–]+|<!--[^>]*-->|\(?\d{1,4}\)?(?=[ \t]*\n))\s+)*"
    return re.compile(sep.join(re.escape(p) for p in seg.split()))


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


class Sources:
    def __init__(self):
        self.cache = {}

    def get(self, sp: str):
        if sp not in self.cache:
            p = CORPUS / sp
            if not p.exists() and (RETIRED / sp).exists():
                p = RETIRED / sp
            self.cache[sp] = (p.read_text(encoding="utf-8"), str(p.relative_to(ROOT))) if p.exists() else (None, None)
        return self.cache[sp]


def segments_from_span(text: str, spans, a: int, b: int) -> list[str]:
    s, e = spans[a - 1][0], spans[b - 1][1]
    # The sentence splitter breaks abbreviations such as "A. D." / "B. C." after the first
    # initial; carry a span that ends on a lone capital initial through the rest of it.
    while re.search(r"(?:^|[\s(])[A-Z]\.$", text[s:e]):
        m = re.match(r"\s?[A-Z]\.", text[e:])
        if not m:
            break
        e += m.end()
    raw = text[s:e]
    segs = [x.strip() for x in PAGE_RE.split(raw)]
    # PAGE_RE.split keeps the captured page numbers at odd positions: drop them
    segs = [x for i, x in enumerate(segs) if i % 2 == 0 and x]
    return segs


def verify(segs: list[str], chunk: str, src: str | None):
    pos = 0
    for s in segs:
        m = loose(s).search(chunk, pos)
        if not m:
            return {"ok": False, "why": f"segment not in chunk: {s[:60]!r}"}
        pos = m.end()
    if src is None:
        return {"ok": False, "why": "source file missing"}
    anchor = locate_chunk(src, chunk)
    note = ""
    pos, spans = anchor, []
    for s in segs:
        m = loose(s).search(src, pos)
        if not m:
            # Anchor miss: the chunk's first long line can recur later in the file, so the
            # anchor lands past the quote. Accept a whole-file match only if it is unique.
            hits = list(loose(s).finditer(src, spans[-1][1] if spans else 0))
            if not hits:
                m2 = tolerant(s).search(src, pos)
                hits = [m2] if m2 else []
                if m2:
                    note = "source has heading/rule/marker lines inside the quoted span (omitted in chunk text)"
            if len(hits) != 1:
                return {"ok": False, "why": f"segment not in source after chunk anchor ({len(hits)} whole-file matches): {s[:60]!r}"}
            m = hits[0]
            note = note or "located by unique whole-file match (chunk anchor missed)"
        spans.append((m.start(), m.end()))
        pos = m.end()
    return {"ok": True, "page": page_at(src, spans[0][0]), "page_end": page_at(src, spans[-1][1] - 1),
            "src_offset": spans[0][0], "v_note": note}


def citation(sp: str, page, page_end, heading: str) -> str:
    if page is None:
        return f"[page not recorded] — section: {heading or '(no heading)'}"
    pr = f"{page}" if page_end in (None, page) else f"{page}–{page_end}"
    if sp == "Jagta_Hua_Kasba_EN.md":
        return f"≈ Hindi-original scan p. {pr} (derived)"
    if sp in SAMAR:
        return f"{SAMAR[sp]}, scan p. {pr} ⚠ old OCR, pending re-OCR"
    return f"scan p. {pr}"


def main():
    C = Corpus()
    codes = json.loads((RUNS / "book_codes.json").read_text(encoding="utf-8"))["codes"]
    idx = json.loads((RUNS / "packets" / "_index.json").read_text(encoding="utf-8"))
    spans = {}
    for l in (RUNS / "packets" / "_sentences.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        spans[r["chunk_id"]] = r["spans"]
    S = Sources()
    items, fails = [], []
    decisions = {}
    done_packets = []
    for pid, ids in sorted(idx.items()):
        f = RUNS / "judgments" / f"{pid}.jsonl"
        if not f.exists():
            continue
        done_packets.append(pid)
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            cid = next(c for c in ids if c.startswith(r["c"]))
            decisions[cid] = {"keep": bool(r.get("keep")), "reason": r.get("reject_reason", ""), "packet": pid}
            for it in r.get("items") or []:
                j = C.idx[cid]
                text, meta = C.text[j], C.meta[j]
                segs = segments_from_span(text, spans[cid], *it["span"])
                src, srcfile = S.get(meta["source_path"])
                v = verify(segs, text, src)
                rec = {"unit": it["unit"], "sub": it["sub"], "xref": it.get("xref") or [], "type": it["type"],
                       "strength": it["strength"], "quote": SEG_JOIN.join(segs), "segments": segs,
                       "gloss": it.get("gloss"), "note": it["note"], "claim": it.get("claim"),
                       "refs": it.get("refs") or [], "span": it["span"], "chunk_id": cid, "packet": pid,
                       "origin": "subagent", "source_path": meta["source_path"], "source_file": srcfile}
                (items if v["ok"] else fails).append((rec, v, meta))
    # ---- Chapter 1 pilot items -------------------------------------------------
    pilot_n = 0
    for l in (RUNS / "C01_verified.jsonl").open(encoding="utf-8"):
        p = json.loads(l)
        cid = p["chunk_id"]
        j = C.idx[cid]
        text, meta = C.text[j], C.meta[j]
        segs = [s for s in p["q"].split(SEG_JOIN) if s.strip()]
        src, srcfile = S.get(meta["source_path"])
        v = verify(segs, text, src)
        # Pilot items stay in C01 under their C01 sub-topic. A pilot "home" elsewhere is kept
        # as a hint: the same chunk was judged for that unit by the subagent pass as well.
        rec = {"unit": "C01", "sub": p["sub"], "xref": [x for x in (p.get("xref") or []) if x != "C01"],
               "home_hint": p.get("home") if p.get("home") not in (None, "C01") else None,
               "type": p["type"], "strength": p["str"], "quote": p["q"], "segments": segs,
               "gloss": p.get("gloss") or None, "note": p["note"], "claim": p.get("claim"), "refs": p.get("refs") or [],
               "span": None, "chunk_id": cid, "packet": "C01-pilot", "origin": "pilot (hand-extracted)",
               "source_path": meta["source_path"], "source_file": srcfile}
        (items if v["ok"] else fails).append((rec, v, meta))
        pilot_n += 1
    # ---- curated claim tags for pilot items (tag_pilot_claims.py) -------------
    pc_path = RUNS / "pilot_claims.json"
    if pc_path.exists():
        pc = {(x["chunk_id"], x["quote_start"]): x["claim"] for x in json.loads(pc_path.read_text(encoding="utf-8"))}
        for rec, _, _ in items:
            if rec["origin"].startswith("pilot") and not rec.get("claim"):
                c = pc.get((rec["chunk_id"], " ".join(rec["quote"].split())[:60]))
                if c:
                    rec["claim"] = dict(c, tagged_by="orchestrator")
    # ---- reviewed claim corrections (claim_overrides.json; claim null = untag) --
    co_path = RUNS / "claim_overrides.json"
    if co_path.exists():
        co = {(x["chunk_id"], x["quote_start"]): x for x in json.loads(co_path.read_text(encoding="utf-8"))}
        for rec, _, _ in items:
            x = co.get((rec["chunk_id"], " ".join(rec["quote"].split())[:60]))
            if x:
                rec["claim"] = x["claim"]
    # ---- merge overlapping quotes (same unit, same book) -----------------------
    # Overlapping chunks of one book yield the same sentence twice; when one item's quote
    # is contained in another's, keep the longer one and record the shorter's place as "also at".
    def norm(q):
        return " ".join(q.split())
    groups = collections.defaultdict(list)
    for t in items:
        groups[(t[0]["unit"], t[0]["source_path"])].append(t)
    merged_items, overlap_merged = [], 0
    for g in groups.values():
        g.sort(key=lambda t: -len(norm(t[0]["quote"])))
        kept = []
        for t in g:
            q = norm(t[0]["quote"])
            host = next((k for k in kept if q in norm(k[0]["quote"])), None)
            if host is None:
                t[0].setdefault("also_at", [])
                kept.append(t)
                continue
            overlap_merged += 1
            hrec = host[0]
            hrec["also_at"].append({"chunk_id": t[0]["chunk_id"], "citation": citation(
                t[0]["source_path"], t[1]["page"], t[1]["page_end"], t[2].get("heading_path", ""))})
            hrec["xref"] = sorted(set(hrec["xref"]) | set(t[0]["xref"]) - {hrec["unit"]})
            if t[0]["strength"] == "direct":
                hrec["strength"] = "direct"
            if t[0].get("claim") and not hrec.get("claim"):
                hrec["claim"] = t[0]["claim"]
            hrec["refs"] = sorted(set(hrec["refs"]) | set(t[0]["refs"]))
        merged_items.extend(kept)
    items = merged_items
    # ---- ids, citations, write -----------------------------------------------
    counters = collections.Counter()
    out = []
    seen_keys = set()
    dups = 0
    for rec, v, meta in sorted(items, key=lambda t: (t[0]["unit"], codes.get(t[0]["source_path"], t[0]["source_path"]),
                                                    t[0]["sub"], v_page(t[1]), t[0]["chunk_id"])):
        key = (rec["unit"], rec["chunk_id"], rec["quote"])
        if key in seen_keys:
            dups += 1
            continue
        seen_keys.add(key)
        code = codes.get(rec["source_path"], "X")
        counters[(rec["unit"], code)] += 1
        rec["id"] = f"{rec['unit']}-{code}-{counters[(rec['unit'], code)]:03d}"
        rec.update(page=v["page"], page_end=v["page_end"], src_offset=v["src_offset"], v_note=v.get("v_note", ""),
                   citation=citation(rec["source_path"], v["page"], v["page_end"], meta.get("heading_path", "")),
                   book_title=meta.get("book_title"), author=meta.get("author"), book_year=meta.get("book_year"),
                   heading=meta.get("heading_path"), language=meta.get("language"), book_code=code)
        out.append(rec)
    ids_ = [r["id"] for r in out]
    assert len(ids_) == len(set(ids_)), "duplicate item ids"
    with (ROOT / "drafting" / "_evidence_log.jsonl").open("w", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (RUNS / "assembly_failures.jsonl").open("w", encoding="utf-8") as fh:
        for rec, v, _ in fails:
            fh.write(json.dumps(dict(rec, why=v["why"]), ensure_ascii=False) + "\n")
    summ = {"packets_judged": len(done_packets), "packets_total": len(idx),
            "chunks_judged": len(decisions), "chunks_kept": sum(d["keep"] for d in decisions.values()),
            "chunks_rejected": sum(not d["keep"] for d in decisions.values()),
            "items_verified": len(out), "items_failed": len(fails), "pilot_items_carried": pilot_n,
            "exact_duplicate_items_dropped": dups, "overlapping_items_merged": overlap_merged,
            "verification_pass_rate": round((len(out) + dups + overlap_merged) / max(len(out) + dups + overlap_merged + len(fails), 1), 4)}
    (RUNS / "judgment_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    (RUNS / "decisions.json").write_text(json.dumps(decisions), encoding="utf-8")
    print(json.dumps(summ, indent=1))
    for rec, v, _ in fails[:20]:
        print("FAIL", rec["chunk_id"][:10], rec["source_path"][:30], v["why"])


def v_page(v):
    return v.get("page") or 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
