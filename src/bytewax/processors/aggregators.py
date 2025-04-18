from collections import deque


def unique_words_builder():
    def update(state, value):
        rec, new_words = value
        state = state or set()
        state.update(new_words)
        return state, len(state)

    return update


def sliding_avg_builder(n):
    def update(state, value):
        buf = state or deque(maxlen=n)
        buf.append(value)
        avg = sum(buf) / len(buf)
        return buf, avg

    return update
