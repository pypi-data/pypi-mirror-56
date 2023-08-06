import os
import json
import logging
import pkg_resources
import sys


from metaflow.exception import MetaflowException

# Disable multithreading security on MacOS
if sys.platform == "darwin":
    os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"


def init_config():
    # Read configuration from $METAFLOW_HOME/<profile>.conf.
    home = os.environ.get('METAFLOW_HOME', '~/.metaflow')
    profile = os.environ.get('METAFLOW_PROFILE')
    path_to_config = os.path.join(home, 'config.json')
    if profile:
        path_to_config = os.path.join(home, 'config_%s.json' % profile)
    path_to_config = os.path.expanduser(path_to_config)
    config = {}
    if os.path.exists(path_to_config):
        with open(path_to_config) as f:
            config = json.load(f)
    elif profile:
        raise MetaflowException('Could not find profile \'%s\' (expecting it at \'%s\')' %
                                (profile, path_to_config))
    return config


# Initialize defaults required to setup environment variables.
METAFLOW_CONFIG = init_config()


def from_env(name, default=None, is_path=False):
    result = os.environ.get(name, METAFLOW_CONFIG.get(name, default))
    if result and is_path:
        return result.rstrip('/')
    return result


###
# Datastore configuration
###
# Path to the local directory to store artifacts for 'local' datastore.
# Also used for tracking 'local' metadata.
DATASTORE_SYSROOT_LOCAL = from_env('METAFLOW_DATASTORE_SYSROOT_LOCAL', '.metaflow', is_path=True)
# S3 bucket and prefix to store artifacts for 's3' datastore.
DATASTORE_SYSROOT_S3 = from_env('METAFLOW_DATASTORE_SYSROOT_S3', is_path=True)
# S3 datatools root location
DATATOOLS_S3ROOT = from_env(
    'METAFLOW_DATATOOLS_S3ROOT', '%s/data' % DATASTORE_SYSROOT_S3, is_path=True)

###
# Datastore local cache (for client access to artifacts)
###
# Path to the client cache (when fetching artifacts, artifacts are cached here)
CLIENT_CACHE_PATH = from_env('METAFLOW_CLIENT_CACHE_PATH', '/tmp/metaflow_client', is_path=True)
# Maximum size (in bytes) of the cache
CLIENT_CACHE_MAX_SIZE = from_env('METAFLOW_CLIENT_CACHE_MAX_SIZE', 10000)

###
# Metadata configuration
###
METADATA_SERVICE_URL = from_env('METAFLOW_SERVICE_ENDPOINT_URL', is_path=True)
METADATA_SERVICE_NUM_RETRIES = from_env('METAFLOW_SERVICE_RETRY_COUNT', 5)
METADATA_SERVICE_HEADERS = from_env('METAFLOW_SERVICE_HEADERS', {})


###
# AWS Batch configuration
###
# IAM role for AWS Batch container with S3 access
ECS_S3_ACCESS_IAM_ROLE = from_env('METAFLOW_ECS_S3_ACCESS_IAM_ROLE')
# Job queue for AWS Batch
BATCH_JOB_QUEUE = from_env('METAFLOW_BATCH_JOB_QUEUE')

###
# Conda plugin configuration
###
# Conda package root location on S3
CONDA_PACKAGE_S3ROOT = from_env(
    'METAFLOW_CONDA_PACKAGE_S3ROOT', '%s/conda' % DATASTORE_SYSROOT_S3, is_path=True)

###
# Debug configuration
###
DEBUG_OPTIONS = ['subcommand', 'sidecar', 's3client']

for typ in DEBUG_OPTIONS:
    vars()['METAFLOW_DEBUG_%s' % typ.upper()] = from_env('METAFLOW_DEBUG_%s' % typ.upper())

###
# AWS Sandbox configuration
###
# Boolean flag for metaflow AWS sandbox access
AWS_SANDBOX_ENABLED = bool(from_env('METAFLOW_AWS_SANDBOX_ENABLED', False))
# Metaflow AWS sandbox auth endpoint
AWS_SANDBOX_STS_ENDPOINT_URL = from_env('METAFLOW_AWS_SANDBOX_STS_ENDPOINT_URL', is_path=True)
# Metaflow AWS sandbox IAM role
AWS_SANDBOX_IAM_ROLE = from_env('METAFLOW_AWS_SANDBOX_IAM_ROLE')
# Metaflow AWS sandbox API auth key
AWS_SANDBOX_API_KEY = from_env('METAFLOW_AWS_SANDBOX_API_KEY')

if AWS_SANDBOX_ENABLED:
    METADATA_SERVICE_URL = '%s/api' % AWS_SANDBOX_STS_ENDPOINT_URL
    METADATA_SERVICE_HEADERS = {'x-api-key': AWS_SANDBOX_API_KEY}
# MAX_ATTEMPTS is the maximum number of attempts, including the first
# task, retries, and the final fallback task and its retries.
#
# Datastore needs to check all attempt files to find the latest one, so
# increasing this limit has real performance implications for all tasks.
# Decreasing this limit is very unsafe, as it can lead to wrong results
# being read from old tasks.
MAX_ATTEMPTS = 6


# the naughty, naughty driver.py imported by lib2to3 produces
# spam messages to the root logger. This is what is required
# to silence it:
class Filter(logging.Filter):
    def filter(self, record):
        if record.pathname.endswith('driver.py') and \
           'grammar' in record.msg:
            return False
        return True


logger = logging.getLogger()
logger.addFilter(Filter())


def get_version(pkg):
    return pkg_resources.get_distribution(pkg).version


# PINNED_CONDA_LIBS are the libraries that metaflow depends on for execution
# and are needed within a conda environment
def get_pinned_conda_libs():
    return {
        'click': '7.0',
        'requests': '2.22.0',
        'boto3': '1.9.235',
        'coverage': '4.5.3'
    }


cached_aws_sandbox_creds = None


def get_authenticated_boto3_session():
    from metaflow.exception import MetaflowException
    import requests
    import json
    import socket
    try:
        from boto3.session import Session
    except (NameError, ImportError):
        raise MetaflowException(
            "Could not import module 'boto3'. Install boto3 first.")

    if sys.platform != 'darwin':
        try:
            requests.get('http://169.254.169.254', timeout=0.1)
            return Session()
        except (socket.timeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
            pass

    if AWS_SANDBOX_ENABLED:
        global cached_aws_sandbox_creds
        if cached_aws_sandbox_creds is None:
            # authenticate using STS
            url = "%s/api/auth/role/token" % AWS_SANDBOX_STS_ENDPOINT_URL
            headers = {
                'Content-Type': 'text/plain',
                'x-api-key': AWS_SANDBOX_API_KEY
            }
            data = {
                "role_arn": AWS_SANDBOX_IAM_ROLE
            }
            try:
                r = requests.post(url, data=json.dumps(data), headers=headers)
                r.raise_for_status()
                cached_aws_sandbox_creds = json.loads(r.text)
            except requests.exceptions.HTTPError as e:
                raise MetaflowException(repr(e))
        return Session(**cached_aws_sandbox_creds)
    return Session()
