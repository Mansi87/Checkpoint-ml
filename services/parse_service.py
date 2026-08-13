import re
import pdfplumber
from docx import Document


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
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_basic_fields(text):
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d[\d\s\-\(\)]{8,}\d)', text)
    linkedin_match = re.search(r'(linkedin\.com/in/[\w\-]+)', text, re.IGNORECASE)

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    probable_name = lines[0] if lines else ""

    return {
        "fullName": probable_name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "linkedin": linkedin_match.group(0) if linkedin_match else "",
    }


def parse_resume_file(file, filename):
    if filename.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(file)
    elif filename.lower().endswith('.docx'):
        raw_text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX allowed.")

    fields = extract_basic_fields(raw_text)

    confidence = {
        "fullName": bool(fields["fullName"]),
        "email": bool(fields["email"]),
        "phone": bool(fields["phone"]),
        "linkedin": bool(fields["linkedin"]),
    }

    return {
        "rawText": raw_text,
        "extractedFields": fields,
        "confidence": confidence,
    }