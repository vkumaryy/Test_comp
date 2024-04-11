import fitz  # PyMuPDF
from pyzbar.pyzbar import decode
import json

def extract_qr_data_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    qr_data = []

    # Loop through each page
    for page_num in range(pdf_document.page_count):
        # Get the page
        page = pdf_document.load_page(page_num)
        
        # Extract images from the page
        images = page.get_images(full=True)

        # Loop through each image on the page
        for img_index, img in enumerate(images):
            # Decode the image as a QR code
            qr_code_data = decode(img[0])

            # If QR code data is found, append it to the list
            if qr_code_data:
                qr_data.append(qr_code_data[0].data.decode())

    # Close the PDF document
    pdf_document.close()

    return qr_data

def main():
    pdf_path = '/home/vikash/Downloads/pdfcj.pdf'
    qr_data = extract_qr_data_from_pdf(pdf_path)

    # Check if data is in the first QR code
    if qr_data:
        print("Data found in the first QR code:", qr_data[0])
    else:
        print("No data found in the first QR code. Scanning the second QR code...")

        # Check the second QR code
        if len(qr_data) > 1:
            print("Data found in the second QR code:", qr_data[1])
        else:
            print("No data found in the second QR code.")

    # Convert QR data to JSON
    json_data = json.dumps(qr_data)
    print("QR data in JSON format:", json_data)

if __name__ == "__main__":
    main()
