# pip install fitz

import fitz  # PyMuPDF library for working with PDFs
import json

def extract_all_text_and_metadata(file_path):
  """
  This function attempts to open a PDF file and extract all text data 
  and metadata from the first page.

  Args:
      file_path: The path to the PDF file.

  Returns:
      A dictionary containing extracted text and metadata or None if there's an error.
  """
  try:
    # Open the PDF with PyMuPDF
    doc = fitz.open(file_path)

    # Get the first page
    page = doc.loadPage(0)

    # Extract text from the page
    text = page.get_text("text")

    # Extract metadata from document info
    metadata = doc.metadata

    # Combine text and metadata into a single dictionary
    all_data = {"text": text, "metadata": metadata}

    # Return the extracted data
    return all_data

  except Exception as e:
    print(f"Error processing PDF: {e}")
    return None

# Replace 'path/to/your/file.pdf' with the actual path to your PDF
file_path = 'path/to/your/file.pdf'

# Extract data and convert to JSON (if successful)
all_data = extract_all_text_and_metadata(file_path)
if all_data:
  json_data = json.dumps(all_data)
  print(json_data)
else:
  print("Failed to extract data from PDF.")
