# Aggregate dossier report — all 19 chapters

Generated after the full Phase 2 dossier batch. Read this before approving
any dossier beyond C01 — several findings below required verification
against actual passage text before they could be trusted, and two checks
(garble, conflicts) turned out to have real false-positive patterns worth
knowing about before you rely on their counts.

## 0. How reliable is each section below

| Check | Mechanism | Reliability |
|---|---|---|
| Research gaps, single-source/thin/empty sub-themes | Deterministic (counting) | High — no LLM judgment involved |
| Corpus-wide structural OCR scan | Deterministic (replacement char / null byte) | High — same signal validated earlier this session via `kb_health.py` |
| Dossier-level semantic garble flags | LLM judgment, cheap backend | **Low** — spot-checked and found a real, broad false-positive pattern (see §3) |
| Label-fit warnings | LLM judgment, cheap backend | **Mixed** — the "Chapter overview" sub-theme's flags are systematic/structural, not meaningful (see §4); the keyword-group sub-themes' flags are more likely genuine |
| Conflicts | LLM judgment, cheap backend | **Mixed** — 1 of 6 confirmed false on direct check (see §5); treat the rest as candidates, not findings |

## 1. Chapter-level research gaps (deterministic, high confidence)

6 of 19 chapters flagged — at least half their sub-themes are EMPTY/SINGLE-SOURCE/THIN, and/or the whole chapter rests on very few independent sources:

| Chapter | Weak sub-themes | Total reliable sources |
|---|---|---|
| **C18** Present Tense | 4/4 | **1** |
| **C14** People of the Plateau | 4/5 | **2** |
| **C10** Words in Stone | 3/4 | **2** |
| **AW** Afterword | 3/4 | 6 |
| **C03** Stones and Forests | 2/5 | 5 |
| **C13** Fields, Wells and Markets | 2/5 | 8 |

C18 and C14 are the most severe — C18 rests entirely on `Jagta_Hua_Kasba_EN.md` (expected, per its own title annotation, but means the chapter has no independent corroboration for anything), and C14 has 4 of 5 sub-themes come back **empty** (no passages retrieved at all for caste/demography/language/everyday-life keyword groups specifically — this corpus appears to have very little content matching those exact terms, even though C14-tagged chunks exist elsewhere).

## 2. Single-source / thin / empty sub-themes (deterministic, high confidence) — 22 total

<details><summary>Full list (click to expand in your editor, or see dossiers/*.json)</summary>

- AW: [SINGLE-SOURCE] "conservation challenge, preservation struggle, community concern" — 2 passages, 1 source
- AW: [THIN] "future of the site, recommendation, improvement, heritage management" — 2 passages, 2 sources
- AW: [SINGLE-SOURCE] "what remains to be done, present-day threat" — 2 passages, 1 source
- C01: [SINGLE-SOURCE] "scriptural mention, textual reference, place-name etymology" — 19 passages, 1 source (all Inscriptions Corpus footnote apparatus — see label-fit note below, this is the same sub-theme flagged in the original C01 review)
- C02: [SINGLE-SOURCE] "land use, catchment, discharge, climatic variables" — 3 passages, 1 source
- C03: [SINGLE-SOURCE] "rock strata, outcrop, escarpment, weathering, erosion, soil profile, alluvium" — 2 passages, 1 source
- C03: [SINGLE-SOURCE] "terrain, topography, quarrying, building-stone source, geo-heritage survey" — 1 passage, 1 source
- C06: [SINGLE-SOURCE] "Bhoja's reign, Bhoja's royal court, courtly patronage, scholar-king, royal patron of learning" — 15 passages, 1 source
- C10: [SINGLE-SOURCE] "inscription, epigraphy, epigraph, paleography, Nagari script" — 7 passages, 1 source
- C10: [SINGLE-SOURCE] "prashasti, praśasti, copper plate, stone inscription, donative record" — 12 passages, 1 source
- C10: [SINGLE-SOURCE] "varnanagakripanika, serpentine scimitar inscription, Corpus Inscriptionum Indicarum" — 6 passages, 1 source
- C13: [SINGLE-SOURCE] "agriculture, cultivation, crop pattern, well irrigation, canal, tank irrigation" — 18 passages, 1 source
- C13: [SINGLE-SOURCE] "temple endowment, economic organisation, agrarian economy" — 12 passages, 1 source
- C14: [EMPTY] "caste, jati, tribe, community composition, ethnic group" — 0 passages
- C14: [EMPTY] "demography, population census, occupation, livelihood" — 0 passages
- C14: [EMPTY] "language, dialect, vernacular speech, social structure, social hierarchy" — 0 passages
- C14: [EMPTY] "everyday life, customs, plateau inhabitants" — 0 passages
- C15: [SINGLE-SOURCE] "Jagta Hua Kasba, resident's account, living tradition" — 9 passages, 1 source
- C18: [SINGLE-SOURCE] "Chapter overview" — 20 passages, 1 source
- C18: [SINGLE-SOURCE] "present-day Udaypur, contemporary life, living heritage, town today" — 7 passages, 1 source
- C18: [SINGLE-SOURCE] "Jagta Hua Kasba, current condition, tourism, local perspective" — 7 passages, 1 source
- C18: [SINGLE-SOURCE] "modern Udaypur, present tense account" — 5 passages, 1 source

</details>

**Pattern**: C10's inscription-focused sub-themes rest entirely on `Inscriptions Corpus.md` (expected — it's the one dedicated epigraphic edition in the corpus, but means C10 has zero independent corroboration for anything); C13's agriculture/economy sub-themes rest entirely on `Temple Economics.md`; C18 is entirely `Jagta_Hua_Kasba_EN.md`. None of these are surprising given each source's own specialization, but they mean these chapters will read as resting on one voice each unless you know of another source to add.

## 3. OCR-garble flags — treat as candidates, not a reliable count

**Corpus-wide structural scan** (reliable): 2/3,623 chunks (0.06%), both in `Samarangan Vol 2 (a)_combined.md` — matches the earlier `kb_health.py` finding exactly.

**Dossier-level semantic scan** (LLM judgment, cheap backend): 72 passages flagged across the 19 dossiers. I spot-checked several of the highest-count sources directly against their actual text before trusting this number, and found a **real, broad false-positive pattern**:
- `Samrangana Sutradhar Vol 1.md` (7 flagged): sampled passage was **coherent, legitimate** traditional timber-selection prescription — flagged only because its content is unusual/archaic to the model, not because it's corrupted.
- `Jagta_Hua_Kasba_EN.md` (7 flagged): sampled passage was **coherent, legitimate** narrative English prose — clear false positive.
- `467921465-Skanda-Purana-13-AITM.md` (4 flagged, was much higher before 2 rounds of prompt recalibration): confirmed false positives on Puranic scripture with unfamiliar-but-correct deity/sage names.
- `Inscriptions Corpus.md` (12 flagged) and `History of Paramara Dynasty DC Ganguly.md` (7 flagged): genuinely ambiguous on inspection — dense footnote apparatus and place-name lists that could be either legitimate scholarly density or real transcription artifacts; I could not tell without more context than a spot-check gives.

Only `P2` (INTACH, the original confirmed case) has actually been verified as real corruption. **My honest read: most of these 72 flags are false positives from the same "unfamiliar register reads as garbled" bias, not a systemic corpus-quality problem** — the true rate is probably much closer to the structural scan's 0.06% than to 72 passages. I'm reporting the raw counts below since you asked for them quantified, but recommend treating this list as "candidates I would NOT trust without a human reading the actual passage," not as a corpus-health finding.

| Chapter | Flagged | Chapter | Flagged |
|---|---|---|---|
| C15 | 11 | C09 | 2 |
| C10 | 9 | C13 | 2 |
| C11 | 9 | C02 | 1 |
| C01 | 8 | C03 | 1 |
| C04 | 5 | C14 | 1 |
| C08 | 4 | C16 | 1 |
| C05 | 4 | C17 | 1 |
| C06 | 3 | C18 | 1 |
| C07 | 3 | | |
| C12 | 3 | | |

By source: Inscriptions Corpus.md (12), Samrangana Sutradhar Vol 1.md (7), History of Paramara Dynasty DC Ganguly.md (7), Jagta_Hua_Kasba_EN.md (7), Intach Udaypur (1).md (5), 467921465-Skanda-Purana-13-AITM.md (4), The cultural heritage of madhya bharat.md (4), Raja_Bhoj_Aur_Parmarkaleen_EN.md (4), The Udayesvara Temple Art Architecture...md (4), iconography...Gupte.md (3), Temple Economics.md (2), Art of Paramaras.md (2), Geo-Heritage...md (2), Temple Architecture of India.md (2), 3 sources with 1 each.

Every flagged passage is still marked `[POSSIBLY GARBLED]` in its dossier and excluded from that sub-theme's independent-source count, per your instruction (corroboration-only, never a sole citation) — that mechanism is applied regardless of my false-positive concerns above, so it errs safe even if the flag itself is often wrong.

## 4. Label-fit warnings — split into two reliability tiers

**43 total flagged.** Before trusting this count, I checked how many were the generic **"Chapter overview"** sub-theme specifically (the one built from the chapter's own full descriptor, not a specific keyword group): **12 of 19** — a rate too high and too uniform to be 12 independent genuine findings. This looks structural: "Chapter overview" retrieval returns the top-K passages most similar to a *broad* chapter description, which by design surfaces topically diverse material — the check's expectation ("a cohesive high-level synopsis") is a standard that kind of retrieval was never going to meet, correct or not. **I'd discount all 12 "Chapter overview" flags as expected noise, not real findings.**

The remaining **31 flags on actual keyword-group sub-themes** are more likely genuine, since those queries were written as specific, coherent sub-topics — a mismatch there is more informative:

- **C01** "Skanda-Purana, Avantya-khanda, Avanti, sacred geography, tirtha" — flagged, but I'd weight this one down too: the reason given ("fragmented, poorly translated... Sanskrit-derived prose") is the same register-bias pattern from §3, not necessarily a real topical mismatch.
- **C04** "prehistory, palaeolithic, chalcolithic..." and "pottery, settlement mound..." — both flagged as returning architectural/religious content instead. Worth checking — could mean genuinely thin prehistoric coverage for this specific angle.
- **C07** "Udayaditya... founding, foundation, town planning" and "tank, reservoir, sagar..." — flagged as returning generic fort/temple descriptions instead of foundation-specific content.
- **C11** "mosque, dargah, tomb, minaret..." and "stepwell, baoli, tank architecture, ghat" — flagged as mostly returning temple/stupa content instead. Plausible: this corpus may simply have thin Islamic-period/stepwell-specific material even though C11 overall has good volume.
- **C12**, **C15**, **C16**, **C17** each have 1-2 keyword-group flags in a similar vein (retrieved content leans generic/adjacent rather than hitting the specific angle).

Full list of all 43 (including the 12 discounted "Chapter overview" ones) is in each chapter's own `dossiers/<id>.md` under "Label-fit warnings."

## 5. Conflicts flagged — 1 confirmed false, rest need verification

6 conflicts found across the 19 chapters. **I checked the C07 one directly against source text and it's a false positive**: the "conflict" (1059 vs. 1080 CE for the temple) is actually two different milestones of the same project — 1059 is construction *start*, 1080 is the flag-staff-hoisting *completion* date, per the inscription texts themselves (P14: "hoisting of flag... took place in 1080 A.D."; P18: "built... in Sam 1116=1059 A.D." — "built" here meaning commenced). This matches what was already established from this session's earlier reading of the same founding story. **The C08 conflict (1059-1087 vs. 1059/1080) is likely the same start-vs-completion pattern** — I didn't verify it directly but flag it as the same likely false-positive shape.

The other 4 are unverified by me — presenting as found, for your judgment:

- **AW**: a "mandir" location inconsistently placed in Kerala's Wayanad vs. Odisha's Lingaraj temple (P9) — worth checking whether these are actually two different mandirs being discussed, not one.
- **C04**: Vidisha district population figures that don't reconcile across census years in one passage (P17) — could be a real source-internal table-reading error, or the model mis-parsing a table.
- **C12**: Śaiva Siddhānta texts giving "three" vs. "four" kinds of *pāśa* (P14, P23) — plausible genuine doctrinal-source variation, the kind of thing worth keeping as a real flagged disagreement.
- **C16**: Mallū Khān's title/status (king vs. governor) at different dates (P42, P43) — could be a real historical succession ambiguity, or just two sources describing different points in an evolving status.

**Recommendation**: don't treat any of these 6 as settled without a direct read of the cited passages — I've shown that's necessary (it caught the C07 false positive) and I didn't have time to do it for all 6.

## 6. What I'd suggest before Phase 3

- **C14 and C18** are the two chapters where the research-gap flag is severe enough (2 and 1 total reliable sources respectively) that I'd want your explicit call on whether to proceed to an outline anyway (acknowledging the thinness) or hold for more sourcing first.
- The garble and label-fit LLM checks are working (they visibly catch real issues sometimes — P2, the original C01 label mismatch) but are noisy enough that I'd treat their per-passage/per-subtheme flags as prompts for a human to look, not as findings to act on unread. Corroboration-only enforcement for garbled passages stays in place regardless, since that's cheap insurance even when the flag itself might be wrong.
- The 6 conflicts are worth a quick human pass — I'd start with C12 and C16 (the two I didn't find an obvious innocent explanation for) before the others.
