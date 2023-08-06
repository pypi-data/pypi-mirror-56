import errno
import os
import sys
from pathlib import Path

import wrapt

ERROR_INVALID_NAME = 123


def is_subdirectory(path, *candidates):
    return any([Path(path) in Path(x).parents for x in candidates])


def is_valid_path(path):
    try:
        if not isinstance(path, str) or not path:
            return False
        _, path = os.path.splitdrive(path)
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in path.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError:
        return False
    else:
        return True


def coerce_pathlib(*path_indexes):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        args = [Path(x) if i in path_indexes else x for i, x in enumerate(args)]
        return wrapped(*args, **kwargs)
    return wrapper


def coerce_string(*path_indexes):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        args = [str(x) if i in path_indexes else x for i, x in enumerate(args)]
        return wrapped(*args, **kwargs)
    return wrapper


@coerce_pathlib(0)
def depth_to_end(path):
    deepest = 0
    start_depth = len(path.parents)
    for dirpath, dirnames, filenames in os.walk(str(path)):
        if not filenames:
            continue
        file_path = Path(dirpath) / Path(filenames[0])
        total_depth = len(file_path.parents)
        relative_depth = total_depth - start_depth
        if relative_depth > deepest:
            deepest = relative_depth
    return deepest


@coerce_pathlib(0)
def depth_from_start(path):
    return len(path.parents)
