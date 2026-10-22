"""Find chunks of a source containing a phrase; report hit/judged status for a chapter.
Usage: python drafting/_tools/twin.py C01 "<source>" "<phrase>" ["<phrase>" ...]"""
import json, sqlite3, sys
from pathlib import Path
ROOT = Path(str(Path(__file__).resolve().parents[2])); RUNS = ROOT / "drafting" / "_runs"
sys.stdout.reconfigure(encoding="utf-8")
ch, src, phrases = sys.argv[1], sys.argv[2], sys.argv[3:]
db = sqlite3.connect(f"file:{ROOT/'chroma_db'/'sidecar.sqlite3'}?mode=ro", uri=True)
H = {json.loads(l)["chunk_id"] for l in (RUNS/f"{ch}_hits.jsonl").open(encoding="utf-8")}
J = {}
for l in (RUNS/f"{ch}_judgments.jsonl").open(encoding="utf-8"):
    r = json.loads(l); J[r["chunk_id"]] = r
for p in phrases:
    for cid, pg in db.execute("select chunk_id,page_start from chunks where source_path=? and instr(text,?)>0", (src, p)):
        j = J.get(cid)
        print(f"{p[:30]!r}: {cid[:10]} p.{pg} hit={cid in H} judged={j['decision'] if j else None} {(j or {}).get('reason','')[:90]}")
