from borb.pdf import Document
from borb.pdf import PDF
from pathlib import Path
import typing

def fix_pdf(in_path: Path, out_path: Path) -> None:
  """
  Attempts to fix a corrupt PDF by opening and saving with borb.

  Args:
      in_path (Path): Path to the corrupt PDF file.
      out_path (Path): Path to save the repaired PDF file.
  """
  doc: typing.Optional[Document] = None
  with open(in_path, "rb") as fh:
    doc = PDF.loads(fh)
  with open(out_path, "wb") as fh:
    PDF.dumps(fh, doc)

import PyPDF2
import re

# Function to extract clean text from a PDF file (first page only)
def extract_clean_text(pdf_path):
    """
    Extracts clean text from the first page of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text with minimal garbage data, or None on error.
    """

    try:
        # Open PDF in binary read mode
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from the first page
            page = pdf_reader.pages[0]
            text = page.extract_text()

            # Preprocessing steps to remove common garbage (adjust as needed)
            text = text.strip()  # Remove leading/trailing whitespace
            text = text.replace('\n\n', '\n')  # Combine redundant newlines
            text = re.sub(r'[^\w\s\.\,\:\!\?\-]', '', text, flags=re.UNICODE)  # Remove non-alphanumeric characters (except common punctuation)

            return text

    except (FileNotFoundError, PyPDF2.PdfReaderError) as e:
        print(f"Error processing PDF: {e}")
        return None  # Indicate error during extraction

if __name__ == "__main__":
    # Input path (replace with yours)
    pdf_path = Path("/home/vikash/Downloads/garb.pdf")

    # Temporary repaired PDF path (can be adjusted)
    repaired_pdf_path = pdf_path.parent / (pdf_path.name + "_repaired.pdf")

    try:
        # Try to fix the PDF (optional repair step)
        fix_pdf(pdf_path, repaired_pdf_path)
        pdf_to_use = repaired_pdf_path
    except Exception as e:  # Catch any errors during repair
        print(f"Error fixing PDF: {e}")
        pdf_to_use = pdf_path  # Fallback to original PDF

    # Extract data (using repaired PDF if available)
    clean_text = extract_clean_text(pdf_to_use)

    if clean_text is not None:
        print(clean_text)
        # Further data extraction logic using clean_text (replace with yours)
    else:
        print("Error extracting data from PDF.")
