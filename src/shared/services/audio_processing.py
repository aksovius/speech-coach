from pydub import AudioSegment


def trim_audio(audio: AudioSegment, time_limit: int = 45) -> AudioSegment:
    """Trim audio to specified time limit.

    Args:
        audio: AudioSegment to trim
        time_limit: Maximum duration in seconds (default: 45)

    Returns:
        Trimmed AudioSegment
    """
    if time_limit:
        end_time = min(time_limit, 45) * 1000  # Convert to milliseconds
        audio = audio[:end_time]
        print(f"Trimmed duration: {len(audio) / 1000:.2f} seconds")
    return audio


def change_speed(audio: AudioSegment, speed_factor: float = 2.0) -> AudioSegment:
    """Change audio playback speed.

    Args:
        audio: AudioSegment to process
        speed_factor: Speed multiplier (default: 2.0)

    Returns:
        Processed AudioSegment
    """
    if speed_factor == 1.0:
        return audio
    return audio.speedup(playback_speed=speed_factor)


async def convert_ogg_to_mp3(
    input_path: str, output_path: str = None, bitrate: str = "320k"
) -> str:
    """Convert OGG file to MP3 format.

    Args:
        input_path: Path to input OGG file
        output_path: Path to output MP3 file (default: replaces .ogg with .mp3)
        bitrate: MP3 bitrate (default: "320k")

    Returns:
        Path to the converted MP3 file
    """
    try:
        if output_path is None:
            output_path = input_path.replace(".ogg", ".mp3")

        audio = AudioSegment.from_file(input_path, format="ogg")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")

        # Export to MP3 with high quality settings
        audio.export(
            output_path,
            format="mp3",
            bitrate=bitrate,
            parameters=[
                "-q:a",
                "0",  # Highest quality
                "-ar",
                "44100",  # Sample rate
                "-ac",
                "2",  # Stereo
            ],
        )
        return output_path
    except Exception as e:
        print(f"Error converting file: {e}")
        raise


async def process_audio(
    input_path: str,
    output_path: str = None,
    time_limit: int = 45,
    speed_factor: float = 2.0,
    bitrate: str = "320k",
) -> str:
    """Process audio file: convert, trim and change speed.

    Args:
        input_path: Path to input OGG file
        output_path: Path to output MP3 file (default: replaces .ogg with .mp3)
        time_limit: Maximum duration in seconds (default: 45)
        speed_factor: Speed multiplier (default: 2.0)
        bitrate: MP3 bitrate (default: "320k")

    Returns:
        Path to the processed MP3 file
    """
    try:
        if output_path is None:
            output_path = input_path.replace(".ogg", ".mp3")

        # Load audio
        audio = AudioSegment.from_file(input_path, format="ogg")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")

        # Process audio
        audio = trim_audio(audio, time_limit)
        audio = change_speed(audio, speed_factor)

        # Export to MP3 with high quality settings
        audio.export(
            output_path,
            format="mp3",
            bitrate=bitrate,
            parameters=[
                "-q:a",
                "0",  # Highest quality
                "-ar",
                "44100",  # Sample rate
                "-ac",
                "2",  # Stereo
            ],
        )
        return output_path
    except Exception as e:
        print(f"Error processing file: {e}")
        raise
