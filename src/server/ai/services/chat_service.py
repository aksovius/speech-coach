import json

from server.ai.client import client
from server.ai.prompts import TOEFL_TOOL_PROMPT
from server.ai.tools.evaluate_toefl import tools
from shared.schemas.toefl_schema import TOEFLResult


async def evaluate_answer(question: str, answer: str) -> TOEFLResult:
    try:
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
        print("Response:", response)
        tool_call = response.choices[0].message.tool_calls[0]
        args_str = tool_call.function.arguments
        args = json.loads(args_str)
        return TOEFLResult(**args)
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return f"Error evaluating answer: {e}"
