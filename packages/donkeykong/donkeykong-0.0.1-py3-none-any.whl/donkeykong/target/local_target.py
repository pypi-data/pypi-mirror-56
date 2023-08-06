import luigi


class LocalTarget(luigi.LocalTarget):
    """Extends luigi.LocalTarget with a protected keyword argument for invalidation purposes."""

    def __init__(self, *args, **kwargs):
        self.protected = kwargs.pop('protected', False)
        super().__init__(*args, **kwargs)
