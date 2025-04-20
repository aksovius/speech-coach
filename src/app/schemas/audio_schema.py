from typing import Optional

from pydantic import BaseModel


class AudioTaskProcessing(BaseModel):
    telegram_id: int
    user_id: int
    file_path: str


class AudioTaskResult(BaseModel):
    telegram_id: int
    user_id: int
    converted_file: str
    uploaded_file: str
    error: Optional[str] = None
