from fastapi import FastAPI

from app.config.init_db import init_db

from app.api.routes.resume_routes import router as resume_router

app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0"
)

app.include_router(resume_router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API is running 🚀"
    }