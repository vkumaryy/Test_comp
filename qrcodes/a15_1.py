import cv2
import PyPDF2
import numpy as np
from pdf2image import convert_from_path
import qrcode
from pyzbar.pyzbar import decode
import base64
import json


def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

def extract_qr_info_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        qr_data = []

        for page_number in range(num_pages):
            page = reader.pages[page_number]
            images = convert_from_path(pdf_file_path, first_page=page_number+1, last_page=page_number+1)
            image_np = np.array(images[0])

            decoded_objects = decode(image_np)
            for obj in decoded_objects:
                qr_data.append(obj.data.decode('utf-8'))

    return qr_data

# Example usage:
pdf_file_path = "/home/vikash/Downloads/pdfcj.pdf"  # Replace "pdf_to_read.pdf" with your PDF file path

# Generating QR code for testing
data_to_encode = "Sample QR code data"
qr_code_path = "temp_qr_code.png"
generate_qr_code(data_to_encode, qr_code_path)

# Inserting generated QR code into the PDF
# Insert the generated QR code into a PDF page here if needed

# Extracting QR code data from PDF
extracted_info = extract_qr_info_from_pdf(pdf_file_path)

if extracted_info:
    # Split the token into its three parts
    try:
        header, payload, signature = extracted_info[0].split('.')
        
        # Decode the header and payload
        decoded_header = base64.b64decode(header + "==").decode('utf-8')
        decoded_payload = base64.b64decode(payload + "==").decode('utf-8')

        # Convert decoded header and payload into JSON
        header_json = json.loads(decoded_header)
        payload_json = json.loads(decoded_payload)

        print("Payload JSON:", payload_json)
    except ValueError:
        print("Invalid JWT token format.")
else:
    print("No JWT token found.")