import asyncio

from app.messaging.broker import broker

if __name__ == "__main__":
    asyncio.run(broker.start())
