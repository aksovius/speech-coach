#!/bin/bash

# Wait for MinIO to be ready
until mc alias set myminio http://minio:9090 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"; do
  echo 'Waiting for MinIO to be ready...'
  sleep 1
done

# Create bucket if it doesn't exist
mc mb "myminio/${MINIO_BUCKET}" || true

# Set bucket policy to public
mc policy set public "myminio/${MINIO_BUCKET}"
