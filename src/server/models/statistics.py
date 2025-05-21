from datetime import datetime

from pydantic import BaseModel, Field


class SessionStatistics(BaseModel):
    """Model for overall session statistics"""

    total_sessions: int = Field(description="Total number of sessions")
    avg_ttr: float = Field(description="Average time to response")
    avg_score: float = Field(description="Average overall score")
    first_session: datetime = Field(description="Date of first session")
    last_session: datetime = Field(description="Date of last session")


class DailyStatistics(BaseModel):
    """Model for daily statistics"""

    date: datetime = Field(description="Date")
    avg_ttr: float = Field(description="Average time to response")
    avg_score: float = Field(description="Average overall score")
    attempts: int = Field(description="Number of attempts")


class WordCloudItem(BaseModel):
    """Model for word cloud item"""

    text: str = Field(description="Word")
    value: int = Field(description="Number of occurrences")
