from bot.gpt.client import client

async def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text
    except Exception as e:
        print(f"❌ Ошибка распознавания речи: {e}")
        return "Ошибка распознавания речи."
