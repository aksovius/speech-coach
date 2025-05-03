.
├── config
│   ├── debezium
│   │   └── connector.json
│   ├── haproxy
│   │   └── haproxy.cfg
│   ├── patroni
│   │   └── patroni.yaml
│   └── postgresql
│       ├── pg_hba.conf
│       └── postgresql.conf
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
├── docs-site
│   ├── blog
│   │   ├── 2019-05-28-first-blog-post.md
│   │   ├── 2019-05-29-long-blog-post.md
│   │   ├── 2021-08-01-mdx-blog-post.mdx
│   │   ├── 2021-08-26-welcome
│   │   │   ├── docusaurus-plushie-banner.jpeg
│   │   │   └── index.md
│   │   ├── authors.yml
│   │   └── tags.yml
│   ├── docs
│   │   ├── intro.md
│   │   ├── tutorial-basics
│   │   │   ├── _category_.json
│   │   │   ├── congratulations.md
│   │   │   ├── create-a-blog-post.md
│   │   │   ├── create-a-document.md
│   │   │   ├── create-a-page.md
│   │   │   ├── deploy-your-site.md
│   │   │   └── markdown-features.mdx
│   │   └── tutorial-extras
│   │       ├── _category_.json
│   │       ├── img
│   │       │   ├── docsVersionDropdown.png
│   │       │   └── localeDropdown.png
│   │       ├── manage-docs-versions.md
│   │       └── translate-your-site.md
│   ├── docusaurus.config.ts
│   ├── package.json
│   ├── README.md
│   ├── sidebars.ts
│   ├── src
│   │   ├── components
│   │   │   └── HomepageFeatures
│   │   │       ├── index.tsx
│   │   │       └── styles.module.css
│   │   ├── css
│   │   │   └── custom.css
│   │   └── pages
│   │       ├── index.module.css
│   │       ├── index.tsx
│   │       └── markdown-page.md
│   ├── static
│   │   └── img
│   │       ├── docusaurus.png
│   │       ├── docusaurus-social-card.jpg
│   │       ├── favicon.ico
│   │       ├── logo.svg
│   │       ├── undraw_docusaurus_mountain.svg
│   │       ├── undraw_docusaurus_react.svg
│   │       └── undraw_docusaurus_tree.svg
│   └── tsconfig.json
├── infra
│   ├── ansible
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
│   ├── temp
│   └── terraform
│       └── main.tf
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.dev.txt
├── scripts
│   └── add_inits.py
├── src
│   ├── app
│   │   ├── ai
│   │   │   ├── client.py
│   │   │   ├── __init__.py
│   │   │   ├── prompts.py
│   │   │   ├── services
│   │   │   │   ├── audio_service.py
│   │   │   │   ├── chat_service.py
│   │   │   │   └── __init__.py
│   │   │   └── tools
│   │   │       ├── evaluate_toefl.py
│   │   │       └── __init__.py
│   │   ├── alembic.ini
│   │   ├── api
│   │   │   ├── deps
│   │   │   │   ├── __init__.py
│   │   │   │   └── user.py
│   │   │   ├── __init__.py
│   │   │   └── routes
│   │   │       ├── __init__.py
│   │   │       ├── question.py
│   │   │       └── user.py
│   │   ├── bot
│   │   │   ├── dp.py
│   │   │   ├── handlers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── question_handler.py
│   │   │   │   ├── start_handler.py
│   │   │   │   └── voice_handler.py
│   │   │   ├── __init__.py
│   │   │   └── middlewares
│   │   │       ├── auth_middleware.py
│   │   │       ├── database_session_middleware.py
│   │   │       ├── __init__.py
│   │   │       └── user_data_middleware.py
│   │   ├── config.py
│   │   ├── consumers
│   │   │   ├── audio_consumer.py
│   │   │   └── __init__.py
│   │   ├── crud
│   │   │   ├── __init__.py
│   │   │   ├── media_crud.py
│   │   │   ├── question_crud.py
│   │   │   ├── user_answers_crud.py
│   │   │   ├── user_crud.py
│   │   │   └── user_quota_crud.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── messaging
│   │   │   ├── broker.py
│   │   │   └── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── schema.py
│   │   ├── requirements.txt
│   │   ├── schemas
│   │   │   ├── audio_schema.py
│   │   │   ├── __init__.py
│   │   │   ├── question_schema.py
│   │   │   ├── toefl_schema.py
│   │   │   └── user_schema.py
│   │   ├── services
│   │   │   ├── answers_service.py
│   │   │   ├── audio_processing.py
│   │   │   ├── audio_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── download_service.py
│   │   │   ├── __init__.py
│   │   │   ├── media_service.py
│   │   │   ├── question_manager.py
│   │   │   ├── question_service.py
│   │   │   └── upload_service.py
│   │   └── utils
│   │       ├── database.py
│   │       └── __init__.py
│   ├── bytewax
│   │   ├── config.py
│   │   ├── Dockerfile
│   │   ├── main2.py
│   │   ├── main.py
│   │   ├── processors
│   │   │   ├── aggregators.py
│   │   │   ├── deserialize.py
│   │   │   ├── filters.py
│   │   │   └── text_processing.py
│   │   ├── requirements.txt
│   │   └── sinks.py
│   └── worker
│       ├── consumers
│       │   └── audio_consumer.py
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── temp
└── tests
    └── app
        └── services

65 directories, 142 files
