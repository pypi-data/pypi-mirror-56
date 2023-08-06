import functools
import json
from multiprocessing import Pool
import os
import tarfile
import shutil
import subprocess
import sys

from metaflow.datatools import S3
from metaflow.metaflow_config import DATASTORE_SYSROOT_LOCAL
from . import CONDA_MAGIC_FILE


def bootstrap_environment(env_id):
    setup_conda_manifest()
    download_conda_packages(env_id)
    install_conda_environment(env_id)

def setup_conda_manifest():
    manifest_folder = os.path.join(os.getcwd(), DATASTORE_SYSROOT_LOCAL)
    if not os.path.exists(manifest_folder):
        os.makedirs(manifest_folder)
    shutil.move(os.path.join(os.getcwd(), CONDA_MAGIC_FILE), 
        os.path.join(manifest_folder, CONDA_MAGIC_FILE))

def download_conda_packages(env_id):
    pkgs_folder = os.path.join(os.getcwd(), "pkgs")
    if not os.path.exists(pkgs_folder):
        os.makedirs(pkgs_folder)
    manifest_folder = os.path.join(os.getcwd(), DATASTORE_SYSROOT_LOCAL)
    with open(os.path.join(manifest_folder, CONDA_MAGIC_FILE)) as f:
        cache_urls = json.load(f)[env_id]['cache_urls']
        with S3() as s3:
            for pkg in s3.get_many(cache_urls):
                shutil.move(pkg.path, os.path.join(pkgs_folder, os.path.basename(pkg.key)))

def install_conda_environment(env_id):
    args = [
        "cd %s" % (os.path.join(os.getcwd(), "pkgs")),
        "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh  >/dev/null 2>&1",
        "bash ~/miniconda.sh -b -p %s  >/dev/null 2>&1" % (os.path.join(os.getcwd(), "conda")),
        "%s/bin/conda create --verbose --yes --offline --no-default-packages --name %s --no-deps $(ls -p | grep -v / | tr '\n' ' ') >/dev/null 2>&1" % (os.path.join(os.getcwd(), "conda"), env_id),
        "cd %s" % (os.getcwd())
    ]
    os.system(" && ".join(args))

if __name__ == "__main__":
    bootstrap_environment(sys.argv[1])