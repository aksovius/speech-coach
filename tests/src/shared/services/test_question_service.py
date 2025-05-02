"""Tests for question_service.py module."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from server.crud import question_crud
from shared.services import question_service


@pytest.mark.asyncio
async def test_get_question_for_user_success():
    """Test successful retrieval of question for user."""
    # Test data
    user_id = 1
    mock_question = {"id": 1, "text": "Test question"}
    db_session = AsyncMock(spec=AsyncSession)

    # Mock question_crud.get_unseen_questions
    with patch.object(
        question_crud, "get_unseen_questions", new_callable=AsyncMock
    ) as mock_get_questions:
        # Setup mock return value
        mock_get_questions.return_value = mock_question

        # Call the tested method
        result = await question_service.get_question_for_user(user_id, db_session)

        # Verify results
        assert result == mock_question
        mock_get_questions.assert_called_once_with(user_id, db_session)


@pytest.mark.asyncio
async def test_get_question_for_user_no_questions():
    """Test when no questions are available for user."""
    # Test data
    user_id = 1
    db_session = AsyncMock(spec=AsyncSession)

    # Mock question_crud.get_unseen_questions
    with patch.object(
        question_crud, "get_unseen_questions", new_callable=AsyncMock
    ) as mock_get_questions:
        # Setup mock return value
        mock_get_questions.return_value = None

        # Call the tested method
        result = await question_service.get_question_for_user(user_id, db_session)

        # Verify results
        assert result is None
        mock_get_questions.assert_called_once_with(user_id, db_session)


@pytest.mark.asyncio
async def test_get_question_for_user_exception():
    """Test error handling when getting questions."""
    # Test data
    user_id = 1
    db_session = AsyncMock(spec=AsyncSession)

    # Mock question_crud.get_unseen_questions
    with patch.object(
        question_crud, "get_unseen_questions", new_callable=AsyncMock
    ) as mock_get_questions:
        # Setup mock to raise exception
        mock_get_questions.side_effect = Exception("Database error")

        # Call the tested method and expect exception
        with pytest.raises(Exception) as exc_info:
            await question_service.get_question_for_user(user_id, db_session)

        # Verify exception
        assert str(exc_info.value) == "Database error"
        mock_get_questions.assert_called_once_with(user_id, db_session)
