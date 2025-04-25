import clickhouse_connect
from bytewax.outputs import StatelessSink, StatelessSinkPartition


class ClickHouseSinkPartition(StatelessSinkPartition):
    def __init__(self, host, database, table):
        self.client = clickhouse_connect.get_client(host=host, database=database)
        self.table = table

    def write_batch(self, items):
        if not items:
            return
        self.client.insert(self.table, items)

    def close(self):
        self.client.disconnect()


class ClickHouseSink(StatelessSink):
    def __init__(self, host, database, table):
        self.host = host
        self.database = database
        self.table = table

    def build(self, _step_id, _worker_index, _worker_count):
        return ClickHouseSinkPartition(self.host, self.database, self.table)
