import PyPDF2
import re

# Function to extract clean text from a PDF file (first page only)

def extract_clean_text(pdf_path):
    """
    Extracts clean text from the first page of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text with minimal garbage data.
    """

    try:
        # Open PDF in binary read mode
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from the first page
            page = pdf_reader.pages[0]
            text = page.extract_text()

            # Preprocessing steps to remove common garbage (adjust as needed)
            text = text.strip()  # Remove leading/trailing whitespace
            text = text.replace('\n\n', '\n')  # Combine redundant newlines
            text = re.sub(r'[^\w\s\.\,\:\!\?\-]', '', text, flags=re.UNICODE)  # Remove non-alphanumeric characters (except common punctuation)

            return text

    except (FileNotFoundError, PyPDF2.PdfReaderError) as e:
        print(f"Error processing PDF: {e}")
        return ""

if __name__ == "__main__":
    pdf_path = "/home/vikash/Downloads/garb.pdf"  # Replace with your PDF path
    clean_text = extract_clean_text(pdf_path)

    if clean_text:
        print(clean_text)
    else:
        print("No text extracted from PDF.")
