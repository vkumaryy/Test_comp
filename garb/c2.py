import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        if pdf_reader.numPages >= 1:
            page = pdf_reader.getPage(0)
            text = page.extractText()
    return text

def clean_text(text):
    # Add any additional cleaning steps as needed
    cleaned_text = " ".join(text.split())  # Remove extra whitespaces
    return cleaned_text

if __name__ == "__main__":
    pdf_path = "/home/vikash/Downloads/garb.pdf"  # Replace with the path to your PDF file
    try:
        extracted_text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(extracted_text)
        print(cleaned_text)
    except Exception as e:
        print("Error occurred:", e)
