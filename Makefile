ENV_FILE=../secrets/speech-coach.env
include $(ENV_FILE)
export
up:
	docker compose --env-file $(ENV_FILE) up --build -d

down:
	docker compose down

dump:
	docker exec -t speech-db pg_dump -U $(DB_USER) $(DB_NAME) > db_dump.sql

restore:
	docker exec -i speech-db psql -U $(DB_USER) $(DB_NAME) < db_dump.sql

log-app:
	docker logs -f speech-app