from .local_target import LocalTarget


def _error_target(target, package):
    def __init__(self, *args, **kwargs):
        raise Exception(f'Please install {package} to use {target}.')

    return type(target, tuple(), {'__init__': __init__})


try:
    from .numpy import LocalNpz, LocalNpy
except ImportError:
    LocalNpy = _error_target('LocalNpy', 'numpy')
    LocalNpz = _error_target('LocalNpz', 'numpy')

try:
    from .pandas import LocalPandasPickle, LocalPandasCSV
except ImportError:
    LocalPandasPickle = _error_target('LocalPandasPickle', 'pandas')
    LocalPandasCSV = _error_target('LocalPandasCSV', 'pandas')

try:
    from .tifffile import LocalTiff
except ImportError:
    LocalTiff = _error_target('LocalTiff', 'tifffile')
