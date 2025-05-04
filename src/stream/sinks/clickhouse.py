import os

import clickhouse_connect
from bytewax.outputs import DynamicSink, StatelessSinkPartition

from shared.logging import get_log_level, setup_logger
from stream.config import (
    CLICKHOUSE_DB,
    CLICKHOUSE_HOST,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
)

# Configure logger with Loki formatter
logger = setup_logger(
    name="stream.clickhouse",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="stream.sinks.clickhouse",
    use_loki=True,
)


class ClickHouseSinkPartition(StatelessSinkPartition):
    def __init__(
        self,
        host,
        column_names,
        table,
        database,
        username="default",
        password="",
        port=8123,
        secure=False,
    ):
        self.client = clickhouse_connect.get_client(
            host=host, port=port, username=username, password=password, secure=secure
        )
        self.table = table
        self.database = database
        self.colum_names = column_names

    def write_batch(self, items):
        if items:
            logger.info(
                "Inserting batch to ClickHouse",
                extra={
                    "event": "db_insert",
                    "table": f"{self.database}.{self.table}",
                    "batch_size": len(items),
                },
            )
            self.client.insert(
                database=self.database,
                table=self.table,
                column_names=self.colum_names,
                data=items,
            )

    def close(self):
        try:
            self.client.disconnect()
        except Exception as e:
            logger.warning(
                "Failed to disconnect ClickHouse client cleanly",
                extra={
                    "event": "db_disconnect_warning",
                    "error": str(e),
                },
            )


class ClickHouseSink(DynamicSink):
    def __init__(
        self,
        table,
        column_names,
        host=CLICKHOUSE_HOST,
        database=CLICKHOUSE_DB,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        port=CLICKHOUSE_PORT,
        secure=False,
    ):
        self.host = host
        self.table = table
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.secure = secure
        self.column_names = column_names

    def build(self, step_id, worker_index, worker_count):
        return ClickHouseSinkPartition(
            host=self.host,
            table=self.table,
            database=self.database,
            username=self.username,
            password=self.password,
            port=self.port,
            secure=self.secure,
            column_names=self.column_names,
        )
