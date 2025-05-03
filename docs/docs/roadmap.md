---
id: roadmap
title: Roadmap
sidebar_label: Roadmap
---

_Last updated: 2024-05-03_

## 📋 About the Project

**Speech Coach** - a Telegram bot for practicing spoken English. Users receive questions, record voice answers, and the system processes them to provide feedback with recommendations for improvement.

## 🛠 Technologies Used

- **Backend**: FastAPI (Telegram server + webhook)
- **Data Processing**: FastStream + Redis Stream
- **Data Storage**: PostgreSQL, MinIO (audio)
- **NLP**: OpenAI API
- **Stream Processing**: Debezium, Redpanda, Bytewax
- **Analytics**: ClickHouse (planned)
- **Infrastructure**: Docker, Ansible, CI/CD

## 🎯 Project Status

### 🔊 Audio Processing
- [x] Audio converter implemented
- [x] Basic audio processing flow
- [x] Automatic file deletion after upload
- [ ] Add TOEFL Speaking 2-4 questions
- [ ] Add interview and work conversation practice questions

### 🤖 Telegram Bot
- [x] Telegram API integration
- [x] Sending questions to users
- [x] Receiving voice answers
- [x] Question sorting by answered status
- [x] Remove questions after answering
- [ ] Multilingual interface
- [ ] Question repetition feature

### 🧠 Analysis and Feedback
- [x] Basic answer analysis via OpenAI
- [ ] Advanced answer quality metrics
- [x] Time analysis from question to answer
- [x] Sliding window analysis (last N answers) via Bytewax
- [ ] Statistics on unique words and their frequency

### 🏗 Infrastructure
- [x] Celery/FastStream integration
- [x] PostgreSQL + MinIO for storage
- [x] Development configuration (environments.dev)
- [x] Containerization of all services
- [x] CI/CD pipeline (linting)
- [x] Ansible playbook for database
- [ ] Redis caching
- [ ] Ansible playbooks for all services
- [ ] Automated deployment

### 📊 Analytics and Stream Processing
- [x] Basic Debezium integration for data capture
- [x] Data transfer via Redpanda
- [x] Initial processing in Bytewax (word counting)
- [ ] Advanced real-time processing
- [ ] ClickHouse integration for analytical data storage
- [ ] Data export for analysis (ClickHouse + PostgreSQL)

### 👁 Monitoring
- [x] Basic logging
- [ ] Loki integration for centralized logs
- [ ] Grafana dashboards for all services
- [ ] Tracing with Jaeger / OpenTelemetry
- [ ] Metrics with Prometheus + Grafana
- [ ] Health endpoints for all services

### 💵 Monetization
- [x] Balance top-up system
- [ ] Credit system (1 GPT request = 1 credit)
- [ ] File storage agreement notification

### 📝 Documentation and Testing
- [x] Basic README
- [x] Architecture diagram
- [x] Tests for key components
- [ ] API and architecture documentation
- [ ] User guide
- [ ] Demo video with explanation in English

### 🌐 External Interfaces
- [ ] Minimal web interface (Next.js + Nest.js)
- [ ] API for integration with other services
- [ ] Preparation for academic collaboration and research

---

_This roadmap is a working document and evolves as development progresses._
