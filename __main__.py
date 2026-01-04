import os
import sys
from pathlib import Path

from PyPDF2 import PdfMerger


def combine_pdfs(directory):
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

    # Create merger object
    merger = PdfMerger()

    # Add all PDFs to merger
    for pdf_file in pdf_files:
        print(f"Adding: {pdf_file.name}")
        merger.append(str(pdf_file))

    # Create output filename
    output_file = f"{dir_path.name}.pdf"
    output_path = dir_path.parent / output_file

    # Write combined PDF
    merger.write(str(output_path))
    merger.close()

    print(f"Combined PDF saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m pdf_combiner <directory>")
        sys.exit(1)

    combine_pdfs(sys.argv[1])
