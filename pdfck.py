import PyPDF2
import os

def check_pdf_integrity(file_path):
    
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            if pdf_reader.trailer['/Root'] is None:
                raise ValueError("PDF structure is invalid")

            if len(pdf_reader.pages) == 0:
                raise ValueError("PDF has no pages")

            

        return True  

    except (FileNotFoundError, PermissionError):
        print("Error: PDF file not found or inaccessible.")
        return False

    except PyPDF2.errors.PdfReadError:
        print("Error: PDF file is corrupted or invalid.")
        return False

    except OSError as e:  # Catch general OS-related errors
        if e.errno == 2:  # No such file or directory
            print("Error: PDF file not found.")
        else:
            print(f"Unexpected OS error: {e}")
        return False

    except ValueError as e:  # Catch specific value errors from our checks
        print(f"Error: PDF is invalid: {e}")
        return False

file_path = "/home/vikash/Downloads/Vktenthmarksheet.pdf"
if check_pdf_integrity(file_path):
    print("PDF file is valid and can be opened.")
else:
    print("PDF file is corrupted or has issues.")
