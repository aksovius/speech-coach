from openai import AsyncOpenAI
from shared.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
