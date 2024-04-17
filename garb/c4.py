from borb.pdf import PDF
from pathlib import Path
import re
from openpyxl import Workbook

def fix_pdf(in_path: Path, out_path: Path) -> None:
    """
    Attempts to fix a corrupt PDF by opening and saving with borb.

    Args:
        in_path (Path): Path to the corrupt PDF file.
        out_path (Path): Path to save the repaired PDF file.
    """
    try:
        with open(in_path, "rb") as fh:
            document = PDF.loads(fh)
        with open(out_path, "wb") as fh:
            PDF.dumps(fh, document)
        print("PDF repaired successfully.")
    except Exception as e:
        print(f"Error fixing PDF: {e}")

def extract_text_from_pdf(pdf_path):
    """
    Extracts textual data from a PDF.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        str: Extracted textual data from the PDF.
    """
    try:
        # Load the PDF document using borb
        with open(pdf_path, "rb") as fh:
            document = PDF.loads(fh)

        # Extract text from all pages
        text = ""
        for page in document.pages:
            text += page.get_text() + "\n"  # Add a newline between pages

        return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def create_spreadsheet_report(pdf_path, text):
    """
    Creates a spreadsheet report with text extracted from the PDF.

    Args:
        pdf_path (str): Path to the PDF file.
        text (str): Extracted text from the PDF.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "PDF Report"

    # Write headers
    ws.append(["PDF Path", "Text"])

    # Write data
    ws.append([pdf_path, text])

    # Save the workbook
    report_path = pdf_path.replace('.pdf', '_report.xlsx')  # Output report path
    wb.save(report_path)
    print(f"Report created successfully: {report_path}")

if __name__ == "__main__":
    # Input PDF path (replace with yours)
    pdf_path = Path("/home/vikash/Downloads/garb.pdf")

    # Temporary path for repaired PDF
    repaired_pdf_path = pdf_path.parent / (pdf_path.stem + "_repaired.pdf")

    # Attempt to fix the PDF
    fix_pdf(pdf_path, repaired_pdf_path)

    # Extract text from the PDF
    if repaired_pdf_path.exists():
        extracted_text = extract_text_from_pdf(repaired_pdf_path)
    else:
        extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text is not None:
        print("Extracted Text:")
        print(extracted_text)

        # Create spreadsheet report
        create_spreadsheet_report(pdf_path, extracted_text)
    else:
        print("Error extracting text from PDF.")
