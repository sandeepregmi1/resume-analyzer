from app.services.embeddings.embedding_model import get_embedding

TECHNICAL_SKILLS = [
    "python", "java", "javascript", "react", "fastapi",
    "docker", "kubernetes", "aws", "sql", "mongodb",
    "machine learning", "deep learning", "nlp"
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership",
    "problem solving", "adaptability"
]


def build_skill_embeddings():
    skill_vectors = {}

    for skill in TECHNICAL_SKILLS + SOFT_SKILLS:
        skill_vectors[skill] = get_embedding(skill)

    return skill_vectors