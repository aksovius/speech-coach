"""Tests for question_schema.py module."""

import pytest
from pydantic import ValidationError
from shared.schemas.question_schema import QuestionRequest, QuestionResponse


def test_question_request_valid():
    """Test valid QuestionRequest model creation."""
    # Test data
    data = {
        "telegram_id": 123456,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
    }

    # Create model instance
    request = QuestionRequest(**data)

    # Verify fields
    assert request.telegram_id == data["telegram_id"]
    assert request.first_name == data["first_name"]
    assert request.last_name == data["last_name"]
    assert request.username == data["username"]


def test_question_request_minimal():
    """Test QuestionRequest model creation with minimal data."""
    # Test data with only required field and None for optional fields
    data = {
        "telegram_id": 123456,
        "first_name": None,
        "last_name": None,
        "username": None,
    }

    # Create model instance
    request = QuestionRequest(**data)

    # Verify fields
    assert request.telegram_id == data["telegram_id"]
    assert request.first_name is None
    assert request.last_name is None
    assert request.username is None


def test_question_response_valid():
    """Test valid QuestionResponse model creation."""
    # Test data
    data = {"id": 1, "category": "Speaking", "text": "Describe your favorite place"}

    # Create model instance
    response = QuestionResponse(**data)

    # Verify fields
    assert response.id == data["id"]
    assert response.category == data["category"]
    assert response.text == data["text"]


def test_question_response_invalid():
    """Test invalid QuestionResponse model creation."""
    # Test data with missing required field
    data = {
        "id": 1,
        "category": "Speaking",
        # Missing text field
    }

    # Verify validation error
    with pytest.raises(ValidationError):
        QuestionResponse(**data)


def test_question_response_from_attributes():
    """Test QuestionResponse model creation from attributes."""

    # Test data
    class MockQuestion:
        id = 1
        category = "Speaking"
        text = "Describe your favorite place"

    # Create model instance from attributes
    response = QuestionResponse.model_validate(MockQuestion())

    # Verify fields
    assert response.id == MockQuestion.id
    assert response.category == MockQuestion.category
    assert response.text == MockQuestion.text
