from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str
    MINIO_BUCKET: str
    DEBUG: bool = False
    
    class Config:
        env_file = None

settings = Settings()
