import PyPDF2
import re
import json

def extract_pdf_data_from_file_to_json(filepath):
    """
    Extracts key-value pairs and table data from the text present on the first page of a PDF file and returns the result in JSON format.

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

            # Extract text content from the first page
            first_page_text = pdf_reader.pages[0].extract_text()

    except Exception as e:
        print(f"Error opening or reading the PDF file: {e}")
        return None

    # Check if the text represents a structured table
    if '|' in first_page_text:
        # Extract data from table format
        rows = first_page_text.split('\n')
        headers = rows[0].split('|')
        table_data = []
        for row in rows[1:]:
            columns = row.split('|')
            row_data = {}
            for i, header in enumerate(headers):
                row_data[header.strip()] = columns[i].strip() if i < len(columns) else ''
            table_data.append(row_data)
        extracted_data["Table Data"] = table_data
    else:
        # Define regular expression to extract key-value pairs
        key_value_pattern = r"([\w\s]+?)\s*:\s*(.*?)(?=\n[\w\s]+?\s*:|$)"

        # Extract key-value pairs
        matches = re.findall(key_value_pattern, first_page_text)
        for match in matches:
            key = match[0].strip()
            value = match[1].strip()
            if value:
                extracted_data[key] = value

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
