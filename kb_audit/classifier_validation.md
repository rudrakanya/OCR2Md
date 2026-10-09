# Stage 1B — Classifier validation

How far the epistemic-status labels in `classified_inventory.jsonl` can be trusted, measured against chunks I labelled by hand.

## Method

- Two samples of 36 claim-bearing chunks each (≥200 chars, Temple_Economics excluded), **stratified by predicted status**: 9 predicted factual, 9 observation, 9 inference, 9 speculation. Stratifying means the rare classes get tested at all, but the raw score overweights them. A prevalence-weighted figure is given below.
- **Round 1 (tuning set, seed 2026).** I labelled it, then changed the lexicon to fix the errors it exposed. Its after-fix score is *in-sample*, so it overstates accuracy.
- **Round 2 (held-out, seed 777).** Drawn after all rule changes. Shuffled, and labelled from the text alone before I looked at predictions. **No rule was changed after scoring it.** This is the honest number.
- Gold files are keyed by a verbatim text snippet, not chunk id, because ids are ordinal and shift whenever the chunking changes: `validation_gold_round1.json`, `validation_gold_round2_heldout.json`. To re-score: `python kb_audit/score_validation.py kb_audit/validation_gold_round*.json`.

## Results

| sample | correct | note |
|---|--:|---|
| Round 1, before fixes | 24/36 (67%) | |
| Round 1, after fixes | 30/36 (83%) | in-sample, optimistic |
| **Round 2, held-out** | **19/36 (53%)** | stratified, so rare classes are overweighted |

Held-out precision by predicted class, and each class's share of claim-bearing chunks:

| predicted | right | share of corpus | reading |
|---|--:|--:|---|
| factual | 7/8 (one snippet collided with another chunk, so 8 not 9) | 84% | trustworthy |
| observation | 6/9 | 6% | usable; errors are field-source background theory and argued passages |
| inference | 4/9 | 7% | half are really factual. The usual trigger is a stray "because" or a citation inside plain narrative |
| speculation | **2/9** | 3% | **not usable as-is**: 3 were anchored inference, 3 factual, 1 observation |

Weighting each class's precision by its share gives about **81% overall accuracy**. That figure is carried by the large, easy factual class. The classes the book cares most about, speculation and inference, are the weakest.

Held-out confusion (predicted → gold): factual→factual 7, factual→observation 1 · observation→observation 6, →inference 2, →factual 1 · inference→inference 4, →factual 4, →observation 1 · speculation→speculation 2, →inference 3, →factual 3, →observation 1.

## Failure modes (held-out)

1. **Perceptual "seem" read as an epistemic hedge.** Kramrisch: "The figures seem to resile charged with energy". That describes how a sculpture looks; it does not doubt a fact.
2. **Anchors the lexicon misses.** "On this basis it may be supposed…" (Tiwari) and a relief the author describes and then identifies with a hedge (Pande: "possibly nine figures") are both anchored, but the anchor is the object or the preceding argument, not a citation word.
3. **Reasoning words inside narrative.** "because", "Thus, where…", or a footnote marker in otherwise plain history (Ganguly #00312, Singh #01133) push factual text into inference.
4. **Background theory in field sources.** A paragraph of generic conservation theory in Geo-Heritage was labelled observation.
5. **Short hedges in long chunks.** A single "derived probably from…" clause (Patil) makes a mostly-asserted chunk speculation once it passes the 1/3 share rule.

## What this means for the audit

- Treat the **speculation and inference counts in `classification_tally.md` as candidate pools, not findings.** 448 speculation candidates at ~22% precision suggests roughly 100 genuinely unanchored claims. That is consistent with the 1A estimate (~129 hedged witness/observation chunks, 9/10 genuine when adjudicated).
- The **factual and observation labels are good enough** for bucketing and source-type work in Stage 2.
- Round-1 fixes that generalised well:
  - deontic "should be shown" is no longer read as opinion
  - bare "thus" is no longer read as reasoning
  - "not possible" is no longer read as a hedge
  - "cf" and footnote asterisks now count as anchors
  - recommendations are no longer read as inferences
  - one more OCR-chatter pattern ("The Ground Truth image…") is now stripped
- Hindi: the Devanagari cue lexicon is thin (`tiwari-jhk-hi`: 0 inference, 6 speculation). Classify the Tiwari pair from the English translation (canonical_for_quotation in the registry); the Hindi text stays for verification.

## Options before Stage 2 (your call)

- **A. Adjudicate the uncertain pool.** Take the ~1,700 inference and speculation candidates, minus Temple_Economics, and have them reviewed by a model pass or by hand, with factual/observation left as-is. This is the cheapest route to trustworthy speculation labels.
- **B. Accept the lexicon labels** and let Stage 2's claim-credibility score carry the uncertainty, with `mixed_status` and `speculation_share` exposed.
- **C. Another round** of lexicon fixes, validated on a new held-out sample. Failure modes 1 and 2 are hard for word lists, so expect diminishing returns.
