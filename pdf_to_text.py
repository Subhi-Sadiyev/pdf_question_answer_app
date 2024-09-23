import fitz ##pip install PyMuPDF, not fitz


## function to parse pdf and save the content to text variable
def extract_text_from_entire_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    # Iterate through all pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text