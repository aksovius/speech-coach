---
id: roadmap
title: Roadmap
sidebar_label: Roadmap
---

_Last updated: 2025-05-11_

## 📋 About the Project

**Speech Coach** is a Telegram bot for practicing spoken English. Users receive questions, record voice answers, and the system processes them to provide feedback with recommendations for improvement.

## 🛠 Technologies Used

- **Backend**: FastAPI (Telegram server + webhook)
- **Data Processing**: FastStream + Redis Stream
- **Data Storage**: PostgreSQL, MinIO (audio)
- **NLP**: OpenAI API
- **Stream Processing**: Debezium, Redpanda, Bytewax
- **Analytics**: ClickHouse
- **Infrastructure**: Docker, Ansible, CI/CD

## ✅ Core Features Implemented

### 🔊 Audio Processing
- [x] Audio converter implemented
- [x] Audio processing via FastStream worker
- [x] Automatic file deletion after upload
- [x] Redis stream integration
- [x] Length and quality control (max 45s, compression)

### 🤖 Telegram Bot
- [x] Telegram API integration
- [x] Send/receive audio questions and answers
- [x] Question sorting and cleanup
- [x] Inline buttons and updated menu UX
- [x] Separate logic for different question types

### 🧠 Answer Analysis
- [x] OpenAI GPT-based analysis
- [x] Answer time tracking
- [x] TTR (unique word ratio)
- [x] Sliding window (last N answers) with Bytewax

### 🏗 Infrastructure
- [x] Docker containerization
- [x] Redis caching: user info and state
- [x] PostgreSQL + MinIO storage
- [x] Basic health check endpoints
- [x] CI/CD for linting and gh-pages
- [x] Ansible for database and basic setup

### 📊 Monitoring and Logs
- [x] Centralized logging via Loki
- [x] Metrics via Prometheus → Grafana
- [x] Grafana dashboards for core services

### 💵 Monetization
- [x] Manual balance top-up system

### 📝 Documentation
- [x] Readme and setup instructions
- [x] Architecture diagram (Graphviz)
- [x] Roadmap and overview

---

## 🛠 In Progress / Priority Tasks

- [ ] **Repeat-answer logic**: tag repeated answers (used for mimicry), exclude from metrics
- [ ] **Word cloud (last 30 days)**: active vocabulary stats via Bytewax → ClickHouse
- [ ] **Dashboard rewrite**:
  - [ ] Move all queries behind backend API
  - [ ] Migrate away from client-DDNS access
  - [ ] Centralize on server; plan for a separate dashboard host
- [ ] **New question types**:
  - [ ] Interview preparation questions
  - [ ] TOEFL Speaking 2–4 (with reading/audio prompt support)
- [ ] **E2E and load testing**:
  - [ ] Simulate multiple users and audio uploads
  - [ ] Track processing time and system load

---

## 🕒 Optional / Future Enhancements

- [ ] Full Ansible deployment for all services
- [ ] ClickHouse retention policy and long-term storage strategy
- [ ] GPT credit-based request system
- [ ] External API for integration
- [ ] Multilingual interface
- [ ] User guide and demo video for portfolio/showcase


---

_This roadmap is a working document and evolves as development progresses._
