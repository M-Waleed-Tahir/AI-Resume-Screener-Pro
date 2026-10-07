import re
import pdfplumber
from pypdf import PdfReader

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def extract_text_from_pdf(self, pdf_file) -> str:
        extracted_text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
        except Exception as e:
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as pdf_err:
                print(f"PyPDF failed: {pdf_err}")

        return extracted_text.strip()

    def extract_contact_info(self, text: str) -> dict:
        emails = re.findall(self.email_pattern, text)
        email = emails[0] if emails else "Not Found"

        # Direct regex search for full phone strings (+92 or local numbers)
        phone_match = re.search(r'(\+?92[-.\s]?\d{3}[-.\s]?\d{7}|\b03\d{2}[-.\s]?\d{7}\b)', text)
        if not phone_match:
            phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

        phone = phone_match.group(0).strip() if phone_match else "Not Found"

        return {
            "email": email,
            "phone": phone
        }

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text