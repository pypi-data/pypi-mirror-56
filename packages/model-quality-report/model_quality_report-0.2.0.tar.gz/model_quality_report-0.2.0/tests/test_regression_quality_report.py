import unittest

import pandas as pd
from sklearn import linear_model

from model_quality_report.quality_metrics import RegressionQualityMetrics
from model_quality_report.random_data_splitter import RandomDataSplitter
from model_quality_report.regression_quality_report import RegressionQualityReport


class TestRegressionQualityReport(unittest.TestCase):

    def setUp(self):
        self.X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20], 'b': [3, 5, 7, 10, 15, 30]})
        self.y = pd.Series([3, 6, 8, 10, 12, 30])
        self.model = linear_model.LinearRegression()
        self.test_size = 0.5
        self.splitter = RandomDataSplitter(test_size=self.test_size)

    def test_calculate_metrics(self):
        y_true = pd.Series([3, -0.5, 2, 7])
        y_pred = pd.Series([2.5, 0.0, 2, 8])

        metrics = RegressionQualityReport._calculate_quality_metrics(y_true, y_pred)
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

    def test_splitting_returns_training_and_test_data(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y)[0]
        self.assertIsNotNone(X_train)
        self.assertIsNotNone(X_test)
        self.assertIsNotNone(y_train)
        self.assertIsNotNone(y_test)

        self.assertAlmostEqual(X_train.shape[0] / self.X.shape[0], 1 - self.test_size)
        self.assertAlmostEqual(y_train.shape[0] / self.X.shape[0], 1 - self.test_size)
        self.assertListEqual(list(X_train.index), list(y_train.index))

        self.assertAlmostEqual(X_test.shape[0] / self.X.shape[0], self.test_size)
        self.assertAlmostEqual(y_test.shape[0] / self.X.shape[0], self.test_size)
        self.assertListEqual(list(X_test.index), list(y_test.index))

    def test_splitting_fails_and_returns_error(self):
        wrong_splitter = RandomDataSplitter(test_size=10)
        quality_report = RegressionQualityReport(self.model, wrong_splitter)
        quality_report._split_data_for_quality_assessment(self.X, self.y)

        self.assertTrue('Split failed' in quality_report._errors.to_string())

    def test_fit_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y)[0]
        quality_report._fit(X_train, y_train)

        self.assertTrue(quality_report._errors.is_empty())

    def test_quality_report_contains_error_if_fit_attribute_is_not_present(self):
        quality_report = RegressionQualityReport('no_model_but_string', self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
        quality_report._fit(X_train, y_train)

        self.assertFalse(quality_report._errors.is_empty())
        self.assertTrue('fit' in quality_report._errors.to_string())

    def test_predict_does_not_create_error_when_proper_model_is_provided(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)
        X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
        quality_report._fit(X_train, y_train)
        prediction_result = quality_report._predict(X_test)

        self.assertTrue(quality_report._errors.is_empty())
        self.assertIsInstance(prediction_result, pd.Series)
        self.assertTrue(len(prediction_result), len(y_train))

    def test_quality_report_contains_error_if_fit_and_predict_attribute_are_not_present(self):
        for model in [None, 'no_model_but_string']:
            quality_report = RegressionQualityReport(model, self.splitter)
            X_train, X_test, y_train, y_test = quality_report._split_data_for_quality_assessment(self.X, self.y, )[0]
            quality_report._fit(X_train, y_train)
            prediction_result = quality_report._predict(X_test)

            self.assertFalse(quality_report._errors.is_empty())
            self.assertTrue('fit' in quality_report._errors.to_string())
            self.assertTrue('predict' in quality_report._errors.to_string())
            self.assertIsInstance(prediction_result, pd.Series)

    def test_quality_report_is_properly_returned(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)

        result = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual([RegressionQualityReport.lbl_metrics, RegressionQualityReport.lbl_data],
                         list(result.keys()))
        self.assertTrue(isinstance(result[RegressionQualityReport.lbl_metrics], dict))
        self.assertTrue(isinstance(result[RegressionQualityReport.lbl_data], dict))

    def test_quality_report_metrics_are_floats(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)
        result = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        for metric_value in result[quality_report.lbl_metrics].values():
            self.assertIsInstance(metric_value, float)

    def test_quality_report_to_frame(self):
        quality_report = RegressionQualityReport(self.model, self.splitter)
        report = quality_report.create_quality_report_and_return_dict(self.X, self.y)

        report_df = RegressionQualityReport.metrics_to_frame(report)

        self.assertIsInstance(report_df, pd.DataFrame)
        self.assertEqual(set(report_df.columns), set([quality_report.lbl_metrics, quality_report.lbl_metric_value]))
