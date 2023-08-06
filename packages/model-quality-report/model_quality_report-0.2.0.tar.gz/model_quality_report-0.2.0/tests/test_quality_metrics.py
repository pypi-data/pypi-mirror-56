import unittest
import numpy as np
import pandas as pd

from sklearn.metrics import explained_variance_score, mean_squared_error, mean_absolute_error, \
    median_absolute_error, r2_score

from model_quality_report.quality_metrics import RegressionQualityMetrics


class TestQualityMetrics(unittest.TestCase):

    def test_explained_variance_score(self):
        y_true = pd.Series([3, -0.5, 2, 7])
        y_pred = pd.Series([2.5, 0.0, 2, 8])
        qm = RegressionQualityMetrics()

        self.assertEqual(qm.explained_variance_score(y_true, y_pred), explained_variance_score(y_true, y_pred))
        self.assertEqual(qm.mean_squared_error(y_true, y_pred), mean_squared_error(y_true, y_pred))
        self.assertEqual(qm.mean_absolute_error(y_true, y_pred), mean_absolute_error(y_true, y_pred))
        self.assertEqual(qm.median_absolute_error(y_true, y_pred), np.median(np.abs(y_pred - y_true)))
        self.assertEqual(qm.r2_score(y_true, y_pred), r2_score(y_true, y_pred))
        self.assertEqual(qm.mape(y_true, y_pred), np.mean(np.abs((y_true - y_pred) / y_true)))
