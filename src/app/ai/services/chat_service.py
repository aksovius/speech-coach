from ai.client import client
from ai.prompts import TOEFL_EXAMINER_PROMPT


async def evaluate_answer(question: str, answer: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": TOEFL_EXAMINER_PROMPT},
                {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"},
            ],
        )
        print("Response:", response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return f"Error evaluating answer: {e}"
