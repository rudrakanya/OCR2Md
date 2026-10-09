"""Re-run the Stage 1A retrieval tests (KB_AUDIT.md §4) against the Stage 2 KB.

    python kb3/eval_chapter_queries.py [--dense] > kb3/eval_results.md
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kb3_query import search  # noqa: E402

TESTS = [  # (chapter, query, profile) — the same intents as the 1A audit
    ("C2", "Betwa river catchment rainfall monsoon streamflow", "evidence"),
    ("C3", "geology sandstone hills caves mesa butte Udaypur", "evidence"),
    ("C6", "Udayaditya founded Udaypur temple tank 1059 1080", "evidence"),
    ("C7", "Udayesvara temple Bhumija plan shikhara sculpture", "evidence"),
    ("C8", "inscriptions of Udaypur serpentine grammar prasasti", "evidence"),
    ("C9", "fortification wall gates stepwell baoli mosque Udaypur", "evidence"),
    ("C13", "legend folklore story told by villagers Udaypur", "prose"),
    ("C14", "Iltutmish Tughluq Mughal conquest decline Vidisha Udaypur", "evidence"),
    ("C15", "Archaeological Survey protection repairs conservation Udaypur temple", "evidence"),
    ("C16", "present-day village life Udaypur lanes panchayat people", "prose"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dense", action="store_true")
    a = ap.parse_args()
    print("# Stage 2 retrieval check: the Stage 1A chapter queries, top 5\n")
    for ch, q, prof in TESTS:
        print(f"## {ch}: \"{q}\" (profile {prof})\n")
        print("| # | chunk | type / status | flags | text |\n|---|---|---|---|---|")
        for i, r in enumerate(search(q, ch, 5, prof, a.dense), 1):
            fl = [t for t in r["tags"] if t in ("folklore", "opinion", "llm_regenerated", "ai_derived", "udaypur_specific")]
            if r["contested_claims"]:
                fl.append("contested")
            t = re.sub(r"\s+", " ", r["text"])[:150].replace("|", "/")
            print(f"| {i} | {r['chunk_id']} | {r['source_type']} / {r['epistemic_status']} | {', '.join(fl)} | {t} |")
        print()


if __name__ == "__main__":
    main()
