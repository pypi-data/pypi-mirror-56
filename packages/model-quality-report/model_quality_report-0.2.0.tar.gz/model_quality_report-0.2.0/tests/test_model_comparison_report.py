import unittest
from collections import OrderedDict
from typing import List

import pandas as pd
from sklearn import linear_model

from model_quality_report.crossvalidation_timeseries_quality_report import CrossValidationTimeSeriesQualityReport
from model_quality_report.model_archetype import ModelArchetype
from model_quality_report.model_comparison_report import ModelComparisonReport
from model_quality_report.random_data_splitter import RandomDataSplitter
from model_quality_report.regression_quality_report import RegressionQualityReport
from model_quality_report.temporal_data_splitter import TimeSeriesCrossValidationDataSplitter


class TestCrossValidationModelComparisonReport(unittest.TestCase):

    def setUp(self):
        self.lbl_date = 'date'
        self.lbl_model = 'model'
        self.lbl_yname = 'y name'
        self.lbl_model_name1 = 'Model 1'
        self.lbl_model_name2 = 'Model 2'
        dates = pd.date_range('2019-01-01', periods=8)
        self.index = pd.DatetimeIndex(dates, name=self.lbl_date)
        self.X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20, 6, 11],
                               'b': [3, 5, 7, 10, 15, 30, 22, 48],
                               'c': [8, 1, 0, 17, 11, 20, 2, 4]},
                              index=self.index)
        y1 = pd.Series([3, 6, 8, 10, 12, 30, 23, 5], name='y1', index=self.index)
        y2 = pd.Series([3, 6, 8, 10, 12, 30, 23, 5], name='y2', index=self.index)
        model1 = LinearModelWrapper(exog_cols=['a', 'b'])
        model2 = LinearModelWrapper(exog_cols=['b', 'c'])
        self.maximum_horizon = 3
        self.quality_report = CrossValidationTimeSeriesQualityReport
        self.splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=dates[2],
                                                              maximum_horizon=self.maximum_horizon)
        self.models_and_data = [(model1, self.X, y1,
                                 OrderedDict({self.lbl_model: self.lbl_model_name1, self.lbl_yname: y1.name})),
                                (model2, self.X, y2,
                                 OrderedDict({self.lbl_model: self.lbl_model_name2, self.lbl_yname: y2.name})),
                                (model2, self.X, y1,
                                 OrderedDict({self.lbl_model: self.lbl_model_name2, self.lbl_yname: y1.name}))]

    def test_basic_model_comparison_results(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()

        self.assertIsInstance(result, dict)

        for _, _, y, experiment_id in self.models_and_data:
            self.assertEqual(y.name, experiment_id[self.lbl_yname])

    def test_report_type(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()

        self.assertIsInstance(result, dict)

    def test_report_conversion(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()
        result_df = quality_report.to_frame(result)

        self.assertIsInstance(result_df, pd.DataFrame)

    def test_error_unequal_experiment_keys(self):
        models_and_data = [(None, None, None, OrderedDict({'a': 1, 'b': 2})),
                           (None, None, None, OrderedDict({'b': 1, 'a': 2}))]
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, models_and_data)

        with self.assertRaises(RuntimeError):
            quality_report._get_experiment_keys(models_and_data)



class TestRegressionModelComparisonReport(unittest.TestCase):

    def setUp(self):
        self.X = pd.DataFrame({'a': [1, 2, 4, 5, 7, 20], 'b': [3, 5, 7, 10, 15, 30]})
        self.y = pd.Series([3, 6, 8, 10, 12, 30], name='y')
        self.model = linear_model.LinearRegression()
        self.test_size = 0.5
        self.splitter = RandomDataSplitter(test_size=self.test_size)
        self.quality_report = RegressionQualityReport
        self.lbl_model = 'model'
        self.lbl_exog = 'exogenous'
        self.lbl_model_name = 'Model'
        self.exog_cols1 = ['a', 'b']
        self.exog_cols2 = ['a']
        self.exog_cols3 = ['b']

        self.models_and_data = [(self.model, self.X[self.exog_cols1], self.y,
                                 OrderedDict({self.lbl_model: self.lbl_model_name,
                                              self.lbl_exog: ', '.join(self.exog_cols1)})),
                                (self.model, self.X[self.exog_cols2], self.y,
                                 OrderedDict({self.lbl_model: self.lbl_model_name,
                                              self.lbl_exog: ', '.join(self.exog_cols2)})),
                                (self.model, self.X[self.exog_cols3], self.y,
                                 OrderedDict({self.lbl_model: self.lbl_model_name,
                                              self.lbl_exog: ', '.join(self.exog_cols3)}))]

    def test_basic_model_comparison_results(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()

        self.assertIsInstance(result, dict)

        for _, X, _, experiment_id in self.models_and_data:
            self.assertEqual(', '.join(X.columns), experiment_id[self.lbl_exog])

    def test_report_type(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()

        self.assertIsInstance(result, dict)

    def test_report_conversion(self):
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, self.models_and_data)
        result = quality_report.create_quality_report_and_return_dict()
        result_df = quality_report.to_frame(result)

        self.assertIsInstance(result_df, pd.DataFrame)

    def test_error_unequal_experiment_keys(self):
        models_and_data = [(None, None, None, OrderedDict({'a': 1, 'b': 2})),
                           (None, None, None, OrderedDict({'b': 1, 'a': 2}))]
        quality_report = ModelComparisonReport(self.splitter, self.quality_report, models_and_data)
        with self.assertRaises(RuntimeError):
            quality_report._get_experiment_keys(models_and_data)


class LinearModelWrapper(ModelArchetype):

    def __init__(self, exog_cols: List[str]):
        self._exog_cols = exog_cols
        self.model = linear_model.LinearRegression()

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.model.fit(X_train[self._exog_cols], y_train)

    def predict(self, X_test: pd.DataFrame):
        return self.model.predict(X_test[self._exog_cols])
