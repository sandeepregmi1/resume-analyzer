import re

def clean_resume_text(text: str) -> str:
    # normalize lowercase
    text = text.lower()

    # fix broken spacing inside words (OCR issue)
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)

    # remove special characters but keep spaces
    text = re.sub(r"[^a-z0-9\s@.+#]", " ", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()