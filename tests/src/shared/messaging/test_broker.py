"""Tests for broker.py module."""

import json

import pytest
from faststream.redis import RedisBroker, TestRedisBroker
from shared.config import settings
from shared.messaging.broker import broker


@pytest.mark.asyncio
async def test_broker_initialization():
    """Test broker initialization with correct settings."""
    # Check that broker is initialized with correct Redis URL
    assert isinstance(broker, RedisBroker)
    assert broker.url == settings.REDIS_URL


@pytest.mark.asyncio
async def test_broker_publish_subscribe():
    """Test message publishing and subscription functionality."""
    test_message = {"test": "data"}
    test_channel = "test_channel"
    received_message = None

    # Define a test handler
    @broker.subscriber(test_channel)
    async def test_handler(msg):
        nonlocal received_message
        received_message = msg

    # Use TestRedisBroker for testing
    async with TestRedisBroker(broker) as test_broker:
        # Publish a message
        await test_broker.publish(test_message, channel=test_channel)

        # Verify message was received
        assert received_message == test_message


@pytest.mark.asyncio
async def test_broker_rpc():
    """Test RPC (Request-Reply) functionality."""
    test_message = {"test": "data"}
    test_channel = "test_rpc_channel"
    response_message = {"response": "success"}

    # Define a test handler that returns a response
    @broker.subscriber(test_channel)
    async def test_handler(msg):
        assert msg == test_message
        return response_message

    # Use TestRedisBroker for testing
    async with TestRedisBroker(broker) as test_broker:
        # Send request and wait for response
        response = await test_broker.request(test_message, channel=test_channel)

        # Verify response
        assert json.loads(response.body) == response_message
