import PyPDF2
import re
import json

def extract_pdf_data_from_file_to_json(filepath):
    """
    Extracts key-value pairs and ticket information from a PDF file and returns the result in JSON format.

    Args:
        filepath: The path to the PDF file.

    Returns:
        A JSON string containing the extracted data.
    """

    extracted_data = {}

    try:
        # Open the PDF file
        with open(filepath, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text content from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

    except Exception as e:
        print(f"Error opening or reading the PDF file: {e}")
        return None

    # Use a regular expression to extract key-value pairs
    regex_pattern = r"([\w\s]+?)\s*:\s*(.*?)(?=\n[\w\s]+?\s*:|$)"
    matches = re.findall(regex_pattern, text)

    serial_number = 1
    for match in matches:
        key = match[0].strip()
        value = match[1].strip()
        if value:  # If value is available, use the key
            extracted_data[key] = value
        else:  # If value is empty, assign a serial number
            extracted_data[f"Value {serial_number}"] = key
            serial_number += 1

    # Convert the extracted data to JSON format
    json_data = json.dumps(extracted_data, indent=4)
    return json_data


# Example usage:
file_path = "/home/vikash/Downloads/pdfcj.pdf"
extracted_json = extract_pdf_data_from_file_to_json(file_path)
if extracted_json:
    print(extracted_json)
else:
    print("Error: An error occurred while processing the PDF file.")
