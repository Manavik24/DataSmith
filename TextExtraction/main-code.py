#pip install PyPDF2

from PyPDF2 import PdfReader

def extract_text_with_pyPDF(PDF_File):
    
    pdf_reader = PdfReader(PDF_File)
    raw_text = ''
    
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text
    
text_with_pyPDF = extract_text_with_pyPDF("SoftSkills.pdf")
print(text_with_pyPDF)

