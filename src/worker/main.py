import asyncio
import logging

from faststream import FastStream

import worker.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from shared.messaging.broker import broker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastStream(broker)

if __name__ == "__main__":
    asyncio.run(app.run())
