#!/usr/bin/env python3
"""
eval/goldset.py — build and validate the labelled evaluation set (§4.1).

There is no way around this: RAG metrics without labels are self-referential. An
LLM judge scoring an LLM's retrieval against an LLM's notion of relevance
measures agreement, not correctness.

So this module bootstraps candidates and then gets out of the way. It generates
questions from real chunks (so a known-relevant passage exists by construction),
writes them with `verified: false`, and reports the verified fraction loudly
until a human has been through them. Every metrics run stamps that fraction into
its results file.

Three kinds of item, all necessary:

  covered        a sub-topic the corpus genuinely supports; tests ranking
  thin           real but sparsely covered; tests the THIN path and the floor
  expected_empty a question the corpus does NOT answer; tests §3.4's guarantee
                 that a pack comes back empty rather than full of Thanjavur

The third kind is the one people skip and the one that matters most. Without it,
a configuration that quietly deletes the empty-pack guarantee scores *better* on
every other metric, because filling a pack with plausible-looking noise raises
recall and leaves precision unmeasured.

Usage:
    python -m eval.goldset --bootstrap 60      # propose items from the corpus
    python -m eval.goldset --negatives 15      # add expected_empty items
    python -m eval.goldset --status            # how much is human-verified
    python -m eval.goldset --review            # walk unverified items one by one
"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from book_outline import CHAPTERS                                    # noqa: E402
from config import CFG                                              # noqa: E402
from console import use_utf8                                        # noqa: E402
from kb_store import KBStore                                        # noqa: E402
from llm import complete_json, get_client, parallel                 # noqa: E402

GOLD = Path("eval/goldset.json")

GEN_SYSTEM = """You write evaluation questions for a retrieval system serving a scholarly history \
of the Udayeśvara (Nīlakaṇṭheśvara) temple at Udaypur, Vidisha district, and the Paramāra dynasty \
of Malwa.

You will be given one passage from the corpus. Write ONE research question that this passage \
genuinely helps answer, and list the specific facts the passage supplies.

Rules:
- The question must be answerable from the passage — but phrased as a researcher would ask it, \
NOT as a restatement of the passage's wording. Someone who had never seen this passage should be \
able to ask it.
- Do not use pronouns that depend on the passage ("this temple"); name things.
- `reference_facts` must be short, checkable statements drawn ONLY from the passage.
- If the passage is boilerplate, a table of contents, a bibliography or OCR noise, return \
{"skip": true} instead.

Return JSON only:
{"question": "...", "reference_facts": ["...", "..."], "difficulty": "covered|thin"}"""

NEG_SYSTEM = """You write NEGATIVE evaluation questions: questions that a researcher might \
plausibly ask of a history of the Udayeśvara temple at Udaypur and the Paramāra dynasty of Malwa, \
but which the following corpus CANNOT answer.

The corpus consists of: %s

A good negative question is:
- in the right general field (Indian temple architecture, medieval Indian dynastic history, the \
Betwa region), so it is not trivially rejected;
- specific about something genuinely outside the corpus — a different region's monuments, a \
period the corpus does not cover, a category of evidence nobody collected (excavation \
stratigraphy, radiocarbon dates, pilgrim numbers, modern visitor statistics);
- NOT nonsense. "Norwegian salmon exports" tests nothing. The point is to catch a retrieval \
system that fills a pack with confident, on-field, off-topic material.

Return JSON only: {"questions": [{"question": "...", "why_absent": "..."}]}"""


def load(path=GOLD):
    if Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {"version": 1, "items": []}


def save(data, path=GOLD):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def next_id(items):
    used = [int(i["id"].split("-")[1]) for i in items if i.get("id", "").startswith("G-")]
    return f"G-{max(used, default=0) + 1:03d}"


def bootstrap(n, store, client, model, seed=7):
    """Propose `n` items from real chunks, spread across sources and chapters."""
    rows = store.db.execute(
        "SELECT rowid, source, trail, text FROM chunks WHERE length(text) > 600").fetchall()
    if not rows:
        raise SystemExit("no chunks in the store — run build_kb.py first")

    # Spread across sources so the set is not dominated by the largest book.
    by_source = {}
    for r in rows:
        by_source.setdefault(r["source"], []).append(r)
    rng = random.Random(seed)
    picks, sources = [], sorted(by_source)
    while len(picks) < n * 2 and sources:
        for s in list(sources):
            pool = by_source[s]
            if not pool:
                sources.remove(s); continue
            picks.append(pool.pop(rng.randrange(len(pool))))
            if len(picks) >= n * 2:
                break

    def one(r):
        msgs = [{"role": "system", "content": GEN_SYSTEM},
                {"role": "user", "content":
                    f"SOURCE: {r['source']}\nSECTION: {r['trail']}\n\nPASSAGE:\n{r['text'][:2400]}"}]
        return r, complete_json(client, model, msgs, max_tokens=800, temperature=0.3, quiet=True)

    def failed(r, e):
        return r, {"skip": True}

    out = []
    for r, data in parallel(one, picks, workers=6, stagger=0.2, on_error=failed):
        if data.get("skip") or not data.get("question"):
            continue
        out.append({
            "chapter": None,
            "subtopic": None,
            "question": data["question"],
            "relevant_chunks": [int(r["rowid"])],
            "reference_facts": data.get("reference_facts", [])[:6],
            "expected_empty": False,
            "kind": data.get("difficulty", "covered"),
            "source_hint": r["source"],
            "verified": False,
            "notes": "bootstrapped from one passage; other passages may also be relevant — "
                     "add them during review, or Recall will read low for the wrong reason",
        })
        if len(out) >= n:
            break
    return out


def negatives(n, store, client, model):
    """Propose `n` expected_empty items — the §3.4 regression test."""
    srcs = [r["source"] for r in store.db.execute("SELECT DISTINCT source FROM chunks")]
    listing = "; ".join(s.replace(".md", "").replace("-", " ") for s in srcs)
    msgs = [{"role": "system", "content": NEG_SYSTEM % listing},
            {"role": "user", "content": f"Write {n} negative questions."}]
    data = complete_json(client, model, msgs, max_tokens=2500, temperature=0.6)
    return [{
        "chapter": None, "subtopic": None,
        "question": q["question"],
        "relevant_chunks": [],
        "reference_facts": [],
        "expected_empty": True,
        "kind": "expected_empty",
        "verified": False,
        "notes": q.get("why_absent", ""),
    } for q in data.get("questions", []) if q.get("question")][:n]


def status(data):
    items = data["items"]
    ver = [i for i in items if i.get("verified")]
    kinds = {}
    for i in items:
        kinds[i.get("kind", "?")] = kinds.get(i.get("kind", "?"), 0) + 1
    return {"total": len(items), "verified": len(ver),
            "verified_frac": len(ver) / len(items) if items else 0.0,
            "kinds": kinds}


def validate(data):
    """Structural problems that would make a metrics run lie."""
    problems = []
    seen = set()
    for i in data["items"]:
        q = (i.get("question") or "").strip()
        if not q:
            problems.append(f"{i.get('id')}: empty question")
        if q.lower() in seen:
            problems.append(f"{i.get('id')}: duplicate question")
        seen.add(q.lower())
        if i.get("expected_empty"):
            if i.get("relevant_chunks"):
                problems.append(f"{i['id']}: expected_empty but lists relevant chunks")
        elif not i.get("relevant_chunks"):
            problems.append(f"{i['id']}: no relevant chunks and not expected_empty")
    n_empty = sum(1 for i in data["items"] if i.get("expected_empty"))
    if data["items"] and n_empty < 8:
        problems.append(f"only {n_empty} expected_empty item(s) — §3.4 says 10-15. "
                        f"Without them a config that deletes the empty-pack guarantee "
                        f"scores better on every other metric.")
    return problems


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Build and validate the gold set")
    ap.add_argument("--bootstrap", type=int, help="propose N items from the corpus")
    ap.add_argument("--negatives", type=int, help="propose N expected_empty items")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--review", action="store_true", help="walk unverified items")
    args = ap.parse_args()

    data = load()

    if args.bootstrap or args.negatives:
        store, client = KBStore(), get_client()
        model = CFG.eval.judge_model
        new = []
        if args.bootstrap:
            print(f"bootstrapping {args.bootstrap} items from the corpus ...", flush=True)
            new += bootstrap(args.bootstrap, store, client, model)
        if args.negatives:
            print(f"proposing {args.negatives} expected_empty items ...", flush=True)
            new += negatives(args.negatives, store, client, model)
        for item in new:
            item["id"] = next_id(data["items"])
            data["items"].append(item)
        save(data)
        print(f"+{len(new)} items -> {GOLD}")
        print("EVERY new item is verified:false. Until a human reviews them, metrics "
              "computed on this set measure agreement with a model, not correctness.")

    if args.validate or args.bootstrap or args.negatives:
        problems = validate(data)
        if problems:
            print(f"\n{len(problems)} structural problem(s):")
            for p in problems[:20]:
                print(f"  - {p}")
        else:
            print("\nNo structural problems.")

    if args.status or args.validate or args.bootstrap or args.negatives:
        s = status(data)
        print(f"\n{s['total']} items, {s['verified']} verified "
              f"({s['verified_frac'] * 100:.0f}%)")
        for k, n in sorted(s["kinds"].items()):
            print(f"  {k:16s} {n:4d}")
        if s["verified_frac"] < 1.0:
            print(f"\n{s['total'] - s['verified']} item(s) await human review: "
                  f"python -m eval.goldset --review")

    if args.review:
        todo = [i for i in data["items"] if not i.get("verified")]
        if not todo:
            print("Everything is verified."); return
        print(f"{len(todo)} unverified item(s). For each: [y]es keep, [n] delete, "
              f"[e]dit question, [s]kip, [q]uit.\n")
        for item in todo:
            print(f"--- {item['id']}  ({item['kind']}) ---")
            print(f"Q: {item['question']}")
            if item.get("reference_facts"):
                for f in item["reference_facts"]:
                    print(f"   fact: {f}")
            if item.get("notes"):
                print(f"   note: {item['notes']}")
            try:
                ans = input("[y/n/e/s/q] > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nstopping"); break
            if ans == "q":
                break
            if ans == "n":
                data["items"] = [x for x in data["items"] if x["id"] != item["id"]]
            elif ans == "e":
                item["question"] = input("new question > ").strip() or item["question"]
                item["verified"] = True
            elif ans == "y":
                item["verified"] = True
            save(data)
        print(f"\nSaved. {status(data)['verified']} verified.")


if __name__ == "__main__":
    main()
