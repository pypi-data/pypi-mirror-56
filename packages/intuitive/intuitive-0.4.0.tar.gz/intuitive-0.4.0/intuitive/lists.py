import collections


def first(l, default=None):
    for e in l:
        return e
    return default


def last(l, default=None):
    for e in l[::-1]:
        return e
    return default


def nth(l, n, default=None):
    for i, e in enumerate(l):
        if i == n:
            return e
    return default


def sort(l, descending=False):
    return sorted(l, reverse=descending)


def sort_by_nth(l, n, descending=False):
    return sorted(l, key=lambda x: x[n], reverse=descending)


def sort_by_func(l, func, descending=True):
    return sorted(l, key=func, reverse=descending)


def sort_by_attribute(l, name, descending=False):
    return sorted(l, key=lambda x: getattr(x, name), reverse=descending)


def sort_by_method(l, name, descending=False):
    return sorted(l, key=lambda x: getattr(x, name)(), reverse=descending)


def frequency_dict(l):
    return collections.Counter(l)
