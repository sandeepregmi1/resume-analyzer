from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity
from app.services.nlp.skill_embeddings import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
    build_skill_embeddings
)



# Precompute skill embeddings (load once)
SKILL_VECTORS = build_skill_embeddings()

THRESHOLD = 0.65  # tuning parameter


def extract_skills_with_embeddings(text: str):
    text_embedding = get_embedding(text)

    technical_found = []
    soft_found = []

    all_skills = TECHNICAL_SKILLS + SOFT_SKILLS

    for skill in all_skills:
        skill_embedding = SKILL_VECTORS[skill]

        score = cosine_similarity(text_embedding, skill_embedding)

        if score >= THRESHOLD:
            if skill in TECHNICAL_SKILLS:
                technical_found.append(skill)
            else:
                soft_found.append(skill)

    return {
        "technical_skills": technical_found,
        "soft_skills": soft_found,
        "all_skills": technical_found + soft_found
    }