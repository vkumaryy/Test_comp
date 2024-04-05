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
