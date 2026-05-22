from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.config.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    file_name = Column(String, nullable=False)
    raw_text = Column(Text, nullable=True)

    parsed_json = Column(JSONB, nullable=True)  

    embedding = Column(JSONB, nullable=True)

    ats_score = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)