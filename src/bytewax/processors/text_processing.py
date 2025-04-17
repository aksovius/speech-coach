import re

def extract_words(rec):
    text = rec["asr_transcript"].lower()
    words = set(re.findall(r"\b\w+\b", text))
    return rec, words

def normalize_text(rec):
    # cleaning up
    rec["asr_transcript"] = rec["asr_transcript"].strip()
    return rec
