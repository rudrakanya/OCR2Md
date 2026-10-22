"""Source-subject detector (writing rule 7): flags a sentence whose grammatical subject, or main clause, is a source
title, an author's name or "the author".

Heuristic, on the sentence with bracketed IDs and quotations removed:
  a. "according to <source>" anywhere; "the author" anywhere (banned outright)
  b. "In <source>'s account/view/reading/telling/words/edition/survey…," or "In *<Title>*," opening the sentence
  c. main clause = the text after an optional leading phrase that ends in a comma; flagged when it opens (after at most
     three determiners/adjectives) with a source name or short form and reaches a reporting verb within ~8 words
Primary sources that are objects of the place (the praśasti, the inscriptions, a slab, a grant) are NOT sources here:
"the inscriptions record…" is about Udaypur's own record. Their modern editors are sources ("the inscriptions' editor").
"""
import re

PEOPLE = ("Ganguly", "Pande", "Hardy", "Patil", "Kramrisch", "Rajpurohit", "Singh", "Mahesh Singh", "Tiwari", "Trivedi", "Shrivastav",
          "Verma", "Adhikari", "Krishna Deva", "Deva", "Gupte", "Sharma", "Venziya", "Suryavanshi", "Kumar", "Cunningham", "Beglar",
          "Kincaid", "Smith", "V\\. A\\. Smith", "Luard", "Vyas", "Bühler", "Buhler", "Garde", "Vaidya", "Ray", "Kielhorn", "Hultzsch",
          "Mirashi", "Bhandarkar", "Lake", "Willis", "Dikshit", "Mitra", "Sircar", "Marshall", "Wakankar", "Misra", "Khare", "Rao",
          "Bhattacharya", "Jain", "Agrawal", "Mishra", "Saxena", "Govind Saxena", "Narayan Vyas")
TITLES = ("Gazetteer", "Gazetteers", "Geo-Heritage", "INTACH", "Jagta Hua Kasba", r"\*Jagta Hua Kasba\*", "Bhojadeva", r"\*Bhojadeva\*",
          "Samarāṅgaṇasūtradhāra", r"\*Samarāṅgaṇasūtradhāra\*", "Samarangana", "Corpus Inscriptionum Indicarum", "CII",
          "Epigraphia Indica", "Skanda-Purāṇa", "Skanda Purāṇa", "Skanda Purana", r"\*Skanda-Purāṇa\*",
          "Bhoja Paramara and His Times", r"\*Bhoja Paramara and His Times\*", "History of the Paramāra Dynasty",
          "Temples of North India", "The Hindu Temple", "Raja Bhoj", "Madhya Bharat volume")
GENERIC = ("survey", "study", "streamflow study", "basin study", "climate study", "climatic study", "report", "inventory",
           "monograph", "catalogue", "account", "compilation", "treatise", "book", "paper", "editor", "editors",
           "inscriptions['’] editor", "translator", "author", "authors", "historian", "historians", "scholar", "scholars",
           "commentator", "gazetteer", "survey team", "researchers", "text")
VERBS = ("says|said|writes|wrote|written|describes|described|records|recorded|notes|noted|reports|reported|calls|called|gives|gave|"
         "places|placed|states|stated|identifies|identified|lists|listed|dates|dated|attributes|attributed|puts|finds|found|counts|"
         "counted|ranks|ranked|mentions|mentioned|suggests|suggested|argues|argued|holds|held|observes|observed|assigns|assigned|"
         "locates|located|credits|credited|reproduces|reproduced|quotes|quoted|distinguishes|distinguished|associates|associated|"
         "presents|presented|treats|treated|regards|regarded|interprets|interpreted|connects|connected|links|linked|explains|explained|"
         "estimates|estimated|documents|documented|refers|referred|reads|takes|took|adds|added|ascribes|ascribed|cites|cited|claims|"
         "claimed|derives|derived|recounts|recounted|remembers|preserves|preserved|offers|offered|devotes|includes|included|contains|"
         "concludes|concluded|judges|judged|considers|considered|deems|deemed|accepts|accepted|rejects|rejected|doubts|doubted|"
         "prefers|preferred|follows|followed|proposes|proposed|thinks|believes|believed|traces|traced|equates|equated|glosses|"
         "glossed|translates|translated|edited|publishes|published|surveyed|characterises|characterised|characterizes|portrays|"
         "depicts|depicted|summarises|summarised|prescribes|prescribed|praises|praised|recommends|recommended|warns|warned|"
         "projects|projected|measures|measured|shows|showed|sets|set|speaks|spoke|tells|told|insists|insisted|maintains|asserts|"
         "classifies|classified|divides|divided|defines|defined|uses|used|has|had|is|was|are|were")
_SRC = "(?:" + "|".join(sorted(PEOPLE + TITLES, key=len, reverse=True)) + ")"
_GEN = "(?:" + "|".join(sorted(GENERIC, key=len, reverse=True)) + ")"
_DET = r"(?:(?:the|a|an|this|that|these|those|one|another|its|his|her|their|later|earlier|same|modern|district|state|1979|"\
       r"colonial|british|local|village)\s+){0,3}"
QUOTES = re.compile(r"[\"“][^\"”]*[\"”]")
A_ACCORDING = re.compile(rf"\baccording to (?:{_DET})?(?:{_SRC}|{_GEN})\b", re.I)
A_AUTHOR = re.compile(r"\bthe author\b", re.I)
B_IN = re.compile(rf"^(?:In|For|To)\s+(?:{_DET})?(?:{_SRC}|{_GEN})(?:[’']s?)?\b[^,]{{0,40}}?(?:account|view|reading|telling|words|edition|"
                  r"survey|report|description|judgement|judgment|estimate|list|inventory|version|interpretation|record)?\s*,", re.I)
B_TITLE = re.compile(r"^In \*[^*]+\*,")
C_MAIN = re.compile(rf"^(?:{_DET})(?:{_SRC}(?:[’']s)?|(?:{_SRC}[’']s\s+)?{_GEN})\b(?:,?\s+[^\s.;:]+){{0,8}}?,?\s+(?:{VERBS})\b")
C_MAIN_I = re.compile(rf"^(?:{_DET})(?:{_GEN})\b(?:,?\s+[^\s.;:]+){{0,8}}?,?\s+(?:{VERBS})\b", re.I)


_PEOPLE = "(?:" + "|".join(sorted(PEOPLE, key=len, reverse=True)) + ")"
# hidden attributions: "dated … by Patil", "in Ganguly's hypothesis", ", while Hardy treats …"
D_BY = re.compile(rf"\b(?:dated|assigned|identified|attributed|described|placed|read|counted|treated|rejected|dismissed|doubted|"
                  rf"proposed|given|recorded|reported|noted|called|located|interpreted|edited|translated)\b[^.;]{{0,60}}?\bby\s+{_PEOPLE}\b")
D_IN = re.compile(rf"\b(?:in|on)\s+{_PEOPLE}[’']s\s+(?:hypothesis|reading|account|view|reconstruction|chronology|interpretation|telling|"
                  rf"words|judgement|judgment|opinion|estimate|edition|scheme|report|survey|description)\b", re.I)
D_WHILE = re.compile(rf"[,;]\s*(?:while|whereas|and|but)\s+{_PEOPLE}\s+(?:{VERBS})\b")


def _main_clause(s):
    s = s.strip().lstrip("*_“\"'(")
    # strip one leading phrase that ends in a comma (adverbial / subordinate), if short
    m = re.match(r"^([^,;:]{1,90}),\s+(.*)$", s)
    cands = [s]
    if m:
        cands.append(m.group(2))
    return cands


def source_led(sentence):
    s = QUOTES.sub("“…”", sentence).strip()
    # testimony must be attributed as memory (canon): "in Tiwari's account/telling/recollection" is not source-led narration
    if re.search(r"\b(?:in|by) Tiwari[’']s (?:account|telling|recollection|testimony|memory)\b", s, re.I):
        return None
    if A_AUTHOR.search(s):
        return "uses 'the author'"
    if A_ACCORDING.search(s):
        return "'according to <source>'"
    if B_TITLE.match(s) or B_IN.match(s):
        return "opens 'In <source> …,'"
    if D_BY.search(s) or D_IN.search(s) or D_WHILE.search(s):
        return "attribution to a named scholar inside the sentence"
    for c in _main_clause(s):
        c = c[0].upper() + c[1:] if c else c
        if C_MAIN.match(c) or C_MAIN.match(c[0].lower() + c[1:]) or C_MAIN_I.match(c):
            return "source/author is the subject of the main clause"
    return None


if __name__ == "__main__":
    tests = ["The Gazetteer gives about thirteen kilometres to Basoda; the author gives sixteen.",
             "Udaypur lies some thirteen to sixteen kilometres from Ganj Basoda.",
             "According to Ganguly, the temple was built in 1059.",
             "In Kincaid's account, the lesser dam was breached.",
             "The inscriptions record a flagstaff raised in 1080.",
             "At Udaypur, black cotton soil covers 75 per cent of the area.",
             "Tiwari attributes Udaypur's importance to its quarries.",
             "Although Ganguly dates it to 1059, the temple was consecrated later.",
             "The district Gazetteer of 1979 calls the Betwa a river of great antiquity.",
             "The streamflow study suggests that low flows come from limited subsurface water.",
             "Geo-Heritage interprets the kunds as deliberate provision.",
             "Kincaid, as quoted by Ganguly, describes a valley enclosed by hills.",
             "Residents include it in their formula.",
             "The survey team could not reach the cave."]
    for t in tests:
        print(bool(source_led(t)), "|", source_led(t), "|", t)
