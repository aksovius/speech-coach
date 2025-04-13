
async def transcribe_audio(audio_path):
    print(f"🔊Start audio transcribe : {audio_path}")
    try:
        with open(audio_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create( # type: ignore
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"],
                language="en",
                temperature=0.0,
                prompt=None
            )
        return response.text
    except Exception as e:
        print(f"❌ audio transcribe error: {e}")
        return "Audio transcribe error"
