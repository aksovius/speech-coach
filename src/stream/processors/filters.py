def filter_none(x):
    return x is not None


def filter_empty_transcript(rec):
    # rec — instance of dict
    return bool(rec.get("asr_transcript"))
