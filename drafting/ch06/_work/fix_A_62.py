from pathlib import Path
p = Path(__file__).resolve().parent.parent.parent / "run/ch6/6.2.md"
t = p.read_text(encoding="utf-8")
R = [
    ("and set any Śaka year after it. [C06-JAGTA-EN-011; C06-KBN-JAGTA-EN-A-006]",
     "and set any Śaka year after it. [C06-JAGTA-EN-011; C06-INTACH-001; C06-KBN-JAGTA-EN-A-006]"),
    ("Where the six lines of 1080 are brief and correct, this record is long, twenty-two lines “teeming with a plethora of errors”, faulty in its language and grammar and in its workmanship too, so that a meaningful translation is hard to make.",
     "Where the flag record is brief and correct, this one is long, “of twenty-two lines in all, and teeming with a plethora of errors”, faulty in its language and grammar and in its workmanship too, so that a meaningful translation is hard to make."),
    ("Like other Paramāra inscriptions it opens", "Like the dynasty's other inscriptions it opens"),
    ("An inventory of the temple adds that six of its stone blocks carry a Sanskrit inscription in Devanagari, dated 1059, on the building of the temple by Udayāditya; whether it and the twenty-two lines are one record is not stated.",
     "Six stone blocks of the temple carry a Sanskrit inscription in Devanagari, dated 1059, on the building of the temple by Udayāditya, and whether they and the long record are one is not stated."),
    ("The pedigree and the long inscription have much in common. Both run from Gondala through his son,",
     "The long inscription has much in common with that sixteenth-century record. Both run from Gondala (Gandal) through his son,"),
    ("to Udayāditya, and both carry the same pair of years; that makes them close, but no record says they are one text. [C04-GANGULY-094; C06-KBN-GANGULY-A-001;",
     "to Udayāditya, and both carry the same pair of years; that makes them close, but no record says they are one text. [C04-GANGULY-094; C06-KBN-GANGULY-A-003; C06-KBN-GANGULY-A-001;"),
    ("records the foundation and the endowment in full,", "sets out the founding and the endowment in full,"),
    ("Beside such a record the twenty-two faulty lines at Udaypur,", "Beside such a record the faulty lines at Udaypur,"),
    ("Ganguly cites the same page of the *Journal of the American Oriental Society*, vol. VII, p. 35, both for",
     "Ganguly cites the same journal page, vol. VII, p. 35, both for"),
]
for a, b in R:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("ok")
