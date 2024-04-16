import subprocess
import PyPDF2
import fitz  # PyMuPDF
import qrcode
import base64
import json
import io

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
    
    # Iterate over each page
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        
        # Get the images on the page
        image_list = page.get_images(full=True)
        
        # Iterate over each image
        for image_index, image_info in image_list.items():
            # Get the image data
            image_data = page.get_pixmap()
            
            # Use Zxing command-line tool to decode QR code from the image
            result = subprocess.run(["zxing", "-q", "--raw", "--", "-"], input=image_data.tobytes(), capture_output=True, text=True)
            if result.returncode == 0:
                qr_data.append(result.stdout.strip())
    
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
    print("No QR code found in the PDF.")