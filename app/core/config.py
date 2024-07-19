# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "CrewAI"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080", "https://localhost", "https://localhost:8080"]


    model_config = SettingsConfigDict(env_file_encoding="utf-8")

# Create a global instance of the Settings
settings = Settings()
