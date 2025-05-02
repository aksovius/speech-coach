import asyncio
import logging

from faststream import FastStream
from shared.messaging.broker import broker

import worker.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastStream(broker)

if __name__ == "__main__":
    asyncio.run(app.run())
