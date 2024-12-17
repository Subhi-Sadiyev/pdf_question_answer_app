import fitz  # pip install PyMuPDF not fitz
import pytesseract
from pdf2image import convert_from_path
import os

### Function to parse PDF and save the content to text variable
def extract_text_from_entire_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text("text")

        if page_text.strip():
            ## If normal text is found, just append it
            text += page_text
        else:
            ## If no text found, we consider it as an image-based page.
            ## Convert just this single page to an image
            images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
            ## There should be exactly one image in the list for this single-page conversion
            for image in images:
                ocr_text = pytesseract.image_to_string(image, lang='aze')
                text += ocr_text
    
    return text