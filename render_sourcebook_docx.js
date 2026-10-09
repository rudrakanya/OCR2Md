// Render BOOK_SOURCEBOOK.md as a compact Word document for circulation.
//   node render_sourcebook_docx.js [excerptsPerChapter]
//
// Target: ~36 pages. Everything load-bearing is kept — coverage, every key
// fact, gaps, the code table and the coverage matrix. What is capped is the
// excerpt pool, which is illustrative backing and survives in full in
// BOOK_SOURCEBOOK.md; each chapter says how many it is showing of how many.
//
// There is no LibreOffice or pandoc on this machine, so the page count is
// ESTIMATED from a line budget, not observed. The estimator prints its working.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, PageOrientation,
  Header, Footer, PageNumber,
} = require("docx");

const HERE = __dirname;
const SRC = path.join(HERE, "BOOK_SOURCEBOOK.md");
const OUT = path.join(HERE, "BOOK_SOURCEBOOK.docx");
const EXCERPTS_PER_CHAPTER = Number(process.argv[2] || 12);   // tuned to land near 36 pages

const LETTER = { width: 12240, height: 15840 };
const MARGIN = { top: 900, bottom: 900, left: 900, right: 900 };
const TEXT_W = LETTER.width - MARGIN.left - MARGIN.right;        // 10440
const LAND_W = LETTER.height - MARGIN.left - MARGIN.right;       // 14040
const COL_GAP = 340;
const COL_W = Math.floor((TEXT_W - COL_GAP) / 2);

// Layout constants the estimator and the renderer must agree on.
const BODY_PT = 9, CITE_PT = 8;
const LINES_PER_COL = 66, CHARS_1COL = 104, CHARS_2COL = 54;

// --- inline markdown ------------------------------------------------------
function runs(text, base = {}) {
  const clean = text.replace(/\[([^\]]+)\]\(#[^)]*\)/g, "$1");
  const out = [];
  const rx = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = rx.exec(clean)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: clean.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else if (tok.startsWith("`"))
      out.push(new TextRun({ text: tok.slice(1, -1), font: "Consolas", size: (base.size || 18) - 2,
                             color: "7A3E00", ...base, font: "Consolas" }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < clean.length) out.push(new TextRun({ text: clean.slice(last), ...base }));
  return out.length ? out : [new TextRun({ text: "", ...base })];
}

const cells = (l) => l.split("|").slice(1, -1).map((c) => c.trim());

function table(lines, width, pt) {
  const header = cells(lines[0]);
  const body = lines.slice(2).map(cells).filter((r) => r.length === header.length);
  const n = header.length;
  const first = n > 6 ? Math.round(width * 0.085) : Math.round(width * 0.17);
  const rest = Math.floor((width - first) / (n - 1));
  const widths = [first, ...Array(n - 1).fill(rest)];
  const mk = (txt, i, head) =>
    new TableCell({
      width: { size: widths[i], type: WidthType.DXA },
      shading: head ? { type: ShadingType.CLEAR, fill: "EEEEEE" } : undefined,
      margins: { top: 20, bottom: 20, left: 60, right: 60 },
      children: [new Paragraph({ children: runs(txt, { size: pt * 2, bold: head }),
                                 spacing: { after: 0, line: 200 } })],
    });
  return new Table({
    columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => mk(h, i, true)) }),
           ...body.map((r) => new TableRow({ children: r.map((c, i) => mk(c, i, false)) }))],
  });
}

// --- trim the excerpt pool, keeping the strongest per sub-theme -----------
function capExcerpts(md, perChapter) {
  const out = [];
  const lines = md.split(/\r?\n/);
  let kept = 0, seen = 0, chapterSeen = 0, chapterKept = 0;
  const flush = [];
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (/^## (C\d+|AF) — /.test(l)) { chapterSeen = 0; chapterKept = 0; }
    if (l.startsWith("> ") && !l.startsWith("> — ")) {
      seen++; chapterSeen++;
      const cite = lines[i + 1] && lines[i + 1].startsWith("> — ") ? lines[i + 1] : null;
      if (chapterKept < perChapter) {
        chapterKept++; kept++;
        out.push(l);
        if (cite) out.push(cite);
      }
      if (cite) i++;
      continue;
    }
    out.push(l);
  }
  return { md: out.join("\n"), kept, seen };
}

// --- estimator ------------------------------------------------------------
function estimate(blocks) {
  let lines = 0;
  for (const b of blocks) lines += b;
  return lines / LINES_PER_COL;
}

// --- block parser ---------------------------------------------------------
function build(md, width, twoCol, tally) {
  const out = [];
  const perLine = twoCol ? CHARS_2COL : CHARS_1COL;
  const add = (chars, extra = 0) => tally.push(Math.max(1, Math.ceil(chars / perLine)) + extra);
  const lines = md.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const line = raw.trimEnd();
    if (!line.trim()) continue;
    if (/^\[↑ contents\]/.test(line.trim()) || line.startsWith("<a id=")) continue;

    if (line.trim().startsWith("|")) {
      const block = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) block.push(lines[i].trim()), i++;
      i--;
      if (block.length >= 2) {
        out.push(table(block, width, twoCol ? 7 : 7.5));
        out.push(new Paragraph({ text: "", spacing: { after: 60 } }));
        tally.push(block.length * 1.15 + 1);
      }
      continue;
    }
    if (line.startsWith("# ")) {
      out.push(new Paragraph({ children: runs(line.slice(2), { size: 30, bold: true }),
                               spacing: { after: 140 } }));
      add(line.length, 1);
    } else if (line.startsWith("## ")) {
      out.push(new Paragraph({ children: runs(line.slice(3), { size: 22, bold: true, color: "1F3864" }),
                               heading: HeadingLevel.HEADING_1, keepNext: true,
                               spacing: { before: 200, after: 90 } }));
      add(line.length, 1.5);
    } else if (line.startsWith("### ")) {
      out.push(new Paragraph({ children: runs(line.slice(4), { size: 18, bold: true, color: "404040" }),
                               heading: HeadingLevel.HEADING_2, keepNext: true,
                               spacing: { before: 120, after: 50 } }));
      add(line.length, 0.5);
    } else if (line.startsWith("> — ")) {
      out.push(new Paragraph({ children: runs(line.slice(4), { size: CITE_PT * 2, color: "555555" }),
                               indent: { left: 240 }, spacing: { after: 70, line: 200 } }));
      add(line.length, 0.2);
    } else if (line.startsWith("> ")) {
      out.push(new Paragraph({ children: runs(line.slice(2), { size: BODY_PT * 2 }),
                               indent: { left: 240 }, spacing: { after: 20, line: 200 },
                               border: { left: { style: BorderStyle.SINGLE, size: 6,
                                                 color: "CCCCCC", space: 6 } } }));
      add(line.length);
    } else if (/^\s{2,}- /.test(raw)) {
      out.push(new Paragraph({ children: runs(line.trim().slice(2), { size: 16, color: "444444" }),
                               indent: { left: 420, hanging: 150 }, spacing: { after: 30, line: 200 } }));
      add(line.length);
    } else if (line.startsWith("- ")) {
      out.push(new Paragraph({ children: runs(line.slice(2), { size: BODY_PT * 2 }),
                               bullet: { level: 0 }, spacing: { after: 40, line: 200 } }));
      add(line.length, 0.2);
    } else {
      out.push(new Paragraph({ children: runs(line, { size: BODY_PT * 2 }),
                               spacing: { after: 80, line: 200 },
                               alignment: AlignmentType.JUSTIFIED }));
      add(line.length, 0.3);
    }
  }
  return out;
}

// --- assemble -------------------------------------------------------------
let md = fs.readFileSync(SRC, "utf8");
const trim = capExcerpts(md, EXCERPTS_PER_CHAPTER);
md = trim.md;

const firstChapter = md.indexOf("## C1 — ");
const matrixAt = md.indexOf("## Coverage matrix");
let front = md.slice(0, firstChapter);
const body = md.slice(firstChapter, matrixAt);
const matrix = md.slice(matrixAt);

front += `\nThis Word edition shows the ${trim.kept} strongest excerpts of ${trim.seen}` +
         ` (up to ${EXCERPTS_PER_CHAPTER} per chapter), chosen by the same ranking. Every key fact,` +
         ` coverage summary, gaps note, source code and matrix cell is here in full;` +
         ` BOOK_SOURCEBOOK.md carries the complete excerpt set.\n`;

const tallyFront = [], tallyBody = [], tallyMatrix = [];
const frontBlocks = build(front, TEXT_W, false, tallyFront);
const bodyBlocks = build(body, COL_W, true, tallyBody);
const matrixBlocks = build(matrix, LAND_W, false, tallyMatrix);

const pagesFront = estimate(tallyFront);
const pagesBody = estimate(tallyBody) / 2;      // two columns per page
const pagesMatrix = estimate(tallyMatrix);
const total = pagesFront + pagesBody + pagesMatrix;

const footer = new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ children: ["Udaypur sourcebook · ", PageNumber.CURRENT, " of ",
                                      PageNumber.TOTAL_PAGES], size: 14, color: "777777" })] })] });
const header = new Header({ children: [new Paragraph({
  alignment: AlignmentType.RIGHT,
  children: [new TextRun({ text: "Udaypur book — sourcebook (generated from the knowledge base)",
                           size: 13, color: "999999" })] })] });

const doc = new Document({
  creator: "Udaypur book pipeline",
  title: "The Udaypur book — sourcebook",
  description: "Per-chapter key facts over cited KB excerpts",
  sections: [
    { properties: { page: { size: LETTER, margin: MARGIN } },
      headers: { default: header }, footers: { default: footer }, children: frontBlocks },
    { properties: { page: { size: LETTER, margin: MARGIN },
                    column: { count: 2, space: COL_GAP, equalWidth: true } },
      headers: { default: header }, footers: { default: footer }, children: bodyBlocks },
    { properties: { page: { size: { ...LETTER, orientation: PageOrientation.LANDSCAPE },
                            margin: MARGIN } },
      headers: { default: header }, footers: { default: footer }, children: matrixBlocks },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  try {
    fs.writeFileSync(OUT, buf);
    console.log(`wrote ${OUT} ${(buf.length / 1024).toFixed(0)} KB`);
  } catch (e) {
    if (e.code !== "EBUSY" && e.code !== "EPERM") throw e;
    const alt = OUT.replace(/\.docx$/, "_new.docx");
    fs.writeFileSync(alt, buf);
    console.log(`BOOK_SOURCEBOOK.docx is open in Word — wrote ${alt} instead ` +
                `${(buf.length / 1024).toFixed(0)} KB`);
  }
  console.log(`excerpts kept ${trim.kept} of ${trim.seen} (cap ${EXCERPTS_PER_CHAPTER}/chapter)`);
  console.log(`estimated pages: front ${pagesFront.toFixed(1)} + chapters ${pagesBody.toFixed(1)}` +
              ` + matrix ${pagesMatrix.toFixed(1)} = ${total.toFixed(1)}  (calculated, not observed)`);
});
