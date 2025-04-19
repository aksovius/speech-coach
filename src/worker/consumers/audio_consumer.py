from messaging.broker import broker
from services import audio_processing, upload_service


@broker.subscriber(stream="audio_stream")
async def handle_task(data: dict):
    print("Получена задача:", data)
    print(">>>>> Получена задача:", data, flush=True)
    print("🔥 ПРИШЛО СООБЩЕНИЕ:", data, type(data), flush=True)
    downloaded_file = data.get("file_path")
    converted_file = await audio_processing.convert_ogg_to_wav(downloaded_file)
    if not converted_file:
        data["error"] = "Failed to convert the audio file."
        await broker.publish(data, stream="audio_response_stream")
        return

    uploaded_file = await upload_service.upload_file(downloaded_file)
    data["converted_file"] = converted_file
    data["uploaded_file"] = uploaded_file
    await broker.publish(data, stream="audio_response_stream")
