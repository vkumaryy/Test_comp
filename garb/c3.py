# import PyPDF2
# import re
# from openpyxl import Workbook

# def extract_clean_text(pdf_path):
#     """
#     Extracts clean text from the first page of a PDF.

#     Args:
#         pdf_path (str): Path to the PDF file.

#     Returns:
#         str: Extracted text with minimal garbage data.
#     """

#     try:
#         # Open PDF in binary read mode
#         with open(pdf_path, 'rb') as pdf_file:
#             pdf_reader = PyPDF2.PdfReader(pdf_file)

#             # Extract text from the first page
#             page = pdf_reader.pages[0]
#             text = page.extract_text()

#             # Preprocessing steps to remove common garbage (adjust as needed)
#             text = text.strip()  # Remove leading/trailing whitespace
#             text = text.replace('\n\n', '\n')  # Combine redundant newlines
#             text = re.sub(r'[^\w\s\.\,\:\!\?\-]', '', text, flags=re.UNICODE)  # Remove non-alphanumeric characters (except common punctuation)

#             return text

#     except (FileNotFoundError, PyPDF2.PdfReadError) as e:
#         print(f"Error processing PDF: {e}")
#         return ""

# def extract_key_fields(text):
#     """
#     Extracts key fields from the cleaned text.

#     Args:
#         text (str): Cleaned text extracted from the PDF.

#     Returns:
#         dict: Dictionary containing extracted key fields.
#     """
#     key_fields = {}

#     # Implement your logic to extract key fields here

#     return key_fields

# def create_spreadsheet_report(pdf_path, clean_text, key_fields):
#     """
#     Creates a spreadsheet report with details extracted from the PDF.

#     Args:
#         pdf_path (str): Path to the PDF file.
#         clean_text (str): Cleaned text extracted from the PDF.
#         key_fields (dict): Dictionary containing extracted key fields.
#     """
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "PDF Report"

#     # Write headers
#     ws.append(["PDF Path", "Cleaned Text", "Key Field 1", "Key Field 2", "Key Field 3"])  # Add more fields as needed

#     # Write data
#     ws.append([pdf_path, clean_text] + list(key_fields.values()))

#     # Save the workbook
#     report_path = pdf_path.replace('.pdf', '_report.xlsx')  # Output report path
#     wb.save(report_path)
#     print(f"Report created successfully: {report_path}")

# if __name__ == "__main__":
#     pdf_path = "/home/vikash/Downloads/garb.pdf"  # Replace with your PDF path
#     clean_text = extract_clean_text(pdf_path)

#     if clean_text:
#         key_fields = extract_key_fields(clean_text)
#         create_spreadsheet_report(pdf_path, clean_text, key_fields)
#     else:
#         print("No text extracted from PDF.")


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
      str: Extracted text with minimal garbage data.
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
    return ""

if __name__ == "__main__":
  # Try to fix the PDF first (replace paths as needed)
  corrupt_pdf_path = Path("/home/vikash/Downloads/garb.pdf")
  repaired_pdf_path = Path("/home/vikash/Downloads/garb.pdf")
  fix_pdf(corrupt_pdf_path, repaired_pdf_path)

  # Extract text from the repaired PDF
  pdf_path = repaired_pdf_path  # Use the repaired PDF path here
  clean_text = extract_clean_text(pdf_path)

  if clean_text:
    print(clean_text)
  else:
    print("No text extracted from PDF.")
