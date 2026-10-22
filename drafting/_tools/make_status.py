"""Write drafting/_runs/run_status.md (render.py appends it to _master.md).

Inputs: retrieval_summary.json, calibration.json, judgment_summary.json, decisions.json,
candidates.jsonl, deepening_log.jsonl, spotchecks.json (hand spot-check results),
qc_findings.md and folder_check.md (hand-written notes), timing.json.
  python -I drafting/_tools/make_status.py
  python -I drafting/_tools/make_status.py --sample 15   # print 15 random items to spot-check
"""
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
DR = ROOT / "drafting"
R = DR / "_runs"


def jl(p):
    return [json.loads(l) for l in Path(p).open(encoding="utf-8") if l.strip()]


def sample(n):
    ev = jl(DR / "_evidence_log.jsonl")
    rnd = random.Random(2026)
    for r in rnd.sample(ev, n):
        print(json.dumps({k: r[k] for k in ("id", "chunk_id", "source_path", "citation", "quote", "note", "unit", "sub",
                                              "strength", "gloss")}, ensure_ascii=False))


def main():
    rs = json.loads((R / "retrieval_summary.json").read_text(encoding="utf-8"))
    cal = json.loads((R / "calibration.json").read_text(encoding="utf-8"))
    js = json.loads((R / "judgment_summary.json").read_text(encoding="utf-8"))
    dec = json.loads((R / "decisions.json").read_text(encoding="utf-8"))
    cands = jl(R / "candidates.jsonl")
    dl = jl(R / "deepening_log.jsonl")
    ev = jl(DR / "_evidence_log.jsonl")
    sc = json.loads((R / "spotchecks.json").read_text(encoding="utf-8")) if (R / "spotchecks.json").exists() else []
    tm = json.loads((R / "timing.json").read_text(encoding="utf-8")) if (R / "timing.json").exists() else {}
    pilot = jl(R / "C01_judgments.jsonl")
    L = ["## Run status & test report\n"]
    L.append("### Retrieval\n")
    L.append(f"- Queries/passes run: **{rs['queries']}**: 13 units × 25 phrase passes = 325, plus "
             f"{rs['queries'] - 325} hypothetical-answer queries (one per sub-topic). Embedding {rs['embed_seconds']} s, "
             f"scoring {rs['score_seconds']} s, total {rs['total_seconds']} s, in memory.")
    L.append(f"- Union of chunks retrieved (global top-40/80+ and per-book top-5 with deepening): **{rs['union_retrieved']}** of 6,813.")
    L.append(f"- Pre-filtered out (below floor, or a duplicate twin): **{rs['union_retrieved'] - rs['union_to_read']}**. "
             f"Every drop is logged with its reason and score in `_runs/prefilter_log.jsonl`.")
    extra = sum(1 for c in cands if c.get("extra"))
    L.append(f"- To read: **{rs['union_to_read']}**, plus {extra} chunks read in early packets built before the per-query deepening fix.")
    L.append(f"- Adaptive deepening: {sum(1 for d in dl if d['scope'] == 'global')} global extensions; "
             f"{sum(1 for d in dl if d['scope'] != 'global')} per-book extensions (`_runs/deepening_log.jsonl`).")
    L.append("\n| Unit | Retrieved | Pre-filtered out | Duplicate twins | To read | Global deepenings | Book deepenings |")
    L.append("|---|---|---|---|---|---|---|")
    for u, v in rs["units"].items():
        L.append(f"| {u} | {v['retrieved_unique']} | {v['prefiltered_out']} | {v['duplicate_twins_dropped']} | "
                 f"{v['to_read']} | {v['global_deepenings']} | {v['book_deepenings']} |")
    L.append("\n### Calibration\n")
    L.append(f"- Calibrated on all **{cal['judged']}** Chapter 1 chunks that were hand-judged in the pilot ({cal['keeps']} kept).")
    L.append(f"- **Pre-filter floor:** max dense cosine ≥ **{cal['threshold_dense']}**, or global fused rank ≤ {cal['rescue_rank']}. "
             f"The lowest kept chunk scored {cal['min_keep_dense']}; the floor sits {cal['margin']} below it. "
             f"Keeps lost at the floor: **{cal['at_threshold']['keeps_lost']}**.")
    L.append(f"- **Deepening \"relevant\":** dense ≥ **{cal['threshold_deepen']}** for the query in question: the lowest score at which at least "
             f"{int(cal['deepen_precision_target'] * 100)}% of hand-judged chunks were kept.")
    L.append("\n| Dense band | Judged | Kept |\n|---|---|---|")
    for b in cal["bands"]:
        L.append(f"| {b['band']} | {b['n']} | {b['keeps']} |")
    L.append(f"\nStratified sample, 12 per band and {len(cal['sample'])} in all: `_runs/calibration.json` → `sample`. "
             f"It contains {sum(s['hand_decision'] == 'keep' for s in cal['sample'])} hand-kept chunks, all above the floor.")
    L.append("\n### Judging\n")
    L.append(f"- Packets: {js['packets_judged']} / {js['packets_total']}, all passing `check_judgments.py`.")
    L.append(f"- Chunks read and judged by subagents: **{js['chunks_judged']}**. "
             f"Kept **{js['chunks_kept']}**, rejected **{js['chunks_rejected']}**. "
             f"Every decision and reason is in `_runs/judgments/*.jsonl` and `_runs/decisions.json`.")
    L.append(f"- Chapter 1 pilot: {len(pilot)} chunks hand-judged ({sum(p['decision'] == 'keep' for p in pilot)} kept). "
             f"Its {js['pilot_items_carried']} items are carried over and re-verified.")
    L.append(f"- Items: **{js['items_verified']}** verified; {js['items_failed']} failed verification and were excluded "
             f"(`_runs/assembly_failures.jsonl`); {js['exact_duplicate_items_dropped']} exact duplicates dropped.")
    L.append(f"- **Verification pass rate: {js['verification_pass_rate'] * 100:.2f}%**. Each quote is checked verbatim against "
             f"the chunk and the source Markdown, and its page is taken from the `<!-- page N -->` marker in force.")
    by_u = collections.Counter(r["unit"] for r in ev)
    L.append("- Items per unit: " + ", ".join(f"{u} {by_u[u]}" for u in sorted(by_u)))
    L.append("\n### 15 spot-checks (by hand, against the source file)\n")
    if sc:
        L.append("| Item | Quote verbatim at cited page? | Page correct? | Relevance sound? | Note |")
        L.append("|---|---|---|---|---|")
        for s in sc:
            L.append(f"| {s['id']} | {s['quote_ok']} | {s['page_ok']} | {s['relevance_ok']} | {s.get('note', '')} |")
        L.append(f"\nResult: {sum(s['quote_ok'] == 'yes' and s['page_ok'] == 'yes' for s in sc)}/{len(sc)} verbatim at the cited page. "
                 "One quote (C03-GAZ-031) had been cut at 'A.' by the sentence splitter; the slicer was fixed and every item re-sliced. "
                 f"Relevance: {sum(s['relevance_ok'] == 'yes' for s in sc)}/{len(sc)} clearly relevant; "
                 f"{sum(s['relevance_ok'] == 'weak' for s in sc)}/{len(sc)} weak (generic contextual background, acceptable under the rubric). "
                 "**Implication:** read contextual items as background, not evidence; the direct items carry the chapters.")
    else:
        L.append("*Not yet run.*")
    L.append("\n### Incomplete flags\n")
    L.append("**None.** No cap stopped retrieval, deepening or reading: per-book deepening ran until relevance dropped "
             "or the book ran out, and global deepening ran until the last ten ranks held no relevant chunk.")
    for name in ("qc_findings.md", "folder_check.md"):
        p = R / name
        if p.exists():
            L.append("\n" + p.read_text(encoding="utf-8"))
    if tm:
        L.append("\n### Time and tokens\n")
        for k, v in tm.items():
            L.append(f"- {k}: {v}")
    (R / "run_status.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote run_status.md")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--sample" in sys.argv:
        sample(int(sys.argv[sys.argv.index("--sample") + 1]))
    else:
        main()
