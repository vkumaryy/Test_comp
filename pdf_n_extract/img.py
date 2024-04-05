import PyPDF2  # For text extraction
import re  # Regular expressions for parsing text
import textract  # Additional text extractor for enhanced capabilities
import json

def extract_structured_data_pyPDF2(file_path):
  """
  Extracts text (using PyPDF2 and textract if needed) and parses key data points from the first page of a PDF invoice using regular expressions.

  Args:
      file_path: The path to the PDF file.

  Returns:
      A dictionary containing extracted data or None if there's an error.
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

    # Initialize empty dictionary for extracted data
    extracted_data = {}

    # Vendor Name (assuming it's in the header)
    vendor_name_match = re.search(r"^(.*?)\n", text, re.DOTALL | re.MULTILINE)
    if vendor_name_match:
      extracted_data["vendor_name"] = vendor_name_match.group(1).strip()

    # Total Amount (assuming it's at the bottom)
    total_amount_match = re.search(r"(?:TOTAL|GRAND TOTAL)[\s:]*([\d.]+)", text, re.DOTALL | re.MULTILINE)
    if total_amount_match:
      extracted_data["total_amount"] = float(total_amount_match.group(1).strip())

    # Name (heuristic approach, might need adjustments based on your invoice format)
    name_match = re.search(r"[Bb]illed To|To: (.*?)\n", text, re.DOTALL | re.MULTILINE)
    if name_match:
      extracted_data["name"] = name_match.group(1).strip()
    else:
      # Alternative heuristic (can be further improved)
      name_match = re.search(r"([A-Z][a-z]+\s[A-Z][a-z]+)", text)
      if name_match:
        extracted_data["name"] = name_match.group(0).strip()

    # Return the extracted data
    return extracted_data

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None

# Replace 'path/to/your/file.pdf' with the actual path
file_path = 'path/to/your/file.pdf'
extracted_data = extract_structured_data_pyPDF2(file_path)

if extracted_data:
  print(json.dumps(extracted_data))
else:
  print("Failed to extract data from PDF.")
