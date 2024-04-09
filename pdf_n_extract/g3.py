import json
import textract
import camelot
from PyPDF2 import PdfReader  # Import for alternative approach
import random
import string


def extract_and_structure_pdf_data(file_path):
    """
    Extracts text and structure data from a PDF, handling potential issues
    and offering alternative text extraction methods. Converts text to JSON
    with random keys for missing entries.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: A JSON string containing the structured data or an error message.
    """

    try:
        # Processing with textract (preferred method)
        text = textract.process(file_path, method='pdf').decode('utf-8')

        # Convert text to JSON with random keys for missing entries
        json_data = text_to_json(text)

        # Structure remaining data (tables)
        tables = camelot.read_pdf(file_path, flavor='stream', pages='all')
        table_data = []
        for table in tables:
            df = table.df  # Access table as DataFrame
            table_json = df.to_json(orient='records')
            table_data.append(json.loads(table_json))

        # Combine text and table data
        structured_data = {"text_data": json.loads(json_data)}
        structured_data["tables"] = table_data

        return json.dumps(structured_data, indent=4)

    except Exception as e:
        # Handle textract exceptions
        error_message = f"Error processing PDF using textract: {str(e)}"
        if "The method \"pdf\" can not be found for this filetype" in str(e):

            # Fallback to PyPDF2 for basic text extraction if textract fails
            try:
                text = extract_text_with_pypdf2(file_path)
                json_data = text_to_json(text)
                structured_data = {"text_data": json.loads(json_data)}
                structured_data["tables"] = []  # No table data in fallback
                return json.dumps(structured_data, indent=4)
            except Exception as e2:
                error_message += f"\nFallback with PyPDF2 also failed: {str(e2)}"

        return json.dumps({"error": error_message})


def extract_text_with_pypdf2(file_path):
    """
    Extracts text from the first page of a PDF using PyPDF2
    (limited functionality compared to textract).

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the first page.
    """

    with open(file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        first_page = reader.pages[0]
        return first_page.extract_text()


def text_to_json(text):
    """
    Converts text data into a JSON object, assigning random keys
    for missing entries in key-value pairs.

    Args:
        text (str): The text data to be converted.

    Returns:
        str: A JSON string representing the parsed data.
    """

    data = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
        else:
            # Assign a random key if no colon is found
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            value = line.strip()
        data[key] = value

    return json.dumps(data, indent=4)


def main():
    """
    Prompts the user for the PDF path and calls the extraction function.
    """

    pdf_path = "/home/vikash/Downloads/pdfcj.pdf"
    extracted_data = extract_and_structure_pdf_data(pdf_path)
    print(extracted_data)


if __name__ == "__main__":
    main()
