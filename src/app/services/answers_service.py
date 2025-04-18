from crud import user_answers_crud
from models.schema import UserAnswer


async def save_answer(answer: UserAnswer, db) -> None:
    await user_answers_crud.save_answer(answer, db)
