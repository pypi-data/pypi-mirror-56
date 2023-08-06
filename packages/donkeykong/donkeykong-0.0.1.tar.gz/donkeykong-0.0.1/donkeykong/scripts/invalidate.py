import click
from luigi.cmdline_parser import CmdlineParser

from ..invalidation import invalidate_stats, invalidate_downstream


@click.option('--yes', is_flag=True, help='Invalidate without asking for confirmation.')
@click.option('--invalidate', 'tasks_to_invalidate', help='Tasks to invalidate.')
@click.option('--module', help='Used for dynamic loading of modules.')
@click.argument('end_task')
@click.command()
def invalidate(end_task, module=None, tasks_to_invalidate=None, yes=False):
    """Invalidate specified task."""
    cmdline_parser_args = ['--module', module, end_task] if module is not None else [end_task]
    end_task = CmdlineParser(cmdline_parser_args).get_task_obj()
    stats = invalidate_stats(end_task, tasks_to_invalidate)
    click.echo(stats)
    if yes or click.confirm('Do you want to continue?', abort=True):
        invalidate_downstream(end_task, tasks_to_invalidate)
        click.echo('Done.')
