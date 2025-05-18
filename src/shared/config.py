from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Provide default values for tests
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/testdb"
    TELEGRAM_BOT_TOKEN: str = "test_token"
    TELEGRAM_API_URL: str = "https://api.telegram.org"
    OPENAI_API_KEY: str = "test_key"
    MINIO_ROOT_USER: str = "test_user"
    MINIO_ROOT_PASSWORD: str = "test_password"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_BUCKET: str = "test-bucket"
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_URL: str = "redis://localhost:6379/1"
    APP_HOST: str = "localhost"
    DEBUG: bool = False

    # ClickHouse settings
    CLICKHOUSE_HOST: str = "clickhouse"
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_USER: str = "user"
    CLICKHOUSE_PASSWORD: str = "password"
    CLICKHOUSE_DATABASE: str = "speech"

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_SERVICE: str = "speech-coach"
    LOG_COMPONENT: str = "unknown"
    STATISTICS_API_URL: str = (
        "https://aksovius.ddns.net/"  # "https://192.168.1.35:3001"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
