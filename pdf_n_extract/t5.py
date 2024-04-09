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
    return text

def convert_to_json(text):
    lines = text.split('\n')
    data = {}
    current_key = None
    current_value = None
    keys_to_delete = []
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if current_key is not None:
                data[current_key] = current_value
            current_key = key
            current_value = value
        elif current_key is not None:
            current_value += " " + line.strip()
    if current_key is not None:
        data[current_key] = current_value

    # Add numbering for keys without key-value pairs
    for key, value in data.items():
        if value == "":
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del data[key]
        data[f"Key{keys_to_delete.index(key)}"] = key

    return json.dumps(data, indent=4)

if __name__ == "__main__":
    pdf_path = "pdf_to_read.pdf"
    resume_text = extract_text_from_pdf(pdf_path)
    json_data = convert_to_json(resume_text)
    print(resume_text)
    print(json_data)