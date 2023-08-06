import abc
import pandas as pd
from typing import List, Tuple


class DataSplitterArchetype(metaclass=abc.ABCMeta):
    """
    Base metaclass for splitting data.
    """

    @abc.abstractmethod
    def split(self, X: pd.DataFrame, y: pd.Series) \
            -> List[Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
        """
        Given a data frame containing features and a series containing corresponding targets, a split into training
        and test data is performed, which are subsequently returned.
        :return: X_train, X_test, y_train, y_test
        """

    @abc.abstractmethod
    def validate_parameters(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """
        A splitting strategy can depend on various parameters, like e.g. the size of the test set or a date  after which
        all data are declared as test data. This functions validates that data and parameters fit to each other.
        :return: error
        """

    @abc.abstractmethod
    def get_parameters(self) -> dict:
        """
        Returns parameters of Splitter as dict
        :return: dict of parameters
        """
