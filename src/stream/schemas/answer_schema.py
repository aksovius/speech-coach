from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    id: int
    user_id: Optional[int]
    asr_transcript: Optional[str]
    gpt_feedback: Optional[str]
    score_overall: Optional[int]
    created_at: Optional[int]
