import clickhouse_connect

from bytewax.outputs import DynamicSink, StatelessSinkPartition
from config import (
    CLICKHOUSE_DB,
    CLICKHOUSE_HOST,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
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
            print("Inserting batch to ClickHouse:", items)
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
            print(f"Warning: failed to disconnect ClickHouse client cleanly: {e}")


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
