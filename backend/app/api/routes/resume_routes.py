import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.resume_model import Resume

from app.schemas.skill_schema import SkillSchema

from app.services.parser.pdf_parser import extract_text_from_pdf
from app.services.parser.docx_parser import extract_text_from_docx
from app.services.parser.txt_parser import extract_text_from_txt
from app.services.parser.cleaner import clean_resume_text

from app.services.nlp.embedding_skill_extractor import extract_skills_with_embeddings
from app.services.ats.ats_calculator import calculate_ats_score

router = APIRouter()

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_extension = file.filename.split(".")[-1].lower()
    allowed_extensions = ["pdf", "docx", "txt"]

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed"
        )

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if file_extension == "pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif file_extension == "docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raw_text = extract_text_from_txt(file_path)

    # Clean text
    cleaned_text = clean_resume_text(raw_text)

    
    # 1. Skill Extraction (Validated)
    
    raw_skills = extract_skills_with_embeddings(cleaned_text)

    try:
        skills = SkillSchema(**raw_skills).model_dump()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Skill schema validation failed: {str(e)}"
        )

    
    # 2. ATS ENGINE (FIXED LOGIC)
    
    ats_result = calculate_ats_score(
        resume_text=cleaned_text,
        job_text="",          # FIX: no fake self-comparison
        missing_skills=[]
    )

    
    # 3. DB SAVE
    
    db: Session = SessionLocal()

    new_resume = Resume(
        file_name=file.filename,
        raw_text=cleaned_text,
        parsed_json=skills,
        ats_score=ats_result["ats_score"]
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    db.close()

    return {
        "message": "Resume uploaded successfully",
        "resume_id": new_resume.id,
        "file_name": file.filename,
        "text_preview": cleaned_text[:500],
        "ats_score": ats_result,
        "skills": skills
    }