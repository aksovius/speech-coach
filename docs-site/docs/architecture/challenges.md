---
id: challenges
title: Technical Challenges
sidebar_label: Challenges
---

# 🧗 Technical Challenges

Building **Speech Coach** presented several architectural and infrastructure challenges, especially when balancing real-time feedback, scalability, and system resilience.

---

## 1. Webhook Handling at Scale

Telegram supports only **one webhook endpoint per bot**, making horizontal scaling non-trivial.

- Initially, a single **FastAPI** instance handles all webhooks.
- To support multiple instances, a load balancer such as **NGINX** or **HAProxy** is required.
- Redis is used to share session or state across instances.

---

## 2. FastAPI Scalability: Horizontal vs Vertical

There are two main strategies to scale the **FastAPI** app:

### 🔁 Vertical Scaling (Deep)

- You can increase the number of **Gunicorn workers** per instance to leverage multiple CPU cores.
- This increases throughput on a single node.
- However, state (e.g., session cache) must be **shared across worker processes** — Redis is planned for this purpose.

### 🌐 Horizontal Scaling (Wide)

- Deploy **multiple FastAPI servers** across different nodes or containers.
- Use a **HAProxy cluster** in front to distribute traffic across instances.
- **Redis** should be clustered (2–3 nodes) to ensure **shared state and high availability**.

To further increase fault tolerance:

- Set up **PostgreSQL in HA mode** using **Patroni + etcd** or a similar orchestrator.
- This ensures automatic failover and seamless recovery in case of DB outages.
- HAProxy can also route database traffic to the active **PostgreSQL leader**.


---

## 3. Stream-Based Audio Processing

Handling voice messages asynchronously and reliably required careful orchestration:

- Used **Redis Streams + FastStream** for async job dispatch
- Workers are isolated, stateless, and can be scaled independently
- Includes retry mechanisms for OpenAI API failures or network issues

#### ⚙️ Preprocessing Optimizations

To reduce processing time and API costs, several audio preprocessing steps were introduced:

- **Downsampling audio** (e.g., 48kHz → 16kHz) to reduce file size without loss of quality for transcription
- **Silence removal** to skip unspoken segments and reduce duration
- **Playback speed-up** (e.g., 2×) to minimize audio length before sending to the API

These techniques significantly improve throughput and reduce expenses when working with usage-billed APIs like Whisper or GPT.

---


## 4. AI Feedback Latency & Rate Limits

Using **OpenAI Whisper + GPT-4** in real-time brings both benefits and limitations:

- Transcription is fast, but GPT-4 generation can be slow under load
- To mitigate latency:
  - Workers handle generation off-main thread
  - A future plan includes **dedicated GPT workers** to offload feedback generation

#### 🌐 Future Improvement: API Failover

To improve reliability, it may be beneficial to introduce a **failover mechanism** for feedback generation:

- Configure a **secondary AI provider** (e.g., Claude, Gemini, or local LLM) as a fallback
- Automatically route requests there in case of timeout, quota exhaustion, or OpenAI downtime
- This ensures **graceful degradation** and uninterrupted user experience under stress

This strategy would reduce single-point-of-failure risks and support continuous operation in production environments.
---

## 5. Real-Time Analytics Pipeline

We adopted a stream-processing architecture to enable real-time analysis:

- **Debezium** captures changes from PostgreSQL (CDC)
- **Redpanda** transports events to **Bytewax**
- Bytewax processes sliding window metrics (e.g., avg. response length, unique words)
- Future: Store analytics in **ClickHouse**, visualize via **Grafana**

#### 💡 Tech Stack Rationale

Originally, a **Kafka + Flink** pipeline was considered. However:

- **Redpanda** was chosen for its **lower operational overhead** while retaining Kafka API compatibility
- **Bytewax** was selected because it's written in **Python**, aligning with the rest of the backend
- Maintaining Flink (written in Scala/Java) for just one part of the pipeline would have added unnecessary complexity

This setup allows for tight integration, faster development, and easier onboarding for Python engineers.
---

## 6. Scalability & Future-Proofing

To ensure the platform evolves smoothly:

- Architecture supports **modular scaling** at each layer
- All services are containerized with Docker
- Infrastructure is managed via **Terraform + Ansible** (Future)
- Monitoring is designed around **Prometheus, Loki, Grafana** (Future)

> See the [System Overview](./overview) or [Data Flow](./data-flow) pages for visual diagrams and architectural context.