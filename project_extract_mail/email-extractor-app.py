import streamlit as st
import re
import pdfplumber
from docx import Document
import tempfile

def extract_emails_from_text(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_emails_from_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1].lower()
    text = ""
    if ext == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif ext == "docx":
        text = extract_text_from_docx(uploaded_file)
    elif ext == "txt":
        text = uploaded_file.read().decode('utf-8', errors='ignore')
    else:
        return []
    return extract_emails_from_text(text)

st.title("📧 Email Extractor from PDFs, DOCX, TXT")

uploaded_files = st.file_uploader(
    "Upload your PDF, DOCX or TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    all_emails = set()
    for uploaded_file in uploaded_files:
        emails = extract_emails_from_file(uploaded_file)
        if emails:
            st.write(f"**{uploaded_file.name}**: {len(emails)} emails found")
            st.write(", ".join(emails))
            all_emails.update(emails)

    st.markdown("---")
    st.write(f"### Total unique emails found: {len(all_emails)}")
    for email in sorted(all_emails):
        st.write(email)

    if all_emails:
        # Export button to download all emails as txt
        emails_txt = "\n".join(sorted(all_emails))
        st.download_button(
            label="Download all emails as TXT",
            data=emails_txt,
            file_name="extracted_emails.txt",
            mime="text/plain"
        )
else:
    st.info("Upload some files to extract emails!")
