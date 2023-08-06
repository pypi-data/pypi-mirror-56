import click

from .invalidate import invalidate
from .run import run
from .server import server


@click.group()
def main():
    pass


main.add_command(run)
main.add_command(invalidate)
main.add_command(server)
