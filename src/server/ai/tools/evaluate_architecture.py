from typing import List

from pydantic import BaseModel, Field


class ArchitectureEvaluation(BaseModel):
    recommended_answer: str = Field(default="")
    content_score: float = Field(default=0.0)
    language_score: float = Field(default=0.0)
    total_score: float = Field(default=0.0)
    feedback: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


tools = [
    {
        "type": "function",
        "function": {
            "name": "evaluate_architecture_response",
            "description": "Evaluate a response to an architecture question",
            "parameters": {
                "type": "object",
                "properties": {
                    "recommended_answer": {
                        "type": "string",
                        "description": "A concise recommended answer that would score 90+ (max 120 words)",
                    },
                    "content_score": {
                        "type": "number",
                        "description": "Score for content correctness & completeness (0-50)",
                    },
                    "language_score": {
                        "type": "number",
                        "description": "Score for language quality (0-50)",
                    },
                    "total_score": {
                        "type": "number",
                        "description": "Total score (content_score + language_score)",
                    },
                    "feedback": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Actionable feedback (max 3 bullets)",
                    },
                    "strengths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of key strengths in the response",
                    },
                    "weaknesses": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of key weaknesses in the response",
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of specific suggestions for improvement",
                    },
                },
                "required": [
                    "recommended_answer",
                    "content_score",
                    "language_score",
                    "total_score",
                ],
            },
        },
    }
]
