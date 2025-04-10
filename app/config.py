from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@postgres/database" # Example URL

    class Config:
        env_file = None

settings = Settings()
