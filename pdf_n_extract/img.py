import PyPDF2
import re
import textract
import json

def extract_structured_data_pyPDF2(file_path):
    """
    Extracts basic invoice data (description, passenger name, basic fare, total amount) from each page of a PDF
    assuming each page contains a separate invoice.

    Args:
        file_path: The path to the PDF file.

    Returns:
        A list of dictionaries containing extracted data for each invoice or None if there's an error.
    """

    try:
        # Open the PDF with PyPDF2
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract data from each page
        extracted_invoices = []
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]

            # Extract text from the page
            try:
                text = page.extract_text()
            except:
                text = textract.process(file_path).decode('utf-8')  # Use textract for wider compatibility

            # Initialize dictionary for invoice data
            invoice_data = {}

            # Description (assuming it's at the beginning)
            description_match = re.search(r"^([^']+)", text)  # Capture text until first single quote
            if description_match:
                invoice_data["description"] = description_match.group(1).strip()

            # Passenger Name (assuming a specific format)
            passenger_name_match = re.search(r"passenger name: (.*?)$", text, re.IGNORECASE)
            if passenger_name_match:
                invoice_data["passenger_name"] = passenger_name_match.group(1).strip()

            # Basic Fare (assuming a numeric value)
            basic_fare_match = re.search(r"\b(\d+\.\d{2})\b", text)  # Match whole number with two decimal places
            if basic_fare_match:
                invoice_data["basic_fare"] = float(basic_fare_match.group(1))

            # Total Amount (assuming a specific format)
            total_amount_match = re.search(r"(?:total amount|total):[\s:]*([\d+\.\d{2}])", text, re.IGNORECASE)
            if total_amount_match:
                invoice_data["total_amount"] = float(total_amount_match.group(1))

            # Append extracted data for this invoice
            extracted_invoices.append(invoice_data)

        # Close the PDF file
        pdf_file.close()

        return extracted_invoices

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

# Call the function with the file path to your PDF file
# Replace 'path/to/your/file.pdf' with the actual path to your PDF file
extracted_data = extract_structured_data_pyPDF2('/home/vikash/Downloads/pdfcj.pdf')
if extracted_data:
    print(json.dumps(extracted_data, indent=4))
