import numpy as np

from .local_target import LocalTarget


class LocalNpy(LocalTarget):
    def open(self, mode='r'):
        return np.load(self.path, mmap_mode=mode)

    def save(self, array):
        np.save(self.path, array)


class LocalNpz(LocalTarget):
    npz = None

    def open(self, mode='r'):
        self.npz = np.load(self.path, allow_pickle=True)
        return self.npz

    def close(self):
        self.npz.close()

    def save(self, *args, **kwargs):
        np.savez(self.path, *args, **kwargs)
