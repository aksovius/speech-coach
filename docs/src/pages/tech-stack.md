---
title: Tech Stack
---


# 🧰 Tech Stack

**Speech Coach** is built with modern, production-grade technologies focused on scalability, real-time data flow, and developer efficiency.

---

## 💻 Backend

- **FastAPI** – Handles Telegram webhooks and RESTful API requests
- **FastStream** – Manages audio processing tasks over **Redis Streams**
- **PostgreSQL** – Stores users, questions, feedback, and session history
- **Redis** – Used for queuing, caching (planned), and stream coordination
- **MinIO** – S3-compatible object storage for voice messages

---

## 🔊 Audio & Feedback Processing

- **OpenAI API** – 
  - **Whisper** for speech-to-text
  - **GPT-4** for feedback generation and sample answers
- **Bytewax** – Stream-based real-time analytics (e.g. sliding windows)
- **Redpanda + Debezium** – CDC from PostgreSQL to analytics pipeline
- **ClickHouse** – High-performance OLAP database for storing and querying metrics

---

## 🛠️ Infrastructure

- **Docker + docker-compose** – Containerized dev environment
- **Ansible** – Partial service automation (in progress)
- **Terraform** – Infrastructure-as-code for future scalability
- **HAProxy** – Planned load balancing for multi-instance deployments
- **Patroni** – Planned high availability setup for PostgreSQL

---

## 📊 Observability & Monitoring (Planned)

- **Prometheus + Grafana** – For metrics collection and visualization
- **Loki** – Centralized logging backend
- <!-- optionally keep for later -->
- <!-- **Jaeger / OpenTelemetry** – For distributed tracing (under consideration) -->

---

This stack reflects a balance of **performance**, **resilience**, and **modern engineering principles** — ready for production scaling and future experimentation.