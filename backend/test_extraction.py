from app.services.nlp.embedding_skill_extractor import extract_skills_with_embeddings
from app.services.nlp.embedding_skill_extractor import SKILL_VECTORS, get_embedding, cosine_similarity

text = """
Ram Sharma
Professional Summary
Senior Data Scientist and Machine Learning Engineer specializing in Generative AI, LLMs, and Autonomous AI Systems...
Technical Skills: Python, Scikit-Learn, TensorFlow, Keras, PyTorch, NLTK, Hugging Face Transformers, OpenCV, FastAPI, Flask, Streamlit.
"""

from app.services.nlp.embedding_skill_extractor import get_embedding, _score_skills, TECHNICAL_SKILLS, SOFT_SKILLS

emb = get_embedding(text.lower().strip())
tech_scored = _score_skills(emb, TECHNICAL_SKILLS)
soft_scored = _score_skills(emb, SOFT_SKILLS)

print("Top 10 Tech Skills Scores:")
for s, score in tech_scored[:10]:
    print(f"{s}: {score}")

print("Top 10 Soft Skills Scores:")
for s, score in soft_scored[:10]:
    print(f"{s}: {score}")

print("Extracted:", extract_skills_with_embeddings(text))
