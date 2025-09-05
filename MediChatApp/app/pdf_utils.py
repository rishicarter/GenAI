from pypdf import PdfReader
from typing import List, Optional
from io import BytesIO

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file.

    Args:
        file (BytesIO): A file-like object containing the PDF data.

    Returns:
        Optional[list[str]]: A list of strings, each representing the text from a page in the PDF.
                             Returns None if the file is not a valid PDF.
    """
    try:
        reader = PdfReader(file)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None