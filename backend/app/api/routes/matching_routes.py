from fastapi import APIRouter
from app.services.matching.job_matcher import match_jobs

router = APIRouter()


@router.post("/match-jobs")
def match_jobs_api(resume_text: str):

    result = match_jobs(resume_text)

    return result