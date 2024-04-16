import PyPDF2
import numpy as np
from pdf2image import convert_from_path
import qrcode
from pyzbar.pyzbar import decode
import jwt

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

    with open(pdf_file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)

        for page_number in range(num_pages):
            images = convert_from_path(pdf_file_path, first_page=page_number+1, last_page=page_number+1)
            image_np = np.array(images[0])

            decoded_objects = decode(image_np)
            
            for obj in decoded_objects:
                qr_data.append(obj.data.decode('utf-8'))

    return qr_data

def decode_jwt_and_get_data(qr_data, public_key_path=None):
    try:
        if public_key_path:
            with open(public_key_path, 'rb') as key_file:
                public_key = load_pem_public_key(key_file.read())
            decoded_data = jwt.decode(qr_data, algorithms=['RS256'], verify=True, key=public_key)
        else:
            # Decode without verification if no public key provided
            decoded_data = jwt.decode(qr_data, algorithms=['RS256'], verify=False)
        if 'data' in decoded_data:
            return decoded_data['data']
        else:
            print("Error: 'data' key not found in decoded JWT.")
            return None
    except jwt.PyJWTError as e:
        print(f"Error: {e}")
        return None



# Example usage:
def main():
    pdf_file_path = "/home/vikash/Documents/GitHub/flasklearn/Test_comp/pc.pdf"

    extracted_info = extract_qr_info_from_pdf(pdf_file_path)
    print("QR code data extracted from PDF:", extracted_info)

    if extracted_info:
        jwt_data = extracted_info[0]  # Assuming there's only one QR code data extracted
        extracted_json = decode_jwt_and_get_data(jwt_data)
        if extracted_json:
            print("Extracted data from JWT:", extracted_json)
        else:
            print("Error: Unable to decode JWT.")
    else:
        print("No QR code data extracted from PDF.")

if __name__ == "__main__":
    main()
