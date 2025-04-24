---
id: architecture-choices
title: Architecture Design
sidebar_label: Architecture Design
---

# 🧠 Architecture Design Choices

This page provides a behind-the-scenes look at the technical decisions made while building **Speech Coach** — what technologies were chosen and why.

---

## 💡 Why FastAPI + Redis Stream + Worker?

I previously worked with Celery, but found it **heavy and configuration-intensive** for lean prototypes. Instead, I chose **FastStream** with **Redis Streams**, which felt like a better fit for a lightweight, real-time system.

Redis Streams preserve message history (unlike pub/sub), similar to Kafka, but with far lower overhead — perfect for **business-layer logic**.

I considered using Redpanda for business messaging too, but decided to **separate responsibilities**:

- **Redis Streams** handle core task distribution
- **Redpanda** handles analytics pipelines

Redis will also be used for caching — for instance, mapping `telegram_id → user_id`, so all internal logic uses a unified user ID. This abstraction allows me to **swap Telegram with WhatsApp, Discord, etc.** in the future.

---

## 🔁 Why Separate FastAPI and Worker?

The architecture is split for performance and scalability:

- **FastAPI** handles routing and distributes tasks — think of it as the "message switchboard"
- **Workers** process audio and generate feedback

This keeps the API responsive and allows independent scaling of workers — even on separate machines. It also reduces coupling and simplifies deployment.

---

## 📤 Why Redis Streams Instead of Kafka?

Kafka is powerful, but **overkill for this project**. Redpanda is a great Kafka alternative — faster, simpler, C++-based — but even that felt too much for core messaging.

Redis is already in the stack for caching and its Streams API is a **natural fit** for low-latency queuing.

---

## 📦 Why MinIO for Audio?

MinIO is a self-hosted, S3-compatible solution — **fast, cheap, local**. It avoids Internet upload delays during audio ingestion, and files can be **replicated to S3** later as a cold backup.

This hybrid gives both performance and portability — with full control.

---

## 📊 Why Bytewax for Analytics?

Bytewax was chosen for two reasons:

1. It's built in **Python**, just like the rest of the backend
2. Analysts can prototype in notebooks, then deploy to production with minimal changes

Other options (like Flink) required Scala/Java and didn't justify the complexity for a Python-native stack.
