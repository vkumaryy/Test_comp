import PyPDF2
import json

def extract_all_text_from_page(file_path, page_num=0):
  """
  This function extracts all text content from a specific page of a PDF using PyPDF2.

  Args:
      file_path: The path to the PDF file.
      page_num (optional): The page number to extract text from (defaults to 0).

  Returns:
      A string containing the extracted text or None if there's an error.
  """
  try:
    # Open the PDF with PyPDF2
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the specified page
    page = pdf_reader.pages[page_num]

    # Extract text from the page using a text extractor (may require installation)
    text = page.extract_text()  # Might require installing a text extractor like 'textract'

    # Close the PDF file
    pdf_file.close()

    return text

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None

# Replace 'path/to/your/file.pdf' with the actual path to your PDF
file_path = 'path/to/your/file.pdf'

# Extract text from the first page
text_data = extract_all_text_from_page(file_path)

# Convert text data to JSON (if successful)
if text_data:
  json_data = json.dumps({"text": text_data})
  print(json_data)
else:
  print("Failed to extract text from PDF.")



import fitz  # PyMuPDF library for working with PDFs
import re
import json

def extract_invoice_data_from_page(file_path, page_num=0):
  """
  Extracts all identifiable data points from the first page of an invoice PDF using fitz.

  Args:
      file_path: The path to the PDF file.
      page_num (optional): The page number to extract data from (defaults to 0).

  Returns:
      A dictionary containing extracted invoice data or None if there's an error.
  """

  try:
    # Open the PDF with PyMuPDF (basic validation)
    doc = fitz.open(file_path)
    if not doc.is_pdf:
      raise ValueError("Invalid PDF file.")

    # Get the first page
    page = doc.loadPage(page_num)

    # Extract text from the page and clean (remove unwanted characters)
    text = page.get_text("text")
    text = re.sub(r"\n\s*", "\n", text).strip()  # Remove extra newlines and spaces

    # Initialize empty dictionary for invoice data
    invoice_data = {}

    # Extract data using generic patterns and heuristics (adjust as needed)
    patterns = {
        "company_name": r"(?:Company|Supplier|Vendor):(.*?)\n[Original for Recipient]",
        "company_address": None,  # Extract from company_name block
        "invoice_number": r"(?:Invoice|Bill) No :(\w+)",
        "date": r"(?:Date|Issue Date) : (\d{2} [A-Z][a-z]{2} \d{4})|(?:Date) : (\d{2} [A-Z][a-z]{2} \d{2})",  # Handle different date formats
        "recipient_name": r"(?:To|Bill To|Recipient):(.*?)\n[PLACE OF SUPPLY]",
        "recipient_address": None,  # Extract from recipient_name block
        "recipient_gstin": r"GSTIN: (\w+)",
        # ... Add more patterns for other data points ...
    }

    for key, pattern in patterns.items():
      if pattern:
        match = re.search(pattern, text, re.DOTALL)
        invoice_data[key] = match.group(1).strip() if match else None

    # Extract company address and recipient address (heuristics)
    if invoice_data.get("company_name"):
      company_info = invoice_data["company_name"].split("\n")
      invoice_data["company_address"] = "\n".join(company_info[1:])
    if invoice_data.get("recipient_name"):
      recipient_info = invoice_data["recipient_name"].split("\n")
      invoice_data["recipient_address"] = "\n".join(recipient_info[1:])

    # Extract items/services (assuming a table structure if possible)
    # ... (code to extract items table data, similar to previous attempts) ...

    # Return extracted invoice data
    return invoice_data

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None

# Replace 'path/to/your/file.pdf' with the actual path to your PDF
file_path = 'path/to/your/file.pdf'

# Extract invoice data from the first page
invoice_data = extract_invoice_data_from_page(file_path)

# Convert invoice data to JSON (if successful)
if invoice_data:
  json_data = json.dumps(invoice_data)
  print(json_data)
else:
  print("Failed to extract invoice data from PDF.")

