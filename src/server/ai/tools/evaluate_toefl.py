tools = [
    {
        "type": "function",
        "function": {
            "name": "evaluate_toefl_response",
            "description": "Evaluate a TOEFL Speaking answer and return score, feedback, and example.",
            "parameters": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "integer",
                        "description": "TOEFL Speaking score from 0 to 4",
                    },
                    "feedback": {
                        "type": "string",
                        "description": "2–4 sentence evaluation of the answer",
                    },
                    "example_answer": {
                        "type": "string",
                        "description": "Sample answer that would receive a score of 4 (under 45 seconds)",
                    },
                },
                "required": ["score", "feedback", "example_answer"],
            },
        },
    }
]
