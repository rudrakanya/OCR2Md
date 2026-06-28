# Book Draft Plan — *The Rising Lord: The Udayeśvara Temple of Udaypur*

**Parameters:** monograph on the Udayeśvara temple · educated general reader · concise (~7–8 ch, ~3,000–4,000 words each) · endnote-style citations.

## Token-efficiency protocol (IMPORTANT)
- **Never load whole giant sources.** Each chapter is drafted from only its small "evidence pack" below: the relevant `_index/*.md` summaries, the `_excerpts/*.md` slices, and at most a few targeted line-range reads from sources.
- The giant sources (`samarangana-sutradhara` 217k w, `bhoja-paramara` 133k w, `paramara-dynasty` 91k w) are accessed **only** via the pre-cut excerpts or precise `Read` offset/limit ranges — never read in full.
- **Diacritics:** sources use OCR-style `â/î/û` for `ā/ī/ū`. Normalize to proper IAST in the prose (e.g. *Kumārapāla, Udayāditya, Bhūmija*).
- **Grounding:** every substantive claim ties to a source; flag gaps as `[GAP — not in sources]`; do not invent dates/quotes. Endnotes per chapter cite source file (+ section).

## Assets already built (Phase 1 — done, token-cheap)
- `_index/` — 10 LLM summaries of the core/regional sources.
- `_excerpts/paramara_udayaditya_and_art.md` (~26k w) — Udayāditya/Naravarman history + Paramāra "Art & Culture".
- `_excerpts/ss_ch49-50_prasadas.md` (~9.5k w) — Samarāṅgaṇasūtradhāra prāsāda (temple-type) chapters.
- Free structural heading-maps of all 3 giants (locations recorded below).

## Chapter outline + evidence packs

1. **Introduction — A Temple on the Betwa**
   Evidence: `_index/vidisha-district-gazetteer.md` (Udaypur town, Betwa, geography; Ch XIX "Udayapur & the Udayeshwara Temple"), `_index/Betwa_Streamflow.md`, `_index/madhya-bharat-cultural-heritage.md`, `_index/udayesvara-temple-art-architecture.md` (intro).

2. **The Paramāras of Malwa — From Bhoja to Udayāditya**
   Evidence: `_excerpts/paramara_udayaditya_and_art.md`, `_index/bhoja-paramara-and-his-times.md`, `_index/parmar-rajput-dynasty-origins.md`.

3. **Raising the Udayeśvara — Patron, Date, and the Udayapur Praśasti**
   Evidence: `_index/udayesvara-temple-art-architecture.md`, `_index/madhya-bharat-inscriptions-and-shrines.md`, `_index/vidisha-district-gazetteer.md`; targeted read — `paramara-dynasty…md` lines 6063–6097 (Udayapur inscription list: Udayāditya saṃvat 1137/AD 1080, Naravarman 1151/1094, …).

4. **The Bhūmija Vision — Plan and Architecture**
   Evidence: `_index/udayesvara-temple-art-architecture.md`, `_index/madhya-bharat-temples-and-architecture.md`, `_index/Temples_of_India.md` (Ch VIII bhūmija/Paramāra), `_excerpts/ss_ch49-50_prasadas.md`; optional read — `samarangana…md` lines 21455+ (Ch 63 Meru/Nāgara prāsādas) for śikhara/bhūmija terms.

5. **The Temple's Visual World — Sculpture and Iconography**
   Evidence: `_index/udayesvara-temple-art-architecture.md` (sculpture/iconography sections), `_index/madhya-bharat-temples-and-architecture.md`.

6. **Philosophy in Stone — Śaiva Siddhānta and Bhoja's *Tattvaprakāśa***
   Evidence: `_index/udayesvara-temple-art-architecture.md` (Part II Metaphysics of Śaivism; Part III *Tattvaprakāśa of Bhoja*), `_index/bhoja-paramara-and-his-times.md` (Bhoja's works/religion), `_excerpts/ss_ch49-50_prasadas.md`.

7. **An Epigraphic Archive — Eight Centuries of Inscriptions** *(ends with a short "afterlife" coda)*
   Evidence: `_index/serpentine-scimitar-inscription-udaypur.md`, `_index/madhya-bharat-inscriptions-and-shrines.md`, `_index/vidisha-district-gazetteer.md` (Tughluq-period mosque, Udayasamudra tank, restoration; Gwalior State & ASI campaigns 1923–1985); targeted read — `paramara-dynasty…md` lines 6063–6097 (Udayapur inscriptions across rulers, saṃvat 1137→1366).

> **Tight 7-chapter book** (user decision). The former optional Ch. 8 (Afterlife/Restoration) is folded into a short coda closing Chapter 7.

## Remaining steps
- **Phase 2 (cheap):** finalize outline by reading only the 12 small `_index`/`_excerpts` files → user approves.
- **Phase 3:** draft one chapter at a time from its evidence pack (small bursts, resumable) → `book_draft/chapter-XX.md`. Review Ch 1 first.
- **Phase 4–5:** coherence + fact-check pass; assemble manuscript + endnotes/bibliography.

> Model-dependent drafting paused on the Claude Code session limit (resets 3:50 pm local). All prep above is done with zero further model spend.
