from server.crud import user_answers_crud
from server.models.schema import UserAnswer


async def save_answer(answer: UserAnswer, db) -> None:
    return await user_answers_crud.save_answer(answer, db)
