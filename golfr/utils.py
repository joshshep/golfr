#! /usr/bin/env python
from os import makedirs
import errno
# http://stackoverflow.com/a/5032238
def ensure_path_exists(path):
    try:
        makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise