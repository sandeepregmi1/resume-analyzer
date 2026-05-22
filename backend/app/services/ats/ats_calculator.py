import re
from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity


# 1. KEYWORD MATCH SCORE
def keyword_score(resume_text: str, job_text: str):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    if not job_words:
        return 0

    match = resume_words.intersection(job_words)
    return len(match) / len(job_words) * 100


# 2. SEMANTIC SIMILARITY SCORE
def semantic_score(resume_text: str, job_text: str):
    resume_vec = get_embedding(resume_text)
    job_vec = get_embedding(job_text)

    score = cosine_similarity(resume_vec, job_vec)
    return max(0, score * 100)


# 3. STRUCTURE SCORE (BASIC RULES)
def structure_score(resume_text: str):
    score = 0

    if "experience" in resume_text.lower():
        score += 25
    if "education" in resume_text.lower():
        score += 25
    if "project" in resume_text.lower():
        score += 25
    if len(resume_text.split()) > 100:
        score += 25

    return score


# 4. FINAL ATS SCORE
def calculate_ats_score(resume_text: str, job_text: str, missing_skills=None):

    kw = keyword_score(resume_text, job_text)
    sem = semantic_score(resume_text, job_text)
    struct = structure_score(resume_text)

    skill_score = 100 if missing_skills is None else max(0, 100 - len(missing_skills) * 10)

    final_score = (
        kw * 0.2 +
        sem * 0.3 +
        skill_score * 0.4 +
        struct * 0.1
    )

    return {
        "ats_score": round(final_score, 2),
        "breakdown": {
            "keyword_match": round(kw, 2),
            "semantic_similarity": round(sem, 2),
            "skill_match": round(skill_score, 2),
            "structure_score": round(struct, 2),
        },
        "missing_skills": missing_skills or []
    }