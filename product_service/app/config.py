from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Подключаемся к той же базе, но порт используем 5433, как настроили в Docker
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgrespassword@localhost:5433/postgres"

    class Config:
        env_file = ".env"

settings = Settings()
