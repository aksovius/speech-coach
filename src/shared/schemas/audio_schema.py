from typing import Optional

from pydantic import BaseModel, Field


class AudioTaskProcessing(BaseModel):
    telegram_id: int
    user_id: int
    file_path: str
    question_category: str = Field(default="general")


class AudioTask(BaseModel):
    telegram_id: int
    file_id: str
    file_unique_id: str
    user_id: Optional[int] = None


class AudioTaskResult(BaseModel):
    telegram_id: int
    user_id: Optional[int] = None
    converted_file: Optional[str] = None
    uploaded_file: Optional[str] = None
    error: Optional[str] = None
    question_category: Optional[str] = "architecture"
