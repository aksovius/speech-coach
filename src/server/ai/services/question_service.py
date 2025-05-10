import json
import os

from server.ai.client import client
from server.ai.prompts import get_prompt_for_question_type
from server.ai.tools.evaluate_question import QuestionEvaluation, tools
from shared.logging import get_log_level, setup_logger

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.ai.question_evaluation",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.ai.question_evaluation",
    use_loki=True,
)


async def evaluate_question(
    question: str, answer: str, question_category: str
) -> QuestionEvaluation:
    try:
        logger.info(
            f"Evaluating {question_category} answer",
            extra={
                "event": f"{question_category}_evaluation_start",
                "question_length": len(question),
                "answer_length": len(answer),
                "question_type": question_category,
            },
        )

        prompt = get_prompt_for_question_type(question_category)

        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"},
            ],
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "evaluate_question_response"},
            },
        )

        logger.debug(
            "Received evaluation response",
            extra={
                "event": f"{question_category}_evaluation_response",
                "model": response.model,
                "usage": dict(response.usage) if hasattr(response, "usage") else {},
            },
        )

        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments
        args = json.loads(args_str)

        logger.info(
            f"{question_category.capitalize()} evaluation completed successfully",
            extra={"event": f"{question_category}_evaluation_success"},
        )

        return QuestionEvaluation(**args)

    except Exception as e:
        logger.error(
            f"Error evaluating {question_category} answer",
            extra={"event": f"{question_category}_evaluation_error", "error": str(e)},
        )
        raise


# Для обратной совместимости
async def evaluate_architecture(question: str, answer: str) -> QuestionEvaluation:
    return await evaluate_question(question, answer, "architecture")
