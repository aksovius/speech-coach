"""Tests for question_manager.py module."""

import json
from unittest.mock import patch

import pytest

from server.models.schema import Question
from shared.schemas.question_schema import QuestionResponse
from shared.services import question_manager


@pytest.fixture
def mock_redis():
    """Fixture to mock Redis client."""
    with patch("shared.services.question_manager.redis_cache") as mock:
        yield mock


def test_set_user_question(mock_redis):
    """Test setting a question for a user."""
    # Test data
    user_id = 1
    question = Question(id=1, text="Test question", category="general")

    # Call the tested method
    question_manager.set_user_question(user_id, question)

    # Verify Redis was called with correct data
    mock_redis.set.assert_called_once()
    call_args = mock_redis.set.call_args[0]
    assert call_args[0] == f"user_question:{user_id}"
    stored_data = json.loads(call_args[1])
    assert stored_data["id"] == question.id
    assert stored_data["text"] == question.text


def test_get_user_question_existing(mock_redis):
    """Test getting an existing question for a user."""
    # Test data
    user_id = 1
    question_data = {"id": 1, "text": "Test question", "category": "general"}

    # Mock Redis get response
    mock_redis.get.return_value = json.dumps(question_data)

    # Call the tested method
    result = question_manager.get_user_question(user_id)

    # Verify Redis was called and correct data was returned
    mock_redis.get.assert_called_once_with(f"user_question:{user_id}")
    assert isinstance(result, QuestionResponse)
    assert result.id == question_data["id"]
    assert result.text == question_data["text"]


def test_get_user_question_nonexistent(mock_redis):
    """Test getting a question for a non-existent user."""
    # Test data
    user_id = 999  # Non-existent user

    # Mock Redis get response
    mock_redis.get.return_value = None

    # Call the tested method
    result = question_manager.get_user_question(user_id)

    # Verify Redis was called and None was returned
    mock_redis.get.assert_called_once_with(f"user_question:{user_id}")
    assert result is None


def test_set_user_question_overwrite(mock_redis):
    """Test overwriting an existing question for a user."""
    # Test data
    user_id = 1
    old_question = Question(id=1, text="Old question", category="general")
    new_question = Question(id=2, text="New question", category="general")

    # Call the tested method twice
    question_manager.set_user_question(user_id, old_question)
    question_manager.set_user_question(user_id, new_question)

    # Verify Redis was called twice with correct data
    assert mock_redis.set.call_count == 2
    last_call_args = mock_redis.set.call_args[0]
    stored_data = json.loads(last_call_args[1])
    assert stored_data["id"] == new_question.id
    assert stored_data["text"] == new_question.text
