"""Phase 5 — chapter-scoped smoke tests over the ChromaDB store.

    python validate_retrieval.py > RETRIEVAL_VALIDATION.md
"""
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb3_chroma_query import search  # noqa: E402

CHAPTER_TESTS = [
    ("C1", "ancient Vidisha Besnagar Heliodorus early references"),
    ("C2", "Betwa river catchment rainfall monsoon streamflow"),
    ("C3", "geology sandstone mesa butte caves of the Udaypur hill"),
    ("C4", "Avanti Malwa Ujjain Dhara dynasties trade routes"),
    ("C5", "Bhoja's own works, learning and authorship"),
    ("C6", "Udayaditya founded Udaypur temple and tank 1059 1080"),
    ("C7", "Udayesvara temple Bhumija plan shikhara sculpture"),
    ("C8", "inscriptions of Udaypur serpentine grammar prasasti"),
    ("C9", "fortification wall gates stepwell baoli mosque"),
    ("C10", "Saiva Siddhanta ritual and the intellectual world of Malwa"),
    ("C11", "agriculture markets stone quarrying crafts economy"),
    ("C12", "communities castes dialects population of the district"),
    ("C13", "legend folklore story told by villagers"),
    ("C14", "Iltutmish Tughluq Mughal conquest and decline"),
    ("C15", "Archaeological Survey protection repairs conservation"),
    ("C16", "present-day village life lanes panchayat people"),
    ("AF", "conservation today encroachment neglect what can be done"),
]
NEW = "rajamartanda-bhoja"


def line(r):
    flags = [t.replace("tag_", "") for t in r if t.startswith("tag_") and r[t]]
    if not r["is_quotable"]:
        flags.insert(0, "NOT-QUOTABLE")
    txt = re.sub(r"\s+", " ", r["text"])[:90].replace("|", "/")
    return (f"| {r['parent_source_id']} | {r['source_type']} | {r['epistemic_status']} | "
            f"{round(r['score'], 2)} | {', '.join(flags[:3])} | {txt} |")


def main():
    P = print
    P("# Retrieval validation (Phase 5)\n")
    P("Chapter-scoped smoke tests against the Chroma collection `udaypur_kb`, "
      "run by `validate_retrieval.py`. Every query is filtered with `where={\"in_<chapter>\": True}`, "
      "so only chunks bucketed into that chapter are candidates.\n")

    P("## 1. Every chapter, top 5\n")
    per_chapter = {}
    for ch, q in CHAPTER_TESTS:
        res = search(q, ch, 5)
        per_chapter[ch] = res
        P(f"### {ch} — \"{q}\"\n")
        P("| source | type | status | score | flags | text |")
        P("|---|---|---|--:|---|---|")
        for r in res:
            P(line(r))
        P("")

    P("## 2. Does the new book reach C5 and C10?\n")
    P("| test | result |")
    P("|---|---|")
    for ch in ("C5", "C10"):
        full = search(dict(CHAPTER_TESTS)[ch], ch, 5000)
        pos = [i + 1 for i, r in enumerate(full) if r["parent_source_id"] == NEW]
        n = len([r for r in full if r["parent_source_id"] == NEW])
        P(f"| {ch} bucket contains the new book | **{n} chunks**; best rank "
          f"{pos[0] if pos else '—'} of {len(full)} on an English query |")
    hi = search("भोज के ग्रंथ, विद्वत्ता और राजमार्तण्ड टीका", "C5", 5000)
    hpos = [i + 1 for i, r in enumerate(hi) if r["parent_source_id"] == NEW]
    P(f"| C5, the same question asked in Devanagari | best rank **{hpos[0] if hpos else '—'}** of {len(hi)} |")
    src = search("Bhoja authorship works learning", "C5", 5, source=NEW)
    P(f"| C5 filtered to the new book (`--source {NEW}`) | returns {len(src)}; top: "
      f"`{src[0]['chunk_id']}` (quotable={src[0]['is_quotable']}) |")

    P("\n## 3. Does the yoga-doctrine layer stay out of unrelated chapters?\n")
    P("| chapter | new-book chunks bucketed | of which yoga-doctrine |")
    P("|---|--:|--:|")
    doctrine_leak = 0
    for ch, _ in CHAPTER_TESTS:
        got = search(None, ch, 5000, source=NEW)
        doc = [r for r in got if r.get("tag_yoga_doctrine")]
        if ch not in ("C5", "C10"):
            doctrine_leak += len(doc)
        P(f"| {ch} | {len(got)} | {len(doc)} |")
    P(f"\nYoga-doctrine chunks bucketed outside C5/C10: **{doctrine_leak}**.")

    P("\n## 4. Is the Tiwari alias fix holding (C13, C16)?\n")
    P("| chapter | Tiwari chunks in top 10 |")
    P("|---|--:|")
    for ch in ("C13", "C16"):
        res = search(dict(CHAPTER_TESTS)[ch], ch, 10, profile="prose")
        P(f"| {ch} | {sum(1 for r in res if r['parent_source_id'].startswith('tiwari-jhk'))} |")

    P("\n## 5. Is non-quotable text ever returned as quotable?\n")
    bad = 0
    tot = 0
    for ch, q in CHAPTER_TESTS:
        res = search(q, ch, 20, quotable_only=True)
        tot += len(res)
        bad += sum(1 for r in res if not r["is_quotable"] or r.get("tag_llm_regenerated") or r.get("tag_needs_recheck"))
    P(f"With `--quotable-only`, {tot} results across all chapters, of which non-quotable: **{bad}**.")

    P("\n## 6. Is the archive reachable?\n")
    import chromadb
    client = chromadb.PersistentClient(path=str(Path(__file__).resolve().parent / "kb3" / "chroma"))
    act = client.get_collection("udaypur_kb")
    arc = client.get_collection("udaypur_kb_archive")
    leaked = act.get(where={"is_archived": True}, limit=5)["ids"]
    P(f"- active collection: {act.count():,} records; archive collection: {arc.count():,} records")
    P(f"- records flagged `is_archived` inside the active collection: **{len(leaked)}**")
    P("- `kb3_chroma_query.py` names only `udaypur_kb`; the archive collection is never opened by the query path.")

    P("\n## 7. Source mix actually reaching the chapters\n")
    P("| chapter | source types in top 5 |")
    P("|---|---|")
    for ch, _ in CHAPTER_TESTS:
        c = collections.Counter(r["source_type"] for r in per_chapter[ch])
        P(f"| {ch} | {', '.join(f'{k} x{v}' for k, v in c.most_common())} |")


if __name__ == "__main__":
    main()
