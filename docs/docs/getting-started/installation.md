---
id: installation
title: Installation
sidebar_label: Installation
---

⚙️ Installing Speech Coach

Ready to try **Speech Coach** locally? Here's how to set it up using Docker Compose. You’ll be up and running in just a few minutes.

---

## 🧰 Prerequisites

Before you begin, make sure the following tools are installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- A `.env` file configured with your secrets (based on the included `.env.example`)

---

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/aksovius/speech-coach.git
cd speech-coach
```

### 2. Configure Environment Variables

Copy the example file and add your own values:

```bash
cp .env.example .env
```

Edit `.env` and fill in required secrets like:

- `DB_PASS`
- `REDIS_PASSWORD`
- `MINIO_ROOT_USER`
- `TELEGRAM_BOT_TOKEN` (needed to link your Telegram bot)

---

### 3. Launch the Application

Build and run everything using Docker Compose:

```bash
docker-compose up --build
```

This will spin up the API server, audio processor, PostgreSQL, Redis, and MinIO.

---

### 4. Connect to Your Telegram Bot

Once the containers are running:

- Make sure your bot token is set in `.env`
- Interact with your bot on Telegram
- You should receive prompts and get feedback on your replies

If using webhooks, ensure your API is publicly accessible with **HTTPS**.

---

### 5. (Optional) Enable HTTPS for Webhooks

If deploying externally:

- Set up **Nginx with SSL** (e.g., via Let's Encrypt)
- Point the webhook URL to your secure endpoint

---

## 🧯 Troubleshooting

- Check if required ports are free: `8000`, `5432`, `6379`, etc.
- Run `docker-compose logs` to view logs and debug issues
- Use `docker ps` to verify all services are up

---

For more advanced setup or environment customization, check out the Configutation section.
