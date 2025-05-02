"""End-to-end tests for the speech coach application."""

import asyncio
import json
import time
from datetime import datetime

import httpx
import pytest
import redis.asyncio as redis
from clickhouse_driver import Client as ClickhouseClient


@pytest.fixture
async def redis_client():
    """Create Redis client."""
    client = redis.Redis(host="redis", port=6379, decode_responses=True)
    yield client
    await client.close()


@pytest.fixture
def clickhouse_client():
    """Create ClickHouse client."""
    client = ClickhouseClient(host="clickhouse")
    yield client
    client.disconnect()


@pytest.fixture
async def telegram_client():
    """Create HTTP client for Telegram mock."""
    async with httpx.AsyncClient(base_url="http://telegram-mock:3000") as client:
        yield client


@pytest.fixture
async def openai_client():
    """Create HTTP client for OpenAI mock."""
    async with httpx.AsyncClient(base_url="http://openai-mock:3000") as client:
        yield client


async def wait_for_message_processing(clickhouse_client, user_id, timeout=30):
    """Wait for message to be processed and appear in ClickHouse."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = clickhouse_client.execute(
            """
            SELECT *
            FROM user_answers
            WHERE user_id = %(user_id)s
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            {"user_id": user_id},
        )
        if result:
            return result[0]
        await asyncio.sleep(1)
    raise TimeoutError("Message processing timeout")


@pytest.mark.asyncio
async def test_voice_message_processing(
    redis_client, clickhouse_client, telegram_client, openai_client
):
    """Test complete flow of voice message processing."""
    # Clear previous test data
    await telegram_client.post("/_test/clear")
    await openai_client.post("/_test/clear")

    # Test data
    user_id = 12345
    file_id = "test_voice_message"

    # Simulate voice message processing
    # 1. Send voice message to Redis
    message_data = {
        "telegram_id": user_id,
        "file_id": file_id,
        "timestamp": datetime.now().isoformat(),
    }
    await redis_client.publish("voice_messages", json.dumps(message_data))

    # 2. Wait for processing and check ClickHouse
    try:
        result = await wait_for_message_processing(clickhouse_client, user_id)

        # 3. Verify the result
        assert result[1] == user_id  # user_id
        assert result[3] is not None  # asr_transcript
        assert result[4] is not None  # score_overall

        # 4. Verify Telegram messages
        messages = (await telegram_client.get("/_test/messages")).json()
        assert len(messages) > 0
        assert messages[-1]["chat_id"] == user_id

        # 5. Verify OpenAI requests
        requests = (await openai_client.get("/_test/requests")).json()
        assert len(requests) > 0
        transcription_request = next(
            r for r in requests if r["type"] == "transcription"
        )
        assert transcription_request is not None

    except TimeoutError:
        pytest.fail("Message processing took too long")
