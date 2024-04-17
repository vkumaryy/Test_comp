from borb.pdf import PDF
from pathlib import Path
import re

def fix_and_extract_text(pdf_path):
    """
    Attempts to fix a corrupt PDF and extract text from it.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        str: Extracted textual data from the PDF, or None on error.
    """
    try:
        # Load the PDF document using borb
        with open(pdf_path, "rb") as fh:
            document = PDF.loads(fh)

        # Fix and save the document (to temporary path)
        temp_pdf_path = pdf_path.with_suffix(".fixed.pdf")
        with open(temp_pdf_path, "wb") as fh:
            PDF.dumps(fh, document)

        # Extract text from the fixed PDF
        with open(temp_pdf_path, "rb") as fh:
            fixed_document = PDF.loads(fh)

        # Extract text from all pages
        text = ""
        for page in fixed_document.pages:
            text += page.get_text() + "\n"  # Add a newline between pages

        # Delete the temporary fixed PDF file
        temp_pdf_path.unlink()

        return text

    except Exception as e:
        print(f"Error fixing and extracting text from PDF: {e}")
        return None

if __name__ == "__main__":
    # Input PDF path (replace with yours)
    pdf_path = Path("/home/vikash/Downloads/garb.pdf")

    # Extract text from the fixed PDF
    extracted_text = fix_and_extract_text(pdf_path)

    if extracted_text is not None:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Error extracting text from PDF.")
