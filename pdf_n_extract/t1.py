import json
import textract


def extract_first_page_data_to_json(file_path):
    """
    Extracts text from the first page of a PDF and returns it as a JSON object.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: A JSON string containing the extracted text or an error message.
    """

    try:
        # Extract text using textract
        text = textract.process(file_path, method='pdf').decode('utf-8')

        # Return a dictionary for more structured data (optional)
        extracted_data = {"text": text}

        return json.dumps(extracted_data, indent=4)

    except Exception as e:
        # Handle exceptions
        error_message = f"Error processing PDF using textract: {str(e)}"
        return json.dumps({"error": error_message})


def main():
    """
    Prompts the user for the PDF path and calls the extraction function.
    """

    pdf_path = input("Enter the path to the PDF file: ")
    extracted_data = extract_first_page_data_to_json(pdf_page)
    print(extracted_data)


if __name__ == "__main__":
    main()
