import PyPDF2  # For text extraction
import re  # Regular expressions for parsing text
import textract  # Additional text extractor for enhanced capabilities pip install textract
import json

def extract_structured_data_pyPDF2(file_path):
  """
  Extracts text (using PyPDF2 and textract if needed) and parses key data points from the first page of a PDF invoice using regular expressions.

  Args:
      file_path: The path to the PDF file.

  Returns:
      A dictionary containing structured invoice data or None if there's an error.
  """

  try:
    # Open the PDF with PyPDF2
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the first page
    page = pdf_reader.pages[0]

    # Extract text from the page, leveraging textract if PyPDF2 fails
    try:
      text = page.extract_text()
    except:
      text = textract.process(file_path).decode('utf-8')  # Use textract for wider compatibility

    # Close the PDF file
    pdf_file.close()

    # Initialize empty dictionary for invoice data
    invoice_data = {}

    # Parsing logic for requested fields:

    # Vendor Name (assuming it's in the header)
    vendor_name_match = re.search(r"^(.*?)\n", text, re.DOTALL | re.MULTILINE)
    if vendor_name_match:
      invoice_data["vendor_name"] = vendor_name_match.group(1).strip()

    # Total Amount (assuming it's at the bottom)
    total_amount_match = re.search(r"(?:TOTAL|GRAND TOTAL)[\s:]*([\d.]+)", text, re.DOTALL | re.MULTILINE)
    if total_amount_match:
      invoice_data["total_amount"] = float(total_amount_match.group(1).strip())

    # Passenger Name (assuming it's in line items)
    passenger_names = []
    for line in text.splitlines():
      passenger_name_match = re.search(r"passenger name: (.*?)$", line, re.IGNORECASE)
      if passenger_name_match:
        passenger_names.append(passenger_name_match.group(1).strip())
    invoice_data["passenger_names"] = passenger_names  # List of passenger names

    # Account Name (assuming it's in bank details)
    account_name_match = re.search(r"Account Name\n(.*?)\n", text, re.DOTALL | re.MULTILINE)
    if account_name_match:
      invoice_data["account_name"] = account_name_match.group(1).strip()

    # Bank Account Number (assuming it's in bank details)
    bank_account_match = re.search(r"Account Number\n(.*?)\n", text, re.DOTALL | re.MULTILINE)
    if bank_account_match:
      invoice_data["bank_account_number"] = bank_account_match.group(1).strip()

    # Ticket Number (assuming it's in line items)
    ticket_numbers = []
    for line in text.splitlines():
      ticket_number_match = re.search(r"Ticket No\. (.*?)$", line, re.IGNORECASE)
      if ticket_number_match:
        ticket_numbers.append(ticket_number_match.group(1).strip())
    invoice_data["ticket_numbers"] = ticket_numbers  # List of ticket numbers

    # Return the extracted data
    return invoice_data

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None
