import PyPDF2
import json
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

    text = text.replace(',', '\n')

    cleaned_text = ""
    lines = text.split('\n')
    for line in lines:
        cleaned_line = re.sub(r'^\s+', '', line)
        if cleaned_line:
            cleaned_text += cleaned_line + '\n'
    return cleaned_text.strip()

def convert_to_json(text):
    lines = text.split('\n')
    json_data = {}
    line_number = 1
    for line in lines:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            json_data[key] = value
        else:
            json_data[f'data-{line_number}'] = line.strip()
            line_number += 1
    return json.dumps(json_data, indent=4)

if __name__ == "__main__":
    pdf_path = "/home/vikash/Downloads/pdfcj.pdf"
    text = extract_text_from_pdf(pdf_path)
    json_data = convert_to_json(text)
    print(json_data)