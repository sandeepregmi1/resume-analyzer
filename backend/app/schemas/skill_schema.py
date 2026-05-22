from pydantic import BaseModel
from typing import List, Dict


class SkillSchema(BaseModel):
    """
    Single source of truth for ALL skill outputs in system
    """

    technical_skills: List[str]
    soft_skills: List[str]
    all_skills: List[str]


class SkillScoreSchema(BaseModel):
    skill_name: str
    score: float


class SkillExtractionResponse(BaseModel):
    skills: SkillSchema
    confidence: Dict[str, float] = {}