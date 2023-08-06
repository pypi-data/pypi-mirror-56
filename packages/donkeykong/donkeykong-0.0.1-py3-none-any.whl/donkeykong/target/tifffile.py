from tifffile import TiffFile

from .local_target import LocalTarget


class LocalTiff(LocalTarget):
    tif = None

    def open(self):
        self.tif = TiffFile(self.path)
        return self

    def close(self):
        if self.tif is not None:
            self.tif.close()

    def __len__(self):
        return len(self.tif.pages)

    @property
    def shape(self):
        return (len(self), *self.tif.pages[0].shape)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.tif.asarray(key=item[0])[item]
        else:
            return self.tif.asarray()[item]
