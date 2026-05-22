import re


def clean_resume_text(text: str) -> str:
    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove unwanted symbols
    text = re.sub(r"[^\w\s@.+#]", "", text)

    return text.strip()