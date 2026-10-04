import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgrespassword@localhost:5433/postgres"
    )
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: str = "guest"

    class Config:
        env_file = ".env"

settings = Settings()
