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


import PyPDF2
import re

def extract_clean_text(pdf_path):
    """
    Extracts clean text from the first page of a PDF, optimized for speed.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text with minimal garbage data.
    """

    try:
        # Open PDF in binary read mode (faster than opening in text mode)
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from the first page (optimized for speed)
            page = pdf_reader.pages[0]
            text = page.extract_text(extract_mode='content')  # Faster extraction mode

            # Basic preprocessing for speed (adjust as needed)
            text = text.strip()  # Remove leading/trailing whitespace

            return text

    except (FileNotFoundError, PyPDF2.PdfReaderError) as e:
        print(f"Error processing PDF: {e}")
        return ""

# Example usage (assuming you have a separate function for key field extraction and report generation)
if __name__ == "__main__":
    pdf_path = "path/to/your/pdf.pdf"
    clean_text = extract_clean_text(pdf_path)

    if clean_text:
        # Further processing for key field extraction (replace with your logic)
        key_fields = extract_key_fields(clean_text)

        # Generate spreadsheet report (replace with your logic)
        generate_report(key_fields)
    else:
        print("No text extracted from PDF.")

