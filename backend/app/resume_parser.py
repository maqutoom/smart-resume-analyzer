from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_upload(filename: str, content_type: str | None, file_bytes: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".pdf") or content_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)

    return file_bytes.decode("utf-8", errors="ignore").strip()

