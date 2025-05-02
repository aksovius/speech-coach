"""Tests for audio_processing.py module."""

import os
import tempfile
from unittest.mock import patch

import pytest

from shared.services.audio_processing import convert_ogg_to_wav


@pytest.mark.asyncio
async def test_convert_ogg_to_wav_success():
    """Test successful OGG to WAV conversion."""
    # Create temporary OGG file
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_ogg:
        temp_ogg.write(b"fake ogg data")
        temp_ogg_path = temp_ogg.name

    # Create temporary WAV file path
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        # Mock AudioSegment
        with patch("pydub.AudioSegment.from_file") as mock_from_file:
            mock_audio = mock_from_file.return_value
            mock_audio.__len__.return_value = 60000  # 60 seconds
            mock_audio.__getitem__.return_value = mock_audio
            mock_audio.export.return_value = None

            # Call convert_ogg_to_wav
            result = await convert_ogg_to_wav(temp_ogg_path, temp_wav_path)

            # Verify the result
            assert result == temp_wav_path
            mock_from_file.assert_called_once_with(temp_ogg_path, format="ogg")
            mock_audio.export.assert_called_once()
    finally:
        # Clean up temporary files
        os.unlink(temp_ogg_path)
        os.unlink(temp_wav_path)


@pytest.mark.asyncio
async def test_convert_ogg_to_wav_with_time_limit():
    """Test OGG to WAV conversion with time limit."""
    # Create temporary OGG file
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_ogg:
        temp_ogg.write(b"fake ogg data")
        temp_ogg_path = temp_ogg.name

    # Create temporary WAV file path
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        # Mock AudioSegment
        with patch("pydub.AudioSegment.from_file") as mock_from_file:
            mock_audio = mock_from_file.return_value
            mock_audio.__len__.return_value = 60000  # 60 seconds
            mock_audio.__getitem__.return_value = mock_audio
            mock_audio.export.return_value = None

            # Call convert_ogg_to_wav with time limit
            result = await convert_ogg_to_wav(
                temp_ogg_path, temp_wav_path, time_limit=30
            )

            # Verify the result
            assert result == temp_wav_path
            mock_from_file.assert_called_once_with(temp_ogg_path, format="ogg")
            mock_audio.__getitem__.assert_called_once_with(
                slice(None, 30000)
            )  # 30 seconds in milliseconds
            mock_audio.export.assert_called_once()
    finally:
        # Clean up temporary files
        os.unlink(temp_ogg_path)
        os.unlink(temp_wav_path)


@pytest.mark.asyncio
async def test_convert_ogg_to_wav_exception():
    """Test error handling in OGG to WAV conversion."""
    # Create temporary OGG file
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_ogg:
        temp_ogg.write(b"fake ogg data")
        temp_ogg_path = temp_ogg.name

    # Create temporary WAV file path
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        # Mock AudioSegment to raise an exception
        with patch("pydub.AudioSegment.from_file") as mock_from_file:
            mock_from_file.side_effect = Exception("FFmpeg error")

            # Call convert_ogg_to_wav and verify exception
            with pytest.raises(Exception) as exc_info:
                await convert_ogg_to_wav(temp_ogg_path, temp_wav_path)

            assert str(exc_info.value) == "FFmpeg error"
    finally:
        # Clean up temporary files
        os.unlink(temp_ogg_path)
        os.unlink(temp_wav_path)
