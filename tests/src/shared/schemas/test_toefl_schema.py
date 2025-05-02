"""Tests for toefl_schema.py module."""

import pytest
from pydantic import ValidationError
from shared.schemas.toefl_schema import TOEFLResult


def test_toefl_result_valid():
    """Test valid TOEFLResult model creation."""
    # Test data
    data = {
        "score": 3,
        "feedback": "Good pronunciation and grammar",
        "example_answer": "This is an example answer",
    }

    # Create model instance
    result = TOEFLResult(**data)

    # Verify fields
    assert result.score == data["score"]
    assert result.feedback == data["feedback"]
    assert result.example_answer == data["example_answer"]


def test_toefl_result_min_score():
    """Test TOEFLResult model with minimum score."""
    # Test data with minimum score
    data = {"score": 0, "feedback": "Needs improvement", "example_answer": "Example"}

    # Create model instance
    result = TOEFLResult(**data)

    # Verify score
    assert result.score == 0


def test_toefl_result_max_score():
    """Test TOEFLResult model with maximum score."""
    # Test data with maximum score
    data = {
        "score": 4,
        "feedback": "Excellent performance",
        "example_answer": "Example",
    }

    # Create model instance
    result = TOEFLResult(**data)

    # Verify score
    assert result.score == 4


def test_toefl_result_invalid_score():
    """Test TOEFLResult model with invalid score."""
    # Test data with invalid score
    data = {
        "score": 5,  # Score above maximum
        "feedback": "Invalid score",
        "example_answer": "Example",
    }

    # Verify validation error
    with pytest.raises(ValidationError):
        TOEFLResult(**data)


def test_toefl_result_negative_score():
    """Test TOEFLResult model with negative score."""
    # Test data with negative score
    data = {
        "score": -1,  # Negative score
        "feedback": "Invalid score",
        "example_answer": "Example",
    }

    # Verify validation error
    with pytest.raises(ValidationError):
        TOEFLResult(**data)
