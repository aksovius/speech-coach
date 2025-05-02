import io
import mimetypes
import uuid
from pathlib import Path

from minio import Minio
from minio.error import S3Error
from shared.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False,  # Set True if using HTTPS
)

if not minio_client.bucket_exists(settings.MINIO_BUCKET):
    minio_client.make_bucket(settings.MINIO_BUCKET)


async def upload_file(file_path: str):
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist")

        original_name = file_path.name
        ext = file_path.suffix
        unique_id = uuid.uuid4().hex
        storage_name = f"{unique_id}{ext}"

        content_type, _ = mimetypes.guess_type(original_name)
        if content_type is None:
            content_type = "application/octet-stream"

        file_data = file_path.read_bytes()

        minio_client.put_object(
            settings.MINIO_BUCKET,
            storage_name,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )

        return storage_name
    except S3Error as e:
        return {"error": str(e)}
