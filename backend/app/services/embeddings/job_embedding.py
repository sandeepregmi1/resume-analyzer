import json
from app.services.embeddings.embedding_model import get_embedding


def generate_job_embedding(job_text: str):
    embedding = get_embedding(job_text)
    return embedding.tolist()


def serialize_embedding(embedding):
    return json.dumps(embedding)


def deserialize_embedding(embedding_str):
    return json.loads(embedding_str)