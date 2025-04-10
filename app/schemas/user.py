from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "telegram_id": 123456789,
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe"
            }
        }