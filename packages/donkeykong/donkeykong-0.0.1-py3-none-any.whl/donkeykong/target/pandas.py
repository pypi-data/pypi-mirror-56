import pandas as pd

from .local_target import LocalTarget


class LocalPandasPickle(LocalTarget):
    def open(self):
        return pd.read_pickle(self.path)

    def save(self, df):
        pd.to_pickle(df, self.path)


class LocalPandasCSV(LocalTarget):
    def __init__(self, *args, csv_kwargs, **kwargs):
        self.csv_kwargs = csv_kwargs
        super().__init__(*args, **kwargs)

    def open(self):
        return pd.read_csv(self.path, **self.csv_kwargs)

    def save(self, df):
        df.to_csv(self.path, **self.csv_kwargs)
