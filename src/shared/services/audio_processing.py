from pydub import AudioSegment


async def convert_ogg_to_wav(input_path: str, output_path: str, time_limit: int = 45):
    """Convert OGG file to WAV format with optional time limit.

    Args:
        input_path: Path to input OGG file
        output_path: Path to output WAV file
        time_limit: Maximum duration in seconds (default: 45)

    Returns:
        Path to the converted WAV file or None if conversion failed
    """
    try:
        audio = AudioSegment.from_file(input_path, format="ogg")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")

        # Trim audio if needed
        if time_limit:
            end_time = min(time_limit, 45) * 1000  # Convert to milliseconds
            audio = audio[:end_time]
            print(f"Trimmed duration: {len(audio) / 1000:.2f} seconds")

        # Export to WAV
        audio.export(
            output_path,
            format="wav",
            parameters=["-ar", "16000", "-ac", "1", "-sample_fmt", "s16"],
        )
        return output_path
    except Exception as e:
        print(f"Error converting file: {e}")
        raise
