import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import os

# Function to parse PDF and save the content to text variable
def extract_text_from_entire_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Iterate through all pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    
    # Check if no text was extracted, implying it might be an image-based PDF
    if not text.strip():
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        # Use Tesseract to extract text from each image
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
    
    return text