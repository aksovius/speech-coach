"""Test configuration for the src directory."""

from unittest.mock import patch

import pytest


# Apply patch to settings before any imports
@pytest.fixture(scope="session", autouse=True)
def patch_settings():
    """Patch settings globally for all tests."""
    mock_settings = {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/testdb",
        "TELEGRAM_BOT_TOKEN": "test_token",
        "OPENAI_API_KEY": "test_key",
        "MINIO_ROOT_USER": "test_user",
        "MINIO_ROOT_PASSWORD": "test_password",
        "MINIO_ENDPOINT": "localhost:9000",
        "MINIO_BUCKET": "test-bucket",
        "REDIS_URL": "redis://localhost:6379",
        "APP_HOST": "localhost",
        "DEBUG": "True",
    }

    with patch.dict("os.environ", mock_settings):
        yield
