from bot.gpt.client import client
from pydub import AudioSegment

async def text_to_speech(text, output_path="output.mp3"):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        temp_mp3 = "temp.mp3"
        with open(temp_mp3, "wb") as f:
            f.write(response.content)

        audio = AudioSegment.from_file(temp_mp3, format="mp3")
        audio.export(output_path, format="ogg", codec="libopus")

        return output_path
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None
