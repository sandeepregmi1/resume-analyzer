# /home/sandeep/Projects/resume-analyzer/backend/app/config/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

# Create DB engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


# Dependency (we will use in FastAPI routes later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()