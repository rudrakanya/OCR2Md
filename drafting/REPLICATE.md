# Replicating the Udaypur drafting on another machine

The repository carries the **process**: the drafting toolkit, every chapter's configuration, plan and evidence pack,
the evidence index and the recorded evidence judgments, the editorial outlines and rulings, the style sheet and the
ledgers. It does **not** carry the drafted chapters (section texts, stitched chapters, footnoted drafts, .docx
outputs) or anything that is generated or binary. Those are rebuilt from the process below.

All paths in the code are relative to the checkout (computed from each file's location), so the repository can live
anywhere. Run commands from the repository root with `python -I -X utf8`.

## 1. Set up

1. Python 3.11. `pip install -r requirements.txt -r drafting/requirements-drafting.txt`
2. Copy `.env.example` to `.env` and add the keys you need (the evidence-map embeddings need `OPENAI_API_KEY`;
   checks, stitching and builds need none).
3. Inputs that are not in git, and where they come from:

| Input | Where | How to get it |
|---|---|---|
| Reference corpus (markdown) | `Udaypur Reference Markdown Files/` | in git |
| Vector store `udaypur_corpus_openai_large` | `chroma_db/` | `python -m src.ingest --rebuild` (paid embeddings; see config.yaml) |
| Corpus snapshot for the evidence tools | `drafting/_tools/corpus_snapshot.npz`, `corpus_meta.pkl` | `python -I drafting/_tools/engine.py` (from the vector store) |
| Retrieval packets and logs | `drafting/_runs/packets/`, `drafting/_runs/*_log.jsonl` | `retrieve_all.py` → `build_packets.py` (step 2) |
| Pandoc for .docx output | `drafting/_tools/vendor/` (not in git) | `pip install pypandoc_binary` |
| Source PDFs, page photos, image stores | `PDF Originals/`, `drafting/image_store*/` images | local only; the image-store tools and manifests are in git |
| Other OCR'd book texts | `Udaipur Books Markdown files/`, `public_domain_staging/` | local only (not read by the KB build) |

## 2. The evidence map (once, shared by all chapters)

Scripts in `drafting/_tools/`, in order:

`make_queries.py` → `engine.py` → `calibrate.py` → `retrieve_all.py` → `build_packets.py` →
*judging* → `check_judgments.py --all` → `assemble.py` → `make_status.py` → `render.py`

*Judging* was done by agent sessions following `_runs/rubric.md` (prompt in `RESUME.md`). The judgments are recorded
in `drafting/_runs/judgments/` (in git), so `assemble.py` rebuilds `drafting/_evidence_log.jsonl` deterministically
without re-judging; `index_evidence_maps.py` then builds the per-chapter `evidence_index/chNN.jsonl` (both are also
in git).

## 3. A chapter

The planning authority is `editorial/Udaypur_Complete_Book_Outline.md`, with rulings in
`editorial/Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md` (Part I) and units in
`editorial/Udaypur_Book_Contents.md`. The current configuration of each chapter is the one named in `_tools/stitch.py`
(`CFGS`) and `_pipe/build_outputs.py` (`CFG`); select it with the environment variable `UDAY_CFG`.

1. **Plan and config.** `chNN/chNN_plan_vK.md` (unit headings `## N.x Title *(…)*`) and `chNN/cfg_chNNvK.py`
   (CH, SECTIONS, OUTLINE, PACK, canon rules, `extra_rules`).
2. **Evidence pack.** `chNN/evidence_pack_vK.json` is in git. To rebuild it: the previous pack plus new slices,
   `_tools/kb_new.py` then `_tools/pack_add_kbn.py`.
3. **Draft the sections** into `run/chN/N.x.md`. Drafting was done in agent sessions following
   `run/DRAFTING_BRIEF.md`, `run/LINE_EDIT_BRIEF.md` and `style/` (one `{{note}}` per paragraph, every claim tied to
   pack IDs). This step is not deterministic; everything after it is.
4. **Check until clean.** `UDAY_CFG=drafting/chNN/cfg_chNNvK.py python -I drafting/_pipe/inhouse.py check`, plus
   `python -I drafting/_tools/ch_rules.py drafting/chNN/cfg_chNNvK.py` for the chapter's canon rules.
5. **Assemble.** `python -I drafting/_tools/stitch.py` (stitched chapter), then
   `python -I drafting/_pipe/build_outputs.py --chapters N` (footnoted markdown and .docx), then the ledger
   (`run/ledger/ledger_chN.json`, `python -I drafting/_pipe/ledger.py merge`).

Chapter state, decisions and open research items: `DRAFTING_PROGRESS.md`, `ROADMAP.md`, `editorial/`.
