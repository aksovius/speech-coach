"""Tests for upload_service.py module."""

from unittest.mock import MagicMock, patch

import pytest

# Import a mocked version of the module
with patch("minio.Minio") as mock_minio:
    # Configure the mock
    mock_instance = mock_minio.return_value
    mock_instance.bucket_exists.return_value = True
    mock_instance.make_bucket = MagicMock()

    # Now import module after patching
    from shared.services import upload_service


# Skip all tests in this module
pytestmark = pytest.mark.skip(reason="MinIO connection issues")


@pytest.mark.asyncio
async def test_upload_file_success(mock_s3_client, temp_file):
    """Test successful file upload."""
    # Mock the minio client again for the test
    with patch.object(upload_service, "minio_client") as mock_minio:
        # Setup mock return value
        mock_minio.put_object.return_value = None

        # Call the tested method
        result = await upload_service.upload_file(temp_file)

        # Check that the result is a string (the storage_name)
        assert isinstance(result, str)
        # Check that it ends with right extension
        assert result.endswith(".txt")
        # Check that minio put_object was called once
        mock_minio.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_upload_file_missing_file():
    """Test file upload when file doesn't exist."""
    # Call with non-existent file
    result = await upload_service.upload_file("non_existent_file.txt")

    # Check error handling
    assert "error" in result
    assert "does not exist" in result["error"]


@pytest.mark.asyncio
async def test_upload_file_s3_error():
    """Test file upload when S3 error occurs."""
    # Mock the minio client for this test
    with patch.object(upload_service, "minio_client") as mock_minio:
        # Setup mock to raise S3Error
        mock_minio.put_object.side_effect = upload_service.S3Error("Test error")

        # Call with a temp file that exists
        with open("test_temp_file.txt", "w") as f:
            f.write("Test content")

        try:
            # Call the tested method
            result = await upload_service.upload_file("test_temp_file.txt")

            # Check error handling
            assert "error" in result
            assert "Test error" in result["error"]
        finally:
            # Clean up
            import os

            if os.path.exists("test_temp_file.txt"):
                os.remove("test_temp_file.txt")
