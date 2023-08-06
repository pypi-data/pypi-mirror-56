from luigi import Task, Target
from luigi import task
from luigi.tools import deps


def flatten(struct):
    """
    Creates a flat list of all items in structured output (dicts, lists, items):

    .. code-block:: python

        >>> sorted(flatten({'a': 'foo', 'b': 'bar'}))
        ['bar', 'foo']
        >>> sorted(flatten(['foo', ['bar', 'troll']]))
        ['bar', 'foo', 'troll']
        >>> flatten('foo')
        ['foo']
        >>> flatten(42)
        [42]
    """
    if struct is None:
        return []
    flat = []
    if isinstance(struct, dict):
        for _, result in struct.items():
            flat += flatten(result)
        return flat
    if isinstance(struct, (str, Task, Target)):
        return [struct]

    try:
        # if iterable
        iterator = iter(struct)
    except TypeError:
        return [struct]

    for result in iterator:
        flat += flatten(result)
    return flat


def get_task_requires(task):
    """Returns task requirements.

    Standard implementation in luigi.tools.deps doesn't include subtasks,
    as they are not considered a requirement.
    """
    if hasattr(task, 'subtasks'):
        return set(flatten(task.requires()) + flatten(task.subtasks()))
    else:
        return set(flatten(task.requires()))


# Monkey patching
task.flatten = flatten
deps.get_task_requires = get_task_requires
