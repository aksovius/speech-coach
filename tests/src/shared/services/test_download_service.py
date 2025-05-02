"""Tests for download_service.py module."""

from unittest.mock import MagicMock, mock_open, patch

import pytest

from shared.services import download_service


class MockResponse:
    """Mock for aiohttp response."""

    def __init__(self, status, content=b"test content"):
        self.status = status
        self._content = content

    async def read(self):
        return self._content

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.mark.asyncio
async def test_download_file_success():
    """Test successful file download."""
    file_url = "https://example.com/test.txt"
    file_path = "test_download.txt"

    # Mock for aiohttp.ClientSession
    mock_session = MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    # Mock for session.get
    mock_resp = MockResponse(status=200)
    mock_session.get.return_value = mock_resp

    with patch("aiohttp.ClientSession", return_value=mock_session):
        with patch("builtins.open", mock_open()) as mock_file:
            # Call the tested method
            result = await download_service.download_file(file_url, file_path)

            # Check results
            assert result == file_path
            mock_session.get.assert_called_once_with(file_url)
            mock_file.assert_called_once_with(file_path, "wb")
            mock_file().write.assert_called_once_with(b"test content")


@pytest.mark.asyncio
async def test_download_file_http_error():
    """Test file download with HTTP error."""
    file_url = "https://example.com/test.txt"
    file_path = "test_download.txt"

    # Mock for aiohttp.ClientSession
    mock_session = MagicMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None

    # Mock for session.get with 404 error
    mock_resp = MockResponse(status=404)
    mock_session.get.return_value = mock_resp

    with patch("aiohttp.ClientSession", return_value=mock_session):
        # Call the tested method
        result = await download_service.download_file(file_url, file_path)

        # Check results
        assert result is None
        mock_session.get.assert_called_once_with(file_url)


@pytest.mark.asyncio
async def test_download_file_exception():
    """Test file download with exception."""
    file_url = "https://example.com/test.txt"
    file_path = "test_download.txt"

    # Mock for aiohttp.ClientSession with exception
    mock_session = MagicMock()
    mock_session.__aenter__.side_effect = Exception("Connection error")

    with patch("aiohttp.ClientSession", return_value=mock_session):
        # Call the tested method
        result = await download_service.download_file(file_url, file_path)

        # Check results
        assert result is None
