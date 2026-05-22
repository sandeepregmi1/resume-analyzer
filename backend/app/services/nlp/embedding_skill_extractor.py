from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity
from app.services.nlp.skill_embeddings import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
    build_skill_embeddings
)

# Precompute once
SKILL_VECTORS = build_skill_embeddings()

# CONFIG
TOP_K_TECH = 8
TOP_K_SOFT = 5

# IMPORTANT: stability threshold (prevents fake skills)
MIN_SCORE = 0.45


def _score_skills(text_embedding, skills):
    scored = []

    for skill in skills:
        skill_emb = SKILL_VECTORS[skill]
        score = cosine_similarity(text_embedding, skill_emb)
        scored.append((skill, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def _filter_by_threshold(scored_list):
    """Remove weak / noisy matches"""
    return [s for s, score in scored_list if score >= MIN_SCORE]


def extract_skills_with_embeddings(text: str):
    """
    Stable + deterministic + no hallucinated skills
    """

    if not text:
        return {
            "technical_skills": [],
            "soft_skills": [],
            "all_skills": []
        }

    text = text.lower().strip()

    # single embedding (stable + deterministic)
    text_embedding = get_embedding(text)

    # 1. Exact Keyword Matching (Prevents Signal Dilution)
    tech_exact = [s for s in TECHNICAL_SKILLS if s in text]
    soft_exact = [s for s in SOFT_SKILLS if s in text]

    # 2. Semantic Scoring for synonyms/context
    tech_scored = _score_skills(text_embedding, TECHNICAL_SKILLS)
    soft_scored = _score_skills(text_embedding, SOFT_SKILLS)

    tech_filtered = _filter_by_threshold(tech_scored)
    soft_filtered = _filter_by_threshold(soft_scored)

    # 3. Combine Exact + Semantic, remove duplicates
    tech_combined = list(dict.fromkeys(tech_exact + [s for s, _ in tech_filtered]))
    soft_combined = list(dict.fromkeys(soft_exact + [s for s, _ in soft_filtered]))

    # Apply Top-K
    technical_found = tech_combined[:TOP_K_TECH]
    soft_found = soft_combined[:TOP_K_SOFT]

    return {
        "technical_skills": technical_found,
        "soft_skills": soft_found,
        "all_skills": technical_found + soft_found
    }