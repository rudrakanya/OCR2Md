"""Chapter 1 v2 — Step 1: use the vector knowledge base (read-only) before drafting.

Reads the in-memory snapshot of the production collection `udaypur_corpus_openai_large`
(drafting/_tools/corpus_snapshot.npz + corpus_meta.pkl, built read-only by engine.py with COLLECTION set
explicitly); query vectors go to drafting/_tools/query_cache.sqlite3. Nothing is written under chroma_db/.

A  context: for every pack item, its own chunk + neighbours (chunk_index ±1) -> trimmed context excerpt
B  gap queries (5–10 per section, hybrid dense+BM25 RRF, each with a per-book sweep) -> candidate chunks
C  contradiction queries for the outline's key claims -> candidate chunks
   relevance is judged by gpt-6.1-sol (one call per batch, all in parallel, effort medium); the model returns
   sentence spans only; quotes are sliced by code from the stored chunk and verified verbatim in the source
   Markdown; page = marker in force. New items: C01-KB-<BOOKCODE>-NNN, tagged kb-new (≤ ~40).
Outputs: evidence_pack_v2.json (pack + context excerpts + new items), ch01_kb_additions.md, kb_v2_state.json

  python -I "drafting/ch01/kb_v2.py" --dry-run
  python -u -I "drafting/ch01/kb_v2.py"
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "_tools"))
import engine as eg  # noqa: E402
import build_packets as bp  # noqa: E402
import assemble as asm  # noqa: E402
import pipeline_v3 as pv  # noqa: E402

D = HERE
CODES = json.loads((HERE.parent / "_runs" / "book_codes.json").read_text(encoding="utf-8"))
SHORT, FLAGS = CODES["codes"], CODES["flags"]
EXCLUDE_SOURCES = {"The Udayesvara Temple Art, Architecture and Philosophy of the Saiva Siddhanta.md"}  # Pande twin
MAX_NEW = 42
GLOBAL_K, BOOK_K = 12, 2
pv.LOG = D / "api_log_v2"                       # v2 has its own log and its own $5 budget
pv.UNACCOUNTED = 0.0
pv.BUDGET = 5.00
pv.EFFORT.update({"kbjudge": "medium"})

GAP = {
    "1.1": ["Udaypur village setting at the foot of the hill, approach to the temple through the village",
            "lanes houses and old gateways of Udaypur town today",
            "उदयपुर गांव की गलियां पुराने दरवाजे और घर",
            "Udaypur landscape hill tank fields Vindhyan sandstone setting",
            "visitors arriving at Udaypur temple from the main road",
            "Chanderi darwaza gate of Udaypur fort wall"],
    "1.2": ["monuments of different periods at Udaypur Hindu and Muslim buildings",
            "Shahi masjid and mahal at Udaypur Mughal period",
            "Udaypur under Gwalior state Scindia administration temple",
            "Archaeological Survey of India protected monument Udaypur temple",
            "Udaypur an important Paramara centre administrative headquarters",
            "inscriptions of later periods at Udaypur pilgrims records"],
    "1.3": ["earliest mention of Udayapura in inscriptions",
            "Vidisha region ancient Dasarna Akara before the Paramaras",
            "Udaypur history before the Paramaras earlier settlement",
            "Bhujariya talab older tank Udaypur",
            "first scholarly accounts of the Udayesvara temple Cunningham Beglar survey"],
    "1.4": ["Udayaditya named the town temple and tank after himself",
            "Udayasamudra tank location ruins",
            "Nilakantheshvara and Udayeshvara names of the temple",
            "Udaipur in Madhya Pradesh distinct from Udaipur in Rajasthan",
            "Udayaditya restored Paramara power after the death of Bhoja"],
    "1.5": ["Udaipur prasasti panegyric genealogy reliability",
            "legends about the temple and local traditions of its building",
            "Udayaditya date of accession reign years",
            "the temple as a living place of worship today"],
    "sig": ["Udayesvara temple significance Bhumija architecture model for later temples",
            "Udaypur temple importance in the history of Indian architecture",
            "Paramara architecture finest surviving temple Udaypur"],
}
CONTRA = {
    "founding attribution and dates": "Udayaditya founded Udayapura and began the temple in 1059 completed 1080",
    "accession c. 1070": "Udayaditya came to the throne in 1070 accession date reign",
    "Tughluq tradition": "Muhammad Tughluq ordered the Udayesvara temple destroyed mosque built",
    "Aurangzeb tradition": "Aurangzeb Udaypur temple legend dream demolition",
    "the praśasti": "Udaipur prasasti date location genealogy undated reliability",
    "Lūṇapasāka date": "Lunapasaka grant Udayapur Vaidyanatha date samvat",
}

JUDGE_SYS = """You select evidence for Chapter 1 of a book on Udaypur (Udayapura), Vidisha district, Madhya Pradesh — NOT Udaipur in Rajasthan.
You receive numbered-sentence chunks from the reference library and a task (gap topics, or key claims to test). Choose only passages that add something NEW and specific for the task (not a restatement of the items already held, listed per chunk).
For a CONTRADICTION task, choose only passages that contradict or qualify the stated claim, and give the claim key and what this source says.
Rules: spans are [first, last] sentence numbers of the chunk (1–4 sentences); never retype text; Temple Economics is contextual only and its 'Udaipur' is Rajasthan; Samarāṅgaṇa (SAMAR-*) is old OCR; Hindi/Sanskrit spans need an English gloss (your own translation).
Return ONLY JSON: {"items": [{"c": "<chunk id prefix as shown>", "span": [a,b], "section": "1.1|1.2|1.3|1.4|1.5", "sub": "S1..S6", "strength": "direct|contextual", "note": "why it matters", "gloss": "only for Hindi/Sanskrit", "claim": {"key": "...", "value": "what this source says"} or null}]} — at most MAX items."""
SUBS = "S1 names/identity; S2 location/setting/approach; S3 references in texts/records; S4 memory/legends; S5 significance; S6 historical questions"


def ts():
    return time.strftime("%H:%M:%S")


def load_corpus():
    C = eg.Corpus()
    by_src = collections.defaultdict(dict)
    for j, m in enumerate(C.meta):
        by_src[m["source_path"]][m.get("chunk_index", 0)] = j
    return C, by_src


def context_excerpt(C, by_src, chunk_id, quote, before=110, after=70):
    j = C.idx.get(chunk_id)
    if j is None:
        return ""
    m = C.meta[j]
    ci, sp = m.get("chunk_index", 0), m["source_path"]
    prev_j, next_j = by_src[sp].get(ci - 1), by_src[sp].get(ci + 1)
    txt = (C.text[prev_j] + "\n" if prev_j is not None else "") + C.text[j] + ("\n" + C.text[next_j] if next_j is not None else "")
    txt = re.sub(r"<!--[^>]*-->", " ", txt)
    words = txt.split()
    qw = " ".join(quote.split()[:6])
    flat = " ".join(words)
    k = flat.find(qw) if qw else -1
    if k < 0:
        return " ".join(words[:before + after]) + " …"
    pre = flat[:k].split()[-before:]
    post = flat[k:].split()[: len(quote.split()) + after]
    return ("… " if len(flat[:k].split()) > before else "") + " ".join(pre + post) + " …"


def retrieve(C, queries, dry):
    """hybrid RRF over the whole collection + per-book sweep; returns {query: [chunk index,…]}"""
    Q = eg.Corpus.embed(queries) if not dry or True else None   # cached; embeddings cost ~nothing
    Dm = (Q @ C.E.T).astype(np.float32)
    L = C.lex_scores(queries)
    F = eg.fuse(Dm, L, C.dup)
    out = {}
    src = C.src
    for i, q in enumerate(queries):
        got = list(np.argsort(-F[i])[:GLOBAL_K])
        for b in C.books:
            if b in EXCLUDE_SOURCES:
                continue
            cols = np.where(src == b)[0]
            fb = eg.fuse(Dm[i:i + 1, cols], L[i:i + 1, cols], C.dup[cols])[0]
            got += [cols[k] for k in np.argsort(-fb)[:BOOK_K] if Dm[i, cols[k]] >= 0.36 or L[i, cols[k]] > 0]
        out[q] = [g for g in dict.fromkeys(int(x) for x in got) if C.src[g] not in EXCLUDE_SOURCES]
    return out, F, Dm


def rank_pool(C, hits, Dm, queries, cap):
    best = collections.defaultdict(float)
    qi = {q: i for i, q in enumerate(queries)}
    for q, js in hits.items():
        for j in js:
            best[j] = max(best[j], float(Dm[qi[q], j]))
    return [j for j, _ in sorted(best.items(), key=lambda t: -t[1])][:cap]


def packet(C, js, held_by_chunk):
    lines = []
    for j in js:
        cid, m, text = C.ids[j], C.meta[j], C.text[j]
        code = SHORT.get(m["source_path"], "?")
        sp = [s for s in bp.sentences(text) if s[0] == "s"]
        lines.append(f"### {cid[:10]} | {code} | scan p.{m.get('page_start')} | {m.get('heading_path') or ''}"
                     + (f" | {FLAGS[code]}" if code in FLAGS else ""))
        if held_by_chunk.get(cid):
            lines.append("ALREADY HELD from this chunk: " + " || ".join(q[:120] for q in held_by_chunk[cid]))
        for k, (_, a, b) in enumerate(sp, 1):
            lines.append(f"[{k}] {' '.join(text[a:b].split())}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    P = {i["id"]: i for i in json.loads((D / "evidence_pack.json").read_text(encoding="utf-8"))}
    C, by_src = load_corpus()
    # ---------------- A: context excerpts (code only)
    for i in P.values():
        i["context"] = context_excerpt(C, by_src, i.get("chunk_id"), i["quote"])
    nA = sum(bool(i["context"]) for i in P.values())
    held = collections.defaultdict(list)
    for i in P.values():
        if i.get("chunk_id"):
            held[i["chunk_id"]].append(" ".join(i["quote"].split()))
    held_ids = set(held)
    # ---------------- B + C retrieval
    gap_q = [(sec, q) for sec, qs in GAP.items() for q in qs]
    con_q = list(CONTRA.items())
    queries = [q for _, q in gap_q] + [q for _, q in con_q]
    hits, F, Dm = retrieve(C, queries, a.dry_run)
    batches = []
    for sec in GAP:
        qs = [q for s, q in gap_q if s == sec]
        pool = rank_pool(C, {q: hits[q] for q in qs}, Dm, queries, 16)
        batches.append(("gap", sec, qs, pool))
    pool = rank_pool(C, {q: hits[q] for _, q in con_q}, Dm, queries, 18)
    batches.append(("contra", "C", [f"{k}: {q}" for k, q in con_q], pool))
    R = pv.Run(a.dry_run)
    caps = {"gap": 7, "contra": 8}

    def judge(kind, sec, qs, pool):
        def job():
            task = ("GAP TOPICS for section " + ("1.2 (significance assessments)" if sec == "sig" else sec) + ":\n- " + "\n- ".join(qs)
                    if kind == "gap" else "KEY CLAIMS TO TEST (find contradicting or qualifying passages):\n- " + "\n- ".join(qs))
            u = f"{task}\n\nSub-topic codes: {SUBS}\n\nCHUNKS:\n{packet(C, pool, held)}"
            out = R.call(f"kb_{kind}_{sec}", 0, "kbjudge", JUDGE_SYS.replace("MAX", str(caps[kind])), u, 600)
            return pv.parse_json(out) if out else None
        return job
    res = R.parallel([((k, s), judge(k, s, qs, pool)) for k, s, qs, pool in batches])
    # ---------------- build verified new items
    S = asm.Sources()
    new, rejected = [], []
    counters = collections.Counter()
    for (kind, sec), r in sorted(res.items(), key=lambda t: str(t[0])):
        if not isinstance(r, dict):
            continue
        pool = next(b[3] for b in batches if b[0] == kind and b[1] == sec)
        for x in r.get("items", [])[: caps[kind]]:
            js = [j for j in pool if C.ids[j].startswith(str(x.get("c", ""))[:10])]
            if len(js) != 1:
                rejected.append((x, "chunk id not in batch"))
                continue
            j = js[0]
            cid, m, text = C.ids[j], C.meta[j], C.text[j]
            sp = [[s[1], s[2]] for s in bp.sentences(text) if s[0] == "s"]
            span = x.get("span") or [0, 0]
            if not (isinstance(span, list) and len(span) == 2 and 1 <= span[0] <= span[1] <= len(sp) and span[1] - span[0] <= 4):
                rejected.append((x, "bad span"))
                continue
            segs = asm.segments_from_span(text, sp, span[0], span[1])
            src_text, src_file = S.get(m["source_path"])
            v = asm.verify(segs, text, src_text)
            if not v["ok"]:
                rejected.append((x, v["why"]))
                continue
            quote = asm.SEG_JOIN.join(segs)
            if any(quote in h or h in quote for h in held.get(cid, [])):
                rejected.append((x, "duplicate of a held item"))
                continue
            code = SHORT.get(m["source_path"], "X")
            if code == "TEMPLE-ECON":
                x["strength"] = "contextual"
            counters[code] += 1
            iid = f"C01-KB-{code}-{counters[code]:03d}"
            cit = asm.citation(m["source_path"], v["page"], v["page_end"], m.get("heading_path", ""))
            page = ("≈ p. %s (Hindi original)" % (v["page"]) if code == "JAGTA-EN" and v["page"] is not None
                    else ("no page; " + (m.get("heading_path") or "")) if v["page"] is None
                    else f"p. {v['page']}" + (f"–{v['page_end']}" if v["page_end"] not in (None, v["page"]) else ""))
            flags = ["kb-new"]
            if code.startswith("SAMAR"):
                flags.append("⚠")
            if code == "JAGTA-EN":
                flags.append("≈ (Hindi original)")
            if v["page"] is None:
                flags.append("no page")
            book_title = next((i["book_title"] for i in P.values() if i["book_code"] == code), m.get("book_title") or code)
            item = {"id": iid, "book_code": code, "book_title": book_title, "page": page, "quote": quote,
                    "strength": x.get("strength", "contextual"), "also": [], "flags": flags, "sub": x.get("sub", "S6"),
                    "note": x.get("note", ""), "gloss": x.get("gloss") or None, "claim": x.get("claim") or None,
                    "chunk_id": cid, "author": m.get("author"), "log_citation": cit, "language": m.get("language"),
                    "kb_step": "B" if kind == "gap" else "C", "kb_section": (sec if kind == "gap" else None),
                    "context": context_excerpt(C, by_src, cid, quote), "v_note": v.get("v_note", "")}
            new.append(item)
            held[cid].append(" ".join(quote.split()))
    new = new[:MAX_NEW]
    pack2 = list(P.values()) + new
    state = {"A_items_with_context": nA, "B_queries": len(gap_q), "C_queries": len(con_q),
             "candidate_chunks": {f"{k}:{s}": len(p) for k, s, _, p in batches},
             "new_items": len(new), "by_step": dict(collections.Counter(i["kb_step"] for i in new)),
             "rejected": [(str(x)[:160], why) for x, why in rejected], "spent_usd": round(R.spent, 4),
             "calls": R.calls, "seconds": round(time.time() - t0)}
    if a.dry_run:
        print(json.dumps({k: v for k, v in state.items() if k not in ("calls", "rejected")}, indent=1))
        return
    (D / "evidence_pack_v2.json").write_text(json.dumps(pack2, ensure_ascii=False, indent=1), encoding="utf-8")
    (D / "kb_v2_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    write_additions(new)
    print(json.dumps({k: v for k, v in state.items() if k not in ("calls", "rejected")}, indent=1))
    print(f"[{ts()}] KB STEP FINISHED", flush=True)


def write_additions(new):
    L = ["# Chapter 1 — knowledge-base additions (v2)\n",
         "Items found in the vector knowledge base for Chapter 1 v2, in the evidence-map format. Quotes are sliced from the "
         "stored chunk and verified verbatim against the source Markdown; pages are the marker in force. Tag: `kb-new`.\n"]
    by_book = collections.defaultdict(list)
    for i in new:
        by_book[(i["book_title"], i["book_code"])].append(i)
    for (title, code), items in sorted(by_book.items()):
        L.append(f"## {title} ({code}, {len(items)})\n")
        for i in items:
            L.append(i["quote"].strip())
            if i.get("gloss"):
                L.append(f"*English rendering [my translation]:* {i['gloss']}")
            extra = [f"step {i['kb_step']}", f"sub {i['sub']}", i["strength"]]
            if i.get("claim"):
                extra.append(f"conflict: {i['claim'].get('key')} → {i['claim'].get('value')}")
            flags = [f for f in i["flags"] if f not in ("kb-new",)]
            L.append(f"`{i['id']}`   {i['page']}" + (f"   {' '.join(flags)}" if flags else "") + "   (" + "; ".join(extra) + ")\n")
    (D / "ch01_kb_additions.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
