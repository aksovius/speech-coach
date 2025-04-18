import asyncio
from app.messaging.broker import broker
import app.messaging.consumers 

if __name__ == "__main__":
    asyncio.run(broker.start())