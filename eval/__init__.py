"""
eval — the measurement layer (§4).

The v2 plan's governing argument is that anything the pipeline could get wrong
by assuming should be measured instead, and that the evaluation layer therefore
comes first: hybrid search, reranking and contextualisation are all retrieval
interventions, and none of them can be justified or tuned without a baseline.

Modules
-------
goldset          build and validate the labelled set (incl. expected_empty items)
eval_retrieval   Recall@k, nDCG@10, MRR, context precision/recall, empty-pack accuracy
eval_generation  faithfulness, citation correctness/completeness, answer relevance
calibrate        sweep RERANK_FLOOR against the gold set and write the measured value
ablate           run configurations end to end and report deltas with confidence intervals

The honest caveat, stated once here rather than hedged everywhere: a gold set
bootstrapped by an LLM and not yet reviewed by a human measures agreement with
a model, not correctness. `goldset.py --status` reports how much of the set is
human-verified, and every metrics run records that fraction alongside its
numbers, so a result can never quietly present itself as better-grounded than
its labels.
"""
