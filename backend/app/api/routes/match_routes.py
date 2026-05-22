from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.resume_model import Resume
from app.models.job_model import Job

from app.services.matching.vector_matcher import rank_jobs_by_vector

from app.services.embeddings.resume_embedding import generate_resume_embedding

router = APIRouter()


@router.get("/vector-match/{resume_id}")
def vector_match(resume_id: int):

    db: Session = SessionLocal()

    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    jobs = db.query(Job).all()

    # Use stored vector if available, otherwise generate it
    resume_vector = resume.embedding
    if not resume_vector:
        resume_vector = generate_resume_embedding(resume.raw_text)

    results = rank_jobs_by_vector(
        resume_vector=resume_vector,
        jobs=jobs,
        top_k=10
    )

    db.close()

    return {
        "resume_id": resume_id,
        "top_matches": results
    }