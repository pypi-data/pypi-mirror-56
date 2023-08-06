import os
from pathlib import Path


def size(path, default=None):
    if Path(path).is_dir():
        return directory_size(path)
    if Path(path).is_file():
        return file_size(path)
    return default


def file_size(path):
    return os.stat(path).st_size


def directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def created_at(path):
    return int(os.stat(path).st_ctime)


def modified_at(path):
    return int(os.stat(path).st_mtime)


def accessed_at(path):
    return int(os.stat(path).st_atime)


def file_statistics(path):
    return os.stat(path)
