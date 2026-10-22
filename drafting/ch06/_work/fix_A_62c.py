from pathlib import Path
p = Path(__file__).resolve().parent.parent.parent / "run/ch6/6.2.md"
t = p.read_text(encoding="utf-8")
R = [
    ("and the fifth has him judge Udayāditya worthy and make him king.",
     "and the fifth tells of a great giver of gold and grain to Brahmins who judged Udayāditya worthy and made him king."),
    ("At the Pānāhedā temple of Maṇḍaleśa, a thirty-eight-line inscription dated V.S. 1116 sets out the founding and the endowment in full, with the builders, the artisans, the composer and the gifts, and it names the Mālava king Sīyaka. [C06-PARTEMPLES-008; C06-CII-022]",
     "A thirty-eight-line inscription of a temple of Maṇḍaleśa, dated V.S. 1116, sets out the founding and the endowment in full, with the builders, the artisans, the composer and the gifts. [C06-PARTEMPLES-008] An inscription of the same year from Pānāhedā names the Mālava king Sīyaka. [C06-CII-022]"),
]
for a, b in R:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("ok")
