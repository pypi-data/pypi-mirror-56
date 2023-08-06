from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

from model_quality_report.data_splitter_archetype import DataSplitterArchetype


class RandomDataSplitter(DataSplitterArchetype):
    """
    Splits data randomly using the sklearn model_selection.train_test_split
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def split(self, X: pd.DataFrame, y: pd.Series) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        return [train_test_split(X, y, **self.kwargs)]

    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> list:

        validation_error = list()
        try:
            train_test_split(X, y, **self.kwargs)
        except Exception as e:
            validation_error.append(str(e))

        return validation_error

    def get_parameters(self):
        return self.kwargs
