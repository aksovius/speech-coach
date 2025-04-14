from typing import Dict
from services import download_service
from services import audio_processing
from ai.services.audio_service import transcribe_audio
from ai.services.chat_service import evaluate_answer
from services import question_manager

async def process_voice_message(file_url: str, question: str) -> Dict[str, str]:
    ogg_path = "temp_audio.ogg"
    # Download the audio file
    downloaded_file = await download_service.download_file(file_url, ogg_path)
    if not downloaded_file:
        return {"error": "Failed to download the audio file."}

    # Convert OGG to WAV
    converted_file = await audio_processing.convert_ogg_to_wav(downloaded_file)
    if not converted_file:
        return {"error": "Failed to convert the audio file."}

    transcription = await transcribe_audio(converted_file)

    if not transcription:
        return {"error": "Failed to transcribe the audio file."}
    answer = await evaluate_answer(question,transcription)
    print(f"Transcription: {transcription}")
    print(f"Answer: {answer}")
    if not answer:
        return {"error": "Failed to evaluate the answer."}
    return {"transcription": transcription, "answer": answer}