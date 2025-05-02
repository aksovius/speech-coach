"""Tests for audio_schema.py module."""

import pytest
from pydantic import ValidationError

from shared.schemas.audio_schema import AudioTaskProcessing, AudioTaskResult


def test_audio_task_processing_valid():
    """Test valid AudioTaskProcessing model creation."""
    # Test data
    data = {"telegram_id": 123456, "user_id": 1, "file_path": "/path/to/audio.ogg"}

    # Create model instance
    task = AudioTaskProcessing(**data)

    # Verify fields
    assert task.telegram_id == data["telegram_id"]
    assert task.user_id == data["user_id"]
    assert task.file_path == data["file_path"]


def test_audio_task_processing_invalid():
    """Test invalid AudioTaskProcessing model creation."""
    # Test data with missing required field
    data = {
        "telegram_id": 123456,
        "user_id": 1,
        # Missing file_path
    }

    # Verify validation error
    with pytest.raises(ValidationError):
        AudioTaskProcessing(**data)


def test_audio_task_result_valid():
    """Test valid AudioTaskResult model creation."""
    # Test data
    data = {
        "telegram_id": 123456,
        "user_id": 1,
        "converted_file": "/path/to/converted.wav",
        "uploaded_file": "/path/to/uploaded.wav",
    }

    # Create model instance
    result = AudioTaskResult(**data)

    # Verify fields
    assert result.telegram_id == data["telegram_id"]
    assert result.user_id == data["user_id"]
    assert result.converted_file == data["converted_file"]
    assert result.uploaded_file == data["uploaded_file"]
    assert result.error is None


def test_audio_task_result_with_error():
    """Test AudioTaskResult model creation with error."""
    # Test data with error
    data = {
        "telegram_id": 123456,
        "user_id": 1,
        "converted_file": "/path/to/converted.wav",
        "uploaded_file": "/path/to/uploaded.wav",
        "error": "Conversion failed",
    }

    # Create model instance
    result = AudioTaskResult(**data)

    # Verify error field
    assert result.error == data["error"]
