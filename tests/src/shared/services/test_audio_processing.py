"""Tests for audio_processing.py module."""

import os
import tempfile
from unittest.mock import AsyncMock, patch

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
        # Mock the subprocess.run function
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = AsyncMock(returncode=0)

            # Call convert_ogg_to_wav
            await convert_ogg_to_wav(temp_ogg_path, temp_wav_path)

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == "ffmpeg"
            assert "-i" in args
            assert temp_ogg_path in args
            assert temp_wav_path in args
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
        # Mock the subprocess.run function
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = AsyncMock(returncode=0)

            # Call convert_ogg_to_wav with time limit
            await convert_ogg_to_wav(temp_ogg_path, temp_wav_path, time_limit=30)

            # Verify subprocess.run was called with correct arguments including time limit
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == "ffmpeg"
            assert "-i" in args
            assert temp_ogg_path in args
            assert temp_wav_path in args
            assert "-t" in args
            assert "30" in args
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
        # Mock the subprocess.run function to raise an exception
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("FFmpeg error")

            # Call convert_ogg_to_wav and verify exception
            with pytest.raises(Exception) as exc_info:
                await convert_ogg_to_wav(temp_ogg_path, temp_wav_path)

            assert str(exc_info.value) == "FFmpeg error"
    finally:
        # Clean up temporary files
        os.unlink(temp_ogg_path)
        os.unlink(temp_wav_path)
