from gpt.client import client

async def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create( # type: ignore
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"],
                language="en",
                temperature=0.0,
                prompt=None,
                initial_prompt=None
            )
        return response.text
    except Exception as e:
        print(f"❌ Ошибка распознавания речи: {e}")
        return "Ошибка распознавания речи."
