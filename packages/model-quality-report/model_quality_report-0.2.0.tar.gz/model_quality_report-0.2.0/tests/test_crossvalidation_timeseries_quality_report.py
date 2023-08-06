import unittest
from unittest.mock import patch
from typing import List

import pandas as pd
import numpy as np
from sklearn import linear_model

from model_quality_report.model_archetype import ModelArchetype
from model_quality_report.quality_metrics import RegressionQualityMetrics
from model_quality_report.random_data_splitter import RandomDataSplitter
from model_quality_report.crossvalidation_timeseries_quality_report import CrossValidationTimeSeriesQualityReport
from model_quality_report.temporal_data_splitter import TimeSeriesCrossValidationDataSplitter


class Test2DQualityReport(unittest.TestCase):

    def setUp(self):
        self.lbl_date = 'date'
        dates = pd.date_range('2019-01-01', periods=7)
        self.index = pd.DatetimeIndex(dates, name=self.lbl_date)
        self.X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20, 6],
                               'b': [3, 5, 7, 10, 15, 30, 22]},
                              index=self.index)
        self.y = pd.Series([3, 6, 8, 10, 12, 30, 23], index=self.index)
        self.model = LinearModelWrapper(exog_cols=['a', 'b'])
        self.maximum_horizon = 2
        self.splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=dates[2],
                                                              maximum_horizon=self.maximum_horizon)

    def test_calculate_metrics(self):
        y_true = pd.Series([3, -0.5, 2, 7])
        y_pred = pd.Series([2.5, 0.0, 2, 8])

        metrics = CrossValidationTimeSeriesQualityReport._calculate_quality_metrics(y_true, y_pred)
        result_dict = {
            RegressionQualityMetrics.lbl_explained_variance_score:
                RegressionQualityMetrics.explained_variance_score(y_true, y_pred),
            RegressionQualityMetrics.lbl_mape:
                RegressionQualityMetrics.mape(y_true, y_pred),
            RegressionQualityMetrics.lbl_mean_absolute_error:
                RegressionQualityMetrics.mean_absolute_error(y_true, y_pred),
            RegressionQualityMetrics.lbl_mean_squared_error:
                RegressionQualityMetrics.mean_squared_error(y_true, y_pred),
            RegressionQualityMetrics.lbl_median_absolute_error:
                RegressionQualityMetrics.median_absolute_error(y_true, y_pred),
            RegressionQualityMetrics.lbl_r2_score:
                RegressionQualityMetrics.r2_score(y_true, y_pred)
        }

        self.assertTrue(isinstance(metrics, dict))
        self.assertDictEqual(metrics, result_dict)

    def test_splitting_fails_and_returns_error(self):
        wrong_splitter = RandomDataSplitter(test_size=10)
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, wrong_splitter)
        quality_report._split_data_for_quality_assessment(self.X, self.y)

        self.assertTrue('Split failed' in quality_report._errors.to_string())

    def test_fit_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y)[0]
        quality_report._fit(X_train, y_train)

        self.assertTrue(quality_report._errors.is_empty())

    def test_quality_report_contains_error_if_fit_attribute_is_not_present(self):
        quality_report = CrossValidationTimeSeriesQualityReport('no_model_but_string', self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
        quality_report._fit(X_train, y_train)

        self.assertFalse(quality_report._errors.is_empty())
        self.assertTrue('fit' in quality_report._errors.to_string())

    def test_predict_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
        quality_report._fit(X_train, y_train)
        prediction_result = quality_report._predict(X_test)

        self.assertTrue(quality_report._errors.is_empty())
        self.assertIsInstance(prediction_result, pd.Series)
        self.assertTrue(len(prediction_result), len(y_train))

    def test_error_when_test_predict_not_aligned(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)

        def _convert_list_of_data_to_pandas(data, name):
            df_list = [pd.DataFrame({name: df, quality_report.lbl_horizon: np.arange(df.shape[0])}) for df in data]
            return (pd.concat(df_list)
                    .set_index(quality_report.lbl_horizon, append=True)
                    .pipe(lambda x: x.sort_values(by=x.columns[0])))

        quality_report._convert_list_of_data_to_pandas = _convert_list_of_data_to_pandas

        result = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        self.assertEqual(result, dict())
        self.assertTrue('not aligned' in quality_report.get_errors().to_string())

    def test_quality_report_contains_error_if_fit_and_predict_attribute_are_not_present(self):
        for model in [None, 'no_model_but_string']:
            quality_report = CrossValidationTimeSeriesQualityReport(model, self.splitter)
            X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
            quality_report._fit(X_train, y_train)
            prediction_result = quality_report._predict(X_test)

            self.assertFalse(quality_report._errors.is_empty())
            self.assertTrue('fit' in quality_report._errors.to_string())
            self.assertTrue('predict' in quality_report._errors.to_string())
            self.assertIsInstance(prediction_result, pd.Series)

    def test_quality_report_is_properly_returned(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)

        result = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual([CrossValidationTimeSeriesQualityReport.lbl_metrics,
                          CrossValidationTimeSeriesQualityReport.lbl_data],
                         list(result.keys()))
        self.assertTrue(isinstance(result[CrossValidationTimeSeriesQualityReport.lbl_metrics], dict))
        self.assertTrue(isinstance(result[CrossValidationTimeSeriesQualityReport.lbl_data], dict))

    def test_quality_report_metrics_are_ndarrays(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        result = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        for metric_value in result[quality_report.lbl_metrics].values():
            self.assertIsInstance(metric_value, dict)
            self.assertEqual(len(metric_value), self.maximum_horizon)

    def test_quality_report_to_frame(self):
        quality_report = CrossValidationTimeSeriesQualityReport(self.model, self.splitter)
        report = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        report_df = CrossValidationTimeSeriesQualityReport.metrics_to_frame(report)

        self.assertIsInstance(report_df, pd.DataFrame)
        self.assertEqual(set(report_df.columns),
                         {quality_report.lbl_metrics, quality_report.lbl_metric_value, quality_report.lbl_horizon})


class LinearModelWrapper(ModelArchetype):

    def __init__(self, exog_cols: List[str]):
        self._exog_cols = exog_cols
        self.model = linear_model.LinearRegression()

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.model.fit(X_train[self._exog_cols], y_train)

    def predict(self, X_test: pd.DataFrame):
        return pd.Series(self.model.predict(X_test[self._exog_cols]), index=X_test.index)
