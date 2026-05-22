from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.job_model import Job
from app.services.embeddings.job_embedding import (
    generate_job_embedding,
    serialize_embedding
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-job")
def create_job(title: str, company: str, description: str, db: Session = Depends(get_db)):

    embedding = generate_job_embedding(description)

    new_job = Job(
        title=title,
        company=company,
        description=description,
        embedding=serialize_embedding(embedding)
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created",
        "job_id": new_job.id
    }