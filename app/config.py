from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    DEBUG: bool = False
    
    class Config:
        env_file = None

settings = Settings()
