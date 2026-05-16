from sqlalchemy import Column, Integer, Float, ForeignKey, Text, DateTime
from datetime import datetime

from app.config.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    score = Column(Float, default=0.0)

    missing_skills = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)