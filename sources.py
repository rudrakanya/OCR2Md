#!/usr/bin/env python3
"""
sources.py — map KB filenames to real bibliographic citations.

The old drafting prompt asked the model to "cite the real scholarly works named
inside the evidence (authors/titles), never file names". That put the burden of
bibliography on a model that could only guess, and produced endnotes like
"Based on the inscriptional material in ...", which are untraceable.

Here the mapping is data, not inference. Each KB source file resolves to a
short form used in endnotes and a full form used in the bibliography. Anything
unmapped degrades to a readable version of its filename and is reported by
`unmapped()`, so a newly ingested source is noticed rather than silently
mis-cited.

v2 note — this file stays hand-curated on purpose. doc_understanding.py can now
read each source and propose these rows:

    python doc_understanding.py --propose-sources

but it PRINTS them for review rather than writing them. A dossier is a model's
reading of a document; it gets provenance wrong when a scanned book states none,
and a bibliography edited by a model without review is exactly the failure this
lookup table exists to prevent. The dossiers do feed `CLASSIFICATION`-adjacent
metadata into kb_store.sources automatically, because that drives retrieval
filtering (§3.6) where a wrong guess costs recall rather than a wrong citation.
"""

# filename -> (short form for endnotes, full form for the bibliography)
SOURCES = {
    "806955603-The-Temple-Architecture-of-India-Adam-Hardy.md": (
        "Hardy, *The Temple Architecture of India*",
        "Hardy, Adam. *The Temple Architecture of India*. Chichester: John Wiley & Sons, 2007."),
    "Betwa_Streamflow.md": (
        "*Streamflow of the Betwa River*",
        "*Streamflow of the Betwa River*. Hydrological study."),
    "Intach Udaypur (1).md": (
        "INTACH, *Udaypur Heritage Documentation*",
        "Indian National Trust for Art and Cultural Heritage (INTACH). "
        "*Heritage Documentation of Udaypur, Vidisha District, Madhya Pradesh*, 2022."),
    "Jagta_Hua_Kasba_EN.md": (
        "*Udaypur: Jagta Hua Kasba* (Eng. trans.)",
        "*Udaypur: Jagta Hua Kasba* [Udaypur: A Town Awake]. Hindi original; "
        "English translation prepared for this study."),
    "Jagta_Hua_Kasba_OCR_text.md": (
        "*Udaypur: Jagta Hua Kasba* (Hindi)",
        "*Udaypur: Jagta Hua Kasba* [Udaypur: A Town Awake]. Hindi text."),
    "Long-termhistoricchangesinclimaticvariablesofBetwa.md": (
        "*Long-term Historic Changes in Climatic Variables of the Betwa Basin*",
        "*Long-term Historic Changes in Climatic Variables of the Betwa Basin*. Climatological study."),
    "Raja_Bhoj_Aur_Parmarkaleen_EN.md": (
        "*Raja Bhoj aur Parmarkālīn Malwa* (Eng. trans.)",
        "*Raja Bhoj aur Parmarkālīn Malwa* [Raja Bhoja and Paramāra-period Malwa]. "
        "Hindi original; English translation prepared for this study."),
    "Some Paramara Templess.md": (
        "*Some Paramāra Temples*",
        "*Some Paramāra Temples*. Architectural survey."),
    "Temple_Economics.md": (
        "*Temple Economics*",
        "*Temple Economics*. Study of the economic organisation of Indian temples."),
    "Temples_of_India.md": (
        "*Temples of India*",
        "*Temples of India*. General survey."),
    "The Hindu Temple Vol 1 Stella Kramrisch.md": (
        "Kramrisch, *The Hindu Temple*, vol. 1",
        "Kramrisch, Stella. *The Hindu Temple*, vol. 1. Calcutta: University of Calcutta, 1946."),
    "The Hindu Temple Vol 2.md": (
        "Kramrisch, *The Hindu Temple*, vol. 2",
        "Kramrisch, Stella. *The Hindu Temple*, vol. 2. Calcutta: University of Calcutta, 1946."),
    "bhoja-paramara-and-his-times.md": (
        "*Bhoja Paramāra and His Times*",
        "*Bhoja Paramāra and His Times*. Historical study of the reign of Bhoja."),
    "bhojdev.md": (
        "*Bhojdev* (Hindi)",
        "*Bhojdev*. Hindi study of Bhoja and the Paramāras."),
    "iconography of hindus, buddhists and jains Gupte.md": (
        "Gupte, *Iconography of the Hindus, Buddhists and Jains*",
        "Gupte, R. S. *Iconography of the Hindus, Buddhists and Jains*. Bombay: "
        "D. B. Taraporevala Sons, 1972."),
    "madhya-bharat-cultural-heritage.md": (
        "Patil, *The Cultural Heritage of Madhya Bharat*",
        "Patil, D. R. *The Cultural Heritage of Madhya Bharat*. Gwalior: Department of "
        "Archaeology, Madhya Bharat Government, 1952."),
    "madhya-bharat-inscriptions-and-shrines.md": (
        "Patil, *The Cultural Heritage of Madhya Bharat* (inscriptions and shrines)",
        "Patil, D. R. *The Cultural Heritage of Madhya Bharat*: inscriptions and shrines. "
        "Gwalior: Department of Archaeology, Madhya Bharat Government, 1952."),
    "madhya-bharat-temples-and-architecture.md": (
        "Patil, *The Cultural Heritage of Madhya Bharat* (temples and architecture)",
        "Patil, D. R. *The Cultural Heritage of Madhya Bharat*: temples and architecture. "
        "Gwalior: Department of Archaeology, Madhya Bharat Government, 1952."),
    "paramara-dynasty-comprehensive-history.md": (
        "Ganguly, *History of the Paramāra Dynasty*",
        "Ganguly, D. C. *History of the Paramāra Dynasty*. Dacca: University of Dacca, 1933."),
    "parmar-rajput-dynasty-origins.md": (
        "*Origins of the Parmār Rajput Dynasty*",
        "*Origins of the Parmār Rajput Dynasty*. Study of the dynasty's origin traditions."),
    "samarangana-sutradhara.md": (
        "Bhoja, *Samarāṅgaṇasūtradhāra*",
        "Bhoja[deva], attrib. *Samarāṅgaṇasūtradhāra*. Sanskrit treatise on architecture, "
        "with translation."),
    "serpentine-scimitar-inscription-udaypur.md": (
        "Singh, 'A Serpentine Scimitar of Letters'",
        "Singh, A. 'A Serpentine Scimitar of Letters': the varṇanāgakṛpāṇikā inscription "
        "at Udaypur, 2019."),
    "udayesvara-temple-art-architecture.md": (
        "*The Udayeśvara Temple: Art and Architecture*",
        "*The Udayeśvara Temple, Udaypur: Art and Architecture*."),
    "vidisha-district-gazetteer.md": (
        "*Vidisha District Gazetteer*",
        "*Madhya Pradesh District Gazetteers: Vidisha*. Bhopal: Government of Madhya Pradesh."),
}


# filename -> (kind, contribution)
#
# `kind` drives the primary/secondary split in the citation plan. "primary" is
# reserved for material that is itself the historical object — a Sanskrit
# treatise, an inscription edition, a colonial-era or government record compiled
# from direct survey, testimony gathered from residents. "secondary" is modern
# scholarly interpretation. "tertiary" is reference/synthesis.
#
# `contribution` says what this source is *for* in a reference table, so a unit
# can be checked for whether it rests on chronology alone, or has architectural
# analysis and primary evidence behind it too.
CLASSIFICATION = {
    "806955603-The-Temple-Architecture-of-India-Adam-Hardy.md":
        ("secondary", "Architectural analysis and typology; Nāgara/Bhūmija classification"),
    "Betwa_Streamflow.md":
        ("primary", "Hydrological measurement; streamflow and discharge data"),
    "Intach Udaypur (1).md":
        ("primary", "Site documentation; measured survey, condition assessment, present-day record"),
    "Jagta_Hua_Kasba_EN.md":
        ("primary", "Local testimony and oral history; the town's account of itself"),
    "Jagta_Hua_Kasba_OCR_text.md":
        ("primary", "Local testimony and oral history (Hindi original)"),
    "Long-termhistoricchangesinclimaticvariablesofBetwa.md":
        ("primary", "Climatological measurement; long-term series"),
    "Raja_Bhoj_Aur_Parmarkaleen_EN.md":
        ("secondary", "Regional historiography of Bhoja and Paramāra Malwa"),
    "Some Paramara Templess.md":
        ("secondary", "Comparative architectural survey of Paramāra temples"),
    "Temple_Economics.md":
        ("secondary", "Economic organisation of temples; land grants, endowments, labour"),
    "Temples_of_India.md":
        ("tertiary", "General survey and context"),
    "The Hindu Temple Vol 1 Stella Kramrisch.md":
        ("secondary", "Śāstric and symbolic interpretation of temple form"),
    "The Hindu Temple Vol 2.md":
        ("secondary", "Śāstric and symbolic interpretation; plates and comparanda"),
    "bhoja-paramara-and-his-times.md":
        ("secondary", "Political and cultural history of Bhoja's reign"),
    "bhojdev.md":
        ("secondary", "Regional historiography of Bhoja (Hindi, part-bilingual)"),
    "iconography of hindus, buddhists and jains Gupte.md":
        ("secondary", "Iconographic identification; attributes, forms, conventions"),
    "madhya-bharat-cultural-heritage.md":
        ("secondary", "Regional cultural and archaeological synthesis"),
    "madhya-bharat-inscriptions-and-shrines.md":
        ("primary", "Epigraphic record; inscriptions and shrine inventory"),
    "madhya-bharat-temples-and-architecture.md":
        ("secondary", "Regional temple architecture survey"),
    "paramara-dynasty-comprehensive-history.md":
        ("secondary", "Dynastic chronology and political narrative"),
    "parmar-rajput-dynasty-origins.md":
        ("secondary", "Origin traditions and clan historiography"),
    "samarangana-sutradhara.md":
        ("primary", "Śāstric prescription; prāsāda taxonomy, proportion, ritual (Skt. + trans.)"),
    "serpentine-scimitar-inscription-udaypur.md":
        ("primary", "Primary epigraphic evidence; the varṇanāgakṛpāṇikā"),
    "udayesvara-temple-art-architecture.md":
        ("secondary", "Monograph on the Udayeśvara temple's art and architecture"),
    "vidisha-district-gazetteer.md":
        ("primary", "Administrative record; demography, agriculture, revenue, topography"),
}


def kind(filename):
    """'primary' | 'secondary' | 'tertiary' — drives the citation plan's split."""
    return CLASSIFICATION.get(filename, ("secondary", ""))[0]


def contribution(filename):
    """What this source contributes to a unit's reference table."""
    return CLASSIFICATION.get(filename, ("", "Unclassified — add to sources.CLASSIFICATION"))[1]


def _fallback(filename):
    stem = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ")
    return f"*{stem.strip()}*"


def short(filename):
    """Endnote form for a KB source filename."""
    return SOURCES.get(filename, (None, None))[0] or _fallback(filename)


def full(filename):
    """Bibliography form for a KB source filename."""
    return SOURCES.get(filename, (None, None))[1] or _fallback(filename)


def endnote(hit):
    """A complete, traceable endnote for one retrieved passage."""
    parts = [short(hit["source"])]
    trail = (hit.get("trail") or hit.get("heading") or "").strip()
    if trail:
        first = trail.split(" > ")[-1][:80]
        parts.append(f"'{first}'")
    if hit.get("page_start"):
        parts.append(f"p. {hit['page_start']}" if hit["page_start"] == hit.get("page_end")
                     else f"pp. {hit['page_start']}-{hit['page_end']}")
    return ", ".join(parts) + "."


def unmapped(filenames):
    """Sources present in the KB but missing from SOURCES — cite-by-guess risks."""
    return sorted(f for f in set(filenames) if f not in SOURCES)
