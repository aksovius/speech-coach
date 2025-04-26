import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER")
DEBEZIUM_TOPIC = os.environ.get("KAFKA_TOPIC")
CLEAN_WORDS_TOPIC = "clean_words"
CLICKHOUSE_HOST = "192.168.1.86"  # os.environ.get("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = 8123  # os.environ.get("CLICKHOUSE_PORT")
CLICKHOUSE_DB = "speech"  # os.environ.get("CLICKHOUSE_DB")
CLICKHOUSE_USER = "default"  # os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = ""  # os.environ.get("CLICKHOUSE_PASSWORD")
