import re

#  common OCR / resume noise 
COMMON_FIXES = {
    "machinelearning": "machine learning",
    "deeplearning": "deep learning",
    "computervision": "computer vision",
    "naturallanguageprocessing": "natural language processing",
    "dataengineering": "data engineering",
    "datascience": "data science",
    "artificialintelligence": "artificial intelligence",
}

def clean_resume_text(text: str) -> str:
    # 1. lowercase
    text = text.lower()

    # 2. fix OCR broken spacing like "s k i l l s"
    text = re.sub(r"(?:\b\w\s){2,}\w\b", lambda m: m.group(0).replace(" ", ""), text)

    # 3. remove special characters but keep spaces
    text = re.sub(r"[^a-z0-9\s@.+#]", " ", text)

    # 4. normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # 5. fix merged words (critical for embeddings)
    for wrong, correct in COMMON_FIXES.items():
        text = text.replace(wrong, correct)

    # 6. final cleanup
    text = re.sub(r"\s+", " ", text).strip()

    return text