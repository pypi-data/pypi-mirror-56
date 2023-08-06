import click
from luigi.cmdline import luigi_run


@click.command(context_settings={'ignore_unknown_options': True})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(args):
    """A wrapper around luigi CLI."""
    luigi_run(args)
