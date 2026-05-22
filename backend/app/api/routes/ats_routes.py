from fastapi import APIRouter
from app.services.ats.ats_calculator import calculate_ats_score

router = APIRouter()


@router.post("/ats-score")
def ats_score(resume_text: str, job_text: str, missing_skills: list = None):

    result = calculate_ats_score(
        resume_text=resume_text,
        job_text=job_text,
        missing_skills=missing_skills
    )

    return result