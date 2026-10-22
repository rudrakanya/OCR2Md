"""Automated rule checks over drafting/_evidence_log.jsonl -> drafting/_runs/qc_rules.json (+ printout)."""
import json, re, sys, collections
from pathlib import Path
ROOT = Path(str(Path(__file__).resolve().parents[2]))
ev = [json.loads(l) for l in (ROOT / "drafting/_evidence_log.jsonl").open(encoding="utf-8")]
DEV = re.compile(r"[\u0900-\u097F]")
RAJ = re.compile(r"\b(Mewar|Mewār|Rana|Rāṇā|Rajasthan|Rājasthān|Pichola|Rajputana|Sisodia|Chittor)\b", re.I)
SAMAR = {"Samrangana Sutradhar Vol 1.md", "Samarangan Vol 2 (a)_combined.md"}
res = collections.OrderedDict()
res["ids_unique"] = len({r["id"] for r in ev}) == len(ev)
res["samar_without_warning"] = [r["id"] for r in ev if r["source_path"] in SAMAR and "⚠" not in r["citation"]]
res["temple_econ_not_contextual"] = [r["id"] for r in ev if r["source_path"] == "Temple Economics.md" and r["strength"] != "contextual"]
LAT = re.compile(r"[A-Za-z]")
# a quote that is mainly Devanagari (more Devanagari than Latin letters) must carry a gloss;
# English passages quoting a few Hindi words do not need one
res["devanagari_without_gloss"] = [r["id"] for r in ev if len(DEV.findall(r["quote"])) > len(LAT.findall(r["quote"])) and not r.get("gloss")]
res["page_none_but_scanp_citation"] = [r["id"] for r in ev if r.get("page") is None and "scan p." in r["citation"]]
res["rajasthan_terms_for_review"] = [(r["id"], RAJ.search(r["quote"] + " " + r["note"]).group(0)) for r in ev if RAJ.search(r["quote"] + " " + r["note"])]
res["yogasutra_without_warning"] = [r["id"] for r in ev if r["source_path"].startswith("patanjala") and "⚠" not in r["note"]]
res["pande_twin_cited"] = [r["id"] for r in ev if r["source_path"].startswith("The Udayesvara Temple Art")]
(ROOT / "drafting/_runs/qc_rules.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
for k, v in res.items():
    print(k, v if isinstance(v, bool) else f"{len(v)}  {v[:12]}")
