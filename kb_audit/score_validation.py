"""Score the classifier against hand-labelled gold sets (keyed by text snippet).

    python kb_audit/score_validation.py kb_audit/validation_gold_round1.json [...]
"""
import collections, json, sys
from pathlib import Path

import re
norm = lambda t: re.sub(r"\s+", " ", t)
inv = [json.loads(l) for l in open(Path(__file__).parent / "classified_inventory.jsonl", encoding="utf-8")]
for path in sys.argv[1:]:
    d = json.load(open(path, encoding="utf-8"))
    ok, conf, misses = 0, collections.Counter(), []
    for it in d["items"]:
        hits = [r for r in inv if norm(it["snippet"]) in norm(r["text"])]
        if not hits:
            # absent from every chunk: stripped in pre-processing (logged)
            pred, cid = "non_claim", "(stripped)"
        else:
            r = hits[0]; cid = r["chunk_id"]
            pred = r["epistemic_status"] if r["claim_bearing"] else "non_claim"
        conf[(it["gold"], pred)] += 1
        if pred == it["gold"]:
            ok += 1
        else:
            misses.append((cid, it["gold"], pred, it["why"]))
    print(f"{path}: {ok}/{len(d['items'])} correct")
    for m in misses:
        print("   MISS", *m)
