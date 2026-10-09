// Render the approved Chapter 1 handoff as Word documents.
//   node chapters/C1/handoff/render_docx.js
// Produces two files from the same approved draft:
//   C1_Udaypur_chapter.docx         the clean chapter — no markers, endnotes as back matter
//   C1_Udaypur_chapter_editor.docx  editor copy — markers, references, provenance appendix
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
} = require("docx");

const HERE = __dirname;
const LETTER = { width: 12240, height: 15840 };          // DXA; US Letter, not A4
const COLS = [900, 1900, 1500, 1500, 900, 4400];         // provenance table, sums to 11100

// --- inline markdown: **bold**, *italic*, `code` -------------------------
function runs(text, base = {}) {
  const out = [];
  const rx = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = rx.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else if (tok.startsWith("`")) out.push(new TextRun({ text: tok.slice(1, -1), font: "Consolas", size: 18, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out.length ? out : [new TextRun({ text: "", ...base })];
}

// A short centred rule, book-style — a paragraph bottom border, never a table.
function sectionRule() {
  return new Paragraph({
    indent: { left: 3600, right: 3600 },
    spacing: { before: 260, after: 260 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "999999", space: 1 } },
    children: [new TextRun({ text: "" })],
  });
}

// The opening words of a section, set in small caps the way a printed book does it.
function leadInRuns(text) {
  const m = /^([^.,;:—]{6,34}?\s\S+)(\s)([\s\S]*)$/.exec(text);
  if (!m || /^[*`]/.test(text)) return runs(text);
  return [new TextRun({ text: m[1], smallCaps: true }), ...runs(m[2] + m[3])];
}

function bodyParagraphs(md, { numberedList = false, leadIn = false } = {}) {
  const out = [];
  let afterHeading = false;
  for (const raw of md.split(/\r?\n/)) {
    const line = raw.trimEnd();
    if (!line.trim()) continue;
    if (/^-{3,}$/.test(line.trim())) { out.push(sectionRule()); continue; }
    if (leadIn && afterHeading && !line.startsWith("#")) {
      out.push(new Paragraph({ children: leadInRuns(line), spacing: { after: 160 },
                               alignment: AlignmentType.JUSTIFIED }));
      afterHeading = false;
      continue;
    }
    afterHeading = line.startsWith("## ");
    if (line.startsWith("# ")) {
      out.push(new Paragraph({ children: runs(line.slice(2)), heading: HeadingLevel.HEADING_1, spacing: { after: 240 } }));
    } else if (line.startsWith("## ")) {
      out.push(new Paragraph({ children: runs(line.slice(3)), heading: HeadingLevel.HEADING_2, spacing: { before: 360, after: 160 } }));
    } else if (line.startsWith("### ")) {
      out.push(new Paragraph({ children: runs(line.slice(4)), heading: HeadingLevel.HEADING_3, spacing: { before: 280, after: 120 } }));
    } else if (numberedList && /^\d+\.\s/.test(line)) {
      out.push(new Paragraph({ children: runs(line), spacing: { after: 80 }, indent: { left: 360, hanging: 360 } }));
    } else {
      out.push(new Paragraph({ children: runs(line), spacing: { after: 160 }, alignment: AlignmentType.JUSTIFIED }));
    }
  }
  return out;
}

// --- provenance appendix: markdown table -> docx table --------------------
function appendixTable(md) {
  const rows = md.split(/\r?\n/).filter((l) => l.trim().startsWith("|"));
  if (!rows.length) return [];
  const cells = (l) => l.split("|").slice(1, -1).map((c) => c.trim());
  const header = cells(rows[0]);
  const body = rows.slice(2).map(cells).filter((r) => r.length === header.length);
  const mk = (text, { bold = false, shaded = false } = {}, i = 0) =>
    new TableCell({
      width: { size: COLS[i] || 1200, type: WidthType.DXA },
      shading: shaded ? { type: ShadingType.CLEAR, fill: "EFEFEF" } : undefined,
      children: [new Paragraph({ children: runs(text, { size: 16, bold }), spacing: { after: 0 } })],
    });
  return [
    new Table({
      columnWidths: COLS,
      width: { size: COLS.reduce((a, b) => a + b, 0), type: WidthType.DXA },
      rows: [
        new TableRow({ tableHeader: true, children: header.map((h, i) => mk(h, { bold: true, shaded: true }, i)) }),
        ...body.map((r) => new TableRow({ children: r.map((c, i) => mk(c, {}, i)) })),
      ],
    }),
  ];
}

function write(children, title, description, file) {
  const doc = new Document({
    creator: "Udaypur book pipeline",
    title,
    description,
    sections: [{
      properties: { page: { size: LETTER, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
      children,
    }],
  });
  return Packer.toBuffer(doc).then((buf) => {
    const out = path.join(HERE, file);
    try {
      fs.writeFileSync(out, buf);
      console.log("wrote", out, (buf.length / 1024).toFixed(0) + " KB");
    } catch (e) {
      if (e.code !== "EBUSY" && e.code !== "EPERM") throw e;
      console.error("SKIPPED " + file + " — the file is open in Word; close it and re-run");
    }
  });
}

// --- editor copy ----------------------------------------------------------
const chapter = fs.readFileSync(path.join(HERE, "C1_chapter.md"), "utf8");
const [chapterBody, sourcesBlock] = chapter.split("## Sources cited");
const provenance = fs.readFileSync(path.join(HERE, "provenance_appendix.md"), "utf8");
const provIntro = provenance.split("| note |")[0];

const editor = [
  ...bodyParagraphs(chapterBody, { leadIn: true }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ text: "Sources cited", heading: HeadingLevel.HEADING_2, spacing: { after: 160 } }),
  ...bodyParagraphs(sourcesBlock || "", { numberedList: true }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ text: "Provenance appendix", heading: HeadingLevel.HEADING_2, spacing: { after: 160 } }),
  ...bodyParagraphs(provIntro.replace(/^#.*$/m, "")),
  ...appendixTable(provenance),
];

// --- reading copy: prose with superscript notes, endnotes as back matter ---
const reading = fs.readFileSync(path.join(HERE, "..", "C1_chapter_reading.md"), "utf8");
// Back matter: every work in full exactly once, then the notes that point to it
// by short form. Chunk ids are internal and are stripped for readers.
const backMatter = fs.readFileSync(path.join(HERE, "..", "C1_endnotes.md"), "utf8")
  .replace(/\s*\[kb:[^\]]*\]/g, "");
const worksCited = backMatter.split("## Works cited")[1].split("## Notes")[0];
const notes = backMatter.split("## Notes")[1];

const clean = [
  ...bodyParagraphs(reading, { leadIn: true }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ text: "Works cited", heading: HeadingLevel.HEADING_2, spacing: { after: 160 } }),
  ...bodyParagraphs(worksCited),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ text: "Notes", heading: HeadingLevel.HEADING_2, spacing: { after: 160 } }),
  ...bodyParagraphs(notes, { numberedList: true }),
];

// C1_Udaypur_chapter.docx is the CLEAN chapter — no [src:] ids, no [ed] flags.
// The marked version keeps its provenance under _editor so nothing is lost.
write(clean, "C1 — Udaypur: A Small Town with a Long Memory",
      "Chapter with endnotes; no drafting markers", "C1_Udaypur_chapter.docx")
  .then(() => write(editor, "C1 — Udaypur (editor copy)",
                    "Drafting markers, numbered references and provenance appendix",
                    "C1_Udaypur_chapter_editor.docx"));
