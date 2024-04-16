import PyPDF2
import numpy as np
from pdf2image import convert_from_path
import qrcode
from pyzbar.pyzbar import decode
import base64
import json
import fitz  # PyMuPDF

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
    qr_data = []

    # Open the PDF file
    pdf_document = fitz.open(pdf_file_path)

    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Convert the page to a pixmap
        pixmap = page.get_pixmap()

        # Debugging: Print pixmap dimensions
        print("Pixmap dimensions:", pixmap.width, pixmap.height)

        # Convert the pixmap to a numpy array
        image_np = np.frombuffer(pixmap.samples, dtype=np.uint8)

        # Debugging: Print size of pixmap samples
        print("Size of pixmap samples:", image_np.size)

        # Decode QR codes in the image
        decoded_objects = decode(image_np)
        for obj in decoded_objects:
            qr_data.append(obj.data.decode('utf-8'))

    pdf_document.close()

    return qr_data

# Example usage:
pdf_file_path = "/home/vikash/Downloads/pdfcj.pdf"  # Replace "pdf_to_read.pdf" with your PDF file path

# Generating QR code for testing
data_to_encode = "Sample QR code data"
qr_code_path = "temp_qr_code.png"
generate_qr_code(data_to_encode, qr_code_path)

# Extracting QR code data from PDF
extracted_info = extract_qr_info_from_pdf(pdf_file_path)
print("QR code data extracted from PDF:", extracted_info)

# Split the token into its three parts
header, payload, signature = extracted_info[0].split('.')

# Decode the header and payload
decoded_header = base64.b64decode(header + "==").decode('utf-8')
decoded_payload = base64.b64decode(payload + "==").decode('utf-8')

# Convert decoded header and payload into JSON
header_json = json.loads(decoded_header)
payload_json = json.loads(decoded_payload)

print("Header JSON:", header_json)
print("Payload JSON:", payload_json)
