from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity


def rank_jobs_by_vector(resume_vector: list, jobs: list, top_k=10):
    """
    Fast vector-based job ranking
    """

    scored_jobs = []

    for job in jobs:

        job_vector = job.embedding

        if not job_vector:
            continue

        score = cosine_similarity(resume_vector, job_vector)

        scored_jobs.append({
            "job_id": job.id,
            "title": job.title,
            "score": float(round(score * 100, 2)),
            "required_skills": job.required_skills
        })

    scored_jobs.sort(key=lambda x: x["score"], reverse=True)

    return scored_jobs[:top_k]