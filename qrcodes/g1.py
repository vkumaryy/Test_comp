import fitz  # PyMuPDF library for PDF handling
import cv2  # OpenCV for QR code detection and decoding
import json  # For optional JSON conversion


def extract_qrcode_data(pdf_path):
    """
    Extracts data from the first QR code found in a PDF, handling potential multiple QR codes.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Decoded data from the first QR code, or None if no QR codes are found.
    """

    doc = fitz.open(pdf_path)
    page_number = 0

    while page_number < len(doc):
        page = doc.load_page(page_number)
        image = page.get_pixmap()  # Get the page image

        # Convert to grayscale (simplifies QR code detection in most cases)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find contours (potential image regions)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = gray[y:y+h, x:x+w]  # Extract region of interest

            # Try decoding QR code from the region
            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(roi)
            if data:
                return data  # Return data from the first QR code found

        page_number += 1

    return None  # No QR codes found


def main():
    pdf_path = "/home/vikash/Downloads/pdfcj.pdf"  # Replace with your actual PDF path

    data = extract_qrcode_data(pdf_path)

    if data:
        # Convert data to JSON if it's a valid JSON string (optional)
        try:
            json_data = json.loads(data)
            print("Successfully extracted data (as JSON):", json_data)
        except json.JSONDecodeError:
            print("Extracted data:", data)
    else:
        print("No QR codes found in the PDF.")


if __name__ == "__main__":
    main()
