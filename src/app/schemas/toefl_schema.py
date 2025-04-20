from pydantic import BaseModel, Field


class TOEFLResult(BaseModel):
    score: int = Field(..., ge=0, le=4)
    feedback: str
    example_answer: str
