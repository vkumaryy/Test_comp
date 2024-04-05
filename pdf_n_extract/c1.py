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
    # Construct the full file path dynamically
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pdf_filename = 'your_pdf_file.pdf'  # Replace 'your_pdf_file.pdf' with the actual PDF filename
    pdf_path = os.path.join(script_dir, pdf_filename)
    
    # Extract data from the PDF
    extracted_data = extract_data_from_pdf(pdf_path)
    print(extracted_data)

if __name__ == "__main__":
    main()
