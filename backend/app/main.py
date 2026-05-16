from fastapi import FastAPI

from app.config.init_db import init_db

app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API is running 🚀"
    }