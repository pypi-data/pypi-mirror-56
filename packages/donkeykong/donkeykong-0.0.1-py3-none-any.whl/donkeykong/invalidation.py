from collections import defaultdict

from luigi.task import flatten
from luigi.tools import deps
from tabulate import tabulate


def invalidate(task):
    """Invalidates a task output.

    Outputs must implement an exists and remove method."""
    outputs = flatten(task.output())
    for output in outputs:
        if not output.protected and output.exists():
            output.remove()


def downstream_dependencies(end_task, starting_tasks=None):
    """Invalidates all downstream tasks.

    :param end_task: Iterable of task objects.
    :param starting_tasks: String or iterable of task family name strings.
    """
    if starting_tasks is None:
        starting_tasks = [None]
    else:
        starting_tasks = flatten(starting_tasks)

    for task_to_invalidate in starting_tasks:
        for dep in deps.find_deps(end_task, task_to_invalidate):
            yield dep


def invalidate_downstream(end_task, tasks_to_invalidate):
    """Invalidates all downstream tasks.

    :param end_task: Iterable of task objects.
    :param tasks_to_invalidate: String or iterable of task family name strings.
    """
    for task in downstream_dependencies(end_task, starting_tasks=tasks_to_invalidate):
        invalidate(task)


def invalidate_stats(end_task, tasks_to_invalidate):
    def stats():
        return [0, 0]

    tasks_stats = defaultdict(stats)
    for task in downstream_dependencies(end_task, starting_tasks=tasks_to_invalidate):
        key = 0 if task.complete() else 1
        tasks_stats[task.task_family][key] += 1
    tasks_stats = [(key, *value) for key, value in tasks_stats.items()]
    return tabulate(tasks_stats, headers=['Task', 'Complete', 'Incomplete'])
