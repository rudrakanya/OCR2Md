# QA review — C7 (draft-v3.md)

Run 2026-09-24T22:44:54 by `chapter_pipeline.py verify C7`. Mechanical checks first; the editorial review below is written by the reviewer against the same draft.

## Mechanical checks

| check | result |
|---|---|
| length | 3,673 words (ok) |
| provenance markers | 90 markers, 35 distinct chunks |
| citations resolving to the dossier | 35/35 (none fabricated) |
| unsourced factual sentences | 0 |
| quotations verified against quotable chunks | all |
| inference/speculation asserted without hedge | 0 |
| evidence spread | pande-udayesvara 14, patil-composite-inscriptions 5, intach-2022-udaypur 5, intach-geoheritage 3, adhikari-2013-un 3, singh-serpentine 2 |
| encoding | clean NFC |
| gaps left in the draft | 0 |
| editorial framing sentences ([ed]) | 46 |

**No mechanical findings.**

## Editorial review

Written against `draft-v3.md` after the mechanical checks passed. Structure: What works · Clarity · Flow · Evidence · Style · Line edits.

### What works

- **The opening earns its place.** The quarry-and-temple observation is concrete, short, and it is doing argumentative work: the building is made of its own hill. It also sets up the closing move about self-recording.
- **The spire section explains a technical idea without a glossary.** "Instead of one curved tower carrying a single rhythm to the top, the spire is assembled out of many small shrines" is the clearest sentence in the chapter, and it arrives after the reader has been given the parts.
- **The two colossus measurements are handled exactly as the style guide asks.** The disagreement is stated, both figures are given, neither is silently preferred.
- **Pande's Śaiva Siddhānta reading is attributed rather than absorbed**, and the chapter says plainly that it is a reading. That is the hardest discipline in a chapter like this and it holds.

### Clarity

- The term *maṇḍovara* appears once, in the moulding list, without gloss. Either gloss it in the flow or cut it; the sentence survives without it.
- "the largest temple in the *bhūmija* manner that the Paramāras developed in Mālava" — the source says largest of the style; "that the Paramāras developed" is doing double duty as a claim about the style's origin. Consider splitting.
- Section 5's title promises "a colossus and a flour-grinder"; the śilpi-signatures paragraph that now closes it is good material but sits outside that promise. Either retitle or move it to Section 2, where the Un comparison already lives.

### Flow

- The chapter's spine — ground, spire, wall, doctrine, hillside, inscriptions — is legible and the bridges between sections are short. Good.
- Two sections open on an abstraction rather than a thing ("A Nāgara wall is a sequence of mouldings before it is anything else"; "The arrangement of those figures is where description ends"). The style guide asks for a specific opening. The first is defensible because the list follows immediately; the second should start with the distribution itself.
- The paragraph beginning "Time has not treated the family equally" interrupts the Un comparison mid-argument. Move it after the Nemawar/Gwalior list.

### Evidence

- 90 markers over 35 distinct chunks, no fabricated ids, all quotations verified. **31 of the 35 cited chunks carry no detected corroboration** — a limitation of the KB's corroboration detector, not evidence that the claims are weak, but every one of them is single-sourced in the strict sense and the prose attributes accordingly.
- The evidence is concentrated in Pande (14 of 35 citations). That is appropriate for a chapter on this temple — she wrote the monograph — but an editor should know the chapter is substantially her account of the building.
- Three deliberate exclusions are recorded in `outline.md` and should not be "fixed" by a later hand: no temple height (the KB has none), no citation of `adhikari-2013-un-00602` (OCR gives 1880 for 1080), no page numbers for the Samarāṅgaṇa (its page metadata is broken).
- The chapter cites no primary śāstra text, though the bucket holds 789 chunks of it. That is a real gap: a paragraph setting the built form against what the *Samarāṅgaṇa-sūtradhāra* prescribes would strengthen Section 2. It was left out because the śāstra chunks in the dossier are generic prescriptions, not statements about this building, and connecting them would be the chapter's own argument rather than a sourced one. Worth a decision from the editor.

### Style

- Register is consistent and the diacritics are clean throughout.
- Two superlatives ride on sources rather than on the author: "most beautiful temple in India" is attributed to a sixteenth-century inscription via Ganguly, and "largest" to the INTACH survey. Correct handling.
- 46 `[ed]` sentences — roughly one in five. That is high but honest: much of this chapter is the author walking the reader around a building. An editor who wants a leaner voice should cut from these first, since removing them costs no evidence.

### Line edits

1. "Nothing was carted in from a prestigious distance." — good line, but "prestigious" is doing the work of an argument. Suggest: "Nothing was carted in from a distance to make a point."
2. "the reader should hold both ends of that span in mind" — instructing the reader. Cut to: "the span matters: the building took some twenty years."
3. "That is the *bhūmija* idea." — fine as a beat, but consider merging into the following sentence to avoid two short declaratives in a row after the technical list.
4. "The building houses its gods the way a town houses its people." — keep. It is the chapter's best image and it is doing structural work.
5. "It is a good one. It is not a fact the building states." — the double short sentence is effective once; there is a similar pair three paragraphs earlier ("And yet the fabric holds."). Vary one.
6. "waiting nine centuries for someone to read it" — the inscription was noticed by Singh, so "waiting" is the author's flourish; it is marked `[ed]` and therefore honest, but consider "unread in the scholarly literature for nine centuries", which is what the source supports.

### Verdict

Ready for the editorial team, with the Section 5 structural note and the śāstra gap flagged for a decision.
