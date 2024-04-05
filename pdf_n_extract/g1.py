import PyPDF2
import json

def extract_all_text_from_page(file_path, page_num=0):
  """
  Extracts all text from the specified page of a PDF using PyPDF2.

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

    # Ensure page number is within valid range
    if page_num < 0 or page_num >= len(pdf_reader.pages):
      raise ValueError("Invalid page number.")

    # Extract text from the specified page
    page = pdf_reader.pages[page_num]
    text = page.extract_text()

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

# Convert text to JSON string (if successful)
if text_data:
  json_data = json.dumps(text_data)
  print(json_data)
else:
  print("Failed to extract text from PDF.")
