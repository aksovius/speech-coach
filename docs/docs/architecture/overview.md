---
id: overview
title: System Overview
sidebar_label: Overview
sidebar_position: 1
---

# 🧠 System Overview

Speech Coach is built with a modular microservices architecture designed for real-time audio processing, AI feedback, and language analytics.

The system is divided into logical layers:

- **User & Frontend** – Interaction through Telegram, routed via NGINX
- **Application Layer** – FastAPI + Redis Stream for async task distribution
- **Processing Layer** – Workers handle transcription and feedback via OpenAI
- **Storage Layer** – PostgreSQL for data, MinIO for audio
- **Analytics Layer** – CDC via Debezium → Redpanda → Bytewax for streaming
- **Monitoring & Visualization (Planned)** – Grafana, Loki, Prometheus, ClickHouse

![Architecture Diagram](/img/architecture-diagram.svg)

This architecture supports future scaling via FastAPI/Worker clusters, HA PostgreSQL, and a frontend dashboard.

For deeper insight into component communication, see [Data Flow](./data-flow).
