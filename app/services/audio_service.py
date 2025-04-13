from typing import Optional

import aiohttp
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

async def download_audio(file_url: str, file_path: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status != 200:
                    print(f"Failed to download file. Status: {resp.status}")
                    return None

                with open(file_path, "wb") as f:
                    f.write(await resp.read())
        return file_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

async def process_voice_message(file_url: str) -> Optional[str]:
    ogg_path = "temp_audio.ogg"
    wav_path = "temp_audio.wav"

    # Download the audio file
    downloaded_file = await download_audio(file_url, ogg_path)
    if not downloaded_file:
        return None

    # Convert OGG to WAV
    converted_file = await convert_ogg_to_wav(downloaded_file)
    if not converted_file:
        return None

    return converted_file