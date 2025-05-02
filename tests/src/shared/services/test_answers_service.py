"""Tests for answers_service.py module."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.schema import UserAnswer
from shared.services.answers_service import save_answer


@pytest.mark.asyncio
async def test_save_answer_success():
    """Test successful answer saving."""
    # Test data
    answer = UserAnswer(
        user_id=1, question_id=1, asr_transcript="Test answer", score_overall=100
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_answer function
    with patch(
        "shared.services.answers_service.user_answers_crud.save_answer",
        new_callable=AsyncMock,
    ) as mock_save:
        # Call save_answer
        await save_answer(mock_session, answer)

        # Verify save_answer was called with correct arguments
        mock_save.assert_called_once_with(mock_session, answer)


@pytest.mark.asyncio
async def test_save_answer_exception():
    """Test error handling when saving answer."""
    # Test data
    answer = UserAnswer(
        user_id=1, question_id=1, asr_transcript="Test answer", score_overall=100
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_answer function to raise an exception
    with patch(
        "shared.services.answers_service.user_answers_crud.save_answer",
        new_callable=AsyncMock,
    ) as mock_save:
        mock_save.side_effect = Exception("Database error")

        # Call save_answer and verify exception
        with pytest.raises(Exception) as exc_info:
            await save_answer(mock_session, answer)

        assert str(exc_info.value) == "Database error"


@pytest.mark.asyncio
async def test_save_answer_invalid_data():
    """Test saving answer with invalid data."""
    # Test data with missing required field
    answer = UserAnswer(
        user_id=1,
        question_id=1,
        asr_transcript="",  # Empty transcript
        score_overall=100,
    )

    # Mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the save_answer function
    with patch(
        "shared.services.answers_service.user_answers_crud.save_answer",
        new_callable=AsyncMock,
    ) as mock_save:
        # Call save_answer
        await save_answer(mock_session, answer)

        # Verify save_answer was called with invalid data
        mock_save.assert_called_once_with(mock_session, answer)
