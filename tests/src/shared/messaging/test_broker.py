"""Tests for broker.py module."""

import asyncio

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
    response_received = asyncio.Event()
    received_response = None

    # Define a test handler that returns a response
    @broker.subscriber(test_channel)
    async def test_handler(msg):
        assert msg == test_message
        return response_message

    # Define a response handler
    @broker.subscriber(f"{test_channel}_response")
    async def response_handler(msg):
        nonlocal received_response
        received_response = msg
        response_received.set()

    # Use TestRedisBroker for testing
    async with TestRedisBroker(broker) as test_broker:
        # Send request
        await test_broker.publish(
            message=test_message,
            channel=test_channel,
            reply_to=f"{test_channel}_response",
        )

        # Wait for response with timeout
        try:
            await asyncio.wait_for(response_received.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            pytest.fail("Timeout waiting for RPC response")

        # Verify response
        assert received_response == response_message
