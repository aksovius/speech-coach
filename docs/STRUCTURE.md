.
├── config
│   ├── debezium.json
│   ├── haproxy.cfg
│   ├── patroni.yaml
│   ├── pg_hba.conf
│   ├── postgresql.conf
│   ├── postgres-source-config.json
│   └── requirements.dev.txt
├── db_dump.sql
├── deploy
│   ├── entrypoint.sh
│   └── init_users.sh
├── docker-compose.yaml
├── docs
│   ├── architecture.md
│   ├── diagrams
│   │   └── sequence.md
│   ├── roadmap.md
│   └── STRUCTURE.md
├── infra
│   ├── ansible
│   │   ├── ansible.pub
│   │   ├── bootstrap.yml
│   │   ├── inventory
│   │   │   ├── group_vars
│   │   │   │   ├── fastapi.yml
│   │   │   │   └── postgresql.yml
│   │   │   └── hosts.yml
│   │   ├── roles
│   │   │   ├── fastapi
│   │   │   │   ├── files
│   │   │   │   │   └── fastapi.service
│   │   │   │   ├── tasks
│   │   │   │   │   └── main.yml
│   │   │   │   └── templates
│   │   │   │       └── requirements.txt
│   │   │   ├── minio
│   │   │   └── postgresql
│   │   │       ├── handlers
│   │   │       │   └── main.yml
│   │   │       └── tasks
│   │   │           └── main.yml
│   │   └── site.yml
│   └── terraform
│       └── main.tf
├── Makefile
├── README.md
├── src
│   ├── app
│   │   ├── ai
│   │   │   ├── client.py
│   │   │   ├── prompts.py
│   │   │   └── services
│   │   │       ├── audio_service.py
│   │   │       └── chat_service.py
│   │   ├── alembic.ini
│   │   ├── api
│   │   │   ├── deps
│   │   │   │   └── user.py
│   │   │   └── routes
│   │   │       ├── question.py
│   │   │       └── user.py
│   │   ├── audio
│   │   ├── bot
│   │   │   ├── dp.py
│   │   │   ├── handlers
│   │   │   │   ├── question_handler.py
│   │   │   │   ├── start_handler.py
│   │   │   │   └── voice_handler.py
│   │   │   └── middlewares
│   │   │       ├── auth_middleware.py
│   │   │       ├── database_session_middleware.py
│   │   │       └── user_data_middleware.py
│   │   ├── config.py
│   │   ├── crud
│   │   │   ├── question_crud.py
│   │   │   ├── user_answers_crud.py
│   │   │   ├── user_crud.py
│   │   │   └── user_quota_crud.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── models
│   │   │   └── schema.py
│   │   ├── requirements.txt
│   │   ├── schemas
│   │   │   ├── question_schema.py
│   │   │   └── user_schema.py
│   │   ├── services
│   │   │   ├── answers_service.py
│   │   │   ├── audio_processing.py
│   │   │   ├── audio_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── download_service.py
│   │   │   ├── question_manager.py
│   │   │   ├── question_service.py
│   │   │   └── upload_service.py
│   │   ├── temp_audio.ogg
│   │   ├── temp_audio.wav
│   │   └── utils
│   │       └── database.py
│   └── bytewax
│       ├── config.py
│       ├── docker-compose.yml
│       ├── Dockerfile
│       ├── main2.py
│       ├── main.py
│       ├── processors
│       │   ├── aggregators.py
│       │   ├── deserialize.py
│       │   ├── filters.py
│       │   └── text_processing.py
│       ├── requirements.txt
│       └── sinks.py
└── tests

38 directories, 79 files
