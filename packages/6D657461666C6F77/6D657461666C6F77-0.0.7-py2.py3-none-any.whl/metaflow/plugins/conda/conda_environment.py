import json
import os
import sys
import tarfile

from metaflow.environment import MetaflowEnvironment
from metaflow.exception import MetaflowException
from .conda import Conda

from . import get_conda_manifest_path, CONDA_MAGIC_FILE


class CondaEnvironment(MetaflowEnvironment):
    TYPE = 'conda'
    _filecache = None

    def __init__(self, flow):
        self.flow = flow

    def init_environment(self, logger):
        # Print a message for now
        logger("Bootstrapping conda environment...(this could take a few minutes)")

    def decospecs(self):
        # Apply conda decorator to all steps
        return ('conda', )

    def _get_conda_decorator(self, step_name):
        step = next(step for step in self.flow if step.name == step_name)
        decorator = next(deco for deco in step.decorators if deco.name == 'conda')
        # Guaranteed to have a conda decorator because of self.decospecs()
        return decorator

    def _get_env_id(self, step_name):
        conda_decorator = self._get_conda_decorator(step_name)
        if conda_decorator.is_enabled():
            return conda_decorator._env_id()
        return None

    def _get_executable(self, step_name):
        env_id = self._get_env_id(step_name)
        if env_id is not None:
            return (os.path.join("/metaflow/conda", "envs", env_id, "bin/python -s"))
        return None

    def bootstrap_commands(self, step_name):
        # Bootstrap conda and execution environment for step
        env_id = self._get_env_id(step_name)
        if env_id is not None:
            return [
                    "echo \'Bootstrapping environment.\'",
                    "python -m metaflow.plugins.conda.batch_bootstrap %s" % env_id,
                    "echo \'Environment bootstrapped.\'"
                ]
        return []

    def add_to_package(self):
        # Add conda manifest file to job package at the top level.
        path = get_conda_manifest_path()
        if os.path.exists(path):
            return [(path, os.path.basename(path))]
        else:
            return []

    def pylint_config(self):
        # Disable (import-error) in pylint
        return ["--disable=F0401"]

    def executable(self, step_name):
        # Get relevant python interpreter for step
        executable = self._get_executable(step_name)
        if executable is not None:
            return executable
        return super(CondaEnvironment, self).executable(step_name)

    @classmethod
    def get_client_info(cls, flow_name, metadata):
        if cls._filecache is None:
            from metaflow.client.filecache import FileCache
            cls._filecache = FileCache()
        info = metadata.get('code-package')
        env_id = metadata.get('conda_env_id')
        if info is None or env_id is None:
            return "Conda environment (no additional information)"
        info = json.loads(info)
        with cls._filecache.get_data(info['ds_type'], flow_name, info['sha']) as f:
            tar = tarfile.TarFile(fileobj=f)
            conda_file = tar.extractfile(CONDA_MAGIC_FILE)
            if conda_file is None:
                return "Conda environment (no conda information file)"
            info = json.loads(conda_file.read().decode('utf-8'))
        new_info = {
            'type': 'Conda',
            'explicit': info[env_id]['explicit'],
            'deps': info[env_id]['deps']}
        return new_info
