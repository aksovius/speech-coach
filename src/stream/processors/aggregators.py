from collections import deque


# Function to initialize and update unique words state
def unique_words_builder():
    def update(state, value):
        # value - this is (data, new_words) from extract_words
        try:
            data, new_words = value
        except (TypeError, ValueError):
            # print(f"Error unpacking value in update: {e}, value: {value}")
            return state or set(), 0
        # Initialize state as an empty set
        state = state or set()
        # Check that new_words is a set
        if not isinstance(new_words, set):
            # print(f"Unexpected new_words type: {type(new_words)}, value: {new_words}")
            return state, 0
        # Add new words
        state.update(new_words)
        # Return state and number of unique words
        return state, len(state)

    return update


def sliding_avg_builder(n):
    """
    Returns a stateful_map updater function:
    - state is a deque of the last n values
    - value is a new value (number of unique words in the current message)
    The function returns (new_state, average_over_buffer).
    """

    def update(state, value):
        # Initialize deque if it doesn't exist
        buf = state or deque(maxlen=n)
        # value is the number of unique words
        buf.append(value)
        # Calculate average: sum(buf)/len(buf)
        avg = sum(buf) / len(buf)
        return buf, avg

    return update
