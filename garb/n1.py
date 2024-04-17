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
    # print(text)
    
    cleaned_text = ""
    lines = text.split('\n')
    for line in lines:
        cleaned_line = re.sub(r'^\s+', '', line)
        if cleaned_line:
            cleaned_text += cleaned_line + '\n'
    return cleaned_text.strip()

def convert_to_json(text):
    lines = text.split('\n')
    key_value_data = {}
    numbered_data = {}
    line_number = 1
    for line in lines:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            key_value_data[key] = value
        else:
            numbered_data[f'data-{line_number}'] = line.strip()
            line_number += 1
    return json.dumps({"key_value_data": key_value_data, "numbered_data": numbered_data}, indent=4)

if __name__ == "__main__":
    pdf_path = "pdf4.pdf"
    text = extract_text_from_pdf(pdf_path)
    json_data = convert_to_json(text)
    print(json_data["key_value_data"])