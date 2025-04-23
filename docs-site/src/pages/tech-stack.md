---
title: Tech Stack
---

# Tech Stack

Speech Coach is built with modern, production-grade tools to ensure scalability and reliability.

## Backend
- **FastAPI**: High-performance web server for handling Telegram webhooks and API requests.
- **FastStream**: Stream processing for audio tasks over Redis Streams.
- **PostgreSQL**: Persistent storage for users, questions, and answers.
- **MinIO**: Object storage for audio files.

## Audio Processing
- **OpenAI API**: Whisper for speech-to-text, GPT-4 for feedback generation.
- **Bytewax**: Real-time stream processing for analytics.
- **Redpanda + Debezium**: Change Data Capture (CDC) from PostgreSQL to analytics pipeline.

## Infrastructure
- **Docker + docker-compose**: Containerized services for easy deployment.
- **HAProxy, Patroni**: Planned high availability for PostgreSQL.
- **Ansible**: Automation for service setup (in progress).
- **Terraform**: Infrastructure-as-code groundwork.

## Observability (Planned)
- **Prometheus + Grafana**: Metrics monitoring.
- **Loki**: Centralized logging.
- **Jaeger/OpenTelemetry**: Distributed tracing.

This tech stack reflects a balance of performance, scalability, and modern development practices.