"""Evidence tiers (editor-in-chief audit §5, approved 2026-10-14). Strongest first for medieval events.

  1 contemporary or near-contemporary inscriptions, read critically (a praśasti is also self-representation)
  2 standing fabric and archaeological observation
  3 later inscriptions (retrospective)
  4 documentary and administrative records; normative texts
  5 modern scholarship (named in the text only when it disagrees or is an actor)
  6 colonial-era observation
  7 modern survey and the Gazetteer (the modern setting)
  8 oral and local tradition and Tiwari's testimony: evidence for memory, not for the event narrated
  9 modern heritage and popular narratives (never adopt their superlatives)
 10 this book's own inference (tagged, verified)

Tiers are per source. CII VII.2 (Trivedi's edition) stands at tier 1 for what the inscriptions say. For dynastic
facts its editor's readings outrank Ganguly's. Ganguly's own interpretations are attributed to him as his reading.
"""

TIER_LABEL = {1: "contemporary inscription", 2: "fabric / archaeology", 3: "later inscription", 4: "document / normative text",
              5: "modern scholarship", 6: "colonial observation", 7: "modern survey / Gazetteer", 8: "tradition / testimony",
              9: "heritage or popular narrative", 10: "own inference"}

BY_CODE = {
    "CII": (1, "inscriptions as edited in CII VII.2; for dynastic facts the editor's readings outrank Ganguly"),
    "SERPENT": (5, "modern epigraphic study"),
    "PANDE": (5, "modern scholarship (temple monograph)"),
    "GANGULY": (5, "modern scholarship, 1933; where he interprets rather than reports, attribute it to him as his reading; CII outranks him on dynastic facts"),
    "HARDY": (5, "modern scholarship (architecture)"), "KRAM-1": (5, "modern scholarship (architecture)"), "KRAM-2": (5, "modern scholarship (architecture)"),
    "TEMPLES-IND": (5, "modern scholarship (architecture)"), "ARTPAR": (5, "modern scholarship (art history)"),
    "PARTEMPLES": (5, "modern scholarship (Paramāra temples)"), "MADHYABHARAT": (5, "modern scholarship and archaeological observation (Patil)"),
    "BHOJA-TIMES": (5, "modern scholarship (Mahesh Singh); page numbers not recoverable"),
    "BETWA-CLIM": (5, "modern science (basin climate study)"), "BETWA-FLOW": (5, "modern science (streamflow study)"),
    "GEOHER": (7, "modern survey (INTACH Geo-Heritage); never adopt its superlatives"), "INTACH": (7, "modern survey (INTACH)"),
    "GAZ": (7, "district Gazetteer, 1979 compilation: the modern setting"),
    "JAGTA-EN": (8, "testimony and local tradition (Tiwari); memory, not the event; pages approximate"),
    "JAGTA-HI": (8, "testimony and local tradition (Tiwari); memory, not the event"),
    "SKANDA": (8, "Purāṇic tradition"),
    "RAJABHOJ-EN": (9, "modern popular account (Rajpurohit): attribute; never adopt its claims as settled"),
    "BHOJDEV-HI": (9, "modern Hindi work, author and year unknown: attribute; corroborate before relying on it"),
    "PARMAR-RAJPUT": (9, "modern popular dynastic history, 2025: attribute; never sole support"),
    "SAMAR-1": (4, "normative treatise attributed to Bhoja; norms, not a record; old OCR, never quote"),
}


def tier_of(item):
    t, note = BY_CODE.get(item.get("book_code", ""), (5, "unclassified source; treat as modern scholarship"))
    return t, f"T{t} {TIER_LABEL[t]}: {note}"


def tag(pack_items):
    """add 'tier' and 'tier_note' to every item (in place) and return the list"""
    for i in pack_items:
        i["tier"], i["tier_note"] = tier_of(i)
    return pack_items
