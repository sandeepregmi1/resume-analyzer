import numpy as np
import json

from app.config.database import SessionLocal
from app.models.job_model import Job

from app.services.embeddings.embedding_model import get_embedding
from app.services.embeddings.similarity import cosine_similarity

from app.services.matching.gap_analysis import skill_gap_analyzer
from app.services.nlp.embedding_skill_extractor import extract_skills_with_embeddings


# LOAD JOBS
def load_jobs(db):
    return db.query(Job).all()


# MAIN MATCHING ENGINE
def match_jobs(resume_text: str, top_k: int = 5):

    db = SessionLocal()

    try:
    
        # 1. RESUME PROCESSING
    
        resume_embedding = get_embedding(resume_text)

        resume_skills_data = extract_skills_with_embeddings(resume_text)
        resume_skills = resume_skills_data["all_skills"]

        jobs = load_jobs(db)

        results = []

    
        # 2. LOOP JOBS
    
        for job in jobs:

            if not job.embedding:
                continue

            job_embedding = np.array(json.loads(job.embedding))

            # semantic match score
            score = cosine_similarity(resume_embedding, job_embedding)

        
            # 3. JOB SKILLS (simple extraction)
        
            job_skills = job.required_skills.split(",") if job.required_skills else []

            print(job_skills, score)

        
            # 4. SKILL GAP ANALYSIS
        
            gap = skill_gap_analyzer(
                resume_skills=resume_skills,
                job_skills=job_skills
            )

        
            # 5. FINAL RESULT
        
            results.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "match_score": round(score * 100, 2),

                "gap_analysis": gap
            })

    
        # 6. SORT RESULTS
    
        results = sorted(results, key=lambda x: x["match_score"], reverse=True)

        return {
            "top_matches": results[:top_k]
        }

    finally:
        db.close()