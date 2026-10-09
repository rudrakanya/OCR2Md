"""Near-duplicate detection across books.

Three files in this corpus reproduce D. R. Patil's 1952 text, and one of them
also contains the whole of "Some Paramāra Temples". Without this pass a single
passage returns two or three times under different book titles, which inflates
precision@k and — worse for a book project — makes one source look like
corroboration from several independent ones.

Chunks are not deleted. The copy keeps its `duplicate_of` pointer and a
`is_duplicate` flag; retrieval demotes it, and the report tells you what was
found, so nothing disappears silently.
"""
from __future__ import annotations

from collections import defaultdict

from .textutil import jaccard, shingles


def find_duplicates(chunks, *, threshold: float = 0.72, shingle_n: int = 8,
                    band_size: int = 24) -> dict[str, tuple[str, float]]:
    """Return {duplicate_chunk_id: (kept_chunk_id, similarity)}.

    Candidate pairs come from an inverted index over a sampled subset of each
    chunk's shingles, so this stays near-linear instead of comparing all
    ~4,500 x 4,500 pairs.
    """
    sigs: dict[str, set[int]] = {}
    for c in chunks:
        sigs[c.chunk_id] = shingles(c.text, shingle_n)

    # Inverted index on the `band_size` smallest shingle hashes — a cheap
    # stand-in for minhash banding that needs no extra dependency.
    buckets: dict[int, list[str]] = defaultdict(list)
    for cid, sig in sigs.items():
        for h in sorted(sig)[:band_size]:
            buckets[h].append(cid)

    order = {c.chunk_id: i for i, c in enumerate(chunks)}
    seen: set[tuple[str, str]] = set()
    dupes: dict[str, tuple[str, float]] = {}

    for members in buckets.values():
        if len(members) < 2 or len(members) > 200:
            continue  # a bucket that large is a boilerplate shingle, not a copy
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i], members[j]
                pair = (a, b) if a < b else (b, a)
                if pair in seen:
                    continue
                seen.add(pair)
                sim = jaccard(sigs[a], sigs[b])
                if sim < threshold:
                    continue
                # Keep the earlier chunk in ingest order; mark the later one.
                keep, drop = (a, b) if order[a] <= order[b] else (b, a)
                # Follow an existing pointer so we never chain duplicates.
                while keep in dupes:
                    keep = dupes[keep][0]
                if drop == keep or drop in dupes:
                    continue
                dupes[drop] = (keep, round(sim, 4))
    return dupes
