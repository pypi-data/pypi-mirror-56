def both(a, b):
    return all([a, b])


def either(a, b):
    return any([a, b])


def neither(a, b):
    return not a and not b
