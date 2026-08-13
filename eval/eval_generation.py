#!/usr/bin/env python3
"""
eval/eval_generation.py — generation metrics (§4.3).

    faithfulness           atomic claims entailed by the retrieved pack. The
                           primary metric, and the one v1 could not report.
    citation correctness   does the E-id on a sentence actually support it?
                           Mechanically checkable, because citations resolve
                           from passage ids rather than being written by a model.
    citation completeness  fraction of factual sentences carrying any citation
    answer relevance       does the section address its sub-topic question?
    ungrounded-term rate   v1's check, retained as a cheap tripwire

§4.3's discipline is followed literally: the cheap deterministic checks run
first, and only what needs a judge gets one. Citation correctness, completeness,
ungrounded terms, truncation and repetition are all mechanical — running an LLM
over them would cost money to produce a worse answer.

Usage:
    python -m eval.eval_generation --dir chapter_drafts
    python -m eval.eval_generation --chapter 6 -v
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CFG                                              # noqa: E402
from console import use_utf8                                        # noqa: E402
from entities import EntityIndex                                    # noqa: E402
from llm import complete_json, get_client                           # noqa: E402
from verify import ungrounded_terms, verify_section                 # noqa: E402

EVID = Path("book/_evidence")
RESULTS = Path("eval/results")

_CITE_RE = re.compile(r"\[E(\d+)\]")
_NOTE_RE = re.compile(r"\[\^(\d+)\]|\[(\d+)\]")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-ɏ])")


def sentences(text):
    body = text.split("## Notes")[0]
    body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)
    return [s.strip() for s in _SENT_SPLIT.split(body) if len(s.strip()) > 40]


def citation_metrics(text, byid, client=None, model=None, judge=True):
    """Completeness (mechanical) and correctness (needs a judge, batched)."""
    sents = sentences(text)
    cited, uncited = [], []
    for s in sents:
        ids = _CITE_RE.findall(s) or [m.group(1) or m.group(2) for m in _NOTE_RE.finditer(s)]
        (cited if ids else uncited).append((s, ids))

    factual_uncited = [s for s, _ in uncited
                       if re.search(r"\d|[A-ZĀĪŪŚṢṆṬḌṄÑṚḤṂ][a-zāīūśṣṇṭḍṅñṛḥṃ]{2,}", s)]
    completeness = len(cited) / len(sents) if sents else 1.0

    out = {"n_sentences": len(sents), "n_cited": len(cited),
           "citation_completeness": round(completeness, 4),
           "uncited_factual_sentences": len(factual_uncited)}

    if not judge or not client or not cited:
        return out

    # Only sentences that actually carry a citation can have a wrong one.
    sample = cited[:60]
    pairs = []
    for i, (s, ids) in enumerate(sample):
        psg = [byid[f"E{n}"]["text"][:900] for n in ids if f"E{n}" in byid]
        if psg:
            pairs.append({"i": i, "sentence": s[:600], "passages": psg})
    if not pairs:
        out["citation_correctness"] = None
        return out
    msgs = [{"role": "system", "content":
             "For each item, decide whether the cited passages support the sentence. Judge only "
             "what the passages say. Return JSON only: "
             '{"results":[{"i":0,"supports":true}]}'},
            {"role": "user", "content": json.dumps(pairs, ensure_ascii=False)[:60000]}]
    try:
        data = complete_json(client, model, msgs, max_tokens=1500, temperature=0.0, quiet=True)
        got = {int(r["i"]): bool(r.get("supports")) for r in data.get("results", [])}
        checked = [i for i in range(len(pairs)) if pairs[i]["i"] in got or i in got]
        vals = [got.get(p["i"], None) for p in pairs]
        vals = [v for v in vals if v is not None]
        out["citation_correctness"] = round(sum(vals) / len(vals), 4) if vals else None
        out["n_citations_checked"] = len(vals)
    except Exception:                                   # noqa: BLE001
        out["citation_correctness"] = None
    return out


def relevance(text, questions, client, model):
    """Does the prose address the questions it was written to answer?"""
    if not questions:
        return None
    msgs = [{"role": "system", "content":
             "Score 0-100 how fully this chapter addresses each research question. 0 means the "
             "question is not addressed at all. Return JSON only: "
             '{"scores":[{"i":0,"s":80}]}'},
            {"role": "user", "content":
             f"QUESTIONS:\n{json.dumps(list(enumerate(questions)), ensure_ascii=False)}\n\n"
             f"CHAPTER (excerpt):\n{text[:30000]}"}]
    try:
        data = complete_json(client, model, msgs, max_tokens=900, temperature=0.0, quiet=True)
        vals = [float(d["s"]) / 100 for d in data.get("scores", [])]
        return round(sum(vals) / len(vals), 4) if vals else None
    except Exception:                                   # noqa: BLE001
        return None


def evaluate_chapter(n, path, client, model, entities, judge=True, deep=False):
    pack_path = EVID / f"ch{n:02d}.json"
    if not pack_path.exists():
        return None
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    passages = [p for s in pack["subtopics"] for p in s["passages"]]
    byid = {p["id"]: p for p in passages}
    text = Path(path).read_text(encoding="utf-8")

    rec = {"chapter": n, "file": str(path), "words": len(text.split())}

    # -- mechanical first (§4.3) --
    rec["ungrounded_terms"] = len(ungrounded_terms(text, passages, entities))
    rec["truncated"] = bool(text.rstrip() and not text.rstrip()[-1] in ".!?\"')]}")
    rec["gaps"] = text.count(CFG.verify.gap_marker)
    rec["unresolved_eids"] = len(set(_CITE_RE.findall(text.split("## Notes")[0])))
    rec.update(citation_metrics(text, byid, client, model, judge))

    if judge:
        rec["answer_relevance"] = relevance(
            text, [s["question"] for s in pack["subtopics"]], client, model)
    if deep:
        rep = verify_section(client, text, passages, entities=entities, model=model)
        rec["faithfulness"] = round(rep.rate, 4)
        rec["claims_checked"] = rep.checked
        rec["unsupported"] = len(rep.unsupported)
        rec["contradicted"] = len(rep.contradicted)
    return rec


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Generation metrics for drafted chapters")
    ap.add_argument("--dir", default="chapter_drafts")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--out")
    ap.add_argument("--no-judge", action="store_true", help="mechanical checks only (free)")
    ap.add_argument("--deep", action="store_true",
                    help="full claim-level faithfulness (slow, the primary metric)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    paths = []
    for p in sorted(Path(args.dir).glob("chapter-*.md")):
        m = re.search(r"chapter-(\d+)", p.name)
        if m and (args.chapter is None or int(m.group(1)) == args.chapter):
            paths.append((int(m.group(1)), p))
    if not paths:
        raise SystemExit(f"no chapter-NN.md in {args.dir}")

    client = None if args.no_judge else get_client()
    entities = EntityIndex.load()
    rows = []
    print(f"{'ch':>3s} {'words':>7s} {'ungr':>5s} {'gaps':>5s} {'cite%':>6s} "
          f"{'citeOK':>7s} {'relev':>6s} {'faith':>6s}")
    print("-" * 60)
    for n, p in paths:
        r = evaluate_chapter(n, p, client, CFG.eval.judge_model, entities,
                             judge=not args.no_judge, deep=args.deep)
        if not r:
            print(f"{n:3d}  (no evidence pack)"); continue
        rows.append(r)
        print(f"{n:3d} {r['words']:7,} {r['ungrounded_terms']:5d} {r['gaps']:5d} "
              f"{r['citation_completeness'] * 100:5.0f}% "
              f"{(r.get('citation_correctness') or 0) * 100:6.0f}% "
              f"{(r.get('answer_relevance') or 0) * 100:5.0f}% "
              f"{(r.get('faithfulness') or 0) * 100:5.0f}%")

    if rows:
        def avg(k):
            v = [r[k] for r in rows if r.get(k) is not None]
            return round(sum(v) / len(v), 4) if v else None
        summary = {"n_chapters": len(rows),
                   "ungrounded_total": sum(r["ungrounded_terms"] for r in rows),
                   "gaps_total": sum(r["gaps"] for r in rows),
                   "truncated": sum(1 for r in rows if r["truncated"]),
                   "citation_completeness": avg("citation_completeness"),
                   "citation_correctness": avg("citation_correctness"),
                   "answer_relevance": avg("answer_relevance"),
                   "faithfulness": avg("faithfulness")}
        print(f"\n{json.dumps(summary, indent=1)}")
        out = Path(args.out) if args.out else RESULTS / f"generation_{CFG.hash()}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"config_hash": CFG.hash(), "summary": summary,
                                   "per_chapter": rows}, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        print(f"-> {out}")


if __name__ == "__main__":
    main()
