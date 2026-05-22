from fastapi import FastAPI

from app.config.init_db import init_db


from app.api.routes import resume_routes, job_routes
from app.api.routes.match_routes import router as match_router




app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0"
)

app.include_router(resume_routes.router)
app.include_router(job_routes.router)

app.include_router(match_router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API is running "
    }