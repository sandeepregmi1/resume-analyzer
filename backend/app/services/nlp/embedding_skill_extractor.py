from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity
from app.services.nlp.skill_embeddings import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
    build_skill_embeddings
)



# Precompute skill embeddings (load once)
SKILL_VECTORS = build_skill_embeddings()

THRESHOLD = 0.45  # tuning parameter


def extract_skills_with_embeddings(text: str):
    technical_found = []
    soft_found = []

    text_lower = text.lower()

    # 1. Exact string matching (Fast and accurate for explicit skills)
    for skill in TECHNICAL_SKILLS:
        if skill.lower() in text_lower:
            technical_found.append(skill)

    for skill in SOFT_SKILLS:
        if skill.lower() in text_lower:
            soft_found.append(skill)

    # 2. Semantic matching for variations (The AI part)
    # We chunk the text into smaller pieces so the embedding doesn't get diluted
    words = text.split()
    chunks = [" ".join(words[i:i+50]) for i in range(0, len(words), 50)]

    all_skills = TECHNICAL_SKILLS + SOFT_SKILLS
    unfound_skills = [s for s in all_skills if s not in technical_found and s not in soft_found]

    if unfound_skills and chunks:
        chunk_embeddings = [get_embedding(c) for c in chunks[:10]] # limit to first 10 chunks to avoid slow processing
        
        for skill in unfound_skills:
            skill_embedding = SKILL_VECTORS[skill]
            
            # Find max similarity across any chunk
            max_sim = max(cosine_similarity(ce, skill_embedding) for ce in chunk_embeddings)
            
            if max_sim >= THRESHOLD:
                if skill in TECHNICAL_SKILLS:
                    technical_found.append(skill)
                else:
                    soft_found.append(skill)

    return {
        "technical_skills": list(set(technical_found)),
        "soft_skills": list(set(soft_found)),
        "all_skills": list(set(technical_found + soft_found))
    }