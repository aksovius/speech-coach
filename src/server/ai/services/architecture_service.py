import json
import os

from server.ai.client import client
from server.ai.prompts import ARCHITECTURE_PROMPT
from server.ai.tools.evaluate_architecture import ArchitectureEvaluation, tools
from shared.logging import get_log_level, setup_logger

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.ai.architecture",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.ai.architecture",
    use_loki=True,
)


async def evaluate_architecture(question: str, answer: str) -> ArchitectureEvaluation:
    try:
        logger.info(
            "Evaluating architecture answer",
            extra={
                "event": "architecture_evaluation_start",
                "question_length": len(question),
                "answer_length": len(answer),
            },
        )

        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": ARCHITECTURE_PROMPT},
                {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"},
            ],
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "evaluate_architecture_response"},
            },
        )

        logger.debug(
            "Received evaluation response",
            extra={
                "event": "architecture_evaluation_response",
                "model": response.model,
                "usage": dict(response.usage) if hasattr(response, "usage") else {},
            },
        )

        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments
        args = json.loads(args_str)

        logger.info(
            "Architecture evaluation completed successfully",
            extra={"event": "architecture_evaluation_success"},
        )

        return ArchitectureEvaluation(**args)

    except Exception as e:
        logger.error(
            "Error evaluating architecture answer",
            extra={"event": "architecture_evaluation_error", "error": str(e)},
        )
        raise
