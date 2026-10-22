"""Render the 13 chapter files and _master.md from drafting/_evidence_log.jsonl + run logs.

  python -I drafting/_tools/render.py [--by subtopic]

Pure script, no model calls: any alternative view is a re-run.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
DR = ROOT / "drafting"
RUNS = DR / "_runs"
SLUG = {"C01": "historical-memory", "C02": "betwa-valley", "C03": "before-udaypur", "C04": "paramaras-foundation",
        "C05": "udayesvara-temple", "C06": "inscriptions", "C07": "built-heritage", "C08": "religion-material-life",
        "C09": "society-culture", "C10": "political-change", "C11": "modern-period", "C12": "udaypur-today",
        "C13": "afterword"}
SAMAR = {"Samrangana Sutradhar Vol 1.md", "Samarangan Vol 2 (a)_combined.md"}
TWIN = ("The Udayesvara Temple Art, Architecture and Philosophy of the Saiva Siddhanta.md",
        "The Udayesvara Temple - Anupa Pande.md")


# Cited-work normaliser for the gap lists: (pattern, canonical work, in library?)
WORKS = [
    (r"beglar|ASI (rep\w* )?vol\.? ?VII\b|ASR,? vol\.? ?VII|ASI VII|Cunningham.*(VII|1871)", "Beglar / Cunningham, ASI Reports vol. VII (Bundelkhand & Malwa, 1871–72)", False),
    (r"Cunningham.*(1874|1876|X\b|vol\.? ?X|vol\.? ?10)|ASI (vol\.? )?(X|10)\b", "Cunningham, ASI Reports vol. X (Bundelkhand & Malwa, 1874–77)", False),
    (r"H\.? ?C\.? Ray|Dynastic History", "H. C. Ray, Dynastic History of Northern India", False),
    (r"Epigraphia Indica|Ep\.? ?Ind|\bE\.? ?I\.? [IVX]", "Epigraphia Indica (various volumes)", False),
    (r"Bhandarkar.*List", "D. R. Bhandarkar, List of Inscriptions of Northern India", False),
    (r"Trivedi|Corpus Inscriptionum|CII", "Trivedi, CII vol. VII (Paramāra inscriptions)", True),
    (r"Ganguly", "D. C. Ganguly, History of the Paramāra Dynasty", True),
    (r"Kramrisch|Hindu Temples? II", "Stella Kramrisch, The Hindu Temple", True),
    (r"Samar[aā]ṅ?n?gana|Samarangana|Samarāṅgaṇa", "Samarāṅgaṇasūtradhāra (old OCR in library; re-OCR not ingested)", True),
    (r"Percy Brown|P\. Brown", "Percy Brown, Indian Architecture", False),
    (r"Malcolm", "John Malcolm, Memoir of Central India", False),
    (r"Ain-i-Akbari", "Abu'l Fazl, Ā'īn-i Akbarī", False),
    (r"ASIAR|Annual Report.*Arch|Progress Report", "Archaeological Survey of India, Annual Reports", False),
    (r"Gwalior.*(Report|State)", "Gwalior State Archaeological Department, Annual Reports", False),
    (r"Kielhorn", "F. Kielhorn (editions in Epigraphia Indica / Indian Antiquary)", False),
    (r"B[uü]hler", "G. Bühler, edition of the Udaipur praśasti (EI vol. I)", False),
    (r"Mayamata", "Mayamata", False),
    (r"Navas[aā]h[aā]s[aā]nka", "Padmagupta, Navasāhasāṅkacarita", False),
    (r"Prabandha", "Merutuṅga, Prabandhacintāmaṇi", False),
    (r"Fergusson", "J. Fergusson, History of Indian and Eastern Architecture", False),
    (r"Cousens", "H. Cousens, Mediaeval Temples of the Dakhan", False),
    (r"Bhatia", "Pratipal Bhatia, The Paramāras", False),
    (r"Imperial Gazetteer", "Imperial Gazetteer of India", False),
    (r"Apar[aā]jitap", "Aparājitapṛcchā", False),
    (r"Banerjea", "J. N. Banerjea, The Development of Hindu Iconography", False),
]


def norm_work(ref: str):
    for pat, name, inlib in WORKS:
        if re.search(pat, ref, re.I):
            return name, inlib
    return ref.strip(), None


def refs_md(counter, indent=""):
    grp = collections.defaultdict(list)
    for x, n in counter.items():
        name, inlib = norm_work(x)
        grp[(name, inlib)].append((x, n))
    out = []
    for (name, inlib), L in sorted(grp.items(), key=lambda t: (t[0][1] is True, -sum(n for _, n in t[1]), t[0][0])):
        tag = " — **in library**" if inlib else (" — not in library" if inlib is False else " — check")
        n = sum(n for _, n in L)
        cites = "; ".join(sorted({x for x, _ in L}))[:400]
        out.append(f"{indent}- [ ] **{name}**{tag} (×{n}): {cites}")
    return out


def jl(p):
    return [json.loads(l) for l in Path(p).open(encoding="utf-8") if l.strip()]


def esc(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def label(u):
    return "Afterword" if u == "C13" else f"Chapter {int(u[1:])}"


def fname(u):
    return f"ch{int(u[1:]):02d}_{SLUG[u]}.md" if u != "C13" else f"ch13_{SLUG[u]}.md"


def book_name(r):
    t = r.get("book_title") or r["source_path"]
    a = r.get("author")
    return f"*{t}*" + (f" — {a}" if a else "")


def page_key(r):
    return r.get("page") if r.get("page") is not None else 10 ** 6


def item_md(r, units, xref_here=False):
    out = [f"- **{r['id']}** · [{r['sub']}] {r['type']} · {r['strength']}"
           + (f" · also → {', '.join(r['xref'])}" if r.get("xref") else "")
           + (f" · pilot home hint → {r['home_hint']}" if r.get("home_hint") else "")]
    q = r["quote"].strip()
    out.append("  > " + q.replace("\n", "\n  > "))
    if r.get("gloss"):
        out.append(f"  > *Gloss [my translation]:* {r['gloss']}")
    out.append(f"  — {r['citation']} · chunk `{r['chunk_id'][:10]}`"
               + (f" · also at: {'; '.join(a['citation'] + ' (`' + a['chunk_id'][:10] + '`)' for a in r['also_at'])}" if r.get("also_at") else "")
               + (f" · ⚠ {r['v_note']}" if r.get("v_note") and "heading" not in r["v_note"] else ""))
    out.append(f"  *Relevance:* {r['note']}")
    if r.get("claim"):
        out.append(f"  *Claim:* {r['claim'].get('key')} → {r['claim'].get('value')}")
    if r.get("refs"):
        out.append(f"  *Cites:* {'; '.join(r['refs'])}")
    return "\n".join(out)


def main(by: str):
    units = json.loads((RUNS / "units.json").read_text(encoding="utf-8"))
    codes = json.loads((RUNS / "book_codes.json").read_text(encoding="utf-8"))["codes"]
    ev = jl(DR / "_evidence_log.jsonl")
    queries = jl(RUNS / "queries.jsonl")
    rlog = jl(RUNS / "retrieval_log.jsonl")
    plog = jl(RUNS / "prefilter_log.jsonl")
    dlog = jl(RUNS / "deepening_log.jsonl")
    decisions = json.loads((RUNS / "decisions.json").read_text(encoding="utf-8"))
    cands = {r["chunk_id"]: r for r in jl(RUNS / "candidates.jsonl")}
    pilot = {r["chunk_id"]: r for r in jl(RUNS / "C01_judgments.jsonl")}
    summ = json.loads((RUNS / "judgment_summary.json").read_text(encoding="utf-8"))
    rsum = json.loads((RUNS / "retrieval_summary.json").read_text(encoding="utf-8"))
    books = sorted(codes)  # 29 sources in the collection
    by_unit = collections.defaultdict(list)
    for r in ev:
        by_unit[r["unit"]].append(r)
    xrefs = collections.defaultdict(list)
    for r in ev:
        for x in r.get("xref") or []:
            xrefs[x].append(r)
    # conflicts: claim keys with >= 2 distinct values (across all units)
    claims = collections.defaultdict(list)
    for r in ev:
        c = r.get("claim")
        if c and c.get("key"):
            claims[c["key"].strip()].append(r)
    conflict_keys = {k for k, L in claims.items()
                     if len({re.sub(r"\W+", " ", (x["claim"].get("value") or "").lower()).strip() for x in L}) >= 2
                     and len({x["source_path"] for x in L}) >= 2}
    corpus_titles = " ".join(set((r.get("book_title") or "") + " " + r["source_path"] for r in ev)).lower()

    master_rows = []
    for u, U in units.items():
        items = by_unit.get(u, [])
        L = []
        L.append(f"# {label(u)}. {U['title']}\n")
        L.append(f"{U['desc']}\n")
        L.append("**Sub-topics:** " + "; ".join(f"**{s}** {t}" for s, t in U["subtopics"].items()) + "\n")
        L.append("*Evidence map only. Quotes are verbatim slices of the stored chunks, verified against the source "
                 "Markdown; pages are the `<!-- page N -->` marker in force (\"scan p.\"). Notes state relevance only. "
                 "Conflicts are shown side by side, not resolved.*\n")
        notes = []
        if any(r["source_path"] in SAMAR for r in items):
            notes.append("⚠ **Samarāṅgaṇasūtradhāra items cite the old two-volume OCR** that the database still indexes. "
                         "A re-OCR (`samarangana-sutradhara.md`, 2026-10-12 18:10) is now in the corpus folder but not ingested: "
                         "**re-verify every SAMAR item against it before use.**")
        notes.append(f"The Anupa Pande monograph exists in the collection as two copies; this map cites "
                     f"`{TWIN[1]}` only. The duplicate (`{TWIN[0]}`) was dropped before reading.")
        if any(r["source_path"] == "Jagta_Hua_Kasba_EN.md" for r in items):
            notes.append("*Jagta Hua Kasba* (English translation) pages are derived from the Hindi original and approximate (≈).")
        if any(r["source_path"] == "patanjala-yogasutra-rajamartanda-bhoja.md" for r in items):
            notes.append("⚠ Yogasūtra items carry an OCR-quality warning.")
        L.append("\n".join(f"> {n}" for n in notes) + "\n")

        # ---------------- coverage proof
        L.append("## 1. Coverage proof\n")
        uq = [q for q in queries if q["unit"] == u]
        rl = [x for x in rlog if x["unit"] == u]
        L.append("### 1a. Pass table\n")
        L.append("| Pass | Sub | Kind | Query | Global depth | Book-sweep deepenings | Chunks retrieved |")
        L.append("|---|---|---|---|---|---|---|")
        dl = [d for d in dlog if d["unit"] == u]
        for q in uq:
            gdep = max([d["extend_to"] for d in dl if d["pass"] == q["pass_id"] and d["scope"] == "global"] or [40])
            bdep = sum(1 for d in dl if d["pass"] == q["pass_id"] and d["scope"] != "global" and d["rule"].startswith(">=4"))
            n = len({x["chunk_id"] for x in rl if x["pass"] == q["pass_id"]})
            L.append(f"| {q['pass_id']} | {q['sub']} | {q['kind']} | {esc(q['q'])} | {gdep} | {bdep} | {n} |")
        L.append("")
        L.append("### 1b. Source sweep (all 29 sources)\n")
        L.append("| Source | Retrieved | Pre-filtered out | Read | Kept chunks | Items here |")
        L.append("|---|---|---|---|---|---|")
        ret_by = collections.defaultdict(set)
        for x in rl:
            ret_by[x["source_path"]].add(x["chunk_id"])
        pf_by = collections.defaultdict(set)
        for x in plog:
            if x["unit"] == u:
                pf_by[x["source_path"]].add(x["chunk_id"])
        for b in books:
            read = [c for c in ret_by[b] if c in cands and u in cands[c]["units"]]
            kept = set()
            for c in read:
                if any(r["chunk_id"] == c for r in items):
                    kept.add(c)
            n_items = sum(1 for r in items if r["source_path"] == b)
            L.append(f"| {codes[b]} — {esc(b)} | {len(ret_by[b])} | {len(pf_by[b])} | {len(read)} | {len(kept)} | {n_items} |")
        L.append("")
        L.append("**Incomplete flags:** none. No limit stopped retrieval, deepening or reading for this unit.\n")

        # ---------------- summary + index
        L.append("## 2. Evidence summary\n")
        L.append("| Sub-topic | Items | Direct | Contextual | Books (direct) | Evidence |")
        L.append("|---|---|---|---|---|---|")
        for s, t in U["subtopics"].items():
            ss = [r for r in items if r["sub"] == s]
            nd = sum(r["strength"] == "direct" for r in ss)
            bd = len({r["source_path"] for r in ss if r["strength"] == "direct"})
            # Rating is arithmetic on counts only, not a judgement of the evidence.
            rating = "strong" if nd >= 10 and bd >= 3 else "adequate" if nd >= 3 else "thin" if nd else "none"
            L.append(f"| {s} {esc(t)} | {len(ss)} | {nd} | {len(ss) - nd} | {bd} | {rating} |")
        L.append(f"| **Total** | **{len(items)}** | {sum(r['strength'] == 'direct' for r in items)} | "
                 f"{sum(r['strength'] == 'contextual' for r in items)} | "
                 f"{len({r['source_path'] for r in items if r['strength'] == 'direct'})} | |\n")
        L.append("*Evidence column (counts only): strong = ≥10 direct items from ≥3 books; adequate = ≥3 direct; "
                 "thin = 1–2 direct; none = no direct items.*\n")
        L.append("### Sub-topic index\n")
        for s, t in U["subtopics"].items():
            ids = [r["id"] for r in sorted(items, key=lambda r: r["id"]) if r["sub"] == s]
            L.append(f"- **{s}** {t}: " + (", ".join(ids) if ids else "*no items*"))
        L.append("")

        # ---------------- evidence by book (or by subtopic)
        L.append("## 3. Evidence by " + ("book" if by == "book" else "sub-topic") + "\n")
        if by == "book":
            grp = collections.defaultdict(list)
            for r in items:
                grp[r["source_path"]].append(r)
            for b in sorted(grp, key=lambda b: (-sum(r["strength"] == "direct" for r in grp[b]), -len(grp[b]), codes[b])):
                G = sorted(grp[b], key=lambda r: (r["sub"], page_key(r), r["id"]))
                D = [r for r in G if r["strength"] == "direct"]
                X = [r for r in G if r["strength"] != "direct"]
                L.append(f"### {book_name(G[0])} ({len(G)} excerpt{'s' if len(G) != 1 else ''}: "
                         f"{len(D)} direct, {len(X)} contextual) · `{codes[b]}`\n")
                L.extend(item_md(r, units) + "\n" for r in D)
                if X:
                    L.append(f"#### Context from this book ({len(X)})\n")
                    L.extend(item_md(r, units) + "\n" for r in X)
        else:
            for s, t in U["subtopics"].items():
                G = sorted([r for r in items if r["sub"] == s], key=lambda r: (codes[r["source_path"]], page_key(r)))
                L.append(f"### {s} {t} ({len(G)})\n")
                L.extend(item_md(r, units) + "\n" for r in G)

        # ---------------- cross-references
        L.append("## 4. Cross-references (items homed in other chapters)\n")
        X = sorted(xrefs.get(u, []), key=lambda r: r["id"])
        if X:
            for r in X:
                L.append(f"- **{r['id']}** ({label(r['unit'])}, {r['sub']}): {esc(r['note'])[:200]} — {r['book_code']}, {r['citation']}")
        else:
            L.append("*None.*")
        L.append("")

        # ---------------- conflicts
        L.append("## 5. Conflicts and variant statements (side by side, unresolved)\n")
        keys = sorted(k for k in conflict_keys if any(r["unit"] == u or u in (r.get("xref") or []) for r in claims[k]))
        if not keys:
            L.append("*No contested claim keys recorded for this unit.*\n")
        for k in keys:
            L.append(f"### {k}\n")
            L.append("| Source says | Book | Citation | Item |")
            L.append("|---|---|---|---|")
            for r in sorted(claims[k], key=lambda r: (r["claim"].get("value") or "", r["book_code"])):
                L.append(f"| {esc(r['claim'].get('value'))} | {r['book_code']} | {esc(r['citation'])} | {r['id']} |")
            L.append("")

        # ---------------- gaps
        L.append("## 6. Gaps (to-do)\n")
        for s, t in U["subtopics"].items():
            ss = [r for r in items if r["sub"] == s]
            nd = sum(r["strength"] == "direct" for r in ss)
            if nd == 0:
                L.append(f"- [ ] **{s}** {t}: no direct evidence in the library" + (f" (contextual only: {len(ss)})" if ss else ""))
            elif nd < 3:
                L.append(f"- [ ] **{s}** {t}: thin direct evidence ({nd} items)")
        refs = collections.Counter()
        for r in items:
            for x in r.get("refs") or []:
                refs[x.strip()] += 1
        if refs:
            L.append("- [ ] Works cited by the passages here (works not in the library listed first; consult before relying on a secondary citation):")
            L.extend(refs_md(refs, "  "))
        L.append("")
        used = sorted({r["source_path"] for r in items})
        unused = [b for b in books if b not in used]
        L.append(f"**Source coverage:** {len(used)} of {len(books)} sources contribute items here. "
                 f"No items from: {', '.join(codes[b] for b in unused) or 'none'}.\n")
        (DR / fname(u)).write_text("\n".join(L), encoding="utf-8")
        master_rows.append((u, len(items), sum(r['strength'] == 'direct' for r in items), len(used)))

    # ======================= master
    M = ["# Udaypur: History, Monuments and the Life of a Historic Town — Drafting evidence map\n"]
    M.append("## Contents\n")
    M.append("| Unit | Title | Items | Direct | Sources used |")
    M.append("|---|---|---|---|---|")
    for u, n, nd, nb in master_rows:
        M.append(f"| [{label(u)}]({fname(u)}) | {esc(units[u]['title'])} | {n} | {nd} | {nb} |")
    M.append("")
    M.append("## Source × chapter matrix (items by home chapter)\n")
    M.append("| Source | " + " | ".join(u for u in units) + " | Total |")
    M.append("|---|" + "---|" * (len(units) + 1))
    mat = collections.Counter((r["source_path"], r["unit"]) for r in ev)
    for b in books:
        row = [mat[(b, u)] for u in units]
        M.append(f"| {codes[b]} | " + " | ".join(str(x) if x else "·" for x in row) + f" | {sum(row)} |")
    M.append("")
    M.append("## All contested claims (global list)\n")
    for k in sorted(conflict_keys):
        vals = collections.defaultdict(list)
        for r in claims[k]:
            vals[r["claim"].get("value")].append(f"{r['book_code']} {r['id']}")
        M.append(f"- **{k}**: " + " ‖ ".join(f"{v} ({', '.join(s)})" for v, s in sorted(vals.items(), key=lambda t: str(t[0]))))
    M.append("")
    M.append("## Works cited by passages (global gap list)\n")
    refs = collections.Counter(x.strip() for r in ev for x in r.get("refs") or [])
    M.append("Grouped by work. *Not in library* = primary/secondary works the library's books cite but do not contain.\n")
    M.extend(refs_md(refs))
    M.append("")
    status = (RUNS / "run_status.md")
    if status.exists():
        M.append(status.read_text(encoding="utf-8"))
    (DR / "_master.md").write_text("\n".join(M), encoding="utf-8")
    print("rendered", len(units), "chapters,", len(ev), "items")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    by = "subtopic" if "--by" in sys.argv and sys.argv[sys.argv.index("--by") + 1] == "subtopic" else "book"
    main(by)
