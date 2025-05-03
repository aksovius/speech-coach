"""Mock implementation of audio_processing module for testing."""


async def convert_ogg_to_wav(file_path: str, time_end: int = 45) -> str:
    """Mock implementation of convert_ogg_to_wav function."""
    return file_path.replace(".ogg", ".wav")


async def convert_ogg_to_mp3(file_path: str, time_end: int = 45) -> str:
    """Mock implementation of convert_ogg_to_mp3 function."""
    return file_path.replace(".ogg", ".mp3")
