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

    # Use a single regular expression to extract key-value pairs and ticket information
    regex_pattern = r"(?:\n:?\s*(\w+)\s*:\s*(.*?)(?=\n|$))|(?:Ticket No\.(.*?)\nPassenger Name(.*?)\nSAC(.*?)\nBasic Fare(.*?)\nTaxes&Chrgs(.*?)\nTot Amount(.*?)\n)"
    matches = re.finditer(regex_pattern, text, re.DOTALL)

    current_key = None
    ticket_data = []
    for match in matches:
        if match.group(1):  # Key-value pair match
            current_key = match.group(1).strip()
            extracted_data[current_key] = match.group(2).strip()
        else:  # Ticket information match
            ticket_data.append({
                "Ticket No.": match.group(3).strip(),
                "Passenger Name": match.group(4).strip(),
                "SAC": match.group(5).strip(),
                "Basic Fare": match.group(6).strip(),
                "Taxes&Chrgs": match.group(7).strip(),
                "Tot Amount": match.group(8).strip(),
            })

    if ticket_data:
        extracted_data["Ticket Information"] = ticket_data

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
