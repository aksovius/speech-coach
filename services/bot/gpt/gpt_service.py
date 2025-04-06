from .client import client
from .prompts import TOEFL_TASK1_PROMPT, TOEFL_EXAMINER_PROMPT

async def generate_question():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": TOEFL_TASK1_PROMPT},
                {"role": "user", "content": "Generate a question for TOEFL Task 1."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating question: {e}")
        return "Error generating question."

async def evaluate_answer(question: str, answer: str) -> str:
    try:
        response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": TOEFL_EXAMINER_PROMPT},
                    {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}
                ]
            )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return answer
