from typing import Union

import pandas as pd
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, median_absolute_error, \
    r2_score

import numpy as np


class RegressionQualityMetrics:
    lbl_explained_variance_score = 'explained_variance_score'
    lbl_mean_absolute_error = 'mean_absolute_error'
    lbl_mean_squared_error = 'mean_squared_error'
    lbl_median_absolute_error = 'median_absolute_error'
    lbl_r2_score = 'r2_score'
    lbl_mape = 'mape'

    @staticmethod
    def explained_variance_score(y_true: pd.Series, y_pred: pd.Series) -> float:
        return explained_variance_score(y_true, y_pred)

    @staticmethod
    def mean_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
        return mean_absolute_error(y_true, y_pred)

    @staticmethod
    def mean_squared_error(y_true: pd.Series, y_pred: pd.Series) -> float:
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def median_absolute_error(y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.median(np.abs(y_pred - y_true)))

    @staticmethod
    def r2_score(y_true: pd.Series, y_pred: pd.Series) -> float:
        return r2_score(y_true, y_pred)

    @staticmethod
    def mape(y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.mean(np.abs((y_true - y_pred) / y_true)))
