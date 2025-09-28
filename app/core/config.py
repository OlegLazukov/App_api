from pydantic import Field
from pydantic_settings import BaseSettings  # pydantic 2.x moved BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description="SQLAlchemy DSN, e.g. postgresql+psycopg2://user:pass@host:5432/db")
    APP_ENV: str = "dev"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
