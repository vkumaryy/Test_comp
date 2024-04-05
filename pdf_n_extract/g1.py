import PyPDF2
import json

def extract_basic_invoice_data(file_path):
  """
  Extracts basic invoice data (company name, invoice number) 
  using PyPDF2 (limited text extraction capabilities).

  Args:
      file_path: The path to the PDF file.

  Returns:
      A dictionary containing extracted invoice data or None if there's an error.
  """

  try:
    # Open the PDF with PyPDF2
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from the first page (limited and unreliable)
    page = pdf_reader.pages[0]  # Use pages[index] instead of getPage(index)
    text = page.extract_text()

    # Initialize empty dictionary for invoice data
    invoice_data = {}

    # Extract company name (heuristic)
    company_name = re.search(r"^(?:Company|Supplier|Vendor):(.*?)\n", text, re.DOTALL)
    invoice_data["company_name"] = company_name.group(1).strip() if company_name else None

    # Extract invoice number (heuristic)
    invoice_number = re.search(r"(?:Invoice|Bill) No : (\w+)", text)
    invoice_data["invoice_number"] = invoice_number.group(1).strip() if invoice_number else None

    # Close the PDF file
    pdf_file.close()

    return invoice_data

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None

# Replace 'path/to/your/file.pdf' with the actual path to your PDF
file_path = 'path/to/your/file.pdf'

# Extract basic invoice data
invoice_data = extract_basic_invoice_data(file_path)

# Convert invoice data to JSON (if successful)
if invoice_data:
  json_data = json.dumps(invoice_data)
  print(json_data)
else:
  print("Failed to extract basic invoice data from PDF.")
