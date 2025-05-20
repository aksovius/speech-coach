import re
from collections import Counter
from datetime import datetime, timezone

import nltk
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))


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


lemmatizer = WordNetLemmatizer()


# Функция преобразования POS из nltk → wordnet
def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # по умолчанию


def lemmatize_text(message):
    text = message["asr_transcript"]
    user_id = int(message["user_id"])

    timestamp = datetime.fromtimestamp(
        message["created_at"] / 1_000_000, tz=timezone.utc
    )

    tokens = wordpunct_tokenize(text.lower())
    pos_tags = pos_tag(tokens)
    lemmas = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        for word, tag in pos_tags
        if word.isalpha() and word not in stop_words
    ]

    lemma_counts = Counter(lemmas)

    return [
        {"user_id": user_id, "timestamp": timestamp, "word": word, "count": count}
        for word, count in lemma_counts.items()
    ]
