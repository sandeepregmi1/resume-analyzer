# /home/sandeep/Projects/resume-analyzer/backend/app/config/croma.py
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config.settings import settings


# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH,
    settings=ChromaSettings(
        anonymized_telemetry=False
    )
)


# Function to get or create a collection
def get_collection(name: str):
    return chroma_client.get_or_create_collection(name=name)