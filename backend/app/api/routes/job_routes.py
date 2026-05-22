from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.job_model import Job

from app.services.embeddings.job_embedding import (
    generate_job_embedding,
    prepare_job_text
)

router = APIRouter()


@router.post("/create-job")
def create_job(title: str, description: str, required_skills: list):

    db: Session = SessionLocal()

    # 1. Create job object
    job = Job(
        title=title,
        description=description,
        required_skills=required_skills
    )

    # 2. 👉 THIS IS WHERE YOU ADD IT (IMPORTANT)
    job_text = prepare_job_text(job)
    job.embedding = generate_job_embedding(job_text)

    # 3. Save to DB
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()

    return {
        "message": "Job created with embedding",
        "job_id": job.id
    }