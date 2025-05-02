"""Tests for media_service.py module."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.schema import Media
from shared.services.media_service import save_media


@pytest.mark.asyncio
async def test_save_media_success():
    """Test successful media saving."""
    # Test data
    media = Media(
        source_type="user_answer",
        source_id=1,
        media_type="audio",
        url="/path/to/media",
        description="Test media",
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_media function
    with patch(
        "shared.services.media_service.media_crud.save_media", new_callable=AsyncMock
    ) as mock_save:
        # Call save_media
        await save_media(mock_session, media)

        # Verify save_media was called with correct arguments
        mock_save.assert_called_once_with(mock_session, media)


@pytest.mark.asyncio
async def test_save_media_exception():
    """Test error handling when saving media."""
    # Test data
    media = Media(
        source_type="user_answer",
        source_id=1,
        media_type="audio",
        url="/path/to/media",
        description="Test media",
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_media function to raise an exception
    with patch(
        "shared.services.media_service.media_crud.save_media", new_callable=AsyncMock
    ) as mock_save:
        mock_save.side_effect = Exception("Database error")

        # Call save_media and verify exception
        with pytest.raises(Exception) as exc_info:
            await save_media(mock_session, media)

        assert str(exc_info.value) == "Database error"


@pytest.mark.asyncio
async def test_save_media_invalid_data():
    """Test saving media with invalid data."""
    # Test data with missing required field
    media = Media(
        source_type="user_answer",
        source_id=1,
        media_type="audio",
        url="",  # Empty URL
        description="Test media",
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_media function
    with patch(
        "shared.services.media_service.media_crud.save_media", new_callable=AsyncMock
    ) as mock_save:
        # Call save_media
        await save_media(mock_session, media)

        # Verify save_media was called with invalid data
        mock_save.assert_called_once_with(mock_session, media)
