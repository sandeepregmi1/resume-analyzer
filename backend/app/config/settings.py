from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Analyzer API"

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    DATABASE_URL: str

    CHROMA_DB_PATH: str = "./chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()