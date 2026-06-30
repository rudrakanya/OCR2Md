# Rebuild the Book with the Vector Knowledge Base — Step-by-Step Guide

This guide shows you how to rebuild the seven-chapter book from the reference
texts, **chapter by chapter**, using a Mistral-powered "vector knowledge base"
for facts and a writing sample for voice. **No prior experience needed** — just
follow the steps in order, in the **VSCode PowerShell terminal** on Windows.

Everything you need comes with the repository, except your own Mistral API key.

---

## TL;DR — the whole workflow (6 commands)

Once setup (Part A) is done, this is the entire rebuild:

```powershell
python build_kb.py "Udaypur Reference Markdown Files"   # 1. build the knowledge base (once)
python kb_search.py "Udayesvara temple architecture" -k 5   # 2. (optional) test it
python make_evidence.py                                  # 3. gather evidence per chapter
python draft_chapter.py all                              # 4. write all seven chapters
python assemble_book.py                                  # 5. stitch into one manuscript
python validate_book.py                                  # 6. quick quality check
```

Output appears in the `book/` folder. The sections below explain each step.

---

## Part A — One-time setup (do this once)

### 1. Check you have Python 3.10 or newer
In the terminal:
```powershell
python --version
```
If it's missing or older than 3.10, install it from <https://www.python.org/downloads/>
(tick "Add Python to PATH" during install).

### 2. Get a free Mistral API key
Go to <https://console.mistral.ai/> → sign in → **API Keys** → create one. Copy it.

### 3. Open the project in VSCode
`File ▸ Open Folder…` and pick the project folder. Then open a terminal:
`Terminal ▸ New Terminal`. Make sure the dropdown next to the `+` says **PowerShell**.

### 4. Create and turn on a "virtual environment"
This keeps the project's packages separate from the rest of your computer.
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If you see a red error about *"running scripts is disabled"*, run this once and try
the activate line again:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
When it works, the prompt starts with `(.venv)`. **Keep this terminal open** and run
every command below in it.

### 5. Install the required packages
```powershell
pip install -r requirements.txt
```

### 6. Put your API key in a `.env` file
```powershell
Copy-Item .env.example .env
notepad .env
```
In Notepad, set the first line to your key, then save and close:
```
MISTRAL_API_KEY=paste-your-key-here
```
> The `.env` file is private and never uploaded. Don't share your key.

You're ready. ✅

---

## Part B — Build the book

> Tip: file/folder names with spaces **must be in quotes**, exactly as shown.

### Step 1 — Build the knowledge base (once)
```powershell
python build_kb.py "Udaypur Reference Markdown Files"
```
This reads all the reference texts, breaks them into small pieces, and turns each
piece into a searchable "vector." It takes a few minutes and costs about $0.10.
It creates a `kb/` folder.
*You only do this once* — running it again is instant and says *"KB is up to date"*
unless the source texts change (use `--force` to rebuild on purpose).

### Step 2 — (Optional) Test the search
```powershell
python kb_search.py "origin of the Paramara dynasty" -k 5
```
You should see a few relevant passages with scores around **0.8+**. That means the
knowledge base is healthy.

### Step 3 — Gather the evidence for each chapter
```powershell
python make_evidence.py
```
For every chapter, this searches the knowledge base and saves the best passages to
`book\_evidence\chNN.md`. These are the *facts* each chapter will be written from.
(To do just some chapters: `python make_evidence.py --chapters 1,2`.)

### Step 4 — Write the chapters
Do one at a time and read each before continuing:
```powershell
python draft_chapter.py 1
```
Open `book\chapter-01.md` and read it. If it looks good, keep going — or write all
of them at once:
```powershell
python draft_chapter.py all
```
Each chapter is written by a Mistral model from **only** that chapter's evidence,
in third-person history style, matching the cadence of the writing sample (found
automatically in the `writing sample ocr` folder). Anything the sources don't
support is flagged `[GAP — not in sources]`.

### Step 5 — Assemble and check
```powershell
python assemble_book.py     # -> book\The_Rising_Lord_manuscript.md (title page + all chapters + bibliography)
python validate_book.py     # prints a per-chapter check: endnotes line up, diacritics intact, no garbled text
```

That's the whole book. 🎉

---

## What's happening under the hood (plain English)

- **Mistral API** gives us two things: *embeddings* (turn text into numbers that
  capture meaning, so we can search by idea, not keywords) and *chat* (write the
  prose). Both use your `MISTRAL_API_KEY`.
- **Vector knowledge base (`kb/`)**: every reference passage is stored as an
  embedding. To find what a chapter needs, we embed the search query and pick the
  passages whose meaning is closest. Those passages are the *only* facts the
  writer is allowed to use — this is what keeps the book grounded and accurate.
- **The voice**: chapters are written in the **third person**, at the level of a
  serious history book, borrowing the flowing, literary rhythm of the handwriting
  sample (not its personal "I" diary tone).

---

## Customizing the book

Everything about the chapters — titles, what each one covers, and the search
queries used to gather its evidence — lives in **one file: `book_outline.py`**.
To change a chapter, edit it there, then re-run `make_evidence.py` and
`draft_chapter.py`. (Because all the scripts read this one file, they always stay
in sync.)

Other handy options:
- `python draft_chapter.py 3 --model mistral-medium-latest` — use a cheaper/faster model.
- `python build_kb.py "<folder>" --force` — force a rebuild of the knowledge base.
- Set `MISTRAL_CHAT_MODEL` / `MISTRAL_EMBED_MODEL` in `.env` to change defaults.

---

## Troubleshooting

| Message | Fix |
|---|---|
| `MISTRAL_API_KEY is not set` | You skipped step A.6, or `.env` is empty. |
| `Activate.ps1 cannot be loaded` | Run the `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` line, then activate again. |
| `ModuleNotFoundError` | The venv isn't on (no `(.venv)` in the prompt) — re-activate and re-run `pip install -r requirements.txt`. |
| `Knowledge base not found in 'kb/'` | Run Step 1 first. |
| `missing evidence pack …` | Run Step 3 (`make_evidence.py`) before Step 4. |
| Garbled Devanagari/accents in the terminal | Just the console display — the saved `.md` files are correct; open them in VSCode to confirm. |

---

## Notes
- Cost: building the knowledge base is ~$0.10; writing all seven chapters is a few
  cents to ~$1, depending on length.
- The drafts are a **starting point** — verify dates, names, and quotations against
  the original sources before publishing, and respect the copyright of the source
  scholarship (this produces transformative synthesis with attribution).
