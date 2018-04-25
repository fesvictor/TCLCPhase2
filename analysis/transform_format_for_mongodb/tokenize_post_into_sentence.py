import re


def tokenize_post_into_sentence(value):
    return [x for x in re.split(r"[.?。]+", value) if len(x) > 0]
