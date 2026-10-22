"""The book's List of Illustrations (book pp. xi-xiv = PDF pp. 4-7), transcribed by eye from the page photos,
keeping the author's wording, spelling, transliteration and punctuation. Italics are not marked. Small capitals
"CE" are written as CE. Page numbers are the book page given in the List's right-hand column.

Lines whose diacritics were checked at full resolution: Pl. 9 (samvarṇā, plain m), 40 (Uma-, no macron) vs
41 (Umā-), 52 (Haṁsavatī), 99-100 (Brahmāṇi, short i), 101 (Gaṇeśāni), 125 (Śivaliṅga).

Writes ../list_of_illustrations.json
"""
import json
from pathlib import Path

FIGURES = [
    (1, "Plan of the Udayeśvara Temple, c. 11th century CE, Udayapur, Madhya Pradesh, Courtesy Archaeological Survey of India.", "4"),
]

PLATES_NOTE = "All the Photographs are of the author, except the ones that belong to the American Institute of Indian Studies."

PLATES = [
    (1, "View of the śikhara from the south-west side.", "3"),
    (2, "View of the Udayeśvara temple complex.", "4"),
    (3, "View of one of the eight subsidiary shrines surrounding the main temple.", "5"),
    (4, "View of Śaiva pratihāras flanking the eastern entrance.", "5"),
    (5, "View of the śikhara and garbhagṛha showing its stellate-cum-circular plan.", "6"),
    (6, "View of the pillar-like buttresses of the garbhagṛha.", "7"),
    (7, "View of the pīṭha and vedībandha mouldings.", "8-9"),
    (8, "View of buttresses and their crowning members (south-east side of the gūḍhamaṇḍapa), Courtesy American Institute of Indian Studies.", "10"),
    (9, "View of the samvarṇā roof of the gūḍhamaṇḍapa, Courtesy American Institute of Indian Studies.", "11"),
    (10, "View of the east, north and south mukhamaṇḍapas, Courtesy American Institute of Indian Studies.", "12"),
    (11, "View of the śukanāsa at the base of the eastern latā, Courtesy American Institute of Indian Studies.", "13"),
    (12, "View of the flag-bearer on the śikhara.", "13"),
    (13, "View of the miniature niche on the lower half of the śukanāsa enshrining the image of the Hariharārkapitāmaha, Courtesy American Institute of Indian Studies.", "14"),
    (14, "Dancing devī on the right side of the miniature niche of the śukanāsa, Courtesy American Institute of Indian Studies.", "15"),
    (15, "Dancing Sarasvatī on the left side of the miniature niche of the śukanāsa, Courtesy American Institute of Indian Studies.", "16"),
    (16, "Dancing Sarasvatī, 9th century CE, Courtesy Da Nang Museum of Cham Sculpture, Vietnam, Accession no. 21.4.", "17"),
    (17, "View of the śukanāsa from the south-east.", "18"),
    (18, "View of the five-storeyed celestial mansion on the northern side of the śukanāsa.", "19"),
    (19, "View of the five-storeyed celestial mansion on the southern side of the śukanāsa.", "20"),
    (20, "Śiva Naṭeśa in the gavākṣa of the śūrasenaka of the western latā.", "21"),
    (21, "Śiva in the miniature niche of the śūrasenaka of the western latā.", "21"),
    (22, "View of the śūrasenaka of the southern latā.", "22"),
    (23, "View of the śūrasenaka of the northern latā.", "23"),
    (24, "View of buttresses on the maṇḍovara of the south-western side of the garbhagṛha.", "24"),
    (25, "General view of the south-east side of the gūḍhamaṇḍapa.", "24"),
    (26, "Mahābhairava enshrined in a khattaka adjacent to the east mukhamaṇḍapa.", "25"),
    (27, "View of buttresses on the south-east side of the gūḍhamaṇḍapa.", "25"),
    (28, "Sūrya enshrined in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "26"),
    (29, "Śiva enshrined in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "27"),
    (30, "Indra depicted in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "28"),
    (31, "Agni housed in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "28"),
    (32, "Ardhanārīśvara enshrined in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "28"),
    (33, "Harihara housed in a khattaka on the south-east side of the gūḍhamaṇḍapa.", "28"),
    (34, "Śiva Naṭeśa depicted on the south-east side of the gūḍhamaṇḍapa (south side).", "29"),
    (35, "General view of the tilaka of the south-east side of the gūḍhamaṇḍapa.", "29"),
    (36, "Ardhanārīśvara depicted in a long rectangular panel on the superstructure of the south mukhamaṇḍapa (east face).", "30"),
    (37, "Syncretic image of Gāyatrī, Sāvitrī and Sarasvatī on the tilaka of the south-east side of gūḍhamaṇḍapa.", "30"),
    (38, "Images of seated Śiva on the tilaka of the south-east side of gūḍhamaṇḍapa.", "31"),
    (39, "Māheśvarī depicted on the tilaka of the south-east side of gūḍhamaṇḍapa.", "31"),
    (40, "Seated Uma-Maheśvara housed in a khattikā on the vedībandha of the south-east side of gūḍhamaṇḍapa.", "32"),
    (41, "Seated Umā-Maheśvara housed in a khattikā on the vedībandha of the south-east side of gūḍhamaṇḍapa.", "32"),
    (42, "General view of the south-west side of the gūḍhamaṇḍapa.", "33"),
    (43, "Śiva Naṭeśa depicted on the south-west side of the gūḍhamaṇḍapa (west side), Courtesy American Institute of Indian Studies.", "35"),
    (44, "View of the buttresses on the south-west side of the gūḍhamaṇḍapa.", "36"),
    (45, "Standing male deity housed in a khattaka on the south-west side of the gūḍhamaṇḍapa.", "37"),
    (46, "Kiraṇākṣa Śiva depicted in a khattaka on the south-west side of the gūḍhamaṇḍapa.", "37"),
    (47, "Yama enshrined in a khattaka on the south-west side of the gūḍhamaṇḍapa.", "37"),
    (48, "Nirṛti depicted in a khattaka on the south-west side of the gūḍhamaṇḍapa.", "37"),
    (49, "Tripurāntaka Śiva enshrined in a khattaka on the south-west side of the gūḍhamaṇḍapa.", "38"),
    (50, "Tripurāntaka Śiva enshrined in a khattaka on the south kapilī.", "38"),
    (51, "General view of the tilaka of the south-west side of gūḍhamaṇḍapa.", "39"),
    (52, "Haṁsavatī depicted on the tilaka of the south-west side of gūḍhamaṇḍapa.", "39"),
    (53, "Bhairava depicted on the tilaka of the south-west side of gūḍhamaṇḍapa.", "40"),
    (54, "Bhairava depicted on the tilaka of the south-west side of gūḍhamaṇḍapa.", "40"),
    (55, "Bhairava depicted on the tilaka of the south-west side of gūḍhamaṇḍapa.", "41"),
    (56, "Seated Gaṇeśa enshrined in a khattikā on the vedībandha of the south-west side of gūḍhamaṇḍapa.", "41"),
    (57, "General view of the north-west side of the gūḍhamaṇḍapa.", "42"),
    (58, "Detailed view of buttresses on the north-west side of the gūḍhamaṇḍapa.", "43"),
    (59, "Varuṇa housed in a khattaka on the north-west side of the gūḍhamaṇḍapa.", "44"),
    (60, "Īśāna enshrined in a khattaka on the north-west side of the gūḍhamaṇḍapa.", "44"),
    (61, "Brahmā depicted in a khattaka on the north-west side of the gūḍhamaṇḍapa.", "44"),
    (62, "Kārttikeya enshrined in a khattaka on the north-west side of the gūḍhamaṇḍapa.", "44"),
    (63, "Śiva Naṭeśa enshrined in a khattaka near the north mukhamaṇḍapa, Courtesy American Institute of Indian Studies.", "45"),
    (64, "Śiva Naṭeśa, Ambarnath temple, 11th century CE, Maharashtra.", "46"),
    (65, "General view of the tilaka of the north-west side of gūḍhamaṇḍapa.", "46"),
    (66, "Vāyu and his consort Śivā enshrined in a khattikā on the vedībandha of the north-west side of gūḍhamaṇḍapa.", "47"),
    (67, "General view of the north-east side of the gūḍhamaṇḍapa.", "47"),
    (68, "View of buttresses on the north-east side of the gūḍhamaṇḍapa.", "48"),
    (69, "Mahiṣāsuramardinī enshrined in a khattaka near the north mukhamaṇḍapa (east side).", "49"),
    (70, "Vāyu enshrined in a khattaka on the north-east side of the gūḍhamaṇḍapa.", "50"),
    (71, "Brahmā enshrined in a khattaka on the north-east side of the gūḍhamaṇḍapa.", "51"),
    (72, "Sarasvatī enshrined in a khattaka on the north-east side of the gūḍhamaṇḍapa.", "51"),
    (73, "Cāmuṇḍā enshrined in a khattaka near the east mukhamaṇḍapa.", "52"),
    (74, "Cāmuṇḍā enshrined in the tilaka of the north-east side of gūḍhamaṇḍapa.", "52"),
    (75, "Śiva enshrined in the tilaka of the north-east side of gūḍhamaṇḍapa.", "53"),
    (76, "Śiva enshrined in the tilaka of the north-east side of gūḍhamaṇḍapa.", "53"),
    (77, "Yogeśvarī enshrined in the tilaka of the north-east side of gūḍhamaṇḍapa.", "53"),
    (78, "Hariharārkapitāmaha enshrined in a long rectangular panel on the superstructure of the north mukhamaṇḍapa.", "54"),
    (79, "Seated Umā-Maheśvara enshrined in a khattikā on the vedībandha of the north-east side of gūḍhamaṇḍapa.", "55"),
    (80, "View of sculptures in the khattakas between the south kapilī and south latā of the garbhagṛha.", "56"),
    (81, "Vīrabhadra enshrined in the khattaka of the south latā.", "56"),
    (82, "Cāmuṇḍā enshrined in a khattaka between the south latā and west latā of the garbhagṛha.", "57"),
    (83, "View of buttresses between the south latā and west latā of the garbhagṛha.", "58-59"),
    (84, "Bhairava enshrined in a khattaka between the south latā and west latā.", "60"),
    (85, "Nirṛti enshrined in a khattaka between the south latā and west latā.", "60"),
    (86, "Viṣṇu enshrined in a khattaka between the south latā and west latā.", "61"),
    (87, "Śiva enshrined in a khattaka between the south latā and west latā.", "61"),
    (88, "Nandikeśvara enshrined in a khattaka between the south latā and west latā.", "62"),
    (89, "Nandikeśvarī enshrined in a khattaka between the south latā and west latā.", "62"),
    (90, "Vīrabhadra enshrined in the khattaka of the west latā.", "63"),
    (91, "Kaumārī enshrined in a khattaka between the west latā and north latā.", "64"),
    (92, "Kārttikeya enshrined in the khattaka at the bottom of the west latā.", "64"),
    (93, "View of buttresses between the west latā and north latā of the garbhagṛha.", "66"),
    (94, "Kumāra enshrined in a khattaka between the west latā and north latā.", "67"),
    (95, "Śiva enshrined in a khattaka between the west latā and north latā.", "67"),
    (96, "Varuṇa enshrined in a khattaka between the west latā and north latā.", "68"),
    (97, "Vāyu enshrined in a khattaka between the west latā and north latā.", "68"),
    (98, "Kubera enshrined in a khattikā on the vedībandha between the west latā and north latā.", "69"),
    (99, "Brahmā-Brahmāṇi enshrined in a khattikā on the vedībandha between the west latā and north latā.", "69"),
    (100, "Brahmā-Brahmāṇi enshrined in a khattikā on the vedībandha between the west latā and north latā.", "69"),
    (101, "Gaṇeśa-Gaṇeśāni enshrined in a khattikā on the vedībandha between the west latā and north latā.", "69"),
    (102, "Sarasvatī enshrined in a khattikā on the vedībandha between the west latā and north latā.", "70"),
    (103, "Cāmuṇḍā enshrined in the khattaka of the north latā.", "70"),
    (104, "View of buttresses between the north latā and north kapilī of the garbhagṛha.", "71"),
    (105, "Umā-Maheśvara enshrined in a khattikā on the vedībandha between the north latā and north kapilī.", "72"),
    (106, "Lakṣmī-Nārāyaṇa enshrined in a khattikā on the vedībandha between the north latā and north kapilī.", "73"),
    (107, "Brahmā-Brahmāṇi enshrined in a khattaka below the north kapilī.", "73"),
    (108, "General view of the north mukhamaṇḍapa.", "74"),
    (109, "View of a dwarf pillar supporting the balcony of the mukhamaṇḍapa.", "75"),
    (110, "Detailed view the north mukhamaṇḍapa.", "75"),
    (111, "Detailed view of the east mukhamaṇḍapa.", "76"),
    (112, "View of the doorway of the south mukhamaṇḍapa, Courtesy American Institute of Indian Studies.", "77"),
    (113, "View of the lintels of the doorway of the south mukhamaṇḍapa.", "78"),
    (114, "Rāhu, Ketu and Saturn on the upper lintel of the doorway of the south mukhamaṇḍapa.", "79"),
    (115, "View of the entrance pillars of the gūḍhamaṇḍapa.", "80"),
    (116, "View of the interior of the gūḍhamaṇḍapa.", "82"),
    (117, "View of a pillar inside the gūḍhamaṇḍapa.", "83"),
    (118, "Tapasvinī Pārvatī enshrined in a niche on a pillar of the gūḍhamaṇḍapa.", "84"),
    (119, "View of the pillars of the antarāla and the entrance to the garbhagṛha.", "85"),
    (120, "Erotic couples on the panels of the pier-like wall-pillars of the gūḍhamaṇḍapa.", "86"),
    (121, "The figure of Nandi inside the gūḍhamaṇḍapa.", "86"),
    (122, "View of the stone stool in the gūḍhamaṇḍapa.", "86"),
    (123, "View of the ceiling of the gūḍhamaṇḍapa.", "87"),
    (124, "View of the ceiling of the antarāla, Courtesy American Institute of Indian Studies.", "88"),
    (125, "View of the Śivaliṅga in the garbhagṛha.", "89"),
    (126, "View of the vedī in front of the temple.", "90"),
    (127, "View of the interior of the vedī.", "91"),
    (128, "View of the mihrab of the mosque on the western side.", "91"),
    (129, "Pisanhārī kā Mandir, Udayapur, Vidisha, Madhya Pradesh.", "92"),
    (130, "Sculpture of Umā-Maheśvara inside the Pisanhārī kā Mandir, Udayapur, Vidisha, Madhya Pradesh.", "93"),
]

# where each List entry sits (PDF page of the List photo), for provenance
LIST_PDF_PAGE = {"fig": 4, (1, 15): 4, (16, 53): 5, (54, 94): 6, (95, 130): 7}


def list_page(kind, n):
    if kind == "figure":
        return 4
    for k, v in LIST_PDF_PAGE.items():
        if isinstance(k, tuple) and k[0] <= n <= k[1]:
            return v


def main():
    out = []
    for n, cap, pg in FIGURES:
        out.append({"kind": "figure", "number": n, "label": f"Fig. {n}", "list_caption": cap, "book_page": pg,
                    "list_pdf_page": list_page("figure", n)})
    for n, cap, pg in PLATES:
        out.append({"kind": "plate", "number": n, "label": f"Pl. {n}", "list_caption": cap, "book_page": pg,
                    "list_pdf_page": list_page("plate", n)})
    p = Path(__file__).resolve().parents[1] / "list_of_illustrations.json"
    p.write_text(json.dumps({"source": "List of Illustrations, book pp. xi-xiv (PDF pp. 4-7), transcribed by eye",
                             "plates_note": PLATES_NOTE, "entries": out}, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(len(out), "entries ->", p)


if __name__ == "__main__":
    main()
