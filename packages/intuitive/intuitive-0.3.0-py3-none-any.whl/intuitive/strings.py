import string


def remove_punctuation(s):
    table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return s.translate(table)


def ensure_single_spaced(s):
    return ' '.join(s.strip().split())
