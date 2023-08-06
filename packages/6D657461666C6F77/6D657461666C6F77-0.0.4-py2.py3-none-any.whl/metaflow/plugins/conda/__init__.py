import errno
import os
import json
import fcntl

from metaflow.metaflow_config import DATASTORE_SYSROOT_LOCAL

CONDA_MAGIC_FILE = 'conda.cnd'


def get_conda_manifest_path():
    return os.path.join(DATASTORE_SYSROOT_LOCAL, CONDA_MAGIC_FILE)


def read_conda_manifest():
    path = get_conda_manifest_path()
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path) as f:
            return json.load(f)
    else:
        return {}


def write_to_conda_manifest(key, value):
    path = get_conda_manifest_path()
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as x:
        if x.errno != errno.EEXIST:
            raise
    with os.fdopen(os.open(path, os.O_RDWR | os.O_CREAT), 'r+') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            data = {}
            if os.path.getsize(path) > 0:
                f.seek(0)
                data = json.load(f)
            data[key] = value
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        except IOError as e:
            if e.errno != errno.EAGAIN:
                raise
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)