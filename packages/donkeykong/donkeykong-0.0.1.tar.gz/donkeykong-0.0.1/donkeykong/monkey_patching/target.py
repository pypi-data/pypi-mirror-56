import luigi


def remove(self):
    raise NotImplementedError(f'Remove method is not implemented in {self.__class__.__name__}.')


# Monkey patching
luigi.Target.remove = remove
luigi.Target.protected = False
luigi.Target.open = lambda self: self
luigi.Target.close = lambda self: None
luigi.Target.__enter__ = lambda self: self.open()
luigi.Target.__exit__ = lambda self, exc_type, exc_val, exc_tb: self.close()
luigi.Target.__del__ = lambda self: self.close()
