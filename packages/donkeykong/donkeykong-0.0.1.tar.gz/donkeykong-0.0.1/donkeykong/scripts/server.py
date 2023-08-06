import click
from luigi.cmdline import luigid


@click.command(context_settings={'ignore_unknown_options': True})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def server(args):
    """A wrapper around luigid CLI."""
    luigid(args)
