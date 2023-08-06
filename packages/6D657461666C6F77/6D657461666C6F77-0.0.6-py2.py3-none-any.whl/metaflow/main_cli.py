import click
import json
import os
import shutil

from os.path import expanduser


def makedirs(path):
    # This is for python2 compatibility.
    # Python3 has os.makedirs(exist_ok=True).
    try:
        os.makedirs(path)
    except OSError as x:
        if x.errno == 17:
            return
        else:
            raise

@click.group()
def main():
    pass

@main.group(help='Commands related to examples in metaflow.')
def examples():
    pass

def get_examples_dir():
    metaflow_dir = os.path.dirname(__file__)
    package_dir = os.path.dirname(metaflow_dir)
    examples_dir = os.path.join(package_dir, 'examples')

    return examples_dir

@examples.command(help='List all examples.')
def list():
    click.echo('Listing all available metaflow examples:')
    for name in os.listdir(get_examples_dir()):
        # Skip hidden files (like .gitignore)
        if not name.startswith('.'):
            click.echo('* {0}'.format(name))

@examples.command(help='Pull an example into your current working directory.')
@click.argument('example')
def pull(example):
    examples_dir = get_examples_dir()

    dst_dir = os.path.join(os.getcwd(), 'metaflow-examples', example)

    # Check if example has already been pulled before.
    if os.path.exists(dst_dir):
        if click.confirm('Example \"{0}\" has already been pulled before. '
                         'Do you wish to delete the existing version?'
                         ''.format(example), abort=True):
            shutil.rmtree(dst_dir)
    click.echo('Pulling example \"{0}\" into your current working '
               'directory.'.format(example))
    # Create destination `metaflow-examples` dir.
    makedirs(os.path.dirname(dst_dir))

    # Copy from (local) metaflow package dir.
    src_dir = os.path.join(examples_dir, example)
    if not os.path.exists(src_dir):
        raise click.BadArgumentUsage(\
            'Example \"{0}\" does not exist. Please run `metaflow examples list`'
            ' to see a list of valid example names.'.format(example))
    shutil.copytree(src_dir, dst_dir)

    # TODO: Should we also display how to run the example on stdout?
    click.echo('Pull successful.')


METAFLOW_CONFIGURATION_DIR = expanduser(os.environ.get('METAFLOW_HOME', '~/.metaflow'))


@main.group(help='Commands related to configuring (remote) environments.')
def configure():
    makedirs(METAFLOW_CONFIGURATION_DIR)

def persist_env(env_dict, profile):
    #print('Persisting for profile:', profile, 'env_dict:', env_dict)
    config_file = 'config.json' if not profile else ('config_%s.json' % profile)
    path = os.path.join(METAFLOW_CONFIGURATION_DIR, config_file)

    click.echo('Writing configuration to: %s' % path)
    with open(path, 'w') as f:
        json.dump(env_dict, f)

@configure.command(help='Configure environment for using metaflow sandbox.')
@click.option('--profile', '-p', default='',
              help="Optional profile under which this configuration would be stored. "
                   "Please export `METAFLOW_PROFILE` if you want access a specific profile.")
def sandbox(profile):
    click.echo('Configuring sandbox environment.')
    # Prompt for user input.
    encoded_bytes = click.prompt('Please enter the magic string you received for your sandbox',
                                 type=bytes)
    # Decode the bytes to env_dict.
    json_str = base64.b64decode(encoded_bytes).decode()
    env_dict = json.loads(json_str)
    # Persist to a file.
    persist_env(env_dict, profile)

@configure.command(help='Configure environment for using your own AWS account.')
@click.option('--profile', '-p', default='',
              help="Optional profile under which this configuration would be stored. "
                   "Please export `METAFLOW_PROFILE` if you want access a specific profile.")
def aws(profile):
    click.echo('Configuring aws environment.')

    if click.confirm('Have you run `aws configure` already?'):
        datastore_s3_root = click.prompt('Please enter AWS S3 bucket prefix to use')
        batch_job_queue = click.prompt('Please enter AWS Batch job queue to use')
        batch_s3_iam_role = click.prompt('Please enter IAM Role for ECS -> S3 access for Batch')
        mli_endpoint_url = click.prompt(
            'Please enter the endpoint for your metadata service (or leave blank)', default='', show_default=False)
        env_dict = {
                    'METAFLOW_DATASTORE_SYSROOT_S3': datastore_s3_root,
                    'METAFLOW_BATCH_JOB_QUEUE': batch_job_queue,
                    'METAFLOW_ECS_S3_ACCESS_IAM_ROLE': batch_s3_iam_role,
                    'METAFLOW_SERVICE_ENDPOINT_URL': mli_endpoint_url
                   }
        persist_env(env_dict, profile)
    else:
        click.echo('Please run it to setup AWS configuration and credentials.')
