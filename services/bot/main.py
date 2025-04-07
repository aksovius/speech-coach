import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from pydub import AudioSegment
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.types import BotCommand
user_questions = {}
from gpt.prompts import *




import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import TELEGRAM_BOT_TOKEN
from handlers import start, question  # импорт других хэндлеров

async def main():
    session = AiohttpSession()
    bot = Bot(token=TELEGRAM_BOT_TOKEN, session=session, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(question.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



# # 🚀 Запуск бота
# async def main():
#     print("🤖 Бот запущен и слушает сообщения...")
#     await bot.delete_webhook(drop_pending_updates=True)
#     await set_bot_commands(bot)
#     await dp.start_polling(bot)


# # Initialize bot
# session = AiohttpSession()
# bot = Bot(
#     token=TELEGRAM_BOT_TOKEN,
#     session=session,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
# dp = Dispatcher()
# print("🤖 Бот инициализирован")

# async def set_bot_commands(bot: Bot):
#     commands = [
#         BotCommand(command="start", description="Начать работу с ботом"),
#         BotCommand(command="help", description="Помощь и описание бота"),
#         BotCommand(command="question", description="Дать задание"),
#         # Добавь свои команды здесь
#         # BotCommand(command="question", description="Получить задание"),
#     ]
#     await bot.set_my_commands(commands)
# # 📌 Конвертация аудио


# # 🎙 Распознавание речи


# # 📝 Коррекция текста (GPT-4)
# # async def correct_text(text):
# #     try:
# #         response = client.chat.completions.create(
# #             model="gpt-4",
# #             messages=[
# #                 {"role": "system", "content": "You are an English teacher correcting grammar."},
# #                 {"role": "user", "content": text}
# #             ]
# #         )
# #         return response.choices[0].message.content
# #     except Exception as e:
# #         print(f"❌ Ошибка GPT-4: {e}")
# #         return text  # Если ошибка, просто возвращаем оригинальный текст


# # 🔊 Текст в речь


# # 🤖 Обработка голосовых сообщений
# @dp.message(F.voice)
# async def handle_voice(message: Message):
#     user_id = message.from_user.id

#     if user_id not in user_questions:
#         await message.answer("🤖 Сначала попроси вопрос с помощью команды /question.")
#         return

#     question = user_questions[user_id]  # получаем активный вопрос
#     try:
#         print("📥 Голосовое сообщение получено")
#         await message.answer("🤖 Обрабатываю ваше голосовое сообщение...")
#         file_info = await bot.get_file(message.voice.file_id)
#         file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

#         # Скачиваем файл
#         async with aiohttp.ClientSession() as session:
#             async with session.get(file_url) as resp:
#                 with open("voice.ogg", "wb") as f:
#                     f.write(await resp.read())
#         await message.answer("✅ Голосовое сообщение скачано")
#         print("✅ Голосовое сообщение скачано")

#         # Конвертируем в WAV
#         wav_file = await convert_ogg_to_wav("voice.ogg")
#         if not wav_file:
#             await message.answer("❌ Ошибка при обработке аудио.")
#             return
#         await message.answer("✅ Голосовое сообщение конвертировано в WAV")
#         # Распознаем текст
#         transcribed_text = await transcribe_audio(wav_file)

#         print(f"📜 User: {transcribed_text}")
#         await message.answer(f"📜 User: {transcribed_text}")
#         response = await evaluate_answer(question, transcribed_text)
#         print(f"📜 Teacher: {response}")
#         await message.answer(f"📜 Teacher: {response}")
#         # Исправляем ошибки
#         # corrected_text = await correct_text(transcribed_text)
#         # print(f"✅ Corrected: {corrected_text}")

#         # speech = await text_for_speech(transcribed_text)
#         # print(f"🔊 Speech: {speech}")
#         # # Генерируем речь
#         # speech_file = await text_to_speech(speech)
#         # if not speech_file:
#         #     await message.answer("❌ Ошибка при генерации речи.")
#         #     return

#         # # Отправляем исправленный голос
#         # await message.answer_voice(FSInputFile(speech_file))

#     except Exception as e:
#         print(f"❌ Ошибка обработки голосового сообщения: {e}")
#         await message.answer("❌ Произошла ошибка при обработке вашего голосового сообщения.")

# @dp.message(Command("start"))
# async def handle_start(message: Message):
#     await message.answer(
#         "👋 Привет! Отправь мне голосовое или текст, и я помогу тебе практиковать английский язык 🎧\n"
#         "Я отвечаю голосом, задаю вопросы и стараюсь говорить просто и понятно — как настоящий учитель! 🧑‍🏫"
#     )


# @dp.message(Command("question"))
# async def send_question(message: Message):
#     user_id = message.from_user.id
#     question = await generate_question()
#     user_questions[user_id] = question  # сохраняем активный вопрос

#     await message.answer(f"❓ Вот вопрос для тебя:\n{question}\n\n💬 Ответь на него, и я помогу тебе с исправлениями!")

# # 🤖 Обработка текстовых сообщений
# @dp.message(F.text)
# async def handle_text(message: Message):
#     try:
#         print(f"📜 User: {message.text}")
#         #corrected_text = await correct_text(message.text)
#         #await message.answer(f"✅ Corrected:\n{corrected_text}")

#         speech = await text_for_speech(message.text)

#         speech_file = await text_to_speech(speech)
#         if not speech_file:
#             await message.answer("❌ Ошибка при генерации речи.")
#             return

#         await message.answer_voice(FSInputFile(speech_file))

#     except Exception as e:
#         print(f"❌ Ошибка обработки текстового сообщения: {e}")
#         await message.answer("❌ Произошла ошибка при обработке вашего текста.")
