from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from typing import List

from app.config.database import SessionLocal
from app.models.job_model import Job

from app.services.embeddings.job_embedding import (
    generate_job_embedding,
    prepare_job_text
)

router = APIRouter()


@router.post("/create-job")
def create_job(
    title: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(..., description="Comma-separated skills, e.g. python,fastapi,docker")
):
    # Parse comma-separated string into clean list
    skills_list = [s.strip() for s in required_skills.split(",") if s.strip()]

    db: Session = SessionLocal()

    # 1. Create job object
    job = Job(
        title=title,
        description=description,
        required_skills=",".join(skills_list)
    )

    # 2. Generate embedding
    job_text = prepare_job_text(job)
    job.embedding = generate_job_embedding(job_text)

    # 3. Save to DB
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()

    return {
        "message": "Job created with embedding",
        "job_id": job.id,
        "title": title,
        "skills_parsed": skills_list
    }