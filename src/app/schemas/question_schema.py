from typing import Optional

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


class QuestionResponse(BaseModel):
    id: int
    category: str
    text: str

    class Config:
        from_attributes = True
