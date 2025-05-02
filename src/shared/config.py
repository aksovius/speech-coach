from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Provide default values for tests
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/testdb"
    TELEGRAM_BOT_TOKEN: str = "test_token"
    OPENAI_API_KEY: str = "test_key"
    MINIO_ROOT_USER: str = "test_user"
    MINIO_ROOT_PASSWORD: str = "test_password"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_BUCKET: str = "test-bucket"
    REDIS_URL: str = "redis://localhost:6379"
    APP_HOST: str = "localhost"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
