import os
import sys
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def combine_pdfs(directory, max_pages=5):
    """Combine all PDFs in a directory into a single PDF."""
    dir_path = Path(directory)

    if not dir_path.is_dir():
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    # Get all PDF files in the directory (sorted)
    pdf_files = sorted(dir_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory}")
        sys.exit(1)

    # Create writer object
    writer = PdfWriter()

    # Add first max_pages of each PDF to writer
    for pdf_file in pdf_files:
        print(f"Adding: {pdf_file.name}")
        reader = PdfReader(str(pdf_file))
        # Add only the first max_pages (or fewer if PDF has less than max_pages)
        pages_to_add = min(max_pages, len(reader.pages))
        for page_num in range(pages_to_add):
            writer.add_page(reader.pages[page_num])

    # Create output filename
    output_file = f"{dir_path.name}.pdf"
    output_path = dir_path.parent / output_file

    # Write combined PDF
    with open(str(output_path), "wb") as output_pdf:
        writer.write(output_pdf)

    # Get and print file size
    file_size = output_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"Combined PDF saved to: {output_path}")
    print(f"File size: {file_size:,} bytes ({file_size_mb:.2f} MB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m pdf_combiner <directory> [max_pages]")
        sys.exit(1)

    max_pages = 5  # Default value
    if len(sys.argv) >= 3:
        try:
            max_pages = int(sys.argv[2])
        except ValueError:
            print(f"Error: max_pages must be an integer, got '{sys.argv[2]}'")
            sys.exit(1)

    combine_pdfs(sys.argv[1], max_pages)
