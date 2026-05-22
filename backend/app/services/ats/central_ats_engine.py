from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity


# 1. STRUCTURE INTELLIGENCE
def structure_score(text: str) -> float:
    text = text.lower()

    score = 0

    sections = {
        "experience": 25,
        "education": 20,
        "project": 25,
        "skills": 15,
        "summary": 15
    }

    for key, val in sections.items():
        if key in text:
            score += val

    # length normalization
    word_count = len(text.split())
    if 100 <= word_count <= 1200:
        score += 20
    elif word_count > 1200:
        score += 10

    return min(score, 100)


# 2. SKILL MATCH INTELLIGENCE
def skill_score(resume_skills, job_skills):
    if not job_skills:
        return 50  # neutral baseline

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set.intersection(job_set)

    precision = len(matched) / len(job_set) * 100
    recall = len(matched) / max(len(resume_set), 1) * 100

    return (precision * 0.6 + recall * 0.4)


# 3. SEMANTIC INTELLIGENCE
def semantic_score(resume_text: str, job_text: str):
    if not job_text:
        return 60  # neutral fallback

    r_vec = get_embedding(resume_text)
    j_vec = get_embedding(job_text)

    return max(0, cosine_similarity(r_vec, j_vec) * 100)


# 4. ROLE ALIGNMENT (NEW LAYER)
def role_alignment_score(resume_text: str, job_text: str):
    """
    Detects how aligned resume is to job domain.
    Simple but effective heuristic layer.
    """

    resume_text = resume_text.lower()
    job_text = job_text.lower()

    job_keywords = set(job_text.split())
    resume_words = set(resume_text.split())

    overlap = resume_words.intersection(job_keywords)

    if not job_keywords:
        return 50

    return len(overlap) / len(job_keywords) * 100


# FINAL ATS BRAIN
def calculate_ats_score(
    resume_text: str,
    job_text: str,
    resume_skills=None,
    job_skills=None
):

    resume_skills = resume_skills or []
    job_skills = job_skills or []

    struct = structure_score(resume_text)
    skill = skill_score(resume_skills, job_skills)
    sem = semantic_score(resume_text, job_text)
    role = role_alignment_score(resume_text, job_text)

    final = (
        struct * 0.25 +
        skill * 0.30 +
        sem * 0.30 +
        role * 0.15
    )

    return {
        "ats_score": round(final, 2),
        "breakdown": {
            "structure": round(struct, 2),
            "skill_match": round(skill, 2),
            "semantic": round(sem, 2),
            "role_alignment": round(role, 2),
        }
    }