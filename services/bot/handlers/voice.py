from aiogram import Router, F
from aiogram.types import Message
from bot.services.question_manager import get_user_question
from bot.audio.convert import convert_ogg_to_wav
from bot.whisper.transcribe import transcribe_audio
from bot.gpt.gpt_service import evaluate_answer

import aiohttp
from bot.config import TELEGRAM_BOT_TOKEN

router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):
    user_id = message.from_user.id
    question = get_user_question(user_id)
    if not question:
        await message.answer("🤖 Сначала попроси вопрос с помощью команды /question.")
        return

    try:
        print("📥 Голосовое сообщение получено")
        await message.answer("🤖 Обрабатываю ваше голосовое сообщение...")
        file_info = await message.bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

        # Скачиваем файл
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                with open("voice.ogg", "wb") as f:
                    f.write(await resp.read())
        await message.answer("✅ Голосовое сообщение скачано")
        print("✅ Голосовое сообщение скачано")

        # Конвертируем в WAV
        wav_file = await convert_ogg_to_wav("voice.ogg")
        if not wav_file:
            await message.answer("❌ Ошибка при обработке аудио.")
            return
        await message.answer("✅ Голосовое сообщение конвертировано в WAV")
        # Распознаем текст
        transcribed_text = await transcribe_audio(wav_file)

        print(f"📜 User: {transcribed_text}")
        await message.answer(f"📜 User: {transcribed_text}")
        response = await evaluate_answer(question, transcribed_text)
        print(f"📜 Teacher: {response}")
        await message.answer(f"📜 Teacher: {response}")
        # Исправляем ошибки
        # corrected_text = await correct_text(transcribed_text)
        # print(f"✅ Corrected: {corrected_text}")

        # speech = await text_for_speech(transcribed_text)
        # print(f"🔊 Speech: {speech}")
        # # Генерируем речь
        # speech_file = await text_to_speech(speech)
        # if not speech_file:
        #     await message.answer("❌ Ошибка при генерации речи.")
        #     return

        # # Отправляем исправленный голос
        # await message.answer_voice(FSInputFile(speech_file))
    except Exception as e:
        print(f"❌ Ошибка обработки голосового сообщения: {e}")
        await message.answer("❌ Произошла ошибка при обработке вашего голосового сообщения.")
