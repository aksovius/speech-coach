---
id: data-flow
title: Data Flow
sidebar_label: Data Flow
sidebar_position: 2
---

# 🔄 Data Flow

This page explains how data moves through the system — from a user's voice message to processed feedback and analytics.

## 1. Voice Message → FastAPI
- User sends a voice message to Telegram
- Telegram forwards it to the FastAPI server (via webhook)
- FastAPI pushes a processing task to **Redis Stream**

## 2. Audio Processing
- The **FastStream worker** listens to Redis and downloads the voice message
- It sends the file to **OpenAI Whisper** for transcription
- The transcript is enriched with feedback using **GPT-4**
- Audio is stored in **MinIO**, transcript and feedback in **PostgreSQL**

## 3. Real-Time Analytics
- **Debezium** watches PostgreSQL changes and sends events to **Redpanda**
- **Bytewax** ingests the stream and performs windowed analysis
- (Planned) Results stored in **ClickHouse** and visualized via **Grafana**

To understand the architectural motivation behind this setup, see [Challenges](./challenges).
