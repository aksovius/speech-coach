def output_builder(worker_index, worker_count):
    def send(item):
        print("[Bytewax Output]", item)
    return send
