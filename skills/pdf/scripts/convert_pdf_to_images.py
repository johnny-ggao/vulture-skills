import os
import sys

import pypdfium2 as pdfium


# Converts each page of a PDF to a PNG image.
#
# Uses pypdfium2 (a binding for PDFium, Chromium's PDF engine): a pure Python
# wheel with no system tools — no Poppler / pdftoppm required. This is the
# on-host render path; it replaces the previous pdf2image (`convert_from_path`)
# implementation, which needed Poppler.


def convert(pdf_path, output_dir, max_dim=1000, dpi=200):
    pdf = pdfium.PdfDocument(pdf_path)
    try:
        count = len(pdf)
        for i in range(count):
            page = pdf[i]
            # scale is in units of 72dpi; dpi/72 gives the requested rendering DPI.
            bitmap = page.render(scale=dpi / 72.0)
            image = bitmap.to_pil()

            # Scale image if needed to keep width/height under `max_dim`
            width, height = image.size
            if width > max_dim or height > max_dim:
                scale_factor = min(max_dim / width, max_dim / height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                image = image.resize((new_width, new_height))

            image_path = os.path.join(output_dir, f"page_{i+1}.png")
            image.save(image_path)
            print(f"Saved page {i+1} as {image_path} (size: {image.size})")

        print(f"Converted {count} pages to PNG images")
    finally:
        pdf.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_pdf_to_images.py [input pdf] [output directory]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert(pdf_path, output_directory)
