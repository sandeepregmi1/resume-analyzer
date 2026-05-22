from app.services.nlp.embedding_skill_extractor import extract_skills_with_embeddings
from app.services.nlp.embedding_skill_extractor import SKILL_VECTORS, get_embedding, cosine_similarity

text = """
Muhammad Ghulam Jillani
Professional Summary
Senior Data Scientist and Machine Learning Engineer specializing in Generative AI, LLMs, and Autonomous AI Systems...
Technical Skills: Python, Scikit-Learn, TensorFlow, Keras, PyTorch, NLTK, Hugging Face Transformers, OpenCV, FastAPI, Flask, Streamlit.
"""

print(extract_skills_with_embeddings(text))
