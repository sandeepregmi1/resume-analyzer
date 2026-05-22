from app.services.embeddings.embedding_model import get_embedding


def generate_job_embedding(job_text: str):
    """
    Always returns: List[float]
    """
    embedding = get_embedding(job_text)
    return embedding.tolist()  # standardized output


def prepare_job_text(job):
    """
    Single source of truth for job embedding input
    """
    return f"""
    {job.title}
    {job.description}
    {" ".join(job.required_skills or [])}
    """.lower()