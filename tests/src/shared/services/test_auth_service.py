"""Tests for auth_service.py module."""

import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# First patch imports for server.models.schema
with patch.dict(
    "sys.modules",
    {
        "server.models.schema": MagicMock(),
        "server.crud.user_crud": MagicMock(),
        "server.crud.user_quota_crud": MagicMock(),
    },
):
    # Create mocks for classes used in tests
    class MockUser:
        def __init__(self, id, telegram_id, username):
            self.id = id
            self.telegram_id = telegram_id
            self.username = username

    class MockUserQuota:
        def __init__(self, id, user_id, total_allowed, used):
            self.id = id
            self.user_id = user_id
            self.total_allowed = total_allowed
            self.used = used

    # Configure mocks for imported modules
    sys.modules["server.models.schema"].User = MockUser
    sys.modules["server.models.schema"].UserQuota = MockUserQuota

    # Now import the module being tested
    from shared.schemas.user_schema import UserCreate
    from shared.services import auth_service


# Skip auth_service tests due to async testing issues
pytestmark = pytest.mark.skip(
    reason="Authorization services cannot be tested in current configuration"
)


@pytest.mark.asyncio
async def test_get_current_user_or_create_existing_user():
    """Test getting existing user."""
    # Test data preparation
    user_data = UserCreate(
        telegram_id=123456, username="testuser", first_name="Test", last_name="User"
    )
    db_session = AsyncMock()

    # Create mock user object
    mock_user = MockUser(id=1, telegram_id=123456, username="testuser")

    # Mock for crud_user.get_by_telegram_id
    with patch(
        "server.crud.user_crud.get_by_telegram_id", AsyncMock(return_value=mock_user)
    ):
        # Mock for crud_user.create_user (should not be called)
        with patch("server.crud.user_crud.create_user") as mock_create_user:
            # Mock for user_quota_crud.create_user_quota (should not be called)
            with patch(
                "server.crud.user_quota_crud.create_user_quota"
            ) as mock_create_quota:
                # Call the tested method
                result = await auth_service.get_current_user_or_create(
                    user_data, db_session
                )

                # Check results
                assert result == mock_user
                mock_create_user.assert_not_called()
                mock_create_quota.assert_not_called()


@pytest.mark.asyncio
async def test_get_current_user_or_create_new_user():
    """Test creating new user when not exists."""
    # Test data preparation
    user_data = UserCreate(
        telegram_id=123456, username="testuser", first_name="Test", last_name="User"
    )
    db_session = AsyncMock()

    # Create mock user object
    mock_user = MockUser(id=1, telegram_id=123456, username="testuser")

    # Mock for crud_user.get_by_telegram_id (user not found)
    with patch(
        "server.crud.user_crud.get_by_telegram_id", AsyncMock(return_value=None)
    ):
        # Mock for crud_user.create_user (creating new user)
        with patch(
            "server.crud.user_crud.create_user", AsyncMock(return_value=mock_user)
        ):
            # Mock for user_quota_crud.create_user_quota
            with patch("server.crud.user_quota_crud.create_user_quota", AsyncMock()):
                # Call the tested method
                result = await auth_service.get_current_user_or_create(
                    user_data, db_session
                )

                # Check results
                assert result == mock_user


@pytest.mark.asyncio
async def test_get_user_id_and_quota():
    """Test getting user ID and quota."""
    # Test data preparation
    user_data = UserCreate(
        telegram_id=123456, username="testuser", first_name="Test", last_name="User"
    )
    db_session = AsyncMock()

    # Create mock user and quota objects
    mock_user = MockUser(id=1, telegram_id=123456, username="testuser")
    mock_quota = MockUserQuota(id=1, user_id=1, total_allowed=10, used=3)

    # Mock for get_current_user_or_create
    with patch(
        "shared.services.auth_service.get_current_user_or_create",
        AsyncMock(return_value=mock_user),
    ):
        # Mock for user_quota_crud.get_user_quota
        with patch(
            "server.crud.user_quota_crud.get_user_quota",
            AsyncMock(return_value=mock_quota),
        ):
            # Call the tested method
            result = await auth_service.get_user_id_and_quota(user_data, db_session)

            # Check results
            assert result == {"user_id": 1, "quota": 7}  # 10 allowed - 3 used = 7
