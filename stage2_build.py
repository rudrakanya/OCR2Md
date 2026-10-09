#!/usr/bin/env python
"""Stage 2 — rebuild the KB from the Stage 1 classified inventory.

    python stage2_build.py              # full build (needs kb3_embed.py vectors for the dense part)
    python stage2_build.py --no-dense   # lexical + prior relevance only

Inputs (all editable, all reviewed in KB_AUDIT / STAGE2_REPORT):
    kb_audit/classified_inventory.jsonl   Stage 1 chunks, statuses, provenance
    kb_audit/source_registry.yaml         book-level facts (type, dates, work_id)
    kb3/source_scores.yaml                source reliability + chapter priors
    kb3/chapters.yaml                     chapter profiles + relevance weights
    kb3/claims_register.yaml              contested claims → contradictions / supersession
    kb3/speculation_adjudication.yaml     hand-adjudicated statuses (override Stage 1)
    kb3/derived_inferences.yaml           AI-derived inference chunks (spec C8)
    kb3/emb_parts/                        bge-m3 int8 vectors keyed by content_hash

Outputs:
    kb3/kb_active.sqlite       the ONLY store retrieval and drafting may open
    kb3/active_vectors.npy     + active_vector_ids.json (row-aligned)
    kb3/kb_quarantine.sqlite   the archive: never opened by kb3_query.py; restorable
    kb3/logs/*.jsonl           every dedup, corroboration, contradiction, quarantine decision
    kb3/review_queue.csv       chunks routed to human review (spec C1)
    kb3/STAGE2_REPORT.md       tallies

Nothing is deleted. Every score is stored separately (spec B); they are only
combined at query time, in kb3_query.py.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sqlite3
import sys
import unicodedata
import zlib
from pathlib import Path

import numpy as np
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
AUD, K3 = ROOT / "kb_audit", ROOT / "kb3"
LOGS = K3 / "logs"
VERSION = "stage2-build/1.0"
NOW = dt.datetime.now().isoformat(timespec="seconds")

sys.path.insert(0, str(ROOT))
from stage1_classify import CITATION  # noqa: E402  (same anchor lexicon as Stage 1)


def rd(p):
    return yaml.safe_load(open(p, encoding="utf-8"))


def norm_ws(t):
    return re.sub(r"\s+", " ", t)


# --------------------------------------------------------------------------
# Folding: strip Latin diacritics only. Devanagari vowel signs are combining
# marks too, and stripping them would destroy the word.
# --------------------------------------------------------------------------
def fold(t: str) -> str:
    out = []
    for ch in unicodedata.normalize("NFD", t):
        if unicodedata.category(ch) == "Mn" and out and ord(out[-1]) < 0x250:
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out)).lower()


# --------------------------------------------------------------------------
# Entities and the Udaipur alias fix (audit D9)
# --------------------------------------------------------------------------
RAJ_CTX = re.compile(r"Rajasthan|Mewar|Ahar|Aghata|Guhila|Sisodi|\bRana\b|District", re.I)
ENTITIES = {
    "udaypur": re.compile(r"\bUdaypur\b|\bUdayapura?m?\b|उदयपुर", re.I),
    "udayaditya": re.compile(r"Udaya[\s-]?[aā]?ditya|Udayâditya|उदयादित्य|उदयदित्य", re.I),
    "udayesvara": re.compile(r"Udaye[sśs]h?[wv]ara?|Udayeśvara|N[iīe]+la?ka[nṇ]?[tṭ]h?e[sś]h?[wv]ara?|नीलकंठेश्वर", re.I),
    "bhoja": re.compile(r"\bBhoja?(?:deva?|dev)?\b|भोज", re.I),
    "jayasimha": re.compile(r"Jaya-?si[mṃn]h?a|Jaisingh|जयसिंह", re.I),
    "naravarman": re.compile(r"Naravarman|Narvarman|नरवर्मन", re.I),
    "tughluq": re.compile(r"Tughl[au]q|Tughlak|तुगलक", re.I),
    "aurangzeb": re.compile(r"Aurangzeb|Alamgir|औरंगजेब", re.I),
    "iltutmish": re.compile(r"Iltutmish|इल्तुतमिश", re.I),
    "vidisha": re.compile(r"Vidisha|Vidiśā|Bhilsa|Besnagar|विदिशा", re.I),
    "mosque": re.compile(r"\bmosque\b|\bmasjid\b|मस्जिद", re.I),
    "flagstaff": re.compile(r"flag-?staff|dhvaja|flag-hoisting|ध्वज", re.I),
    "tank": re.compile(r"Udaya-?samudra|Udaysagar|Udayasagar|\btank\b|talab|उदयसागर", re.I),
    "inscription": re.compile(r"inscription|prasasti|praśasti|prashasti|शिलालेख|अभिलेख", re.I),
}


def sentences(t):
    return re.split(r"(?<=[.!?।॥])\s+", t)


def entity_set(text: str) -> set[str]:
    found = {k for k, rx in ENTITIES.items() if rx.search(text)}
    for s in sentences(text):
        if re.search(r"\bUdaipur\b", s) and not RAJ_CTX.search(s):
            found.add("udaypur")
            break
    return found


# --------------------------------------------------------------------------
# Event dating (spec A: dual dating; never invent a date)
# --------------------------------------------------------------------------
CITE_SPANS = re.compile(
    r"\([A-Z][^()]{0,80}?\b(?:1[5-9]\d{2}|20[0-2]\d)[a-z]?(?:[,:;][^()]*)?\)"   # (Deva 1975), (Trivedi 1978, 88-89)
    r"|\b(?:Vol\.|J\.\s?R\.\s?A\.\s?S|J\.\s?A\.\s?S\.\s?B|E\.\s?I\.|I\.\s?A\.|ASR|A\.S\.I\.|pp?\.)[^.;]{0,40}")
RX_CE = re.compile(r"\b(\d{3,4})\s*(?:A\.?\s?D\.?|C\.?\s?E\.?)(?![a-z])|\bA\.?\s?D\.?\s*(\d{3,4})\b")
RX_BCE = re.compile(r"\b(\d{1,4})\s*B\.?\s?C\.?(?:E\.?)?(?![a-z])")
RX_VS = re.compile(r"(?:V\.\s?S\.|\bVS\b|Vikram(?:a)?\s*Sa[mṃ]vat|\bSa[mṃ]vat|\bSam\.?|संवत्?)\s*(\d{3,4})\b")
RX_SAKA = re.compile(r"(?:[SŚ]aka|\bShak)\s*(?:Samvat|era)?\s*(\d{3,4})\b")
RX_AH = re.compile(r"\bA\.?\s?H\.?\s*(\d{3,4})\b")
RX_CENT = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)\s+(?:C\.?|century)\s*(B\.?\s?C\.?E?\.?)?", re.I)
RX_BARE = re.compile(r"\b(?:in|of|year|dated|since|until|till|from|by|around|about|c\.|circa)\s+(1[0-9]\d{2}|20[0-2]\d)\b")


def event_years(text: str):
    """-> (min, max, confidence, basis) or None. 'dated' only for era-marked years."""
    t = re.sub(r"\$\^\{?(st|nd|rd|th)\}?\$", r"\1", text)          # 12$^{th}$ → 12th
    t = CITE_SPANS.sub(" ", t)
    hard, soft, basis = [], [], []
    for m in RX_CE.finditer(t):
        y = int(m.group(1) or m.group(2))
        if 1 <= y <= 2030:
            hard.append((y, y)); basis.append("CE")
    for m in RX_BCE.finditer(t):
        hard.append((-int(m.group(1)), -int(m.group(1)))); basis.append("BCE")
    for m in RX_VS.finditer(t):
        y = int(m.group(1)) - 57
        if 0 < y <= 2030:
            hard.append((y, y + 1)); basis.append("VS-57")
    for m in RX_SAKA.finditer(t):
        y = int(m.group(1)) + 78
        if 78 < y <= 2030:
            hard.append((y, y + 1)); basis.append("Saka+78")
    for m in RX_AH.finditer(t):
        y = round(int(m.group(1)) * 0.970229 + 621.5693)
        hard.append((y, y + 1)); basis.append("AH→CE")
    for m in RX_CENT.finditer(t):
        c = int(m.group(1))
        if 1 <= c <= 21:
            if m.group(2):
                soft.append((-(c * 100), -(c - 1) * 100 - 1))
            else:
                soft.append(((c - 1) * 100 + 1, c * 100))
            basis.append("century")
    for m in RX_BARE.finditer(t):
        y = int(m.group(1))
        soft.append((y, y)); basis.append("bare-year")
    spans = hard or soft
    if not spans:
        return None
    lo, hi = min(s[0] for s in spans), max(s[1] for s in spans)
    return lo, hi, ("dated" if hard else "approximate"), sorted(set(basis))


def fmt_years(lo, hi):
    f = lambda y: f"{-y} BCE" if y < 0 else f"{y} CE"
    return f(lo) if lo == hi else f"{f(lo)} – {f(hi)}"


def year_of(pubdate):
    m = re.search(r"(1[5-9]\d{2}|20[0-2]\d)", str(pubdate or ""))
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------
# Scores (spec B). Each is stored on its own; see STAGE2_REPORT for the rubric.
# --------------------------------------------------------------------------
# Refined taxonomy (Phase 2). Primacy = proximity to the event, not date.
PRIMACY = {"primary_authorial_paramara": 1.0, "primary_epigraphic": 1.0, "primary_scriptural": 0.9,
           "field_observation_survey": 0.9, "field_observation_reportage": 0.85,
           "secondary_core": 0.65, "secondary_comparative": 0.55, "environmental_scientific": 0.6,
           "reference_tertiary": 0.3, "contextual_thematic": 0.2,
           # coarse Stage 1 values, still accepted
           "primary": 1.0, "field_observation": 0.9, "secondary_scholarship": 0.6,
           "contextual_background": 0.2}
CONTEXTUAL = {"contextual_thematic", "contextual_background"}
FIELD = {"field_observation_survey", "field_observation_reportage", "field_observation"}
RECENCY_TIERS = {"secondary_core", "secondary_comparative", "environmental_scientific",
                 "reference_tertiary", "secondary_scholarship"}
CRED_BASE = {"factual": 0.80, "observation": 0.80, "inference": 0.70, "speculation": 0.35}


def primacy(c):
    p = PRIMACY[c["source_type"]]
    tags = set(c["tags"])
    if c["source_type"] in FIELD and "secondhand_history" in tags:
        p, why = 0.5, "field source reporting pre-modern history it did not witness"
    elif c["source_type"] not in PRIMACY or (c["source_type"] in RECENCY_TIERS and "embeds_primary_text" in tags):
        p, why = max(p, 0.7), "quotes primary text in the original script"
    elif c.get("origin") == "AI-derived":
        p, why = 0.4, "AI-derived synthesis over cited chunks"
    else:
        why = f"source_type {c['source_type']}"
    return p, why


def credibility(c):
    """Claim credibility. Single-source is NOT penalised (spec B3); penalties
    only for genuine problems: provenance/fidelity, internal hedging,
    contradiction by stronger evidence."""
    s = CRED_BASE[c["epistemic_status"]]
    why = [f"base {c['epistemic_status']} {s:.2f}"]
    tags = set(c["tags"])
    if c["epistemic_status"] in ("factual", "inference") and CITATION.search(c["text"]):
        s += 0.05; why.append("+0.05 cited")
    if "llm_regenerated" in tags:
        s -= 0.20; why.append("-0.20 AI-restated text ([cite:] markers): wording not verified against source")
    if "ocr_damaged" in tags:
        s -= 0.10; why.append("-0.10 OCR damage")
    prov = c["provenance"]
    if not prov.get("heading_trail") and prov.get("page_start") is None:
        s -= 0.10; why.append("-0.10 no page or section locator")
    if c.get("mixed_status") and c.get("speculation_share", 0) > 0 and c["epistemic_status"] != "speculation":
        d = round(0.10 * c["speculation_share"], 3)
        s -= d; why.append(f"-{d} speculative aside ({c['speculation_share']:.0%} of text)")
    if "scriptural_register" in tags:
        s = min(s, 0.60); why.append("cap 0.60: mythic register (credible as a witness to the text, not to events)")
    for adj, note in c.get("_register_adj", []):
        s += adj; why.append(note)
    if c.get("origin") == "AI-derived":
        s = c["_support_cred"] * c["inference_confidence"]
        why = [f"mean support credibility {c['_support_cred']:.2f} × inference_confidence {c['inference_confidence']:.2f}"]
    return round(min(1.0, max(0.05, s)), 3), why


def recency(c, pub_year):
    if c["source_type"] not in RECENCY_TIERS or pub_year is None:
        return None                     # spec B5: tie-breaker in these tiers only
    return round(min(1.0, max(0.0, (pub_year - 1900) / (2026 - 1900))), 3)


# --------------------------------------------------------------------------
# Near-duplicate detection (spec D): MinHash over 5-word shingles + LSH
# --------------------------------------------------------------------------
NPERM, BANDS = 64, 16
_rng = np.random.default_rng(20260922)
_A = _rng.integers(1, 2**31 - 1, NPERM, dtype=np.int64)
_B = _rng.integers(0, 2**31 - 1, NPERM, dtype=np.int64)
_P = np.int64(2**31 - 1)


def shingles(text):
    w = re.findall(r"\w+", fold(text))
    return {zlib.crc32(" ".join(w[i:i + 5]).encode()) for i in range(max(0, len(w) - 4))}


def minhash(sh):
    h = np.fromiter(sh, dtype=np.int64)
    return ((np.outer(_A, h) + _B[:, None]) % _P).min(axis=1)


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


# --------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-dense", action="store_true")
    ap.add_argument("--vectors", default="kb3/emb_e5", help="directory of part_*.npy/.json vectors")
    ap.add_argument("--model", default="intfloat/multilingual-e5-small")
    ap.add_argument("--query-prefix", default="query: ")
    # Thresholds are MODEL-SPECIFIC. Measured for multilingual-e5-small on this
    # corpus: random claim-bearing pairs average cos 0.811 (p99 0.878), so the
    # 0.85 that suited bge-m3 sat below the 90th percentile of random pairs and
    # produced 236,856 bogus "corroborations". True translation pairs run
    # 0.88-0.94, which is why the cross-lingual link also demands a mutual
    # nearest neighbour inside a positional window rather than a bare cutoff.
    # 0 disables the semantic corroboration detector. Default OFF: verified by
    # sampling, multilingual-e5-small cannot tell "same claim" from "same
    # subject area" (random pairs average 0.811; at 0.92 it was still pairing
    # unrelated survey prose and OCR garbage). A false corroboration tells the
    # writer a claim is confirmed when it is not, which is worse than missing
    # one, so corroboration rests on dated entity-year keys and the claims
    # register until a stronger embedder (bge-m3) is available.
    ap.add_argument("--corro-cos", type=float, default=0.0)
    ap.add_argument("--dup-cos", type=float, default=0.97)
    ap.add_argument("--xling-cos", type=float, default=0.88)
    args = ap.parse_args(argv)
    LOGS.mkdir(parents=True, exist_ok=True)
    logs = {n: open(LOGS / f"{n}.jsonl", "w", encoding="utf-8") for n in
            ("dedup", "corroboration", "contradiction", "quarantine", "status_override", "scoring", "build")}

    def log(name, **kw):
        logs[name].write(json.dumps(kw, ensure_ascii=False) + "\n")

    registry = {s["source_id"]: s for s in rd(AUD / "source_registry.yaml")["sources"]}
    sscores = rd(K3 / "source_scores.yaml")["sources"]
    chap = rd(K3 / "chapters.yaml")
    CH = chap["chapters"]
    CIDS = [c["id"] for c in CH]
    register = rd(K3 / "claims_register.yaml")["claims"]
    adjud = {i["chunk_id"]: i for i in rd(K3 / "speculation_adjudication.yaml")["items"]}
    derived = rd(K3 / "derived_inferences.yaml")["inferences"]

    chunks = [json.loads(l) for l in open(AUD / "classified_inventory.jsonl", encoding="utf-8")]
    by_id = {c["chunk_id"]: c for c in chunks}
    order = {c["chunk_id"]: i for i, c in enumerate(chunks)}
    print(f"{len(chunks):,} Stage 1 chunks")

    # ---- 0. footnote rescue ----------------------------------------------------
    # Stage 1 filed whole footnote blocks as apparatus when they OPEN with
    # reference lines ("E. I., Vol. X, p. 20; Ibid."), even where a note goes
    # on to argue (Ganguly's notes on Paramāra origins). Blocks outside an
    # index/contents/bibliography heading that contain a real argumentative
    # sentence are made claim-bearing again and re-labelled with the Stage 1
    # sentence rules.
    from stage1_classify import apparatus_heading, split_sentences, label_sentence
    ARG = re.compile(r"\b(is|was|are|were|has|had|have|seems?|suggests?|believe[sd]?|thinks?|holds?|argues?|appears?|may|might|must|would|could|should)\b")
    REFLIKE = re.compile(r"\bVol\.|\bpp?\.\s?\d|\bIbid|\bop\.\s?cit|\bed\.|\b(19|20)\d{2}\b")
    for c in chunks:
        if "content_kind:apparatus" not in c["tags"] or apparatus_heading(c["provenance"]["heading_trail"]):
            continue
        sents = split_sentences(c["text"].replace("\n", " "))
        good = [s for s in sents if len(s) >= 80 and len(re.findall(r"\b[a-z]{3,}\b", s)) >= 10
                and ARG.search(s) and len(REFLIKE.findall(s)) <= 1]
        if not good:
            continue
        field = c["source_type"] == "field_observation"
        wts = collections.Counter()
        for s in good:
            wts[label_sentence(s, field)[0]] += len(s)
        tot = sum(wts.values())
        st = ("speculation" if wts["speculation"] / tot >= 1 / 3 else
              "inference" if (wts["speculation"] + wts["inference"]) / tot >= 1 / 3 else
              "observation" if wts["observation"] >= wts["factual"] else "factual")
        c.update(claim_bearing=True, epistemic_status=st,
                 tags=sorted((set(c["tags"]) - {"content_kind:apparatus"}) | {"footnote"}))
        c["status_basis"] = "footnote rescued from apparatus; status from its argumentative sentences"
        log("status_override", chunk_id=c["chunk_id"], stage1="apparatus (non-claim)", stage2=st,
            reason="footnote block containing argument", sentences=len(good))

    # ---- 0b. lists of figures / plates / caption runs --------------------------
    # "Figure 27: Sanchi Stupa…62 Figure 28: …64" collapses into one paragraph,
    # so Stage 1's line-based apparatus test missed it. Many labels packed into
    # little text = a list of illustrations, not a claim.
    FIG = re.compile(r"\b(?:Figure|Fig\.|Image|Plate|Pl\.)\s*\d+", re.I)
    for c in chunks:
        if not c["claim_bearing"]:
            continue
        n_fig = len(FIG.findall(c["text"]))
        if n_fig >= 4 and len(c["text"]) / n_fig < 110:
            c["claim_bearing"] = False
            c["tags"] = sorted(set(c["tags"]) | {"content_kind:apparatus", "figure_list"})
            log("status_override", chunk_id=c["chunk_id"], stage1=c["epistemic_status"], stage2="non_claim",
                reason=f"list of figures/captions ({n_fig} labels in {len(c['text'])} chars)")

    # ---- 1. status overrides from adjudication -------------------------------
    for cid, it in adjud.items():
        c = by_id[cid]
        c["stage1_status"] = c["epistemic_status"]
        new = it["adjudicated_status"]
        if new == "non_claim":
            c["claim_bearing"] = False
            c["tags"] = sorted(set(c["tags"]) | {"content_kind:ocr_garbage"})
        else:
            c["epistemic_status"] = new
        c["tags"] = sorted(set(c["tags"]) | set(it.get("add_tags", [])))
        c["status_basis"] = f"adjudicated: {it['reason']}"
        log("status_override", chunk_id=cid, stage1=c["stage1_status"], stage2=new, reason=it["reason"])
    for c in chunks:
        c.setdefault("status_basis", "stage1 lexical classifier (see kb_audit/classification_log.jsonl)")

    # ---- 2. AI-derived inference chunks (spec C8) ---------------------------
    for d in derived:
        missing = [s for s in d["supports"] if s not in by_id]
        if missing:
            sys.exit(f"{d['id']}: support ids not in inventory: {missing}")
        c = {"chunk_id": d["id"], "parent_source_id": "ai-derived", "work_id": d["id"],
             "source_type": "secondary_core", "origin": "AI-derived",
             "epistemic_status": "inference", "claim_bearing": True, "mixed_status": False,
             "speculation_share": 0.0, "inference_share": 1.0, "tags": ["ai_derived"],
             "provenance": {"file": "kb3/derived_inferences.yaml", "title": d["title"],
                            "author": "AI-derived (Claude, claude-opus-5)", "publication_date": "2026-09-22",
                            "date_confidence": "dated", "heading_trail": d["title"], "page_start": None,
                            "page_end": None, "char_start": None, "char_end": None},
             "cues": [], "text": norm_ws(d["text"]), "n_chars": len(d["text"]),
             "content_hash": hashlib.sha1(d["text"].encode()).hexdigest()[:16],
             "supports": d["supports"], "inference_confidence": d["inference_confidence"],
             "_chapters_hint": d["chapters"], "status_basis": "AI-derived inference over cited chunks"}
        chunks.append(c); by_id[c["chunk_id"]] = c; order[c["chunk_id"]] = len(order)

    # ---- 3. vectors -----------------------------------------------------------
    vec = {}
    if not args.no_dense:
        for f in sorted((ROOT / args.vectors).glob("part_*.json")):
            hs = json.loads(f.read_text())
            arr = np.load(f.with_suffix(".npy")).astype(np.float32)
            vec.update(zip(hs, arr))
        print(f"{len(vec):,} vectors loaded")
    have_dense = bool(vec)

    # ---- 4. metadata: dates, entities ---------------------------------------
    n_retyped = 0
    for c in chunks:
        reg = registry.get(c["parent_source_id"], {})
        prov = c["provenance"]
        # The inventory was chunked before the Phase 2 taxonomy refinement, so
        # refresh source_type from the registry. Chunks with their own layer
        # (the Rājamārtaṇḍa: authorship vs yoga-doctrine) keep the type their
        # layer rule assigned.
        if reg.get("source_type") and not c.get("layer") and c["source_type"] != reg["source_type"]:
            log("status_override", chunk_id=c["chunk_id"], field="source_type",
                stage1=c["source_type"], stage2=reg["source_type"], reason="Phase 2 refined taxonomy")
            c["source_type"] = reg["source_type"]
            n_retyped += 1
        c["title"] = prov.get("title") or reg.get("title")
        c["author"] = prov.get("author") or reg.get("author")
        c["publication_date"] = prov.get("publication_date") or reg.get("publication_date")
        c["publication_date_confidence"] = prov.get("date_confidence") or reg.get("date_confidence") or "undated-flagged"
        ev = event_years(c["text"]) if c["claim_bearing"] else None
        if c["source_type"] == "field_observation" and c["epistemic_status"] == "observation" and reg.get("observation_date"):
            c["event_date"], c["date_confidence"] = reg["observation_date"], "approximate"
            c["event_date_basis"] = "registry observation_date (firsthand report of the visit)"
            yrs = [int(y) for y in re.findall(r"(?:19|20)\d{2}", reg["observation_date"])]
            c["event_year_min"], c["event_year_max"] = (min(yrs), max(yrs)) if yrs else (None, None)
        elif ev:
            c["event_year_min"], c["event_year_max"], c["date_confidence"], basis = ev
            c["event_date"] = fmt_years(ev[0], ev[1])
            c["event_date_basis"] = "dates in chunk text: " + ", ".join(basis)
        elif reg.get("event_date"):
            c["event_date"] = reg["event_date"]
            c["date_confidence"] = reg.get("event_date_confidence", "approximate")
            c["event_date_basis"] = "registry event_date (source-level)"
            c["event_year_min"] = c["event_year_max"] = None
        else:
            c["event_date"], c["date_confidence"] = None, "undated-flagged"
            c["event_date_basis"] = "no date in text or registry — flagged, not invented"
            c["event_year_min"] = c["event_year_max"] = None
        c["entities"] = sorted(entity_set(c["text"]))
        if {"udaypur", "udayesvara", "udayaditya"} & set(c["entities"]):
            c["tags"] = sorted(set(c["tags"]) | {"udaypur_specific"})

    print(f"{n_retyped:,} chunks retyped to the refined taxonomy")

    # ---- 5. chapter relevance (spec F; formula documented in chapters.yaml) ---
    terms = {}                                   # folded term -> set(chapter)
    for ch in CH:
        for t in ch["seed_terms"]:
            terms.setdefault(fold(str(t)), set()).add(ch["id"])
    lat = [t for t in terms if re.search(r"[a-z0-9]", t)]
    dev = [t for t in terms if t not in lat]
    rx_lat = re.compile(r"\b(" + "|".join(sorted(map(re.escape, lat), key=len, reverse=True)) + r")\b")
    rx_dev = re.compile("(" + "|".join(sorted(map(re.escape, dev), key=len, reverse=True)) + ")") if dev else None
    tf_all, df = [], collections.Counter()
    for c in chunks:
        ft = fold(c["text"]) + (" udaypur" if "udaypur" in c["entities"] else "")
        tf = collections.Counter(rx_lat.findall(ft))
        if rx_dev:
            tf.update(rx_dev.findall(ft))
        tf_all.append(tf)
        df.update(tf.keys())
    N = len(chunks)
    idf = {t: math.log(N / (1 + df[t])) for t in terms}
    tau = chap["lexical_tau"]
    w = chap["weights"]

    D = None
    if have_dense:
        from embed_e5 import load_model, encode
        tok, model = load_model(args.model)
        # Embed the chapter profile INCLUDING its seed terms, which carry the
        # Devanagari and IAST forms. An English-only description leaves Hindi
        # and Sanskrit chunks scoring near the corpus mean, which is how the
        # Rājamārtaṇḍa's Hindi introduction stayed out of C5.
        cv = encode([f"{ch['title']}. {ch['description']} " + " ".join(str(t) for t in ch["seed_terms"])
                     for ch in CH], tok, model, args.query_prefix).astype(np.float32)
        del model
        idx = [i for i, c in enumerate(chunks) if c["content_hash"] in vec]
        M = np.stack([vec[chunks[i]["content_hash"]] for i in idx]) @ cv.T
        mu, p99 = M.mean(axis=0), np.percentile(M, 99, axis=0)
        D = {}
        for row, i in enumerate(idx):
            D[i] = np.clip((M[row] - mu) / (p99 - mu), 0, 1)
        log("scoring", step="dense_calibration", mean=dict(zip(CIDS, map(float, mu))),
            p99=dict(zip(CIDS, map(float, p99))))

    for i, c in enumerate(chunks):
        prior = sscores.get(c["parent_source_id"], {}).get("chapter_prior", {}) or {}
        if c.get("_chapters_hint"):
            prior = {k: 0.8 for k in c["_chapters_hint"]}
        scores, comp = {}, {}
        for j, ch in enumerate(CH):
            k = ch["id"]
            s = sum(idf[t] * math.log1p(n) for t, n in tf_all[i].items() if k in terms[t])
            L = 1 - math.exp(-s / tau)
            P = float(prior.get(k, 0.0))
            if D is not None and i in D:
                r = w["lexical"] * L + w["dense"] * float(D[i][j]) + w["prior"] * P
            else:                                   # no vector: reweight lexical + prior
                r = (w["lexical"] * L + w["prior"] * P) / (w["lexical"] + w["prior"])
            scores[k] = round(r, 3)
            comp[k] = (round(L, 3), None if D is None or i not in D else round(float(D[i][j]), 3), P)
        c["chapter_scores"] = scores
        c["_components"] = comp
        tags = set(c["tags"])
        buckets = []
        contextual = c["source_type"] in CONTEXTUAL or "thematic" in tags
        # The Rājamārtaṇḍa's yoga-doctrine layer bears on Bhoja's learning and
        # nothing else: it is eligible for C5 and C10 only, however the score
        # falls elsewhere (spec Phase 3: must not flood unrelated chapters).
        doctrine_only = {"C5", "C10"} if "yoga_doctrine" in tags else None
        for ch in CH:
            anc = ch.get("anchor")
            if anc and c["claim_bearing"] and (
                    c["parent_source_id"] in anc.get("sources", []) or c["source_type"] in anc.get("source_types", [])) and (
                    c["epistemic_status"] in anc.get("statuses", []) or tags & set(anc.get("tags", []))):
                buckets.append(ch["id"])            # chapter defined by this source (e.g. C16 ← Tiwari)
                continue
            if doctrine_only and ch["id"] not in doctrine_only:
                continue
            bar = chap["bucket_threshold"] + (chap.get("contextual_extra_threshold", 0) if contextual else 0)
            if scores[ch["id"]] < bar:
                continue
            st = c["epistemic_status"]
            if contextual:                          # spec C5: informs, never leads a chapter
                buckets.append(ch["id"] + ":admitted")
            elif st in ch.get("welcome", []) or tags & set(ch.get("welcome_tags", [])):
                buckets.append(ch["id"])
            elif st in ch.get("admitted", []):
                buckets.append(ch["id"] + ":admitted")
        c["chapter_buckets"] = buckets

    # ---- 6. near-duplicates (spec D) -----------------------------------------
    uf = UF()
    sigs, shs = {}, {}
    for c in chunks:
        if not c["claim_bearing"] or c.get("origin"):
            continue
        sh = shingles(c["text"])
        if len(sh) >= 8:
            shs[c["chunk_id"]] = sh
            sigs[c["chunk_id"]] = minhash(sh)
    buckets_lsh = collections.defaultdict(list)
    rows = NPERM // BANDS
    for cid, sg in sigs.items():
        for b in range(BANDS):
            buckets_lsh[(b, sg[b * rows:(b + 1) * rows].tobytes())].append(cid)
    pairs = set()
    for ids in buckets_lsh.values():
        if 1 < len(ids) < 200:
            for a in range(len(ids)):
                for b in range(a + 1, len(ids)):
                    pairs.add((ids[a], ids[b]) if ids[a] < ids[b] else (ids[b], ids[a]))
    dup_links = []
    for a, b in pairs:
        j = len(shs[a] & shs[b]) / len(shs[a] | shs[b])
        if j >= 0.5:
            dup_links.append((a, b, "minhash_jaccard", round(j, 3)))
    # cross-language: Tiwari Hindi original ↔ English translation (same work)
    if have_dense:
        en = [c for c in chunks if c["parent_source_id"] == "tiwari-jhk-en" and c["content_hash"] in vec and c["claim_bearing"]]
        hi = [c for c in chunks if c["parent_source_id"] == "tiwari-jhk-hi" and c["content_hash"] in vec and c["claim_bearing"]]
        if en and hi:
            E = np.stack([vec[c["content_hash"]] for c in en]); H = np.stack([vec[c["content_hash"]] for c in hi])
            S = H @ E.T
            pos_en = np.array([k / len(en) for k in range(len(en))]); pos_hi = np.array([k / len(hi) for k in range(len(hi))])
            back = S.argmax(axis=0)                                # best HI for each EN
            for r_, c in enumerate(hi):
                window = np.abs(pos_en - pos_hi[r_]) <= 0.10          # translations keep their order
                s = np.where(window, S[r_], -1)
                best = int(s.argmax())
                # mutual nearest neighbour, not a bare cutoff: with a small
                # multilingual model the translation signal is only ~0.07 above
                # the random-pair mean, so agreement in both directions is what
                # makes the link trustworthy.
                if s[best] >= args.xling_cos and int(back[best]) == r_:
                    dup_links.append((c["chunk_id"], en[best]["chunk_id"], "crosslingual_mutual_nn", round(float(s[best]), 3)))
        # dense near-duplicates across different works (reprints, composites)
        ids_d = [c for c in chunks if c["content_hash"] in vec and c["claim_bearing"] and c["source_type"] not in CONTEXTUAL]
        V = np.stack([vec[c["content_hash"]] for c in ids_d])
        for s0 in range(0, len(ids_d), 2048):
            blk = V[s0:s0 + 2048] @ V.T
            for r_, col in zip(*np.nonzero(blk >= args.dup_cos)):
                a, b = ids_d[s0 + r_], ids_d[col]
                if s0 + r_ < col and a["parent_source_id"] != b["parent_source_id"]:
                    dup_links.append((a["chunk_id"], b["chunk_id"], "dense_cosine", round(float(blk[r_, col]), 3)))
    for a, b, method, score in dup_links:
        uf.union(a, b)

    def canon_key(cid):                       # which copy is canonical for quotation
        c = by_id[cid]; reg = registry.get(c["parent_source_id"], {})
        return (0 if reg.get("canonical_for_quotation") else 1,
                0 if c["parent_source_id"] in ("patil-1952",) else 1,
                {"primary": 0, "field_observation": 1}.get(c["source_type"], 2),
                year_of(reg.get("publication_date")) or 9999, order[cid])
    clusters = collections.defaultdict(list)
    for a, b, *_ in dup_links:
        clusters[uf.find(a)].append(a); clusters[uf.find(a)].append(b)
    dup_of = {}
    for root, members in clusters.items():
        members = sorted(set(members), key=canon_key)
        for m in members[1:]:
            dup_of[m] = members[0]
    for a, b, method, score in dup_links:
        log("dedup", a=a, b=b, method=method, score=score, cluster_canonical=dup_of.get(a, a))
    for c in chunks:
        c["duplicate_of"] = dup_of.get(c["chunk_id"])

    def indep(cid):
        """Independence unit for counting: the work of the cluster's canonical copy."""
        root = dup_of.get(cid, cid)
        return by_id[root]["work_id"]

    # ---- 7. contradictions + supersession from the claims register -----------
    contra = collections.defaultdict(set)
    sup_by = {}
    for c in chunks:
        c["_register_adj"] = []
        c["contested_claims"] = []
    for k in register:
        pos = k["positions"]
        for pi, p in enumerate(pos):
            for ent in p["chunks"]:
                cid = ent["id"]
                c = by_id[cid]
                if norm_ws(ent["snippet"]) not in norm_ws(c["text"]):
                    sys.exit(f"claims register {k['id']}: snippet not found in {cid} — re-point the entry")
                c["contested_claims"].append({"claim": k["id"], "position": p["label"], "disposition": p["disposition"]})
                c["tags"] = sorted(set(c["tags"]) | set(p.get("add_tags", [])) | {"contested"})
                if p["disposition"] in ("contradicted", "superseded"):
                    c["_register_adj"].append((-0.25, f"-0.25 contradicted by stronger evidence (claims register {k['id']})"))
                if p["disposition"] == "superseded" and not ent.get("incidental"):
                    sup_by[cid] = p["superseded_by"][0]
                for qi, q in enumerate(pos):
                    if qi == pi or p.get("context") or q.get("context"):
                        continue
                    for other in q["chunks"]:
                        contra[cid].add(other["id"])
                        log("contradiction", claim=k["id"], a=cid, a_position=p["label"], b=other["id"],
                            b_position=q["label"], a_disposition=p["disposition"], b_disposition=q["disposition"])
    for c in chunks:
        c["contradiction_ids"] = sorted(contra.get(c["chunk_id"], []))
        c["superseded_by"] = sup_by.get(c["chunk_id"])
        if c["superseded_by"]:
            log("contradiction", action="superseded", chunk_id=c["chunk_id"], superseded_by=c["superseded_by"])

    # ---- 8. corroboration (spec D): same claim, different independent works ---
    keyidx = collections.defaultdict(set)
    for c in chunks:
        if not c["claim_bearing"] or c["source_type"] in CONTEXTUAL:
            continue
        for s in sentences(c["text"]):
            ev = event_years(s)
            if not ev or ev[2] != "dated":
                continue
            ents = entity_set(s) - {"inscription"}
            for e in ents:
                for y in {ev[0], ev[1]}:
                    keyidx[(e, y)].add(c["chunk_id"])
    corro = collections.defaultdict(dict)
    for key, ids in keyidx.items():
        if len(ids) < 2 or len(ids) > 60:
            continue
        ids = sorted(ids)
        for a in ids:
            for b in ids:
                if a >= b or indep(a) == indep(b):
                    continue
                va, vb = vec.get(by_id[a]["content_hash"]), vec.get(by_id[b]["content_hash"])
                if va is not None and vb is not None and float(va @ vb) < 0.55:
                    continue                              # same entity+year, different topic
                corro[a].setdefault(b, key); corro[b].setdefault(a, key)
    # semantic detector: same subject in different words, e.g. two authors
    # describing the same relief. Requires a shared named entity so that
    # merely similar-sounding passages about different temples do not count.
    n_sem = 0
    if have_dense and args.corro_cos > 0:
        GENERIC = {"inscription", "mosque", "tank"}
        pool = [c for c in chunks if c["claim_bearing"] and not c.get("origin") and c["content_hash"] in vec
                and c["source_type"] not in CONTEXTUAL and set(c["entities"]) - GENERIC]
        V = np.stack([vec[c["content_hash"]] for c in pool])
        for s0 in range(0, len(pool), 1024):
            blk = V[s0:s0 + 1024] @ V.T
            for r_, col in zip(*np.nonzero(blk >= args.corro_cos)):
                a, b = pool[s0 + r_], pool[col]
                if s0 + r_ >= col or indep(a["chunk_id"]) == indep(b["chunk_id"]):
                    continue
                shared = (set(a["entities"]) & set(b["entities"])) - GENERIC
                if shared:
                    key = ("semantic", round(float(blk[r_, col]), 3), sorted(shared))
                    corro[a["chunk_id"]].setdefault(b["chunk_id"], key)
                    corro[b["chunk_id"]].setdefault(a["chunk_id"], key)
                    n_sem += 1
        print(f"semantic corroboration pairs: {n_sem:,}")
    for k in register:                                    # same register position, different works
        for p in k["positions"]:
            ids = [e["id"] for e in p["chunks"]]
            for a in ids:
                for b in ids:
                    if a != b and indep(a) != indep(b):
                        corro[a].setdefault(b, ("register", k["id"]))
    for c in chunks:
        cid = c["chunk_id"]
        if c.get("origin"):
            c["corroboration_ids"] = c["supports"]
            c["corroboration_count"] = len({indep(s) for s in c["supports"]})
            continue
        others = corro.get(cid, {})
        c["corroboration_ids"] = sorted(others)[:30]
        c["corroboration_count"] = len({indep(o) for o in others} - {indep(cid)})
        for o, key in list(others.items())[:30]:
            log("corroboration", a=cid, b=o, key=list(key), a_work=indep(cid), b_work=indep(o))
    for c in chunks:
        if c["claim_bearing"] and c["corroboration_count"] == 0 and not c.get("origin"):
            c["tags"] = sorted(set(c["tags"]) | {"single_source"})

    # ---- 9. scores ------------------------------------------------------------
    for c in chunks:
        if c.get("origin"):
            sup = [by_id[s] for s in c["supports"]]
            c["_support_cred"] = float(np.mean([credibility(s)[0] for s in sup]))
        c["score_primacy"], c["primacy_basis"] = primacy(c)
        rel = sscores.get(c["parent_source_id"], {})
        c["score_source_reliability"] = rel.get("reliability", 0.5 if c.get("origin") else None)
        c["score_claim_credibility"], c["credibility_basis"] = credibility(c)
        c["score_recency"] = recency(c, year_of(c["publication_date"]))
        c["relevance_tags"] = sorted(t for t in c["tags"] if not t.startswith("content_kind"))

    # ---- 10. quarantine decisions (spec C1, C4, C6, E) -------------------------
    overrides = {}
    if (K3 / "quarantine_overrides.jsonl").exists():
        for line in open(K3 / "quarantine_overrides.jsonl", encoding="utf-8"):
            o = json.loads(line)
            overrides[o["chunk_id"]] = o                # last decision per chunk wins
    review = []
    for c in chunks:
        q = None
        maxr = max(c["chapter_scores"].values())
        if not c["claim_bearing"]:
            q = "non_claim: apparatus / OCR garbage (index, contents, bibliography, unreadable text)"
        elif c["superseded_by"] and "folklore" not in c["tags"]:
            q = f"obsolete: superseded by {c['superseded_by']}"
        elif adjud.get(c["chunk_id"], {}).get("quarantine"):
            q = "unsupported speculation (adjudicated)"
        elif maxr < chap["irrelevant_below"] and not c["chapter_buckets"]:
            if not have_dense and c["source_type"] not in CONTEXTUAL:
                # lexical-only relevance cannot see topic in other words; C6: when in doubt, retain
                c["review_status"] = "review: below irrelevance threshold on lexical-only scores, kept active"
                review.append((c, "kept_active_lexical_only"))
            elif c["source_type"] in FIELD:
                c["review_status"] = "review: below irrelevance threshold, kept active (field-source safeguard)"
                review.append((c, "kept_active"))
            else:
                q = f"irrelevant: clears no chapter (max relevance {maxr:.2f} < {chap['irrelevant_below']})"
                review.append((c, "quarantined"))
        ov = overrides.get(c["chunk_id"])             # human review wins (kb3_quarantine.py)
        if ov and ov["action"] == "restore":
            q = None
            c["review_status"] = f"restored by review: {ov.get('note', '')}"
        elif ov and ov["action"] == "quarantine":
            q = f"{ov['reason']} (manual review)"
        c["is_quarantined"] = q is not None
        c["quarantine_reason"] = q
        c.setdefault("review_status", None)

    # AI-derived chunks may only rest on active chunks
    for c in chunks:
        if c.get("origin"):
            bad = [s for s in c["supports"] if by_id[s]["is_quarantined"]]
            if bad:
                sys.exit(f"{c['chunk_id']} rests on quarantined chunks {bad}")

    # ---- 11. write stores -------------------------------------------------------
    COLS = ["chunk_id", "parent_source_id", "work_id", "origin", "source_type", "epistemic_status",
            "status_basis", "claim_bearing", "title", "author", "publication_date", "publication_date_confidence",
            "event_date", "event_year_min", "event_year_max", "date_confidence", "event_date_basis",
            "chapter_scores", "chapter_buckets", "relevance_tags", "entities",
            "corroboration_ids", "corroboration_count", "contradiction_ids", "contested_claims",
            "duplicate_of", "superseded_by", "is_quarantined", "quarantine_reason", "review_status",
            "score_primacy", "primacy_basis", "score_source_reliability", "score_claim_credibility",
            "credibility_basis", "score_recency", "inference_confidence", "supports",
            "provenance", "cues", "text", "content_hash", "n_chars"]
    JSONC = {"chapter_scores", "chapter_buckets", "relevance_tags", "entities", "corroboration_ids",
             "contradiction_ids", "contested_claims", "credibility_basis", "supports", "provenance", "cues"}

    def row(c):
        return [json.dumps(c.get(k), ensure_ascii=False) if k in JSONC else c.get(k) for k in COLS]

    for name in ("kb_active.sqlite", "kb_quarantine.sqlite"):
        (K3 / name).unlink(missing_ok=True)
    act = sqlite3.connect(K3 / "kb_active.sqlite")
    qua = sqlite3.connect(K3 / "kb_quarantine.sqlite")
    ddl = "create table chunks (rowid integer primary key, " + ", ".join(f'"{k}"' for k in COLS) + ")"
    act.execute(ddl)
    qua.execute(ddl.replace("chunks (", "chunks (quarantined_at, "))
    act.execute("create virtual table chunks_fts using fts5(text, aliases, tokenize='unicode61 remove_diacritics 2')")
    act.execute("create table meta (k primary key, v)")
    act.execute("create table links (a, b, kind, basis)")
    ph = ",".join("?" * len(COLS))
    active_ids = []
    for c in chunks:
        if c["is_quarantined"]:
            qua.execute(f"insert into chunks (quarantined_at, {','.join(chr(34)+k+chr(34) for k in COLS)}) values (?, {ph})",
                        [NOW] + row(c))
            log("quarantine", action="quarantine", chunk_id=c["chunk_id"], reason=c["quarantine_reason"], at=NOW)
        else:
            cur = act.execute(f"insert into chunks ({','.join(chr(34)+k+chr(34) for k in COLS)}) values ({ph})", row(c))
            act.execute("insert into chunks_fts (rowid, text, aliases) values (?,?,?)",
                        (cur.lastrowid, c["text"], " ".join(c["entities"])))
            active_ids.append(c["chunk_id"])
    for a, b, method, score in dup_links:
        act.execute("insert into links values (?,?,?,?)", (a, b, "duplicate", f"{method}:{score}"))
    for c in chunks:
        for o in c["contradiction_ids"]:
            act.execute("insert into links values (?,?,?,?)", (c["chunk_id"], o, "contradiction", "claims_register"))
        if c["superseded_by"]:
            act.execute("insert into links values (?,?,?,?)", (c["chunk_id"], c["superseded_by"], "superseded_by", "claims_register"))
    # orphans from the old store (audit D7): archived, not lost
    old = ROOT / "kb" / "store.sqlite"
    n_orphan = 0
    if old.exists():
        o = sqlite3.connect(f"file:{old}?mode=ro", uri=True)
        for rid, src, text in o.execute("select rowid, source, text from chunks where source like '%udayesvara-temple-art-architecture%'"):
            rec = {k: None for k in COLS}
            rec.update(chunk_id=f"orphan-udayesvara-summary-{rid}", parent_source_id="udayesvara-temple-art-architecture (deleted)",
                       text=text, claim_bearing=True, is_quarantined=True,
                       quarantine_reason="orphan: source file deleted from disk; chunk carried over from kb/store.sqlite for review",
                       provenance={"old_store_rowid": rid, "file": src})
            qua.execute(f"insert into chunks (quarantined_at, {','.join(chr(34)+k+chr(34) for k in COLS)}) values (?, {ph})",
                        [NOW] + row(rec))
            log("quarantine", action="quarantine", chunk_id=rec["chunk_id"], reason=rec["quarantine_reason"], at=NOW)
            n_orphan += 1
    act.executemany("insert into meta values (?,?)", [
        ("built_at", NOW), ("version", VERSION), ("dense", str(have_dense)),
        ("note", "ACTIVE store. The quarantine archive is a separate file that retrieval never opens.")])
    act.commit(); qua.commit()
    if have_dense:
        keep = [cid for cid in active_ids if by_id[cid]["content_hash"] in vec]
        np.save(K3 / "active_vectors.npy", np.stack([vec[by_id[k]["content_hash"]] for k in keep]).astype(np.float16))
        (K3 / "active_vector_ids.json").write_text(json.dumps(keep))

    with open(K3 / "review_queue.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["chunk_id", "source", "decision", "max_relevance", "best_chapter", "text_start"])
        for c, dec in review:
            best = max(c["chapter_scores"], key=c["chapter_scores"].get)
            wr.writerow([c["chunk_id"], c["parent_source_id"], dec, c["chapter_scores"][best], best, c["text"][:160]])

    # ---- 12. report ------------------------------------------------------------
    for k, v in chap.items():
        if k != "chapters":
            log("scoring", param=k, value=v)
    log("build", at=NOW, version=VERSION, chunks=len(chunks), active=len(active_ids),
        quarantined=sum(c["is_quarantined"] for c in chunks) + n_orphan, dense=have_dense,
        dup_links=len(dup_links), register_claims=len(register), derived=len(derived))
    for f in logs.values():
        f.close()
    write_report(chunks, CH, chap, dup_links, n_orphan, review, have_dense)
    print(f"active {len(active_ids):,} | quarantined {sum(c['is_quarantined'] for c in chunks) + n_orphan:,} "
          f"| dup links {len(dup_links):,} | dense={have_dense}")
    return 0


def write_report(chunks, CH, chap, dup_links, n_orphan, review, have_dense):
    act = [c for c in chunks if not c["is_quarantined"]]
    L = ["# Stage 2 build report", "", f"Built {NOW} by `stage2_build.py` ({VERSION}); dense relevance: {have_dense}.", ""]
    L += ["## Stores", "", f"- active (`kb3/kb_active.sqlite`): **{len(act):,}** chunks",
          f"- quarantine archive (`kb3/kb_quarantine.sqlite`): **{len(chunks) - len(act) + n_orphan:,}** chunks, never opened by retrieval", ""]
    qr = collections.Counter((c["quarantine_reason"] or "").split(":")[0] for c in chunks if c["is_quarantined"])
    qr["orphan"] += n_orphan
    L += ["| quarantine reason | chunks |", "|---|--:|"] + [f"| {k} | {v:,} |" for k, v in qr.most_common()]
    L += ["", f"Review queue (`kb3/review_queue.csv`): {len(review):,} chunks below the irrelevance threshold "
          f"({sum(1 for _, d in review if d == 'kept_active'):,} kept active under the field-source safeguard)."]
    tw = [c for c in chunks if c["parent_source_id"].startswith("tiwari-jhk")]
    L += ["", f"*Jagta Hua Kasba* safeguard: {sum(not c['is_quarantined'] for c in tw):,} of {len(tw):,} chunks active; "
          f"quarantined only as non-claim: {sum(c['is_quarantined'] for c in tw):,}."]
    L += ["", "## Evidentiary mix per chapter bucket (active chunks)", "",
          "| chapter | bucketed | welcome | admitted | primary | field | secondary | tertiary | contextual | folklore-tagged |",
          "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for ch in CH:
        k = ch["id"]
        inb = [c for c in act if k in c["chapter_buckets"] or f"{k}:admitted" in c["chapter_buckets"]]
        t = collections.Counter(c["source_type"] for c in inb)
        L.append(f"| {k} | {len(inb):,} | {sum(k in c['chapter_buckets'] for c in inb):,} | "
                 f"{sum(f'{k}:admitted' in c['chapter_buckets'] for c in inb):,} | {t['primary']:,} | {t['field_observation']:,} | "
                 f"{t['secondary_scholarship']:,} | {t['reference_tertiary']:,} | {t['contextual_background']:,} | "
                 f"{sum('folklore' in c['tags'] for c in inb):,} |")
    nb = sum(1 for c in act if c["claim_bearing"] and not c["chapter_buckets"])
    L += ["", f"Active claim-bearing chunks in no bucket (relevant to something, below {chap['bucket_threshold']} everywhere): {nb:,}"]
    st = collections.Counter(c["epistemic_status"] for c in act if c["claim_bearing"])
    dc = collections.Counter(c["date_confidence"] for c in act if c["claim_bearing"])
    L += ["", "## Status and dating (active, claim-bearing)", "", "| epistemic_status | chunks |", "|---|--:|"]
    L += [f"| {k} | {v:,} |" for k, v in st.most_common()]
    L += ["", "| event date_confidence | chunks |", "|---|--:|"] + [f"| {k} | {v:,} |" for k, v in dc.most_common()]
    m = collections.Counter(d[2] for d in dup_links)
    L += ["", "## Deduplication (links only; nothing removed)", "", "| method | links |", "|---|--:|"]
    L += [f"| {k} | {v:,} |" for k, v in m.most_common()]
    L += [f"", f"Chunks marked `duplicate_of` another: {sum(1 for c in chunks if c['duplicate_of']):,}"]
    cc = collections.Counter(min(c["corroboration_count"], 5) for c in act if c["claim_bearing"])
    L += ["", "## Corroboration (independent works, duplicate clusters counted once)", "", "| independent corroborating works | chunks |", "|---|--:|"]
    L += [f"| {'5+' if k == 5 else k} | {v:,} |" for k, v in sorted(cc.items())]
    L += ["", "`single_source` means no independent corroboration was DETECTED: by the dated entity-year keys, "
          "the semantic detector (bge-m3 cosine ≥ 0.85 plus a shared named entity), or the claims register. "
          "It is information for the writer, not a penalty (spec B3). Most general scholarship is legitimately single-source."]
    ct = [c for c in chunks if c["contested_claims"]]
    L += ["", "## Contested claims", "", f"{len(ct)} chunks carry a contested claim; "
          f"{sum(1 for c in chunks if c['superseded_by'])} superseded; "
          f"{sum(1 for c in chunks if c['contradiction_ids'])} have contradiction_ids. See `kb3/claims_register.yaml`."]
    (K3 / "STAGE2_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
