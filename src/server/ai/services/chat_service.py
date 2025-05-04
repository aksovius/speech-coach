import json
import os

from server.ai.client import client
from server.ai.prompts import TOEFL_TOOL_PROMPT
from server.ai.tools.evaluate_toefl import tools
from shared.logging import get_log_level, setup_logger
from shared.schemas.toefl_schema import TOEFLResult

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.ai.chat",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.ai.chat",
    use_loki=True,
)


async def evaluate_answer(question: str, answer: str) -> TOEFLResult:
    try:
        logger.info(
            "Evaluating answer",
            extra={
                "event": "evaluation_start",
                "question_length": len(question),
                "answer_length": len(answer),
            },
        )
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": TOEFL_TOOL_PROMPT},
                {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"},
            ],
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "evaluate_toefl_response"},
            },
        )
        logger.debug(
            "Received evaluation response",
            extra={
                "event": "evaluation_response",
                "model": response.model,
                "usage": dict(response.usage) if hasattr(response, "usage") else {},
            },
        )
        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments
        args = json.loads(args_str)

        logger.info(
            "Evaluation completed successfully",
            extra={"event": "evaluation_success", "result_type": "TOEFLResult"},
        )
        return TOEFLResult(**args)
    except Exception as e:
        logger.error(
            "Error evaluating answer",
            extra={"event": "evaluation_error", "error": str(e)},
        )
        return f"Error evaluating answer: {e}"
