import PyPDF2
import json

def extract_metadata(pdf_path):
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            reader = PyPDF2.PdfFileReader(file)
            
            # Check if the PDF is valid
            if reader.isEncrypted:
                print("The PDF file is encrypted and cannot be processed.")
                return None
            
            # Extract data from the first page
            first_page = reader.getPage(0)
            metadata = first_page.extractText()
            return metadata
    except Exception as e:
        print("Error:", e)
        return None

def main():
    pdf_path = 'path_to_your_pdf_file.pdf'  # Change this to the path of your PDF file
    metadata = extract_metadata(pdf_path)
    if metadata:
        print("Data extracted successfully from the first page:")
        print(metadata)
    else:
        print("Failed to extract data.")

if __name__ == "__main__":
    main()
