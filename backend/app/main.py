from fastapi import FastAPI

app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API is running 🚀"
    }