
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

if __name__ == "__main__":
    pdf_path = "/home/vikash/Downloads/pdfcj.pdf"
    resume_text = extract_text_from_pdf(pdf_path)
    print(resume_text)