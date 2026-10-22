"""Passage-level evidence metrics for eval/benchmark_passages_v1.yaml (Phase 10).

Deliberately separate from src/evaluate.py: this is specific to the new
passage-anchored schema (supporting_passages / context_only /
duplicate_ocr_of), not a change to the production book-level evaluator.

WHAT COUNTS AS A MATCH
-----------------------------------------------------------------------------
A retrieved hit's stored text "contains the evidence" for one passage entry
if the entry's `excerpt` (whitespace-normalized) is a substring of the hit's
text (also whitespace-normalized). Excerpts are kept short and
single-sentence specifically so they are unlikely to straddle a chunk
boundary; `caveats()` below flags any case where NO hit in the whole
collection's visible top-k window contains an excerpt that is independently
known (from direct reading) to exist in the source file -- that is reported
as a possible chunk-split, not silently scored as "passage absent".

DUPLICATE-OCR GROUPING
-----------------------------------------------------------------------------
A query's `supporting_passages` entries, together with each entry's
`duplicate_ocr_of` siblings, are grouped: every passage inside one group is
the SAME underlying fact (possibly OCR'd more than once), so finding any one
member of a group counts as finding that group once. Evidence Recall@k is
the fraction of DISTINCT GROUPS found in the top k, never the fraction of
raw passage strings -- so a duplicate-OCR pair cannot inflate coverage past
what one piece of evidence should count for.
"""
from __future__ import annotations

import re

_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    return _WS.sub(" ", text or "").strip()


def passage_match(hit_text: str, excerpt: str) -> bool:
    """True if `excerpt` appears verbatim (whitespace-normalized) in hit_text."""
    if not excerpt:
        return False
    return normalize(excerpt) in normalize(hit_text)


def build_evidence_groups(spec: dict) -> list[list[dict]]:
    """One group per distinct fact. Each supporting_passages entry seeds a
    group; its `duplicate_ocr_of` entries (if any) join the SAME group."""
    groups = []
    for p in spec.get("supporting_passages") or []:
        group = [p] + list(p.get("duplicate_ocr_of") or [])
        groups.append(group)
    return groups


def group_found_at_rank(hit_texts: list[str], group: list[dict]) -> int | None:
    """1-based rank of the first hit (in hit_texts, already in retrieval
    order) that matches ANY member of this evidence group. None if absent
    from hit_texts entirely."""
    for rank, text in enumerate(hit_texts, 1):
        if any(passage_match(text, member.get("excerpt", "")) for member in group):
            return rank
    return None


def evidence_recall_at_k(hit_texts: list[str], groups: list[list[dict]], k: int) -> float | None:
    """Fraction of distinct evidence groups found within the top k hits.
    None (not 0.0) when the query has zero evidence groups (e.g. a
    confirmed-unanswerable query) -- there is nothing to recall, which is a
    different fact than "recalled nothing of what was expected"."""
    if not groups:
        return None
    window = hit_texts[:k]
    found = sum(1 for g in groups if group_found_at_rank(window, g) is not None)
    return found / len(groups)


def first_evidence_rank(hit_texts: list[str], groups: list[list[dict]]) -> int | None:
    """Rank of the first hit that matches ANY evidence group (reciprocal-rank
    input). None if no group has any evidence (confirmed-unanswerable) or if
    none was found in hit_texts."""
    if not groups:
        return None
    ranks = [r for g in groups for r in [group_found_at_rank(hit_texts, g)] if r is not None]
    return min(ranks) if ranks else None


def reciprocal_rank(rank: int | None) -> float:
    return 1.0 / rank if rank else 0.0
