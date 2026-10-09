#!/usr/bin/env python
"""Step 4 evidence — do OpenAI vectors fix the English-to-Devanagari asymmetry?

    python phase4_probe.py --stores v1 v2 v2-openai

Phase 3 found that an English query could not reach the Hindi and Sanskrit
sources: RAJM (Bhoja's own Rājamārtaṇḍa), BHJ-H, TIW-H and RAJ-E never appeared
in twelve top-8 lists, while the same corpus queried in Hindi returned them at
once. That is the one defect that would justify a re-embed, so it is measured
directly rather than argued.

Each query runs against each collection with ITS OWN embedder (a collection has
exactly one vector space), and the comparison is like-for-like where it matters:
v2 and v2-openai hold identical text, so any difference between them is the
model alone. v1 is shown for continuity but differs in chunking too.

The headline number is REACH: over the English queries, how many of the four
Devanagari-script sources appear anywhere in the top-k.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "kb3" / "chroma"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"

STORES = {
    "v1": ("udaypur_kb", "local"),
    "v2": ("udaypur_kb_v2", "local"),
    "v2-openai": ("udaypur_kb_v2_openai", "openai"),
}
DEVA_SOURCES = {"RAJM", "BHJ-H", "TIW-H", "SAM"}      # Devanagari-bearing works

ENGLISH = [
    "Udayesvara temple inscription date of consecration",
    "Udayaditya accession date and reign",
    "Bhoja's own writings and authorship",
    "yoga sutra commentary attributed to Bhoja",
    "Sapta Matrka iconography niches four handed goddess",
    "bhumija temple shikhara form and latas",
    "Paramara dynasty genealogy Bhoja successors",
    "temple proportions and measurement canon",
    "Udaypur town life lanes and market",
    "Betwa river seasonal flow and rainfall",
    "stepwell baoli water structures at Udaypur",
    "sculpture on the jangha of the temple exterior",
]
HINDI = [
    "भोज का योगसूत्र भाष्य राजमार्तण्ड",
    "उदयपुर कस्बे का जीवन और बाजार",
    "मूर्ति लक्षण और प्रतिमा विज्ञान",
    "परमार वंश का इतिहास",
]


class Embedder:
    def __init__(self, kind):
        self.kind = kind
        self._l = None
        self._o = None

    def __call__(self, texts, is_query=True):
        if self.kind == "local":
            if self._l is None:
                from embed_e5 import load_model, encode
                self._l = (*load_model("intfloat/multilingual-e5-small"), encode)
            tok, model, encode = self._l
            V = encode(list(texts), tok, model, "query: " if is_query else "passage: ")
            return np.asarray(V, dtype=np.float32)
        if self._o is None:
            from openai import OpenAI
            from phase4_embed_v2 import load_key
            self._o = OpenAI(api_key=load_key())
        r = self._o.embeddings.create(model="text-embedding-3-large",
                                      input=list(texts), dimensions=1536)
        return np.asarray([d.embedding for d in r.data], dtype=np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stores", nargs="+", default=["v2", "v2-openai"],
                    choices=sorted(STORES))
    ap.add_argument("-k", type=int, default=8)
    a = ap.parse_args()

    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    code = {s["source_id"]: s.get("code") or s["source_id"] for s in reg["sources"]}

    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA))
    have = {c.name for c in client.list_collections()}

    results = {}
    for name in a.stores:
        coll, kind = STORES[name]
        if coll not in have:
            print(f"!! {coll} does not exist yet — skipping {name}")
            continue
        col = client.get_collection(coll)
        emb = Embedder(kind)
        print(f"\n{'='*74}\n{name}: {coll} ({kind}), {col.count()} vectors\n{'='*74}")
        per = {}
        for label, qs in (("english", ENGLISH), ("hindi", HINDI)):
            QV = emb(qs, is_query=True)
            rows = []
            for q, qv in zip(qs, QV):
                r = col.query(query_embeddings=[qv.tolist()], n_results=a.k,
                              include=["metadatas"])
                cs = [code.get(m.get("parent_source_id"), "?") for m in r["metadatas"][0]]
                rows.append({"q": q, "codes": cs})
                print(f"  [{label}] {q[:46]:48s} {' '.join(cs)}")
            per[label] = rows
        # reach: which Devanagari sources appear at all, across the english set
        seen_en = {c for r in per["english"] for c in r["codes"]}
        seen_hi = {c for r in per["hindi"] for c in r["codes"]}
        reach = sorted(DEVA_SOURCES & seen_en)
        slots = collections.Counter(c for r in per["english"] for c in r["codes"])
        dev_slots = sum(v for k, v in slots.items() if k in DEVA_SOURCES)
        tot = sum(slots.values())
        print(f"\n  Devanagari sources reached by ENGLISH queries: "
              f"{reach or 'NONE'}  ({len(reach)}/{len(DEVA_SOURCES)})")
        print(f"  their share of English top-{a.k} slots: {dev_slots}/{tot} "
              f"({dev_slots/max(1,tot):.1%})")
        print(f"  Devanagari sources reached by HINDI queries  : "
              f"{sorted(DEVA_SOURCES & seen_hi) or 'NONE'}")
        print(f"  distinct sources over all English queries: {len(seen_en)}")
        results[name] = {"per": per, "deva_reached_en": reach,
                         "deva_slots_en": dev_slots, "slots_en": tot,
                         "deva_reached_hi": sorted(DEVA_SOURCES & seen_hi),
                         "distinct_sources_en": len(seen_en),
                         "top_sources": slots.most_common(8)}

    if len(results) > 1:
        print(f"\n{'='*74}\nCOMPARISON\n{'='*74}")
        print(f"{'store':12s} {'Devanagari srcs reached (EN)':30s} {'EN slots':>9s} "
              f"{'distinct srcs':>13s}")
        for n, r in results.items():
            print(f"{n:12s} {str(r['deva_reached_en'] or 'none'):30s} "
                  f"{r['deva_slots_en']:>4d}/{r['slots_en']:<4d} "
                  f"{r['distinct_sources_en']:>13d}")
    p = ROOT / "kb_audit" / "phase4_probe.json"
    p.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
