import re

# OCR / resume common merged-word fixes
COMMON_FIXES = {
    "machinelearning": "machine learning",
    "deeplearning": "deep learning",
    "computervision": "computer vision",
    "naturallanguageprocessing": "natural language processing",
    "dataengineering": "data engineering",
    "datascience": "data science",
    "artificialintelligence": "artificial intelligence",
    "nlp": "nlp",
    "mlops": "mlops",
    "llmops": "llmops"
}


def clean_resume_text(text: str) -> str:
    if not text:
        return ""

    # 1. lowercase (IMPORTANT for deterministic matching)
    text = text.lower()

    # 2. fix broken spaced letters: "m a c h i n e"
    text = re.sub(r"(?:\b[a-z]\s){3,}[a-z]\b", lambda m: m.group(0).replace(" ", ""), text)

    # 3. fix OCR weird line breaks (hyphen split words)
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)

    # 4. normalize non-alphanumeric junk (keep important symbols for emails/skills)
    text = re.sub(r"[^a-z0-9\s@.+#-]", " ", text)

    # 5. normalize whitespace early (important before replacements)
    text = re.sub(r"\s+", " ", text).strip()

    # 6. fix merged technical terms (VERY IMPORTANT for embeddings)
    for wrong, correct in COMMON_FIXES.items():
        text = text.replace(wrong, correct)

    # 7. final whitespace normalization
    text = re.sub(r"\s+", " ", text).strip()

    return text