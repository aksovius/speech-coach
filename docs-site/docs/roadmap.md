---
id: roadmap
title: Roadmap
sidebar_label: Roadmap
---

_Last updated: 2025-04-22_

## ✅ Completed Tasks
- [x] Audio converter implemented
- [x] Integrated Celery/FastStream
- [x] Upload answers to MinIO
- [x] Save answers to PostgreSQL
- [x] Question sorting by answered status
- [x] Audio processing minimum viable flow
- [x] PostgreSQL + MinIO storage connected
- [x] Balance top-up
- [x] Created `enviroments.dev`
- [x] Added `Makefile`
- [x] Linter integration
- [x] Auto-delete files after upload
- [x] Basic README created
- [x] Architecture diagram (Graphviz)
- [x] Containerization of all services
- [x] Ansible playbook for database


### Core Features
- [ ] Redis cache for `user_id`
- [ ] Script to migrate question bank
- [ ] Multilingual interface (basic and auto-translation)
- [ ] Credit system (1 GPT request = 1 credit)
- [ ] File storage agreement notification
- [ ] Whisper temperature setting control
- [x] Remove questions after answering
- [ ] Enable question repetition
- [ ] Time analysis: measure time from question to answer
- [ ] Sliding window analysis (Flink): TTR per 10 lessons / day / month

### Infrastructure
- [ ] Redis integration for session caching
- [ ] Ansible playbooks for all services
- [ ] Helm chart (optional / future)
- [ ] CI/CD pipeline for deploy (not only lint)
- [ ] Logging aggregation (ELK/EFK stack)
- [ ] Tracing with Jaeger / OpenTelemetry
- [ ] Metrics with Prometheus + Grafana
- [ ] Health endpoints: `/healthz`, `/readyz` for all services
- [ ] Auto-restart or rollback on service failure

### Observability & Monitoring
- [ ] Connect Loki for centralized logs
- [ ] Grafana dashboards for FastAPI, Bytewax, Redis, ClickHouse
- [ ] Setup ClickHouse for analytics backend

### Testing & Documentation
- [ ] Extend tests (Pytest + coverage)
- [ ] Improve docs (`/docs`, architecture overview)
- [ ] Add usage guide (Markdown or screencast intro)
- [ ] Demo video with voice-over in English

### Future Enhancements
- [ ] Add TOEFL Speaking 2-4 question types
- [ ] Add interview & conversation practice questions
- [ ] Launch minimal frontend (Next.js + Nest.js API)
- [ ] Research export API / interface for collaboration
- [ ] Prepare for academic collaboration and research publication
- [ ] Expose data pipeline for analysis (ClickHouse + PostgreSQL export)

---

_This roadmap is a working document and evolves as development progresses._
