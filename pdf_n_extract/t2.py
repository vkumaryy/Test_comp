import pandas as pd
import numpy as np
import PyPDF2
import tabula
import json


def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Combined text extracted from all pages.
    """

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_tables_from_pdf(pdf_path):
    """Extracts tables from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: List of pandas DataFrames, each representing a table.
    """

    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables


def extract_data_from_pdf(pdf_path, default_key=None):
    """Extracts text and table data from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
        default_key (str, optional): Optional key for text without colons. Defaults to None.

    Returns:
        dict: Dictionary containing extracted data.
    """

    text = extract_text_from_pdf(pdf_path)
    tables = extract_tables_from_pdf(pdf_path)

    data = {}

    # Extracting Text Data
    text_lines = text.split('\n')
    for line in text_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            data[key] = value
        elif default_key:
            data[default_key] = line

    # Extracting Table Data
    for table_num, table in enumerate(tables):
        try:
            # Handle potential conversion errors (non-numeric values)
            try:
                table_data = table.to_dict(orient='records')
            except pd.errors.ConversionError:
                print(f"Warning: Conversion errors in table {table_num + 1}. Filling with NaNs...")
                table_data = table.to_dict(orient='records', errors='coerce')

            for row_num, row in enumerate(table_data):
                for key, value in row.items():
                    new_key = f"Table_{table_num + 1}_Row_{row_num + 1}_{key}"
                    data[new_key] = value
        except ValueError as e:
            print(f"Error processing table {table_num + 1}: {e}")

    return data


def pdf_to_json(pdf_path, default_key=None, json_path='output.json'):
    """Converts a PDF file to JSON format.

    Args:
        pdf_path (str): Path to the PDF file.
        default_key (str, optional): Optional key for text without colons. Defaults to None.
        json_path (str, optional): Path to the output JSON file. Defaults to 'output.json'.
    """

    data = extract_data_from_pdf(pdf_path, default_key)
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Example usage
pdf_path = '/home/vikash/Downloads/pdfcj.pdf'
default_key = 'Text_From_PDF'
json_path = 'output.json'

pdf_to_json(pdf_path, default_key, json_path)
