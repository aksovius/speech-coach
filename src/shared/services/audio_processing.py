from pydub import AudioSegment


async def convert_ogg_to_wav(file_path, time_end: int = 45):
    end_time = min(time_end, 45) * 1000  # Ensure end_time does not exceed 45 seconds
    try:
        audio = AudioSegment.from_file(file_path, format="ogg")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")
        trimmed_audio = audio[:end_time]  # Convert seconds to milliseconds
        print(f"Trimmed duration: {len(trimmed_audio) / 1000:.2f} seconds")
        wav_path = file_path.replace(".ogg", ".wav")
        trimmed_audio.export(
            wav_path,
            format="wav",
            parameters=["-ar", "16000", "-ac", "1", "-sample_fmt", "s16"],
        )
        return wav_path
    except Exception as e:
        print(f"Error converting file: {e}")
        return None
