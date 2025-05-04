import asyncio
import os
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from server.models.schema import Base, Question


async def load_questions(file_path: str):
    """
    Load questions from a text file into the database.

    File format:
    category: Category name
    text: Question text
    correct_answer: Correct answer text (optional)
    ---
    """
    # Create database engine
    engine = create_async_engine(os.environ.get("DATABASE_URL"))

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Read and parse questions file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Total content length: {len(content)}")

    # Split into individual questions and add a separator at the end
    questions_raw = [q.strip() for q in content.split("\n\n") if q.strip()]
    print(f"Found {len(questions_raw)} questions")

    async with async_session() as session:
        for i, question_raw in enumerate(questions_raw, 1):
            print(f"\nProcessing question {i}:")
            print("-" * 50)
            print(question_raw)
            print("-" * 50)

            if not question_raw.strip():
                continue

            # Parse question data
            question_data = {}
            for line in question_raw.strip().split("\n"):
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                question_data[key.strip()] = value.strip()

            print(f"Parsed data: {question_data}")

            # Create question object
            question = Question(
                category=question_data.get("category", "general"),
                text=question_data["text"],
                correct_answer=question_data.get("correct_answer", None),
            )

            # Add to session
            session.add(question)

        # Commit all questions
        await session.commit()

    print(f"Successfully loaded questions from {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_questions.py <questions_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)

    asyncio.run(load_questions(file_path))
