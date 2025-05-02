"""Tests for audio_service.py module."""

from unittest.mock import AsyncMock, patch

import pytest

from shared.schemas.audio_schema import AudioTaskProcessing

# Use patch for broker module before importing audio_service
with patch("shared.messaging.broker.broker") as mock_broker:
    # Configure mocks
    mock_broker.publish = AsyncMock()

    # Now import the module
    from shared.services import audio_service


@pytest.mark.asyncio
async def test_process_voice_message_success():
    """Test successful voice message processing."""
    # Input data
    file_url = "https://example.com/voice.ogg"
    user_id = 123
    telegram_id = 456
    downloaded_file_path = "shared/temp/test-uuid.ogg"

    # Mock for download_service
    with patch(
        "shared.services.download_service.download_file",
        AsyncMock(return_value=downloaded_file_path),
    ):
        # Mock for uuid.uuid4()
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = "test-uuid"

            # Reset mock for broker.publish
            audio_service.broker.publish.reset_mock()

            # Call the tested method
            result = await audio_service.process_voice_message(
                file_url, user_id, telegram_id
            )

            # Check results
            audio_service.broker.publish.assert_called_once()
            call_args = audio_service.broker.publish.call_args[0]
            # Check that first argument is an instance of AudioTaskProcessing
            assert isinstance(call_args[0], AudioTaskProcessing)
            assert call_args[0].telegram_id == telegram_id
            assert call_args[0].user_id == user_id
            assert call_args[0].file_path == downloaded_file_path
            # Check that correct stream is specified
            assert audio_service.broker.publish.call_args[1]["stream"] == "audio_stream"
            # Expect empty dict for success (or None)
            assert result is None or result == {}


@pytest.mark.asyncio
async def test_process_voice_message_download_failure():
    """Test voice message processing when download fails."""
    # Input data
    file_url = "https://example.com/voice.ogg"
    user_id = 123
    telegram_id = 456

    # Mock for download_service with download failure
    with patch(
        "shared.services.download_service.download_file", AsyncMock(return_value=None)
    ):
        # Mock for uuid.uuid4()
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = "test-uuid"

            # Reset mock for broker.publish
            audio_service.broker.publish.reset_mock()

            # Call the tested method
            result = await audio_service.process_voice_message(
                file_url, user_id, telegram_id
            )

            # Check results
            audio_service.broker.publish.assert_not_called()
            # Check error message
            assert "error" in result
            assert result["error"] == "Failed to download the audio file."
