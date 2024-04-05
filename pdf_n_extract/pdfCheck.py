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


import PyPDF2
import json
import os

def extract_data_from_pdf(pdf_path):
    try:
        # Check if the file exists
        if not os.path.isfile(pdf_path):
            return json.dumps({"error": "File not found."})
        
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            reader = PyPDF2.PdfFileReader(file)
            
            # Check if the PDF is valid
            if reader.isEncrypted:
                return json.dumps({"error": "The PDF file is encrypted and cannot be processed."})
            
            # Extract text from the first page
            first_page = reader.getPage(0)
            text = first_page.extractText()
            
            # Extract data from the text
            data = {}
            lines = text.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            
            return json.dumps(data, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    pdf_path = 'path_to_your_pdf_file.pdf'  # Change this to the path of your PDF file
    extracted_data = extract_data_from_pdf(pdf_path)
    print(extracted_data)

if __name__ == "__main__":
    main()

