from pydantic import Extra
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    #JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int
    REFRESH_TOKEN_HOURS: int

    class Config:
        env_file = Path(__file__).resolve().parents[2]/".env"
        extra = Extra.allow

@lru_cache()
def get_settings() -> Settings:
    return Settings()