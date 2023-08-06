import errno
import os
import json
import fcntl

CONDA_MAGIC_FILE = 'conda.cnd'


def get_conda_manifest_path(ds_root):
    return os.path.join(ds_root, CONDA_MAGIC_FILE)


def read_conda_manifest(ds_root):
    path = get_conda_manifest_path(ds_root)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path) as f:
            return json.load(f)
    else:
        return {}


def write_to_conda_manifest(ds_root, key, value):
    path = get_conda_manifest_path(ds_root)
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