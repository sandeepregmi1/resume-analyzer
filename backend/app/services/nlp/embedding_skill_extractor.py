from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity
from app.services.nlp.skill_embeddings import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
    build_skill_embeddings
)

# Precompute once
SKILL_VECTORS = build_skill_embeddings()

# ---------- CONFIG ----------
TOP_K_TECH = 8
TOP_K_SOFT = 5


def _score_skills(text_embedding, skills):
    """Return ranked skills with similarity scores"""
    scored = []

    for skill in skills:
        skill_emb = SKILL_VECTORS[skill]
        score = cosine_similarity(text_embedding, skill_emb)
        scored.append((skill, score))

    # sort highest first
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored


def extract_skills_with_embeddings(text: str):
    """
    Stable deterministic skill extractor:
    - No chunking
    - No threshold dependency
    - Top-K ranking instead of binary filtering
    """

    text = text.lower()

    # 1. single embedding (stable representation)
    text_embedding = get_embedding(text)

    # 2. score all skills
    tech_scored = _score_skills(text_embedding, TECHNICAL_SKILLS)
    soft_scored = _score_skills(text_embedding, SOFT_SKILLS)

    # 3. deterministic selection (TOP-K)
    technical_found = [s for s, _ in tech_scored[:TOP_K_TECH]]
    soft_found = [s for s, _ in soft_scored[:TOP_K_SOFT]]

    return {
        "technical_skills": technical_found,
        "soft_skills": soft_found,
        "all_skills": technical_found + soft_found
    }