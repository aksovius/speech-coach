import asyncio
import logging

import consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from faststream import FastStream
from messaging.broker import broker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastStream(broker)

if __name__ == "__main__":
    asyncio.run(app.run())
