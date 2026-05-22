from app.services.embeddings.embedding_model import get_embedding

def generate_resume_embedding(resume_text: str):
    """
    Always returns: List[float]
    """
    embedding = get_embedding(resume_text)
    return embedding.tolist()  # standardized output
