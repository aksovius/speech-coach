from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

class QuestionResponce(BaseModel):
    id: int
    category: str
    text: str

    class Config:
        orm_mode = True