from typing import Optional

from pydantic import BaseModel, Field


class AudioTaskProcessing(BaseModel):
    telegram_id: int
    user_id: int
    file_path: str
    question_category: str = Field(default="general")


class AudioTaskResult(BaseModel):
    telegram_id: int
    user_id: int
    converted_file: str
    uploaded_file: str
    error: Optional[str] = None
