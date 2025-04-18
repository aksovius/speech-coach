from pydub import AudioSegment


async def convert_ogg_to_wav(file_path):
    try:
        audio = AudioSegment.from_file(file_path, format="ogg")
        wav_path = file_path.replace(".ogg", ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting file: {e}")
        return None
