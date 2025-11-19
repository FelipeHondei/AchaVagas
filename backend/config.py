from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str = "Job Aggregator API"
    debug: bool = True

    database_url: str = "postgresql+psycopg2://jobs:jobs@localhost:5432/jobs"
    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    email_host: str | None = None
    email_port: int = 587
    email_user: str | None = None
    email_password: str | None = None
    email_from: str = "no-reply@job-aggregator.local"

    linkedin_username: str | None = None
    linkedin_password: str | None = None

    spacy_model: str = "pt_core_news_md"
    openai_api_key: str | None = None

    scraping_default_location: str = "Brazil"
    scraping_default_query: str = "Data Analyst"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if not settings.celery_broker_url:
        settings.celery_broker_url = settings.redis_url
    if not settings.celery_result_backend:
        settings.celery_result_backend = settings.redis_url
    return settings

