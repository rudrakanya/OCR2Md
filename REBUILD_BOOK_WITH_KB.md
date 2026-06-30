# Rebuilding the Book with the Vector Knowledge Base — Collaborator Guide

This guide lets a teammate reproduce the seven-chapter book **chapter by chapter**
from the reference texts, using a **Mistral-powered vector knowledge base** for
grounding and the **writing-style sample** for voice. Every command is written
for the **VSCode integrated PowerShell terminal** on Windows.

```
 reference .md ──build_kb.py──▶  kb/ (vector store)
                                   │
 "writing sample ocr" ─OCR──▶ style reference
                                   │            make_evidence.py (per chapter)
                                   ▼                     │
                          draft_chapter.py  ◀── book/_evidence/chNN.md
                                   │
                                   ▼
                        book/chapter-NN.md ──assemble_book.py──▶ full manuscript
```

---

## 1. How it works (read this first)

### The Mistral API — two endpoints we use
- **Embeddings** (`mistral-embed`): turns a piece of text into a 1,024-number
  vector ("embedding") that captures its meaning. Similar passages get similar
  vectors. We embed the reference corpus once.
- **Chat** (`mistral-large-latest`): a text-generation model. We give it the
  *retrieved* source passages plus style/voice instructions, and it writes a
  chapter grounded in those passages.

Both are reached through the official `mistralai` Python SDK using your
`MISTRAL_API_KEY`.

### The vector knowledge base (`kb/`)
1. **Chunk** — every `.md` reference file is split into ~350–450-word chunks,
   each tagged with its source file and heading.
2. **Embed** — each chunk is embedded with `mistral-embed`; the vectors are
   L2-normalized and saved.
3. **Retrieve** — to answer a query, we embed the query and take the chunks
   whose vectors are most similar (cosine similarity = a dot product on the
   normalized vectors). This is *semantic* search: it finds passages by meaning,
   not keywords.
4. **Ground (RAG)** — those retrieved chunks become the *only* facts the chat
   model is allowed to use when drafting. This is "retrieval-augmented
   generation," and it is what keeps the book grounded in the sources.

The prebuilt store has **5,377 chunks** and lives in three files:
`kb/embeddings.npy` (the vectors), `kb/chunks.jsonl` (the text + metadata),
`kb/config.json` (model + dimensions). You will rebuild these in Step 1.

### The drafting voice
Chapters are written in **third person**, at the register and complexity of a
serious history book, but carrying the **flowing, literary cadence of the
handwriting sample** in `writing sample ocr/` (long sentences, em-dash asides,
elevated diction) — *not* its first-person diary voice. That voice spec is built
into `draft_chapter.py`; the OCR'd sample is fed in as an extra exemplar.

---

## 2. Prerequisites
- **Python 3.10+** (`python --version`).
- **VSCode** with the Python extension.
- A **Mistral API key** — create one free at <https://console.mistral.ai/> → *API Keys*.
- The **project files** (clone the repo) **plus two data folders that are not in
  the public repo** and must be obtained from the project owner / shared drive:
  - `Udaypur Reference Markdown Files/` — the source corpus.
  - `writing sample ocr/` — the handwriting style sample (images).
  Place both inside the project folder before you start.

---

## 3. One-time setup (VSCode + PowerShell)

1. **Open the project in VSCode:** `File ▸ Open Folder…` → select the
   `markdown extractor` (project) folder.
2. **Open a PowerShell terminal:** `Terminal ▸ New Terminal`. Make sure it says
   *PowerShell* (use the `∨` dropdown next to the `+` to pick *PowerShell* if not).
   The prompt should already be in the project folder.
3. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If activation is blocked with a "running scripts is disabled" error, run this
   once in the same terminal and try again:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
   You should now see `(.venv)` at the start of the prompt.
4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
5. **Add your Mistral key.** Copy the template and edit it:
   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```
   Set the line to your key (no quotes, no spaces):
   ```
   MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   `.env` is git-ignored — never commit your key.

> Run **every** command below from this same activated PowerShell terminal, from
> the project root. Folder names with spaces **must be quoted** (`"like this"`).

---

## 4. Step 1 — Build the vector knowledge base
```powershell
python build_kb.py "Udaypur Reference Markdown Files"
```
This chunks and embeds the whole corpus (a few minutes; ~$0.10 of embeddings).
It creates the `kb/` folder: `embeddings.npy`, `chunks.jsonl`, `config.json`.
You only need to rebuild it if the source texts change.

## 5. Step 2 — Sanity-check retrieval
```powershell
python kb_search.py "bhumija sikhara plan of the Udayesvara temple" -k 5
python kb_search.py "origin of the Paramara Rajput dynasty Agnikula" -k 5
```
You should see relevant passages with similarity scores around **0.8+**. If so,
the KB is healthy.

## 6. Step 3 — Prepare the writing-style reference
OCR the handwriting sample into Markdown so the drafter can imitate its cadence:
```powershell
python ocr_to_markdown.py "writing sample ocr" --output-dir output
```
This writes `output\writing sample ocr\*.md`. `draft_chapter.py` auto-detects it;
no further action needed. (Remember: the *voice* used is third-person history —
the sample supplies rhythm and texture, not the first-person diary tone.)

## 7. Step 4 — Generate per-chapter evidence packs
```powershell
python make_evidence.py
```
For each of the seven chapters this runs several KB searches and writes the top
retrieved passages to `book\_evidence\ch01.md … ch07.md`. These are the grounded
"source dossiers" each chapter is written from.

## 8. Step 5 — Draft the chapters (the chapter-by-chapter rebuild)
Draft one chapter at a time and review each before moving on:
```powershell
python draft_chapter.py 1
```
Open `book\chapter-01.md`, read it, and if the voice/grounding look right,
continue:
```powershell
python draft_chapter.py 2
python draft_chapter.py 3
# …through 7, or all at once:
python draft_chapter.py all
```
Each call sends that chapter's evidence pack + the style reference + the
third-person history voice spec to `mistral-large-latest`, and writes
`book\chapter-NN.md` with numbered endnotes. Drafts are grounded **only** in the
evidence; anything unsupported is marked `[GAP — not in sources]`.

## 9. Step 6 — Assemble and validate
```powershell
python assemble_book.py     # -> book\The_Rising_Lord_manuscript.md (+ contents + bibliography)
python validate_book.py     # per-chapter checks: endnote consistency, IAST, no mojibake
```

---

## 10. Customizing the rebuild
- **Retrieval per chapter:** edit the `QUERIES` dictionary in `make_evidence.py`
  (add/replace the search phrases for any chapter), then re-run `make_evidence.py`.
- **Chapter titles / scope:** edit the `CHAPTERS` dictionary in `draft_chapter.py`.
- **Models:** override per run with `--model`, e.g.
  `python draft_chapter.py 1 --model mistral-medium-latest`, or set
  `MISTRAL_CHAT_MODEL` / `MISTRAL_EMBED_MODEL` in `.env`.
- **Style file:** pass a specific exemplar with
  `python draft_chapter.py 1 --style-file "output\writing sample ocr\<name>.md"`.

## 11. Troubleshooting (PowerShell)
- **`MISTRAL_API_KEY not set`** — `.env` is missing or empty; redo Step 3.5.
- **`Activate.ps1 cannot be loaded`** — run the `Set-ExecutionPolicy -Scope
  Process -ExecutionPolicy Bypass` line, then activate again.
- **`ModuleNotFoundError`** — the venv isn't active (no `(.venv)` in the prompt)
  or deps aren't installed; re-activate and `pip install -r requirements.txt`.
- **`No .md files in …` / path errors** — quote folder names with spaces, and run
  from the project root.
- **Garbled Devanagari/diacritics in the terminal** — that's just the console
  display; the saved `.md` files are correct UTF-8 (open them in VSCode to verify).
- **Inline `python -c "…"` quoting fails in PowerShell** — don't; run the project
  scripts directly as shown.

## 12. Cost & notes
- Embedding the corpus is roughly **$0.10**; drafting seven chapters with
  `mistral-large-latest` is a few cents to ~$1 depending on length.
- Drafts are a **starting point**: verify dates, names, and quotations against the
  original sources before any publication, and respect the copyright of the
  source scholarship (this workflow produces transformative synthesis with
  attribution, not reproduction).
