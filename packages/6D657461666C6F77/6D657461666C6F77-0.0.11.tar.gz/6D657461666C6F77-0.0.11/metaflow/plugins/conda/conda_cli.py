import click

from .conda import Conda


@click.group()
def cli():
    pass


@cli.group(help='Commands related to Conda environment.')
@click.pass_obj
def conda(obj):
    pass

@conda.command(help='Resolve Conda environments for the flow.')
@click.argument('step-to-resolve',
                required=False)
@click.option('--force/--not-force',
              show_default=True,
              default=False,
              help='Force resolution of Conda environment.')
@click.pass_obj
def resolve(obj,
            step_to_resolve=None,
            force=False):
    obj.environment.init_environment(obj.logger)
    for step in obj.flow:
        if step_to_resolve is None or step.__name__ == step_to_resolve:
            for deco in step.decorators:
                if deco.name == "conda":
                    obj.echo("Resolving for step %s.." % step.__name__, fg='yellow', bold=False)
                    env_id = deco._resolve_step_environment(obj.datastore.datastore_root, force=force)
                    obj.echo("Using/Generated Conda environment %s" % (env_id), fg='yellow', indent=True, bold=False)