from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@postgres/toefl"

    class Config:
        env_file = ".env"

settings = Settings()
