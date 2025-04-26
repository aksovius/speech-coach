import re

from nltk.tokenize import wordpunct_tokenize


def extract_words(rec):
    text = rec["asr_transcript"].lower()
    words = set(re.findall(r"\b\w+\b", text))
    return rec, words


def normalize_text(rec):
    # cleaning up
    rec["asr_transcript"] = rec["asr_transcript"].strip()
    return rec


def calculate_ttr_simple(message):
    text = message["asr_transcript"]
    tokens = wordpunct_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    total_words = len(tokens)
    unique_words = len(set(tokens))
    ttr = unique_words / total_words if total_words > 0 else 0.0
    timestamp = message["created_at"] // 1_000_000  # Convert to seconds

    return [message["user_id"], timestamp, ttr, message["score_overall"]]


def calculate_ttr_from_words(words):
    """
    words: words list (list[str])
    """
    if not words:
        return 0.0

    total_words = len(words)
    unique_words = len(set(words))
    ttr = unique_words / total_words

    return ttr
