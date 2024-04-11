import PyPDF2
import qrcode
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import json

# Function to extract data from QR code image
def extract_data_from_qr(image_path):
    decoded_objects = decode(image_path)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        return data

# Load the PDF file
pdf_file = open('/home/vikash/Downloads/pdfcj.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Loop through each page of the PDF
for page_num in range(pdf_reader.numPages):
    images = convert_from_path('/home/vikash/Downloads/pdfcj.pdf', first_page=page_num+1, last_page=page_num+1)

    # Check each image on the page for QR codes
    for i, image in enumerate(images):
        qr_data = extract_data_from_qr(image)
        
        if qr_data:
            json_data = json.loads(qr_data)
            print(json.dumps(json_data, indent=4))
            break

pdf_file.close()