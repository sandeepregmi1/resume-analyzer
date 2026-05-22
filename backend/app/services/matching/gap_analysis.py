from typing import List



# MAIN GAP ANALYZER
def analyze_skill_gap(resume_skills: List[str], job_skills: List[str]):

    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    # Common skills
    matched_skills = list(resume_set.intersection(job_set))

    # Missing skills (critical for job)
    missing_skills = list(job_set - resume_set)

    # Extra skills (not required by job)
    extra_skills = list(resume_set - job_set)

    # Gap score (how well resume matches job)
    if len(job_set) == 0:
        gap_score = 0
    else:
        gap_score = (len(matched_skills) / len(job_set)) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "gap_score": round(gap_score, 2)
    }

# RECOMMENDATION ENGINE (RULE-BASED AI)

def generate_recommendations(missing_skills: List[str]):

    recommendations = []

    for skill in missing_skills:

        if skill in ["aws", "azure", "gcp"]:
            recommendations.append("Learn cloud fundamentals + deploy a project")

        elif skill in ["docker", "kubernetes"]:
            recommendations.append("Practice containerization + microservices")

        elif skill in ["machine learning", "ml"]:
            recommendations.append("Study ML basics + build 2 ML projects")

        elif skill in ["sql", "postgresql", "mongodb"]:
            recommendations.append("Practice database queries and schema design")

        elif skill in ["fastapi", "django", "flask"]:
            recommendations.append("Build REST APIs and authentication systems")

        else:
            recommendations.append(f"Learn {skill} through projects and tutorials")

    return recommendations

# COMBINE EVERYTHING (FINAL ENGINE)

def skill_gap_analyzer(resume_skills, job_skills):

    base_analysis = analyze_skill_gap(resume_skills, job_skills)

    recommendations = generate_recommendations(base_analysis["missing_skills"])

    base_analysis["recommendations"] = recommendations

    return base_analysis