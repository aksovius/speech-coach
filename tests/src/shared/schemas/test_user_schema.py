"""Tests for user_schema.py module."""

import pytest
from pydantic import ValidationError

from shared.schemas.user_schema import UserCreate


def test_user_create_valid():
    """Test valid UserCreate model creation."""
    # Test data
    data = {
        "telegram_id": 123456789,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
    }

    # Create model instance
    user = UserCreate(**data)

    # Verify fields
    assert user.telegram_id == data["telegram_id"]
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.username == data["username"]


def test_user_create_minimal():
    """Test UserCreate model creation with minimal data."""
    # Test data with only required field and None for optional fields
    data = {
        "telegram_id": 123456789,
        "first_name": None,
        "last_name": None,
        "username": None,
    }

    # Create model instance
    user = UserCreate(**data)

    # Verify fields
    assert user.telegram_id == data["telegram_id"]
    assert user.first_name is None
    assert user.last_name is None
    assert user.username is None


def test_user_create_invalid_telegram_id():
    """Test UserCreate model with invalid telegram_id."""
    # Test data with invalid telegram_id
    data = {
        "telegram_id": "not_a_number",  # Invalid telegram_id
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
    }

    # Verify validation error
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_create_from_attributes():
    """Test UserCreate model creation from attributes."""

    # Test data
    class MockUser:
        telegram_id = 123456789
        first_name = "John"
        last_name = "Doe"
        username = "johndoe"

    # Create model instance from attributes
    user = UserCreate.model_validate(MockUser())

    # Verify fields
    assert user.telegram_id == MockUser.telegram_id
    assert user.first_name == MockUser.first_name
    assert user.last_name == MockUser.last_name
    assert user.username == MockUser.username


def test_user_create_json_schema():
    """Test UserCreate model JSON schema."""
    # Get JSON schema
    schema = UserCreate.model_json_schema()

    # Verify schema properties
    assert "example" in schema
    assert schema["example"]["telegram_id"] == 123456789
    assert schema["example"]["first_name"] == "John"
    assert schema["example"]["last_name"] == "Doe"
    assert schema["example"]["username"] == "johndoe"
