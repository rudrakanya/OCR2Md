"""Build ch11/evidence_pack_v1.json: evidence_index/ch11.jsonl (Temple Economics excluded, R9) plus borrowed recalls (free)."""
import json, glob
from pathlib import Path
D = Path(__file__).resolve().parent.parent
idx = {}
for f in sorted(glob.glob(str(D / "evidence_index" / "*.jsonl"))):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            x = json.loads(l); idx.setdefault(x["id"], x)
for f in sorted(glob.glob(str(D / "ch0*" / "evidence_pack_v*.json"))):
    for x in json.load(open(f, encoding="utf-8")):
        idx.setdefault(x["id"], x)
own = [json.loads(l)["id"] for l in open(D / "evidence_index" / "ch11.jsonl", encoding="utf-8") if l.strip()]
own = [i for i in own if "TEMPLE-ECON" not in i]
BORROW = """C07-PANDE-005 C01-PANDE-012 C01-PANDE-013 C01-KB-PANDE-001 C01-KB-PANDE-002 C07-PANDE-008 C07-PANDE-009
C10-MADHYABHARAT-006 C01-PANDE-003 C01-PANDE-002 C06-JAGTA-EN-016 C05-GANGULY-012 C05-PANDE-008 C07-KRAM-1-001 C02-PANDE-001
C05-KRAM-1-034 C05-PARTEMPLES-003 C01-MADHYABHARAT-013 C01-PANDE-011 C01-INTACH-006 C01-CII-009 C01-KBN-CII-004
C06-JAGTA-EN-015 C06-JAGTA-HI-029 C06-JAGTA-HI-013 C01-SERPENT-002 C01-KB-SERPENT-001 C01-KB-JAGTA-EN-004 C01-GEOHER-005
C07-INTACH-027 C07-INTACH-028 C07-INTACH-005 C07-INTACH-006 C13-GEOHER-004 C07-GEOHER-059 C07-JAGTA-HI-065 C06-JAGTA-HI-026
C13-JAGTA-HI-021 C07-JAGTA-HI-064 C07-JAGTA-HI-042 C07-JAGTA-HI-066 C07-INTACH-026 C02-GEOHER-018 C02-GEOHER-024
C01-JAGTA-EN-022 C01-MADHYABHARAT-012 C01-KRAM-1-001 C07-JAGTA-HI-052 C02-JAGTA-EN-003 C07-GEOHER-018 C10-JAGTA-EN-021 C10-JAGTA-EN-015 C12-JAGTA-EN-003""".split()
out = [idx[i] for i in own + BORROW]
json.dump(out, open(D / "ch11" / "evidence_pack_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(own), "own +", len(BORROW), "borrowed =", len(out))
