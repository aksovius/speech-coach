"""Tests for audio_processing.py module."""

import os
from pathlib import Path

import pytest
from pydub import AudioSegment

from shared.services.audio_processing import convert_ogg_to_mp3, process_audio


@pytest.mark.asyncio
async def test_convert_ogg_to_mp3_success():
    """Test successful conversion of OGG to MP3."""
    # Create temporary test files
    temp_ogg_path = "test.ogg"
    temp_mp3_path = "test.mp3"

    # Create a test OGG file
    audio = AudioSegment.silent(duration=1000)  # 1 second of silence
    audio.export(temp_ogg_path, format="ogg")

    try:
        # Call convert_ogg_to_mp3
        result = await convert_ogg_to_mp3(temp_ogg_path, temp_mp3_path)

        # Verify the result
        assert result == temp_mp3_path
        assert Path(temp_mp3_path).exists()

        # Verify the converted file
        converted_audio = AudioSegment.from_file(temp_mp3_path, format="mp3")
        assert len(converted_audio) > 0

    finally:
        # Clean up
        Path(temp_ogg_path).unlink(missing_ok=True)
        Path(temp_mp3_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_convert_ogg_to_mp3_with_time_limit():
    """Test conversion with time limit."""
    # Create temporary test files
    temp_ogg_path = "test.ogg"
    temp_mp3_path = "test.mp3"

    # Create a test OGG file
    audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
    audio.export(temp_ogg_path, format="ogg")

    try:
        # Call process_audio with time limit
        result = await process_audio(
            temp_ogg_path, temp_mp3_path, time_limit=2, speed_factor=1.0
        )

        # Verify the result
        assert result == temp_mp3_path
        assert os.path.exists(temp_mp3_path)

        # Check if the file was trimmed correctly
        processed_audio = AudioSegment.from_mp3(temp_mp3_path)
        assert len(processed_audio) <= 2000  # Should be less than 2 seconds

    finally:
        # Cleanup
        if os.path.exists(temp_ogg_path):
            os.remove(temp_ogg_path)
        if os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)


@pytest.mark.asyncio
async def test_convert_ogg_to_mp3_exception():
    """Test handling of non-existent file."""
    # Create temporary test files
    temp_ogg_path = "nonexistent.ogg"
    temp_mp3_path = "test.mp3"

    try:
        # Call convert_ogg_to_mp3 and verify exception
        with pytest.raises(Exception):
            await convert_ogg_to_mp3(temp_ogg_path, temp_mp3_path)

    finally:
        # Clean up
        Path(temp_mp3_path).unlink(missing_ok=True)
