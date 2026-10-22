"""One-off: curated claim tags for Chapter 1 pilot items (the pilot schema had no claim field).

Keyed by (chunk_id, first 60 chars of the normalised quote) so tags survive id renumbering.
Values are what each source says, never a resolution. Writes drafting/_runs/pilot_claims.json,
which assemble.py applies to pilot items.
"""
import json
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
FD = "temple foundation/consecration date"
RD = "Udayāditya: reign dates"
RB = "Udayāditya: relation to Bhoja"
PR = "Udaipur praśasti: location / date / reliability"
TF = "town founder / foundation"
TB = "temple builder"
SL = "temple survival legend"
DL = "distance / location of Udaypur"
POP = "population of Udaypur"
LU = "Lūṇapasāka record: date"
TK = "Udayasamudra tank: identification"
PF = "palace founder"
IC = "inscription count at Udaypur"
BC = "brass cover of the liṅga: donor"
BM = "Bedni/Berni Mata legend"
T = {
 "C01-ARTPAR-005": (FD, "construction begun Saṃvat 1116 (OCR garbled)"),
 "C01-BHOJA-TIMES-001": (TB, "Paramāra king Udayāditya"),
 "C01-BHOJA-TIMES-010": (RD, "c. 1010–1087 (table)"),
 "C01-CII-008": (PR, "undated"),
 "C01-CII-010": (LU, "1173 A.C."),
 "C01-CII-012": (TB, "a king of the Nēmaka (feudatory) dynasty placed in charge of Udaipur (editor's reading)"),
 "C01-CII-014": (RB, "16th-c. genealogy (son of Gyātā, grandson of Gōndala), rejected by the editor"),
 "C01-CII-015": (PR, "undated"),
 "C01-GANGULY-002": (TK, "founded by Udayāditya per an inscription in the temple"),
 "C01-GANGULY-004": (DL, "thirty miles north of Bhilsa"),
 "C01-GANGULY-006": (PR, "about 1072 A.D. (reign of Udayāditya)"),
 "C01-GANGULY-008": (PR, "undated; early part of the reign"),
 "C01-GANGULY-009": (PR, "lying in front of the Nīlakaṇṭheśvara temple"),
 "C01-GANGULY-010": (LU, "1172 A.D."),
 "C01-GANGULY-013": (SL, "Muhammad Tughluq gunpowder story (1325)"),
 "C01-GANGULY-014": (SL, "Aurangzeb, returning from the Deccan"),
 "C01-GANGULY-020": (FD, "1059 per a fragmentary 1513 record, 'perfunctorily executed'"),
 "C01-GANGULY-021": (FD, "1059 (author's hypothesis)"),
 "C01-GANGULY-023": (RB, "feudatory line ruling at Udayapur (author's inference)"),
 "C01-GANGULY-024": (TF, "Udayāditya, per a contemporary inscription; the legend called a myth"),
 "C01-GANGULY-025": (FD, "1080 = repair of the flag-staff"),
 "C01-GANGULY-026": (RD, "1059–1086"),
 "C01-GAZ-003": (TF, "Udayāditya, latter half of the 11th century"),
 "C01-GAZ-004": (TK, "excavated by Udayāditya; ruins seen a short distance away"),
 "C01-GAZ-007": (DL, "13 km from Basoda; 55 km NE of Vidisha"),
 "C01-GAZ-008": (DL, "nearest station Bareth, 6.5 km west"),
 "C01-GAZ-009": (POP, "928 and 1,619 (both given for 1901); 2,025 (1971)"),
 "C01-GAZ-010": (LU, "1173 A.D., attributed to Udayāditya"),
 "C01-GAZ-015": (RD, "before 1080 to 1086"),
 "C01-GAZ-016": (FD, "begun V.S. 1116 (1059); flag-staff erected 1080"),
 "C01-GEOHER-003": (POP, "6,383 (2011 census)"),
 "C01-GEOHER-006": (PR, "in Gwalior Museum; gives 1059 CE"),
 "C01-GEOHER-007": (PF, "said to be Udayāditya"),
 "C01-GEOHER-008": (TF, "Udayāditya in 1059 CE, after defeating a native chief of Bhrangarajpur (legend)"),
 "C01-GEOHER-013": (BM, "a dancer at the court of King Udayāditya"),
 "C01-GEOHER-021": (TK, "Udaysagar Talab, built by Udayāditya in 1059 CE"),
 "C01-HARDY-004": (FD, "founded 1059, consecrated 1080"),
 "C01-INTACH-001": (TF, "Parmar king Udayāditya"),
 "C01-INTACH-005": (POP, "6,383 (villageinfo.in)"),
 "C01-INTACH-006": (BC, "commander Bappa Saheb (Gwalior state)"),
 "C01-JAGTA-EN-002": (TB, "Maharaj Udayāditya"),
 "C01-JAGTA-EN-008": (DL, "seventy km from Vidisha"),
 "C01-JAGTA-EN-009": (POP, "about eight thousand"),
 "C01-JAGTA-EN-017": (PF, "Auliya Ibn Abdul Samad under Jahangir (per a farman translation)"),
 "C01-JAGTA-EN-018": (FD, "oldest Paramāra inscription at Udaipur is of 1080"),
 "C01-JAGTA-EN-019": (PR, "found in the temple courtyard; kept in the Gwalior museum"),
 "C01-JAGTA-EN-021": (IC, "11 (in this series)"),
 "C01-JAGTA-EN-023": (IC, "around a hundred"),
 "C01-JAGTA-EN-026": (PF, "Jahangir (claim reported by the author)"),
 "C01-JAGTA-EN-033": (BM, "danced on a thread across the reservoir; someone broke it"),
 "C01-JAGTA-EN-045": (FD, "three years' construction"),
 "C01-JAGTA-EN-046": (FD, "V.S. 1137 = 30 March 1080"),
 "C01-JAGTA-EN-047": (FD, "more than twenty years' construction"),
 "C01-JAGTA-EN-048": (FD, "V.S. 1116 / Śaka 981 = 1059 CE (another inscription)"),
 "C01-JAGTA-EN-049": (RB, "son of 'Pata'/'Jnata' (Gandal → Pata genealogy)"),
 "C01-JAGTA-EN-050": (TF, "Udayāditya; no earlier Paramāra inscription, so a new town"),
 "C01-JAGTA-EN-051": (TB, "son of a feudatory (name unclear)"),
 "C01-JAGTA-EN-052": (PR, "undated; time of Udayāditya"),
 "C01-JAGTA-EN-053": (RD, "1070–1093"),
 "C01-JAGTA-HI-002": (IC, "20+ on the three doorways"),
 "C01-JAGTA-HI-005": (SL, "defended by Udaypur's ancestors (Narayan Vyas)"),
 "C01-JAGTA-HI-008": (TK, "Udaya Samudra measured by the INTACH team"),
 "C01-JAGTA-HI-011": (RB, "'bandhu' not taken to mean brother (H.C. Ray)"),
 "C01-KRAM-1-001": (FD, "1059–1080 (plan caption)"),
 "C01-KRAM-2-002": (RD, "c. 1059–1087"),
 "C01-MADHYABHARAT-001": (TF, "Udayāditya founded town, temple and tank, named after himself"),
 "C01-MADHYABHARAT-002": (DL, "4 miles east of Bareth; about 8 miles from Basoda"),
 "C01-MADHYABHARAT-005": (SL, "Aurangzeb legend vs Mohammad Tughlaq (Patil)"),
 "C01-MADHYABHARAT-011": (RD, "1058–1087"),
 "C01-MADHYABHARAT-012": (FD, "commenced V.S. 1116 (1059); flag-staff V.S. 1137 (1080)"),
 "C01-MADHYABHARAT-013": (BC, "Khande Rao Appaji, V.S. 1841 (1775)"),
 "C01-PANDE-001": (TF, "Udayāditya"),
 "C01-PANDE-003": (SL, "Aurangzeb ordered demolition (Beglar's record)"),
 "C01-PANDE-005": (SL, "Muhammad Tughlaq, 1325 (local tradition)"),
 "C01-PANDE-011": (BC, "Khanderao Appaji, 1775 CE"),
 "C01-PARTEMPLES-005": (FD, "flag hoisted 1080"),
 "C01-PARTEMPLES-006": (FD, "completed 1080"),
 "C01-RAJABHOJ-EN-003": (LU, "1171 CE (inscription of V.S. 1229)"),
 "C01-SERPENT-001": (FD, "temple and tank founded 1080"),
 "C01-SERPENT-003": (FD, "built around 1080"),
}


def main():
    ev = {}
    for l in (ROOT / "drafting" / "_evidence_log.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        ev[r["id"]] = r
    out = []
    for i, (k, v) in T.items():
        r = ev[i]
        assert r["origin"].startswith("pilot"), i
        out.append({"chunk_id": r["chunk_id"], "quote_start": " ".join(r["quote"].split())[:60],
                    "claim": {"key": k, "value": v}, "tagged_by": "orchestrator (pilot schema had no claim field)"})
    (ROOT / "drafting" / "_runs" / "pilot_claims.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(out), "pilot claim tags")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
