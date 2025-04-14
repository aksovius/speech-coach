.
├── app
│   ├── alembic.ini
│   ├── api
│   │   ├── deps
│   │   │   └── user.py
│   │   └── routes
│   │       ├── question.py
│   │       └── user.py
│   ├── audio
│   ├── bot
│   │   ├── dp.py
│   │   ├── handlers
│   │   │   ├── question_handler.py
│   │   │   ├── start_handler.py
│   │   │   └── voice_handler.py
│   │   └── middlewares
│   │       ├── auth_middleware.py
│   │       ├── database_session_middleware.py
│   │       └── user_data_middleware.py
│   ├── config.py
│   ├── crud
│   │   ├── question_crud.py
│   │   ├── user_crud.py
│   │   └── user_quota_crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models
│   │   └── schema.py
│   ├── requirements.txt
│   ├── schemas
│   │   ├── question_schema.py
│   │   └── user_schema.py
│   ├── services
│   │   ├── audio_service.py
│   │   ├── auth_service.py
│   │   ├── question_manager.py
│   │   ├── question_service.py
│   │   └── whisper_service.py
│   └── utils
│       └── database.py
├── config
│   ├── haproxy.cfg
│   └── patroni.yaml
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
│   └── terraform
│       └── main.tf
├── Makefile
└── README.md

20 directories, 41 files
