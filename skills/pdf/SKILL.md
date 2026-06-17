---
name: pdf
description: >-
  "PDF creation, editing, and analysis with support for text extraction, tables, images, forms, merging/splitting, and rendering. Use when working with PDF documents (.pdf files) for: (1) Creating new PDF documents, (2) Extracting content from PDFs, (3) Editing or modifying existing PDFs, (4) Filling in PDF forms, (5) Merging, splitting, or transforming PDFs, (6) Analyzing PDF content, or any other PDF tasks"
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

### PyMuPDF (fitz) - All-in-one alternative

A single dependency (imported as `pymupdf` or legacy `fitz`) that covers nearly every task in this guide with no system tools and 2–5× the speed of pypdf / pdfplumber. **It is AGPL-3.0 and is deliberately NOT bundled** (`requirements.txt` lists only permissive deps) — treat it as opt-in. Prefer the bundled permissive stack (pypdf / pdfplumber / reportlab / **pypdfium2** for rendering); reach for PyMuPDF only when a task genuinely needs it, and then you **must** apply the license disclosure rule below.

| Capability | fitz API | Notes |
|---|---|---|
| Open / save | `pymupdf.open(path)` / `doc.save(out, incremental=True)` | Auto-repairs damaged PDFs; supports incremental writes |
| Merge / split | `doc.insert_pdf(src)` / `doc.select([0,2,4])` | In-place page manipulation |
| Rotate pages | `page.set_rotation(90)` | |
| Extract text | `page.get_text("text" \| "blocks" \| "words" \| "dict")` | One API, 4+ granularities |
| Extract tables | `page.find_tables()` → `table.to_pandas()` | Built-in; complex merged cells need PyMuPDF Pro |
| Render page → image | `page.get_pixmap(dpi=200).save(...)` | Replaces pdf2image; no Poppler |
| Extract embedded images | `page.get_images(full=True)` + `pymupdf.Pixmap(doc, xref)` | Replaces `pdfimages` CLI |
| OCR scanned PDFs | `page.get_textpage_ocr(language="eng")` | Built-in Tesseract integration |
| Search text | `page.search_for("keyword")` → list of rects | Pair with annotations for auto-highlight |
| Annotations | `page.add_highlight_annot(rect)` / `add_text_annot(point, ...)` | Pypdf cannot create most annotations |
| **Redaction (irreversible)** | `page.add_redact_annot(rect)` + `page.apply_redactions()` | True content removal — pypdf "black box" still leaks text |
| Watermark | `page.show_pdf_page(rect, src_doc, src_page)` | |
| Encrypt | `doc.save(out, encryption=pymupdf.PDF_ENCRYPT_AES_256, owner_pw=..., user_pw=...)` | AES-256 supported |
| Form fields | `page.widgets()` (read) / `page.add_widget(...)` (create) | Pypdf cannot create widgets |
| Vector graphics | `page.get_drawings()` | Extract paths; pdfplumber cannot |
| Markdown export (RAG/LLM) | `pymupdf4llm.to_markdown(doc)` | Separate `pymupdf4llm` package; not bundled, and AGPL like PyMuPDF (opt-in) |

📌 **License disclosure rule** — PyMuPDF is licensed under **AGPL-3.0**. Whenever a task is actually executed using PyMuPDF, you **must** append the following notice to your final reply to the user:

> This task used **PyMuPDF**, licensed under **AGPL-3.0** (https://www.gnu.org/licenses/agpl-3.0.html). If you intend to integrate the result into a closed-source, commercial, or permissively-licensed (MIT / Apache / BSD) project, please review the AGPL terms or consider a commercial license from Artifex (https://artifex.com/licensing/).

## Command-Line Tools (off-host only)

> These CLIs (`poppler-utils`, `qpdf`) are **not present on the host** and are not installed by this skill. On the host, use the pure-Python equivalents: text → `pdfplumber`; render/extract images → `pypdfium2` (`scripts/convert_pdf_to_images.py`) / `pypdf` `page.images`; merge/split/rotate/decrypt → `pypdf`. The commands below are for off-host environments where these tools exist.

### pdftotext (Requires poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf (Requires qpdf)
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs (OCR — limited on host)

OCR needs a Tesseract engine, which is **not available on the host** (neither the `tesseract` binary for `pytesseract` nor for PyMuPDF's `get_textpage_ocr`). On the host you can still rasterize pages with the bundled renderer, but recognizing text from them requires an off-host Tesseract:

```python
# Render pages on-host (pypdfium2, no system tools):
#   python scripts/convert_pdf_to_images.py scanned.pdf out_dir/
# Then OCR the PNGs off-host (where tesseract is installed):
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("out_dir/page_1.png"))
```

If the user needs OCR and only the host is available, tell them it requires a Tesseract install off-host — do not silently skip it.

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```python
# On-host: pypdf extracts embedded images, no system tools.
from pypdf import PdfReader
reader = PdfReader("input.pdf")
n = 0
for page in reader.pages:
    for img in page.images:          # pypdf >= 4
        with open(f"output_prefix-{n:03d}-{img.name}", "wb") as f:
            f.write(img.data)
        n += 1
```
```bash
# Off-host alternative (poppler-utils): pdfimages -j input.pdf output_prefix
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

Pick whichever column fits the task best. If you go with the fitz API, remember to append the AGPL disclosure to your final reply (see the [PyMuPDF section](#pymupdf-fitz---all-in-one-alternative)).

| Task | Tool | Command/Code | fitz API |
|------|-----------|--------------|----------|
| Merge PDFs | pypdf | `writer.add_page(page)` | `doc.insert_pdf(src)` |
| Split PDFs | pypdf | One page per file | `doc.select([i])` + `doc.save(...)` |
| Extract text | pdfplumber | `page.extract_text()` | `page.get_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` | `page.find_tables()` |
| Render page → image | pypdfium2 | `python scripts/convert_pdf_to_images.py in.pdf out_dir/` | `page.get_pixmap(dpi=...)` |
| Extract embedded images | pdfimages (CLI) | `pdfimages -j ...` | `page.get_images(full=True)` |
| Create PDFs | reportlab | Canvas or Platypus | `page.insert_htmlbox(rect, html)` |
| OCR scanned PDFs | pytesseract | Convert to image first | `page.get_textpage_ocr()` |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md | `page.widgets()` |

## Dependencies

**Python packages** — declared in `requirements.txt` and installed by the host's auto-ensure at runtime (no manual `pip install`): `pypdf`, `pdfplumber`, `reportlab`, `Pillow`, `pypdfium2`. All are pure-Python wheels needing no system tools. `pypdfium2` (PDFium) is the on-host page→image renderer — it replaces `pdf2image`, so Poppler is not needed.

**PyMuPDF (`pymupdf`/`fitz`)** is **not** bundled (AGPL-3.0). Use only when truly needed, and apply the license disclosure rule above.

**System tools — off-host only (NOT on the host):**

| Tool | Provides | On-host replacement |
|------|----------|---------------------|
| `poppler` / `poppler-utils` | `pdftotext`, `pdfimages`, `pdf2image` | `pdfplumber` (text) · `pypdfium2` (render) · `pypdf` `page.images` (embedded images) |
| `qpdf` | `qpdf` CLI | `pypdf` (merge/split/rotate/decrypt) |
| `tesseract` | OCR backend | none on host — OCR requires an off-host Tesseract install |

If a task genuinely needs a tool that only exists off-host (e.g. OCR), tell the user what's missing and that it must be run/installed off-host — never silently skip a requested step or hardcode around it.

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md
