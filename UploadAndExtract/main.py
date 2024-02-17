import streamlit as st
import PyPDF2

def extract_text_with_pyPDF(file):
    pdf_reader = PyPDF2.PdfReader(file)
    raw_text = ''
    
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text

file = st.file_uploader("Upload a PDF file", type="pdf")

if file:
    text_with_pyPDF = extract_text_with_pyPDF(file)
    st.text(text_with_pyPDF)
