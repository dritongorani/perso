import os
import re
from tkinter import Tk, filedialog
from docx import Document
import pdfplumber

def extract_emails_from_text(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_emails_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    elif ext == ".docx":
        text = extract_text_from_docx(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        return []
    return extract_emails_from_text(text)

def main():
    # Ouvrir boîte dialogue pour choisir dossier
    root = Tk()
    root.withdraw()  # cacher la fenêtre principale
    folder_selected = filedialog.askdirectory(title="Choisissez un dossier contenant des documents")
    
    if not folder_selected:
        print("Aucun dossier sélectionné, sortie.")
        return

    print(f"Dossier sélectionné : {folder_selected}")

    all_emails = set()
    for root_dir, dirs, files in os.walk(folder_selected):
        for file in files:
            full_path = os.path.join(root_dir, file)
            emails = extract_emails_from_file(full_path)
            if emails:
                print(f"[{file}] Emails trouvés: {emails}")
                all_emails.update(emails)
    
    print("\n=== Tous les emails extraits ===")
    for e in sorted(all_emails):
        print(e)

if __name__ == "__main__":
    main()
