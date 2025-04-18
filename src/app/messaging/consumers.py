from app.messaging.broker import broker

@broker.subscriber("tasks")
async def handle_task(data: dict):
    print("Получена задача:", data)
    # здесь вызываешь логику, например services.question_service.process(data)
