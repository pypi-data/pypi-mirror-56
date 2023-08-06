import abc
import pandas as pd


class ModelArchetype(metaclass=abc.ABCMeta):
    """
    Base metaclass for model provided to quality report library. It is basically used to provide type hints.

    """

    @abc.abstractmethod
    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Each model passed to quality report must have a fit function
        """

    @abc.abstractmethod
    def predict(self, X_test: pd.DataFrame):
        """
        Each model passed to quality report must have a predict function
        """
