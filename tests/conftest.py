"""Pytest fixtures for testing."""

import asyncio
import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def event_loop():
    """Fixture to provide an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_config():
    """Fixture to mock config settings."""
    with patch("shared.config.settings") as mock_settings:
        mock_settings.MINIO_ROOT_USER = "test_user"
        mock_settings.MINIO_ROOT_PASSWORD = "test_password"
        mock_settings.MINIO_ENDPOINT = "localhost:9000"
        mock_settings.MINIO_BUCKET = "test-bucket"
        mock_settings.REDIS_URL = "redis://localhost:6379"
        mock_settings.DATABASE_URL = "postgresql://user:password@localhost:5432/testdb"
        mock_settings.TELEGRAM_BOT_TOKEN = "test_token"
        mock_settings.OPENAI_API_KEY = "test_key"
        mock_settings.APP_HOST = "localhost"
        mock_settings.DEBUG = True
        yield mock_settings


@pytest.fixture
def mock_broker():
    """Fixture to mock message broker."""
    with patch("shared.messaging.broker.broker") as mock_broker:
        # Create Future for async result
        future = asyncio.Future()
        future.set_result(None)

        # Add connect method and other necessary attributes
        mock_broker.connect = MagicMock(return_value=future)
        mock_broker.publish = MagicMock(return_value=future)
        mock_broker.producer = True  # Needed for check in broker.publish
        mock_broker.is_connected = True

        yield mock_broker


@pytest.fixture
def temp_file():
    """Fixture to create and clean up a temporary file."""
    filepath = "test_temp_file.txt"
    with open(filepath, "w") as f:
        f.write("test content")
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def temp_ogg_file():
    """Mock fixture for ogg file."""
    filepath = "test_audio.ogg"
    # This doesn't create a real OGG file, just a mock
    with open(filepath, "w") as f:
        f.write("mock ogg data")
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def mock_s3_client():
    """Fixture to mock S3 client for MinIO."""
    with patch("aioboto3.Session") as mock_session:
        mock_client = MagicMock()
        mock_client.__aenter__ = MagicMock(return_value=mock_client)
        mock_client.__aexit__ = MagicMock(return_value=None)
        mock_client.upload_file = MagicMock()
        mock_client.download_file = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        yield mock_client
