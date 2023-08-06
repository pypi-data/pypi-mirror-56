import click
import json
import os
import shutil

from os.path import expanduser

from metaflow.datastore.local import LocalDataStore
from metaflow.metaflow_config import DATASTORE_LOCAL_DIR


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

def echo_dev_null(*args, **kwargs):
    pass

def echo_always(line, **kwargs):
    click.secho(line, **kwargs)

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    global echo
    echo = echo_always

    import metaflow
    echo('Metaflow ',
         fg='magenta',
         bold=True,
         nl=False)

    if ctx.invoked_subcommand is None:
        echo('(%s): ' % metaflow.__version__,
             fg='magenta',
             bold=False,
             nl=False)
    else:
        echo('(%s)\n' % metaflow.__version__,
             fg='magenta',
             bold=False)

    if ctx.invoked_subcommand is None:
        echo("Metaflow is a microframework "\
             "for Data Science projects.\n",
             fg='magenta')

        # metaflow URL
        echo('https://metaflow.org', fg='cyan', nl=False)
        echo('  - Find the documentation')

        # metaflow help email
        echo('help@metaflow.org', fg='cyan', nl=False)
        echo('     - Reach out for help\n')

        # print a short list of next steps.
        short_help = {'tutorials': 'Browse and access metaflow tutorials.',
                      'configure': 'Configure metaflow to run remotely.',
                      'help': 'Shows all available commands to run.'}

        echo('Commands:', bold=False, nl=True)

        for cmd, desc in short_help.items():
            echo('  metaflow {0:<10} '.format(cmd),
                 fg='cyan',
                 bold=False,
                 nl=False)

            echo('%s' % desc)

@main.command(help='Show all available commands.')
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())

@main.command(help='Shows flows accessible from the current working tree.')
def status():
    from metaflow.client import namespace, metadata, Metaflow

    # Get the local data store path
    path = LocalDataStore.get_datastore_root_from_config(echo,
                                                         create_on_absent=False)
    # Throw an exception
    if path is None:
        raise click.ClickException("Could not find " +\
                                   click.style('"%s"' % DATASTORE_LOCAL_DIR,
                                               fg='red') +\
                                   " in the current working tree.")

    stripped_path = os.path.dirname(path)
    namespace(None)
    metadata('local@%s' % stripped_path)
    echo('Working tree found at: ', nl=False)
    echo('"%s"\n' % stripped_path, fg='cyan')
    echo('Available flows:', fg='cyan', bold=True)
    for flow in Metaflow():
        echo('* %s' % flow, fg='cyan')

@main.group(help="Browse and access the metaflow tutorial episodes.")
def tutorials():
    pass

def get_tutorials_dir():
    metaflow_dir = os.path.dirname(__file__)
    package_dir = os.path.dirname(metaflow_dir)
    tutorials_dir = os.path.join(package_dir, 'metaflow', 'tutorials')

    return tutorials_dir

def get_tutorial_metadata(tutorial_path):
    metadata = {}
    with open(os.path.join(tutorial_path, 'README.md')) as readme:
        content =  readme.read()

    paragraphs = [paragraph.strip() \
                  for paragraph \
                  in content.split('#') if paragraph]
    metadata['description'] = paragraphs[0].split('**')[1]
    header = paragraphs[0].split('\n')
    header = header[0].split(':')
    metadata['episode'] = header[0].strip()[len('Episode '):]
    metadata['title'] = header[1].strip()

    for paragraph in paragraphs[1:]:
        if paragraph.startswith('Before playing'):
            lines = '\n'.join(paragraph.split('\n')[1:])
            metadata['prereq'] = lines.replace('```', '')

        if paragraph.startswith('Showcasing'):
            lines = '\n'.join(paragraph.split('\n')[1:])
            metadata['showcase'] = lines.replace('```', '')

        if paragraph.startswith('To play'):
            lines = '\n'.join(paragraph.split('\n')[1:])
            metadata['play'] = lines.replace('```', '')

    return metadata

def get_all_episodes():
    episodes = []
    for name in sorted(os.listdir(get_tutorials_dir())):
        # Skip hidden files (like .gitignore)
        if not name.startswith('.'):
            episodes.append(name)
    return episodes

@tutorials.command(help="List the available episodes.")
def list():
    echo('Episodes:', fg='cyan', bold=True, nl=True)
    for name in get_all_episodes():
        path = os.path.join(get_tutorials_dir(), name)
        metadata = get_tutorial_metadata(path)
        echo('* {0: <18} '.format(metadata['episode']),
             fg='cyan',
             nl=False)
        echo('- {0}'.format(metadata['title']))

    echo('\nTo pull your favorite episode(s), type: ', nl=True)
    echo('metaflow tutorials pull [EPISODES]', fg='cyan')

def validate_episode(episode):
    src_dir = os.path.join(get_tutorials_dir(), episode)
    if not os.path.exists(src_dir):
        raise click.BadArgumentUsage("Episode " + \
                                     click.style("\"{0}\"".format(episode),
                                                 fg='red') + " does not exist."\
                                     " To see a list of available episodes, "\
                                     "type:\n" + \
                                     click.style("metaflow tutorials list",
                                                 fg='cyan'))

def autocomplete_episodes(ctx, args, incomplete):
    return [k for k in get_all_episodes() if incomplete in k]

@tutorials.command(help="Pull episode(s) "\
                   "into your current working directory.")
@click.argument('episode', nargs=-1, autocompletion=autocomplete_episodes)
def pull(episode):
    episodes = episode
    tutorials_dir = get_tutorials_dir()

    if len(episodes) == 0:
        episodes = get_all_episodes()
    else:
        # Validate that the list is valid.
        for episode in episodes:
            validate_episode(episode)
    # Create destination `metaflow-tutorials` dir.
    dst_parent = os.path.join(os.getcwd(), 'metaflow-tutorials')
    makedirs(dst_parent)

    # Pull specified episodes.
    for episode in episodes:
        dst_dir = os.path.join(dst_parent, episode)
        # Check if episode has already been pulled before.
        if os.path.exists(dst_dir):
            if click.confirm("Episode " + \
                             click.style("\"{0}\"".format(episode), fg='red') +\
                             " has already been pulled before. Do you wish "\
                             "to delete the existing version?"):
                shutil.rmtree(dst_dir)
            else:
                continue
        echo('Pulling episode ', nl=False)
        echo('\"{0}\"'.format(episode), fg='cyan', nl=False)
        # TODO: Is the following redudant?
        echo(' into your current working directory.')
        # Copy from (local) metaflow package dir to current.
        src_dir = os.path.join(tutorials_dir, episode)
        shutil.copytree(src_dir, dst_dir)

    echo('\nTo know more about an episode, type:\n', nl=False)
    echo('metaflow tutorials info [EPISODE]', fg='cyan')

@tutorials.command(help='Find out more about an episode.')
@click.argument('episode', autocompletion=autocomplete_episodes)
def info(episode):
    validate_episode(episode)
    src_dir = os.path.join(get_tutorials_dir(), episode)
    metadata = get_tutorial_metadata(src_dir)
    echo('Synopsis:', fg='cyan', bold=True, nl=True)
    echo('%s' % metadata['description'])

    echo('\nShowcasing:', fg='cyan', bold=True, nl=True)
    echo('%s' % metadata['showcase'])

    if 'prereq' in metadata:
        echo('\nBefore playing:', fg='cyan', bold=True, nl=True)
        echo('%s' % metadata['prereq'])

    echo('\nTo play:', fg='cyan', bold=True)
    echo('%s' % metadata['play'])

METAFLOW_CONFIGURATION_DIR = expanduser(os.environ.get('METAFLOW_HOME', '~/.metaflow'))

@main.group(help="Configure Metaflow to "\
            "run on our sandbox or an AWS account.")
def configure():
    makedirs(METAFLOW_CONFIGURATION_DIR)

def persist_env(env_dict, profile):
    #print('Persisting for profile:', profile, 'env_dict:', env_dict)
    config_file = 'config.json' if not profile else ('config_%s.json' % profile)
    path = os.path.join(METAFLOW_CONFIGURATION_DIR, config_file)

    echo('Writing configuration to: %s' % path)
    with open(path, 'w') as f:
        json.dump(env_dict, f)

@configure.command(help='Get Metaflow up and running on our sandbox.')
@click.option('--profile', '-p', default='',
              help="Optional profile under which this configuration would be stored. "
                   "Please export `METAFLOW_PROFILE` if you want access a specific profile.")
def sandbox(profile):
    echo('Configuring sandbox environment.')
    # Prompt for user input.
    encoded_bytes = click.prompt('Please enter the magic string you received for your sandbox',
                                 type=bytes)
    # Decode the bytes to env_dict.
    json_str = base64.b64decode(encoded_bytes).decode()
    env_dict = json.loads(json_str)
    # Persist to a file.
    persist_env(env_dict, profile)

@configure.command(help='Get Metaflow up and running on your own AWS environment.')
@click.option('--profile', '-p', default='',
              help="Optional profile under which this configuration would be stored. "
                   "Please export `METAFLOW_PROFILE` if you want access a specific profile.")
def aws(profile):
    echo('Configuring aws environment.')

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
                    'METAFLOW_SERVICE_URL': mli_endpoint_url
                   }
        persist_env(env_dict, profile)
    else:
        echo('Please run it to setup AWS configuration and credentials.')
