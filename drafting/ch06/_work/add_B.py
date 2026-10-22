"""Worker B: add verbatim corpus slices to pack_B via kbn_local.py (free)."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent / "kbn_local.py"
S = [
 # CII No. 24, the Udaypur praśasti (pp. 131-135, 139)
 ("CII", 2114, "The orthographical peculiarities", "as in viśras-tāngō, l. 23;"),
 ("CII", 2115, "The language is fluent", "is not happy."),
 ("CII", 2118, "For example, cf. the beginning", "Mālatī-Mādhava."),
 ("CII", 2116, "After the introductory", "pertaining to this house."),
 ("CII", 2117, "It tells us in vv. 5-6", "as the Sun and the moon."),
 ("CII", 2117, "The present inscription, as we may note here", "composed about 1005 A.C."),
 ("CII", 2122, "Padmagupta appears", "this myth."),
 ("CII", 2126, "In verse 8, which begins the genealogy", "to be used in every day life."),
 ("CII", 2127, "The description here is purely conventional", "as already stated before."),
 ("CII", 2128, "Verse 12 introduces", "Harsolā grants of Siyaka himself."),
 ("CII", 2129, "The next three verses (13-15)", "though some of these may be of a doubtful nature."),
 ("CII", 2130, "Verses 14-15 of the present record", "is evidently inadmissible."),
 ("CII", 2137, "With reference to Vākpati's victory over the Chōlas", "a very great distance from Mālwā."),
 ("CII", 2138, "About Vākpati's end", "which we know from some other sources."),
 ("CII", 2139, "Vākpati's younger brother was Sindhurāja", "the Muralas (X, 14-20)."),
 ("CII", 2140, "The assertion of the prāśastikāra", "the Karnāṭas and the Turushkas."),
 ("CII", 2147, "Prithu, after whom", "on the word urvīdhara here."),
 ("CII", 2151, "About Indraratha and", "to know its details."),
 ("CII", 2152, "The first three of these names", "from the east to the west."),
 ("CII", 2154, "The enemies referred to here are not specified", "in the last days of Bhōja, or immediately after his death."),
 ("CII", 2167, "The next verse (22)", "Part B)."),
 ("CII", 2171, "[Metres", "Mandākrāntā ]."),
 ("CII", 2239, "To notice the contents", "members of the Nēmaka dynasty."),
 # Nagpur praśasti (No. 33), pp. 176-178
 ("CII", 2786, "It consists of forty lines", "appearing in the main record:"),
 ("CII", 2794, "The language is generally correct", "who wrote the prasastī on the stone."),
 ("CII", 2795, "It is also full of words", "there is yat-bhaṅga."),
 ("CII", 2796, "The purpose of the inscription is to record", "by the king himself (vv. 55-56)."),
 ("CII", 2797, "Beginning with a small sentence", "in the records of the Paramāra house."),
 ("CII", 2801, "The poet's name is not specifically mentioned", "composed by Naravarman himself."),
 ("CII", 2804, "It is noteworthy that the first four names", "worthless for the historian."),
 ("CII", 2808, "It is rather strange", "no reference to his learning."),
 # Pānāhedā praśasti of Maṇḍalika (V.S. 1116), pp. 422-423
 ("CII", 6814, "The language of the inscription is Sanskrit;", "as the poet himself asserts in v. 60,"),
 ("CII", 6830, "The name of the composer", "belonged to Valabhī."),
 # Somēśvara praśasti (Kirāḍu), p. 481
 ("CII", 7712, "The next verse relates the myth", "a king of Maru-mandala."),
]
for code, line, a, b in S:
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(H), "B", code, str(line), a, b], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip() or r.stderr.strip()[-300:])
