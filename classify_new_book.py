#!/usr/bin/env python
"""Phase 3 — layer, gate and merge the Rājamārtaṇḍa into the classified inventory.

    python classify_new_book.py            # writes the merged inventory + a report

The book has two layers that must not be mixed (spec Phase 3):

  pdf 1-4     front matter: title page and imprint. Evidence FOR Bhoja's
              authorship, so it is kept and tagged, not discarded.
  pdf 5-33    the editor's Hindi introduction (bhūmikā) on Dhāreśvara Bhoja,
              his works, his views and their dating. This is MODERN
              scholarship about Bhoja -> secondary_core, the C5/C10 layer.
  pdf 35      half-title: "धारेश्वर भोजदेवविरचित-राजमार्तण्डवृत्ति समेतम्".
  pdf 36-116  Bhoja's commentary itself. Sūtra-by-sūtra yoga doctrine:
              relevant to Bhoja's learning, NOT to Udaypur, the temple or
              dynastic history -> contextual_thematic, gated exactly like
              Temple Economics. A chunk here that actually names Bhoja,
              Dhārā, the Paramāras or Mālava is promoted back to the
              authorship layer (primary_authorial_paramara).

Quotability comes from the OCR gate: a chunk on a `needs_recheck` page is
`is_quotable = false` and carries `needs_recheck`, because on this badly
bound volume line-ends are cropped in the scan itself.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUD = ROOT / "kb_audit"
SRC = "rajamartanda-bhoja"

INTRO_END, HALF_TITLE = 33, 35
BHOJA = re.compile(
    r"भोज|धारेश्वर|धारा(?:नगर|पुर)|परमार|मालव|Bhoja|Dh[aā]r[aā]|Param[aā]ra|M[aā]lava", re.I)
# the commentary's own signature lines (colophon-like), strongest authorship evidence
COLOPHON = re.compile(r"भोजदेव(?:विरचित|कृत)|राजमार्तण्ड|श्रीभोज|इति\s+श्री")


def layer_of(page: int | None, text: str):
    """-> (layer, source_type, tags, note)"""
    if page is None:
        page = 999
    if page <= 4:
        return ("front_matter", "primary_authorial_paramara", ["title_page", "bhoja_authorship"],
                "title page / imprint: evidence for authorship and edition")
    if page <= INTRO_END or page == HALF_TITLE:
        return ("editor_introduction", "secondary_core", ["editor_introduction", "bhoja_authorship"],
                "editor's introduction on Dhāreśvara Bhoja, his works and their dating")
    if COLOPHON.search(text):
        return ("bhoja_authorship", "primary_authorial_paramara", ["bhoja_authorship", "colophonic"],
                "commentary text naming Bhoja / the Rājamārtaṇḍa itself")
    if BHOJA.search(text):
        return ("bhoja_authorship", "primary_authorial_paramara", ["bhoja_authorship"],
                "commentary passage that names Bhoja, Dhārā, the Paramāras or Mālava")
    return ("yoga_doctrine", "contextual_thematic", ["yoga_doctrine", "thematic"],
            "sūtra-by-sūtra yoga doctrine: Bhoja's learning, not Udaypur history")


def main():
    qc = {r["pdf_page"]: r for r in json.loads((ROOT / "ocr_cache/qc_patanjala.json").read_text(encoding="utf-8"))}
    new = [json.loads(l) for l in open(AUD / "classified_inventory_rajamartanda.jsonl", encoding="utf-8")]
    tally = collections.Counter()
    for c in new:
        prov = c["provenance"]
        page = prov.get("page_start")
        layer, stype, tags, note = layer_of(page, c["text"])
        g = qc.get(page, {})
        c["source_type"] = stype
        c["layer"] = layer
        c["layer_basis"] = note
        c["tags"] = sorted(set(c["tags"]) | set(tags) | ({"needs_recheck"} if g.get("status") == "needs_recheck" else set()))
        c["is_quotable"] = bool(g) and g.get("status") == "pass" and "llm_regenerated" not in c["tags"]
        c["ocr_gate"] = g.get("status", "unknown")
        c["ocr_confidence"] = g.get("conf_mean")
        prov["pdf_page"] = page
        prov["printed_page"] = g.get("printed_page")
        prov["page_image"] = (f"ocr_cache/patanjala-yogasutra-rajamartanda-bhoja.pages/images/page_{page:03d}.jpg"
                              if page else None)
        tally[(layer, c["is_quotable"])] += 1
    (AUD / "classified_inventory_rajamartanda.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in new) + "\n", encoding="utf-8")

    # merge into the main inventory, replacing any earlier copy of this source
    main_path = AUD / "classified_inventory.jsonl"
    keep = [l for l in open(main_path, encoding="utf-8") if json.loads(l)["parent_source_id"] != SRC]
    with open(main_path, "w", encoding="utf-8") as f:
        f.writelines(keep)
        for c in new:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"merged: {len(keep):,} existing + {len(new)} new = {len(keep) + len(new):,} chunks")
    for (layer, q), n in sorted(tally.items()):
        print(f"  {layer:22s} quotable={str(q):5s} {n:4d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
