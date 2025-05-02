"""Tests for question_manager.py module."""

from shared.services import question_manager


def test_set_user_question():
    """Test setting a question for a user."""
    # Test data
    user_id = 1
    question = {"id": 1, "text": "Test question"}

    # Call the tested method
    question_manager.set_user_question(user_id, question)

    # Verify the question was set
    assert question_manager.user_questions[user_id] == question


def test_get_user_question_existing():
    """Test getting an existing question for a user."""
    # Test data
    user_id = 1
    question = {"id": 1, "text": "Test question"}

    # Set up test data
    question_manager.user_questions[user_id] = question

    # Call the tested method
    result = question_manager.get_user_question(user_id)

    # Verify the correct question was returned
    assert result == question


def test_get_user_question_nonexistent():
    """Test getting a question for a non-existent user."""
    # Test data
    user_id = 999  # Non-existent user

    # Call the tested method
    result = question_manager.get_user_question(user_id)

    # Verify None was returned
    assert result is None


def test_set_user_question_overwrite():
    """Test overwriting an existing question for a user."""
    # Test data
    user_id = 1
    old_question = {"id": 1, "text": "Old question"}
    new_question = {"id": 2, "text": "New question"}

    # Set up initial state
    question_manager.user_questions[user_id] = old_question

    # Call the tested method
    question_manager.set_user_question(user_id, new_question)

    # Verify the question was overwritten
    assert question_manager.user_questions[user_id] == new_question


def test_clear_user_questions():
    """Test clearing all user questions."""
    # Test data
    user_id1 = 1
    user_id2 = 2
    question1 = {"id": 1, "text": "Question 1"}
    question2 = {"id": 2, "text": "Question 2"}

    # Set up test data
    question_manager.user_questions[user_id1] = question1
    question_manager.user_questions[user_id2] = question2

    # Clear the dictionary
    question_manager.user_questions.clear()

    # Verify the dictionary is empty
    assert len(question_manager.user_questions) == 0
