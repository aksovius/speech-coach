from server.models.schema import Question
from shared.cache.redis_cache import redis_cache
from shared.schemas.question_schema import QuestionResponse


def set_user_question(user_id: str, question: Question):
    """
    Saves user question to Redis cache.

    Args:
        user_id (str): User ID
        question (Question): Question object
    """
    question_data = QuestionResponse.model_validate(question)
    redis_cache.set(f"user_question:{user_id}", question_data.model_dump_json())


def get_user_question(user_id: str) -> QuestionResponse:
    """
    Retrieves user question from Redis cache.

    Args:
        user_id (str): User ID

    Returns:
        QuestionResponse: Question data or None if not found
    """
    data = redis_cache.get(f"user_question:{user_id}")
    if data:
        return QuestionResponse.model_validate_json(data)
    return None
