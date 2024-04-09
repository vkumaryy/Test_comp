import json
import textract
import camelot
from PyPDF2 import PdfReader
import random
import string


def extract_and_structure_pdf_data(file_path):
    try:
        text = textract.process(file_path, method='pdf').decode('utf-8')
        json_data = text_to_json(text)
        tables = camelot.read_pdf(file_path, flavor='stream', pages='all')
        table_data = [json.loads(table.df.to_json(orient='records')) for table in tables]
        structured_data = {"text_data": json.loads(json_data), "tables": table_data}
        return json.dumps(structured_data, indent=4)

    except Exception as e:
        error_message = f"Error processing PDF using textract: {str(e)}"
        if "The method \"pdf\" can not be found for this filetype" in str(e):
            try:
                text = extract_text_with_pypdf2(file_path)
                json_data = text_to_json(text)
                structured_data = {"text_data": json.loads(json_data), "tables": []}
                return json.dumps(structured_data, indent=4)
            except Exception as e2:
                error_message += f"\nFallback with PyPDF2 also failed: {str(e2)}"
        return json.dumps({"error": error_message})


def extract_text_with_pypdf2(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        first_page = reader.pages[0]
        return first_page.extract_text()


def text_to_json(text):
    data = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
        else:
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            value = line.strip()
        data[key] = value
    return json.dumps(data, indent=4)


pdf_path = "/home/vikash/Downloads/pdfcj.pdf"
extracted_data = extract_and_structure_pdf_data(pdf_path)
print(extracted_data)
