---
id: installation
title: Installation
sidebar_label: Installation
---

## Installing Speech Coach

Follow these steps to set up Speech Coach locally using Docker Compose.

### Prerequisites
- **Docker** and **Docker Compose** installed.
- **Git** for cloning the repository.
- Environment variables configured in `secrets/speech-coach.env`.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/aksovius/speech-coach.git
   cd speech-coach
   ```
2. Set up environment variables:
- Copy secrets/speech-coach.env.example to secrets/speech-coach.env.
- Fill in required values (e.g., DB_PASS, REDIS_PASSWORD, MINIO_ROOT_USER).
3. Build and run the services:
```bash
docker-compose up --build
```
4. Access the Telegram bot:
- Configure your Telegram bot token in the environment file.
- Interact with the bot to test functionality.

Troubleshooting
- Ensure all ports (e.g., 8000, 5432, 6379) are available.
- Check container logs with docker-compose logs for errors.

For detailed configuration, see Configuration.
