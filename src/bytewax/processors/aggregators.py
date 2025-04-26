from collections import deque


# Функция для инициализации и обновления состояния уникальных слов
def unique_words_builder():
    def update(state, value):
        # value - это (data, new_words) из extract_words
        try:
            data, new_words = value
        except (TypeError, ValueError):
            # print(f"Error unpacking value in update: {e}, value: {value}")
            return state or set(), 0
        # Инициализируем состояние как пустое множество
        state = state or set()
        # Проверяем, что new_words - это множество
        if not isinstance(new_words, set):
            # print(f"Unexpected new_words type: {type(new_words)}, value: {new_words}")
            return state, 0
        # Добавляем новые слова
        state.update(new_words)
        # Возвращаем состояние и количество уникальных слов
        return state, len(state)

    return update


def sliding_avg_builder(n):
    """
    Возвращает функцию-апдейтер для stateful_map:
    - state — это deque последних n значений
    - value — это новое значение (количество уникальных слов в текущем сообщении)
    Функция возвращает (новый_state, среднее_по_buffer).
    """

    def update(state, value):
        # инициализируем deque, если его нет
        buf = state or deque(maxlen=n)
        # value — само число уникальных слов
        buf.append(value)
        # считаем среднее: sum(buf)/len(buf)
        avg = sum(buf) / len(buf)
        return buf, avg

    return update
