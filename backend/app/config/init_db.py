# /home/sandeep/Projects/resume-analyzer/backend/app/config/init_db.py
from app.config.database import Base, engine

# Import all models so SQLAlchemy registers them
from app.models import User, Resume, Job, Match


def init_db():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")