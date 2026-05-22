import re
from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity



# STRUCTURE SCORE (RULE-BASED)

def structure_score(resume_text: str):
    score = 0
    text = resume_text.lower()

    if "experience" in text:
        score += 25
    if "education" in text:
        score += 25
    if "project" in text:
        score += 25
    if len(text.split()) > 100:
        score += 25

    return score


# KEYWORD MATCH
def keyword_score(resume_text: str, job_text: str):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    if not job_words:
        return 0

    return len(resume_words.intersection(job_words)) / len(job_words) * 100


# SEMANTIC SIMILARITY
def semantic_score(resume_text: str, job_text: str):
    resume_vec = get_embedding(resume_text)
    job_vec = get_embedding(job_text)

    return max(0, cosine_similarity(resume_vec, job_vec) * 100)


# FINAL ATS ENGINE (ONLY ONE SOURCE OF TRUTH)
def calculate_ats_score(resume_text: str, job_text: str, missing_skills=None):

    kw = keyword_score(resume_text, job_text)
    sem = semantic_score(resume_text, job_text)
    struct = structure_score(resume_text)

    skill_penalty = 0
    if missing_skills:
        skill_penalty = len(missing_skills) * 8

    skill_score = max(100 - skill_penalty, 40)

    final_score = (
        kw * 0.25 +
        sem * 0.35 +
        skill_score * 0.25 +
        struct * 0.15
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