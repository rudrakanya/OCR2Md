"""Chapter 3, draft v1 — configuration for the shared toolkit (drafting/_pipe). Set UDAY_CFG to this file."""
from pathlib import Path

CH = 3
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch03"))
SECTIONS = ["3.1", "3.2", "3.3", "3.4", "3.5"]
OUTLINE = D / "ch03_outline.md"
PACK = D / "evidence_pack_v2.json"
LOG = D / "api_log"
OUT = D / "ch03_draft_v1.md"
TITLE = "Before Udaypur: Prehistory, Early Vidisha and the Historical Landscape of Central India"
DOCX_NAME = "Chapter 3 - Before Udaypur - Draft v1 (footnoted).docx"
WMIN, WMAX, TOTAL_TARGET = 3800, 4200, 4000
BUDGET, RESERVE = 5.00, 0.90
BASELINE = None
VOICE_SRC = None
OPEN_IN = ("Chapter 2 ended on the country that produced the town — the Betwa valley's land, water and stone. "
           "Open by turning from that country to its human past: who lived, ruled and travelled here before Udaypur existed.")
CLOSE_OUT = "Chapter 4 turns to the Paramāras and the foundation of Udaypur in the eleventh century."
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Vidisha", "Besnagar", "Bhilsa"]
TIWARI_FULL_NAME = True
GAZ_MODERN_ONLY = False      # Chapter 3: the Gazetteer may carry ancient history (≤ 40% of a section's evidence, per the brief)

CONFLICTS = {}               # filled after the outline is written (see bottom)

CHAPTER_BRIEF = """You are writing Chapter 3, "Before Udaypur: Prehistory, Early Vidisha and the Historical Landscape of Central India", of a history of Udaypur (Vidisha district, Madhya Pradesh, India) — the town founded by the Paramāra king Udayāditya in the eleventh century, NOT Udaipur in Rajasthan. The chapter tells the country's human past before the town existed, and why that past made Udaypur possible or explains it. Vidisha and Central India are context for Udaypur, not the subject: every paragraph ties its material back to Udaypur's ground — its river valley, its distance from Vidisha, its roads, the sacred geography it inherited, the powers the Paramāras would inherit.

CHAPTER CANON (binding):
- Stop before the Paramāra foundation (Chapter 4). Leave temple architecture, the Bhūmija style and the Udayasamudra tank to Chapters 5 and 7, the inscriptions in detail to Chapter 6, geology and the river system to Chapter 2 (refer back in a clause).
- Ancient literature (epics, Purāṇas, Buddhist and Jain texts, Kālidāsa) gives tradition and literary memory, presented as such ("the epics place…", "in Buddhist tradition…"); archaeology and inscriptions give dated evidence; keep the two apart.
- Dates: give each as the evidence gives it; where items differ, give the range around the object.
- *Jagta Hua Kasba* (JAGTA) is testimony and the author's reflection: never the source of an ancient fact or a measurement; its pages are approximate. Its author is Vijay Manohar Tiwari: name him in full once at his first mention in the chapter, then "Tiwari"; avoid gendered pronouns.
- The district Gazetteer (GAZ) is a 1979 compilation; where it is the only source for an ancient claim, keep the claim modest.
- Temple Economics is excluded entirely."""

# ---- knowledge-base gap queries (S1 prehistory, S3 Daśārṇa/Ākara; plus Udaypur-proximal ties) — at most 25 new items
KB_IN = D / "evidence_pack.json"
KB_MAX_NEW = 25
KB_TOPIC = "Before Udaypur: prehistory, early Vidisha/Besnagar, Daśārṇa and Ākara, powers before the Paramāras, trade routes and sacred centres"
KB_SUBS = "S1 prehistory; S2 early Vidisha/Besnagar; S3 Dasharna/Akara and ancient regional geography; S4 early medieval powers before the Paramaras; S5 trade routes and sacred centres"
KB_GAP = {
    "3.1": ["rock shelters and rock paintings near Udaypur Basoda Vidisha", "stone tools palaeolithic microlithic Betwa valley",
            "early settlement mound near Udaypur prehistoric remains", "शैलचित्र और पाषाणकालीन औज़ार उदयपुर के पास",
            "cave on Udaypur hill ancient occupation sixth century"],
    "3.2": ["Dasharna country ancient name of eastern Malwa Vidisha capital", "Akara janapada east Malwa Avanti west Malwa",
            "Dasarna river Dhasan ancient geography Meghaduta", "दशार्ण देश विदिशा आकर"],
    "3.3": ["Besnagar ancient city excavations Heliodorus pillar Vidisha", "Vidisha distance from Udaypur ancient city nearby"],
    "3.4": ["Gupta period remains near Udaypur Udayagiri Vishnu Varaha", "Pratihara Rashtrakuta remains Pathari Badoh Gyaraspur near Udaypur",
            "eighth century inscription Udaypur hill", "earlier dynasty at Udaypur before the Paramaras"],
    "3.5": ["trade route Vidisha to Ujjain and the Deccan through eastern Malwa", "road from north India to the Deccan passing Udaypur Basoda",
            "Patari ruins near Udaypur temples"],
}
KB_CONTRA = {"Besnagar destruction": "Besnagar destroyed deluge abandoned Bhilsa founded eighth century tenth century",
             "Heliodorus pillar date": "Heliodorus Garuda pillar date century BC"}

CONFLICTS = {
    "3.1": [("the country's name: Daśārṇa and Ākara", [r"Da[sś]ār?[nṇ]a|Dasharna|Dashārna", r"[AĀ]kara"])],
    "3.2": [("Sanchi's builder: Ashoka vs Vidisha's merchants", [r"Sa[nñ]ch[iī]", r"A[sś]oka|Ashoka", r"merchant|business|banker|donation|donor"]),
            ("Heliodorus pillar date", [r"Heliodor", r"140"])],
    "3.4": [("Besnagar's end: sudden vs gradual, seventh to tenth century", [r"Besnagar", r"deluge|devastat|destroy|desert", r"branch|gradual|not known|unknown|ninth|9th|tenth|10th"])],
}
# spare evidence for the length guard (used only if a section ends short)
EXTRA_POOL = {
    "3.1": ["C03-GAZ-040", "C03-GAZ-008", "C03-KB-GAZ-003", "C03-JAGTA-HI-007", "C03-RAJABHOJ-EN-004"],
    "3.2": ["C03-GAZ-018", "C03-GAZ-012", "C03-GAZ-016", "C03-GAZ-021", "C03-GAZ-026", "C03-GAZ-032", "C03-MADHYABHARAT-016", "C03-KB-GAZ-005", "C03-KB-GAZ-004", "C03-JAGTA-EN-002", "C03-KRAM-1-003"],
    "3.3": ["C03-GAZ-062", "C03-MADHYABHARAT-028", "C03-CII-007", "C03-RAJABHOJ-EN-007", "C03-KRAM-1-006"],
    "3.4": ["C03-GAZ-044", "C03-GAZ-046", "C03-GAZ-048", "C03-GAZ-049", "C03-GAZ-057", "C03-GAZ-059", "C03-MADHYABHARAT-023", "C03-MADHYABHARAT-025", "C03-KRAM-1-004", "C03-GAZ-007", "C03-GAZ-054", "C03-KB-GAZ-008"],
    "3.5": ["C03-TEMPLES-IND-007", "C03-JAGTA-HI-012", "C03-JAGTA-HI-011", "C03-TEMPLES-IND-004"],
}

# borrowed for the refine pass: Udaypur and Pathari on opposite slopes of the same range (Chapter 2 items, tagged borrowed)
REFINE_EXTRA = {"3.5": ["C02-KB-GAZ-009", "C02-GAZ-008"], "3.4": ["C02-KB-GAZ-009"]}

REPORT_OUTLINE_NOTES = """**Outline (`ch03_outline.md`)** — argument: *Udaypur was founded in a country that was already old — a Betwa valley used since the Stone Age, the hinterland of ancient Vidisha (capital of Ākara/Daśārṇa and a crossroads of the north–south roads) and, by the eighth to tenth centuries, a contested frontier with temples and towns a few kilometres from Udaypur's own hill; the eleventh-century town inherited its roads, its sacred geography and its rivals rather than creating them.* Five sections in chronological and geographical order (3.1 first traces and names 800 · 3.2 Vidisha 950 · 3.3 roads and holy places 650 · 3.4 first-millennium kings and shrines 850 · 3.5 the eighth–tenth-century frontier 750 = 4,000), each with an explicit tie to Udaypur, ≤ 40% Gazetteer evidence (3.1's prehistory has no alternative source), boundaries to Chapters 2, 4, 5, 6 and 7, and four open questions stated rather than padded. Evidence profile: 156 mapped items (S1 3 · S2 80 · S3 10 · S4 40 · S5 23; Gazetteer 64) plus 24 `kb-new` items (no prehistoric site near Udaypur was found; the cave, the eighth-century hill inscription, Pathari and Badoh were) and 2 borrowed Chapter 2 items (Udaypur and Pathari on opposite slopes of the same range).

**After the pipeline.** The pipeline draft (4,117 words, ≤ 1 source-led sentence per section) had heavy repetition — mostly from the length-guard expansions (one paragraph stated the stone-tools fact five times) — plus unsupported claims of Pathari's and Badoh's proximity, Tiwari's full name four times and some meta-commentary. A rhythm pass, then a dedupe-and-enrich pass (cut every restatement, fix the verifier's flagged sentences, replace the cut words with unused evidence) and hand fixes followed; the near-duplicate count went from 10 to 0. The last re-verification of 3.4 could not run (OpenAI credits exhausted), so its six hand-edited sentences were checked by the editor against their quotes."""
